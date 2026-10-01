"""Original-byte/CFG proof of selector branches and all byte-index addresses."""
import argparse,hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
T=P.parent if(P.parent/'validate-title-source-annotations.py').exists() else P/'dependencies'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(src,out):
 if out.exists():raise RuntimeError('immutable result exists')
 status=json.loads((src/'capture-01.status.json').read_text())
 if status.get('exit')!=0 or status.get('terminal') is not True or status.get('exception') is not None or status['driver_sha256']!=sha(src/'capture.py') or not(src/'capture-01.stdout').read_bytes() or(src/'capture-01.stderr').read_bytes():raise RuntimeError('upstream capture failed/incomplete')
 v=json.loads((src/'source-01.json').read_text())
 if v.get('wrapper_complete') is not True or v['wrapper_sha256']!=sha(src/'capture.py'):raise RuntimeError('capture wrapper incomplete/mixed')
 V=load('presentation_annotation',T/'validate-title-source-annotations.py');roles=V.validate(v)
 G=load('presentation_cfg',T/'prove_owner_reload_order.py')
 if sha(T/'prove_owner_reload_order.py')!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise RuntimeError('graph identity changed')
 legacy=src/'retained/selector-callers-raw-01.json'
 if sha(legacy)!='a362ef91feb4e2f80045af35a825d0dbc6b1556f08a45d0c4ccf271b2fcf0576':raise RuntimeError('retained caller source changed')
 old=json.loads(legacy.read_text());old_roles=V.validate(old)
 if old.get('selector_discovery_driver_sha256')!=sha(src/'retained/selector-callers.py'):raise RuntimeError('retained caller driver changed')
 raw=(G.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise RuntimeError('wrong original image')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
 sections=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,offset in sections:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
  raise RuntimeError('unbacked original bytes')
 if [(int(r['start'],16),int(r['end_exclusive'],16)) for r in v['ranges']]!=[(0x309230,0x3092f7),(0x306bd0,0x306c5b)]:raise RuntimeError('required source population changed')
 for r in v['ranges']+old['ranges']:
  lo=int(r['start'],16);hi=int(r['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(lo,hi-lo):raise RuntimeError('original byte mismatch')
 ix={int(i['pc'],16):i for r in v['ranges'] for i in r['instructions']}
 def need(pc,m,a):
  if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('operation changed '+hex(pc))
 pins=[(0x309230,'mov','qword ptr [rsp + 8], rbx'),(0x309235,'push','rdi'),(0x309236,'sub','rsp, 0x60'),
 (0x30923a,'mov','rax, qword ptr [rip + 0x1c3b5ef]'),(0x309241,'xor','rax, rsp'),(0x309244,'mov','qword ptr [rsp + 0x58], rax'),
 (0x309249,'movdqa','xmm0, xmmword ptr [rip + 0xa0715f]'),(0x309251,'mov','rbx, rdx'),(0x309254,'mov','rax, qword ptr [rip + 0x2bb5edd]'),(0x30925b,'mov','rdi, rcx'),
 (0x30925e,'movdqa','xmm1, xmmword ptr [rip + 0xa0715a]'),(0x309266,'mov','dword ptr [rsp + 0x50], 0x4e'),(0x30926e,'movdqu','xmmword ptr [rsp + 0x20], xmm0'),
 (0x309274,'movdqa','xmm0, xmmword ptr [rip + 0xa07154]'),(0x30927c,'movdqu','xmmword ptr [rsp + 0x40], xmm0'),(0x309282,'movdqu','xmmword ptr [rsp + 0x30], xmm1'),
 (0x309288,'test','rax, rax'),(0x30928b,'je','0x3092be'),(0x30928d,'mov','ecx, dword ptr [rax + 0xc]'),(0x309290,'call','0x20e600'),(0x309295,'test','rax, rax'),(0x309298,'je','0x3092be'),
 (0x30929a,'mov','rax, qword ptr [rip + 0x2bb5e97]'),(0x3092a1,'mov','ecx, dword ptr [rax + 0xc]'),(0x3092a4,'call','0x20e600'),(0x3092a9,'mov','rcx, qword ptr [rip + 0x2bb5e88]'),(0x3092b0,'movzx','edx, word ptr [rcx + 8]'),(0x3092b4,'imul','ecx, edx, 0x113'),(0x3092ba,'add','ecx, eax'),(0x3092bc,'jmp','0x3092c0'),(0x3092be,'xor','ecx, ecx'),
 (0x3092c0,'cmp','rbx, rcx'),(0x3092c3,'je','0x3092cb'),(0x3092c5,'movzx','eax, word ptr [rbx + 0x24]'),(0x3092c9,'jmp','0x3092df'),
 (0x3092cb,'mov','rax, qword ptr [rdi + 0x698]'),(0x3092d2,'movzx','eax, byte ptr [rax + 4]'),(0x3092d6,'sub','eax, 0x1b'),(0x3092d9,'cdqe',''),(0x3092db,'mov','eax, dword ptr [rsp + rax*4 + 0x20]'),
 (0x3092df,'mov','rcx, qword ptr [rsp + 0x58]'),(0x3092e4,'xor','rcx, rsp'),(0x3092e7,'call','0x808c40'),(0x3092ec,'mov','rbx, qword ptr [rsp + 0x70]'),(0x3092f1,'add','rsp, 0x60'),(0x3092f5,'pop','rdi'),(0x3092f6,'ret',''),
 (0x306be0,'mov','rsi, rdx'),(0x306be3,'mov','rdi, rcx'),(0x306c0a,'mov','ebx, 3'),(0x306c3d,'mov','rdx, rsi'),(0x306c4a,'mov','rcx, rdi'),(0x306c4d,'call','0x309230'),(0x306c52,'mov','edx, eax'),(0x306c54,'mov','ecx, ebx'),(0x306c56,'call','0x32fc30')]
 for pc,m,a in pins:need(pc,m,a)
 body=v['ranges'][0];local={int(i['pc'],16):i for i in body['instructions']}
 g=G.graph(local,0x309230,0x3092f7)
 if g['returns']!=[0x3092f6] or {target for pc,target in g['calls']}!={'0x20e600','0x808c40'} or len(g['calls'])!=3:raise RuntimeError('changed function/control boundary')
 if [(i['pc'],i['mnemonic'],i['args']) for i in body['instructions'] if i['mnemonic'].startswith('j')]!=[('0x30928b','je','0x3092be'),('0x309298','je','0x3092be'),('0x3092bc','jmp','0x3092c0'),('0x3092c3','je','0x3092cb'),('0x3092c9','jmp','0x3092df')]:raise RuntimeError('unexpected local guard')
 const=read(0xd103b0,48);table=list(struct.unpack('<12I',const))+[ix[0x309266] and 0x4e]
 if table!=list(range(42,79,3)):raise RuntimeError('original table changed')
 rows=[]
 for t in range(256):
  # This is the exact zero-extended-byte SUB32->CDQE sequence, not a
  # real-number substitution for a floating or machine-code execution.
  u=(t-0x1b)&0xffffffff;index=u-(1<<32) if u&(1<<31) else u;off=0x20+4*index
  if 27<=t<=39:kind='initialized-table';value=table[index]
  elif t<=26:kind='outside-table-preceding';value=None
  elif t==40:kind='local-unwritten-gap';value=None
  elif t<=42:kind='stored-cookie-word';value=None
  elif t<=44:kind='saved-rdi-word';value=None
  elif t<=46:kind='caller-return-address-word';value=None
  elif t<=48:kind='saved-rbx-word';value=None
  else:kind='outside-frame-caller-bytes';value=None
  rows.append({'type_byte':t,'signed_index':index,'frame_offset':off,'end_exclusive':off+4,'classification':kind,'initialized_table_value':value})
 if [r['type_byte'] for r in rows if r['classification']=='initialized-table']!=list(range(27,40)) or min(r['frame_offset'] for r in rows)!=-0x4c or max(r['frame_offset'] for r in rows)!=0x3b0:raise RuntimeError('byte domain incomplete')
 partition=[]
 for row in rows:
  if partition and partition[-1]['classification']==row['classification']:partition[-1]['type_max']=row['type_byte'];partition[-1]['last_read_end_exclusive']=row['end_exclusive']
  else:partition.append({'type_min':row['type_byte'],'type_max':row['type_byte'],'classification':row['classification'],'first_read_offset':row['frame_offset'],'last_read_end_exclusive':row['end_exclusive']})
 counts={k:sum(r['classification']==k for r in rows) for k in {r['classification'] for r in rows}}
 if sorted(counts.values())!=[1,2,2,2,2,13,27,207]:raise RuntimeError('domain partition failed')
 # Reuse the retained caller observation; no new eight-site census or claim
 # about all indirect calls. The new prefix closes just the producer transfer.
 callers=old['direct_call_sites'];sites=[int(s['call_pc'],16) for s in callers]
 if sites!=[0x25daed,0x306c56,0x3140ba,0x352304,0x3530cf,0x3535a3,0x3ca07c,0x50d115]:raise RuntimeError('retained site population changed')
 oldix={int(i['pc'],16):i for r in old['ranges'] for i in r['instructions']}
 for pc in sites:
  if(oldix[pc]['mnemonic'],oldix[pc]['args'])!=('call','0x32fc30'):raise RuntimeError('retained call identity changed')
 result={'producer_complete':True,'method':'A STATIC_ONLY original-byte/address/CFG proof; no native/game execution',
 'exe_sha256':hashlib.sha256(raw).hexdigest(),'driver_sha256':sha(Path(__file__)),'source_sha256':sha(src/'source-01.json'),
 'annotation_prerequisite':roles,'retained_annotation_prerequisite':old_roles,'retained_callers_sha256':sha(legacy),'instruction_assertions':len(pins),
 'graphs':[{'entry':'0x309230','visited':len(g['visited']),'returns':[hex(i) for i in g['returns']],'calls':[{'pc':hex(pc),'target':target} for pc,target in g['calls']]}],
 'original_constants':{'address':'0xd103b0','bytes':const.hex(),'sha256':hashlib.sha256(const).hexdigest(),'table':table,'last_entry_literal_pc':'0x309266'},
 'comparison':'Full64-bit entry RDX(savedRBX) equals zero-extended computedECX. Null context or null first resolver uses0. Other arm rereads context, uses low32 second20E600 return + u16(context+8)*0x113 modulo32. First and second calls not assumed equal/stable.',
 'unequal_branch':'MOVZX EAX WORD[entryRDX+24] yields0..65535 if accessible; no local type/table bound. Normal-return cookie check is not selector validation.',
 'equal_branch':{'formula':'index=SEXT32((ZEXT8(type)-27) modulo2^32); address=postprologueRSP+20hex+4*index','table_domain':[27,39],'offset_extrema':[-76,944],'partition':partition,'cases':rows},
 'counterexamples':[{k:r[k] for k in r} for r in rows if r['type_byte'] in [26,27,39,40,41,42,43,45,47,48,49,255]],
 'caller_transfer':{'start':'0x306bd0','captured_prefix_end':'0x306c5b','producer_call':'0x306c4d','request_call':'0x306c56','manager':3,'selector':'normal-return EAX zero-extended into EDX; no intervening check','retained_sites':len(callers),'complete_caller_cfg':False},
 'premises':['Correct original body, normal ABI/valid private frame/accessible input references','Named external calls normal-return and preserve nonvolatile registers/frame memory per stated contracts; no unproved native helper effects','Frame/table/cookie/saved-word provenance requires no asynchronous/alias interference'],
 'established':['Table read stays inside13initializedDWORDs iff equal-branch typeByte27..39; no local type guard','Table branch for those types returns42..78 step3, independent existing fact corroborated not new census','Out-of-band source addresses include gap/cookie/saved registers/return-address words, not a sanitized presentation table','Unequal branch returns full u16; immediate original caller carries result to manager3 request without index check'],
 'unresolved':['Natural type/context/branch admission and actual loaded pointers/relocation','External20E600 and cookie helper effects/normal returns/interference','Values of gap/caller bytes; whether any out-of-band read naturally occurs or faults','Other producers/callers/indirect edges, whole OV42/21 rejection or gameplay consequences'],
 'limits':'256 algebraic byte-address cases and source pins are not execution tests. No unsafe state/native code/game launched; retained site integrity is not independent semantic acceptance.'}
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'producer_complete':True,'pins':len(pins),'byte_domain_cases':len(rows),'table_domain':[27,39],'source_counterexamples':'not executed'}))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--src',type=Path,default=P);args=ap.parse_args();main(args.src,args.output)
