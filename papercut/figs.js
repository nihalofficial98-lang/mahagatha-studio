// Multi-colour paper-cut cast for Mahagatha: jointed profile figures (facing right), every piece a cut sheet of coloured paper.
import { PAL, piece, P, Pl, trace, fill, cut, cutTaper, inset, ellipsePoly, curve } from './paper.js';
import { sawRow, crescent, crescentRows, swirl, rosette, plum, coin, dots, taper } from './motifs.js';
import { mul, T, R, S, put } from './rig.js';

export const PAPER = {
  skinBrahma: '#d9873a', skinShiva: '#5f86c9', skinFair: '#e3a46a', skinDark: '#b8683a',
  saffron: '#ef9a1f', gold: '#e8b83c', white: '#f3ead2', maroon: '#8e1b36', magenta: '#c3326e', teal: '#1f8a8a',
  green: '#3f8a4a', ink: '#241a33', tiger: '#d98a2c', red: '#d2201f', indigo: '#2a2f6b', ash: '#cfd3e6'
};
const C = {};
const key = (...a) => a.join('|');
const once = (k, f) => C[k] || (C[k] = f());

// ---------- head (profile, facing right) ----------
const FACE = [[26, -92], [34, -76], [46, -60], [40, -55], [36, -50], [38, -44], [31, -36], [10, -30], [-12, -32], [-34, -60], [-24, -96], [4, -102]];
function head(kind, skin, seed) {
  return once(key('head', kind, skin), () => piece([-110, -230, 90, 24], g => {
    const face = P(FACE, true, .3, seed);
    if (kind === 'brahma') {            // tall three-point crown, white beard
      for (const [x, h] of [[-18, 62], [4, 88], [24, 62]]) fill(g, q => trace(q, Pl([[x - 12, -96], [x, -96 - h], [x + 12, -96]], true, .3, seed + x)), PAPER.gold);
      fill(g, q => trace(q, Pl([[-30, -92], [-30, -108], [30, -108], [30, -92]], true, .3, seed)), PAPER.gold);
      sawRow(g, [[-26, -102], [26, -102]], 9, 7, 1, .8);
    }
    if (kind === 'shiva') {             // jata: coiled bun, locks, crescent moon
      fill(g, q => trace(q, P(ellipsePoly(-4, -128, 30, 30, 0, 28).slice(0, -1), true, .4, seed + 2)), PAPER.ink);
      fill(g, q => trace(q, P([[-30, -90], [-52, -70], [-58, -30], [-52, 10], [-40, -20], [-34, -60]], true, .4, seed + 3)), PAPER.ink);
      swirl(g, -4, -128, 22, 2.3, 4, 0, 1);
      fill(g, q => { q.arc(18, -158, 14, 0, 7); }, PAPER.ash);
      cut(g, q => q.arc(24, -161, 12, 0, 7));
    }
    if (kind === 'woman') {             // hair bun + long braid
      fill(g, q => trace(q, P(ellipsePoly(-30, -92, 26, 24, 0, 28).slice(0, -1), true, .4, seed + 2)), PAPER.ink);
      fill(g, q => trace(q, P([[-34, -72], [-56, -40], [-62, 30], [-52, 40], [-44, -10], [-28, -50]], true, .4, seed + 3)), PAPER.ink);
      plum(g, -34, -96, 9);
    }
    if (kind === 'man' || kind === 'rishi') {   // hair knot
      fill(g, q => trace(q, P(ellipsePoly(-14, -112, 22, 20, 0, 24).slice(0, -1), true, .4, seed + 2)), PAPER.ink);
      if (kind === 'rishi') sawRow(g, [[22, -38], [-6, -24], [-24, -40]], 14, 6, 1, .9);
    }
    fill(g, q => trace(q, face), skin);
    if (kind === 'brahma') fill(g, q => trace(q, Pl([[34, -44], [38, -30], [20, 6], [-8, 14], [-26, -20], [-8, -30]], true, .5, seed + 9)), PAPER.white);   // beard
    // face cuts: eye crescent, brow, ear ring, tilak
    crescent(g, 26, -70, 9, Math.PI * 1.05, Math.PI * 1.95, 4);
    taper(g, [[14, -84], [26, -88], [38, -82]], 3);
    if (kind === 'shiva') { crescent(g, 14, -90, 6, Math.PI * 1.1, Math.PI * 1.9, 2.4); taper(g, [[12, -98], [16, -90], [12, -86]], 2); }
    if (kind === 'woman' || kind === 'brahma') cut(g, q => q.arc(-16, -52, 4, 0, 7));
    inset(g, face, 3.2, 1.3, skin);
    if (kind === 'woman') { fill(g, q => q.arc(32, -86, 3.6, 0, 7), PAPER.red); }
    if (kind === 'brahma' || kind === 'shiva') taper(g, [[22, -98], [36, -90]], 2.2);
  }, { seed }));
}

