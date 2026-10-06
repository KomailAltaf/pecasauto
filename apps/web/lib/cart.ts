import { CartLine, Product } from "./types";

export function addLine(lines:CartLine[], product:Product):CartLine[] {
  const found = lines.find(line=>line.product.id===product.id);
  return found ? lines.map(line=>line.product.id===product.id?{...line,quantity:line.quantity+1}:line) : [...lines,{product,quantity:1}];
}
export const cartSubtotal = (lines:CartLine[]) => lines.reduce((sum,line)=>sum+line.product.price*line.quantity,0);
export const shippingCost = (subtotal:number) => subtotal <= 0 ? 0 : subtotal >= 75 ? 0 : 4.90;
