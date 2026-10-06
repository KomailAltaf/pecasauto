"use client";

import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, ArrowRight, ChevronRight, Database, Search } from "lucide-react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { SearchResponse, VehicleCandidate } from "@/lib/types";

type Tab = "registration" | "vin" | "manual" | "oem";
const tabs: [Tab, string][] = [["registration", "Matrícula"], ["vin", "VIN"], ["manual", "Selecionar veículo"], ["oem", "Referência / OEM"]];

export function VehicleSearch() {
  const [tab, setTab] = useState<Tab>("registration");
  const [value, setValue] = useState("");
  const [result, setResult] = useState<SearchResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [manual, setManual] = useState<any>(null);
  const [selection, setSelection] = useState<string[]>([]);
  const router = useRouter();

  useEffect(() => { api.manualVehicles().then(data => setManual(data.vehicles)).catch(() => {}); }, []);
  const placeholder = tab === "registration" ? "AB-12-CD" : tab === "vin" ? "Introduza os 17 caracteres" : "SAMPLE-BRAKE-001";

  const submit = async () => {
    setError("");
    if (!value.trim()) { setError("Introduza um valor para pesquisar."); return; }
    if (tab === "oem") { router.push(`/catalogo?q=${encodeURIComponent(value)}`); return; }
    if (tab === "manual") return;
    setBusy(true);
    try { setResult(await api.searchVehicle(tab, value)); }
    catch (caught: any) { setError(caught.message); }
    finally { setBusy(false); }
  };

  const loadDemoConflict = async () => {
    setError(""); setBusy(true);
    try { setResult(await api.demoConflict()); }
    catch (caught: any) { setError(caught.message); }
    finally { setBusy(false); }
  };

  const select = async (candidate: VehicleCandidate) => {
    try {
      await api.saveVehicle({
        ...candidate,
        nickname: "Meu Carro",
        registration: result?.input.method === "registration" ? result.input.value : undefined,
        vin: result?.input.method === "vin" ? result.input.value : undefined,
        match_method: "USER_CONFIRMED",
        candidate_set: result?.candidates || [candidate],
      });
      localStorage.setItem("pecasauto-active-vehicle-v2", JSON.stringify(candidate));
      router.push(`/catalogo?vehicle=${candidate.id}`);
    } catch (caught: any) { setError(caught.message); }
  };

  const manualOptions = useMemo(() => {
    if (!manual) return [];
    let node: any = manual;
    for (const item of selection) node = node?.[item];
    return Array.isArray(node) ? node : Object.keys(node || {});
  }, [manual, selection]);
  const manualLabels = ["Marca", "Modelo", "Geração", "Ano", "Motor"];
  const confirmManual = () => {
    const [make, model, generation, year, engine] = selection;
    select({ id: `manual-${make}-${model}-${engine}`, make, model, generation, year_range: year, engine, provider: "manual_demo", ktype_status: "NOT_AVAILABLE", precision: "ENGINE", verification_state: "USER_CONFIRMED_DEMO_DATA" });
  };
  const sourceClass = result?.source_type.toLowerCase().replaceAll("_", "-") || "";

  return <div className="search-shell" id="pesquisa">
    <div className="search-tabs">{tabs.map(([id, label]) => <button key={id} className={`search-tab ${tab === id ? "active" : ""}`} onClick={() => { setTab(id); setResult(null); setValue(""); }}>{label}</button>)}</div>
    <div className="search-body">
      {tab !== "manual" ? <>
        <div className="search-row"><div className="input-wrap"><Search size={20}/><input aria-label={tab} value={value} onChange={event => setValue(event.target.value)} placeholder={placeholder} onKeyDown={event => event.key === "Enter" && submit()}/></div><button className="btn red" onClick={submit} disabled={busy}>{busy ? "A procurar…" : "Encontrar peças"}<ArrowRight size={18}/></button></div>
        <p className="search-note"><strong>{tab === "registration" ? "PORTUGAL · LIVE PROVIDER REQUIRED" : tab === "oem" ? "PESQUISA DEMO" : "VALIDAÇÃO"}</strong> · A identificação do veículo não prova compatibilidade.</p>
        <button className="btn ghost small" onClick={loadDemoConflict} disabled={busy}>Carregar exemplo de conflito <span className="tag demo">DEMO CANNED RESULT</span></button>
      </> : <div>
        <div className="manual-steps">{manualLabels.map((label, index) => <div className="field" key={label}><label>{index + 1}. {label}</label><select className="select" value={selection[index] || ""} disabled={index > selection.length} onChange={event => setSelection([...selection.slice(0, index), event.target.value])}><option value="">Selecionar</option>{index === selection.length && manualOptions.map((item: string) => <option key={item}>{item}</option>)}{selection[index] && <option>{selection[index]}</option>}</select></div>)}</div>
        <p className="search-note"><strong>DEMO VEHICLE DATA</strong> · A seleção manual será ligada ao catálogo licenciado.</p>
        {selection.length === 5 && <button className="btn" onClick={confirmManual}>Confirmar veículo <ChevronRight size={18}/></button>}
      </div>}
      {error && <div className="warning-box">{error}</div>}
    </div>

    {result && <div className="vehicle-results">
      <div className="result-head"><div><span className={`tag ${sourceClass}`}>{result.source_type}</span><h2>{["CONFLICT", "MULTIPLE", "MORE_INFORMATION_REQUIRED"].includes(result.outcome) ? "Confirmação necessária" : "Resultado da identificação"}</h2><p>{result.message}</p></div>{result.outcome === "CONFLICT" && <AlertTriangle color="#a96d08" size={30}/>}</div>
      {result.source_type === "DEMO" && <div className="warning-box"><strong>DEMO CANNED RESULT</strong> · Estes candidatos não vieram de Auto Ways, TecDoc, vPIC ou qualquer outra API.</div>}
      {result.candidates.length > 0 && <div className="candidate-grid">{result.candidates.map(candidate => <article className="candidate" key={candidate.id}>
        <div style={{display:"flex", gap:8, flexWrap:"wrap"}}><span className="tag">{candidate.precision}</span><span className="tag demo">{candidate.verification_state}</span></div>
        <h3>{candidate.make} {candidate.model} {candidate.generation}</h3>
        <p>{candidate.year_range || "Ano por confirmar"} · {candidate.engine || "Motor por confirmar"} · {candidate.power_kw ? `${candidate.power_kw} kW` : "Potência por confirmar"} · {candidate.fuel || "Combustível por confirmar"}</p>
        <div className="candidate-meta"><span>Motor<br/><strong>{candidate.engine_code || "Por confirmar"}</strong></span><span>K-Type<br/><strong>{candidate.ktype ? `${candidate.ktype} (${candidate.ktype_status})` : "Não disponível"}</strong></span></div>
        <div className="candidate-footer"><span className="ktype">Fonte: {candidate.provider}</span>{["BASIC", "MODEL"].includes(candidate.precision) ? <button className="btn small" onClick={() => { const matchedMake = Object.keys(manual || {}).find(item => item.toLowerCase() === candidate.make?.toLowerCase()); setTab("manual"); setResult(null); setSelection(matchedMake ? [matchedMake] : []); }}>Completar manualmente</button> : <button className="btn small" onClick={() => select(candidate)}>Confirmar este veículo</button>}</div>
      </article>)}</div>}
      <details className="trace-panel"><summary><Database size={15}/> Ver painel de validação</summary><div className="trace-content"><div className="trace-step"><strong>INPUT</strong><span>{result.input.method}</span><span>{result.input.value}</span></div>{result.trace.map((step, index) => <div className="trace-step" key={index}><strong>{step.provider}</strong><span>{step.source_type} · {step.status}</span><span>{step.detail} {step.latency_ms ? `· ${Math.round(step.latency_ms)} ms` : ""}</span></div>)}<div className="trace-step"><strong>FITMENT</strong><span>NOT READY</span><span>Sem FitmentProvider licenciado, todos os produtos exigem confirmação.</span></div><pre className="trace-raw">{JSON.stringify(result.raw_provider_result, null, 2)}</pre></div></details>
    </div>}
  </div>;
}
