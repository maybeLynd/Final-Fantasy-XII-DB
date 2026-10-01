import collections, hashlib, importlib.util, json, os, shutil, subprocess, sys, traceback
from datetime import datetime, timezone
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
R=W/'run-01'
EXE=Path('Database/Tools/work/exe/FFXII_TZA.exe').resolve()
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def git(*args):
 p=subprocess.run(['git',*args],capture_output=True,text=True)
 assert p.returncode==0 and not p.stderr,(args,p.returncode,p.stderr)
 return p.stdout.strip()
def sweep(spans,lo,n):
 events=collections.Counter();events[lo]+=0;events[lo+n]+=0
 for e,z in spans:
  a,b=max(e,lo),min(e+z,lo+n)
  if a<b:events[a]+=1;events[b]-=1
 depth=0;last=lo;dist=collections.Counter()
 for pos,delta in sorted(events.items()):
  dist[depth]+=pos-last;depth+=delta;last=pos
 assert depth==0 and sum(dist.values())==n
 return dict(unique_overlap=sum(v for k,v in dist.items() if k>=2),additional_cover_sum=sum((k-1)*v for k,v in dist.items() if k>=2),union=sum(v for k,v in dist.items() if k>=1),depth_bytes={str(k):v for k,v in sorted(dist.items())})
