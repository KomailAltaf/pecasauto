import { CheckCircle2, CircleHelp, ShieldAlert, XCircle } from "lucide-react";
import { FitmentState } from "@/lib/types";
const copy:Record<FitmentState,string>={COMPATIBLE:"Compatível",CONFIRM_COMPATIBILITY:"Confirmar compatibilidade",NOT_COMPATIBLE:"Não compatível",UNKNOWN:"Compatibilidade por verificar"};
export function FitmentBadge({state}:{state:FitmentState}){const Icon=state==="COMPATIBLE"?CheckCircle2:state==="NOT_COMPATIBLE"?XCircle:state==="UNKNOWN"?CircleHelp:ShieldAlert;return <span className={`fitment ${state.toLowerCase()}`}><Icon size={16}/>{copy[state]}</span>}
