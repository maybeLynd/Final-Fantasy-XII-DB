"""Task-specific source discovery with explicit input/decoder coverage."""
import hashlib,importlib.util,json,struct,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(p for p in P.parents if(p/'agent_flow/tools/vbfextract.py').is_file())
GEN=ROOT/'Database/FFXII TZA/25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py'
ARCHIVE=Path(r'D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf')
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 out=P/'raw-01.json'
 if out.exists() or(P/'raw').exists():raise RuntimeError('immutable output exists')
 rawdir=P/'raw';rawdir.mkdir();sys.path.insert(0,str(ROOT/'agent_flow/tools'))
 G=load('summon_authored_existing_decoder',GEN);verbs=G.load_verbs()
 if verbs.get(0x3044,(None,))[0]!=2:raise RuntimeError('target native arity prerequisite unavailable')
 exe=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if sha(exe)!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise RuntimeError('reference EXE identity changed')
 pe=struct.unpack_from('<I',exe,60)[0];opt=struct.unpack_from('<H',exe,pe+20)[0];secs=[struct.unpack_from('<IIII',exe,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',exe,pe+6)[0])]
 addr=0x1f28a50;binding=None
 for vs,va,size,o in secs:
  if 0x120000+va<=addr and addr+8<=0x120000+va+size:binding=exe[o+addr-0x120000-va:o+addr-0x120000-va+8]
 if binding!=bytes.fromhex('b0ff500000000000'):raise RuntimeError('native3044 result identity changed')
 ins,anomaly=G.decode(bytes.fromhex('4f01004f1b00584430'))
 args,status=G.resolve_args(ins,2,2,verbs)
 if anomaly is not None or ins[-1]!=(6,0x58,0x3044) or status!='ok' or [a[1] for a in args]!=[1,27]:raise RuntimeError('decoder/argument positive failed')
 control=ROOT/'Database/Tools/work/ASTRA/sn1-variable-name-binding/retained/btlctrl.ebp'
 cb=control.read_bytes();control_sha=sha(cb)
 if control_sha!='660a79970be651607311e07b4426db739eabb5b68e5784ad6ab5949a06e26b08':raise RuntimeError('retained positive identity changed')
 parent=ROOT/'Database/Tools/work/ASTRA/sn1-variable-name-binding/raw.json'
 pv=json.loads(parent.read_text());matches=[r for r in pv['reference']['files'] if r.get('module')=='btlctrl' and r.get('extension')=='ebp']
 if len(matches)!=1 or matches[0].get('sha256')!=control_sha:raise RuntimeError('retained positive identity not bound')
 cs=cb[0x80:0x80+G.U32(cb,0x84)];cd=G.U32(cs,0x18);cc=G.U32(cs,cd)
 cstarts=sorted({G.U32(cs,cd+4+i*0x30+8) for i in range(cc)});cbounds=sorted(set(cstarts)|{cd});control_calls=0
 for st in cstarts:
  ci,ca=G.decode(cs[st:min(z for z in cbounds if z>st)])
  if ca is not None:raise RuntimeError('retained positive decode incomplete')
  control_calls+=sum(op in [0x58,0x59,0x5d,0x5e] for _,op,_ in ci)
 if control_calls!=962:raise RuntimeError('retained actual CALL control changed')
 (rawdir/'positive-btlctrl.ebp').write_bytes(cb)
 coverage=[];sites=[];totalbytes=0;totalfunctions=0;rawcandidates=0;budgetfail=None;start=time.monotonic();before=ARCHIVE.stat()
 # Existing extractor may fall back to raw on a decompression error. Track
 # this concrete path and reject the input, even if the shared extractor returns.
 olddecomp=G.V.zlib.decompress;decomp_errors=[]
 def observed_decomp(*a,**k):
  try:return olddecomp(*a,**k)
  except Exception as e:decomp_errors.append(repr(e));raise
 G.V.zlib.decompress=observed_decomp
 with ARCHIVE.open('rb') as f:
  prefix=f.read(16)
  if len(prefix)!=16 or prefix[:4]!=b'SRYK':raise RuntimeError('archive header missing')
  hlen=struct.unpack_from('<I',prefix,4)[0]
  if not 16<=hlen<=64*1024*1024:raise RuntimeError('archive header budget exceeded')
  f.seek(0);header=f.read(hlen)
  if len(header)!=hlen:raise RuntimeError('archive header truncated')
  header_sha=sha(header);f.seek(0);names,blocks=G.V.load_index(f)
  paths=sorted(p for p in names if p.lower().endswith('.ebp'))
  if not paths:raise RuntimeError('no EBP input coverage')
  for path in paths:
   row={'path':path,'archive_entry':list(names[path]),'status':'UNPREPARED'};coverage.append(row)
   if time.monotonic()-start>120 or totalbytes+names[path][1]>512*1024*1024 or names[path][1]>16*1024*1024:
    row['status']='BUDGET_STOP';budgetfail=path;break
   decomp_errors.clear()
   try:
    b=G.V.read_entry(f,names,blocks,path);totalbytes+=len(b);row.update(bytes=len(b),sha256=sha(b))
    if decomp_errors:raise RuntimeError('extractor fallback after decompression error')
    if len(b)<0x88 or G.U32(b,0x80)!=0x8000000b:raise ValueError('unsupported EBP section0 signature')
    length=G.U32(b,0x84)
    if length<0x50 or 0x80+length>len(b):raise ValueError('truncated section0')
    sec=b[0x80:0x80+length];directory=G.U32(sec,0x18)
    if directory<0x50 or directory+4>len(sec):raise ValueError('invalid directory position')
    cnt=G.U32(sec,directory)
    if not 0<cnt<=0x400 or directory+4+cnt*0x30>len(sec):raise ValueError('invalid/empty directory extent')
    pool=G.U32(sec,0x4c);starts={}
    for k in range(cnt):
     d=directory+4+k*0x30;s=G.U32(sec,d+8);n=pool+G.U32(sec,d)
     if not 0<=n<len(sec) or not 0x50<=s<directory:raise ValueError('invalid code/name boundary')
     term=sec.find(b'\0',n)
     if term<0:raise ValueError('unterminated script name')
     starts.setdefault(s,sec[n:term].decode('cp932',errors='strict'))
    bounds=sorted(set(starts)|{directory});row.update(status='COVERED_LITERAL_CODE_SPANS',function_spans=len(starts),matches=0,decoded_candidate_functions=0,anomalies=[])
    totalfunctions+=len(starts)
    for st in sorted(starts):
     end=min(x for x in bounds if x>st);code=sec[st:end]
     candidates=[]
     for op in [0x58,0x59,0x5d,0x5e]:
      pattern=bytes([op,0x44,0x30]);cursor=0
      while True:
       i=code.find(pattern,cursor)
       if i<0:break
       candidates.append(i);cursor=i+1
     candidates=sorted(set(candidates))
     # No pattern means no literal native3044 instruction in this bounded
     # byte span, regardless of unknown other opcodes. Do not invent execution.
     if not candidates:continue
     rawcandidates+=len(candidates);ins,anomaly=G.decode(code);row['decoded_candidate_functions']+=1
     if anomaly is not None:row['anomalies'].append({'start':st,'relative_pc':anomaly,'unresolved_candidates':[p for p in candidates if p>=anomaly]})
     for j,(pc,op,imm) in enumerate(ins):
      if pc not in candidates or op not in [0x58,0x59,0x5d,0x5e] or imm!=0x3044:continue
      args,status=G.resolve_args(ins,j,2+int(op in [0x59,0x5e]),verbs)
      sites.append({'path':path,'script':starts[st],'function_start':st,'section_pc':st+pc,'file_pc':0x80+st+pc,'opcode':hex(op),'args_push_order':args,'arg_resolution_status':status,'function_decode_anomaly':anomaly,'entry_sha256':row['sha256']});row['matches']+=1
     row.setdefault('candidate_alignments',[]).append({'start':st,'raw_candidate_pcs':candidates,'decoded_target_pcs':[pc for pc,op,imm in ins if op in [0x58,0x59,0x5d,0x5e] and imm==0x3044],'anomaly':anomaly})
    if row['matches'] or row['anomalies']:
     name=sha(path.encode())[:16]+'.ebp';(rawdir/name).write_bytes(b);row['retained_raw']=name
   except Exception as e:row.update(status='UNAVAILABLE_OR_UNSUPPORTED',exception=repr(e),decompression_failures=list(decomp_errors))
  f.seek(0)
  if sha(f.read(hlen))!=header_sha:raise RuntimeError('archive index changed during collection')
 G.V.zlib.decompress=olddecomp
 after=ARCHIVE.stat()
 if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise RuntimeError('archive stat changed during collection')
 failures=[r for r in coverage if r['status']!='COVERED_LITERAL_CODE_SPANS'];anomalies=[r for r in coverage if r.get('anomalies')]
 result={'collection_complete':budgetfail is None and len(coverage)==len(paths),'method':'A designated reference archive literal/nativecall site discovery, not execution','exe_sha256':sha(exe),'native_result_slot':{'address':hex(addr),'bytes':binding.hex(),'result':'0x50ffb0'},'tools':{'collector_sha256':sha(Path(__file__).read_bytes()),'decoder_path':str(GEN.relative_to(ROOT)),'decoder_sha256':sha(GEN.read_bytes()),'extractor_sha256':sha((ROOT/'agent_flow/tools/vbfextract.py').read_bytes()),'verb_table_sha256':sha(Path(G.VERB_TSV).read_bytes())},'archive':{'path':str(ARCHIVE),'size':before.st_size,'mtime_ns':before.st_mtime_ns,'header_bytes':hlen,'header_sha256':header_sha,'whole_archive_hash':'NOT_RECOMPUTED','ebp_index_entries':len(paths)},'positive_controls':{'synthetic_call_decode':[(6,0x58,0x3044)],'synthetic_argument_order':[1,27],'retained_btlctrl_sha256':control_sha,'actual_control_CALLs':control_calls},'coverage':coverage,'sites':sites,'read_bytes':totalbytes,'function_spans':totalfunctions,'raw_candidates':rawcandidates,'unsupported_entries':len(failures),'anomalous_candidate_entries':len(anomalies),'budget_stop':budgetfail,'elapsed_seconds':time.monotonic()-start,'limits':'Header/index and each decompressed entry identified, whole archive not rehashed. Explicit unsupported/decode gaps prevent universal absence. Sites are syntax and resolved producer leads, not actual branch execution/dynamic range/initialized actor type. No game/PC/native/peer edits.'}
 out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:result[k] for k in ['collection_complete','read_bytes','function_spans','raw_candidates','unsupported_entries','anomalous_candidate_entries','budget_stop','elapsed_seconds']}));print('ALIGNED_TARGET_SITES',len(sites))
 if not result['collection_complete']:raise RuntimeError('bounded collection incomplete; raw coverage retained')
if __name__=='__main__':main()
