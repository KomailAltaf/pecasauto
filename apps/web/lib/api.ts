import { Product, SavedVehicle, SearchResponse, VehicleCandidate } from "./types";

export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Role = "customer" | "admin";
async function request<T>(path:string, options?:RequestInit, role?:Role):Promise<T> {
  const url = role ? `/api/platform${path.replace(/^\/api/,"")}` : `${API_URL}${path}`;
  const response = await fetch(url, { ...options, headers:{"Content-Type":"application/json", ...(options?.headers||{})}, cache:"no-store" });
  if (!response.ok) throw new Error((await response.json().catch(()=>({detail:"Erro de ligação"}))).detail || "Erro de ligação");
  return response.json();
}

export const api = {
  searchVehicle: (method:"registration"|"vin", value:string) => request<SearchResponse>("/api/vehicles/search", {method:"POST", body:JSON.stringify({method,value})}),
  demoConflict: () => request<SearchResponse>("/api/vehicles/demo/conflict"),
  manualVehicles: () => request<{source_type:string; vehicles:Record<string,any>}>("/api/vehicles/manual"),
  saveVehicle: (vehicle:VehicleCandidate & {nickname:string; registration?:string; vin?:string;match_method?:string;candidate_set?:VehicleCandidate[]}) => request<SavedVehicle>("/api/garage", {method:"POST", body:JSON.stringify(vehicle)}, "customer"),
  garage: () => request<SavedVehicle[]>("/api/garage", undefined, "customer"),
  removeVehicle: async (id:number) => { const response=await fetch(`/api/platform/garage/${id}`, {method:"DELETE"}); if(!response.ok) throw new Error("Não foi possível remover a viatura."); },
  products: (params="") => request<Product[]>(`/api/products${params}`),
  product: (id:string|number) => request<Product>(`/api/products/${id}`),
  oem: (reference:string) => request<Product[]>(`/api/search/oem?reference=${encodeURIComponent(reference)}`),
  providers: () => request<{source_type:string; providers:any[]}>("/api/providers", undefined, "admin"),
  dashboard: () => request<any>("/api/admin/dashboard", undefined, "admin"),
  createOrder: (payload:any) => request<{id:number;status:string;total:number;source_type:string}>("/api/orders", {method:"POST", body:JSON.stringify(payload)}, "customer"),
};
