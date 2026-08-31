/* ChartBenchLive service worker — offline-first app shell.
   The cache name embeds the build stamp, so every deploy changes this
   file, which is exactly what makes the browser's service-worker update
   check notice a new version: it installs alongside the old one, the
   page shows an "Update ready" toast, and SKIP_WAITING + controllerchange
   swap it in. Keep SW_BUILD in sync with APP_BUILD in index.html —
   build-deploy checks are the reminder. */
const SW_BUILD = '2026-08-30 19:19';
const CACHE = 'cblive-' + SW_BUILD.replace(/[^0-9]/g, '');
const PRECACHE = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith('cblive-') && k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('message', e => {
  if(e.data && e.data.type === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if(req.method !== 'GET') return;
  const url = new URL(req.url);
  if(url.origin !== location.origin) return;
  // Cache-first: on stage, never wait on the network. ignoreSearch for
  // page loads so cache-busting queries (?v=...) still hit the cached
  // shell. Anything fetched from the network on a miss is cached for
  // next time.
  const isPage = req.mode === 'navigate' || url.pathname.endsWith('/') || url.pathname.endsWith('/index.html');
  e.respondWith(
    caches.match(req, { ignoreSearch: isPage }).then(hit => hit || fetch(req).then(res => {
      if(res.ok){
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }).catch(() => (isPage ? caches.match('./index.html') : Promise.reject(new Error('offline')))))
  );
});
