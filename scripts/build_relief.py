"""Offline relief from Mapzen/Terrain Tiles elevation (AWS Open Data), reprojected to EPSG:3310."""
import pathlib,requests,concurrent.futures,math,io,re
import numpy as np
from PIL import Image
from pyproj import Transformer
from scipy.ndimage import map_coordinates,gaussian_filter
ROOT=pathlib.Path(__file__).resolve().parents[1]
cache=ROOT/'sources/elevation';cache.mkdir(exist_ok=True)
z=6;x0,x1,y0,y1=9,12,23,26
mosaic=np.zeros(((y1-y0+1)*256,(x1-x0+1)*256),dtype=float)
def get(t):
 x,y=t;f=cache/f'{z}-{x}-{y}.png'
 if not f.exists():
  r=requests.get(f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png',timeout=40);r.raise_for_status();f.write_bytes(r.content)
 a=np.array(Image.open(f).convert('RGB')).astype(float)
 return x,y,(a[:,:,0]*256+a[:,:,1]+a[:,:,2]/256)-32768
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for x,y,a in ex.map(get,[(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)]):mosaic[(y-y0)*256:(y-y0+1)*256,(x-x0)*256:(x-x0+1)*256]=a
W,H=1240,1194
xs=np.linspace(-490,1000,W)*1000;ys=np.linspace(-625,810,H)*-1000
X,Y=np.meshgrid(xs,ys)
lon,lat=Transformer.from_crs(3310,4326,always_xy=True).transform(X,Y)
tx=(lon+180)/360*(2**z)*256-x0*256
ty=(1-np.arcsinh(np.tan(np.deg2rad(lat)))/np.pi)/2*(2**z)*256-y0*256
h=map_coordinates(mosaic,[ty,tx],order=1,mode='nearest')
h=gaussian_filter(h,0.65)
gy,gx=np.gradient(h,1200,1200)
# Multi-directional relief; only terrain variation is rendered, not a fabricated elevation surface.
slope=np.arctan(np.sqrt(gx**2+gy**2));aspect=np.arctan2(-gx,gy)
alt=np.deg2rad(42);az=np.deg2rad(315)
shade=np.sin(alt)*np.cos(slope)+np.cos(alt)*np.sin(slope)*np.cos(az-aspect)
shadow=np.clip((0.80-shade)*280,0,170)
# Increase ridge readability slightly while leaving flat valley floors almost unmarked.
shadow*=np.clip(np.sqrt(gx**2+gy**2)*8,0,1)
a=np.zeros((H,W,4),dtype=np.uint8);a[:,:,:3]=[69,79,66];a[:,:,3]=shadow.astype(np.uint8)
Image.fromarray(a).save(ROOT/'assets/relief.png',optimize=True)
print('Relief image created', (ROOT/'assets/relief.png').stat().st_size)
# Fonts, embedded in the self-contained deliverable; CSS is stored locally for reproducibility.
css=(ROOT/'sources/font.css').read_text()
fontfaces=[]
for idx,block in enumerate(css.split('@font-face')):
 if 'url(' not in block:continue
 url=re.search(r'url\(([^)]+)',block).group(1)
 r=requests.get(url,timeout=30);r.raise_for_status();f=ROOT/f'assets/font-{idx}.ttf';f.write_bytes(r.content)
 fontfaces.append({'family':re.search(r"font-family: '([^']+)'",block).group(1),'weight':re.search(r'font-weight: (\d+)',block).group(1),'style':'italic' if 'font-style: italic' in block else 'normal','path':str(f.relative_to(ROOT))})
import json
(ROOT/'data/fonts.json').write_text(json.dumps(fontfaces))
print('Fonts',len(fontfaces))
