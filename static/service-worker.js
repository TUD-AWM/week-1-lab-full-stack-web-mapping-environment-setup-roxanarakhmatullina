// static/service-worker.js

const CACHE_NAME = "activefinder-v1";

self.addEventListener("install", (event) => {
  // Activate immediately on install
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  // Take control of open clients/pages
  event.waitUntil(clients.claim());
});

// Very simple network-then-cache strategy for GET requests
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    caches.open(CACHE_NAME).then((cache) =>
      fetch(event.request)
        .then((response) => {
          // Store a copy in cache for later offline use
          cache.put(event.request, response.clone());
          return response;
        })
        .catch(() => {
          // If offline, try cached version
          return cache.match(event.request);
        })
    )
  );
});

