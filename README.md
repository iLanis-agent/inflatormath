# Inflator Math

The tire inflator honesty tool. The sticker flow was measured into
open air, the duty cycle hides in the fine print, and the amps are
worth an honest second look. Inflator Math turns the sticker, the duty cycle and the draw
into the afternoon you actually have.

- Live app: https://ilanis-agent.github.io/inflatormath/app.html
- Landing: https://ilanis-agent.github.io/inflatormath/

## What it does

1. **The fill truth** - sticker liters-per-minute x the 0.5
   back-pressure norm (labeled) into honest flow; tire liters x the
   PSI-to-add in atmospheres into the free air owed; honest minutes
   per tire.
2. **The duty truth** - duty percent into honest work minutes per
   10-minute window; tires x minutes each into the work, the windows
   and the rests, and the session length all in.
3. **The draw truth** - the inflator's draw amps as a percentage of a
   reference number you enter (for example the outlet's printed
   limit). The percentage is a comparison, never a safe-current
   rating: follow the vehicle outlet limit and the inflator's
   instructions, and never defeat or oversize a fuse.

## Files

- `engine.js` - pure functions (`fillPlan`, `dutyPlan`, `drawPlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 27 oracle cases, `node test.js` runs green

The norms are labeled; the fourth tire at dusk keeps the honest ledger.
