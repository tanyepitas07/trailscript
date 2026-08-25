# preview/ — prototypes, not the product

Nothing in here is shipped. These are working mockups built to settle a design
question before v2 is implemented, and they are deliberately public so they can
be opened and argued with from any machine.

| File | What it is for |
|---|---|
| `clinic-strip.html` | The layout chosen from four candidates: a short fixed map above a dense list, with a pinned Done bar. Also the first working demonstration of the multi-endpoint failover for live map data. |
| `alltrails-options.html` | Four routes for bringing AllTrails data in, each tested against the live site rather than assumed. Carries the evidence for why two of them are dead. |

`clinic-strip.html` tries `overpass-api.de` **first and on purpose**, because that
host is unreachable from the network this project is developed on. Watching it
fail and then succeed against `overpass.openstreetmap.fr` is the point of the
prototype - the endpoint readout in the bottom-left of the map records every
attempt with its timing.
