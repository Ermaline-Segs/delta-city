# Writes docs/workplaces.md (where each post clocks in) from the game data made by guide_data.py.
# Usage: python3 source/tools/guide_doc.py out/guide.json   (run from the repository root)
import json,sys
g=json.load(open(sys.argv[1]));B=g['buildings']
TYPES=('police','court','util','uni','trans','house','agri','trade','culture','stats','foreign','federal','presidency','stategov')
NATIONAL=('federal','presidency','trade','culture','stats','foreign')
ALIAS={'Agriculture & Resource Officer':'Agriculture & Resources Officer','Minister of Information, Culture & Heritage':'Minister of Culture & Heritage'}
nice=lambda ch:' '.join(w.capitalize() for w in ''.join(c for c in ch if c.isalnum() or c=='-').split('-') if w).replace('Igp','IGP')
lab=lambda b:' '.join(w.lower() if w in('OF','AND') else w if w in('&','-') else w.capitalize() for w in b['label'].split())
out=['# Where each post clocks in','',
 'Worked out from `docs/interiors_from_discord.md`: each post clocks in only in its own office or staff room, inside its own',
 'building, in the state the post belongs to. Once clocked in, anywhere in that building keeps you at work; leaving it',
 'clocks you out. Posts at the hospital, the banks, Immigration and the Treasury keep those buildings\' existing rules.','',
 'The same post under two names: '+'; '.join(f'"{b}" is "{a}"' for a,b in ALIAS.items())+'.','']
for st in ['Asaba','Warri','Ozoro','Agbor']:
    out+=['## '+st,'','| Post | Building | Room |','|---|---|---|']
    for p,(i,ch) in sorted(g['work'][st].items()):
        b=B[i]
        if b['type'] not in TYPES: continue
        if st!='Asaba' and b['type'] in NATIONAL: continue
        name=p+(f' (also "{ALIAS[p]}")' if p in ALIAS else '')
        out.append(f'| {name} | {lab(b)} | {nice(ch)} |')
    out.append('')
out.append('National posts (the President, ministers, the Federal Council, and the Trade, Culture, Statistics and Foreign Affairs staff) are listed under Asaba.')
open('docs/workplaces.md','w').write('\n'.join(out)+'\n');print(len(out),'lines')