def run():
 assert not R.exists(),'Write-once; inspect retained failure instead of replay'
 R.mkdir()
 srcs=['Database/Tools/dashboard/build_views.py','Database/Tools/analysis-kit/gfz-scripts/generation.py','Database/Tools/analysis-kit/gfz-scripts/uc1_band.py']
 identity={'head':git('rev-parse','HEAD'),'driver_sha256':sha(Path(__file__)),'python':sys.executable,'python_version':sys.version,'started':datetime.now(timezone.utc).isoformat(),'source':[],'inputs':[],'limits':'Repository Python original adapter, labelled extent fixtures and copied census; shipping PE read only, no guest instructions/live game execution.'}
 for name in srcs:
  p=Path(name);before=sha(p);target=R/'original'/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
  assert sha(p)==sha(target)==before
  identity['source'].append({'path':name,'sha256':before,'last_commit':git('log','-1','--format=%H','--',name),'blob':git('hash-object','--no-filters',name)})
 inputs=['Database/Tools/work/graph/functions.tsv','Database/FFXII TZA/99-Unresolved-Residual/Unlisted-Code/uc1-applied-population-1-64.tsv','Database/FFXII TZA/99-Unresolved-Residual/Unlisted-Code/uc1-applied-population-65-256.tsv']
 for i,name in enumerate(inputs):
  p=Path(name);before=sha(p);target=R/'inputs'/('canonical-'+str(i)+'.tsv');target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target)
  assert sha(p)==sha(target)==before
  identity['inputs'].append({'path':name,'copy':target.relative_to(R).as_posix(),'sha256':before})
 identity['exe']={'path':str(EXE),'sha256':sha(EXE),'bytes':EXE.stat().st_size,'external':True,'copied':False}
 gs=R/'original/Database/Tools/analysis-kit/gfz-scripts';sys.path.insert(0,str(gs.resolve()))
 source=R/'original/Database/Tools/dashboard/build_views.py'
 spec=importlib.util.spec_from_file_location('original_overlap_adapter',source);adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
 import pefile,uc1_band
 pe=pefile.PE(str(EXE),fast_load=True);sec=next(s for s in pe.sections if s.Name.rstrip(b'\0')==b'.text')
 lo,n=pe.OPTIONAL_HEADER.ImageBase+sec.VirtualAddress,sec.Misc_VirtualSize;assert n>256;pe.close()
 identity['text']={'lo':lo,'size':n};identity['pefile']={'module':pefile.__file__,'sha256':sha(pefile.__file__),'version':pefile.__version__}
 assert Path(uc1_band.__file__).resolve()==(gs/'uc1_band.py').resolve()
 identity['loaded']={'adapter':str(Path(adapter.__file__).resolve()),'uc1_band':str(Path(uc1_band.__file__).resolve()),'generation':str(Path(adapter.G.__file__).resolve())}
 (R/'identity.json').write_bytes((json.dumps(identity,indent=2)+'\n').encode())
 cases=[]
 for name,offsets in [('disjoint',[(0,12),(16,8)]),('double',[(0,12),(4,8)]),('triple',[(0,12),(4,8),(8,4)])]:
  d=R/'fixtures'/name;d.mkdir(parents=True)
  f=d/'functions.tsv';f.write_bytes(('entry\tname\tsize\n'+''.join('%08X\tFIXTURE_%s_%d\t%d\n'%(lo+a,name,i,z) for i,(a,z) in enumerate(offsets))).encode())
  bands=[]
  for i in (1,2):
   b=d/('band%d.tsv'%i);b.write_bytes(b'kind\tstart\tend\n');bands.append(str(b))
  spans=[(lo+a,z) for a,z in offsets];expected=sweep(spans,lo,n)
  observation=adapter.text_intervals(str(f),tuple(bands),str(EXE))
  assert sum(observation['bytes'].values())==n and observation['population']==len(offsets)
  if name!='triple':assert observation['overlap']==expected['unique_overlap'], 'Positive control failed; no broad conclusions'
  cases.append(dict(name=name,intervention='Synthetic extent rows and schema-valid empty UC1 bands; actual certified PE external read',spans=spans,oracle=expected,original=observation,exception=None))
  (R/(name+'.json')).write_bytes((json.dumps(cases[-1],indent=2)+'\n').encode())
 # Exact real census invocation is separate from the controlled counterexample.
 f=R/identity['inputs'][0]['copy'];bands=tuple(str(R/i['copy']) for i in identity['inputs'][1:])
 sizes={}
 for i,line in enumerate(f.read_text('utf-8').splitlines()):
  p=line.split('\t')
  if i==0 or len(p)<3 or p[1].startswith(('Unwind@','Catch_All@')):continue
  try:sizes[int(p[0],16)]=int(p[2])
  except ValueError:continue
 band=uc1_band.load(bands[0]);other=uc1_band.load(bands[1])
 # Exact combined-band load is used, with restoration of the copied module global.
 saved=uc1_band.BAND_TSVS
 try:uc1_band.BAND_TSVS=bands;merged=uc1_band.load()
 finally:uc1_band.BAND_TSVS=saved
 population,info=uc1_band.apply(sizes,merged)
 expected=sweep(list(population.items()),lo,n);original=adapter.text_intervals(str(f),bands,str(EXE))
 actual=dict(name='canonical-copied-census',oracle=expected,original=original,population_info=info,exception=None)
 (R/'canonical.json').write_bytes((json.dumps(actual,indent=2)+'\n').encode())
 assert sum(original['bytes'].values())==n
 assert sha(EXE)==identity['exe']['sha256']
 for i in identity['inputs']:assert sha(i['path'])==sha(R/i['copy'])==i['sha256']
 for s in identity['source']:assert sha(s['path'])==sha(R/'original'/s['path'])==s['sha256']
 result={'cases':[c['name'] for c in cases],'triple_unique':cases[-1]['oracle']['unique_overlap'],'triple_reported':cases[-1]['original']['overlap'],'canonical_unique':expected['unique_overlap'],'canonical_reported':original['overlap'],'unchanged_inputs_and_source':True,'guest_code_or_live_game_executed':False,'ended':datetime.now(timezone.utc).isoformat()}
 assert result['triple_reported']==cases[-1]['oracle']['additional_cover_sum'] and result['triple_reported']!=result['triple_unique']
 (R/'summary.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
 print(json.dumps(result,indent=2))
if __name__=='__main__':
 try:run()
 except BaseException:
  if R.exists():(R/'failure.txt').write_text(traceback.format_exc())
  raise
