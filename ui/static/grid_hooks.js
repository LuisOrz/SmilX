window.SMILX = __DATA__;
window.smilxOpen = function (id) {
  id = Number(id);
  smilxHintDone();
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
  const img = e.target.closest && (e.target.closest('.data-img') || e.target.closest('.smx-zoom'));
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
  if (!q) {   // reset: back to Text search with an empty query
    const t = Array.from(document.querySelectorAll('#mols2grid .m2g-search-options .m2g-option')).find(o => o.textContent.trim() === 'Text');
    if (t) t.click();
    const b = document.querySelector('#mols2grid .m2g-searchbar');
    if (b) { b.value = ''; if (window.jQuery) jQuery(b).trigger({ type: 'keyup', target: b }); }
    return;
  }
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

// ── Zoom affordance ───────────────────────────────────────────────────────
// Every card gets a small magnifier; the first card pulses with a
// "Click to zoom" label until the user opens a zoom once (remembered).
const ZOOM_ICON = 'M10.5 4a6.5 6.5 0 0 1 5.2 10.4l4.2 4.2-1.4 1.4-4.2-4.2A6.5 6.5 0 1 1 10.5 4zm0 2a4.5 4.5 0 1 0 0 9 4.5 4.5 0 0 0 0-9zM9.5 8h2v1.5H13v2h-1.5V13h-2v-1.5H8v-2h1.5z';
function hintSeen() { try { return localStorage.getItem('smilxZoomHint') === '1'; } catch (e) { return false; } }
function smilxHintDone() {
  try { localStorage.setItem('smilxZoomHint', '1'); } catch (e) {}
  document.querySelectorAll('.m2g-cell.smx-hint').forEach(c => c.classList.remove('smx-hint'));
}
function decorate() {
  const cells = document.querySelectorAll('#mols2grid .m2g-cell:not(.m2g-phantom)');
  cells.forEach(cell => {
    if (cell.querySelector('.smx-zoom')) return;
    const b = document.createElement('span');
    b.className = 'smx-zoom'; b.title = 'Zoom in'; b.setAttribute('role', 'button'); b.setAttribute('aria-label', 'Zoom in');
    const NS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(NS, 'svg'); svg.setAttribute('viewBox', '0 0 24 24'); svg.setAttribute('width', '16'); svg.setAttribute('height', '16');
    const path = document.createElementNS(NS, 'path'); path.setAttribute('d', ZOOM_ICON); path.setAttribute('fill', 'currentColor');
    svg.appendChild(path); b.appendChild(svg); cell.appendChild(b);
  });
  if (!hintSeen() && cells.length && !document.querySelector('.m2g-cell.smx-hint')) {
    cells[0].classList.add('smx-hint');
    if (!cells[0].querySelector('.smx-hint-label')) {
      const l = document.createElement('span'); l.className = 'smx-hint-label'; l.textContent = 'Click to zoom';
      cells[0].appendChild(l);
    }
  }
}
(function watch() {
  const list = document.querySelector('#mols2grid .m2g-list');
  if (!list) return setTimeout(watch, 150);
  decorate();
  new MutationObserver(() => decorate()).observe(list, { childList: true, subtree: false });
})();
