# Vehicle data: what works, what doesn't, and what to tell Fahad

**What is built.** Customer enters a plate or VIN → we normalise it (Portuguese plate formats, VIN structure) → a provider cascade chosen by environment variables (`VEHICLE_PROVIDER`, `AUTOWAYS_API_TOKEN`, …) → results become normalised candidate vehicles with a precision level (BASIC → ENGINE → EXACT_VARIANT) and a source → the customer confirms one → it is saved to their garage. The frontend only talks to our API, never to a provider. Nothing in this path is tied to one car: I ran it against a throwaway server that mimics Autoways' published response format, with only environment variables set, using several arbitrary plates and VINs (synthetic data, not real vehicles).

**Why a random plate or VIN does not work today.** No Portuguese plate provider is connected. The one live source (free vPIC, an American VIN database) returns the make only for European VINs. So the system correctly answers "waiting for plate provider" and offers manual selection.

**What is missing.** One credential. Adding a token for a plate/VIN provider (Autoways, Tips4y, Matricula.co.pt or TelePeças) is configuration, not a frontend rewrite. Untested on real vehicles until we have the token.

**What free data can do.** Check the VIN has a valid structure and name the manufacturer. **Where it stops:** model, engine, power and variant for European cars, and it cannot tell a real VIN from a made-up one. It is never treated as exact: free results are capped at BASIC and flagged "needs a second source".

**How cheap paid lookup fits.** Roughly €0.10–0.40 per plate (published prices, untested here). It returns make, model, engine, kW and often a K-Type. Results are marked unvalidated until cross-checked, and the customer confirms the car. Saved confirmed vehicles reduce repeat lookups.

**Multiple variants.** Normal. Every candidate is shown with its engine, power and source, each selectable, and the choice is stored with the candidates that were offered. *Known flaw:* two variants from one provider are currently labelled "sources disagree" (CONFLICT) instead of "several versions found" (MULTIPLE); Codex is to fix this.

**How K-Type connects the vehicle to catalogue data.** K-Type is TecDoc's vehicle ID; catalogues link parts to it. It is the bridge from "which car" to "which parts". A K-Type from a lookup provider is a candidate only, until a licensed catalogue or second source confirms it. Fitment (does this part fit that car) is a separate step and is **not built**: every product says "confirm compatibility".

**Where TecDoc fits later.** Behind the same catalogue and fitment interfaces: licensed K-Type, vehicle-to-part links, OE references. Customer screens do not change. Licence price: quote required.

**What David can safely tell Fahad.**
- "The lookup flow and safety rules are built; plate/VIN search will work as soon as we connect a provider, and we will test it on your cars first."
- "Until a licensed catalogue is connected, parts say 'confirm compatibility', never 'fits'."
- "Multiple versions are handled by asking the customer."

**What not to say.** That plate search already works; that parts are verified to fit; that any K-Type is verified; that prices or provider rights are settled; that partslink24 is integrated.
