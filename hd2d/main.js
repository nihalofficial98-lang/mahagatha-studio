// Mahagatha pixel diorama (2.5D) pilot: EP4 first 54 s on the owner's voice. Pixel sprites standing in a lit, fogged 3D miniature, tilt-shift lens.
import * as THREE from 'three';
import { makePost } from './post_ts.js';
import { PX, ramp, hex, h2, fbm, texOf, rock, cobbles, ground, billboard, glow, blob, mulberry } from './px.js';
import { mat, mesh, box, fire } from './kit.js';
import { sky, stars, particles, flick } from './fx.js';
import { makeFigure } from './sprites.js';

const W = 1920, H = 1080, Q = new URLSearchParams(location.search);
const WORDS = await (await fetch('words.json')).json();
const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.2;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.getElementById('stage').appendChild(renderer.domElement);
const camera = new THREE.PerspectiveCamera(32, W / H, .3, 2000);
const ov = document.getElementById('ov').getContext('2d');
let post = null;

// ---------- pixel set pieces ----------
const matCache = {};
const M = k => matCache[k] || (matCache[k] = ({
  grass: () => mat(ground(96, 96, { seed: 3, grass: ['#0e2a1c', '#1c4a2c', '#2f7a3c', '#58a850', '#8acc6a'], dirt: ['#2a1e14', '#4a3624', '#6a5034'] })),
  stone: () => mat(cobbles(96, 96, { seed: 4, cols: ['#1c1824', '#3a3350', '#5a5078', '#8a80a8', '#b0a8c8'] })),
  gold: () => mat(cobbles(96, 96, { seed: 6, cols: ['#3a2208', '#7a4c14', '#b8841e', '#e8b838', '#ffe080'] })),
  rock: () => mat(rock(96, 96, { seed: 5, cols: ['#1a1a2c', '#2e3050', '#46507a', '#6a78a8', '#98a8d0'] })),
  rockW: () => mat(rock(96, 96, { seed: 9, cols: ['#3a1a2a', '#6a2a48', '#a04466', '#d4789a', '#f4b0c4'] })),
  snow: () => mat(ground(96, 96, { seed: 8, grass: ['#8a98c0', '#b4c0e0', '#dde6f6', '#ffffff'], dirt: ['#8a98c0', '#b4c0e0', '#dde6f6'] })),
}[k])());
function mountains(sc, cols, snow = true) {
  const R = mulberry(7);
  for (let i = 0; i < 8; i++) {
    const r = 9 + R() * 6, h = 14 + R() * 14, x = -60 + i * 17 + R() * 5, z = -52 - R() * 10;
    const m = mesh(new THREE.ConeGeometry(r, h, 7).translate(0, h / 2, 0), M(cols)); m.position.set(x, 0, z); sc.add(m);
    if (snow) { const s = mesh(new THREE.ConeGeometry(r * .36, h * .36, 7).translate(0, h * .82, 0), M('snow')); s.position.set(x, 0, z); sc.add(s); }
  }
}
function tree(h = 4) {
  const P = new PX(36, 52), G = ramp(['#0e2a1c', '#1c4a2c', '#2f7a3c', '#58a850', '#8acc6a']), B = ramp(['#2a1a10', '#4a2e1a', '#6a4426']);
  P.rect(16, 28, 4, 24, B(.5, 0, 0)); P.rect(16, 28, 1, 24, B(.9, 0, 0));
  P.fill((x, y) => { for (const [cx, cy, r] of [[18, 16, 13], [10, 22, 8], [26, 22, 8], [18, 8, 8]]) { const d = Math.hypot(x - cx, (y - cy) * 1.1) / r; if (d < 1) return G(.9 - d * .6 + (fbm(x * .3, y * .3, 4) - .5) * .4 - (y - cy) * .01, x, y); } return null; });
  P.outline(.3); const m = billboard(texOf(P.done()), 36 / 12, 52 / 12 * 1, {}); m.scale.setScalar(h / 4.3); return m;
}
function lotusMesh() {
  const P = new PX(80, 40), A = ramp(['#8a1f52', '#d4488a', '#f488b8', '#ffd0e4']);
  for (const [a, n, s] of [[-.95, 1, 1], [.95, 1, 1], [-.5, 1.1, 1.1], [.5, 1.1, 1.1], [0, 1.25, 1.3]]) for (let i = 0; i < 22 * s; i++) for (let j = -5; j <= 5; j++) { const t = i / (22 * s), wd = (1 - t) * 5 * Math.sin(Math.min(1, t * 3.2) * 1.57); if (Math.abs(j) < wd) P.set(Math.round(40 + Math.sin(a) * (i + 3) + j * Math.cos(a)), Math.round(36 - Math.cos(a) * (i + 3) + j * Math.sin(a) * 0), A(.35 + t * .6 - Math.abs(j) / 12, i, j)); }
  P.outline(.3); return billboard(texOf(P.done()), 80 / 20, 40 / 20, { em: null });
}
function textPlane(text, w, h, size, col = '#fff1d6', bg = null) {
  const c = document.createElement('canvas'); c.width = 1024; c.height = Math.round(1024 * h / w); const g = c.getContext('2d');
  if (bg) { g.fillStyle = bg; g.fillRect(0, 0, c.width, c.height); }
  g.font = `700 ${size}px FreeSerif`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = col; g.shadowColor = col; g.shadowBlur = 18; g.fillText(text, c.width / 2, c.height / 2);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  return new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false, fog: false, toneMapped: false }));
}
function ring(r, col, i = 2.5, y = 0) { const m = new THREE.Mesh(new THREE.TorusGeometry(r, .08, 6, 64), new THREE.MeshBasicMaterial({ color: new THREE.Color(col).multiplyScalar(i), fog: false })); m.position.y = y; return m; }
const POSES = { idle: {}, idleB: { bob: 1 }, trident: { item: 'trident', arm: 'low' }, head: { item: 'head', arm: 'fwd' }, headW: { item: 'head', arm: 'fwd', step: 1 }, veena: { item: 'veena', arm: 'fwd' }, up: { arm: 'up' }, pray: { arm: 'pray' } };
const FIG = {}; const fig = k => FIG[k] || (FIG[k] = makeFigure(k, POSES));
function put(sc, who, x, z, pose, flip = false, s = 1) { const f = fig(who); const g = new THREE.Group(); g.add(f.root); f.root.scale.setScalar(s); g.position.set(x, 0, z); sc.add(g); f.frame(pose); f.root.position.set(0, 0, 0); f.root.rotation.y = 0; f.mesh.scale.x = flip ? -1 : 1; return { g, f }; }

