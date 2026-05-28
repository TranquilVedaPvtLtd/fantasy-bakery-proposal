# Goal: Fantasy Bakery Proposal v2 — Locked Decisions Shipped

Ship the updated Fantasy Bakery custom-cake-platform proposal to GitHub Pages, reflecting all decisions locked with the principal in the brainstorming session on 2026-05-28.

## Locked decisions

1. **Setup price unchanged.** ₹3,55,000 platform + ₹20,000 WhatsApp = ₹3,75,000 total setup (excl. 18% GST). Payment 40/30/30 (kickoff / UAT / go-live + sign-off).
2. **Monthly retainer raised to ₹25,000/mo.** Platform line ₹10,000 → ₹15,000 (+50%, justified by AI ops layer: prompt tuning, theme library upkeep, generation quality watch, costing-rule maintenance). WhatsApp line unchanged at ₹10,000.
3. **Positioning Option B.** AI Cake Studio is the front door. A secondary "Shop ready-to-eat" track exists for cheesecakes / pastries / croissants but is NOT the hero. Pioneer-the-category narrative.
4. **Hybrid AI generation flow.** Pre-baked curated theme libraries (~25-40 hand-approved images per theme, 8-10 themes at launch) render instantly on theme select. A "Generate fresh designs" button triggers on-demand generation of 6 new variations (~90s wait). Customer's 3-iteration customization is fully on-demand.
5. **Hard cap at 3 iterations.** After iteration 3, the Customize button greys out; design at iteration 3 is the final spec; customer must Lock & Order or restart from theme library. No escape hatch.
6. **Raw-material recipe IP build from scratch.** 2-3 weeks of chef interviews, ingredient master, recipe-per-product capture, weighing trials, price lock. Runs parallel to front-end so it does NOT extend critical path. Framed as a value-add deliverable Vinayak owns.
7. **Visual reset: editorial cinematic.** Drop pastel-painterly; move to Bon Appétit + Cravings warm-premium-craft. New stills + new motion. NOT dark moody. NOT pastel pop.
8. **3 motion panels:** AI Cake Studio in action; Costing Engine live numbers; Job Card production handoff.
9. **Timeline: 12 weeks** (was 10-12 weeks).
10. **AI cost passes through to Vinayak at ~₹100-150 per custom order, zero markup.**

## Hard constraints

- Contact is Shruti only: `shruti@jarvisdaily.com` / `+91 9673758777`
- No "Vallabh" anywhere
- No em-dashes (—). Use hyphens (-)
- No M1 / M2 / M3 phase tags
- Data Ownership and Intellectual Property clause must remain present, three-point structure
- Address Vinayak Sanas only
- Pricing math must reconcile

## Phase plan

- **Phase 1 (fast, deterministic):** Update index.html pricing block to ₹25K/mo (₹15K platform + ₹10K WhatsApp), timeline to 12 weeks, sharpen AI flow copy (hybrid + hard cap 3), insert raw-material IP-build value-add framing. Run pricing math validation. Commit. Push. Verify live page reflects new pricing.
- **Phase 2 (visual pipeline):** Queue Higgsfield jobs for 6 new editorial stills + 3 motion panels via Cinema Studio V2. FFmpeg seamless-loop. Wire into HTML. Commit. Push. Verify.
- **Phase 3 (final QA):** Playwright headless verify, screenshot, confirm pricing math, no Vallabh, no em-dash, Vinayak addressed.

VERIFY: bash ralf/verify.sh
