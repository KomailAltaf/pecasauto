export default {
  routes: [
    { method: "GET", path: "/pecasauto/homepage", handler: "public-content.homepage", config: { auth: false } },
    { method: "GET", path: "/pecasauto/products/:externalId", handler: "public-content.product", config: { auth: false } }
  ]
};
