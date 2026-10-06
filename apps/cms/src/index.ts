export default {
  register() {},
  async bootstrap({ strapi }) {
    const homepageApi = strapi.documents("api::homepage.homepage" as any);
    const homepage = await homepageApi.findFirst({ status: "published", populate: "*" } as any);
    if (!homepage) {
      const draft = await homepageApi.create({
        data: {
          title: "PeçasAuto",
          intro: "Conteúdo editorial gerido no Strapi. Pesquisa, fitment, preço e stock continuam no FastAPI.",
          pageBuilder: [
            {
              __component: "sections.hero",
              eyebrow: "Peças automóvel · Portugal",
              heading: "Encontre as peças certas para o seu carro.",
              body: "Identifique a viatura e confirme a compatibilidade antes da compra.",
              primaryLabel: "Encontrar peças",
              primaryHref: "#pesquisa"
            },
            {
              __component: "sections.feature-grid",
              heading: "Uma experiência simples, com a complexidade controlada por trás.",
              features: [
                { title: "Compatibilidade controlada", body: "Sem certezas positivas sem uma fonte autorizada.", icon: "shield" },
                { title: "Entrega", body: "Estimativas live pertencem ao backend operacional.", icon: "truck" },
                { title: "Apoio em português", body: "Confirmação humana quando os dados são incompletos.", icon: "support" }
              ]
            }
          ],
          seo: { metaTitle: "PeçasAuto — protótipo", metaDescription: "Protótipo local de ecommerce automóvel português.", noIndex: true }
        } as any,
        status: "draft"
      } as any);
      await homepageApi.publish({ documentId: draft.documentId } as any);
    }

    const categoryApi = strapi.documents("api::category.category" as any);
    let category = await categoryApi.findFirst({ filters: { slug: "travagem" }, status: "published" } as any);
    if (!category) {
      const draft = await categoryApi.create({ data: { name: "Travagem", slug: "travagem", description: "Conteúdo editorial demonstrativo." }, status: "draft" } as any);
      await categoryApi.publish({ documentId: draft.documentId } as any);
      category = await categoryApi.findFirst({ filters: { slug: "travagem" }, status: "published" } as any);
    }

    const brandApi = strapi.documents("api::brand.brand" as any);
    let brand = await brandApi.findFirst({ filters: { slug: "brembo" }, status: "published" } as any);
    if (!brand) {
      const draft = await brandApi.create({ data: { name: "Brembo", slug: "brembo", description: "Marca de demonstração editorial." }, status: "draft" } as any);
      await brandApi.publish({ documentId: draft.documentId } as any);
      brand = await brandApi.findFirst({ filters: { slug: "brembo" }, status: "published" } as any);
    }

    const productApi = strapi.documents("api::product-editorial.product-editorial" as any);
    const product = await productApi.findFirst({ filters: { externalId: "PA-DIS-001" }, status: "published" } as any);
    if (!product) {
      const draft = await productApi.create({
        data: {
          externalId: "PA-DIS-001",
          displayName: "Disco de travão — conteúdo editorial demo",
          shortDescription: "A descrição e as imagens são CMS; preço, stock e compatibilidade não são.",
          brand: brand?.documentId,
          category: category?.documentId,
          seo: { metaTitle: "Disco de travão demo", metaDescription: "Conteúdo de produto demonstrativo.", noIndex: true }
        } as any,
        status: "draft"
      } as any);
      await productApi.publish({ documentId: draft.documentId } as any);
    }
  }
};
