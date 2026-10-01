"""Original recursive loop supplies fresh bit indices0..31 under normalABI."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 src,stp,out=map(pathlib.Path,sys.argv[1:])
 if out.exists():raise ValueError('immutable result exists')
 p=src/'status-recursion-index-bound-source-01.json';v=json.loads(p.read_text());st=json.loads(stp.read_text())
 if st.get('terminal') is not True or st.get('exit')!=0 or st.get('source_sha256')!=sha(p) or st.get('driver_sha256')!=sha(src/'capture-status-recursion-index-bound.py'):raise ValueError('capture prerequisite failed or missing')
 if v.get('exe_sha256')!=SHA or v.get('invocation_driver_sha256')!=st['driver_sha256']:raise ValueError('source identity mismatch')
 if [(c['bytes'],c['expected'],c['observed']) for c in v['controls']]!=[('0f1101','w','w'),('488d4104','addr','addr'),('f00fb101','rw','rw')]:raise ValueError('capture role controls failed')
 s=importlib.util.spec_from_file_location('recursive_reviewed_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S);annotations=S.validate(v)
 root=next(p0 for p0 in W.parents if (p0/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());image=(root/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(image).hexdigest()!=SHA:raise ValueError('reference image changed')
 pe=struct.unpack_from('<I',image,60)[0];opt=pe+24;secs=[struct.unpack_from('<IIII',image,opt+struct.unpack_from('<H',image,pe+20)[0]+40*k+8) for k in range(struct.unpack_from('<H',image,pe+6)[0])]
 if [(q['start'],q['end_exclusive']) for q in v['ranges']]!=[('0x30e360','0x30e395'),('0x30e645','0x30e6e7')]:raise ValueError('missing/different loop source')
 for q in v['ranges']:
  a=int(q['start'],16);b=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']));matches=[image[ro+a-0x120000-va:ro+a-0x120000-va+len(b)] for _,va,rs,ro in secs if 0x120000+va<=a and a+len(b)<=0x120000+va+rs]
  if matches!=[b]:raise ValueError('loop bytes differ from shipping reference')
 ix={int(i['pc'],16):i for q in v['ranges'] for i in q['instructions']}
 expect={0x30e38c:('mov','byte ptr [rsp + 0x40], r8b'),0x30e391:('movzx','edi, r8b'),
 0x30e682:('xor','edx, edx'),0x30e684:('jmp','0x30e68a'),0x30e686:('xor','edx, edx'),0x30e688:('mov','ecx, edx'),
 0x30e68a:('mov','eax, dword ptr [rcx + 0xc]'),0x30e68d:('mov','dword ptr [rsp + 0x4c], eax'),0x30e691:('test','eax, eax'),0x30e693:('je','0x30e6e7'),
 0x30e695:('mov','rbp, qword ptr [rsp + 0x50]'),0x30e69a:('mov','edi, edx'),0x30e69c:('mov','ebx, dword ptr [rsp + 0x228]'),
 0x30e6a3:('bt','eax, edi'),0x30e6a6:('jae','0x30e6d2'),0x30e6b9:('movzx','r8d, dil'),0x30e6c7:('call','0x30e360'),
 0x30e6cc:('mov','eax, dword ptr [rsp + 0x4c]'),0x30e6d0:('xor','edx, edx'),0x30e6d2:('inc','edi'),0x30e6d4:('cmp','edi, 0x20'),0x30e6d7:('jl','0x30e6a3')}
 for pc,pair in expect.items():
  if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args'])!=pair:raise ValueError('loop operation mismatch '+hex(pc))
 body=[i for pc,i in ix.items() if 0x30e69a<=pc<0x30e6d9]
 counter_writes=[i['pc'] for i in body if i['args'].split(',')[0] in {'edi','rdi','di','dil'} and i['mnemonic'] not in {'cmp','test','bt','push'}]
 if counter_writes!=['0x30e69a','0x30e6d2']:raise ValueError('unaccounted counter write')
 if [i['pc'] for i in body if i['mnemonic']=='call']!=['0x30e6c7']:raise ValueError('loop call boundary changed')
 indices=list(range(32));states=[{'before':n,'argument':n&255,'after':(n+1)&0xffffffff,'continues':n+1<32} for n in indices]
 if states[-1]['continues'] or any(n['argument']!=n['before'] for n in states):raise ValueError('bounded counter proof failed')
 r={'status':'PRODUCER_CHECKED_BOUNDED_LOOP_INDEPENDENT_PENDING','method':'A original source + induction/bounded arithmetic','question':'Does0030E6C7 inherit incoming outerR8B?','answer':'No. Reached initialization resetsEDI fromEDX0; the32-bit mask loop supplies fresh bit index0..31. Bound independent of outerR8B; branch/resource validity and ordinarycalleeABI remain premises.','exe_sha256':SHA,'source_sha256':sha(p),'capture_status_sha256':sha(stp),'checker_sha256':sha(pathlib.Path(__file__)),'annotations':annotations,'counter_local_writes':counter_writes,'bounded_arithmetic_states':states,'inheritance_counterexample':{'outer_byte':31,'selected_metadata_mask':'0x10','recursive_argument':4,'limits':'Conditional loop-entry/mask witness, not a natural initialized resource or original-code execution'},'affected_claims':['SWE2-STRUCT caller cone0030E6C7 line: inheritedouterbyte -> bounded maskbit loop','FABLE/OPUS compositional region-A status argument bounds'],'limitations':['Local path through30E682/686, validrow atRCX and nonzero32-bit mask required for recursion','Normal ABI preserves nonvolatileEDI across0030E360 and backing callerframe/metadata stable as required; noexception or arbitrarymemory interference guarantee','Not a complete fullfunction/caller census or proof that outerarbitrarybyte/state is safe','No nativecallback effect, natural branch/resource binding/scheduling/lifetime or playerpresentation proof','32 enumeration states are arithmetic proof controls, not32 original-code executions'],'native_runs':0,'live_runs':0,'new_whole_runtime_rows_closed':0,'cleanup':'Finite read-only source analysis; noPC/game/nativeinstrument/save/config/reference/peerprocesswrites'}
 out.write_text(json.dumps(r,indent=2)+'\n');print('Original recursivecall uses fresh0..31 maskbit index, not inheritedouter byte; initialization/ABI premises retained')
if __name__=='__main__':main()
