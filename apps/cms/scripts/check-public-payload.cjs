// Regression check: public editorial endpoints must never expose admin-user audit data or secrets.
// Usage: node scripts/check-public-payload.cjs [baseUrl] [externalId...]
const base = process.argv[2] || "http://localhost:1337";
const ids = process.argv.slice(3);
const BAD = ["createdby", "updatedby", "password", "email", "token", "localizations"];
const walk = (value, path = "") => {
  if (Array.isArray(value)) return value.flatMap((item) => walk(item, path));
  if (value && typeof value === "object") return Object.entries(value).flatMap(([key, item]) => [path + key, ...walk(item, path + key + ".")]);
  return [];
};
(async () => {
  const urls = [`${base}/api/pecasauto/homepage`, ...ids.map((id) => `${base}/api/pecasauto/products/${encodeURIComponent(id)}`)];
  let failed = false;
  for (const url of urls) {
    const payload = await (await fetch(url)).json();
    const leaks = walk(payload.data).filter((key) => BAD.some((bad) => key.toLowerCase().includes(bad)));
    console.log(leaks.length ? "FAIL" : "PASS", url, leaks.join(",") || "");
    if (leaks.length) failed = true;
  }
  process.exit(failed ? 1 : 0);
})();
