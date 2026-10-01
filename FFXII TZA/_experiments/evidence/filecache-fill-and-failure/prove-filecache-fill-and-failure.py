"""Original key provenance and conditional failure call sequence, no live/native run."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
ROOT=next(p for p in W.parents if (p/'Database/FFXII TZA/_experiments/evidence').is_dir())
E=ROOT/'Database/FFXII TZA/_experiments/evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def retained(folder,pin,name):
 if sha(folder/'manifest.json')!=pin:raise ValueError('retained manifest identity failed')
 m=json.loads((folder/'manifest.json').read_text());member=next(x for x in m['members'] if x['path']==name)
 if sha(folder/name)!=member['sha256']:raise ValueError('retained input member identity failed')
 return json.loads((folder/name).read_text()),dict(folder=str(folder.relative_to(ROOT)),manifest_sha256=pin,path=name,sha256=member['sha256'])
def main(src,out):
 if out.exists():raise ValueError('immutable result exists')
 raw=[];deps=[]
 for folder,pin,name in [(E/'filecache-key-preprocessing','f7b5ffccc16ae832d1a7279e1f616c2687e97868b4d98d4378db48ba17e15db6','filecache-key-boundaries-source-01.json'),
                        (E/'filecache-key-preprocessing','f7b5ffccc16ae832d1a7279e1f616c2687e97868b4d98d4378db48ba17e15db6','filecache-key-boundaries-source-02.json'),
                        (E/'filecache-equal-key','c34fb511c5468f266db55c13c58aaf7318e3ede3b4c285fd4a3656598f5c1b09','filecache-equal-key-source-01.json')]:
  v,d=retained(folder,pin,name);raw.append(v);deps.append(d)
 for prefix,driver,name in [('filecache-fill-key-resolver-capture-01','capture-filecache-fill-key-provenance.py','filecache-fill-key-resolver-source-01.json'),
                           ('filecache-release-allocator-thunks-qualification-01','qualify-filecache-failure-thunks.py','filecache-release-allocator-thunks-qualified-01.json')]:
  st=json.loads((src/(prefix+'.status.json')).read_text())
  if st.get('exit')!=0 or st.get('terminal') is not True or st.get('driver_sha256')!=sha(src/driver):raise ValueError('required producer upstream failed/incomplete/stale')
  if not(src/(prefix+'.stdout')).read_bytes().strip() or (src/(prefix+'.stderr')).read_bytes():raise ValueError('required producer output missing/error')
  v=json.loads((src/name).read_text())
  field='invocation_driver_sha256' if 'capture' in driver else 'qualification_driver_sha256'
  if v.get(field)!=sha(src/driver):raise ValueError('actual upstream invocation identity failed')
  raw.append(v)
 V=load('fill_failure_roles',src/'validate-title-source-annotations.py')
 for v in raw:
  if v['exe_sha256']!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong original image')
  V.validate(v)
 ranges={int(q['start'],16):q for v in raw for q in v['ranges']}
 required=[(0x59ee90,0x59f1fc,'b6631ed174665398c271a8ad7cd9bb57310fc5ffe1b3da0a2d59234caaaea036'),
  (0x59a9b0,0x59aad5,'136b8edf92cd2249948a2b64c352813d83e5c702cca78460593ffc3b510fe5ab'),
  (0x1d6d20,0x1d6d6f,'1450e4923b04dec355461f06e9d0b52e1ead55e83c6e1316ee5685d544632725'),
  (0x20c1b0,0x20c2f2,'1d0c92e0a1312e02b1d838f4724e02d257a2ddedcd63cd5a8f4d61f5dac72008'),
  (0x1d6a20,0x1d6a6d,'1fb87c5cf1cf0d9cc2f68b6d328a5cef161e4d3286abb179f2299f5b8f30ddb6'),
  (0x20b680,0x20b83b,'6351d3140ac8de9d876ff304797e949053c599ed62218e8075c965d1a8f20e00'),
  (0x20c300,0x20c438,'7f56074a74f27acc403c1f72c1c8a5d2538e7b889e2056d748f877b3a7918245'),
  (0x20b0f0,0x20b126,'b1da229162eec2af3b5d3a189ad84cf951c1b3088bf8ec9371c780e918a08ee6'),
  (0x1d6b00,0x1d6b1e,'6789b9059f785f40178f250fad4a848d281caa716ec3e7ff70044e66304caa6b'),
  (0x20be40,0x20be45,'9ea1b5a6305ab65a5a39e6a355bdba14459c993ba6f8e545f435331120aace26'),
  (0x210ec0,0x210ecb,'eb913ece367750b730dced1bdb6b26910a40265b985fec6e44ea2d5eb9626e4d'),
  (0x85e730,0x85e737,'5d4894502060351fbcf564d58fb893ec562008b824aedd793051746a482b0e8c')]
 for lo,hi,pin in required:
  q=ranges[lo]
  if (int(q['end_exclusive'],16),q['sha256'])!=(hi,pin):raise ValueError('required original complete boundary/identity failed')
 ix={int(i['pc'],16):i for q in ranges.values() for i in q['instructions']}
 gp=src/'prove_owner_reload_order.py'
 if sha(gp)!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise ValueError('reviewed CFG helper changed')
 G=load('fill_failure_graph',gp)
 tails={0x20b0f0:'qword ptr [rip + 0x6b7a22]',0x1d6b00:'0x20be40',0x20be40:'0x20b0f0',0x210ec0:'0x85e730',0x85e730:'qword ptr [rip + 0x64409]'}
 gs={lo:G.graph(ix,lo,hi,tail=tails.get(lo)) for lo,hi,pin in required}
 def need(pc,m,args):
  if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('required original dataflow operation changed '+hex(pc))
 ops=[(0x59eec1,'mov','rdi, rdx'),(0x59eec4,'mov','r15, rcx'),(0x59efd7,'lea','r9, [r15 + 0x28]'),
  (0x59efe2,'mov','rcx, rdi'),(0x59efe5,'call','0x1d6d20'),(0x59f18f,'mov','rdx, r14'),
  (0x59f192,'call','0x19aee0'),(0x59f19b,'test','rax, rax'),(0x59f19e,'je','0x59f1c0'),
  (0x59f1ab,'test','r12b, r12b'),(0x59f1ae,'je','0x59f1bc'),(0x59f1b0,'mov','edx, dword ptr [r15 + 0x28]'),(0x59f1b7,'call','0x59a9b0'),
  (0x1d6d34,'mov','rbx, r9'),(0x1d6d3c,'mov','rbp, rcx'),(0x1d6d47,'mov','qword ptr [rsp + 0x20], rbx'),
  (0x1d6d52,'mov','rdx, rbp'),(0x1d6d55,'call','0x20c1b0'),(0x20c1ee,'mov','r14, qword ptr [rsp + 0x1a0]'),
  (0x20c213,'call','0x20c440'),(0x20c218,'cmp','byte ptr [rsp + 0x40], 0'),(0x20c21d,'je','0x20c2c7'),
  (0x20c228,'call','0x674a00'),(0x20c22d,'mov','dword ptr [r14], eax'),(0x20c2c7,'or','rax, 0xffffffffffffffff'),
  (0x59a9c3,'mov','esi, edx'),(0x59a9d4,'mov','qword ptr [rsp + 0x50], rax'),(0x59aa98,'lea','rdx, [rsp + 0x50]'),
  (0x59aaa2,'mov','ecx, esi'),(0x59aaa4,'call','0x1d6a20'),(0x59aaa9,'mov','qword ptr [rbx + 0x20], rax'),
  (0x59aaad,'test','rax, rax'),(0x59aab0,'jg','0x59aac1'),(0x59aab2,'mov','rcx, qword ptr [rsp + 0x50]'),
  (0x59aaba,'je','0x59aac1'),(0x59aabc,'call','0x1d6b00'),(0x1d6b06,'mov','rbx, rcx'),(0x1d6b11,'mov','rdx, rbx'),
  (0x1d6b19,'jmp','0x20be40'),(0x20be40,'jmp','0x20b0f0'),(0x210ec6,'jmp','0x85e730'),
  (0x85e730,'jmp','qword ptr [rip + 0x64409]'),(0x20c400,'call','0x210ec0'),(0x20c40d,'je','0x20c423'),
  (0x20c423,'xor','eax, eax'),(0x20b726,'call','0x20c300'),(0x20b72b,'mov','rbx, rax'),(0x20b737,'mov','rax, rbx')]
 for op in ops:need(*op)
 nonempty=G.graph(ix,0x20c1b0,0x20c2f2,fixed={0x20c21d:False,0x20c282:True})
 empty=G.graph(ix,0x20c1b0,0x20c2f2,fixed={0x20c21d:True})
 if not G.dominates(nonempty,0x20c22d,0x20c2c1) or 0x20c22d in empty['visited']:raise ValueError('nonempty miss versus empty output-store distinction failed')
 resolver=gs[0x59ee90]
 # CFG domination alone admits an impossible bypass-then-armed path. Preserve
 # the original nonvolatile arm bit through its three definitions and branch.
 need(0x59eed6,'xor','r12b, r12b');need(0x59efc4,'mov','r12b, 1')
 need(0x59efce,'setne','r12b')
 arm_writes=[i['pc'] for i in ranges[0x59ee90]['instructions'] if i['args'].split(', ')[0] in ['r12b','r12d','r12w','r12'] and i['mnemonic'] not in ['cmp','test','push','pop']]
 if arm_writes!=['0x59eed6','0x59efc4','0x59efce']:raise ValueError('unhandled resolver arm definition')
 todo=[(resolver['entry'],False,False)];seen=set();fill_states=[];false_arm_successors=[]
 while todo:
  pc,armed,looked=todo.pop()
  if (pc,armed,looked) in seen:continue
  seen.add((pc,armed,looked))
  if pc==0x59eed6:arms=[False]
  elif pc==0x59efc4:arms=[True]
  elif pc==0x59efce:arms=[False,True] # unknown condition, sound overapproximation
  else:arms=[armed]
  if pc==0x59efe5:looked=True
  if pc==0x59f1b7:fill_states.append((armed,looked))
  for arm in arms:
   successors=resolver['edges'][pc]
   if pc==0x59f1ae:
    successors=[pc+len(bytes.fromhex(ix[pc]['bytes']))] if arm else [0x59f1bc]
    if not arm:false_arm_successors.extend(successors)
   todo.extend((p,arm,looked) for p in successors)
 if not fill_states or any(not arm or not looked for arm,looked in fill_states) or set(false_arm_successors)!={0x59f1bc}:
  raise ValueError('correlated arm/lookup provenance failed or empty')
 direct_key_writes=[i['pc'] for i in ranges[0x59ee90]['instructions'] for m in i['memory'] if m['role'] in ['w','rw'] and m['base']=='r15' and m['displacement']==0x28]
 if direct_key_writes:raise ValueError('resolver key slot overwritten locally')
 key_source=[(i['pc'],i['args']) for i in ranges[0x59a9b0]['instructions'] if i['args'].split(', ')[0]=='esi' and i['mnemonic'] not in ['cmp','test']]
 if key_source!=[('0x59a9c3','esi, edx')]:raise ValueError('fill key register overwritten')
 slot_writes=[i['pc'] for i in ranges[0x59a9b0]['instructions'] for m in i['memory'] if m['role'] in ['w','rw'] and m['base']=='rsp' and m['displacement']==0x50]
 if slot_writes!=['0x59a9d4']:raise ValueError('caller buffer slot changed locally')
 failed_fill=G.graph(ix,0x59a9b0,0x59aad5,fixed={0x59a9df:True,0x59aab0:False,0x59aaba:False})
 if not G.dominates(failed_fill,0x59aaa4,0x59aabc) or 0x59aabc not in failed_fill['visited']:raise ValueError('conditional second-release boundary missing')
 null_wrapper=G.graph(ix,0x20c300,0x20c438,fixed={0x20c40d:True})
 if 0x20c41b in null_wrapper['visited'] or not G.dominates(null_wrapper,0x20c400,0x20c423):raise ValueError('normal null allocation return boundary failed')
 decl=raw[-1]['malloc_import_declaration']
 if decl['iat_va']!='0x8c2b40' or decl['name']!='malloc' or ix[0x85e730]['memory'][0]['rip_target']!='0x8c2b40':raise ValueError('malloc declaration/reference wrong')
 def serial(g):return {'visited':sorted(g['visited']),'calls':g['calls'],'returns':g['returns'],'tails':g['tails']}
 r=dict(method='A STATIC_ONLY',producer_complete=True,driver_sha256=sha(Path(__file__)),
  source_pins=[dict(path=n,sha256=sha(src/n)) for n in ['filecache-fill-key-resolver-source-01.json','filecache-release-allocator-thunks-qualified-01.json']],
  external_dependencies=deps,original_graphs={hex(lo):serial(g) for lo,g in gs.items()},instruction_assertions=len(ops),
  partitions={'nonempty_normalized_cache_miss':serial(nonempty),'empty_normalized_cache_path':serial(empty),'conditional_fill_second_release':serial(failed_fill),'null_wrapper_allocation':serial(null_wrapper)},
  correlated_resolver_proof=dict(reachable_abstract_states=len(seen),fill_states=fill_states,false_arm_successors=sorted(set(false_arm_successors)),arm_definitions=arm_writes,limits='Two boolean facts, SETNE overapproximated both ways; opaque callees preserve nonvolatile R12 under normal ABI. Not natural state/branch-frequency evidence.'),
  conclusions=['For this chain, fill key comes from direct lookup hash of original raw path, not recomputation from separately normalized lowercase archive lookup name. LowDWORD source+28 is populated before ordinary nonempty lookup miss; wrapper preserves its fifth output pointer.',
   'Empty normalized lookup bypasses hash/output-key store and returns-1. Its key output is not newly prepared. Do not apply nonempty miss provenance universally.',
   'On valid equal-key hit with normal malloc16 null return after incoming release,20C300 returns0; insertion/registration propagate0; fill retains its original nonnull buffer slot and invokes1D6B00->20BE40->20B0F0. Two release-boundary invocations receive the same incoming pointer under explicit normal-return/noninterference premises.',
   '210EC0->85E730 tailcalls statically declared malloc with sizeRCX16. No original local throwing-new wrapper is present on that path; imported CRT configuration/effects are not observed.'],
  limits=['NOT a natural OOM/double-free/crash result. Whether16B malloc can normally fail immediately after freeing this particular allocation, with the real loaded heap/handler/thread state, remains unproved.',
   'A duplicate boundary invocation is not proof that both native frees succeed or that the process survives them. No original machine code was executed and no free/malloc stub was used.',
   'One bounded source chain is not complete insertion/address-escape/writer/key-population closure. Archive namespace collision result already independently accepted separately; no rerun.',
   'Normal ABI, stable valid disjoint source/objects/stack, ordinary callee contracts and no interfering mutation are premises. Source raw01 thunk capture lacked a prehashed named wrapper receipt; qualifier verifies original bytes/roles prospectively, without recapture or stronger historical invocation claim.'],
  required_consumers=['FABLE cache-key provenance/OV33 E2 precise remaining premises','OPUS cache ownership and failure-call boundary, with natural allocation-null reachability still open'],
  cleanup='Read-only original image/retained evidence; fresh outputs, finite own helpers; no game/PC/save/config/reference/peer mutation',native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0)
 out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
 print('SOURCE PROVENANCE AND CONDITIONAL SECOND RELEASE VERIFIED; 12 original boundaries; no natural allocation failure claim')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=W);p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.source,a.out)
