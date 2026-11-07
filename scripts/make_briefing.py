import pathlib,json,re,math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
ROOT=pathlib.Path(__file__).resolve().parents[1]
for f in json.loads((ROOT/'data/fonts.json').read_text()):
 name=('SerifI' if f['style']=='italic' else 'Serif') if f['family']=='Instrument Serif' else ('Sans'+f['weight'])
 pdfmetrics.registerFont(TTFont(name,str(ROOT/f['path'])))
pdfmetrics.registerFontFamily('Sans400',normal='Sans400',bold='Sans700',italic='Sans400',boldItalic='Sans700')
N=json.loads((ROOT/'data/network-geo.json').read_text());G=json.loads((ROOT/'data/geography.json').read_text());PS=json.loads((ROOT/'data/projects.json').read_text())
from editorial import apply_projects, apply_routes
apply_projects(PS); apply_routes(N['routes'])
routes={r['id']:r for r in N['routes']};cities={c['id']:c for c in N['cities']};projects={p['id']:p for p in PS}
INK='#1c373a';GREEN='#19776a';MUTED='#65736e';PAPER='#fafaf6';LINE='#d7e0d1';PALE='#eef3e9';ORANGE='#b77542'
COL={15:'#176b57',30:'#2d7fa1',60:'#786598',120:'#b0803b',240:'#a66455',None:'#83928a'}
PLAN='https://dot.ca.gov/-/media/dot-media/programs/rail-mass-transportation/documents/california-state-rail-plan/2024-ca-state-rail-plan-a11y.pdf'
APP='https://dot.ca.gov/-/media/dot-media/programs/rail-mass-transportation/documents/california-state-rail-plan/20241203-appendices-a11y.pdf'
W,H=612,792
out=ROOT/'California-Rail-Electeds-Briefing.pdf'
c=canvas.Canvas(str(out),pagesize=(W,H),pageCompression=1)
c.setTitle('California, Connected — Elected-official briefing on the 2024 State Rail Plan')
c.setAuthor('California Rail Atlas — independent visualization')
c.setSubject('Geographic rail vision, service frequencies, implementation dependencies and an elected-official agenda')

def fill(col):c.setFillColor(HexColor(col))
def stroke(col):c.setStrokeColor(HexColor(col))
def text(x,y,s,size=10,font='Sans400',color=INK):
 fill(color);c.setFont(font,size);c.drawString(x,y,str(s))
def right(x,y,s,size=9,font='Sans400',color=MUTED):fill(color);c.setFont(font,size);c.drawRightString(x,y,str(s))
def para(x,top,s,width,size=9,leading=None,color=MUTED,font='Sans400'):
 style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.5,textColor=HexColor(color),spaceAfter=0)
 p=Paragraph(s,style);pw,ph=p.wrap(width,900);p.drawOn(c,x,top-ph);return ph

def label(x,y,s,color=GREEN,size=7.3):
 fill(color);t=c.beginText(x,y);t.setFont('Sans700',size);t.setCharSpace(1.1);t.textLine(s);t.setCharSpace(0);c.drawText(t)
def rule(y,x1=40,x2=572):stroke(LINE);c.setLineWidth(.65);c.line(x1,y,x2,y)
def box(x,y,w,h,color=PALE,r=6,border=None):
 fill(color)
 if border:stroke(border)
 c.roundRect(x,y,w,h,r,fill=1,stroke=bool(border))
def link(x,y,label,url,size=7.2):
 text(x,y,label,size,'Sans400',GREEN);tw=pdfmetrics.stringWidth(label,'Sans400',size);c.linkURL(url,(x,y-2,x+tw,y+size),relative=0,thickness=0)
def footer(page,section):
 rule(42);text(40,26,'CALIFORNIA, CONNECTED  /  '+section,6.8,'Sans500',MUTED);right(572,26,f'{page} / 4',7,'Sans500',MUTED)
