import csv,collections,re
E='/tmp/gfz_v121_evidence/'
F={r['entry']:r for r in csv.DictReader(open(E+'V121_CORR_FULL_GRAPH_FUNCS.tsv'),delimiter='\t')}
unres={e for e,r in F.items() if not r['owner'] and r['final_no_owner']=='false' and 'GFZ.V121.CodeDomain.' not in (r['tags'] or '')}
# Current should be 562
print('unresolved',len(unres))
# graph undirected among unresolved, collect known adjacencies
adj=collections.defaultdict(set); known=collections.defaultdict(list)

def domains(r):
 return [t[len('GFZ.V121.CodeDomain.'):] for t in (r['tags'] or '').split(';') if t.startswith('GFZ.V121.CodeDomain.')]

def root(r):
 if r['owner']: return 'OWNER:'+r['owner']
 ds=domains(r)
 # only concrete semantic seeds; generic mechanism/runtime/boundary are excluded
 roots=[]
 for d in ds:
  if d.startswith('Phyre.'): roots.append('Phyre')
  elif d.startswith('ThirdParty.Physics.Bullet'): roots.append('Bullet')
  elif d.startswith('ThirdParty.Rendering.PPFX'): roots.append('PPFX')
  elif d.startswith('ThirdParty.Rendering.Yebis'): roots.append('Yebis')
  elif d.startswith('ThirdParty.Scripting.Lua') or d.startswith('Lua.'): roots.append('Lua')
  elif d.startswith('ThirdParty.Video.') or d.startswith('Media.Video.WebM') or d.startswith('Media.Video.VbfMkv'): roots.append('Video')
  elif d.startswith('ThirdParty.Audio.LibVorbis'): roots.append('Vorbis')
  elif d.startswith('ThirdParty.Compression.Zlib'): roots.append('Zlib')
  elif d.startswith('ThirdParty.XML.Libxml2'): roots.append('Libxml2')
  elif d.startswith('ThirdParty.UI.DearImGui'): roots.append('DearImGui')
  elif d.startswith('Microsoft.'): roots.append('Microsoft')
  elif d.startswith('EASTL.'): roots.append('EASTL')
  elif d.startswith('Presentation.') and not d.startswith('Presentation.Runtime'): roots.append('Presentation')
  elif d.startswith('Platform.Windows.'): roots.append('PlatformWindows')
  elif d.startswith('Platform.Graphics.'): roots.append('PlatformGraphics')
  elif d.startswith('SaveLoad.'): roots.append('SaveLoad')
  elif d.startswith('StoryEvent.'): roots.append('StoryEvent')
  elif d.startswith('Gameplay.Combat.'): roots.append('GameplayCombat')
  elif d.startswith('World.'): roots.append('World')
 return roots[0] if len(set(roots))==1 and roots else None

for e in csv.DictReader(open(E+'V121_CORR_FULL_GRAPH_EDGES.tsv'),delimiter='\t'):
 a=e['caller'];b=e['callee']
 if a in unres and b in unres:
  adj[a].add(b);adj[b].add(a)
 elif a in unres and b in F:
  rr=root(F[b]);
  if rr: known[a].append((b,rr,'callee'))
 elif b in unres and a in F:
  rr=root(F[a]);
  if rr: known[b].append((a,rr,'caller'))
# comps
seen=set(); comps=[]
for n in sorted(unres):
 if n in seen:continue
 st=[n];seen.add(n);c=[]
 while st:
  x=st.pop();c.append(x)
  for y in adj[x]:
   if y not in seen:seen.add(y);st.append(y)
 seeds=[]
 for x in c:seeds += known[x]
 rc=collections.Counter(r for _,r,_ in seeds)
 comps.append((c,seeds,rc))
# report components with single concrete root and >=2 distinct known seed funcs
rows=[]
for i,(c,seeds,rc) in enumerate(comps):
 distinct=set(s[0] for s in seeds)
 if len(rc)==1 and len(distinct)>=2:
  r=next(iter(rc));rows.append((len(c),len(distinct),sum(rc.values()),r,i,c,seeds))
print('qualifying comps',len(rows),'functions',sum(x[0] for x in rows))
print('roots',collections.Counter((x[3] for x in rows)))
for x in sorted(rows,reverse=True)[:80]:
 print('COMP',x[4],'n',x[0],'seeds',x[1],'edges',x[2],'root',x[3],'nodes',','.join(sorted(x[5])[:20]))
# write
with open(E+'V121_CORR_SEMANTIC_COMPONENT_AUDIT.tsv','w',newline='') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['component','node_count','seed_function_count','seed_edge_count','root','nodes','seeds'])
 for n,se,ed,r,i,c,seeds in sorted(rows,key=lambda z:z[4]):
  w.writerow([i,n,se,ed,r,';'.join(sorted(c)),';'.join(f'{a}:{rr}:{dir}' for a,rr,dir in seeds)])
