"""Conditional representation proof from original instructions, not new samples."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def need(ix,pc,m,a):
 if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('original transfer witness changed '+hex(pc))
def derive(ix,tables,G):
 expected=[(0x267e14,'mov','eax, dword ptr [rcx]'),(0x267e18,'jle','0x267e3b'),
 (0x267e1a,'dec','eax'),(0x267e1c,'movsxd','r8, eax'),(0x267e1f,'mov','dword ptr [rcx], eax'),
 (0x267e21,'movzx','edx, byte ptr [r8 + rcx + 4]'),(0x267e27,'sub','edx, 1'),(0x267e2a,'je','0x267e51'),
 (0x267e2c,'cmp','edx, 1'),(0x267e2f,'je','0x267e42'),(0x267e36,'call','0x8620c0'),
 (0x267e3b,'xor','eax, eax'),(0x267e42,'cvttss2si','eax, dword ptr [rcx + r8*4 + 0x184]'),
 (0x267e51,'mov','eax, dword ptr [rcx + r8*4 + 0x184]'),
 (0x267fd9,'call','0x262440'),(0x267fde,'mov','eax, dword ptr [rbp - 0x18]'),
 (0x267fe1,'shr','eax, 0x1c'),(0x267fe4,'cmp','eax, 5'),(0x267fe7,'ja','0x268062'),
 (0x267fe9,'lea','rdx, [rip - 0x147ff0]'),(0x267ff0,'mov','ecx, dword ptr [rdx + rax*4 + 0x1480e8]'),
 (0x267ffa,'jmp','rcx'),(0x268004,'movzx','ecx, byte ptr [rcx + rax]'),
 (0x268015,'movsx','ecx, byte ptr [rcx + rax]'),(0x268026,'movzx','ecx, word ptr [rax + rcx*2]'),
 (0x268037,'movsx','ecx, word ptr [rax + rcx*2]'),(0x268048,'mov','ecx, dword ptr [rax + rcx*4]'),
 (0x268058,'movss','xmm0, dword ptr [rax + rcx*4]'),
 (0x268008,'mov','dword ptr [rbp - 0x10], ecx'),(0x268019,'mov','dword ptr [rbp - 0x10], ecx'),
 (0x26802a,'mov','dword ptr [rbp - 0x10], ecx'),(0x26803b,'mov','dword ptr [rbp - 0x10], ecx'),
 (0x26804b,'mov','dword ptr [rbp - 0x10], ecx'),(0x26805d,'movss','dword ptr [rbp - 0x10], xmm0'),
 (0x268078,'movss','xmm0, dword ptr [rbp - 0x10]'),(0x2680c6,'mov','eax, dword ptr [rbp - 0x10]'),
 (0x268062,'movsx','ecx, word ptr [rbp - 0x2c]'),(0x268066,'sub','ecx, 1'),
 (0x268069,'je','0x2680ae'),(0x26806e,'jne','0x2680dd'),
 (0x268076,'jge','0x2680dd'),(0x268080,'mov','byte ptr [rax + rbx + 4], 2'),
 (0x268098,'movss','dword ptr [rbx + rcx*4 + 0x184], xmm0'),
 (0x2680b4,'jge','0x2680dd'),(0x2680b9,'mov','byte ptr [rax + rbx + 4], 1'),
 (0x2680c9,'mov','dword ptr [rbx + rcx*4 + 0x184], eax'),
 (0x2650b9,'mov','eax, r8d'),(0x2650bc,'sar','eax, 0x18'),(0x2650bf,'mov','ebx, r8d'),
 (0x2650c2,'and','eax, 7'),(0x2650c8,'cmp','eax, 5'),(0x2650cb,'ja','0x26516c'),
 (0x2650d1,'lea','rcx, [rip - 0x1450d8]'),(0x2650da,'mov','r8d, dword ptr [rcx + rax*4 + 0x145180]'),
 (0x2650e5,'jmp','r8'),(0x309c13,'mov','dword ptr [rdx], eax'),
 (0x348355,'call','0x267e10'),(0x34835a,'mov','r8d, eax'),(0x348363,'call','0x2650b0'),
 (0x34836e,'call','0x267e10'),(0x348373,'mov','r8d, eax'),(0x34837c,'call','0x2650b0'),
 (0x348381,'mov','rdx, rsi'),(0x348384,'mov','rcx, rax'),(0x34838a,'call','0x309c00'),
 (0x348880,'call','0x267e10'),(0x348888,'mov','ebx, eax'),(0x34888a,'call','0x267e10'),
 (0x34888f,'mov','edx, ebx'),(0x348891,'mov','ecx, eax'),(0x348893,'call','0x30eea0'),
 (0x30eea8,'cmp','edx, -1'),(0x30eeb2,'add','bx, ax'),(0x30eead,'mov','eax, 0xd0'),
 (0x30eeb7,'mov','ebx, 0xffff'),(0x30eef5,'movzx','r8d, bx')]
 for op in expected:need(ix,*op)
 pop=G.graph(ix,0x267e10,0x267e5e)
 if set(pop['returns'])!={0x267e41,0x267e50,0x267e5d}:raise RuntimeError('integer-pop exit population changed')
 for tag,ret,loadpc in [(1,0x267e5d,0x267e51),(2,0x267e50,0x267e42)]:
  g=G.graph(ix,0x267e10,0x267e5e,fixed={0x267e18:False,0x267e2a:tag==1,0x267e2f:tag==2})
  if g['returns']!=[ret] or g['calls'] or not G.dominates(g,loadpc,ret):raise RuntimeError('tag-specific original pop path changed')
 empty=G.graph(ix,0x267e10,0x267e5e,fixed={0x267e18:True})
 if empty['calls'] or empty['returns']!=[0x267e41]:raise RuntimeError('empty pop path changed')
 targets=tables[0]['targets'];want=[hex(x) for x in [0x267ffc,0x26800d,0x26801e,0x26802f,0x268040,0x268050]]
 if targets!=want:raise RuntimeError('typed load dispatch changed')
 paths=[];loadpcs=[0x268004,0x268015,0x268026,0x268037,0x268048,0x268058]
 temppcs=[0x268008,0x268019,0x26802a,0x26803b,0x26804b,0x26805d]
 for width,dest in enumerate(targets):
  for kind in [1,2]:
   # Dispatch edge comes from verified original table, never linear decoding of data.
   local={pc:dict(i) for pc,i in ix.items()};local[0x267ffa]['args']=dest
   g=G.graph(local,0x267fc0,0x2680e8,fixed={0x267fe7:False,0x268069:kind==1,0x26806e:False,0x268076:False,0x2680b4:False})
   tagpc=0x2680b9 if kind==1 else 0x268080;storepc=0x2680c9 if kind==1 else 0x268098
   usepc=0x2680c6 if kind==1 else 0x268078
   if not all(G.dominates(g,a,b) for a,b in [(loadpcs[width],temppcs[width]),(temppcs[width],usepc),(usepc,storepc),(tagpc,storepc)]):raise RuntimeError('load/tag/store control flow changed')
   # Frame is private and resolver has returned. No later callee occurs on these
   # paths. Width-inclusive overlap rejects a changed temporary before its use.
   for pc in g['visited']:
    if pc==temppcs[width] or not temppcs[width]<pc<usepc:continue
    for mem in ix[pc]['memory']:
     if mem['base']=='rbp' and mem['index'] is None and mem['role'] in ('w','rw'):
      lo=mem['displacement'];hi=lo+mem['size']
      if lo<-0x0c and hi>-0x10:raise RuntimeError('loaded temporary overwritten before payload copy')
   paths.append(dict(width=width,resolved_kind=kind,tag=kind,load_entry=dest,tag_pc=hex(tagpc),payload_store=hex(storepc)))
 # Every pointer-return arm masks the offset, independently of incoming width/kind.
 getter_targets=tables[1]['targets']
 if set(getter_targets)!={hex(x) for x in [0x2650e8,0x2650fc,0x265110,0x26512d,0x265141,0x265155]}:raise RuntimeError('reference getter dispatch changed')
 for maskpc in [0x2650ee,0x265102,0x26511f,0x265133,0x265147,0x26515e,0x265170]:need(ix,maskpc,'and','eax, 0xffffff')
 import capstone
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 for pc in pop['visited']:
  i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access()
  if {i.reg_name(x) for x in wr}&{'rbx','ebx','bx','bl','bh'}:raise RuntimeError('second pop can overwrite first argument EBX carrier')
 # These are arithmetic predictions under the proved load/kind premises, not calls.
 def sx(x,n):x&=(1<<n)-1;return x-(1<<n) if x&(1<<(n-1)) else x
 def dec(v):return 0xffff if v==-1 else (v+0xd0)&0xffff
 rows=[]
 for w in range(511,535):
  e=w-0xd0
  vals=[e&255,sx(e,8),e&65535,sx(e,16),e]
  rows.append(dict(word=w,encoded=e,int_kind_decoded={k:dec(v) for k,v in zip(['u8','s8','u16','s16','s32'],vals)}))
 if any(any(r['int_kind_decoded'][k]!=r['word'] for k in ['u16','s16','s32']) for r in rows):raise RuntimeError('word-preserving typed load invariant contradicted')
 if any(r['int_kind_decoded']['u8']!=r['word']-256 or r['int_kind_decoded']['s8']!=r['word']-256 for r in rows):raise RuntimeError('byte-wide countermodel changed')
 return dict(original_pop='positive valid-depth tag1 returns exact payload DWORD; tag2 CVTTSS2SI; empty/negative depth returns0; unknown tags call original error handler then local zero only if it returns normally',
 native_store='309C13 writes raw DWORD through first native out pointer. It does not use typed POPV clamps. Both descriptors are popped before2650B0; first return pointer is retained inRSI and becomesRDX. Width/float fields do not select this write.',
 selector_argument='348880 first integer pop->EBX preserved across34888A second pop->EDX at348893/30EEA0. Second pop->ECX. This does not prove authored stack argument order.',
 typed_load_paths=paths,
 low16_invariant='For available original queue words w other thanCF/FFFF, e=w-D0. Any integer-tagged transfer v with low16(v)=low16(e) and v!=-1 decodes to w because (v+D0) mod2^16=w. u16/s16 loads satisfy both; -1 occurs for either only when low16(e)=FFFF, corresponding to excluded wordCF. Full32 identity is stronger than required.',
 candidate_calculations=rows,
 float_countermodel=dict(word=511,encoded=303,payload_hex='0000012f',binary32_class='positive subnormal <1',int_pop=0,decoder_word=208,
   condition='Same raw encoded DWORD is loaded as payload and tagged2; relevant SIMD exceptions masked, including denormal if applicable. DAZ changes the subnormal to0 but not the resulting integer0. No authored float binding or machine-code execution claimed.'),
 remaining='Actual source declarations/references, successful resolver same-cell binding, valid backing capacity, stack depth, absence of intervening writes/aliasing, natural interpreter reachability and later command admission remain open.')

def main(out):
 if out.exists():raise RuntimeError('immutable result exists')
 pins=json.loads((P/'input-identities-01.json').read_text())['inputs']
 for x in pins:
  if sha(P/x['path'])!=x['sha256']:raise RuntimeError('retained prerequisite changed '+x['path'])
 receipt=json.loads((P/'capture-01.status.json').read_text())
 if receipt.get('terminal') is not True or receipt.get('exit')!=0 or receipt.get('exception') is not None or receipt.get('driver_sha256')!=sha(P/'capture.py'):raise RuntimeError('upstream capture failed/incomplete/stale')
 if not (P/'capture-01.stdout').read_bytes().strip() or (P/'capture-01.stderr').read_bytes():raise RuntimeError('missing/error capture output')
 V=load('shared_annotation_validator','validate-title-source-annotations.py');G=load('retained_CFG','prove_owner_reload_order.py')
 if not callable(getattr(G,'graph',None)) or not callable(getattr(G,'dominates',None)):raise RuntimeError('required actual CFG interface missing')
 names=['source-01.json']+['retained/remap/'+n for n in ['spattack-info-raw-01.json','effective-and-script-id-raw-01.json','spattack-queue-reader-raw-01.json','spattack-output-writers-raw-02.json']]
 ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());im=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 pin='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 if hashlib.sha256(im).hexdigest()!=pin:raise RuntimeError('original image changed')
 pe=struct.unpack_from('<I',im,60)[0];op=struct.unpack_from('<H',im,pe+20)[0];secs=[struct.unpack_from('<IIII',im,pe+24+op+k*40+8) for k in range(struct.unpack_from('<H',im,pe+6)[0])]
 def rd(a,n):
  for vs,v,rs,r in secs:
   if 0x120000+v<=a and a+n<=0x120000+v+rs:return im[r+a-0x120000-v:r+a-0x120000-v+n]
  raise RuntimeError('unbacked original range')
 ix={};checks=[];sourcepins=[]
 for n in names:
  r=json.loads((P/n).read_text());checks.append(V.validate(r));sourcepins.append(dict(path=n,sha256=sha(P/n)))
  if r['exe_sha256']!=pin:raise RuntimeError('source provenance mismatch')
  for q in r['ranges']:
   blob=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']));lo=int(q['start'],16)
   if blob!=rd(lo,len(blob)):raise RuntimeError('retained source differs from original EXE')
   for i in q['instructions']:
    pc=int(i['pc'],16)
    if pc in ix and ix[pc]!=i:raise RuntimeError('source overlap disagreement')
    ix[pc]=i
 source=json.loads((P/'source-01.json').read_text())
 if source.get('driver_sha256')!=sha(P/'capture-index-path.py') or source.get('invocation_driver_sha256')!=sha(P/'capture.py'):raise RuntimeError('actual capture invocation identity changed')
 for t in source['tables']:
  b=bytes.fromhex(t['bytes'])
  if len(b)!=24 or b!=rd(int(t['start'],16),24) or hashlib.sha256(b).hexdigest()!=t['sha256'] or t['targets']!=[hex(0x120000+x) for x in struct.unpack('<6I',b)]:raise RuntimeError('original dispatch table mismatch')
 old=json.loads((P/'retained/EXP013/observations.json').read_text())
 if old.get('status')!='OBSERVED_MATCHING_BOUNDARIES' or len(old.get('cases',[]))!=14 or old['probe_sha256']!=sha(P/'retained/EXP013/probe.py') or old['reader_sha256']!=sha(P/'retained/EXP013/reader-snapshot.py') or old['exe_sha256']!=pin:raise RuntimeError('historical EXP013 incomplete/mismatched')
 if hashlib.sha256(rd(0x267e10,78)).hexdigest()!=old['code']['0x267e10']['sha256']:raise RuntimeError('historical pop code identity mismatch')
 facts=derive(ix,source['tables'],G)
 z=dict(producer_complete=True,method='A retained shipping code and conditional representation invariant; bounded static decode only, no new native/emulator/live calls',
        exe_sha256=pin,driver_sha256=sha(Path(__file__)),source_pins=sourcepins,annotation_prerequisites=checks,input_pins=pins,facts=facts,
        retained_EXP013=dict(cases=14,new_cases=0,limits='historical synthetic0x284 stack/error-handlerRETstub/Unicorn2.1.4; corroboration, not actual interpreter state'),
        limits='Valid stable resolved record and four writable output bytes; typed load width0..5 and kind1/2; PUSHV depth0..62 then valid pop, private stack/frame, normal native ABI/returns/no interference. Static resolved dispatch edges are not natural reachability; no entire interpreter, reference lifetime, actual authored widths/aliases or command execution proven.',
        affected_claims=['OV42 unchanged VM-transfer premise of spattack-native-word-remap','FABLE native queue output versus typed PUSHV/kind representation','OPUS exact out-pointer/selector pop argument contract'])
 with out.open('x') as f:json.dump(z,f,indent=2)
 print('PROVED conditional integer transfer/low16 sufficiency; byte/float countermodels; natural binding still OPEN')
if __name__=='__main__':main(Path(sys.argv[1]))
