import pathlib,json,base64,csv
from pyproj import Transformer
ROOT=pathlib.Path(__file__).resolve().parents[1]
def data_uri(path,mime):return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
network=json.loads((ROOT/'data/network-geo.json').read_text())
projects=json.loads((ROOT/'data/projects.json').read_text())
from editorial import apply_projects, apply_routes
apply_projects(projects); apply_routes(network['routes'])
project=Transformer.from_crs(4326,3310,always_xy=True)
inverse=Transformer.from_crs(3310,4326,always_xy=True)
for p in projects:
 x,y=project.transform(p['lon'],p['lat']);p['p']=[round(x/1000,3),round(-y/1000,3)]
geojson={'type':'FeatureCollection','name':'California 2024 State Rail Plan — generalized corridor interpretation','features':[]}
for r in network['routes']:
 cs=[list(inverse.transform(x*1000,-y*1000)) for x,y in r['coords']]
 geojson['features'].append({'type':'Feature','geometry':{'type':'LineString','coordinates':[[round(x,6),round(y,6)] for x,y in cs]},'properties':{'id':r['id'],'name':r['name'],'service_type':r['kind'],'geometry_note':r['geometryLabel'],'source_url':r['source']['url'],'source_page':r['source']['page'],'source_pdf_page':r['source']['pdfPage'],'source_document':r['source'].get('document','main plan'),'basis':'existing-inventory' if r.get('baseline') else 'planning-goal','service_goals':None if r.get('baseline') else r['phases'],'existing_inventory':r.get('inventory'),'notes':r['notes'],'discrepancy':r['conflict']}})
(ROOT/'data/vision-corridors.geojson').write_text(json.dumps(geojson,indent=2))
css=[]
for f in json.loads((ROOT/'data/fonts.json').read_text()):
 css.append(f"@font-face{{font-family:'{f['family']}';font-style:{f['style']};font-weight:{f['weight']};font-display:swap;src:url({data_uri(ROOT/f['path'],'font/ttf')}) format('truetype');}}")
brief=ROOT/'California-Rail-Electeds-Briefing.pdf'
data={'network':network,'geography':json.loads((ROOT/'data/geography.json').read_text()),'capital':json.loads((ROOT/'data/capital-projects.json').read_text()),'projects':projects,'geojson':geojson,'relief':data_uri(ROOT/'assets/relief.png','image/png'),'briefing':base64.b64encode(brief.read_bytes()).decode() if brief.exists() else ''}
html=(ROOT/'app.html').read_text().replace('__FONTS__','\n'.join(css)).replace('__CSS__',(ROOT/'style.css').read_text()).replace('__DATA__',json.dumps(data,separators=(',',':')).replace('</','<\\/')).replace('__JS__',(ROOT/'app.js').read_text())
assert not any(x in html for x in ['__FONTS__','__CSS__','__DATA__','__JS__'])
notices='\n\n'.join(p.name+'\n'+p.read_text() for p in sorted((ROOT/'licenses').glob('*.txt')))
html=html.replace('<head>', '<!-- Embedded font license notices\n'+notices.replace('--','- -')+'\n-->\n<head>',1)
(ROOT/'California-Rail-Atlas.html').write_text(html)
# Shareable source-linked CSVs use the same structured data as the live atlas.
service_rows=[]
for r in network['routes']:
 if r.get('baseline'):continue
 for y,ph in r['phases'].items():
  service_rows.append(dict(corridor_id=r['id'],corridor=r['name'],service_type=r['kind'],horizon=y,active=ph['active'],headway_minutes=ph['headway'] if ph['headway'] is not None else '',frequency=ph['label'],bound=ph['bound'] or '',detail=ph['detail'],source_page=r['source']['page'],source=r['source']['url'],geometry=r['geometryLabel'],notes=r['notes'],source_discrepancy=r['conflict'] or ''))
capital_rows=[dict(**r,source='https://dot.ca.gov/-/media/dot-media/programs/rail-mass-transportation/documents/california-state-rail-plan/20241203-appendices-a11y.pdf#page='+str(r['pdfPage'])) for r in data['capital']]
baseline_rows=[dict(route_id=r['id'],route=r['name'],service_type=r['kind'],basis='Existing service in the 2024 plan inventory — not a horizon target',inventory_year=r['inventory']['year'],frequency=r['inventory']['frequency'],full_route=r['inventory']['fullRoute'],detail=r['inventory']['detail'],source_pdf_page=r['source']['pdfPage'],source=r['source']['url'],geometry=r['geometryLabel'],notes=r['notes']) for r in network['routes'] if r.get('baseline')]
for filename,rows in [('service-goals.csv',service_rows),('long-distance-baseline.csv',baseline_rows),('capital-projects.csv',capital_rows)]:
 with (ROOT/'data'/filename).open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)

print('Standalone atlas:',len(html),'bytes; embedded PDF:',brief.exists())
