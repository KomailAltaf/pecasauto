"use client";
import { useParams } from "next/navigation";
import { AdminNav } from "@/components/AdminNav";

const content:Record<string,{title:string;description:string;items:string[]}>= {
  products:{title:"Products",description:"Demo catalogue management boundary.",items:["Product master data","OE and manufacturer references","Images and technical attributes","Category assignment"]},
  orders:{title:"Orders",description:"Orders created by the local demo checkout.",items:["Order status","Customer and delivery","Payment state","ERP synchronization later"]},
  vehicles:{title:"Vehicles",description:"Canonical identities and customer confirmations.",items:["Provider provenance","Candidate history","K-Type verification state","Saved vehicle profiles"]},
  inventory:{title:"Inventory",description:"Demo stock now; Primavera boundary later.",items:["Own warehouse stock","Supplier availability","Retail price","Delivery promise"]},
  integrations:{title:"Integrations",description:"Replaceable operational connectors.",items:["Primavera / Cegid","GLS","Payment provider","Supplier import jobs"]},
};
export default function AdminSection(){const {section}=useParams<{section:string}>();const page=content[section]||content.products;return <div className="admin-shell"><AdminNav/><section className="admin-content"><span className="tag demo">NOT BUILT · PLACEHOLDER</span><h1 className="section-title" style={{fontSize:46}}>{page.title}</h1><p className="section-copy">{page.description}</p><div className="warning-box"><strong>NOT BUILT:</strong> this page documents the intended module boundary only. It is not a working administration module.</div><div className="category-grid" style={{marginTop:30}}>{page.items.map((item,i)=><div className="category-card" key={item}><span className="tag">{String(i+1).padStart(2,"0")}</span><h3>{item}</h3><p>PLACEHOLDER · planned for the Phase 1 implementation.</p></div>)}</div></section></div>}