// ---------- torso / lower garment ----------
function body(kind, skin, cloth, trim, seed) {
  return once(key('body', kind, skin, cloth), () => piece([-90, -300, 90, 24], g => {
    const upper = P([[-34, -300], [30, -300], [40, -250], [30, -170], [34, -130], [-34, -130], [-30, -170], [-40, -250]], true, .3, seed);
    const lowerPts = kind === 'woman'
      ? [[-48, -230], [44, -230], [60, 0], [-64, 0]]                           // sari to the ground
      : [[-42, -150], [44, -150], [60, -10], [34, 0], [0, -14], [-30, 0], [-58, -10]];   // dhoti
    const lower = P(lowerPts, true, .35, seed + 1);
    fill(g, q => trace(q, upper), kind === 'woman' ? cloth : skin);
    fill(g, q => trace(q, lower), cloth);
    if (kind === 'woman') {             // pallu over the shoulder
      fill(g, q => trace(q, P([[-34, -296], [6, -296], [50, -150], [38, -130], [-6, -200]], true, .4, seed + 4)), trim);
    }
    // cuts: hem crescents, waist band, ornaments
    crescentRows(g, -44, -22, 50, -22, 11, 3.6, 0, .7);
    sawRow(g, [[-58, -4], [-30, 2], [0, -10], [34, 2], [58, -6]], 9, 7, -1, .7);
    fill(g, q => trace(q, Pl([[-42, -154], [44, -154], [46, -138], [-44, -138]], true, .3, seed + 6)), trim);
    cut(g, q => { for (let x = -34; x <= 34; x += 17) { q.moveTo(x + 4, -146); q.arc(x, -146, 4, 0, 7); } });
    if (kind === 'shiva') {             // tiger skin + serpent garland + ash lines
      fill(g, q => trace(q, Pl([[-40, -150], [44, -150], [58, -50], [30, -34], [0, -46], [-30, -30], [-52, -48]], true, .5, seed + 8)), PAPER.tiger);
      for (let i = 0; i < 6; i++) { const x = -34 + i * 14; cut(g, q => { q.moveTo(x, -138); q.lineTo(x + 5, -100 - (i % 2) * 14); q.lineTo(x + 8, -138); q.closePath(); }); }
      for (const y of [-262, -246, -230]) taper(g, [[-24, y], [0, y - 6], [24, y]], 3);
    }
    if (kind === 'brahma' || kind === 'rishi') taper(g, [[-26, -292], [4, -240], [30, -190]], 4);   // sacred thread
    swirl(g, 0, -272, 14, 2, 3, 0, 1);
    // necklace of beads
    cut(g, q => { for (let i = 0; i < 9; i++) { const a = Math.PI * (.12 + i * .095); q.moveTo(Math.cos(a) * 22 + 4, -280 + Math.sin(a) * 18 + 3); q.arc(Math.cos(a) * 22, -280 + Math.sin(a) * 18, 3, 0, 7); } });
    inset(g, upper, 4, 1.4, kind === 'woman' ? cloth : skin);
  }, { seed }));
}

// ---------- arm (shoulder pivot at 0,0; hangs down +y) ----------
function arm(skin, band, seed) {
  return once(key('arm', skin, band), () => piece([-24, -14, 24, 150], g => {
    const a = P([[-9, -8], [9, -8], [10, 60], [8, 112], [14, 126], [8, 140], [-6, 140], [-12, 126], [-7, 112], [-9, 60]], true, .3, seed);
    fill(g, q => trace(q, a), skin);
    fill(g, q => trace(q, Pl([[-11, 22], [11, 22], [11, 32], [-11, 32]], true, .3, seed)), band);
    fill(g, q => trace(q, Pl([[-9, 100], [10, 100], [10, 108], [-9, 108]], true, .3, seed)), band);
    inset(g, a, 2.8, 1.1, skin);
  }, { seed }));
}

