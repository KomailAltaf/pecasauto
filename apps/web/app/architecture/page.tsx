import { Boxes, CarFront, CreditCard, Database, FileText, Globe2, ServerCog, ShieldCheck, Truck, Warehouse } from "lucide-react";

export default function ArchitecturePage() { return <>
  <section className="page-hero"><div className="container"><span className="eyebrow" style={{color:"#83d3ad"}}>Internal product architecture</span><h1>Editorial content and operational truth stay separate.</h1><p>The customer application never depends directly on a vehicle-data provider, ERP or shipping service.</p></div></section>
  <section className="section"><div className="container"><div className="arch-flow">
    <div className="arch-node"><CarFront/><strong>Customer</strong><span>Matrícula · VIN · Manual · OEM</span></div><div className="arch-arrow">↓</div>
    <div className="arch-node"><Globe2/><strong>Next.js frontend</strong><span>Portuguese-first customer experience</span></div><div className="arch-arrow">↓ TWO CLEAR OWNERSHIP BOUNDARIES ↓</div>
    <div className="provider-cluster"><div><FileText/><strong>Strapi CMS</strong><br/><small>RENDERED NOW<br/>homepage hero · product editorial<br/>MODELLED, NOT RENDERED<br/>pages · navigation · footer · FAQ · SEO · promotions</small></div><div><ServerCog/><strong>FastAPI</strong><br/><small>OPERATIONAL TRUTH<br/>vehicle · fitment · price · stock · orders</small></div></div><div className="arch-arrow">↓</div>
    <div className="arch-node"><Database/><strong>Vehicle Identity Service</strong><span>Normalization · candidates · precision · provenance</span></div><div className="arch-arrow">↓ PROVIDER ADAPTERS ↓</div>
    <div className="provider-cluster"><div>Auto Ways<br/><small>NOT CONFIGURED</small></div><div>TIPS4Y<br/><small>DOCUMENTED</small></div><div>Matricula.co.pt<br/><small>NOT CONFIGURED</small></div><div>TelePeças<br/><small>WAITING</small></div><div>vPIC<br/><small>TESTED · BASIC</small></div><div>TecAlliance<br/><small>WAITING</small></div></div><div className="arch-arrow">↓</div>
    <div className="arch-node"><CarFront/><strong>Normalized vehicle</strong><span>Internal identity · explicit confirmation state</span></div><div className="arch-arrow">↓</div>
    <div className="arch-node"><ShieldCheck/><strong>K-Type / Catalogue vehicle / Fitment</strong><span>Separate decisions · no positive claim without a trusted source</span></div><div className="arch-arrow">↓</div>
    <div className="arch-node"><Boxes/><strong>Catalogue + inventory + price</strong><span>Demo now · TecDoc and suppliers later</span></div><div className="arch-arrow">↓</div>
    <div className="arch-node"><Warehouse/><strong>Primavera / Cegid</strong><span>Stock · prices · customers · orders · invoices</span></div><div className="arch-arrow">↓</div>
    <div className="arch-node"><CreditCard/><strong>Cart + checkout</strong><span>Server-calculated prices · payment boundary</span></div><div className="arch-arrow">↓</div>
    <div className="arch-node"><Truck/><strong>GLS</strong><span>NOT CONFIGURED · demo estimates only</span></div>
  </div>
  <div className="principle">TECDOC LATER <span>plugs into the provider layer.</span><br/>It does not require rebuilding the customer journey.</div>
  <div className="category-grid" style={{marginTop:28}}><div className="category-card"><span className="tag">STRAPI · LIVE NOW</span><h3>Rendered editorial</h3><p>Homepage hero and product editorial are published into the storefront now. Brands, categories and images support that content.</p></div><div className="category-card"><span className="tag demo">MODELLED · NOT RENDERED</span><h3>Future CMS surfaces</h3><p>Pages, navigation, footer, FAQs, SEO, banners and promotions have models but are not yet wired into customer routes.</p></div><div className="category-card"><span className="tag">FASTAPI</span><h3>Operational truth</h3><p>Identity, fitment, K-Type mapping, live price/stock, checkout rules, orders and integrations.</p></div></div>
  <div className="principle" style={{marginTop:28}}>FREE / OPEN PROVIDER <span>→ low-cost provider → customer confirmation → catalogue vehicle ID → trusted fitment source.</span></div>
  </div></section>
</>; }
