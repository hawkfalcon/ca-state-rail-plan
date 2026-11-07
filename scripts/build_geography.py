import json,math,pathlib,collections
import numpy as np
from shapely.geometry import shape,LineString,MultiLineString,box,mapping
from shapely.ops import transform
from pyproj import Transformer
from scipy.spatial import cKDTree
import networkx as nx
ROOT=pathlib.Path(__file__).resolve().parents[1]
project=Transformer.from_crs(4326,3310,always_xy=True).transform
unproject=Transformer.from_crs(3310,4326,always_xy=True).transform
def pt(c):
 x,y=project(c[0],c[1]);return [round(x/1000,3),round(-y/1000,3)]
def svg_poly(geom):
 if geom.is_empty:return ''
 if geom.geom_type=='Polygon':
  rings=[geom.exterior]+list(geom.interiors)
  return ''.join('M'+'L'.join(f'{x/1000:.3f},{-y/1000:.3f}' for x,y in r.coords)+'Z' for r in rings)
 if hasattr(geom,'geoms'):return ''.join(svg_poly(g) for g in geom.geoms)
 return ''
def svg_line(geom):
 if geom.is_empty:return ''
 if geom.geom_type in ('LineString','LinearRing'):
  return 'M'+'L'.join(f'{x/1000:.3f},{-y/1000:.3f}' for x,y in geom.coords)
 if hasattr(geom,'geoms'):return ''.join(svg_line(g) for g in geom.geoms)
 return ''
clip=box(-126,31.0,-110,43.5)
# Geographic base layers are public-domain Natural Earth, projected to California Albers.
states=json.loads((ROOT/'sources/states.geojson').read_text())
features=[]
for f in states['features']:
 g=shape(f['geometry'])
 if not g.intersects(clip):continue
 g=transform(project,g.intersection(clip)).simplify(180,preserve_topology=True)
 features.append(dict(name=f['properties'].get('name'),country=f['properties'].get('admin'),d=svg_poly(g)))
lakes=[]
for f in json.loads((ROOT/'sources/lakes.geojson').read_text())['features']:
 g=shape(f['geometry'])
 if not g.intersects(clip):continue
 g=transform(project,g.intersection(clip)).simplify(140,preserve_topology=True)
 lakes.append(dict(name=f['properties'].get('name'),d=svg_poly(g)))
# Decode Census-derived us-atlas TopoJSON; retain California county boundaries only.
topo=json.loads((ROOT/'sources/counties.topojson').read_text())
sx,sy=topo['transform']['scale'];tx,ty=topo['transform']['translate']
def decode_arc(idx):
 rev=idx<0;arc=topo['arcs'][~idx if rev else idx];x=y=0;coords=[]
 for dx,dy in arc:x+=dx;y+=dy;coords.append([x*sx+tx,y*sy+ty])
 return coords[::-1] if rev else coords
ids=set()
def arcs(v):
 if isinstance(v,int):ids.add(v if v>=0 else ~v)
 else:
  for x in v:arcs(x)
for f in topo['objects']['counties']['geometries']:
 if str(f['id']).zfill(5).startswith('06'):arcs(f['arcs'])
county=''.join(svg_line(transform(project,LineString(decode_arc(i))).simplify(130)) for i in ids)
# Surveyed rail alignments from Caltrans. Routing is along a geographically filtered physical graph.
rail=json.loads((ROOT/'sources/rail-gis.geojson').read_text())['features']
cache={}
def match(f,sel):
 if not sel:return True
 p=f['properties']
 return bool((sel.get('pass') and sel['pass'] in (p.get('PASS_NETWO') or '')) or (sel.get('comm') and any(s in (p.get('COMM_NETWO') or '') for s in (sel['comm'] if isinstance(sel['comm'],list) else [sel['comm']]))) or ((p.get('SUBDIVISIO') or '') in sel.get('subs',[])) or ((p.get('ROW_OWNER') or '') in sel.get('owners',[])))
def graph(sel):
 key=json.dumps(sel,sort_keys=True)
 if key in cache:return cache[key]
 fs=[f for f in rail if match(f,sel)];G=nx.Graph()
 ends=[]
 for f in fs:
  geom=shape(f['geometry']);gs=[geom] if geom.geom_type=='LineString' else list(geom.geoms)
  for g in gs:
   g=transform(project,g).simplify(20)
   cs=[(round(x/5)*5,round(y/5)*5) for x,y in g.coords]
   ends.extend([cs[0],cs[-1]])
   for a,b in zip(cs,cs[1:]):
    if a!=b:G.add_edge(a,b,weight=math.dist(a,b),virtual=False)
 if not G:raise ValueError('No features for '+str(sel))
 ns=list(G.nodes);arr=np.array(ns);tree=cKDTree(arr)
 # GIS feature endpoints that differ slightly are connected within 120 m.
 for a in set(ends):
  for i in tree.query_ball_point(a,120):
   b=ns[i]
   if a!=b and not G.has_edge(a,b):G.add_edge(a,b,weight=math.dist(a,b),virtual=True)
 cache[key]=(G,ns,tree)
 return cache[key]
