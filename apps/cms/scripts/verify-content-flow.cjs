const { createStrapi } = require("@strapi/strapi");
const path = require("node:path");

async function main() {
  const appDir = process.cwd();
  const app = await createStrapi({ appDir, distDir: path.join(appDir, "dist") }).load();
  try {
    const homepageApi = app.documents("api::homepage.homepage");
    const before = await homepageApi.findFirst({ status: "published", populate: { pageBuilder: { populate: "*" } } });
    if (!before) throw new Error("Published homepage seed not found");
    const marker = `${before.title} · DRAFT FLOW CHECK`;
    await homepageApi.update({ documentId: before.documentId, data: { title: marker }, status: "draft" });
    const stillPublished = await homepageApi.findFirst({ status: "published" });
    if (stillPublished.title !== before.title) throw new Error("Draft leaked into published content");
    await homepageApi.publish({ documentId: before.documentId });
    const published = await homepageApi.findFirst({ status: "published", populate: { pageBuilder: { populate: "*" } } });
    if (published.title !== marker) throw new Error("Publish did not refresh content");
    if (!published.pageBuilder?.some(section => section.__component === "sections.hero")) throw new Error("Page builder hero missing");
    await homepageApi.update({ documentId: before.documentId, data: { title: before.title }, status: "draft" });
    await homepageApi.publish({ documentId: before.documentId });

    const productApi = app.documents("api::product-editorial.product-editorial");
    const product = await productApi.findFirst({ filters: { externalId: "PA-DIS-001" }, status: "published" });
    if (!product) throw new Error("Published product editorial seed not found");
    const originalDescription = product.shortDescription;
    await productApi.update({ documentId: product.documentId, data: { shortDescription: `${originalDescription} · EDIT CHECK` }, status: "draft" });
    const unchangedProduct = await productApi.findFirst({ filters: { externalId: "PA-DIS-001" }, status: "published" });
    if (unchangedProduct.shortDescription !== originalDescription) throw new Error("Product draft leaked into published content");
    await productApi.publish({ documentId: product.documentId });
    const changedProduct = await productApi.findFirst({ filters: { externalId: "PA-DIS-001" }, status: "published" });
    if (!changedProduct.shortDescription.endsWith("EDIT CHECK")) throw new Error("Product publish did not refresh");
    await productApi.update({ documentId: product.documentId, data: { shortDescription: originalDescription }, status: "draft" });
    await productApi.publish({ documentId: product.documentId });
    const publicProductShape = await productApi.findFirst({
      filters: { externalId: "PA-DIS-001" }, status: "published",
      populate: {
        brand: { fields: ["name", "slug"] }, category: { fields: ["name", "slug"] },
        images: { fields: ["name", "url", "alternativeText", "width", "height"] }, seo: true
      }
    });
    const publicJson = JSON.stringify(publicProductShape);
    for (const forbidden of ["createdBy", "updatedBy", "password", "resetPasswordToken", "registrationToken"]) {
      if (publicJson.includes(`\"${forbidden}\"`)) throw new Error(`Public product leaks ${forbidden}`);
    }

    console.log(JSON.stringify({
      status: "PASS",
      database: "PostgreSQL",
      homepage: "draft isolated, publish refreshed, restored",
      pageBuilder: "hero component present",
      productEditorial: "draft isolated, publish refreshed, restored",
      publicProductSecurity: "explicit populate allowlist; no admin user/password/token fields",
      operationalBoundary: ["price", "stock", "fitment", "orders"],
    }, null, 2));
  } finally {
    await app.destroy();
  }
  process.exit(0);
}

main().catch(error => { console.error(error); process.exit(1); });
