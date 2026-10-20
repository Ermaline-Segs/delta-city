# Reads docs/interiors_from_discord.md into a list of categories and channels with their rules.
# Usage: python3 source/tools/guide_parse.py out/discord.json   (run from the repository root)
import re,json,sys
t=open('docs/interiors_from_discord.md').read()
body=t[t.index('## The full structure'):]
cats=[];cur=None;ch=None;lines=body.split('\n');i=0
while i<len(lines):
    l=lines[i]
    if l.startswith('====') and i+2<len(lines) and lines[i+2].startswith('===='):
        cur={'cat':lines[i+1].strip(),'rooms':[]};cats.append(cur);i+=3;continue
    m=re.match(r'^#(\S+)\s*$',l)
    if m and cur is not None:
        ch={'ch':m.group(1),'rules':{}};cur['rooms'].append(ch);i+=1;continue
    m=re.match(r'^\s{2,}([A-Za-z ,+\-]+?):\s*(.*)$',l)
    if m and ch is not None and cur is not None:
        ch['rules'][m.group(1).strip()]=[x.strip() for x in m.group(2).split('|') if x.strip()];i+=1;continue
    if l.startswith('```') and cur and cats.index(cur)>0: pass
    i+=1
json.dump(cats,open(sys.argv[1],'w'),indent=0,ensure_ascii=False)
for c in cats: print(len(c['rooms']),c['cat'])
