# California, Connected
## A geographic, frequency-first atlas of the 2024 California State Rail Plan

**Start here:** Open `California-Rail-Atlas.html` in a modern browser, or visit the GitHub Pages site. No API key, internet connection or web server is required for the atlas itself. The source-document links need internet access.

This independent visualization is designed for elected officials and staff: understand the statewide service vision, inspect a corridor, and connect its service goals to the decisions and investments needed to implement it.

## Deliverables

- **`California-Rail-Atlas.html`** — the complete, self-contained interactive atlas, including the embedded briefing PDF and downloadable datasets. The Pages build publishes the same file as `index.html`.
- **`California-Rail-Electeds-Briefing.pdf`** — a four-page, US Letter briefing: geographic vision, frequency comparison, high-leverage dependencies and an elected-official agenda.
- **`data/service-goals.csv`** — 210 service-goal records: 70 corridor/service layers × three planning horizons.
- **`data/long-distance-baseline.csv`** — four existing Amtrak routes and inventory frequencies from Appendix 3.1, explicitly separate from future service goals.
- **`data/capital-projects.csv`** — 180 capital, grade-separation and fleet entries transcribed from Appendix 2.1–2.3, with source-page links.
- **`data/vision-corridors.geojson`** — generalized geographic corridor lines with source, goal/baseline classification, service-goal and existing-inventory metadata. Not engineering or navigation data. Alternate horizon-specific bus extents are held in the atlas's underlying network data.
- **[`California-Rail-Atlas-Package.zip`](California-Rail-Atlas-Package.zip)** — a portable bundle of the atlas, briefing, shareable data, this guide and attribution/license notices.

Downloads: [briefing PDF](California-Rail-Electeds-Briefing.pdf) · [service goals CSV](data/service-goals.csv) · [existing Amtrak baseline CSV](data/long-distance-baseline.csv) · [capital register CSV](data/capital-projects.csv) · [corridor GeoJSON](data/vision-corridors.geojson).

If your in-app file preview restricts downloads, use the separately supplied PDF/CSV files, or download the HTML and open it in a browser.

## Suggested first five minutes

1. Choose **“A six-part guide to the plan.”** The tour explains the network and finishes in Implementation.
2. Toggle **2028 / 2034 / 2050** to see how service goals change.
3. Keep **Frequency** selected to see how often the service is envisioned; switch to **Rail family** to distinguish high-speed/blended, intercity and regional roles.
4. Choose a regional view, search for a city, or click a corridor. Each corridor has a frequency, source, qualifications, implementation notes and related projects.
5. Visit **Implementation** for the phased program, role-specific actions and searchable capital register.

### Map controls

- Drag to pan; scroll to zoom. `+` and `−` zoom; the home button returns to the statewide view.
- The layers button controls service families, integrated buses, the gray **Amtrak long-distance** baseline (on by default), 25 delivery-priority markers, physical rail/freight context, counties, terrain and frequency labels.
- The map download button exports the current view as SVG.
- `/` opens search. Common abbreviations such as SLO, LA and SF are supported, and search includes all 180 capital entries as well as mapped places, routes and selected projects.
- `Esc` closes the active search or layer menu first, then the mobile detail sheet; it does not clear the selected route while closing a menu. With no overlay open, it clears a selection. With the map focused, arrow keys pan and `Home` resets.
- On phones, **Show map** closes the detail sheet without losing the selection. The Sources section remains available in the navigation.
- Role buttons in Implementation show only the relevant questions. Shared URLs restore the chosen page, horizon, and supported map region/color or capital entry.
- The **Corridor index** provides a keyboard-readable text alternative to selecting map lines.

## Read it correctly

**This is a 2024-plan interpretation, not a live 2026 status tracker.** The underlying plan is dated December 2024 and was released January 7, 2025. Later annual reports and project announcements are not mixed into its service vision. Prepared October 2026.

- **Horizon ≠ promised opening date.** 2028, 2034 and 2050 are the main plan's planning horizons.
- **Line ≠ funding commitment.** Existing rail geography does not prove the future service, capacity or funding is secured.
- **Dashed ≠ simply “unbuilt.”** Dashed lines denote conceptual/generalized geometry. Solid lines follow generalized physical rail corridors, including corridors proposed to carry new service.
- **Frequency ≠ timetable.** Targets are strategic service goals, usually per direction, not a promise at every station or between every pair of cities. Daily, limited, seasonal and qualitative goals are not converted into invented headways.
- **Visual hierarchy separates targets from context.** Limited/other and existing long-distance rail use fine strokes, below the 240-minute band’s weight—not an invented numeric frequency. Buses are gray and dotted in both color modes.
- **Overlapping layers are not automatically additive.** A regional and intercity layer may not be evenly spaced or stop at the same places. Explicit combined corridor goals are identified in the inspector.
- **Scope is selective and strategic.** There are 70 strategic goal layers, four existing Amtrak routes and 97 city/hub anchors, not every station or local bus. Urban transit is summarized through hub connections. Gray routes retain the 2024 Appendix 3.1 inventory: Coast Starlight, California Zephyr and Southwest Chief daily round trips; Sunset Limited three days per week. This baseline remains visible with every horizon, but is not a future-service pledge or a live timetable. Daily trains are not converted to regular headways. Physical rail context is not a freight-volume or active-passenger-service map.
- **Costs are planning figures.** Appendix costs are not current estimates, appropriations or remaining funding gaps. Package/component costs may overlap. The separate Section 130 inventory in Appendix 2.4 is not part of the 180-row register.
- **Actions are a synthesis.** Elected-official asks and project dependency interpretations are grounded in the plan, but are not verbatim agency directives or an official Caltrans endorsement.

