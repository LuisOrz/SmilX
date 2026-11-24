(() => {
  if (window.smilxShowIsomer) return;
  const doc = document;
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const sub = (f) => esc(f).replace(/(\d+)/g, '<sub>$1</sub>');
  const pubchemCache = new Map();
  let state = { frame: null, id: 0, total: 0 };

  const root = doc.createElement('div');
  root.id = 'smx-modal';
  root.innerHTML = `
    <div class="smx-scrim" data-close></div>
    <div class="smx-dialog" role="dialog" aria-modal="true" aria-labelledby="smx-title">
      <header><div class="t"><div class="eyebrow2" id="smx-count"></div><h3 id="smx-title"></h3><div class="smi" id="smx-smi"></div></div>
        <button class="x" data-close aria-label="Close">&times;</button></header>
      <div class="smx-body"><div class="fig" id="smx-fig"></div><div class="info" id="smx-info"></div></div>
      <footer>
        <button class="b" id="smx-prev" aria-label="Previous isomer">&larr; Previous</button>
        <button class="b" id="smx-next" aria-label="Next isomer">Next &rarr;</button>
        <span class="sp"></span>
        <span class="hide-sm note"><kbd>&larr;</kbd> <kbd>&rarr;</kbd> navigate &middot; <kbd>Esc</kbd> close</span>
        <button class="b" id="smx-copy">Copy SMILES</button>
        <a class="b fill" id="smx-pc" target="_blank" rel="noopener">PubChem &#8599;</a>
      </footer>
    </div>`;
  doc.body.appendChild(root);

  const $ = (id) => doc.getElementById(id);
  function close() { root.classList.remove('open'); }
  root.addEventListener('click', (e) => { if (e.target.hasAttribute('data-close')) close(); });
  function onKey(key) {
    if (!root.classList.contains('open')) return false;
    if (key === 'Escape') close();
    else if (key === 'ArrowRight') go(1);
    else if (key === 'ArrowLeft') go(-1);
    else return false;
    return true;
  }
  window.smilxModalKey = onKey;
  doc.addEventListener('keydown', (e) => { if (onKey(e.key)) e.preventDefault(); });
  function go(step) {
    if (!state.frame || !state.total) return;
    let n = state.id + step;
    if (n < 1) n = state.total; if (n > state.total) n = 1;
    try { state.frame.smilxOpen(n); } catch (err) {}
  }
  $('smx-prev').onclick = () => go(-1);
  $('smx-next').onclick = () => go(1);
  $('smx-copy').onclick = async () => {
    const t = $('smx-smi').textContent;
    try { await navigator.clipboard.writeText(t); $('smx-copy').textContent = 'Copied ✓'; }
    catch (e) { $('smx-copy').textContent = 'Copy failed'; }
    setTimeout(() => { $('smx-copy').textContent = 'Copy SMILES'; }, 1400);
  };

  function row(k, v, cls) { return `<dt>${k}</dt><dd class="${cls||''}">${v}</dd>`; }

  function pubchem(key) {
    const box = $('smx-pubchem');
    if (!key) { box.innerHTML = '<span class="unk">No InChIKey</span>'; return; }
    const show = (r) => {
      if (!$('smx-pubchem') || $('smx-pubchem').dataset.key !== key) return;
      if (r && r.cid) {
        $('smx-title').textContent = r.title || $('smx-title').textContent;
        box.innerHTML = `<span class="known">Known compound in PubChem</span><br>
          <b>${esc(r.title || '')}</b>${r.iupac ? `<br>IUPAC name: ${esc(r.iupac)}` : ''}<br>
          CID <a href="https://pubchem.ncbi.nlm.nih.gov/compound/${r.cid}" target="_blank" rel="noopener">${r.cid}</a>`;
      } else if (r && r.notfound) {
        box.innerHTML = '<span class="unk">No PubChem record</span><br>No compound with this exact InChIKey is registered in PubChem.';
      } else {
        box.innerHTML = '<span class="unk">PubChem unavailable</span><br>Could not reach PubChem right now. Use the PubChem button to search manually.';
      }
    };
    if (pubchemCache.has(key)) { show(pubchemCache.get(key)); return; }
    box.innerHTML = 'Searching PubChem by InChIKey…';
    fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/${encodeURIComponent(key)}/property/Title,IUPACName/JSON`)
      .then(r => r.status === 404 ? { notfound: true } : (r.ok ? r.json() : Promise.reject(r.status)))
      .then(j => {
        if (j.notfound) return j;
        const p = j && j.PropertyTable && j.PropertyTable.Properties && j.PropertyTable.Properties[0];
        return p ? { cid: p.CID, title: p.Title, iupac: p.IUPACName } : { notfound: true };
      })
      .then(r => { pubchemCache.set(key, r); show(r); })
      .catch(() => show(null));
  }

  window.smilxShowIsomer = function (payload) {
    const p = payload.p || {};
    state = { frame: payload.frame, id: Number(payload.id), total: Number(payload.total) };
    $('smx-count').textContent = `Isomer ${state.id} of ${state.total}`;
    $('smx-title').innerHTML = sub(p.formula || '');
    $('smx-smi').textContent = p.smiles || '';
    $('smx-fig').innerHTML = (payload.svg || '<span class="note">2D depiction unavailable</span>') + '<span class="cap">2D · RDKit</span>';
    $('smx-pc').href = p.inchikey ? `https://pubchem.ncbi.nlm.nih.gov/#query=${encodeURIComponent(p.inchikey)}`
                                  : `https://pubchem.ncbi.nlm.nih.gov/#query=${encodeURIComponent(p.smiles || '')}`;
    const rings = p.rings ? `${p.rings} (${(p.ring_sizes || []).map(s => s + '-membered').join(', ')})` : '0';
    const stereo = (p.stereoisomers == null) ? '—' : p.stereoisomers;
    const groups = (p.groups && p.groups.length) ? p.groups.map(g => `<span>${esc(g)}</span>`).join('')
                                                 : '<span class="none">None detected (saturated hydrocarbon skeleton)</span>';
    const flags = (p.flags || []).map(f => `<div class="flag">${esc(f)}</div>`).join('');
    $('smx-info').innerHTML = `
      <section><h4>Known compound?</h4><div class="pc" id="smx-pubchem" data-key="${esc(p.inchikey)}"></div></section>
      <section><h4>Functional groups</h4><div class="chips2">${groups}</div>${flags}</section>
      <section><h4>Structure</h4><dl>
        ${row('Rings', rings)}
        ${row('Double bonds', p.double_bonds)}
        ${row('Triple bonds', p.triple_bonds)}
        ${row('Stereocenters', p.stereocenters)}
        ${row('Stereogenic C=C / C=N', p.stereo_double_bonds)}
        ${row('Possible stereoisomers', stereo)}
      </dl><p class="note">SmilX lists constitutional isomers; stereoisomers of each are not enumerated separately.</p></section>
      <section><h4>Computed properties</h4><dl>
        ${row('Molecular weight', p.mw + ' g/mol')}
        ${row('Monoisotopic mass', p.exact_mass + ' Da')}
        ${row('H-bond donors / acceptors', p.hbd + ' / ' + p.hba)}
        ${row('Rotatable bonds', p.rot_bonds)}
        ${row('TPSA', p.tpsa + ' Å²')}
        ${row('logP (Crippen, estimated)', p.logp)}
        ${row('Fraction sp³ carbons', p.fsp3)}
      </dl></section>
      <section><h4>Identifiers</h4><dl>
        ${row('InChIKey', esc(p.inchikey), 'mono')}
        ${row('InChI', esc(p.inchi), 'mono')}
      </dl></section>
      <p class="note">Computed with RDKit from the 2D structure. Known-compound data comes from PubChem (NCBI), matched by InChIKey.</p>`;
    root.classList.add('open');
    setTimeout(() => { try { window.focus(); $('smx-next').focus({ preventScroll: true }); } catch (e) {} }, 0);
    pubchem(p.inchikey);
  };
})();
