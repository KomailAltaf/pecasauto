"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { SlidersHorizontal } from "lucide-react";
import { api } from "@/lib/api";
import { Product, VehicleCandidate } from "@/lib/types";
import { ProductCard } from "@/components/ProductCard";

const brands = ["BOSCH", "BREMBO", "TRW", "ATE", "MANN-FILTER", "MAHLE", "VALEO", "FEBI"];

function Catalogue() {
  const params = useSearchParams();
  const [products, setProducts] = useState<Product[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [stock, setStock] = useState(false);
  const [sort, setSort] = useState("brand");
  const [vehicle, setVehicle] = useState<VehicleCandidate | null>(null);
  const [error, setError] = useState("");
  const q = params.get("q") || "";
  const category = params.get("category") || "";
  useEffect(() => { try { setVehicle(JSON.parse(localStorage.getItem("pecasauto-active-vehicle-v2") || "null")); } catch {} }, []);
  useEffect(() => {
    const query = q ? `?q=${encodeURIComponent(q)}` : category ? `?category=${encodeURIComponent(category)}` : "";
    api.products(query).then(setProducts).catch(caught => setError(caught.message));
  }, [q, category]);
  const shown = useMemo(() => products
    .filter(product => (!selected.length || selected.includes(product.brand)) && (!stock || product.stock > 0))
    .sort((a, b) => sort === "price" ? a.price - b.price : a.brand.localeCompare(b.brand)), [products, selected, stock, sort]);

  return <>
    <section className="page-hero"><div className="container"><span className="eyebrow" style={{color:"#83d3ad"}}>Catálogo demonstrativo</span><h1>{category || q ? `Resultados para ${category || q}` : "Peças automóvel"}</h1><p>Produto, preço, stock, entrega e fitment são dados demonstrativos.</p></div></section>
    <section className="section"><div className="container">
      {vehicle && <div className="vehicle-context"><div><strong>Catálogo aberto com {vehicle.make} {vehicle.model} {vehicle.generation}</strong><span>{vehicle.engine} · {vehicle.power_kw} kW · compatibilidade ainda por verificar</span></div><span className="tag demo">VEÍCULO CONFIRMADO · FITMENT NÃO VERIFICADO</span></div>}
      <div className="catalogue-layout"><aside className="filter-panel"><h3><SlidersHorizontal size={18}/> Filtrar</h3><div className="filter-group"><strong>MARCA</strong>{brands.map(brand => <label className="check" key={brand}><input type="checkbox" checked={selected.includes(brand)} onChange={() => setSelected(value => value.includes(brand) ? value.filter(item => item !== brand) : [...value, brand])}/>{brand}</label>)}</div><div className="filter-group"><strong>DISPONIBILIDADE</strong><label className="check"><input type="checkbox" checked={stock} onChange={event => setStock(event.target.checked)}/>Em stock</label></div><div className="filter-group"><strong>COMPATIBILIDADE</strong><p className="search-note">Sem FitmentProvider ligado: todos os produtos exigem confirmação.</p></div></aside>
        <div><div className="catalogue-head"><div><h1>{shown.length} produtos</h1><p>Amostras para testar pesquisa, catálogo e checkout.</p></div><select className="select" value={sort} onChange={event => setSort(event.target.value)}><option value="brand">Ordenar por marca</option><option value="price">Preço mais baixo</option></select></div>{error && <div className="warning-box">{error}</div>}<div className="product-grid">{shown.map(product => <ProductCard key={product.id} product={product}/>)}</div></div>
      </div>
    </div></section>
  </>;
}

export default function CataloguePage() { return <Suspense><Catalogue/></Suspense>; }
