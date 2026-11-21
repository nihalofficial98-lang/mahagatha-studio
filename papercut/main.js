// Mahagatha papercut pilot: EP4 first 54 s on the owner's real voice. Multi-colour cut paper, 12 fps characters, 24 fps camera.
import { PAL, canvas, piece, P, Pl, trace, fill, cut, cutTaper, inset, ellipsePoly, finishPaper, fillPaper, rnd } from './paper.js';
import { sawRow, crescentRows, swirl, rosette, plum, coin, dots, taper, cloudCut } from './motifs.js';
import { mul, T, R, S, put } from './rig.js';
import { PAPER, drawFig, CAST, skull, trident } from './figs.js';

const cv = document.getElementById('cv'), g = cv.getContext('2d'), W = 1920, H = 1080;
const WORDS = await (await fetch('words.json')).json();
const q = new URLSearchParams(location.search);
const L = {}; const once = (k, f) => L[k] || (L[k] = f());

// ---------- scenery pieces ----------
const band = (col, seed, amp = 40, h = 520) => once('band' + col + seed, () => piece([0, 0, 2300, h], g => {
  const pts = []; for (let x = 0; x <= 2300; x += 20) pts.push([x, amp + Math.sin(x * .007 + seed) * amp * .8 + Math.sin(x * .021 + seed * 2) * amp * .3]);
  pts.push([2300, h], [0, h]);
  fill(g, q => trace(q, Pl(pts, true, .5, seed)), col);
  crescentRows(g, 30, amp * 2 + 30, 2270, h - 60, 16, 3.4, 0, .7);
}, { ss: 1.2, seed }));
const mount = (col, seed, peak = 360, snow = true) => once('mt' + col + seed, () => piece([0, 0, 2300, 560], g => {
  const pts = [[0, 560]]; for (let x = 0; x <= 2300; x += 60) pts.push([x, 560 - peak * (.35 + .65 * Math.abs(Math.sin(x * .0043 + seed) * .7 + Math.sin(x * .0111 + seed * 3) * .3))]);
  pts.push([2300, 560]);
  fill(g, q => trace(q, Pl(pts, true, .6, seed)), col);
  if (snow) { const ridge = pts.slice(1, -1); sawRow(g, ridge.map(p => [p[0], p[1] + 34]), 16, 10, -1, .8); fill(g, q => { q.moveTo(0, 0); }, col); }
  for (let i = 0; i < 14; i++) taper(g, [[100 + i * 160, 520], [110 + i * 160, 440], [96 + i * 160, 390]], 4);
}, { ss: 1.2, seed }));
const stars = (seed, n = 90, col = PAPER.gold) => once('st' + seed, () => piece([0, 0, 2300, 900], g => {
  for (let i = 0; i < n; i++) {
    const x = rnd(i, seed) * 2300, y = rnd(i, seed + 7) * 900, r = 3 + rnd(i, seed + 3) * 9;
    fill(g, q => { q.moveTo(x, y - r * 1.6); q.quadraticCurveTo(x, y, x + r, y); q.quadraticCurveTo(x, y, x, y + r * 1.6); q.quadraticCurveTo(x, y, x - r, y); q.quadraticCurveTo(x, y, x, y - r * 1.6); }, col);
  }
}, { ss: 1, seed, edge: .6 }));
const mandala = (col, r, seed, n = 8) => once('md' + col + r + seed, () => piece([-r - 10, -r - 10, r + 10, r + 10], g => {
  fill(g, q => q.arc(0, 0, r, 0, 7), col);
  cut(g, q => { q.arc(0, 0, r * .9, 0, 7); q.arc(0, 0, r * .86, 0, 7); }, 'evenodd');
  for (let i = 0; i < n; i++) { const a = i * Math.PI * 2 / n; cut(g, q => { q.moveTo(0, 0); q.ellipse(Math.cos(a) * r * .55, Math.sin(a) * r * .55, r * .3, r * .1, a, 0, 7); }); }
  rosette(g, 0, 0, r * .28, 8, 0, .3);
  crescentRows(g, -r * .6, r * .72, r * .6, r * .72, 10, 3, 0, .6);
  sawRow(g, Array.from({ length: 41 }, (_, i) => [Math.cos(i / 40 * 6.283) * r, Math.sin(i / 40 * 6.283) * r]), 12, 9, 1, .8);
}, { ss: 1.4, seed }));
const lotus = () => once('lotus', () => piece([-190, -110, 190, 70], g => {
  for (const [a, s, col] of [[-.9, 1, '#e0558a'], [.9, 1, '#e0558a'], [-.45, 1.1, '#f08ab0'], [.45, 1.1, '#f08ab0'], [0, 1.2, '#f7b5cf']]) {
    g.save(); g.rotate(a); fill(g, q => trace(q, P([[0, 20], [-34 * s, -50 * s], [0, -110 * s], [34 * s, -50 * s]], true, .3, 3)), col); g.restore();
  }
  fill(g, q => trace(q, P([[-190, 40], [-120, 66], [0, 70], [120, 66], [190, 40], [100, 20], [-100, 20]], true, .4, 8)), PAPER.green);
  cut(g, q => { for (let i = -3; i <= 3; i++) taper(g, [[i * 40, 56], [i * 40 + 6, 44], [i * 40, 30]], 3); });
}, { ss: 1.4 }));
const rays = (col, n = 18, R0 = 160, R1 = 900) => once('ray' + col, () => piece([-R1, -R1, R1, R1], g => {
  for (let i = 0; i < n; i++) { const a = i * Math.PI * 2 / n, w = .07; fill(g, q => { q.moveTo(Math.cos(a) * R0, Math.sin(a) * R0); q.lineTo(Math.cos(a - w) * R1, Math.sin(a - w) * R1); q.lineTo(Math.cos(a + w) * R1, Math.sin(a + w) * R1); q.closePath(); }, col); }
}, { ss: .8, edge: .5 }));
const grass = (col, seed) => once('gr' + col, () => piece([0, 0, 2300, 200], g => {
  const pts = [[0, 200]]; for (let x = 0; x <= 2300; x += 14) pts.push([x, 70 + Math.sin(x * .01 + seed) * 22 + ((x / 14) % 2) * 16]); pts.push([2300, 200]);
  fill(g, q => trace(q, Pl(pts, true, .4, seed)), col);
}, { ss: 1.2, seed }));
const txt = (s, size, col = PAPER.gold) => once('tx' + s + size + col, () => {
  const [m, mg] = canvas(10, 10); mg.font = `700 ${size}px FreeSerif`; const w = Math.ceil(mg.measureText(s).width) + 24, h = Math.ceil(size * 1.5), K = 2;
  const [c, gg] = canvas(w * K, h * K); gg.scale(K, K); gg.font = `700 ${size}px FreeSerif`; gg.fillStyle = col; gg.fillText(s, 12, size * 1.1);
  finishPaper(c, gg, { seed: 4, edge: 1.4 }); return { c, x0: -w / 2, y0: -h / 2, w, h };
});
// cream ribbon with the quotation / curse (a strip of black paper with cut-out letters)
const ribbon = (s, size = 64) => once('rb' + s, () => {
  const [m, mg] = canvas(10, 10); mg.font = `700 ${size}px FreeSerif`; const tw = Math.ceil(mg.measureText(s).width), w = tw + 120, h = size * 2, K = 1.6;
  const [c, gg] = canvas(w * K, h * K); gg.scale(K, K);
  gg.beginPath(); trace(gg, Pl([[0, 8], [w, 8], [w - 24, h / 2], [w, h - 8], [0, h - 8], [24, h / 2]], true, .4, 3)); gg.fillStyle = PAPER.ink; gg.fill();
  gg.globalCompositeOperation = 'destination-out'; gg.font = `700 ${size}px FreeSerif`; gg.fillStyle = '#000'; gg.fillText(s, 60, h / 2 + size * .34);
  gg.globalCompositeOperation = 'source-over';
  finishPaper(c, gg, { seed: 6, edge: 1.2 });
  return { c, x0: -w / 2, y0: -h / 2, w, h };
});
const stamp = (p, x, y, s = 1, rot = 0, o = {}) => put(g, p, mul(T(x, y), mul(R(rot), S(s))), o);
const lay = (p, x, y, par, cam, s = 1) => stamp(p, x - cam.x * par, y - cam.y * par, s, 0, { shadow: .5 });

