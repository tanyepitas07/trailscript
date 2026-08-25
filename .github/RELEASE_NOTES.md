TrailScript for Loma Linda University School of Medicine, Advanced Integration Week 2026.

## Which file do I want?

**Just want to try it?** Download **`TrailScript-standalone.html`** and double-click it. One file,
nothing else needed - the 42,555 US ZIP codes, the offline site copy and the QR code generator are
all inside it. No install, no server, no folder to unzip.

| File | What it is | Open which file |
|---|---|---|
| `TrailScript-standalone.html` | The whole clinician tool as a single file. | itself |
| `TrailScript-clinician-tool.zip` | The same tool as separate files. | `index.html` |
| `TrailScript-epic-smart-app.zip` | The version that launches inside an EHR. | `launch.html` |

**Do not** use the per-file **Download raw file** button on `index.html` in the repository.
`index.html` loads four scripts that sit beside it, so downloading it on its own leaves it with none
of them. It will open, look normal, and reject every ZIP code you type while claiming a ZIP table of
42,555 entries that is not in fact loaded. This release exists so that nobody has to hit that.

## Known issue in this version

The live OpenStreetMap lookup uses `overpass-api.de`. On some networks - university and hospital
networks especially - that host is unreachable and the tool falls back to a bundled offline copy of
the Loma Linda region. It says so on screen and in the printed text, but the wording reads like a
temporary outage rather than a network block.

Measured 25 Aug 2026: on a network where `overpass-api.de` failed six times out of six,
`overpass.openstreetmap.fr` answered the identical query in 2.0 s. Multi-endpoint failover is the
fix and is not in this release.

## What it does

Takes a patient's ZIP code and returns real local parks, trails and greenways from OpenStreetMap,
ranked by distance, with current air quality, temperature and UV. The clinician picks up to four and
the tool produces a plain-text block for the After Visit Summary plus a printable handout with
driving-directions QR codes.

Read-only. No patient data is stored or transmitted. Every clinical sentence is either a verbatim
guideline quote shown with its citation, or is visibly labelled as an unreviewed AI draft.
