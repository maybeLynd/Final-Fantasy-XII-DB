import collections, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def oracle(spans,lo,n):
 events=collections.Counter({lo:0,lo+n:0})
 for a,z in spans:
  a,b=max(a,lo),min(a+z,lo+n)
  if a<b:events[a]+=1;events[b]-=1
 depth=0;last=lo;dist=collections.Counter();triples=[]
 for p,d in sorted(events.items()):
  dist[depth]+=p-last
  if depth>=3 and last<p:triples.append({'start':last,'end':p,'depth':depth,'contributors':[[a,a+z] for a,z in spans if a<=last and a+z>=p]})
  depth+=d;last=p
 assert depth==0 and sum(dist.values())==n
 return {'unique_overlap':sum(v for k,v in dist.items() if k>=2),'additional_cover_sum':sum((k-1)*v for k,v in dist.items() if k>=2),'union':sum(v for k,v in dist.items() if k>=1),'depth_bytes':{str(k):v for k,v in sorted(dist.items())}},triples
def check(w):
 r=w/'run-02';i=json.loads((r/'identity.json').read_bytes());receipt=json.loads((w/'capture-terminal.json').read_bytes())
 assert receipt['returncode']==0 and receipt['terminal'] and not receipt['stderr']
 assert sha(w/'capture.py')==receipt['driver_sha256']==i['driver_sha256']
 for s in i['source']:assert sha(r/'original'/s['path'])==s['sha256']
 for s in i['inputs']:assert sha(r/s['copy'])==s['sha256']
 for s in i['reader_dependencies']:assert sha(r/s['copy'])==s['sha256']
 assert not (r/'failure.txt').exists()
 assert 'ModuleNotFoundError' in (w/'run-01/failure.txt').read_text()
 assert sha(w/'capture-initial.py')!=sha(w/'capture.py')
 lo,n=i['text']['lo'],i['text']['size'];answers=[]
 for name in ('disjoint','double','triple'):
  case=json.loads((r/(name+'.json')).read_bytes());expected,_=oracle(case['spans'],lo,n)
  assert expected==case['oracle'] and case['exception'] is None
  assert sum(case['original']['bytes'].values())==n and case['original']['population']==len(case['spans'])
  assert case['original']['exe_sha']==i['exe']['sha256']
  if name!='triple':assert case['original']['overlap']==expected['unique_overlap']
  else:assert (expected['unique_overlap'],case['original']['overlap'],expected['additional_cover_sum'])==(8,12,12)
  answers.append({'case':name,'unique':expected['unique_overlap'],'reported':case['original']['overlap']})
 # Reconstruct the accepted population edits from captured TSVs, without calling
 # the producer's overlap loop or uc1.apply during reduction.
 sizes={}
 for j,line in enumerate((r/i['inputs'][0]['copy']).read_text('utf-8').splitlines()):
  p=line.split('\t')
  if j==0 or len(p)<3 or p[1].startswith(('Unwind@','Catch_All@')):continue
  try:sizes[int(p[0],16)]=int(p[2])
  except ValueError:continue
 for entry in i['inputs'][1:]:
  lines=(r/entry['copy']).read_text('utf-8').splitlines();lines=[s for s in lines if not s.startswith('#')];head=lines[0].split('\t')
  for line in lines[1:]:
   p=line.split('\t')
   try:k=p[head.index('kind')];a,b=int(p[head.index('start')],16),int(p[head.index('end')],16)
   except (ValueError,IndexError):continue
   if k=='remove-listed':assert a in sizes;sizes.pop(a)
   elif k=='extend-listed':assert a in sizes;sizes[a]=b-a
   elif k in ('admit-frontier','split-part'):assert a not in sizes;sizes[a]=b-a
 expected,triples=oracle(list(sizes.items()),lo,n);actual=json.loads((r/'canonical.json').read_bytes())
 assert expected==actual['oracle'] and actual['exception'] is None
 assert actual['original']['population']==len(sizes)==35064
 assert sum(actual['original']['bytes'].values())==n
 assert actual['original']['overlap']==expected['additional_cover_sum']==1759 and expected['unique_overlap']==1758
 return {'verdict':'REJECT scoped unique-overlap measure at exact original source','fixtures':answers,'canonical_unique':1758,'canonical_reported':1759,'multiply_covered_segments':triples,'source_commit':i['source'][0]['last_commit'],'limits':'Physical extent accounting only; no re-adjudication of UC1 extents, native behavior, class tiling or full migration/database acceptance.'}
if __name__=='__main__':print(json.dumps(check(Path(__file__).resolve().parent),indent=2))
