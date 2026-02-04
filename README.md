![Loaf Control Banner](photos/loaf-control-banner.jpeg)

# Loaf Control

Minimal sourdough baking log for tracking and analyzing loaves.

## Setup

```bash
make install
```

## Workflow

```bash
# Single loaf
make new NUM=6
# Edit loaves/loaf-006.yaml
make calculate NUM=6
make validate NUM=6

# Batch operations
make calculate              # All loaves
make validate               # All loaves
```

## How to Use

**Disclaimer:** This project is aggressively vibe-coded for one person's kitchen and should absolutely not be used as-is. If you're brave/foolish enough to try it anyway, edit `CLAUDE.md` to match your flour types, oven setup, and local conditions. The file exists to keep Claude (the AI assistant) aligned with your baking context - treat it as your personal sourdough knowledge base.

## Structure

```
loaves/          # One YAML per bake
photos/          # Crumb and crust photos
scripts/         # Analysis and utility scripts
template.yaml    # Reference template
Makefile         # Automation commands
```

## Key Concepts

**Sentinel Values:**
- `-1` = not tracked/measured (filter out in analysis)
- `0` = actually zero/skipped (e.g., no rye flour, no room proof)
- `""` = empty string for optional fields

**Quality Scale (1-5):**
Compare to YOUR previous bakes, not professional bakeries:
- 1 = inedible/failure
- 2 = edible but poor
- 3 = acceptable daily bread
- 4 = good, serve to guests
- 5 = best you've made so far

**Derived Fields:**
`hydration_pct`, `inoculation_pct`, `salt_pct` are auto-calculated from ingredient grams.

## Tips

- **Focus on quality_overall** - it's the most important field for correlations
- Track flour types precisely - mix ratios matter for flavor/texture
- Measure ambient_temp once at bulk ferment start (better than guessing average)
- Use bulk_end_state to capture fermentation readiness, not just time
- Proof sequence: room first, then fridge (0 for skipped stages)
- Take consistent photos (same lighting/angle) for future computer vision

## Units

- Weight: grams
- Temperature: celsius
- Time: hours (decimals like 4.5) for fermentation
- Duration: minutes for bake times
- Dates: YYYY-MM-DD
