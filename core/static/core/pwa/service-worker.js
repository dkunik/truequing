const CACHE_NAME = "truequing-v9";

const URLS_TO_CACHE = [
    "/static/core/css/main.css",
    "/static/core/pwa/manifest.json",
    "/static/core/pwa/icon-192.png",
    "/static/core/pwa/icon-512.png",
    "/static/core/pwa/offline-db.js",
    "/sync-offline/",
];

self.addEventListener("install", function (event) {

    event.waitUntil(
        caches.open(CACHE_NAME).then(function (cache) {
            return cache.addAll(URLS_TO_CACHE);
        })
    );

    self.skipWaiting();
});

self.addEventListener("activate", function (event) {

    event.waitUntil(
        caches.keys().then(function (cacheNames) {
            return Promise.all(
                cacheNames.map(function (cacheName) {

                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }

                })
            );
        })
    );

    self.clients.claim();
});

self.addEventListener("fetch", function (event) {

    if (event.request.mode === "navigate") {

        event.respondWith(

            fetch(event.request)

                .catch(function () {

                    return caches.match("/sync-offline/");

                })

        );

        return;
    }

    event.respondWith(

        caches.match(event.request)

            .then(function (cachedResponse) {

                return (
                    cachedResponse
                    ||
                    fetch(event.request)
                );

            })

    );
});



