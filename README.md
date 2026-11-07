# California, Connected
## A geographic atlas of the 2024 California State Rail Plan

The 2024 plan describes a statewide rail network in three planning horizons. This atlas puts those service goals on a map and lets readers follow a corridor from its proposed frequency to the projects and operating decisions it may require. It is an independent reading of the plan, not a Caltrans publication or a record of current service.

Open `California-Rail-Atlas.html` or `index.html` in a modern browser to use the atlas offline. They are the same self-contained file; `index.html` is the entry point served by GitHub Pages from the root of `main`. The atlas embeds its fonts, data and briefing; links to source documents require an internet connection.

## Files and downloads

The main deliverable is the interactive atlas. The companion files are available here and in the download package:

- [Four-page elected-official briefing (PDF)](California-Rail-Electeds-Briefing.pdf)
- [Service goals (CSV)](data/service-goals.csv) — 210 records: 70 corridor/service layers across the 2028, 2034 and 2050 horizons.
- [Existing long-distance Amtrak service (CSV)](data/long-distance-baseline.csv) — the four routes listed in Appendix 3.1. This inventory is separate from the proposed service goals.
- [Capital register (CSV)](data/capital-projects.csv) — 180 entries transcribed from Appendices 2.1–2.3, with source-page links.
- [Generalized corridor lines (GeoJSON)](data/vision-corridors.geojson) — includes source references and distinguishes planning goals from existing-service inventory. It is not engineering or navigation data; horizon-specific bus extents are in the atlas data.
- [`California-Rail-Atlas-Package.zip`](California-Rail-Atlas-Package.zip) — atlas, briefing, data, this guide and attribution/license notices.

The atlas can also download its current map as SVG and export service, inventory and capital-register data. If a file preview blocks downloads, save the HTML file and open it in a browser.

## Getting around

Start with **A six-part guide to the plan** if you want an introduction. Otherwise, choose a horizon, search for a place or corridor, or use the regional buttons to move around the map. Select a line to see its frequency, source, qualifications and implementation notes. The **Implementation** view brings together the plan’s phased program, role-specific questions and searchable capital register. **Sources** collects the source material and cartographic notes.

A few useful controls:

- Drag to pan; scroll, `+` and `−` to zoom; use the home button to return statewide.
- The layers menu includes service families, integrated buses, the gray Amtrak long-distance inventory (on by default), delivery-priority markers, physical rail context, counties, terrain and frequency labels.
- Press `/` to search. Search recognizes common abbreviations, including SLO, LA and SF, and covers mapped places, routes, projects and all 180 capital entries. Use the arrow keys and Enter to select a result.
- Press `Esc` to close the active menu or search. With no overlay open, it clears the selection. With the map focused, the arrow keys pan and `Home` resets the view.
- On a phone, **Show map** closes the details sheet without clearing the selected corridor. Sources stays available in the navigation.
- The **Corridor index** is a text alternative to selecting lines on the map. Shared links restore supported views, horizons, colors and capital-register entries.

## How to read the map

This is an interpretation of the **2024 California State Rail Plan**, dated December 2024 and released January 7, 2025. It is not a live service or funding tracker. Later reports and project announcements have not been folded into the plan’s service vision. Prepared October 2026.

The three map horizons—2028, 2034 and 2050—are planning horizons, not promised opening dates. A line on the map does not establish that a service is funded, or that the necessary capacity is in place. Solid lines follow generalized physical rail corridors; dashed lines indicate conceptual or generalized geometry. Neither style is a construction-status key.

Frequencies are strategic goals, usually expressed per direction. They do not promise a train at every station or a particular timetable. Daily, seasonal, limited and qualitative services are left in those terms rather than converted to invented headways. Where regional and intercity layers overlap, their frequencies should not be added unless the plan gives a combined corridor goal: stops and departure times may differ.

The map includes 70 strategic goal layers, four Amtrak routes from the existing-service inventory, and 97 city and hub anchors. It is not a complete station list or a local-bus map. Urban transit appears through hub connections. Physical rail context is not a map of freight volume or active passenger service. Closely parallel services may be offset slightly to remain visible.

