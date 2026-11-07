"""Internal consistency checks, not a substitute for agency review of service plans."""
import json,math,pathlib,csv,xml.etree.ElementTree as ET
import pymupdf
ROOT=pathlib.Path(__file__).resolve().parents[1]
n=json.loads((ROOT/'data/network-geo.json').read_text());p=json.loads((ROOT/'data/projects.json').read_text());cap=json.loads((ROOT/'data/capital-projects.json').read_text())
assert len(n['routes'])==74 and len(n['cities'])==97
goals=[r for r in n['routes'] if not r.get('baseline')];baseline=[r for r in n['routes'] if r.get('baseline')]
assert len(goals)==70 and len(baseline)==4 and len(p)==25 and len(cap)==180
for records in [n['routes'],n['cities'],p,cap]:assert len({r['id'] for r in records})==len(records)
city_ids={r['id'] for r in n['cities']};project_ids={r['id'] for r in p};capital_ids={r['id'] for r in cap}
for r in n['routes']:
 assert set(r['phases'])=={'2028','2034','2050'},r['id']
 assert set(r['nodes'])<=city_ids and set(r['projects'])<=project_ids,r['id']
 assert r['source']['url'].endswith('#page='+str(r['source']['pdfPage'])),r['id']
 if r.get('baseline'):
  assert r['kind']=='longdistance' and r['source']['document']=='appendix'
  assert r['inventory']['year']==2024 and r['source']['pdfPage'] in [23,24]
  assert all(ph['headway'] is None and ph['label']==r['inventory']['frequency'] for ph in r['phases'].values())
 assert len(r['coords'])>=2 and all(math.isfinite(v) for xy in r['coords'] for v in xy),r['id']
 assert all(ph['headway'] in [None,15,30,60,120,240] for ph in r['phases'].values()),r['id']
for row in cap:
 assert isinstance(row['cost'],int) and row['cost']>0
 assert row['horizon'] in ['Near Term','Mid Term','Long Term']
 assert 6<=row['pdfPage']<=17
for row in p:assert row['capitalId'] in capital_ids,row['id']
for filename,count in [('service-goals.csv',210),('long-distance-baseline.csv',4),('capital-projects.csv',180)]:
 with (ROOT/'data'/filename).open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f));assert len(rows)==count;assert all(row['source'].startswith('https://dot.ca.gov/') for row in rows)
for a in json.loads((ROOT/'data/geometry-audit.json').read_text()):
 if a['id'].startswith('amtrak-'):assert not a['gaps_m'] and max(a['snaps_m'])<1500,a
gj=json.loads((ROOT/'data/vision-corridors.geojson').read_text())
assert len([f for f in gj['features'] if f['properties']['basis']=='existing-inventory' and f['properties']['service_goals'] is None])==4
assert len(pymupdf.open(ROOT/'California-Rail-Electeds-Briefing.pdf'))==4
pdf=pymupdf.open(ROOT/'California-Rail-Electeds-Briefing.pdf')
for i,page in enumerate(pdf):
 for b in page.get_text('blocks'):
  assert b[0]>=20 and b[2]<=592 and b[1]>=10 and b[3]<=780,(i+1,b[:4])
exp=ROOT/'assets/qa-export.svg'
if exp.exists():ET.parse(exp)
result={'route_layers':74,'goal_layers':70,'existing_amtrak_routes':4,'cities_hubs':97,'horizon_records':210,'delivery_priorities':25,'capital_rows':180,'briefing_pages':4,'unique_ids':True,'source_links':True,'valid_geometries':True,'pdf_text_within_page_bounds':True,'svg_export_well_formed':exp.exists()}
(ROOT/'data/validation-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
