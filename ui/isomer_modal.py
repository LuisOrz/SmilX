"""
Isomer zoom dialog
------------------
Lives in the main Streamlit document (not inside the grid iframe) so it can
float over the page. The grid iframe calls `window.parent.smilxShowIsomer()`
with the RDKit-computed info of one isomer and a large SVG drawn by RDKit.js.
Known-compound data comes from PubChem (PUG-REST, queried by InChIKey).
"""

MODAL_CSS = r"""
<style>
#smx-modal { position: fixed; inset: 0; z-index: 1000000; display: none; }
#smx-modal.open { display: block; }
#smx-modal .smx-scrim { position: absolute; inset: 0; background: rgba(4,6,12,.62); backdrop-filter: blur(3px); animation: smxFade .18s ease both; }
#smx-modal .smx-dialog {
    position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%);
    width: min(1060px, 94vw); max-height: min(780px, 90vh); display: flex; flex-direction: column;
    background: var(--surface-3, #20263a); color: var(--on, #e6e8f0); border-radius: 28px; overflow: hidden;
    box-shadow: 0 24px 48px rgba(0,0,0,.55), 0 0 0 1px rgba(173,198,255,.10); animation: smxPop .22s cubic-bezier(.2,0,0,1) both;
    font-family: 'Outfit', system-ui, sans-serif;
}
@keyframes smxFade { from { opacity: 0; } to { opacity: 1; } }
@keyframes smxPop { from { opacity: 0; transform: translate(-50%,-48%) scale(.97); } to { opacity: 1; transform: translate(-50%,-50%); } }
#smx-modal header { display: flex; align-items: flex-start; gap: 16px; padding: 20px 22px 14px 26px; }
#smx-modal header .t { flex: 1; min-width: 0; }
#smx-modal .eyebrow2 { font: 600 12px 'IBM Plex Mono', monospace; letter-spacing: .08em; text-transform: uppercase; color: var(--primary, #adc6ff); }
#smx-modal h3 { margin: 4px 0 4px; font: 700 1.45rem 'Outfit', sans-serif; color: var(--on, #e6e8f0); line-height: 1.2; }
#smx-modal h3 sub { font-size: .65em; }
#smx-modal .smi { font: 500 13px 'IBM Plex Mono', monospace; color: var(--on-2, #b8bfd2); word-break: break-all; }
#smx-modal .x { flex: 0 0 auto; width: 40px; height: 40px; border-radius: 50%; border: none; background: transparent; color: var(--on-2, #b8bfd2); font-size: 22px; cursor: pointer; }
#smx-modal .x:hover { background: rgba(230,232,240,.08); color: var(--on, #e6e8f0); }
#smx-modal .smx-body { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr); gap: 18px; padding: 0 22px 8px 26px; min-height: 0; flex: 1; }
#smx-modal .fig { background: #fff; border-radius: 18px; display: grid; place-items: center; min-height: 300px; padding: 10px; position: relative; }
#smx-modal .fig svg { width: 100%; height: auto; max-height: 56vh; }
#smx-modal .fig .cap { position: absolute; left: 12px; bottom: 10px; font: 500 11px 'IBM Plex Mono', monospace; color: #5a6275; }
#smx-modal .info { overflow-y: auto; padding-right: 6px; max-height: calc(min(780px, 90vh) - 190px); }
#smx-modal .info::-webkit-scrollbar { width: 8px; } #smx-modal .info::-webkit-scrollbar-thumb { background: #3a4258; border-radius: 8px; }
#smx-modal section { background: var(--surface-2, #1a1f2c); border-radius: 16px; padding: 12px 14px; margin-bottom: 10px; }
#smx-modal section h4 { margin: 0 0 8px; font: 600 12px 'Outfit', sans-serif; letter-spacing: .08em; text-transform: uppercase; color: var(--on-3, #8c94ab); }
#smx-modal dl { display: grid; grid-template-columns: auto 1fr; gap: 5px 14px; margin: 0; font-size: 14px; }
#smx-modal dt { color: var(--on-3, #8c94ab); }
#smx-modal dd { margin: 0; color: var(--on, #e6e8f0); font-weight: 500; text-align: right; font-variant-numeric: tabular-nums; }
#smx-modal dd.mono, #smx-modal .mono { font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; word-break: break-all; text-align: left; }
#smx-modal .chips2 { display: flex; flex-wrap: wrap; gap: 6px; }
#smx-modal .chips2 span { font-size: 13px; font-weight: 600; padding: 4px 10px; border-radius: 8px; background: var(--primary-c, #233a6b); color: var(--on-primary-c, #d9e2ff); }
#smx-modal .chips2 span.none { background: transparent; color: var(--on-3, #8c94ab); font-weight: 500; padding-left: 0; }
#smx-modal .flag { font-size: 13.5px; color: #ffe0a8; background: var(--warn-c, #4a3510); padding: 7px 10px; border-radius: 10px; margin-top: 6px; }
#smx-modal .pc { font-size: 14px; color: var(--on-2, #b8bfd2); line-height: 1.5; }
#smx-modal .pc b { color: var(--on, #e6e8f0); }
#smx-modal .pc .known { color: var(--on-green-c, #a8f2cc); background: var(--green-c, #133d2b); display: inline-block; padding: 3px 9px; border-radius: 999px; font-weight: 600; font-size: 12.5px; margin-bottom: 6px; }
#smx-modal .pc .unk { color: var(--on-2, #b8bfd2); background: rgba(230,232,240,.08); display: inline-block; padding: 3px 9px; border-radius: 999px; font-weight: 600; font-size: 12.5px; margin-bottom: 6px; }
#smx-modal .note { font-size: 12px; color: var(--on-3, #8c94ab); margin: 4px 2px 6px; line-height: 1.5; }
#smx-modal footer { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; padding: 12px 22px 18px 26px; border-top: 1px solid rgba(230,232,240,.08); }
#smx-modal footer .sp { flex: 1; }
#smx-modal .b { height: 40px; padding: 0 16px; border-radius: 999px; font: 600 14px 'Outfit', sans-serif; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; text-decoration: none;
    border: 1px solid var(--outline, #4a5470); background: transparent; color: var(--primary, #adc6ff); transition: background .15s, border-color .15s; }
#smx-modal .b:hover { background: rgba(173,198,255,.08); border-color: var(--primary, #adc6ff); }
#smx-modal .b.fill { background: var(--primary, #adc6ff); color: var(--on-primary, #0b2a63); border-color: transparent; }
#smx-modal .b.fill:hover { background: var(--primary-h, #c4d5ff); }
#smx-modal .b:disabled { opacity: .4; cursor: default; }
#smx-modal kbd { font: 500 11px 'IBM Plex Mono', monospace; color: var(--on-3, #8c94ab); border: 1px solid #3a4258; border-bottom-width: 2px; border-radius: 5px; padding: 0 5px; }
@media (max-width: 820px) {
    #smx-modal .smx-dialog { top: auto; bottom: 0; left: 0; transform: none; width: 100vw; max-height: 92vh; border-radius: 28px 28px 0 0; animation: smxUp .25s cubic-bezier(.2,0,0,1) both; }
    @keyframes smxUp { from { transform: translateY(30px); opacity: 0; } to { transform: none; opacity: 1; } }
    #smx-modal .smx-body { grid-template-columns: 1fr; overflow-y: auto; }
    #smx-modal .info { max-height: none; overflow: visible; }
    #smx-modal .fig { min-height: 220px; }
    #smx-modal .hide-sm { display: none; }
}
@media (prefers-reduced-motion: reduce) { #smx-modal .smx-dialog, #smx-modal .smx-scrim { animation: none; } }
</style>
"""

