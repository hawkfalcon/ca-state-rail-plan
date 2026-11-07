# Sources, attribution and scope

This is an independent explanatory work. No endorsement by Caltrans, CalSTA, the California High-Speed Rail Authority, transit operators or local governments is implied. Caltrans logos and branding are not used.

## Service vision and capital program

California Department of Transportation, **2024 California State Rail Plan**, December 2024, released January 7, 2025. Primary interpretation follows the service tables (pp. 37–38), supplemented by service maps and narrative (pp. 30–36), design principles (pp. 15–20) and implementation material (pp. 50–59).

[Official plan PDF](https://dot.ca.gov/-/media/dot-media/programs/rail-mass-transportation/documents/california-state-rail-plan/2024-ca-state-rail-plan-a11y.pdf)

[Official appendix PDF](https://dot.ca.gov/-/media/dot-media/programs/rail-mass-transportation/documents/california-state-rail-plan/20241203-appendices-a11y.pdf)

The register digitizes 180 entries from Appendix 2.1–2.3, preserving original project descriptions, agencies and costs. Cost numbers are planning figures, not current budgets, appropriations or funding gaps. Package and component costs can overlap. The Section 130 inventory is not included.

The four gray long-distance Amtrak routes use the **existing-service inventory in Appendix 3.1, PDF pp. 23–24**: daily Coast Starlight, California Zephyr and Southwest Chief round trips, and Sunset Limited operating three days per week. These are 2024 baseline descriptions, not newly assigned horizon targets or current timetable verification. The layer is held constant across horizon views solely for context, with California rail-GIS extents and interstate continuation labels rather than a drawn national alignment. It is exported separately from the 210 service-goal records.

## Physical geography

- **Caltrans California Rail Network**: reference rail alignments, selected and generalized for a statewide atlas. Historic operator/route attributes are used only to select geographic corridors. They are not a live service inventory. [GIS layer](https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHrailroad/California_Rail_Network/FeatureServer/0)
- **Caltrans California Rail Stations**: geographic reference for selected station/city anchors. Not a complete station inventory. [GIS layer](https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHrailroad/California_Rail_Stations/FeatureServer/0)
- **Natural Earth**: public-domain state/shoreline and lake geography, generalized to map scale. [naturalearthdata.com](https://www.naturalearthdata.com/)
- **US Atlas**: Census-derived cartographic county boundaries. [us-atlas](https://github.com/topojson/us-atlas)
- **Mapzen / Tilezen Terrain Tiles**: terrain context from the public elevation tile collection on AWS Open Data, reprojected and rendered as relief for offline display. Underlying elevations draw on USGS, NASA and other source datasets; not an engineering surface. [Terrain Tiles](https://registry.opendata.aws/terrain-tiles/) · [Source attribution](https://github.com/tilezen/joerd/blob/master/docs/attribution.md)

Projection: California Albers, EPSG:3310. Lines are generalized and close overlapping service layers may be offset cartographically. Dashed geometry indicates a conceptual/generalized connection, not a selected engineering alignment or a uniform project status. Existing rail geometry does not imply secured funding or approval for future passenger service. Future hub anchors are approximate.

## Typefaces

- **DM Sans**, SIL Open Font License. Full notice: `licenses/DM-Sans-OFL.txt`.
- **Instrument Serif**, SIL Open Font License. Full notice: `licenses/Instrument-Serif-OFL.txt`.

Font notices are also embedded as an HTML comment in the standalone atlas. No external font network requests are made by the finished atlas.

## Interpretation and known discrepancy

Service goals are operator-neutral, strategic and horizon-specific. Daily, seasonal and qualitative frequencies are not silently converted into regular intervals. Some frequencies are corridor aggregates or map bands, not each train's stopping pattern. The atlas does not add overlapping service layers to imply uniformly spaced combined service.

The long-term Santa Barbara–Los Angeles frequency differs between Table 1 (hourly) and the p. 34 narrative (half-hourly). The atlas uses the table's 60-minute value and flags the difference. Other map-band interpretations and geographic qualifications are documented on the relevant corridor cards.

Implementation asks and dependency narratives are an explanatory synthesis, not official or verbatim agency directives. This edition interprets the 2024 plan; it intentionally does not blend in later project-status or grant updates.
