# Inflator Math

The tire inflator honesty tool. The sticker flow was measured into
open air, the duty cycle hides in the fine print, and the fuse votes
last. Inflator Math turns the sticker, the duty cycle and the socket
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
3. **The socket truth** - socket fuse x the 0.8 norm (labeled) into
   honest amps; draw amps against the honest limit: holds, on the
   edge, or blows the fuse.

## Files

- `engine.js` - pure functions (`fillPlan`, `dutyPlan`, `socketPlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 27 oracle cases, `node test.js` runs green

The norms are labeled; the fourth tire at dusk keeps the honest ledger.
