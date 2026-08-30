// Copies the ChartBenchLive web app from ../perform into www/ for
// Capacitor to bundle. Deliberately skips sw.js (a native app IS the
// offline shell — no service worker wanted inside the webview) and the
// versions/ snapshot folder (dev history, not app payload).
// Run via `npm run sync` (which then runs `cap sync` to push www/ into
// the android/ and ios/ projects).
const fs = require('fs');
const path = require('path');

const SRC = path.join(__dirname, '..', 'perform');
const OUT = path.join(__dirname, 'www');
const FILES = [
  'index.html',
  'manifest.json',
  'icon-192.png',
  'icon-512.png',
  'icon-maskable-512.png',
  'apple-touch-icon.png',
];

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });
for(const f of FILES){
  fs.copyFileSync(path.join(SRC, f), path.join(OUT, f));
}
console.log('www/ synced from perform/:', FILES.join(', '));