// ---------- scene recipes (one per picture) ----------
function stage(o) {
  const sc = new THREE.Scene(); sc.fog = new THREE.FogExp2(o.fog, o.fogD ?? .009);
  const sk = sky({ top: o.top, mid: o.mid, hor: o.hor, moonDir: new THREE.Vector3(o.mx ?? -.3, .4, -1), moonCol: o.moonCol ?? '#dfe8ff', moonI: o.moonI ?? 1 }); sc.add(sk.mesh);
  if (o.stars !== 0) sc.add(stars(o.stars ?? 500, 3));
  sc.add(new THREE.HemisphereLight(o.hemiS ?? '#8a90c8', o.hemiG ?? '#1a1626', o.hemi ?? .8));
  const key = new THREE.DirectionalLight(o.keyC ?? '#aab6e8', o.key ?? .8); key.position.set(-14, 22, 16); key.castShadow = true; key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -16, right: 16, top: 16, bottom: -16, near: 1, far: 80 }); key.shadow.bias = -.0006; sc.add(key);
  const g = box(70, .6, 50, M(o.ground ?? 'grass')); g.position.set(0, -.6, -8); sc.add(g);
  return sc;
}
const SCN = [
  { a: 0, b: 2.5, build() {     // 1: Kailash night
      const sc = stage({ fog: '#1c1e48', top: '#0a0c26', mid: '#241c5a', hor: '#6a4aa0', ground: 'snow', key: .7 }); mountains(sc, 'rock');
      const f1 = put(sc, 'brahma', -2.6, 0, 'idle', false, 1.2), f2 = put(sc, 'shiva', 2.4, 0, 'trident', true, 1.2); sc.add(glow('#9ab0ff', 7, .5).translateY(3).translateX(-6).translateZ(-20));
      const pl = new THREE.PointLight('#ffb060', 14, 18, 1.8); pl.position.set(0, 2, 3); sc.add(pl);
      return { sc, cam: [0, 3.4, 8.2], look: [0, 1.7, 0] }; } },
  { a: 2.5, b: 6.4, build() {   // 2: the head stuck to Shiva's hand
      const sc = stage({ fog: '#3a0f26', fogD: .03, top: '#12040e', mid: '#5a1424', hor: '#c8482c', ground: 'stone', key: .4 });
      put(sc, 'shiva', 0, 0, 'head', true, 1.15); const pl = new THREE.PointLight('#ff4a2a', 30, 12, 1.6); pl.position.set(-2, 2.5, 3); sc.add(pl);
      sc.add(glow('#ff5a30', 6, 1.4).translateY(2).translateZ(-1)); mountains(sc, 'rockW', false);
      return { sc, cam: [0, 2.7, 6.2], look: [0, 1.7, 0], fov: 30 }; } },
  { a: 6.4, b: 13.6, build() {  // 3: walking the cosmos
      const sc = stage({ fog: '#101c3a', fogD: .012, top: '#04061a', mid: '#0e2a4a', hor: '#2a5a8a', stars: 1200, ground: 'stone', key: .5, moonI: 0 });
      for (const [x, y, z, r, c] of [[-9, 5, -12, 4, '#9a5af0'], [10, 7, -16, 6, '#30c0c0'], [2, 9, -20, 8, '#f0a040']]) { sc.add(ring(r, c, 3, y).translateX(x).translateZ(z)); sc.add(glow(c, r * 3, .35).translateX(x).translateY(y).translateZ(z)); }
      put(sc, 'shiva', -.5, 0, 'headW', false, 1.1); const pl = new THREE.PointLight('#7ac0ff', 16, 16, 1.6); pl.position.set(-3, 3, 4); sc.add(pl);
      return { sc, cam: [3, 3, 7.5], look: [0, 1.7, 0] }; } },
  { a: 13.6, b: 18.4, build() { // 4: not a war, a curse
      const sc = stage({ fog: '#2a0a20', top: '#0a0210', mid: '#3a0c30', hor: '#8a1c48', ground: 'stone', key: .3, stars: 300 });
      const t = textPlane('श्राप', 9, 4, 360, '#ffd870'); t.position.set(0, 4.2, -2); sc.add(t); sc.add(ring(5, '#d04a86', 3, 4.2).translateZ(-3)); sc.add(glow('#d04a86', 22, .5).translateY(4.2).translateZ(-4));
      put(sc, 'shiva', -5, 1, 'trident', false, 1); put(sc, 'brahma', 5, 1, 'idle', true, 1);
      return { sc, cam: [0, 3.4, 10], look: [0, 2.8, 0] }; } },
  { a: 18.4, b: 23.29, build() {// 5: Narada and Brahma at dusk
      const sc = stage({ fog: '#4a1c48', fogD: .016, top: '#1a1038', mid: '#7a2a68', hor: '#f08a58', ground: 'grass', key: .9, keyC: '#ffb888', moonCol: '#ffd0a0', stars: 150 }); mountains(sc, 'rockW', false);
      put(sc, 'narada', -3.2, 0, 'veena', false); put(sc, 'brahma', 3.2, 0, 'idle', true); for (let i = 0; i < 6; i++) { const t = tree(4 + i % 3); t.position.set(-14 + i * 5.6, 0, -8 - (i % 2) * 5); sc.add(t); }
      return { sc, cam: [0, 3.4, 8.2], look: [0, 1.7, 0] }; } },
  { a: 23.29, b: 30.2, build() {// 6: Brahma on the lotus
      const sc = stage({ fog: '#7a4a1c', fogD: .014, top: '#3a2410', mid: '#d08a24', hor: '#ffd070', ground: 'gold', key: 1.1, keyC: '#ffe0a0', hemiS: '#ffd890', stars: 0, moonI: 0 });
      const l = lotusMesh(); l.scale.setScalar(2.4); l.position.set(0, 0, .2); sc.add(l); put(sc, 'brahma', 0, -.1, 'idle', false, 1.1).g.position.y = 1.1;
      sc.add(glow('#ffe080', 18, .9).translateY(3).translateZ(-3)); sc.add(ring(3.2, '#ffd060', 3, 3.2).translateZ(-2)); mountains(sc, 'rockW', false);
      return { sc, cam: [0, 3.2, 8.5], look: [0, 2.3, 0] }; } },
  { a: 30.2, b: 37.6, build() { // 7: Manu and Brahmi
      const sc = stage({ fog: '#3a6a58', fogD: .014, top: '#2a5a90', mid: '#6aa8c8', hor: '#f4e8b8', ground: 'grass', key: 1, keyC: '#fff0c8', hemiS: '#a8d8f0', stars: 0, moonI: 0 }); mountains(sc, 'rock', false);
      put(sc, 'manu', -2.4, 0, 'pray', false); put(sc, 'brahmi', 2.6, 0, 'idle', true); for (let i = 0; i < 9; i++) { const t = tree(4.5 + i % 3); t.position.set(-18 + i * 4.6, 0, -6 - (i % 3) * 3.5); sc.add(t); }
      return { sc, cam: [0, 3.4, 8.2], look: [0, 1.7, 0] }; } },
  { a: 37.6, b: 47.5, build() { // 8: the curse words
      const sc = stage({ fog: '#240c3a', top: '#080214', mid: '#2a0c52', hor: '#6a2a98', ground: 'stone', key: .3, stars: 500 });
      put(sc, 'narada', -4.2, 0, 'veena', false); put(sc, 'brahma', 4.2, 0, 'idle', true);
      const t = textPlane('तुम उसकी इच्छा करोगे… जिसकी इच्छा नहीं करनी चाहिए।', 16, 2.6, 56, '#f0d8ff'); t.position.set(0, 6, -2); sc.add(t);
      const pl = new THREE.PointLight('#b060ff', 30, 20, 1.6); pl.position.set(0, 5, 4); sc.add(pl); sc.add(glow('#a050ff', 16, .6).translateY(4).translateZ(-4));
      return { sc, cam: [0, 3.6, 10], look: [0, 2.6, 0] }; } },
  { a: 47.5, b: 54.4, build() {  // 9: a curse becomes law
      const sc = stage({ fog: '#1a1440', top: '#05041a', mid: '#1a1450', hor: '#4a3a98', ground: 'gold', key: .5, stars: 900 });
      for (const [r, c] of [[6, '#ffd060'], [4.4, '#d04a86'], [2.8, '#60e0e0']]) sc.add(ring(r, c, 3, 5).translateZ(-3));
      sc.add(glow('#ffd060', 26, .6).translateY(5).translateZ(-4)); const t = textPlane('प्रकृति का नियम', 12, 3, 150, '#fff1d6'); t.position.set(0, 5, -2.5); sc.add(t);
      return { sc, cam: [0, 3.6, 11], look: [0, 4.4, 0] }; } },
];

