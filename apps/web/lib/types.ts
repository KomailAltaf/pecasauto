export type Precision = "BASIC" | "MODEL" | "ENGINE" | "EXACT_VARIANT";
export type FitmentState = "COMPATIBLE" | "CONFIRM_COMPATIBILITY" | "NOT_COMPATIBLE" | "UNKNOWN";

export interface VehicleCandidate {
  id: string; make?: string; model?: string; generation?: string; year_range?: string;
  engine?: string; engine_code?: string; power_kw?: number; fuel?: string; variant?: string;
  provider: string; external_vehicle_id?: string; ktype?: string;
  ktype_status: "VERIFIED" | "UNVERIFIED" | "CONFLICT" | "NOT_AVAILABLE";
  precision: Precision; verification_state: string;
}

export interface TraceStep { provider: string; status: string; detail: string; source_type: "REAL_TESTED" | "DEMO" | "MOCK" | "DOCUMENTED_CAPABILITY" | "WAITING_FOR_ACCESS" | "NOT_CONFIGURED" | "RESEARCH_ONLY"; latency_ms?: number; }
export interface SearchResponse { outcome: string; source_type: string; input: Record<string,string>; candidates: VehicleCandidate[]; trace: TraceStep[]; raw_provider_result?: unknown; message: string; may_claim_compatibility: boolean; }
export interface SavedVehicle extends VehicleCandidate { database_id: number; nickname: string; registration?: string; vin?: string; match_method?:string; candidate_set?:VehicleCandidate[]; }
export interface Product { id:number; brand:string; name:string; sku:string; manufacturer_reference:string; oe_references:string[]; ean:string; category:string; image_kind:string; price:number; iva_rate:number; stock:number; delivery_estimate:string; fitment_state:FitmentState; attributes:Record<string,string>; demo:boolean; }
export interface CartLine { product: Product; quantity: number; }
