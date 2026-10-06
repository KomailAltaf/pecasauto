declare const strapi: any;

// Public payloads must never include admin-user audit relations (createdBy/updatedBy) or internal keys.
const STRIP_KEYS = new Set(["createdBy", "updatedBy", "localizations", "password", "resetPasswordToken", "registrationToken"]);
export function sanitizePublicContent(value: any): any {
  if (Array.isArray(value)) return value.map(sanitizePublicContent);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).filter(([key]) => !STRIP_KEYS.has(key)).map(([key, item]) => [key, sanitizePublicContent(item)]));
  }
  return value;
}

export default {
  async homepage(ctx) {
    ctx.body = {
      source: "STRAPI_CMS",
      ownership: "EDITORIAL_ONLY",
      data: sanitizePublicContent(await strapi.documents("api::homepage.homepage" as any).findFirst({ status: "published", populate: { pageBuilder: { populate: "*" }, seo: true } } as any))
    };
  },
  async product(ctx) {
    ctx.body = {
      source: "STRAPI_CMS",
      ownership: "EDITORIAL_ONLY",
      excludedOperationalFields: ["price", "stock", "fitment", "orders"],
      data: sanitizePublicContent(await strapi.documents("api::product-editorial.product-editorial" as any).findFirst({
        filters: { externalId: ctx.params.externalId }, status: "published",
        populate: {
          images: { fields: ["name", "url", "alternativeText", "width", "height"] },
          seo: true,
          brand: { fields: ["name", "slug"] },
          category: { fields: ["name", "slug"] }
        }
      } as any))
    };
  }
};
