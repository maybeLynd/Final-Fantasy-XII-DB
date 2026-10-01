"""Conditional original primary admission; preserve alternate loaders/overrides."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
 s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('primary_cfg','prove-title-queue-consumption.py');S=module('primary_roles','validate-title-source-annotations.py')
def main():
 if len(sys.argv) not in (2,3,4):raise ValueError('fresh result [disposable inputs [disposable upstream]]')
 out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
 if out.exists():raise ValueError('immutable result exists')
 d=src/'capture-bts-primary-admission.py';st=json.loads((src/'bts-primary-admission-capture-01.status.json').read_text())
 if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(d):raise ValueError('primary capture failed/stale')
 if not(src/'bts-primary-admission-capture-01.stdout').read_bytes().strip() or (src/'bts-primary-admission-capture-01.stderr').read_bytes().strip():raise ValueError('primary capture incomplete')
 upstream=pathlib.Path(sys.argv[3]) if len(sys.argv)==4 else S.ROOT/'Database/FFXII TZA/_experiments/evidence/bts-index-binding'
 manifest=upstream/'manifest.json'
 if not manifest.is_file() or P.sha(manifest)!='c57c6b668c5b567014a01c5da45dcbf7899645e4547a6bc310edce0972891abb':raise ValueError('upstream canonical manifest missing/changed')
 members=json.loads(manifest.read_text())['members']
 if len(members)!=152 or any(not(upstream/x['path']).is_file() or P.sha(upstream/x['path'])!=x['sha256'] for x in members):raise ValueError('upstream canonical member missing/changed')
 prior=upstream/'bts-index-binding-result-03.json';r=json.loads(prior.read_text());st0=json.loads((upstream/'bts-index-binding-positive-03.status.json').read_text())
 if r.get('producer_complete') is not True or st0.get('exit')!=0 or st0.get('checker_sha256')!=r.get('checker_sha256') or P.sha(upstream/'prove-bts-index-binding.py')!=r['checker_sha256']:raise ValueError('upstream index result failed/stale')
 for p in r['source_pins']+r['required_invocation_receipts']:
  if P.sha(upstream/p['path'])!=p['sha256']:raise ValueError('upstream index evidence changed')
 pins=[];raw,ix=P.load(src,'bts-primary-admission-source-01.json',pins);annotations=S.validate(raw)
 if raw.get('invocation_driver_sha256')!=P.sha(d):raise ValueError('capture driver changed')
 original=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(original).hexdigest()!=P.SHA:raise ValueError('reference image changed')
 e=struct.unpack_from('<I',original,60)[0];o=struct.unpack_from('<H',original,e+20)[0];secs=[struct.unpack_from('<IIII',original,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',original,e+6)[0])]
 def read(a,n):
  for vs,va,rs,ro in secs:
   if 0x120000+va<=a and a+n<=0x120000+va+rs:return original[ro+a-0x120000-va:ro+a-0x120000-va+n]
  raise ValueError('original bytes unbacked')
 for q in raw['ranges']:
  if bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))!=read(int(q['start'],16),int(q['end_exclusive'],16)-int(q['start'],16)):raise ValueError('primary original bytes changed')
 cfg=P.closed(ix,0x330310,0x330497)
 retained=json.loads((src/'index-path-raw-02.json').read_text());S.validate(retained)
 size={int(i['pc'],16):i for q in retained['ranges'] if q['start'] in ['0x32e400','0x2df960','0x46de70'] for i in q['instructions']}
 for q in retained['ranges']:
  if q['start'] in ['0x32e400','0x2df960','0x46de70'] and bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))!=read(int(q['start'],16),int(q['end_exclusive'],16)-int(q['start'],16)):raise ValueError('retained size bytes changed')
 ops=[(0x330324,'mov','r12d, edx'),(0x330335,'cmp','edx, 0xd4'),(0x33033b,'jne','0x33034f'),(0x33034f,'mov','rdx, rsi'),(0x330352,'mov','ecx, ebp'),(0x330354,'call','0x32e400'),(0x330359,'mov','edi, eax'),(0x33036a,'or','qword ptr [rax + r13 + 0x21a6e48], 0x20000'),(0x330376,'test','edi, edi'),(0x330378,'jle','0x330456'),(0x33039c,'call','0x36a100'),(0x3303c5,'mov','qword ptr [rax + r13 + 0x21a6c00], r15'),(0x330407,'call','0x861eba'),(0x33040e,'call','0x3304a0'),(0x330444,'call','0x32e620'),(0x33045b,'test','r14d, r14d'),(0x330473,'jne','0x330490'),(0x33047a,'call','0x5c5230'),(0x330481,'jne','0x330490'),(0x330483,'lea','r8d, [rsi + 2]'),(0x33048b,'call','0x32eb40')]
 for pc,m,a in ops:P.need(ix,pc,m,a)
 for pc,m,a in [(0x32e41a,'test','r8, r8'),(0x32e41d,'je','0x32e431'),(0x32e431,'call','0x46de70'),(0x32e43d,'jle','0x32e44b'),(0x46de70,'jmp','0x2df960')]:P.need(size,pc,m,a)
 for pc,m,a in [(0x2df960,'movsxd','rax, ecx'),(0x2df963,'imul','r8, rax, 0x1388'),(0x2df96a,'movsxd','rcx, edx'),(0x2df974,'add','r8, rcx'),(0x2df977,'mov','eax, dword ptr [rax + r8*4]'),(0x2df97b,'ret','')]:P.need(size,pc,m,a)
 if size[0x2df96d]['memory'][0]['rip_target']!='0x2ec3ee0':raise ValueError('FST base changed')
 fields=sorted({f for row in r['rows'] for f in row['fields']})
 if len(fields)!=31 or 212 in fields:raise ValueError('cached selector exception is not excluded')
 for f in fields:
  if any(next(e for e in t['entries'] if e['kind']==5)['values'][next(e for e in t['entries'] if e['kind']==5)['indices'].index(3*f)]!=-1 for t in r['fst_alternatives']):raise ValueError('primary missing-size premise changed')
 # Cut the positive-size edge and inspect actual local normal control flow.
 todo=[0x330456];seen=set();calls=[]
 while todo:
  pc=todo.pop()
  if pc in seen:continue
  i=ix[pc];seen.add(pc);m=i['mnemonic'];n=pc+len(bytes.fromhex(i['bytes']))
  if m=='ret':continue
  if m=='jmp':todo.append(int(i['args'],16));continue
  if m.startswith('j'):todo.append(int(i['args'],16))
  if m=='call':calls.append(dict(pc=i['pc'],target=i['args']))
  todo.append(n)
 if calls!=[dict(pc='0x33047a',target='0x5c5230'),dict(pc='0x33048b',target='0x32eb40')]:raise ValueError('nonpositive suffix effects changed')
 result=dict(status='PRODUCER_VALID_CONDITIONAL_PRIMARY_ADMISSION_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,annotation_prerequisite=annotations,normal_cfg=cfg,nonpositive_suffix_calls=calls,fields=fields,
  upstream_index_result=dict(path=str(prior.relative_to(S.ROOT)) if prior.is_relative_to(S.ROOT) else str(prior),sha256=P.sha(prior),commit='fdc46b6eba1cf92e283290d1737fd55f945157d0',manifest_sha256=P.sha(manifest),all152_members_verified=True,independent_acceptance=False),
  established=['All31 authored bts field selectors differ from212. Under the actual manager0 namespace5/base3*field call boundary they do not enter330310 special cached-buffer selector212 branch.',
  'With no kind5 runtime size override and unchanged retained FST, all31 primary sizes are-1. Original32E400 preserves this nonpositive fallback value. Original330310 TEST EDI/JLE skips its primary allocation36A100, primary pointer publication, cached memcpy/callback and primary request32E620.',
  'The loader ORs manager flags20000 BEFORE the signed positive-size guard. Reaching that local OR does not prove primary allocation, read acceptance or executed callback. Persistence of the bit under other calls/concurrency is not proved.',
  'The nonpositive suffix still may call5C5230 and staged sibling32EB40(base+2) for manager0. The original payload pointer is not locally overwritten on this suffix; prior state, teardown and later/pending callbacks remain separate. This is no new primary admission, not no global requests/effects.',
  'The alternate3306E0 route is not covered. Canonical32E3F0 is already a diagnostic-return stub; its existence is not proof that it filled a filename buffer or that the alternate path is naturally selected.'],
  limitations=['Normal original byte/ABI and unchanged FST/null-override premises, not actual initialization or natural reachability','No full stale/pending payload lifetime, alias/embedded script census, sibling terminal effect or alternate3306E0 execution','No whole GR18/OV/AQ closure, independent SPEC and canonical incorporation remain pending','No new native/emulated/live original-code executions or historical census reruns'],
  affected_claims=['FABLE/OPUS GR18 bts indexed-primary admission boundary and attempted flag versus actual payload','Actual normal reachability must additionally establish override/alternate-loader selection and owner lifecycle'],
  next_discriminator='Use existing option5/size-override initialization/writer evidence before any real-process observation; only actual unresolved selection/lifetime needs can justify C.',
  required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in ['capture-bts-primary-admission.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','index-path-raw-02.json','bts-primary-admission-capture-01.status.json','bts-primary-admission-capture-01.stdout','bts-primary-admission-capture-01.stderr']],
  checker_sha256=P.sha(pathlib.Path(__file__)),native_runs=0,live_runs=0,cleanup='Only finite shipping source/data reads; no PC/game/native/save/config/reference/peer change')
 out.open('x').write(json.dumps(result,indent=2)+'\n');print('Conditional bts indexed-primary admission refused; attempted flag and sibling/alternate paths remain distinct')
if __name__=='__main__':main()