### A visible source discrepancy

For **Santa Barbara–Los Angeles in 2050**, Table 1 (p. 38) describes coordinated hourly regional/intercity service. The narrative (p. 34) describes combined half-hourly service. The atlas uses **60 minutes from the table**, flags it with an asterisk, and preserves the discrepancy. Implementation planning should resolve it.

The plan's capital-program headline is **$307B**. The rounded appendix summary categories total about **$307.7B**. Neither figure is presented as money already secured.

## Sources and cartography

Primary sources:

1. [2024 California State Rail Plan](https://dot.ca.gov/-/media/dot-media/programs/rail-mass-transportation/documents/california-state-rail-plan/2024-ca-state-rail-plan-a11y.pdf): service tables pp. 37–38; service maps pp. 30–36; network principles pp. 15–20; implementation pp. 50–59.
2. [2024 appendices](https://dot.ca.gov/-/media/dot-media/programs/rail-mass-transportation/documents/california-state-rail-plan/20241203-appendices-a11y.pdf): Appendix 2.1–2.3 for the digitized capital register; Appendix 3.1 (PDF pp. 23–24) for the four existing long-distance Amtrak services.
3. [Official plan and annual-report page](https://dot.ca.gov/programs/rail/california-state-rail-plan): publication context and the place to check later progress.

Geography:

- California Albers, **EPSG:3310**. Geographic coordinates are reprojected for a statewide map; cities, coastlines and reference rail corridors are not rearranged into a schematic.
- [Caltrans California Rail Network GIS](https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHrailroad/California_Rail_Network/FeatureServer/0): existing physical corridor reference. Its historic service attributes are used to identify alignments, not as a live timetable.
- [Caltrans California Rail Stations GIS](https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHrailroad/California_Rail_Stations/FeatureServer/0): geographic reference for selected existing anchors. Proposed city/hub anchors remain approximate.
- Natural Earth: state/shoreline and lake geography (public domain).
- US Atlas: Census-derived cartographic county boundaries.
- Mapzen / Tilezen Terrain Tiles, AWS Open Data: terrain relief, reprojected and embedded for offline use. Relief is contextual and not an engineering elevation model.
- New corridors, tunnels, future alternatives and generalized interstate/bus links are explicitly distinguished from reference rail geometry. Close parallel services may be cartographically offset for legibility.

Fonts: DM Sans and Instrument Serif, distributed under the SIL Open Font License. Full notices are in `licenses/` and embedded as a comment in the standalone HTML.

## Source files and rebuilding

The workspace also contains modular source files (`app.html`, `style.css`, `app.js`), Python data/cartography/briefing scripts, and the intermediate audit datasets. These are not required to view or share the finished HTML. Explanatory project and selected-corridor copy is maintained separately in `content/editorial.json`; `scripts/editorial.py` restricts edits to independent narrative fields. The original appendix register is not copy-edited.

### Portable development and release

Requirements: Python 3.10+ and Node.js 20+ (CI uses Node 22 / Python 3.12). From the repository root:

```sh
python -m pip install -r requirements.txt
npm ci
npx playwright install chromium
npm run build          # briefing + self-contained atlas + Pages index.html
npm test               # data validation and desktop/mobile browser journeys
npm run preview        # http://localhost:3000 (serves index.html when built)
```

The Pages workflow builds and tests `index.html` as served from the site root before publishing the artifact. The atlas embeds its data, fonts, and briefing, and uses no root-relative application assets, so it works at the repository project-site path as well as offline. A repository administrator must first enable GitHub Pages in **Settings → Pages** and set **Build and deployment → Source** to **GitHub Actions**. The workflow cannot enable Pages itself with its restricted `GITHUB_TOKEN`; once enabled, merge to `main` or run the workflow manually to publish.

To re-create the network geometry from the local reference inputs, run `scripts/build_network.py`, `scripts/build_geography.py`, and `scripts/build_projects.py` first. The local Natural Earth input files are clipped to the study region to avoid shipping global data. `scripts/build_relief.py` downloads elevation tiles and fonts if needed.

Optional local preview:

```sh
python server.py
```

The server binds to `0.0.0.0:3000`. The HTML remains fully self-contained and does not use the server for any API calls.

## Quality checks

Automated browser checks cover the three horizons, regional views, rail-family colors, service/layer filters, search, the source-discrepancy card, the corridor index, the complete six-step tour, capital register search/filter/sort/expansion, role lenses, CSV/PDF/SVG downloads, map expansion, mobile layout and offline rendering. Data checks cover unique identifiers, source links, complete horizon records and finite geometries. These checks do not substitute for agency review of future operating or engineering plans.

The atlas explains the proposed service and the decisions needed to provide it. Its estimates, horizons and generalized geography should be checked against project-level studies before being used for delivery decisions.