MODAL_JS = r"""
<script>
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
</script>
"""

# Injected into the grid iframe (mols2grid custom_header).
GRID_JS_TEMPLATE = r"""
<script>
window.SMILX = __DATA__;
window.smilxOpen = function (id) {
  id = Number(id);
  const p = (window.SMILX.props || {})[id];
  if (!p) return;
  let svg = '';
  try {
    if (window.RDKit) {
      const m = RDKit.get_mol(p.smiles);
      if (m) { svg = m.get_svg(560, 420); m.delete(); }
    }
  } catch (e) {}
  try {
    if (window.parent && window.parent.smilxShowIsomer) {
      window.parent.smilxShowIsomer({ id: id, total: window.SMILX.total, svg: svg, p: p, frame: window });
    }
  } catch (e) {}
};
// Click on a structure → open the zoom dialog (instead of toggling selection)
document.addEventListener('click', function (e) {
  const img = e.target.closest && e.target.closest('.data-img');
  if (!img) return;
  const cell = img.closest('.m2g-cell');
  const idEl = cell && cell.querySelector('.data-ID');
  if (!idEl) return;
  e.stopPropagation(); e.preventDefault();
  window.smilxOpen(idEl.textContent.trim());
}, true);
// Keys pressed while focus is still inside the grid → forward to the dialog
document.addEventListener('keydown', function (e) {
  try {
    if (window.parent.smilxModalKey && window.parent.smilxModalKey(e.key)) { e.preventDefault(); e.stopPropagation(); }
  } catch (err) {}
}, true);
// Clearer search labels and placeholders
window.smilxSmarts = function (q) {
  const opt = Array.from(document.querySelectorAll('#mols2grid .m2g-search-options .m2g-option'))
                   .find(o => o.textContent.trim() !== 'Text');
  if (opt) opt.click();
  const bar = document.querySelector('#mols2grid .m2g-searchbar');
  if (!bar) return;
  bar.value = q;
  if (window.jQuery) jQuery(bar).trigger({ type: 'keyup', target: bar });
  else bar.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
};
(function tweak() {
  const opts = document.querySelectorAll('#mols2grid .m2g-search-options .m2g-option');
  const bar = document.querySelector('#mols2grid .m2g-searchbar');
  if (!opts.length || !bar) return setTimeout(tweak, 150);
  opts.forEach(o => { if (o.textContent.trim() === 'SMARTS') { o.textContent = 'Substructure'; o.title = 'SMARTS substructure search: matching atoms are highlighted'; }
                      else { o.title = 'Matches the text of the ID or SMILES'; } });
  const ph = () => {
    const sel = document.querySelector('#mols2grid .m2g-search-options .m2g-option.sel');
    bar.placeholder = (sel && sel.textContent.trim() === 'Text') ? 'ID or SMILES…' : 'SMARTS, e.g. C=O';
  };
  ph(); opts.forEach(o => o.addEventListener('click', () => setTimeout(ph, 0)));
})();
</script>
"""
