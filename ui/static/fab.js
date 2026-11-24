(() => {
  const doc = document;
  // Built with DOM calls: Streamlit's sanitizer drops scripts whose strings contain tags
  function arrow() {
    const NS = 'http://www.w3.org/2000/svg';
    const svg = doc.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24'); svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor'); svg.setAttribute('stroke-width', '2.4');
    svg.setAttribute('stroke-linecap', 'round'); svg.setAttribute('stroke-linejoin', 'round');
    svg.setAttribute('aria-hidden', 'true');
    const path = doc.createElementNS(NS, 'path'); path.setAttribute('d', 'M12 5v14M5 12l7 7 7-7');
    svg.appendChild(path); return svg;
  }
  function scroller() {
    const c = [doc.querySelector('[data-testid="stMain"]'), doc.querySelector('[data-testid="stAppViewContainer"]'),
               doc.querySelector('.stApp'), doc.scrollingElement];
    for (const el of c) if (el && el.scrollHeight - el.clientHeight > 4 &&
        (el === doc.scrollingElement || /(auto|scroll)/.test(getComputedStyle(el).overflowY))) return el;
    return doc.scrollingElement;
  }
  let fab = doc.getElementById('smilx-fab');
  if (!fab) {
    fab = doc.createElement('button');
    fab.id = 'smilx-fab'; fab.type = 'button';
    const lbl = doc.createElement('span'); lbl.className = 'lbl'; lbl.textContent = 'Scroll down';
    fab.appendChild(arrow()); fab.appendChild(lbl);
    doc.body.appendChild(fab);
    fab.addEventListener('click', () => {
      const s = scroller(), vh = s.clientHeight;
      const smooth = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
      const mode = fab.dataset.mode;
      if (mode === 'top') { s.scrollTo({ top: 0, behavior: smooth }); return; }
      if (mode === 'results') {
        const anchor = doc.querySelector('.st-key-explorer-compact, .st-key-explorer, #smilx-res-bar');
        if (anchor) { s.scrollBy({ top: anchor.getBoundingClientRect().top - 72, behavior: smooth }); return; }
      }
      s.scrollBy({ top: vh * 0.75, behavior: smooth });
    });
  }
  function update() {
    const s = scroller();
    const vh = s.clientHeight, max = s.scrollHeight - vh, y = s.scrollTop;
    const bar = doc.querySelector('#smilx-res-bar');
    const resBelow = bar && bar.getBoundingClientRect().top > vh - 60;
    let mode = null;
    if (resBelow) mode = 'results';                          // results exist but are out of view
    else if (!bar && max > vh * 0.6 && y < 40) mode = 'down'; // long page (no grid on screen), still at the top
    else if (y > vh * 1.2) mode = 'top';                      // far down: offer a way back
    fab.classList.toggle('show', !!mode);
    if (!mode) return;
    fab.classList.toggle('up', mode === 'top');
    fab.classList.toggle('down', mode !== 'top');
    fab.classList.toggle('pulse', mode === 'results');
    fab.dataset.mode = mode;
    const label = mode === 'top' ? 'Back to top' : (mode === 'results' ? 'See results' : 'Scroll down');
    const span = fab.querySelector('.lbl');
    if (span.textContent !== label) span.textContent = label;
    fab.setAttribute('aria-label', label); fab.title = label;
  }
  if (!window.__smilxFab) {
    window.__smilxFab = true;
    // close the results ⋮ menu when clicking anywhere else or pressing Esc
    doc.addEventListener('click', (e) => {
      doc.querySelectorAll('details.rb-more[open]').forEach(d => { if (!d.contains(e.target)) d.removeAttribute('open'); });
    });
    doc.addEventListener('keydown', (e) => { if (e.key === 'Escape') doc.querySelectorAll('details.rb-more[open]').forEach(d => d.removeAttribute('open')); });
    doc.addEventListener('scroll', update, true);
    window.addEventListener('resize', update);
    setInterval(update, 700);
  }
  setTimeout(update, 50);
})();