def path_for(nodes,sel):
 G,ns,tree=graph(sel)
 target=[];snaps=[]
 for lon,lat in nodes:
  xy=project(lon,lat);d,i=tree.query(xy);target.append(ns[i]);snaps.append(round(float(d)))
 coords=[];gaps=[]
 for start,end in zip(target,target[1:]):
  try:part=nx.shortest_path(G,start,end,weight='weight')
  except nx.NetworkXNoPath:
   # Only bridge small digitization gaps, explicitly record every gap for auditing.
   comp1=list(nx.node_connected_component(G,start));comp2=list(nx.node_connected_component(G,end))
   tr=cKDTree(np.array(comp2));ds,ix=tr.query(np.array(comp1));i=int(np.argmin(ds));a=comp1[i];b=comp2[ix[i]];dist=float(ds[i]);gaps.append(round(dist))
   if dist>3000:
    part=nx.shortest_path(G,start,a,weight='weight')+[b]+nx.shortest_path(G,b,end,weight='weight')[1:]
   else:
    H=G.copy();H.add_edge(a,b,weight=dist,virtual=True);part=nx.shortest_path(H,start,end,weight='weight')
  coords+=part if not coords else part[1:]
 if len(coords)<2:return [],snaps,gaps
 line=LineString(coords).simplify(110)
 return [[round(x/1000,3),round(-y/1000,3)] for x,y in line.coords],snaps,gaps
