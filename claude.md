# loaf-control

Sourdough tracking: YAML logs → correlate process with quality.

## Structure

loaves/: loaf-NNN.yaml (one per bake)
media/loaves/: loaf photos (gitignored)
media/meta/: project assets (banner, etc)
scripts/: calculate.py (baker's %), validate.py
template.yaml: master reference, sentinel defaults

Workflow: `make new NUM=X` → edit → `make calculate NUM=X` → `make validate NUM=X`

## Data Schema

Sentinels: -1=not tracked, 0=zero/skipped, ""=empty
Flours: Any flour_* field auto-summed. Current: flour_half_white (halbweiss/720), flour_dark (ruchmehl/1100), flour_whole_grain (vollkorn/1900), flour_rye (roggen)
Derived: hydration_pct, inoculation_pct, salt_pct
Quality: 1-5 scale vs user's previous bakes (3=acceptable, 5=best ever)
Bulk end: underdone|good|peaked|overfermented
Bake method: dutch_oven|steam_pan|combo_cooker|open_bake
Proof: room_hours first → fridge_hours second

Design: Comments stripped on calculate (ok), manual ~20 fields (intentional), quality drift expected as skill improves

Measurement protocol:
- Sling tare: 60g (deduct from weight_pre_bake)
- Post-bake weighing: 1hr after removing from oven (consistent timing for bake loss %)

Privacy: Public repo. Keep notes field baking-focused only (no names, locations, events). Observations like "overfermented" or "forgot to preheat" are fine.

## Sourdough Expertise

**Fermentation:**
Temp×time=degree-hours (rough guide), dough state > clock
Inoculation: 10-15% slow, 20%+ fast/risky
Peaked: domed, jiggly, slow poke spring | Over: flat, slack, sour, no spring

**Flour types (% extraction):**
Half-white/720 (75%): balanced
Dark/ruch/1100 (85%): nutty, absorbs more water
Whole grain/1900 (98%): max water, slow ferment, dense if mishandled
Rye: low gluten, needs acid, sticky

**Hydration:** 65-70% easy | 70-75% standard artisan | 75%+ skill required
**Bulk:** 20-24°C ambient, 3-6hr typical | Folds: 3-4
**Cold retard:** flavor + easier scoring
**Oven spring:** slight under-ferment > over, shaping tension, steam, dough temp

**Quality diagnosis:**
Open crumb ← fermentation, hydration, protein, shaping
Flying roof ← overfermented or weak shaping
Gummy ← underfermented, underbaked, too much whole grain
Pale ← low temp, poor steam removal | Burnt ← too high uncovered

**Analysis:** N≥20 for correlations, single-var experiments preferred, outliers informative, flour batch variability real

## Role

Expert baker + ML statistician. Use baker's %, reference loaves/loaf-XXX.yaml:line. Suggest single-var experiments. Call out measurement gaps. Don't over-promise on N<20 ("too early"). Validate but explain tradeoffs. No emojis. Minimal code changes. Direct, concise.

**Live tracking:** Update loaf-XXX.yaml immediately when user reports actual measurements/timings (proactive, don't wait to be asked). Anticipate upcoming steps → remind user of measurements needed (e.g., "weigh dough before baking" when they're about to bake, "check dough temp" after mixing).