The gray Amtrak routes show the inventory in Appendix 3.1: daily round trips for the Coast Starlight, California Zephyr and Southwest Chief, and three days per week for the Sunset Limited. They remain visible across horizons for context; they are neither future service promises nor live timetable information. Daily trains are not translated into regular headways. Their fine gray strokes distinguish this inventory from the proposed frequency bands. Buses are gray and dotted in both color modes; limited and other services use fine strokes rather than an invented frequency.

Costs are planning figures, not current estimates, appropriations or remaining funding gaps; package and component costs may overlap. The plan gives a $307 billion capital-program headline, while its rounded appendix categories add to about $307.7 billion. Neither figure is money already secured. The 180-entry register does not include the separate Section 130 inventory in Appendix 2.4. The elected-official questions and project dependencies are an interpretation of the plan, not verbatim agency directives or a Caltrans endorsement.

### One discrepancy the map does not resolve

For Santa Barbara–Los Angeles in 2050, Table 1 (p. 38) describes coordinated hourly regional and intercity service; the narrative (p. 34) describes combined half-hourly service. The atlas follows the table’s 60-minute figure, marks it with an asterisk and notes the conflict. Service planning will need to resolve it.


## Sources and mapmaking

The main references are the [2024 California State Rail Plan](https://dot.ca.gov/-/media/dot-media/programs/rail-mass-transportation/documents/california-state-rail-plan/2024-ca-state-rail-plan-a11y.pdf) (service tables pp. 37–38; maps pp. 30–36; network principles pp. 15–20; implementation pp. 50–59) and its [appendices](https://dot.ca.gov/-/media/dot-media/programs/rail-mass-transportation/documents/california-state-rail-plan/20241203-appendices-a11y.pdf) (capital register, Appendices 2.1–2.3; existing-service inventory, Appendix 3.1, PDF pp. 23–24). See the [official plan and annual-report page](https://dot.ca.gov/programs/rail/california-state-rail-plan) for publication context and later progress reports.

The map uses California Albers (EPSG:3310). The Caltrans [rail network GIS](https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHrailroad/California_Rail_Network/FeatureServer/0) and [station GIS](https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHrailroad/California_Rail_Stations/FeatureServer/0) supply references for physical corridors and selected existing anchors; historic service attributes are not treated as a current timetable. Natural Earth supplies state, shoreline and lake geography; US Atlas supplies Census-derived county boundaries. Terrain relief comes from Mapzen/Tilezen Terrain Tiles hosted by AWS Open Data. It is contextual, not an engineering elevation model. Proposed corridors, tunnels, alternatives and bus links are distinguished from reference rail geography; proposed city and hub locations are approximate.

DM Sans and Instrument Serif are distributed under the SIL Open Font License. The notices are in `licenses/` and embedded in the standalone HTML. See [`ATTRIBUTION.md`](ATTRIBUTION.md) for the full attribution record.

## Build and test

The modular source is in `app.html`, `style.css` and `app.js`; explanatory project and corridor copy is in `content/editorial.json`. The capital-register wording is transcribed from the appendices and is not copy-edited. Python scripts prepare data and the briefing, then assemble the self-contained atlas.

Requirements: Python 3.10+ and Node.js 20+ (the workflow uses Python 3.12 and Node 22). From the repository root:

```sh
python -m pip install -r requirements.txt
npm ci
npx playwright install chromium
npm run build
npm test
npm run preview
```

`npm run build` regenerates the briefing and atlas, then refreshes `index.html`. Commit both HTML files when publishing a change; GitHub Pages serves the committed `index.html` from the root of `main`. `npm test` runs data validation and the desktop/mobile browser checks. `npm run preview` serves the built atlas at `http://localhost:3000`.

To regenerate network geometry from the local reference inputs, run `scripts/build_network.py`, `scripts/build_geography.py` and `scripts/build_projects.py` first. `scripts/build_relief.py` downloads elevation tiles and fonts when needed. The local Natural Earth inputs are clipped to the study region.

Pages is configured to publish from the root of `main` (**Settings → Pages → Deploy from a branch**). GitHub publishes the committed `index.html`; the Actions workflow separately rebuilds the atlas and runs data and browser checks on pushes and pull requests. The atlas should still be checked against project-level studies before being used for operating, engineering or delivery decisions.