network=json.loads((ROOT/'data/network.json').read_text());city={c['id']:c for c in network['cities']}
for c in city.values():c['p']=pt([c['lon'],c['lat']])
# Explicit ordered generalized traces; these are NEVER advertised as engineered alignments.
traces={
 'transbay': ['oakland',[-122.304,37.807],[-122.349,37.802],[-122.394,37.789],'sf'],
 'transbay-regional':['sf',[-122.394,37.789],[-122.349,37.802],[-122.304,37.807],'oakland','coliseum'],
 'valley-link-west':['pleasanton',[-121.815,37.709],'livermore',[-121.655,37.722],'mountain-house'],
 'cross-valley':['lemoore',[-119.651,36.325],'kings',[-119.572,36.318],'visalia',[-119.133,36.30],'porterville'],
 'hsr-sac':['sacramento',[-121.46,38.43],[-121.33,38.18],'stockton','modesto','merced'],
 'hsr-merced-madera':['merced',[-120.391,37.239],[-120.299,37.10],[-120.163,36.966],'madera'],
 'hsr-valley-trunk':['madera',[-119.883,36.819],'fresno',[-119.79,36.68],[-119.72,36.50],'kings',[-119.58,36.19],[-119.519,35.977],[-119.338,35.71],[-119.286,35.64],[-119.11,35.46],'bakersfield'],
 'brightline':['rancho',[-117.54,34.137],[-117.443,34.273],[-117.420,34.357],[-117.367,34.445],[-117.294,34.524],'victor',[-117.024,34.846],[-116.675,34.965],[-116.36,35.08],[-115.92,35.39],[-115.55,35.68],[-115.33,35.88],'las-vegas'],
 'hsr-sd':['rancho',[-117.536,33.90],[-117.455,33.78],[-117.38,33.57],[-117.14,33.43],[-117.08,33.25],'escondido',[-117.108,32.948],[-117.18,32.805],'san-diego'],
 'bus-northcoast':['arcata',[-124.02,40.71],[-123.81,39.99],[-123.72,39.41],[-123.21,39.15],'cloverdale','healdsburg'],
 'bus-redding':['redding','chico','sacramento'],
 'bus-reno':['sacramento','roseville','auburn',[-120.75,39.25],[-120.18,39.33],'reno'],
 'bus-tahoe':['sacramento',[-120.80,38.73],[-120.18,38.80],'south-tahoe']
}
audit=[]
for r in network['routes']:
 ns=[[city[n]['lon'],city[n]['lat']] for n in r['nodes']]
 if r['geometry']=='rail':
  # Limit route via points to geography on the intended corridor; station anchors may denote future rather than existing stations.
  route_nodes=ns
  if r['id']=='north-valley':route_nodes=[ns[0],ns[1],[-121.556,39.136],[-121.694,39.366],ns[-1]]
  if r['id']=='valley-rail':route_nodes=[ns[0],[-121.403,38.17],*ns[1:]]
  if r['id']=='oakland-merced':route_nodes=[ns[0],ns[1],[-121.788,38.018],ns[2],[-120.917,37.667],ns[-1]]
  if r['id']=='valley-legacy':route_nodes=[ns[0],[-119.781,36.738],ns[2],[-119.01,35.373]]
  if r['id']=='north-bay-east':route_nodes=[ns[0],[-122.452,38.139],[-122.331,38.218],[-122.207,38.230],ns[-1]]
  if r['id']=='napa-branch':route_nodes=[[-122.291,38.225],ns[-1]]
  if r['id']=='vallejo-branch':route_nodes=[[-122.28,38.169],ns[-1]]
  if r['id']=='altamont':route_nodes=[ns[0],ns[1],[-121.427,37.701],ns[2],ns[3],ns[4]]
  if r['id']=='riverside-direct':route_nodes=[ns[0],[-117.810,34.059],ns[-1]]
  if r['id']=='coachella':route_nodes=[[-117.312,34.058],ns[1],ns[2]]
  if r.get('baseline'):
   # Trace each existing national-network train along its own historic GIS route
   # selection. Never send the Chief via the new Victor Valley HSR hub, or the
   # Starlight down the Peninsula. End at the available GIS boundary, with an
   # interstate continuation label rather than invented nationwide geometry.
   route_nodes=ns+[r['geometryEnd']]
  coords,snaps,gaps=path_for(route_nodes,r['selector'])
  r['coords']=coords;r['geometryLabel']='Caltrans rail GIS · generalized'
  if max(snaps,default=0)>5000 or max(gaps,default=0)>3000:
   r['geometryLabel']='Rail GIS with generalized connection(s)';r['hasGaps']=True
  if r['id']=='reno-seasonal':
   # Caltrans layer stops near the Nevada border. Append an openly generalized interstate tail.
   if coords:coords.extend([pt([-119.95,39.46]),city['reno']['p']]);r['hasGaps']=True;r['geometryLabel']='California rail GIS + generalized Nevada tail'
  audit.append({'id':r['id'],'snaps_m':snaps,'gaps_m':gaps,'points':len(coords)})
 else:
  if r['id'] in traces:seq=traces[r['id']]
  elif r.get('via'):seq=[r['nodes'][0]]+r['via']+[r['nodes'][-1]]
  else:seq=r['nodes']
  coords=[]
  for q in seq:
   coords.append(city[q]['p'] if isinstance(q,str) else pt(q))
  r['coords']=coords;r['geometryLabel']='Generalized bus connection' if r['geometry']=='bus' else 'Conceptual corridor · not a final alignment'
 # Frequency-varying bus extents in 2050, represented without pretending to be new rail.
 if r['id']=='bus-redding':r['coordsByYear']={'2050':[city['redding']['p'],city['chico']['p']]}
 if r['id']=='bus-northcoast':r['coordsByYear']={'2034':r['coords'][:-1],'2050':r['coords'][:-1]}
 if r['id']=='bus-crossvalley':r['coordsByYear']={'2028':r['coords']+[city['hanford']['p'],city['visalia']['p'],city['porterville']['p']],'2034':r['coords']+[city['kings']['p'],city['visalia']['p'],city['porterville']['p']]}
 # Map route should always be finite.
 assert len(r['coords'])>=2,r['id']
 assert all(math.isfinite(n) for pair in r['coords'] for n in pair)
# All California physical rail for the optional freight/rail context layer.
freight=[]
for f in rail:
 g=transform(project,shape(f['geometry'])).simplify(200)
 freight.append(svg_line(g))
base={'states':features,'lakes':lakes,'counties':county,'railContext':''.join(freight),'projection':'California Albers · EPSG:3310','worldBounds':[-490,-625,1000,810]}
(ROOT/'data/geography.json').write_text(json.dumps(base,separators=(',',':')))
(ROOT/'data/network-geo.json').write_text(json.dumps(network,separators=(',',':')))
(ROOT/'data/geometry-audit.json').write_text(json.dumps(audit,indent=2))
print('Geographic routes built:',len(network['routes']))
for a in audit:
 if max(a['snaps_m'],default=0)>3000 or max(a['gaps_m'],default=0)>1000:print('CHECK',a)
print('Base map',len(json.dumps(base)),'bytes')
