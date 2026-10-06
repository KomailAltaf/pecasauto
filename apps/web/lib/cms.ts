export const CMS_URL = process.env.STRAPI_URL || process.env.NEXT_PUBLIC_STRAPI_URL || "http://localhost:1337";

export type CmsHomepage = {
  title: string;
  intro?: string;
  pageBuilder?: Array<Record<string, any>>;
};

export async function getHomepageContent(): Promise<CmsHomepage | null> {
  try {
    const response = await fetch(`${CMS_URL}/api/pecasauto/homepage`, { cache: "no-store" });
    if (!response.ok) return null;
    const payload = await response.json();
    return payload.ownership === "EDITORIAL_ONLY" ? payload.data : null;
  } catch { return null; }
}

export async function getProductEditorial(externalId: string) {
  try {
    const response = await fetch(`${CMS_URL}/api/pecasauto/products/${encodeURIComponent(externalId)}`, { cache: "no-store" });
    if (!response.ok) return null;
    const payload = await response.json();
    return payload.ownership === "EDITORIAL_ONLY" ? payload.data : null;
  } catch { return null; }
}
