// Typewriter placeholder for the formula field (same idea as ELAYA SMILES):
// types an example, holds it, deletes it, moves to the next one. While it types,
// the field border lights up with the SmilX blue→green gradient (stronger as the
// word grows). It pauses whenever the user focuses the field or it has a value.
(() => {
  const doc = document;
  if (window.__smilxTW) return;           // one loop per page load; survives reruns
  window.__smilxTW = true;

  const TYPE = 110, DELETE = 55, HOLD = 1400, GAP = 450;
  const st = { i: 0, pos: 0, phase: 'type' };
  let base = null;

  const input = () => doc.querySelector('.st-key-formula_input input');
  const frame = () => doc.querySelector('.st-key-formula_input [data-testid="stTextInputRootElement"]');
  const examples = () => (window.__smilxExamples && window.__smilxExamples.length) ? window.__smilxExamples : ['C6H6'];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function idle(el, f) {
    if (f) { f.classList.remove('smx-typing'); f.style.removeProperty('--smx-p'); }
    if (el && base !== null && el.placeholder !== base) el.placeholder = base;
    st.pos = 0; st.phase = 'type';
  }

  function tick() {
    const el = input(), f = frame();
    if (!el || !f) { setTimeout(tick, 700); return; }                 // another page is open
    if (base === null) base = el.getAttribute('placeholder') || '';
    if (el.value || doc.activeElement === el || reduced) { idle(el, f); setTimeout(tick, 500); return; }

    const list = examples();
    const word = list[st.i % list.length];
    f.classList.add('smx-typing');

    if (st.phase === 'type') {
      st.pos += 1;
      el.placeholder = word.slice(0, st.pos) + '|';
      f.style.setProperty('--smx-p', (st.pos / word.length).toFixed(2));
      if (st.pos >= word.length) { st.phase = 'del'; el.placeholder = word; setTimeout(tick, HOLD); return; }
      setTimeout(tick, TYPE); return;
    }
    // deleting
    st.pos -= 1;
    el.placeholder = word.slice(0, Math.max(st.pos, 0)) + '|';
    f.style.setProperty('--smx-p', (Math.max(st.pos, 0) / word.length).toFixed(2));
    if (st.pos <= 0) {
      st.phase = 'type'; st.i += 1;
      el.placeholder = '|';
      setTimeout(tick, GAP); return;
    }
    setTimeout(tick, DELETE);
  }
  setTimeout(tick, 600);
})();
