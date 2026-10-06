import { Disc3, Filter, PackageOpen } from "lucide-react";
export function PartVisual({kind,large=false}:{kind:string;large?:boolean}){
  const Icon=kind.includes("filter")?Filter:kind.includes("brake")?Disc3:PackageOpen;
  return <div className={`part-visual ${large?"large":""} ${kind}`}><span className="part-ring"/><Icon size={large?104:64} strokeWidth={1.25}/><small>DEMO IMAGE</small></div>
}
