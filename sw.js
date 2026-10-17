/*
  Offline service worker for Japan 2026.

  Navigations prefer the deployed document, then fall back to the canonical cached shell.
  Static same-origin assets use stale-while-revalidate. Query-string navigation state is
  normalised to one shell key so Today, Trip, and Prep cannot drift into separate copies.
*/
const CACHE_PREFIX = 'japan-2026-shell-';
const CACHE = `${CACHE_PREFIX}32387070bf5d`;
const SHELL = [
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-192.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png',
  // Hero photos: precached so every day's photo is there offline.
  './photos/asakusa.webp',
  './photos/tokyo.webp',
  './photos/yokohama.webp',
  './photos/nikko.webp',
  './photos/shinkansen.webp',
  './photos/inari.webp',
  './photos/uji.webp',
  './photos/nara.webp',
  './photos/kyoto.webp',
  './photos/osaka-bay.webp',
  './photos/himeji.webp',
  './photos/osaka.webp',
  './photos/shinsekai.webp',
  './photos/expo.webp',
  './photos/fuji.webp',
  './photos/haneda.webp'
];
const SHELL_KEY = new URL('./index.html', self.location).href;
const NAVIGATION_TIMEOUT_MS = 2600;

const canonicalKey = request =>
  request.mode === 'navigate'
    ? new Request(SHELL_KEY, { credentials: 'same-origin' })
    : request;

const store = async (cache, key, response) => {
  if (!response || !response.ok) return response;
  try { await cache.put(key, response.clone()); } catch {}
  return response;
};

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await cache.add(SHELL[0]);
    await Promise.all(SHELL.slice(1).map(url => cache.add(url).catch(() => undefined)));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys
      // japan-2026-vNN is the previous build's namespace; it is never read again.
      .filter(key => (key.startsWith(CACHE_PREFIX) && key !== CACHE) || /^japan-2026-v\d+$/.test(key))
      .map(key => caches.delete(key)));
    if (self.registration.navigationPreload) {
      try { await self.registration.navigationPreload.enable(); } catch {}
    }
    await self.clients.claim();
  })());
});

self.addEventListener('message', event => {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil((async () => {
    const windows = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    const inScope = windows.filter(client => client.url.startsWith(self.registration.scope));
    const existing = inScope.find(client => client.focused)
      || inScope.find(client => client.visibilityState === 'visible')
      || inScope.find(client => 'focus' in client);
    if (existing) return existing.focus();
    return self.clients.openWindow('./?tab=today');
  })());
});

async function networkNavigation(event) {
  const request = event.request;
  const cache = await caches.open(CACHE);
  const key = canonicalKey(request);

  const network = (async () => {
    try {
      const preloaded = await event.preloadResponse;
      const response = preloaded || await fetch(request);
      return await store(cache, key, response);
    } catch {
      return null;
    }
  })();

  const timed = await Promise.race([
    network,
    new Promise(resolve => setTimeout(() => resolve(null), NAVIGATION_TIMEOUT_MS))
  ]);
  if (timed) return timed;

  const cached = await cache.match(key) || await cache.match(SHELL_KEY);
  if (cached) {
    event.waitUntil(network);
    return cached;
  }

  const late = await network;
  return late || Response.error();
}

async function staleWhileRevalidate(event) {
  const request = event.request;
  const cache = await caches.open(CACHE);
  const cached = await cache.match(request);
  const network = fetch(request)
    .then(response => store(cache, request, response))
    .catch(() => null);

  if (cached) {
    event.waitUntil(network);
    return cached;
  }
  return await network || Response.error();
}

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  // The document's update probe deliberately bypasses the cached shell, then stores the
  // successful response under the canonical key before the page reloads.
  if (url.searchParams.has('swBypass')) {
    event.respondWith((async () => {
      const response = await fetch(request, { cache: 'no-store' });
      if (response && response.ok) {
        const cache = await caches.open(CACHE);
        await store(cache, new Request(SHELL_KEY, { credentials: 'same-origin' }), response);
      }
      return response;
    })());
    return;
  }

  if (request.mode === 'navigate') {
    event.respondWith(networkNavigation(event));
    return;
  }

  event.respondWith(staleWhileRevalidate(event));
});
