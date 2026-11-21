// Pixel-art cast for Mahagatha (3/4 view facing right, 44x64 px frames) drawn procedurally; each pose is one frame of an atlas.
import * as THREE from 'three';
import { PX, ramp, hex, texOf, billboard, blob } from './px.js';
export const SPX = 1 / 32, FW = 44, FH = 64;
const R = (a) => ramp(a, .22);
const C = {
  skinBrahma: R(['#7a3a1c', '#b86a30', '#dd9248', '#f5b66a']), skinFair: R(['#8a4a2c', '#c98450', '#eeb27a', '#ffd5a0']), skinDark: R(['#4a2418', '#7a4228', '#a1603a', '#c0804e']),
  skinShiva: R(['#1f2f6b', '#35529e', '#5a82cc', '#8db0ee']), saffron: R(['#8a3a0a', '#d06a14', '#f2a028', '#ffd05a']), white: R(['#6f6a78', '#aaa4b4', '#e0dae6', '#fffaf0']),
  gold: R(['#5a3a10', '#a87a24', '#e0b040', '#fff0a0']), magenta: R(['#5a0f3a', '#962460', '#d04a86', '#f48ab4']), teal: R(['#0c3a44', '#16707a', '#2aa5a5', '#7ae0d0']),
  ink: R(['#08060c', '#14101c', '#2a2236']), tiger: R(['#6a2a08', '#c06a14', '#ee9a2c', '#ffc860']), beard: R(['#8a8694', '#c4c0cc', '#eeeaf4', '#ffffff']),
  ash: R(['#7a86a6', '#b4bed6', '#e2e8f4']), red: R(['#5a0a14', '#a8182a', '#e0382e']), wood: R(['#2e1a10', '#5e3a1e', '#92602e']),
};
const OUT = hex('#120a18');
function head(P, cx, cy, skin, o = {}) {
  P.ellipse(cx, cy, 5.5, 6.5, skin(.62, cx, cy)); P.ellipse(cx - 1.5, cy + 1, 3.5, 4.5, skin(.82, cx, cy)); P.ellipse(cx + 1, cy - 3, 3.5, 2, skin(.5, cx, cy));
  P.set(cx + 5, cy, skin(.62, 0, 0)); P.set(cx + 5, cy + 1, skin(.5, 0, 0));          // nose
  P.set(cx + 2, cy - 1, OUT); P.set(cx + 3, cy - 1, OUT); P.set(cx + 1, cy - 3, OUT); P.set(cx + 4, cy - 3, OUT);   // eye + brow
  if (o.bindi) P.set(cx + 4, cy - 3, C.red(.9, 0, 0));
  if (o.sad) P.set(cx + 3, cy + 3, OUT);
}
function crown(P, cx, cy) { P.poly([[cx - 5, cy - 5], [cx - 4, cy - 12], [cx - 1, cy - 7], [cx + 1, cy - 14], [cx + 3, cy - 7], [cx + 6, cy - 11], [cx + 6, cy - 5]], (x, y) => C.gold(.55 + (cy - 5 - y) * -.04 + .3, x, y)); P.rect(cx - 5, cy - 6, 11, 2, C.gold(.95, 0, 0)); P.set(cx + 1, cy - 8, C.red(.9, 0, 0)); }
function arm(P, x0, y0, x1, y1, skin, w = 2) { for (let i = 0; i < w; i++) P.line(x0 + i, y0, x1 + i, y1, skin(.6 + i * .15, i, 0)); P.rect(x1 - 1, y1 - 1, 3, 3, skin(.8, 0, 0)); }
function legs(P, cloth, kind, st) {
  if (kind === 'woman') { P.poly([[14, 34], [30, 34], [35, 62], [9, 62]], (x, y) => cloth(.5 + (x - 22) * .014 + (y % 7 === 0 ? -.12 : 0), x, y)); P.rect(9, 59, 26, 2, C.gold(.8, 0, 0)); return; }
  P.poly([[15, 36], [30, 36], [33, 58], [11, 58]], (x, y) => cloth(.5 + (x - 22) * .012 + (y % 6 === 0 ? -.12 : 0), x, y));
  P.rect(11, 56, 22, 2, C.gold(.8, 0, 0));
  const s = st ? 2 : 0; P.rect(14 + s, 58, 5, 4, C.skinDark(.5, 0, 0)); P.rect(24 - s, 58, 5, 4, C.skinDark(.6, 0, 0));
}
export const WHO = {
  brahma: { skin: C.skinBrahma, cloth: C.saffron, kind: 'man' }, shiva: { skin: C.skinShiva, cloth: C.tiger, kind: 'man' },
  brahmi: { skin: C.skinFair, cloth: C.magenta, kind: 'woman' }, manu: { skin: C.skinFair, cloth: C.teal, kind: 'man' }, narada: { skin: C.skinDark, cloth: C.white, kind: 'man' },
};
function draw(P, E, who, p) {
  const c = WHO[who], by = p.bob || 0;
  legs(P, c.cloth, c.kind, p.step);
  const topY = 20 + by;
  if (c.kind === 'woman') P.poly([[15, topY], [29, topY], [30, 38], [14, 38]], (x, y) => c.cloth(.55 + (y - 20) * .01, x, y)), P.poly([[16, topY], [28, topY], [32, 40], [26, 40]], (x, y) => C.gold(.55, x, y));
  else P.poly([[15, topY], [29, topY], [28, 37], [16, 37]], (x, y) => c.skin(.55 + (29 - x) * .012, x, y));
  if (who === 'brahma' || who === 'narada' || who === 'manu') P.line(16, topY + 1, 28, 34, C.white(.8, 0, 0));      // sacred thread
  P.rect(14, 36, 17, 3, C.gold(.8, 0, 0));
  if (who === 'shiva') { for (const y of [topY + 4, topY + 7, topY + 10]) P.line(17, y, 27, y - 1, C.ash(.8, 0, 0)); P.poly([[15, 36], [30, 36], [32, 52], [28, 49], [22, 53], [16, 49], [12, 52]], (x, y) => ((x * 3 + y) % 5 === 0 ? C.tiger(.2, x, y) : C.tiger(.7, x, y))); }
  // far arm
  arm(P, 16, topY + 3, 13, topY + 16, c.skin, 2);
  // head(s)
  const hy = 12 + by;
  if (who === 'brahma') { head(P, 17, hy + 1, c.skin); head(P, 27, hy + 1, c.skin); P.ellipse(22, hy - 4, 4, 4, c.skin(.5, 0, 0)); }
  head(P, 22, hy, c.skin, { bindi: who === 'brahmi' });
  if (who === 'brahma') { P.poly([[18, hy + 4], [27, hy + 4], [26, hy + 13], [22, hy + 16], [19, hy + 12]], (x, y) => C.beard(.8 - (y - hy) * .02, x, y)); crown(P, 22, hy - 3); }
  if (who === 'shiva') { P.ellipse(21, hy - 8, 4.5, 4, C.ink(.6, 0, 0)); P.ellipse(21, hy - 8, 2, 1.5, C.ink(.9, 0, 0)); P.poly([[16, hy - 2], [15, hy + 16], [19, hy + 8]], (x, y) => C.ink(.4, x, y)); P.rect(27, hy - 12, 3, 3, C.ash(.95, 0, 0)); E && E.rect(27, hy - 12, 3, 3, C.ash(.95, 0, 0)); }
  if (who === 'brahmi') { P.ellipse(17, hy - 3, 5, 4, C.ink(.5, 0, 0)); P.poly([[17, hy], [14, hy + 20], [18, hy + 22], [19, hy + 6]], (x, y) => C.ink(.5, x, y)); P.set(18, hy - 7, C.gold(.9, 0, 0)); }
  if (who === 'manu' || who === 'narada') { P.ellipse(19, hy - 6, 4, 3.5, C.ink(.6, 0, 0)); if (who === 'narada') P.poly([[25, hy + 3], [28, hy + 8], [22, hy + 15], [17, hy + 7]], (x, y) => C.beard(.7, x, y)); }
  // near arm + item
  const a = p.arm || 'low';
  const sx = 28, sy = topY + 3;
  if (a === 'low') arm(P, sx, sy, 31, topY + 17, c.skin);
  if (a === 'fwd') arm(P, sx, sy, 36, topY + 10, c.skin);
  if (a === 'up') arm(P, sx, sy, 34, topY - 6, c.skin);
  if (a === 'pray') { arm(P, sx, sy, 27, topY + 11, c.skin); }
  if (p.item === 'trident') { P.line(34, 63, 34, 1, C.gold(.8, 0, 0)); P.line(35, 63, 35, 1, C.gold(.5, 0, 0)); for (const x of [31, 38]) P.line(x, 9, x, 2, C.gold(.9, 0, 0)); P.line(34, 8, 34, 0, C.gold(1, 0, 0)); P.line(31, 9, 38, 9, C.gold(.9, 0, 0)); P.rect(33, 16, 3, 2, C.red(.9, 0, 0)); }
  if (p.item === 'head') { P.ellipse(36, topY + 17, 4.5, 5, C.skinBrahma(.6, 0, 0)); P.set(38, topY + 17, OUT); P.poly([[33, topY + 13], [34, topY + 9], [36, topY + 12], [38, topY + 9], [39, topY + 13]], (x, y) => C.gold(.8, x, y)); P.poly([[33, topY + 20], [39, topY + 20], [36, topY + 25]], (x, y) => C.beard(.8, x, y)); }
  if (p.item === 'veena') { P.line(34, topY + 14, 41, topY - 8, C.wood(.8, 0, 0)); P.ellipse(33, topY + 17, 4, 4, C.red(.55, 0, 0)); P.ellipse(40, topY - 9, 2, 2, C.gold(.8, 0, 0)); }
  if (p.item === 'kamandalu') { P.ellipse(35, topY + 15, 3, 4, C.gold(.7, 0, 0)); }
}
export function makeFigure(who, poses) {
  const names = Object.keys(poses), n = names.length, P = new PX(FW * n, FH), E = new PX(FW * n, FH);
  names.forEach((k, i) => { const p1 = new PX(FW, FH), e1 = new PX(FW, FH); draw(p1, e1, who, poses[k]); p1.outline(.3); for (let y = 0; y < FH; y++) for (let x = 0; x < FW; x++) { const c = p1.get(x, y); if (c) P.set(i * FW + x, y, c); const e = e1.get(x, y); if (e) E.set(i * FW + x, y, e); } });
  const tex = texOf(P.done()), em = texOf(E.done()); for (const t of [tex, em]) t.repeat.set(1 / n, 1);
  const mesh = billboard(tex, FW * SPX, FH * SPX, { em, emCol: '#ffffff', emI: 2 });
  const root = new THREE.Group(); root.add(mesh); const sh = blob(.5, .55); sh.position.y = .015; root.add(sh);
  return { root, mesh, frame(name) { const i = names.indexOf(name); tex.offset.x = em.offset.x = i / n; }, face(cam, flip = false) { root.rotation.y = Math.atan2(cam.position.x - root.position.x, cam.position.z - root.position.z); mesh.scale.x = flip ? -1 : 1; } };
}
