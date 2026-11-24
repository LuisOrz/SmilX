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
