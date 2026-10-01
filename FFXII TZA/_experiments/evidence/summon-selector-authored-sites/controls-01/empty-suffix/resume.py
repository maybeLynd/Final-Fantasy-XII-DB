"""Finish only the unread suffix and discriminate the small unsupported files."""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(p for p in P.parents if(p/'agent_flow/tools/vbfextract.py').is_file());sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 out=P/'raw-02.json';folder=P/'raw-02'
 if out.exists() or folder.exists():raise RuntimeError('immutable output exists')
 st=json.loads((P/'collect-01.status.json').read_text());old=json.loads((P/'raw-01.json').read_text())
 if st.get('terminal') is not True or st.get('exit')!=1 or st.get('exception') is not None or st['driver_sha256']!=sha((P/'collect.py').read_bytes()) or old['tools']['collector_sha256']!=st['driver_sha256'] or old['collection_complete'] is not False or old['raw_candidates']!=0 or old['sites'] or old['budget_stop'] is None:raise RuntimeError('not the exact retained budget partial')
 if (P/'collect-01.stderr').read_text().splitlines()[-1]!='RuntimeError: bounded collection incomplete; raw coverage retained':raise RuntimeError('unrelated upstream failure cannot resume')
 if old['read_bytes']!=536854000 or old['archive']['ebp_index_entries']!=10045 or len(old['coverage'])!=9430:raise RuntimeError('partial population changed')
 sys.path.insert(0,str(ROOT/'agent_flow/tools'));import vbfextract as V
 if sha((ROOT/'agent_flow/tools/vbfextract.py').read_bytes())!=old['tools']['extractor_sha256']:raise RuntimeError('extractor changed')
 g=ROOT/old['tools']['decoder_path']
 if sha(g.read_bytes())!=old['tools']['decoder_sha256']:raise RuntimeError('decoder changed')
 a=Path(old['archive']['path']);now=a.stat()
 if (now.st_size,now.st_mtime_ns)!=(old['archive']['size'],old['archive']['mtime_ns']):raise RuntimeError('archive source changed')
 folder.mkdir();rows=[];sites=[];readbytes=0;start=time.monotonic();olddecomp=V.zlib.decompress;errors=[]
 def checked(*args,**kwargs):
  try:return olddecomp(*args,**kwargs)
  except Exception as e:errors.append(repr(e));raise
 V.zlib.decompress=checked
 with a.open('rb') as f:
  header=f.read(old['archive']['header_bytes'])
  if sha(header)!=old['archive']['header_sha256']:raise RuntimeError('archive header changed')
  f.seek(0);names,blocks=V.load_index(f);paths=sorted(p for p in names if p.lower().endswith('.ebp'))
  k=paths.index(old['budget_stop'])
  if paths[:k]!=[r['path'] for r in old['coverage'][:-1]] or any(list(names[r['path']])!=r['archive_entry'] for r in old['coverage']):raise RuntimeError('partial/index correspondence changed')
  prior_unsupported=[r['path'] for r in old['coverage'][:-1] if r['status']!='COVERED_LITERAL_CODE_SPANS']
  todo=paths[k:]+prior_unsupported
  planned=sum(names[p][1] for p in todo)
  if len(paths)!=10045 or len(paths[k:])!=616 or planned>40*1024*1024:raise RuntimeError('exact suffix budget changed')
  for path in todo:
   if time.monotonic()-start>30:raise RuntimeError('suffix time budget exceeded')
   errors.clear();b=V.read_entry(f,names,blocks,path);readbytes+=len(b)
   if errors:raise RuntimeError('extractor decompression fallback invalidates input')
   original=next((r for r in old['coverage'] if r['path']==path and r['status']=='UNAVAILABLE_OR_UNSUPPORTED'),None)
   if original and (original['sha256']!=sha(b) or original['bytes']!=len(b)):raise RuntimeError('unsupported preimage changed')
   # Whole-entry byte absence is a stronger discriminator than guessing the
   # layout of the small unsupported/empty modules. It proves literal absence
   # only; no compressed/generated program or runtime reachability guarantee.
   hits=[]
   for op in [0x58,0x59,0x5d,0x5e]:
    token=bytes([op,0x44,0x30]);cursor=0
    while True:
     j=b.find(token,cursor)
     if j<0:break
     hits.append({'file_pc':j,'opcode':hex(op)});cursor=j+1
   row={'path':path,'sha256':sha(b),'bytes':len(b),'archive_entry':list(names[path]),'source_method':'WHOLE_DECOMPRESSED_ENTRY_LITERAL_SCAN','candidate_hits':hits,'previous_layout_status':original['status'] if original else None};rows.append(row)
   if original or hits:
    name=sha(path.encode())[:16]+'.ebp';(folder/name).write_bytes(b);row['retained_raw']=name
   sites.extend({'path':path,**hit} for hit in hits)
  f.seek(0)
  if sha(f.read(old['archive']['header_bytes']))!=old['archive']['header_sha256']:raise RuntimeError('archive header changed during suffix')
 V.zlib.decompress=olddecomp;after=a.stat()
 if (now.st_size,now.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise RuntimeError('archive stat changed during suffix')
 result={'collection_complete':True,'literal_question_settled':not sites,'method':'A suffix/full-entry literal discriminator; prior recognized code spans reused','collector_sha256':sha(Path(__file__).read_bytes()),'parent_raw_sha256':sha((P/'raw-01.json').read_bytes()),'parent_status_sha256':sha((P/'collect-01.status.json').read_bytes()),'parent_failure':'BUDGET_STOP: retained partial, not a prior successful full run','archive':old['archive'],'new_read_bytes':readbytes,'planned_read_bytes':planned,'old_prefix_entries':k,'new_suffix_entries':len(paths[k:]),'small_layout_gaps_checked_as_whole_bytes':len(prior_unsupported),'coverage':rows,'literal_candidates':sites,'elapsed_seconds':time.monotonic()-start,'limits':'No literal native3044 CALL candidate in covered section0 function spans plus the whole unread/gap entries, if candidates empty. Existing prefix directory coverage/layout and noninterference assumptions retained. Whole files/other sections of already recognized prefix entries were not rescanned. This is not natural unreachability, wholearchive identity, compressed/generated/external programs, other native writers, dynamic gameplay or stats-type proof.'}
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['collection_complete','literal_question_settled','old_prefix_entries','new_suffix_entries','small_layout_gaps_checked_as_whole_bytes','new_read_bytes','elapsed_seconds']}))
 if sites:raise RuntimeError('new literal candidates require original aligned decode; raw retained')
if __name__=='__main__':main()
