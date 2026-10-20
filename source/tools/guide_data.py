# Turns the parsed guide into the game data in index.html (the <script id="dguide"> block): each building,
# its rooms with who may use / only look, and each post's own room for clocking in (one workplace per post per state).
# Usage: python3 source/tools/guide_data.py out/discord.json out/guide.json   then paste guide.json into the dguide block.
import json,re,sys
cats=json.load(open(sys.argv[1]))
BLOCK={'ASABA — CAPITAL':'Asaba','🌊WARRI':'Warri','🌴OZORO':'Ozoro','🏘️AGBOR':'Agbor'}
TYPES=[('police',r'POLICE'),('court',r'COURT'),('util',r'UTILITIES'),('uni',r'UNIVERSITY'),('trans',r'TRANSPORT'),('house',r'HOUSING DEVELOPMENT'),
       ('hotel',r'HOUSING & HOSPITALITY'),('agri',r'AGRICULTURE|NATURAL RESOURCES|FOOD PRODUCTION|AGRICULTURAL SERVICES'),('trade',r'TRADE'),('culture',r'CULTURE'),
       ('stats',r'STATISTICS'),('foreign',r'FOREIGN'),('presidency',r'PRESIDENCY'),('federal',r'FEDERAL COUNCIL'),('lifestyle',r'LIFESTYLE'),('hosp',r'HOSPITAL'),
       ('treasury',r'NATIONAL TREASURY'),('bank',r'BANK'),('stategov',r'STATE GOVERNMENT'),('immstate',r'— CAPITAL|^🌊WARRI$|^🌴OZORO$|^🏘️AGBOR$'),('imm',r'IMMIGRATION AUTHORITY'),
       ('arrivals',r'ARRIVALS'),('media',r'MEDIA'),('admin',r'ADMINISTRATION')]
def clean(s):
    s=re.sub(r'[^\w &,\'—-]','',s).replace('—','-').strip(' -')
    return re.sub(r'\s+',' ',s)
def plain(ch):
    w=re.sub(r'[^a-z0-9-]','',ch.lower()).replace('--','-').strip('-').split('-')
    w=[x for x in w if x]
    up={'igp':'IGP','id':'ID'}
    return ' '.join(up.get(x,x.capitalize()) for x in w)
base=lambda p:re.sub(r'\s*\(.*?\)\s*$','',p).strip()
STOP={'of','the','and','officer','office','services','service','state','minister','ministry','national','general','s'}
SYN={'driller':['rig','oil'],'farmer':['farm'],'student':['lecture'],'driver':['staff'],'heritage':['site'],'inspector-general':['igp'],'inspector':[]}
def stem(w):return re.sub(r'(ies|s)$','',w)
def words(s):return [w for w in (stem(x) for x in re.findall(r'[a-z]+',s.lower())) if w not in STOP]
def match(a,b):
    if a==b:return True
    n=0
    while n<min(len(a),len(b)) and a[n]==b[n]:n+=1
    return n>=6 or (min(len(a),len(b))>=4 and n==min(len(a),len(b)))
PUBLIC=re.compile(r'^(Citizen of|Visitor |Deltans|@everyone|Asylum)')
NOTPOST=('Chief Administrator','Cuffed','Jail','Outpatient','Hospitalized','Dental Patient','In-Surgery')
OVERRIDE={"Dean of Students' Affairs":'academic-office','Professor':'professor-office|lecturers-office','Student':'lecture-halls','Chief Registrar':'clerk-office',
  'Superintendent':'police-operations','Police Officer':'police-operations','Agricultural Inspector':'general-inspection|inspection','Director of Culture & Heritage':'directors-office','State Statistics Director':'directors-office','Secretary to the State Government':'ssg-office','State Police & Security Commissioner':'commisioner-office|commissioner-office','Federal Council':'federal-chambers|🗂️chief-of-staff','Inspector-General of Police & Security':'igp-office'}