def header(page,section):
 fill(PAPER);c.rect(0,0,W,H,fill=1,stroke=0)
 box(40,740,22,26,INK,4);stroke('#e9b486');c.setLineWidth(1.15)
 c.line(47,744,47,762);c.line(51,744,51,762);p=c.beginPath();p.moveTo(56,762);p.lineTo(56,757);p.curveTo(56,751,45,752,45,746);c.drawPath(p,stroke=1)
 text(72,753,'California, connected.',18,'Serif',INK);right(572,755,'THE 2024 STATE RAIL PLAN',7.2,'Sans700',MUTED)
 right(572,743,'Independent elected-official briefing',6.8,'Sans400',MUTED);footer(page,section)
def money(n):return '$'+(f'{n/1e9:,.2f}'.rstrip('0').rstrip('.')+'B' if n>=1e9 else f'{n/1e6:,.1f}'.rstrip('0').rstrip('.')+'M')

def mapdraw(x0,y0,w,h):
 b=[-402,-445,488,630];k=min(w/(b[2]-b[0]),h/(b[3]-b[1]));ox=x0+(w-(b[2]-b[0])*k)/2;oy=y0+(h-(b[3]-b[1])*k)/2
 def xy(p):return ox+(p[0]-b[0])*k,oy+(b[3]-b[1])*k-(p[1]-b[1])*k
 def path(ds):
  p=c.beginPath()
  for m in re.finditer(r'([MLZ])([^MLZ]*)',ds):
   t,nums=m.groups()
   if t=='Z':p.close();continue
   v=nums.split(',')
   if len(v)!=2:continue
   px,py=xy([float(v[0]),float(v[1])]);p.moveTo(px,py) if t=='M' else p.lineTo(px,py)
  return p
 c.saveState();clip=c.beginPath();clip.rect(x0,y0,w,h);c.clipPath(clip,stroke=0,fill=0);fill('#e4eef0');c.rect(x0,y0,w,h,fill=1,stroke=0)
 for s in G['states']:
  fill('#f7f7ed' if s['name']=='California' else '#edf0e7');stroke('#b0bba9');c.setLineWidth(.5);c.drawPath(path(s['d']),fill=1,stroke=1)
 c.saveState();c.clipPath(path(''.join(s['d'] for s in G['states'])),stroke=0,fill=0);rx,ry=xy([-490,810]);c.setFillAlpha(.35);c.drawImage(str(ROOT/'assets/relief.png'),rx,ry,width=1490*k,height=1435*k,mask='auto');c.restoreState()
 stroke('#b9c4b2');c.setLineWidth(.3);c.setStrokeAlpha(.5);c.drawPath(path(G['counties']),stroke=1);c.setStrokeAlpha(1)
 for l in G['lakes']:fill('#dce9ec');c.drawPath(path(l['d']),fill=1,stroke=0)
 for r in sorted(N['routes'],key=lambda r:(0 if r.get('baseline') else 1,1000-(r['phases']['2050']['headway'] or 999))):
  ph=r['phases']['2050']
  if not ph['active'] or r['id']=='van-nuys-core':continue
  pts=(r.get('coordsByYear',{}).get('2050') or r['coords']);pts=[xy(p) for p in pts]
  offset=(r.get('offset') or 0)*.43
  if offset:
   pp=[]
   for i,p in enumerate(pts):
    a=pts[max(0,i-1)];d=pts[min(len(pts)-1,i+1)];dx=d[0]-a[0];dy=d[1]-a[1];ln=math.hypot(dx,dy) or 1;pp.append([p[0]+dy/ln*offset,p[1]-dx/ln*offset])
   pts=pp
  width={15:2.8,30:2,60:1.25,120:.9,240:.6,None:.38}[ph['headway']]
  color=COL[ph['headway']]
  if r['kind']=='bus':width=.45;color='#7c8289'
  if r.get('baseline'):width=.38;color='#7c8289'
  p=c.beginPath();p.moveTo(*pts[0])
  for q in pts[1:]:p.lineTo(*q)
  c.setDash();c.setLineJoin(1);c.setLineCap(1);stroke(PAPER);c.setLineWidth(width+1);c.drawPath(p)
  stroke(color);c.setLineWidth(width)
  if r['geometry']=='concept' or r.get('hasGaps'):c.setDash(3,2.6);c.setLineCap(0)
  if r['kind']=='bus':c.setDash(1,2)
  c.drawPath(p)
 c.setDash();c.setLineCap(1)
 active=set(n for r in N['routes'] if r['phases']['2050']['active'] for n in r['nodes'])
 taken=[]
 def collision(b):return any(not(b[0]>a[2] or b[2]<a[0] or b[1]>a[3] or b[3]<a[1]) for a in taken)
 for city in sorted(N['cities'],key=lambda c:c['rank']):
  if city['id'] not in active:continue
  x,y=xy(city['p'])
  if not(x0+5<x<x0+w-5 and y0+5<y<y0+h-5):continue
  fill('#345b49' if city['rank']<2 else '#f9faf1');stroke('#749479');c.setLineWidth(.55);c.circle(x,y,1.65 if city['rank']<2 else 1.05,fill=1,stroke=1)
  if city['rank']>2:continue
  name=city['name'];fs=6.4 if city['rank']<2 else 5.7
  if name=='San Ysidro / Tijuana':name='San Ysidro'
  tw=pdfmetrics.stringWidth(name,'Sans500' if city['rank']<2 else 'Sans400',fs)
  options=[(x+4,y-2),(x-tw-4,y-2),(x-tw/2,y+6),(x-tw/2,y-11)]
  if city['id']=='sf':options=[(x-tw-4,y-2)]+options
  for xx,yy in options:
   bb=[xx-1,yy-1,xx+tw+2,yy+fs+2]
   if bb[0]<x0+3 or bb[2]>x0+w-3 or bb[1]<y0+3 or bb[3]>y0+h-3 or collision(bb):continue
   taken.append(bb);fill('#f7f8ee');c.setFillAlpha(.88);c.rect(xx-1,yy-1,tw+2,fs+2,fill=1,stroke=0);c.setFillAlpha(1);text(xx,yy,name,fs,'Sans500' if city['rank']<2 else 'Sans400','#315044');break
 # Geographic label and off-map interstate connection.
 tx,ty=xy([192,-148]);label(tx,ty,'NEVADA','#9dab92',7)
 tx,ty=xy([-285,240]);c.saveState();c.translate(tx,ty);c.rotate(39);label(0,0,'PACIFIC OCEAN','#739a9c',6.5);c.restoreState()
 tx,ty=xy([475,475]);text(tx-65,ty+6,'To Phoenix →',6.5,'Sans500','#786598')
 c.restoreState();stroke(LINE);c.setLineWidth(.65);c.rect(x0,y0,w,h,fill=0,stroke=1)

