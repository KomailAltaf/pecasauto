"use client";

import Link from "next/link";
import { CarFront, Plus, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { SavedVehicle } from "@/lib/types";

export default function GaragePage() {
  const [vehicles, setVehicles] = useState<SavedVehicle[]>([]);
  const load = () => api.garage().then(setVehicles).catch(() => {});
  useEffect(() => { void load(); }, []);
  const remove = async (id: number) => { await api.removeVehicle(id); void load(); };
  const activate = (vehicle: SavedVehicle) => localStorage.setItem("pecasauto-active-vehicle-v2", JSON.stringify(vehicle));
  return <>
    <section className="page-hero"><div className="container"><span className="eyebrow" style={{color:"#83d3ad"}}>Conta demonstrativa</span><h1>Meu Carro</h1><p>Guarde veículos confirmados e reutilize-os sem repetir o percurso de identificação.</p></div></section>
    <section className="section"><div className="container"><div className="garage-grid">
      {vehicles.map(vehicle => <article className="garage-card" key={vehicle.database_id}><div className="garage-icon"><CarFront/></div><span className="tag">{vehicle.verification_state}</span><h2>{vehicle.nickname}</h2><strong>{vehicle.make} {vehicle.model} {vehicle.generation}</strong><p>{vehicle.engine} · {vehicle.power_kw} kW · {vehicle.fuel}<br/>K-Type: {vehicle.ktype || "não disponível"} · {vehicle.provider}</p><div className="product-actions"><Link href="/catalogo" className="btn small" onClick={() => activate(vehicle)}>Ver peças</Link><button className="btn ghost small" onClick={() => remove(vehicle.database_id)}><Trash2 size={16}/> Remover</button></div></article>)}
      <article className="garage-card" style={{display:"grid",placeItems:"center",textAlign:"center",minHeight:240}}><div><Plus size={38}/><h2>Adicionar veículo</h2><p>Use matrícula, VIN ou seleção manual.</p><Link href="/#pesquisa" className="btn ghost">Identificar veículo</Link></div></article>
    </div></div></section>
  </>;
}
