# TrailScript

A clinician tool that turns "you should walk more" into a specific place a patient can go this week,
and puts it on the After Visit Summary.

Built for Loma Linda University School of Medicine, Advanced Integration Week 2026 (Lifestyle category).

**Live tool:** open `index.html`
**EHR launch:** open `launch.html`

---

## What problem this solves

Physical activity counselling is one of the highest-yield things a clinician can do and one of the
least reliably done. When it happens it usually ends at generic advice, which leaves the patient to
work out where to actually go. The After Visit Summary is the one artifact of the visit the patient
physically leaves with, and today it carries static text if it carries anything.

TrailScript takes a ZIP code and a few clinical constraints and returns real, currently-existing
local parks, trails and greenways, then produces a paste-ready block for the AVS.

## Two ways to run it, one codebase

**Path A - SMART on FHIR app.** `launch.html` performs a standard SMART EHR launch, reads the
patient's postal code from the FHIR `Patient` resource, and runs the search automatically. Verified
against the SMART reference sandbox at `launch.smarthealthit.org`. Registration in a production Epic
requires a client ID and a health-system security review.

**Path B - SmartPhrase plus a public link.** Any clinician can create a SmartPhrase in Epic in
minutes with no approval, no security review, and no build request. The phrase carries a link to
this tool and a single `***` wildcard that marks the paste target. The tool's output is plain ASCII
so it survives Epic's editor intact. This is the version that can be in use next month.

The patient-facing result is identical either way.

## What it does

- Resolves a US ZIP code to a coordinate **locally** from a bundled 42,555-entry table. The ZIP is
  never sent anywhere.
- Optionally accepts a nearby landmark to tighten the radius, which matters in San Bernardino County
  where a single ZIP can span many miles. That text goes to a public geocoder, so the field carries
  an explicit warning never to enter a patient's home address.
- Queries OpenStreetMap live via the Overpass API for parks, nature reserves, named paths and signed
  hiking routes, plus restrooms, drinking water, parking and benches, and matches amenities to sites
  within 400 m.
- Computes real trail length from route geometry and real elevation gain by sampling a terrain model
  along that geometry - for selected sites only, and only for linear features.
- Shows current air quality, today's high temperature and peak UV for the search area. In the Inland
  Empire these are clinical facts, not garnish.
- Pre-sets filters from a comorbidity profile, shows verbatim guideline text with its citation, and
  produces an AVS block plus a printable handout with driving-directions QR codes.

## Rules the code is built on

1. **Never state a fact the data does not contain.** Surface, lighting and wheelchair access are
   shown only where OpenStreetMap records them, and render as "not recorded" otherwise. The tool
   reports its own data coverage on every search - of 305 sites within 10 miles of the ZIP 92354 centroid (captured 25 Aug 2026), 275 (90.2%) carry no
surface tag and one records wheelchair access. The figure is radius-dependent - 90.0% at 5 mi,
85.0% at 15 mi, 77.7% at 25 mi.
2. **The clinician prescribes; the software does not.** Every clinical sentence is either a verbatim
   guideline quote shown with its citation, or is explicitly labelled as an unreviewed AI draft.
   There is nothing in between, and an automated test enforces the distinction.
3. **Read-only, no storage, no PHI.** The app requests `patient/Patient.read` and nothing else.

## Data sources

| What | Source | Licence |
|---|---|---|
| Parks, trails, paths, amenities | OpenStreetMap contributors via Overpass API | ODbL |
| Landmark geocoding | Nominatim (OpenStreetMap) | ODbL |
| Elevation | Open-Meteo elevation API (terrain model) | free tier, no key |
| Air quality, temperature, UV | Open-Meteo | free tier, no key |
| US ZIP centroids | `zipcodes` npm package, bundled | see package |
| Trail name lookups | AllTrails search links | AllTrails publishes no developer API; none of its data is scraped, stored or redistributed. Written confirmation of the scope of their approval is still outstanding |

## Testing

`test-planb.js` runs the real page in Chromium against live-captured fixtures.
**120 assertions, all passing** (22 for the Plan A build in `test-app.js`, 80 for this build in `test-planb.js`, 18 for the SMART on FHIR launch
in `test-smart.js`). **Seven deliberately planted defects** - a drifted guideline quote, a
removed draft banner, a broken ASCII filter, a park allowed to claim a trail length, and an
unlabelled clinical directive emitted outside the draft banner - each caused failures, so the
controls are known to work rather than merely present.

The last of those is worth its own note. An earlier version of the suite checked the comorbidity
data tables and passed while the shipped output printed unlabelled clinical directives on every
search. The test now reads the emitted text and fails if any clinical phrase falls outside the
quoted or drafted zones.

## Known limits

1. Overpass is a free community endpoint and rate-limits; the tool reports that plainly instead of
   showing an empty list.
2. Accessibility tagging in OpenStreetMap is extremely sparse. The tool never infers it.
3. US ZIP codes only.
4. This tool has never been used with a real patient and makes no outcome claim.

## Credits

Designed and built with Claude Opus 5 (Anthropic) as coding and drafting tool, under faculty
approval, August 2026. All clinical content requires clinician review before patient use.