# PAGE 1 — geographic vision
header(1,'THE VISION')
label(40,711,'READING THE STATEWIDE VISION')
text(40,671,'Reading the 2050 network.',41,'Serif')
para(40,650,'High-speed rail would connect regions, with conventional trains and buses serving other journeys. The proposed network depends on the connections between them.',529,10.5,15.5)
mapdraw(40,166,365,445)
label(421,593,'THE 2050 PROPOSAL',size=7)
text(421,548,'30–60',39,'Sans400',GREEN);text(421,526,'minutes',13,'Sans500',GREEN)
para(421,511,'Typical service goal across most of the state. Not every corridor; not an every-stop guarantee.',149,9,13.5)
link(421,458,'Plan p. 18',PLAN+'#page=25')
rule(440,421,570)
text(421,402,'1,500',38,'Sans400',INK);text(421,383,'miles of overhead power',8.5,'Sans500',INK)
para(421,370,'Envisioned by 2050 across the busiest and high-speed segments.',149,9,13.5)
link(421,325,'Plan p. 5',PLAN+'#page=12')
rule(308,421,570)
text(421,270,'$307B',36,'Sans400',INK)
para(421,256,'The plan’s capital-program headline. <b>Not money already secured.</b>',149,9,13.5)
link(421,209,'Plan pp. 50–51',PLAN+'#page=57')
box(421,95,151,91,INK,6)
label(433,170,'VISION ≠ TIMETABLE','#d2e4bc',6.7)
para(433,158,'These are 2024 planning targets, not live service, current project status or guaranteed opening dates.',125,8.4,12.5,'#e4eddb')
box(40,83,365,73,'#f2f5eb',4,LINE)
for i,(s,h) in enumerate([('≤15 min',15),('30 min',30),('60 min',60),('120 min',120),('240 min',240),('Other',None)]):
 xx=51+(i%3)*118;yy=143-(i//3)*18;stroke(COL[h]);c.setLineWidth({15:2.8,30:2,60:1.25,120:.9,240:.6,None:.38}[h]);c.line(xx,yy,xx+22,yy);text(xx+28,yy-2.2,s,7.5,'Sans400',MUTED)
stroke('#7c8289');c.setLineWidth(.45);c.setDash(1,2);c.line(51,109,73,109);c.setDash();text(79,106.5,'Timed buses · no numeric frequency specified',6.8,'Sans400',MUTED)
stroke('#7c8289');c.setLineWidth(.38);c.line(51,94,73,94);text(79,91.5,'Long-distance Amtrak · 2024 inventory, not 2050 targets',6.5,'Sans400',MUTED)
para(40,73,'Thicker numeric bands = more frequent. Fine Other lines are unquantified. Dotted gray = bus. Dashed = conceptual/generalized; solid = mapped rail, not funding. Selected hubs; urban transit summarized in the atlas.',532,7.1,10.5)
c.showPage()
# PAGE 2 — frequency table
header(2,'FREQUENCY & PHASING')
label(40,711,'SELECTED SERVICE GOALS, BY PLANNING HORIZON')
text(40,671,'How often would trains run?',39,'Serif')
para(40,653,'Selected service goals—not booked train paths or a passenger timetable. The atlas has 70 goal layers plus four gray long-distance Amtrak routes from the 2024 inventory.',532,10,15)
y=594;xs=[40,255,343,431,572]
box(40,y,532,28,INK,4)
for xx,s in zip(xs,['CORRIDOR / SERVICE','2028','2034','2050 VISION']):label(xx+10,y+10,s,'#f0f5e7',6.7)
rows=[
 ('Sacramento–Oakland','60 min','60 min','30 min'),
 ('Sacramento–Roseville','1 daily RT','240 min','30 min'),
 ('San Francisco–San Jose regional','≤15 min','≤15 min','≤15 min'),
 ('Sacramento–Merced conventional','Growing','60 min combined','60 min regional'),
 ('Merced–Bakersfield HSR','—','60 min','30 branch; ≤15 trunk¹'),
 ('Gilroy–Salinas intercity','Limited','Growth','60 min'),
 ('Salinas–SLO state-service layer²','Timed bus','Timed bus','240 min'),
 ('San Luis Obispo–Santa Barbara','240 min','240 min','240 min'),
 ('Santa Barbara–Los Angeles','120 min','120 min','60 min* combined'),
 ('Los Angeles–San Diego intercity','60 min','60 min','30 min'),
 ('Lancaster–Santa Clarita regional','60 min','60 min','60 min'),
 ('Santa Clarita–Los Angeles regional','30 min','30 min','30 min'),
 ('Las Vegas–Rancho Cucamonga','60 min','60 min','30 min'),
 ('Sacramento–Chico regional','Timed bus','Timed bus','120 min'),
 ('Novato–Suisun/Fairfield regional','Timed bus','Timed bus','≤60 min'),
 ('Healdsburg–Cloverdale regional','—','60 min','60 min'),
]
for i,row in enumerate(rows):
 y-=22
 if i%2==0:fill('#f0f3ea');c.rect(40,y,532,22,fill=1,stroke=0)
 for j,s in enumerate(row):
  col=INK if j==0 else GREEN if ('30 min' in s or '≤15' in s) else MUTED
  text(xs[j]+10,y+8,s,7.9 if j==0 else 7.2,'Sans500' if j==0 else 'Sans400',col)
 stroke('#dce3d3');c.setLineWidth(.35);c.line(40,y,572,y)
para(40,231,'² Existing rail is not absent: the plan inventories a daily Coast Starlight round trip through Salinas–SLO and the Bay Area. It is separate from these future service goals. [Appendix 3.1, PDF p. 24]',532,7.5,10.5)
para(40,202,'¹ The long-term map shows a 30-minute Merced–Madera branch and a ≤15-minute combined HSR trunk south of Madera. This is not ≤15-minute service between every pair of stations.',532,7.5,10.5)
para(40,173,'* Santa Barbara–LA: Table 1 says coordinated hourly service; p. 34’s narrative says combined half-hourly. This briefing uses the table’s 60-minute value and flags the disagreement. RT = round trip.',532,7.5,10.5)
box(40,76,258,70,PALE,5,LINE);label(53,130,'REPEATING DOES NOT MEAN 24/7',size=6.6);para(53,120,'A 30-minute target means two departures per hour in a uniform pattern. It does not specify operating span, peak overlays or every stopping pattern.',232,8,11.5)
box(310,76,262,70,'#f1f0f5',5,'#e0dce8');label(323,130,'DO NOT ADD OVERLAPPING LINES',color='#796a91',size=6.6);para(323,120,'Two service layers in one corridor do not automatically create evenly spaced departures. Timetables and transfers must be designed together.',236,8,11.5,'#766981')
link(40,56,'Sources: service tables pp. 37–38; regional maps pp. 30–36; network principles pp. 15–18',PLAN+'#page=44',7)
c.showPage()
# PAGE 3 — projects and the service they unlock
header(3,'NETWORK DEPENDENCIES')
label(40,711,'INFRASTRUCTURE AND THE SERVICE IT SUPPORTS')
text(40,671,'Projects and their connections.',40,'Serif')
para(40,648,'These six examples show how individual projects affect journeys across the network. Costs are the 2024 appendix estimates, not current appropriations or remaining funding gaps.',532,10,15)
briefs=[
 ('stockton','Stockton crossing','Separating the UP–BNSF crossing would reduce conflicts between freight and passenger trains. <b>Ask:</b> which services does the design accommodate, and how would the available train paths and reliability change?'),
 ('merced','Merced interchange','Passengers from Sacramento and the Bay Area would change here for the initial high-speed line. <b>Ask:</b> how far will they walk, how long will they wait, and what happens when an arriving train is late?'),
 ('central-hsr','Initial high-speed line','The mid-term plan proposes hourly Merced–Bakersfield trains. <b>Ask:</b> when will power, signaling, trains, testing, maintenance and connecting services be ready, alongside the track and structures?'),
 ('mega-corridor','Across the Bay','A second Bay crossing is part of a $57B corridor package that includes Carquinez capacity, electrification and shoreline protection. <b>Ask:</b> what could run at each stage, and who is responsible for the connections between projects?'),
 ('link-us','LA Union Station','Through tracks would let trains continue south without reversing at Union Station. <b>Ask:</b> which routes would run through, which platforms and trains would they use, and what other corridor work would be needed?'),
 ('san-clemente','San Clemente coast','Erosion and unstable slopes can interrupt the LA–San Diego railway. <b>Ask:</b> what protection is needed now, which longer-term alternatives are being studied, and how do they compare on outages and community and environmental effects?'),
]
y=608
for id,title,copy in briefs:
 p=projects[id];h=83
 box(40,y-h,532,h-5,'#f2f5ec',5)
 n=PS.index(p)+1;box(52,y-32,20,20,INK,4);text(58,y-26,n,8,'Sans600','#f5f8ed')
 titleh=para(84,y-10,title,156,18,19.5,INK,'Serif')
 text(84,y-26-titleh,money(p['cost'])+'  ·  '+str(p['year']),8,'Sans600',GREEN)
 link(84,y-h+12,'Appendix PDF p. '+str(p['pdfPage']),APP+'#page='+str(p['pdfPage']),6.6)
 para(260,y-12,copy,297,8.4,12.3,MUTED)
 y-=88
para(40,77,'Do not add these figures to estimate a funding gap: package and component costs can overlap. The interactive atlas includes 25 delivery priorities and a searchable 180-entry capital, grade-separation and fleet register. These selected projects are not the full capital program.',532,7.9,11.5)
c.showPage()
# PAGE 4 — elected action and accountability
header(4,'IMPLEMENTATION')
label(40,711,'QUESTIONS FOR PUBLIC DECISION-MAKERS')
text(40,671,'Questions for elected officials.',38,'Serif')
para(40,649,'These suggested questions draw on the plan; they are not quoted Caltrans recommendations. They concern the timetable, the resources to operate it, and the connections between projects.',532,9.8,14.5)
for i,(yr,title,copy) in enumerate([
 ('2028','COMMITTED PROJECTS','The near-term program focuses on projects described as funded or committed in the 2024 plan. Check their current status separately.'),
 ('2034','INITIAL HSR CONNECTIONS','The mid-term program includes the initial high-speed line and related connections, with funding and delivery decisions still to resolve.'),
 ('2050','LONGER-TERM PLANNING','Further extensions and capacity need service studies, alternatives, environmental review, railroad agreements and funding.')]):
 x=40+i*181;box(x,493,170,126,INK if i==2 else PALE,6, None if i==2 else LINE)
 color='#f2f7e8' if i==2 else INK;text(x+14,580,yr,31,'Sans400',color);label(x+14,561,title,'#acc99a' if i==2 else GREEN,6.6);para(x+14,548,copy,142,8,11.8,'#c6d9ba' if i==2 else MUTED)
para(40,482,'2024 funding description: near term funded/committed; mid term funded or with a funding path; much long-term funding unidentified. Horizons are not guaranteed opening dates. Verify current commitments separately.',532,7.4,10.8)
label(40,438,'SIX QUESTIONS FOR PROJECT REVIEW')
qs=[('Which timetable is it designed for?','State & regional boards: ask for the service pattern, connections and reliability standard the design is intended to support.'),('Who will fund the service?','State & operators: identify the ongoing costs of trains, crews, power and maintenance, and who will cover them.'),('What else needs to be ready?','State & regional boards: identify the connecting projects, shared decisions and agency responsible for each.'),('Has the railroad agreed?','State, operators & hosts: confirm how train paths, dispatching and maintenance would be arranged on shared tracks.'),('How will the line remain usable?','All levels: distinguish emergency protection from long-term adaptation, and compare the effects of alternatives.'),('How will people reach the station?','Cities & counties: consider housing, bus connections, accessible walking routes and displacement around stations.')]
for i,(head,body) in enumerate(qs):
 col=i%2;row=i//2;x=40+col*276;top=416-row*68
 text(x,top,f'0{i+1}',10,'Sans600',ORANGE);text(x+25,top,head,9.2,'Sans600',INK);para(x+25,top-9,body,230,8.2,11.8,MUTED)
box(40,168,532,48,'#eaf1e1',5,LINE);label(52,202,'OPERATIONS AND MAINTENANCE',size=6.5);para(52,192,'The plan models <b>$2.4B/year</b> for operations and maintenance of the proposed system. These recurring costs need a funding arrangement alongside the capital program. [Plan p. 51]',508,8.3,12)
rule(151)
label(40,134,'READ THIS BRIEFING RESPONSIBLY',size=6.7)
para(40,122,'<b>Geography:</b> California Albers; Caltrans rail GIS. Dashed routes are conceptual/generalized connections, not approved engineering. Hubs are selected anchors; urban transit is summarized. Gray Amtrak routes show the 2024 inventory, not future service goals (Appendix 3.1).',258,7.3,10.6)
para(314,122,'<b>Evidence:</b> December 2024 main plan (released January 2025), pp. 15–38 and 50–59; Appendices 2.1–2.3 and 3.1. No later project-status updates are blended in. Main plan capital headline: $307B; rounded appendix summary: ~$307.7B. This is an independent visualization, not Caltrans endorsement.',258,7.3,10.6)
link(40,55,'Official plan',PLAN,7);link(113,55,'Official appendices',APP,7);right(572,55,'Companion: California-Rail-Atlas.html · Prepared October 2026',6.6,'Sans400',MUTED)
c.save()
print('Created',out.name,out.stat().st_size,'bytes')
