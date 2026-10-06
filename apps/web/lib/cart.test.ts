import { describe, expect, it } from "vitest";
import { addLine, cartSubtotal, shippingCost } from "./cart";

const product:any={id:1,price:20};
describe("cart",()=>{
  it("adds and increments a product",()=>expect(addLine(addLine([],product),product)[0].quantity).toBe(2));
  it("calculates subtotal and free shipping threshold",()=>{ const lines:any=[{product,quantity:4}]; expect(cartSubtotal(lines)).toBe(80); expect(shippingCost(80)).toBe(0); });
  it("charges no shipping for an empty cart",()=>expect(shippingCost(0)).toBe(0));
});