COUNCIL=re.compile(r'council|chambers')
def score(p,r):
    pw=words(p)+sum((SYN.get(w,[]) for w in words(p)),[])
    cw=words(r['ch']);ov=sum(1 for a in pw if any(match(a,b) for b in cw));extra=sum(1 for b in cw if not any(match(a,b) for a in pw))
    return (ov*10-extra*2+(3 if 'office' in r['ch'] else 0)+(3 if re.search('operations|staff',r['ch']) else 0)
            +(25 if p.startswith('Minister') and 'minister' in r['ch'] else 0)-(15 if COUNCIL.search(r['ch']) else 0))
def staffrooms(p,rooms):
    cand=[r for r in rooms if any(base(x)==p for x in r['use'])]
    return [r for r in cand if not any(PUBLIC.match(x) for x in r['use']+r['see'])] or cand
# decided with the owner after phase 1 (only ever added to the guide): posts the database has that the guide's rooms do not name,
# and the director's offices the Culture and Statistics bureaus did not have
EXTRA_USE={'police':[(r'^police-operations$',['Police Officer'])],'agri':[(r'inspection$',['Agricultural Inspector'])]}
NEW_ROOMS={'culture':[{'ch':'directors-office','use':['Director of Culture & Heritage'],'see':[]}],'stats':[{'ch':'directors-office','use':['State Statistics Director'],'see':[]}]}
out=[];block=None
for c in cats:
    name=c['cat']
    for k,v in BLOCK.items():
        if k in name: block=v
    if name.startswith('ROLES THE RULES') or not c['rooms']: continue
    typ=next((t for t,rx in TYPES if re.search(rx,name)),'other')
    rooms=[]
    typ0=typ
    for r in c['rooms']:
        R=r['rules'];use=R.get('View + send',[])+R.get('Send, no history',[])+R.get('Runs the voice room',[])+R.get('May create private threads',[])
        see=R.get('Read-only',[])+R.get('Can see the channel',[])
        dedup=lambda L:list(dict.fromkeys(L))
        rooms.append({'ch':r['ch'],'name':plain(r['ch']),'use':dedup(use),'see':[x for x in dedup(see) if x not in use]})
    for rx,add in EXTRA_USE.get(typ,[]):
        for r in rooms:
            if re.search(rx,r['ch']):r['use']=r['use']+[x for x in add if x not in r['use']]
    for nr in NEW_ROOMS.get(typ,[]):
        if not any(r['ch']==nr['ch'] for r in rooms):rooms.append({'ch':nr['ch'],'name':plain(nr['ch']),'use':list(nr['use']),'see':list(nr['see'])})
    posts=dict.fromkeys(base(p) for r in rooms for p in r['use'] if not PUBLIC.match(p) and 'Visitor' not in p and p not in NOTPOST)
    clock={}
    for p in posts:
        staff=staffrooms(p,rooms)
        if p in OVERRIDE:
            hit=next((o for o in OVERRIDE[p].split('|') if any(r['ch']==o for r in staff)),None)
            if hit:clock[p]=[hit,100];continue
        best=max(staff,key=lambda r:score(p,r));clock[p]=[best['ch'],score(p,best)]
    out.append({'cat':name,'label':clean(name),'state':block,'type':typ,'rooms':rooms,'clock':clock})
# one workplace per post in each state: the building where its own room scores best (national buildings count for every state)
WORK={}
for st in ['Asaba','Warri','Ozoro','Agbor']:
    W={}
    for i,b in enumerate(out):
        if b['state'] not in (st,None) and not (b['state']=='Asaba' and b['type'] in ('federal','presidency','trade','culture','stats','foreign')):continue
        for p,(ch,sc) in b['clock'].items():
            if p not in W or sc>W[p][2]:W[p]=[i,ch,sc]
    WORK[st]={p:[i,ch] for p,(i,ch,sc) in W.items()}
for b in out:b['clock']={p:v[0] for p,v in b['clock'].items()}
out={'buildings':out,'work':WORK}
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,separators=(',',':'))