// ---------- subtitles ----------
const CUES = (() => {
  const out = []; let cur = []; const flush = () => { if (cur.length) { out.push({ t0: cur[0][1], t1: cur[cur.length - 1][2] + .35, text: cur.map(w => w[0]).join(' ') }); cur = []; } };
  for (const w of WORDS) { cur.push(w); if (/[।?!…"”]$/.test(w[0]) || cur.length >= 7) flush(); }
  flush(); for (let i = 0; i < out.length - 1; i++) out[i].t1 = Math.min(out[i].t1, out[i + 1].t0 - .02); return out;
})();
const subStrip = text => once('sub' + text, () => {
  const [m, mg] = canvas(10, 10); mg.font = '700 46px FreeSerif'; const tw = mg.measureText(text).width, w = Math.ceil(tw + 130), h = 78, K = 1.5;
  const [c, gg] = canvas(w * K, h * K); gg.scale(K, K);
  const poly = []; for (let x = 0; x <= w; x += 10) poly.push([x, 4 + (x / 10 % 2) * 3]); poly.push([w - 20, h / 2]); for (let x = w; x >= 0; x -= 10) poly.push([x, h - 4 - (x / 10 % 2) * 3]); poly.push([20, h / 2]);
  gg.beginPath(); trace(gg, Pl(poly, true, .3, 5)); gg.fillStyle = '#5b1230'; gg.fill();
  for (let k = 0; k < 40; k++) { gg.fillStyle = `rgba(232,184,60,${.25 + rnd(k, 3) * .35})`; gg.beginPath(); gg.arc(30 + rnd(k, 1) * (w - 60), 10 + rnd(k, 2) * (h - 20), .8 + rnd(k, 4) * 1.4, 0, 7); gg.fill(); }
  rosette(gg, 42, h / 2, 12, 6, 0, .25); rosette(gg, w - 42, h / 2, 12, 6, 0, .25);
  finishPaper(c, gg, { seed: 9, edge: 1 });
  gg.setTransform(K, 0, 0, K, 0, 0); gg.font = '700 46px FreeSerif'; gg.fillStyle = '#fff1d6'; gg.textBaseline = 'middle'; gg.fillText(text, 65, h / 2 + 3);
  return { c, w, h };
});
function drawSubs(t) {
  for (const c of CUES) {
    if (t < c.t0 || t > c.t1) continue;
    const s = subStrip(c.text), u = Math.floor((t - c.t0) * 12) / 12, drop = u < .08 ? -14 : u < .16 ? -5 : 0;
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.shadowColor = 'rgba(20,4,12,.5)'; g.shadowBlur = 8; g.shadowOffsetX = 3; g.shadowOffsetY = 5;
    g.drawImage(s.c, 960 - s.w / 2, 1080 - 62 - s.h + drop, s.w, s.h); g.restore();
  }
}

// ---------- scenes ----------
const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
const step = t => Math.floor(t * 12) / 12;
function sky(kind) {
  const t = { night: ['indigo', 'rgba(90,30,110,.35)'], void: ['ink', 'rgba(20,70,80,.35)'], dusk: ['indigo', 'rgba(190,60,90,.55)'], gold: ['rice', 'rgba(240,160,40,.55)'], earth: ['rice', 'rgba(60,150,150,.45)'], curse: ['ink', 'rgba(120,10,40,.5)'] }[kind];
  fillPaper(g, t[0], 0, 0, W, H, [1, 0, 0, 1, 0, 0], t[1]);
}
const cam = (t, s0, s1, a) => { const u = ease((t - s0.a) / (s0.b - s0.a)); return { z: 1 + (s1.z - 1) * u, x: (s1.x || 0) * u, y: (s1.y || 0) * u }; };
const camera = (u, d, z0 = 1, z1 = 1.08, dx = 0, dy = 0) => ({ z: z0 + (z1 - z0) * (u / d), x: dx * (u / d), y: dy * (u / d) });
function world(c, fn) { g.save(); g.translate(W / 2, H / 2); g.scale(c.z, c.z); g.translate(-W / 2, -H / 2); fn(); g.restore(); }
const walk = (t, k = 1) => ({ bob: Math.abs(Math.sin(t * 4 * k)) * -5, sh1: -.1 + Math.sin(t * 4 * k) * .35, sh2: .1 - Math.sin(t * 4 * k) * .35, lean: Math.sin(t * 4 * k) * .015 });
const breathe = t => ({ bob: Math.sin(t * 1.6) * 2.2 });
const FIGC = [1, 0, 0, 1, 0, 0];
const fig = (who, pose, cm = { x: 0, y: 0 }) => drawFig(g, FIGC, who, pose);
const GROUND = 905;

const SCENES = [
  { a: 0, b: 2.5, draw(t, u) {       // wide: Shiva and Brahma on Kailash night
      sky('night'); const c = camera(u, 2.5, 1, 1.07, -12, 0);
      world(c, () => { lay(stars(1), 0, 0, .1, c); lay(band('#6b2f8a', 1, 50), -100, 600, .2, c); lay(mount('#2c3f8f', 2, 380, true), -100, 500, .3, c); lay(mount('#3b5ab5', 5, 300, true), -250, 580, .5, c);
        lay(grass('#1f6a63', 3), -100, 850, .9, c);
        const s = step(t); fig('brahma', { x: 420, y: GROUND, s: 1.15, ...breathe(s) }); fig('shiva', { x: 1380, y: GROUND, s: 1.28, flip: 1, hand1: 'trident', sh1: .1, ...breathe(s + 1) }); });
    } },
  { a: 2.5, b: 6.4, draw(t, u) {     // close-up: the head stuck to Shiva's hand
      sky('curse'); const c = camera(u, 3.9, 1.02, 1.12, 0, 0);
      world(c, () => { stamp(rays('#e6482a'), 960, 470, 1 + u * .06, u * .12, { shadow: 0, alpha: .55 }); lay(stars(7, 50, '#f3c35a'), 0, 0, .1, c);
        const s = step(t); fig('shiva', { x: 980, y: 1060, s: 1.9, ...breathe(s), sh1: -.35 + Math.sin(s * 5) * .05, hand1: 'head' }); });
    } },
  { a: 6.4, b: 13.6, draw(t, u) {     // Shiva walks the cosmos with the head
      sky('void'); const c = camera(u, 7.2, 1, 1.05, -260, 0);
      world(c, () => { lay(stars(3, 120), 0, 0, .15, c);
        stamp(mandala('#7b2cbf', 330, 3, 8), 1500 - c.x * .3, 300, 1, u * .5, { shadow: .6 }); stamp(mandala('#1f8a8a', 210, 5, 10), 380 - c.x * .5, 760, 1, -u * .6, { shadow: .6 });
        lay(band('#233b7a', 2, 60), -100, 760, .5, c); lay(band('#1f6a63', 4, 40), -100, 880, .8, c);
        const s = step(t), w = walk(s); fig('shiva', { x: 560 + u * 120, y: GROUND + 20, s: 1.35, hand1: 'head', ...w, sh1: -.2 + Math.sin(s * 4) * .1 }); });
    } },
  { a: 13.6, b: 18.4, draw(t, u) {    // not a war but a curse
      sky('curse'); const c = camera(u, 4.8, 1, 1.06, 0, -10);
      world(c, () => { stamp(rays('#7a1a3a'), 960, 520, 1, u * .1, { shadow: 0, alpha: .5 });
        stamp(mandala('#c3326e', 420, 9, 12), 960, 520, 1, -u * .25, { shadow: .8 });
        const pop = ease((t - 16.9) / .3); if (pop > 0) stamp(txt('श्राप', 190, PAPER.gold), 960, 560, .6 + .4 * pop, 0, { shadow: 1, alpha: pop });
        stamp(trident(), 280, 620, 1.1, -.35, { shadow: .8 }); stamp(trident(), 1640, 620, 1.1, .35, { shadow: .8 }); });
    } },
  { a: 18.4, b: 23.29, draw(t, u) {   // Narada gives the curse to his father
      sky('dusk'); const c = camera(u, 4.9, 1, 1.07, 14, 0);
      world(c, () => { lay(stars(11, 60), 0, 0, .1, c); lay(band('#b0315f', 3, 60), -100, 640, .3, c); lay(mount('#45266e', 8, 300, false), -150, 560, .5, c); lay(grass('#2d2155', 6), -100, 860, .9, c);
        const s = step(t); fig('narada', { x: 480, y: GROUND, s: 1.2, hand1: 'veena', sh1: -.5, ...breathe(s) }); fig('brahma', { x: 1400, y: GROUND, s: 1.2, flip: 1, ...breathe(s + 2) }); });
    } },
  { a: 23.29, b: 30.2, draw(t, u) {    // Brahma the creator on the lotus
      sky('gold'); const c = camera(u, 6.9, 1, 1.06, 0, 8);
      world(c, () => { stamp(rays('#f6c34a', 20), 960, 440, 1, u * .06, { shadow: 0, alpha: .75 }); stamp(mandala('#e0558a', 300, 4, 8), 960, 440, 1, u * .12, { shadow: .8, alpha: .9 });
        lay(band('#e7a23a', 2, 50), -100, 760, .4, c); lay(band('#1f8a8a', 6, 40), -100, 880, .7, c);
        stamp(lotus(), 960, 880, 1.3, 0, { shadow: 1 }); const s = step(t); fig('brahma', { x: 960, y: 850, s: 1.2, ...breathe(s) }); });
    } },
  { a: 30.2, b: 37.6, draw(t, u) {     // Manu and Brahmi: the first couple
      sky('earth'); const c = camera(u, 7.4, 1, 1.07, 0, 0);
      world(c, () => { lay(stars(13, 40, '#f7e6a0'), 0, 0, .1, c); lay(mount('#2a9a8d', 4, 280, false), -150, 590, .4, c); lay(mount('#1f7a6d', 9, 200, false), 0, 650, .6, c); lay(grass('#3f8a4a', 4), -100, 840, .9, c);
        const s = step(t), a = ease((t - 31.2) / .5), b = ease((t - 33.7) / .5);
        if (a > 0) fig('manu', { x: 700, y: GROUND, s: 1.25 * (.9 + .1 * a), ...breathe(s) }); if (b > 0) fig('brahmi', { x: 1200, y: GROUND, s: 1.25 * (.9 + .1 * b), flip: 1, ...breathe(s + 1) }); });
    } },
  { a: 37.6, b: 47.5, draw(t, u) {     // Narada's curse words
      sky('curse'); const c = camera(u, 9.9, 1, 1.05, -10, 0);
      world(c, () => { stamp(mandala('#5b1b6e', 360, 1, 10), 960, 480, 1, u * .2, { shadow: .8 }); lay(stars(15, 60, '#d77ab0'), 0, 0, .1, c);
        const s = step(t); fig('narada', { x: 420, y: GROUND, s: 1.15, hand1: 'veena', sh1: -.9, ...breathe(s) }); fig('brahma', { x: 1500, y: GROUND, s: 1.15, flip: 1, ...breathe(s + 1) });
        const k = ease((t - 39.7) / .5); stamp(ribbon('तुम उसकी इच्छा करोगे', 56), 960, 330, 1, 0, { shadow: 1, alpha: k });
        const k2 = ease((t - 44.2) / .5); stamp(ribbon('जिसकी इच्छा नहीं करनी चाहिए', 56), 960, 450, 1, 0, { shadow: 1, alpha: k2 }); });
    } },
  { a: 47.5, b: 54.4, draw(t, u) {     // a curse becomes law
      sky('night'); const c = camera(u, 6.9, 1, 1.1, 0, 0);
      world(c, () => { lay(stars(2, 100), 0, 0, .1, c); stamp(mandala('#e8b83c', 400, 2, 16), 960, 500, 1, u * .35, { shadow: 1 }); stamp(mandala('#c3326e', 260, 6, 8), 960, 500, 1, -u * .5, { shadow: 1 });
        const k = ease((t - 49.2) / .4); stamp(txt('प्रकृति का नियम', 110, '#fff1d6'), 960, 505, k, 0, { shadow: 1, alpha: k }); });
    } },
];

window.DUR = 54.34;
window.render = (t) => {
  g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, H); g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
  const sc = SCENES.find(s => t >= s.a && t < s.b) || SCENES[SCENES.length - 1], u = t - sc.a;
  sc.draw(t, u);
  // fade between scenes (paper flip)
  const f = Math.max(0, .18 - (t - sc.a)) / .18; if (f > 0) { g.save(); g.globalAlpha = f * .85; g.fillStyle = '#120a1c'; g.fillRect(0, 0, W, H); g.restore(); }
  if (!q.get('nosub')) drawSubs(t);
};
await document.fonts.ready;
window.READY = true;