// ---------- props ----------
export function trident(seed = 5) {
  return once('trident', () => piece([-50, -330, 50, 60], g => {
    fill(g, q => trace(q, Pl([[-4, 60], [4, 60], [4, -250], [-4, -250]], true, .4, seed)), PAPER.gold);
    for (const x of [-26, 0, 26]) fill(g, q => trace(q, Pl([[x - 6, -240], [x, -320], [x + 6, -240]], true, .3, seed + x)), PAPER.gold);
    fill(g, q => trace(q, Pl([[-30, -226], [30, -226], [30, -240], [-30, -240]], true, .3, seed)), PAPER.gold);
    cut(g, q => q.arc(0, -150, 5, 0, 7));
    fill(g, q => q.arc(10, -190, 9, 0, 7), PAPER.red);
  }, { seed }));
}
export function skull(seed = 5) {
  return once('skull', () => piece([-40, -40, 40, 50], g => {
    const s = P([[-26, -4], [-28, -22], [-14, -36], [10, -36], [26, -22], [24, -2], [14, 10], [14, 32], [-12, 32], [-12, 10]], true, .3, seed);
    fill(g, q => trace(q, s), '#ece4cc');
    cut(g, q => { q.arc(-10, -10, 7, 0, 7); q.moveTo(21, -10); q.arc(14, -10, 7, 0, 7); });
    cut(g, q => trace(q, Pl([[-3, 6], [3, 6], [0, 15]], true, .2, 1)));
    inset(g, s, 2.5, 1, '#ece4cc');
  }, { seed }));
}
export function head5(seed = 5, skin = PAPER.skinBrahma) {   // a detached Brahma head, hand-held
  return head('brahma', skin, seed);
}
export function veena(seed = 7) {
  return once('veena', () => piece([-30, -150, 30, 40], g => {
    fill(g, q => trace(q, P(ellipsePoly(0, 20, 22, 20, 0, 24).slice(0, -1), true, .3, seed)), PAPER.maroon);
    fill(g, q => trace(q, Pl([[-4, 0], [4, 0], [4, -140], [-4, -140]], true, .3, seed)), PAPER.gold);
    cut(g, q => q.arc(0, 22, 6, 0, 7)); fill(g, q => q.arc(0, -144, 9, 0, 7), PAPER.gold);
  }, { seed }));
}

// ---------- the cast ----------
export const CAST = {
  brahma: { head: 'brahma', skin: PAPER.skinBrahma, cloth: PAPER.saffron, trim: PAPER.gold, band: PAPER.gold, kind: 'man', heads: 4 },
  shiva: { head: 'shiva', skin: PAPER.skinShiva, cloth: PAPER.tiger, trim: PAPER.maroon, band: PAPER.ash, kind: 'shiva' },
  brahmi: { head: 'woman', skin: PAPER.skinFair, cloth: PAPER.magenta, trim: PAPER.gold, band: PAPER.gold, kind: 'woman' },
  manu: { head: 'man', skin: PAPER.skinFair, cloth: PAPER.teal, trim: PAPER.gold, band: PAPER.gold, kind: 'man' },
  narada: { head: 'rishi', skin: PAPER.skinDark, cloth: PAPER.white, trim: PAPER.saffron, band: PAPER.gold, kind: 'rishi' },
};
const SH = [0, -262], NECK = [4, -296];
// draw a figure: pose = {x,y,s,flip,sh1,sh2,head,bob,hand1:'trident'|'head'|'veena', lean}
export function drawFig(g, Cm, who, pose = {}) {
  const c = CAST[who], p = { s: 1, ...pose };
  const B = body(c.kind, c.skin, c.cloth, c.trim, 11), A = arm(c.skin, c.band, 12);
  let root = mul(Cm, T(p.x || 0, p.y || 0)); if (p.flip) root = mul(root, S(-1, 1)); root = mul(root, S(p.s));
  root = mul(root, R(p.lean || 0)); root = mul(root, T(0, p.bob || 0));
  const o = { shadow: 1 };
  put(g, A, mul(mul(root, T(-34, SH[1])), mul(R(p.sh2 ?? -.18), S(1.25))), { shadow: .6 });        // far arm
  put(g, B, mul(root, S(1.35, 1)), o);
  if (c.heads === 4 && p.heads !== 1) {             // fan of extra heads behind
    put(g, head('brahma', c.skin, 14), mul(mul(root, T(NECK[0] - 10, NECK[1] - 10)), mul(R(-.12), S(-1.3, 1.3))), { shadow: .8 });
    put(g, head('brahma', c.skin, 15), mul(mul(root, T(NECK[0] + 6, NECK[1] - 40)), mul(R(.08), S(1.1, 1.1))), { shadow: .8 });
  }
  put(g, head(c.head, c.skin, 13), mul(mul(root, T(NECK[0], NECK[1] + 16)), mul(R(p.head || 0), S(1.5))), o);
  const M1 = mul(mul(root, T(34, SH[1])), mul(R(p.sh1 ?? .3), S(1.25)));
  put(g, A, M1, o);
  const hand = mul(M1, T(0, 132));
  if (p.hand1 === 'trident') put(g, trident(), mul(hand, R(-.1)), o);
  else if (p.hand1 === 'head') put(g, head5(21), mul(mul(hand, T(8, 36)), mul(R(.5), S(.62))), o), put(g, A, M1, { shadow: 0, alpha: 0 });
  else if (p.hand1 === 'veena') put(g, veena(), mul(hand, R(.18)), o);
  return { hand, root };
}