// ---------- subtitles (a dark band, serif italic, centred low) ----------
const CUES = (() => { const out = []; let cur = []; const fl = () => { if (cur.length) { out.push({ t0: cur[0][1], t1: cur.at(-1)[2] + .35, text: cur.map(w => w[0]).join(' ') }); cur = []; } }; for (const w of WORDS) { cur.push(w); if (/[।?!…"”]$/.test(w[0]) || cur.length >= 7) fl(); } fl(); for (let i = 0; i < out.length - 1; i++) out[i].t1 = Math.min(out[i].t1, out[i + 1].t0 - .02); return out; })();
function overlay(t) {
  ov.clearRect(0, 0, W, H); const c = CUES.find(c => t >= c.t0 && t <= c.t1); if (!c) return;
  const g = ov.createLinearGradient(0, H - 230, 0, H); g.addColorStop(0, 'rgba(8,4,16,0)'); g.addColorStop(1, 'rgba(8,4,16,.78)'); ov.fillStyle = g; ov.fillRect(0, H - 230, W, 230);
  ov.font = 'italic 700 52px FreeSerif'; ov.textAlign = 'center'; ov.fillStyle = '#fff1d6'; ov.shadowColor = 'rgba(0,0,0,.8)'; ov.shadowBlur = 8; ov.fillText(c.text, W / 2, H - 68); ov.shadowBlur = 0;
}
const built = {};
window.DUR = 54.34;
window.render = t => {
  const i = SCN.findIndex(s => t >= s.a && t < s.b), sc = SCN[i < 0 ? SCN.length - 1 : i], k = SCN.indexOf(sc);
  const S = built[k] || (built[k] = sc.build()); const u = (t - sc.a) / (sc.b - sc.a);
  camera.position.set(S.cam[0] + (u - .5) * 1.2, S.cam[1], S.cam[2] - u * .8); camera.fov = S.fov ?? 32; camera.updateProjectionMatrix(); camera.lookAt(...S.look);
  S.sc.traverse(o => { if (o.userData.update) o.userData.update(t, camera); });
  if (!post) { post = makePost(renderer, S.sc, camera, W, H, { ssaa: +(Q.get('ss') ?? 2) }); post.bloom.strength = .6; post.bloom.radius = .75; post.bloom.threshold = .85; post.vig.uniforms.amt.value = .62; post.vig.uniforms.warm.value = .1; post.vig.uniforms.contrast.value = .25; post.vig.uniforms.sat.value = 1.12; }
  post.dof.scene = S.sc; if (post.dof.ao) post.dof.ao.scene = S.sc; post.vig.uniforms.fade.value = 1;
  post.dof.tiltAmt = 9; post.dof.tiltC = .55; post.dof.tiltW = .22; post.dof.tiltF = .3; post.dof.maxCoc = 7;
  post.composer.render(); overlay(t);
};
await document.fonts.ready; window.READY = true;
