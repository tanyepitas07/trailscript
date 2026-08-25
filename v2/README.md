# v2 — in progress

Live at `/v2/`. **v1 at the repository root is untouched**, so anything already
being demonstrated keeps working exactly as it did.

## What is new here

| | |
|---|---|
| **No limit on selections** | v1 capped it at four. Gone. |
| **Two sources, never merged** | OpenStreetMap *places* and AllTrails *routes* are separate tabs with separate badges. They describe different kinds of thing and merging them by name produces confident wrong pairings. |
| **Every AllTrails tag is a link** | Difficulty and length open the trail page, the rating and review count open `#trail-reviews`, and Photos opens `/photos`. All three URLs were verified to return 200 rather than assumed. |
| **Three ways to import routes** | A one-click bookmarklet, pasting the page text, or typing it in. All three run inside the clinician's own browsing, which is the only place the browser permits reading another site. |
| **Multi-endpoint live data** | Three Overpass endpoints tried in order, every attempt shown with its timing. `overpass-api.de` is tried first deliberately: it is the one that has failed. |
| **Seven-day forecast** | Full week on the clinician screen and on the handout, with the best two or three days named. |
| **Live weather warnings** | Active National Weather Service alerts, quoted in the government's own words with attribution. |
| **Conditions-driven precautions** | A baseline for everyone, plus additions triggered by heat, cold, air quality, UV, wind, and rain in the forecast. |
| **Comorbidities are multi-select** | And when two selections disagree — arthritis wants a soft surface, neuropathy wants a firm one — the conflict is shown to the clinician rather than silently resolved. |
| **Drive time, not straight-line miles** | Real driving minutes for the sites actually chosen. |
| **Fees, opening hours, lighting** | Already present in the map data and previously discarded. A parking fee and a 5pm gate are the two things most likely to defeat a prescription. |
| **The QR code says what it is** | "Driving directions — open your phone camera and point it at this square." |

## The rule that has not changed

Every clinical sentence is either quoted from a named source or is labelled as
an unreviewed draft. The clinician screen shows that labelling explicitly. The
patient handout attributes sources inline in ordinary words and never uses the
phrase "AI draft" — a deliberate difference in register, not in honesty.
