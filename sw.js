const VERSION = "rutina-v12";
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  ...["0276","0289","0292","0293","0294","0313","0314","0333","0334","0381",
      "0409","0410","0417","0426","0630","0705","0795","1409","1760","2135",
      "2137","2188","3142","3645",
      // calentamiento / enfriamiento
      "3636","1471","0002","1167","3533","1604","3561","1368",
      "1271","0643","1365","0713","0613","1511","1424","1377"].map(id => `./gifs/${id}.gif`),
];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(hit =>
      hit || fetch(e.request).then(res => {
        if (res.ok && e.request.method === "GET" && new URL(e.request.url).origin === location.origin) {
          const copy = res.clone();
          caches.open(VERSION).then(c => c.put(e.request, copy));
        }
        return res;
      })
    )
  );
});
