"""Exact first-switch mapping and local status-argument bound, Method A.

Fresh source-directory, capture-status and result. No runtime sampling.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ix,p,m,a):
 if p not in ix or (ix[p]['mnemonic'],ix[p]['args'])!=(m,a):raise ValueError('original operation mismatch '+hex(p))
def main():
 source,status,out=map(pathlib.Path,sys.argv[1:])
 if out.exists():raise ValueError('immutable result exists')
 p=source/'ov58d-order-switch-source-02.json';st=json.loads(status.read_text());v=json.loads(p.read_text())
 if st.get('exit')!=0 or st.get('terminal') is not True or st.get('source_sha256')!=sha(p) or st.get('driver_sha256')!=sha(source/'capture-ov58d-order-switch.py'):
  raise ValueError('failed/missing capture prerequisite')
 if v.get('exe_sha256')!=SHA or v.get('image_base')!='0x120000' or v.get('wrapper_complete') is not True or v.get('invocation_driver_sha256')!=st['driver_sha256']:
  raise ValueError('original source provenance incomplete')
 if [(c['bytes'],c['expected'],c['observed']) for c in v['controls']]!=[('0f1101','w','w'),('488d4104','addr','addr'),('f00fb101','rw','rw')]:raise ValueError('failed capture roles')
 s=importlib.util.spec_from_file_location('reviewed_switch_roles',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S);annotations=S.validate(v)
 spans=[(q['start'],q['end_exclusive']) for q in v['ranges']]
 if spans!=[('0x2fdda0','0x2fe534'),('0x305080','0x30510f'),('0x30e360','0x30e395'),('0x30e588','0x30e5b7')]:raise ValueError('missing normal/source ranges')
 ix={int(i['pc'],16):i for q in v['ranges'] for i in q['instructions']};tables={int(t['address'],16):t for t in v['tables']}
 if set(tables)!={0x2fe534,0x2fe54c,0x2fe598,0x1eec6a8}:raise ValueError('missing/different original tables')
 # The retained capture's checked status is required, but a self-consistent
 # synthetic record must not masquerade as shipping bytes. Check this path too.
 root=next(p0 for p0 in W.parents if (p0/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
 image=(root/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(image).hexdigest()!=SHA:raise ValueError('reference image changed')
 pe=struct.unpack_from('<I',image,60)[0];opt=pe+24
 sections=[struct.unpack_from('<IIII',image,opt+struct.unpack_from('<H',image,pe+20)[0]+40*k+8) for k in range(struct.unpack_from('<H',image,pe+6)[0])]
 def original(pc,n):
  for _,va,rs,ro in sections:
   if 0x120000+va<=pc and pc+n<=0x120000+va+rs:return image[ro+pc-0x120000-va:ro+pc-0x120000-va+n]
  raise ValueError('unbacked original span')
 for q in v['ranges']:
  blob=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))
  if blob!=original(int(q['start'],16),len(blob)):raise ValueError('code differs from shipping reference')
 for t in tables.values():
  if hashlib.sha256(bytes.fromhex(t['bytes'])).hexdigest()!=t['sha256']:raise ValueError('mixed table bytes')
  if bytes.fromhex(t['bytes'])!=original(int(t['address'],16),len(bytes.fromhex(t['bytes']))):raise ValueError('table differs from shipping reference')
 first=bytes.fromhex(tables[0x2fe534]['bytes']);selectors=bytes.fromhex(tables[0x2fe54c]['bytes']);tail=bytes.fromhex(tables[0x2fe598]['bytes'])
 if len(first)!=24 or len(selectors)!=76 or len(tail)!=0xc0:raise ValueError('table extent incomplete')
 targets=[0x120000+x for x in struct.unpack('<6I',first)]
 if targets!=[0x2fde39,0x2fde7b,0x2fde98,0x2fdf18,0x2fdf5a,0x2fdec1]:raise ValueError('first arm identities changed')
 if max(selectors)>=len(targets):raise ValueError('selector outside physical slots')
 expected=[
 (0x2fdda6,'mov','rax, qword ptr [rcx + 0x708]'),(0x2fddad,'mov','rbx, rcx'),(0x2fddb0,'movzx','edx, word ptr [rcx + 0x714]'),
 (0x2fddb7,'cmp','byte ptr [rbx + 0x6b4], 0'),(0x2fddc2,'je','0x2fddcf'),(0x2fddce,'ret',''),
 (0x2fddcf,'movzx','r8d, dx'),(0x2fddd8,'mov','eax, r8d'),(0x2fdddb,'cmp','r8d, 0x4158'),(0x2fdde2,'ja','0x2fe17f'),(0x2fdde8,'je','0x2fe12b'),
 (0x2fddee,'cmp','r8d, 0x40d1'),(0x2fddf5,'ja','0x2fdfc8'),(0x2fddfb,'cmp','r8d, 0x4092'),(0x2fde02,'jae','0x2fdf93'),
 (0x2fde08,'mov','r8d, 0x4046'),(0x2fde0e,'sub','eax, r8d'),(0x2fde11,'cmp','eax, 0x4b'),(0x2fde14,'ja','0x2fe523'),
 (0x2fde1a,'lea','r9, [rip - 0x1dde21]'),(0x2fde21,'cdqe',''),(0x2fde23,'movzx','eax, byte ptr [r9 + rax + 0x1de54c]'),
 (0x2fde2c,'mov','ecx, dword ptr [r9 + rax*4 + 0x1de534]'),(0x2fde34,'add','rcx, r9'),(0x2fde37,'jmp','rcx'),
 (0x2fde80,'sub','dl, 0x48'),(0x2fde83,'mov','byte ptr [rbx + 0x54], dl'),(0x2fde86,'mov','eax, 1'),(0x2fde8b,'mov','byte ptr [rbx + 0x6b4], 2'),(0x2fde97,'ret',''),
 (0x2fdf18,'mov','rcx, qword ptr [rbx + 0x698]'),(0x2fdf1f,'lea','r8d, [rdx - 0x51]'),(0x2fdf31,'mov','rdx, rcx'),(0x2fdf40,'call','0x30e360'),(0x2fdf59,'ret',''),
 (0x2fdf5a,'mov','rcx, qword ptr [rbx + 0x698]'),(0x2fdf61,'lea','r8d, [rdx - 0x71]'),(0x2fdf6e,'mov','rdx, rcx'),(0x2fdf79,'call','0x30e360'),(0x2fdf92,'ret',''),
 (0x305094,'movzx','edi, word ptr [rcx + 0x714]'),(0x3050d0,'movzx','eax, di'),(0x3050d3,'add','eax, 0xffffc000'),(0x3050e8,'mov','rdx, qword ptr [rdx + rax*8]'),(0x3050fe,'jmp','rdx'),
 (0x30e38c,'mov','byte ptr [rsp + 0x40], r8b'),(0x30e391,'movzx','edi, r8b'),(0x30e588,'movzx','edx, byte ptr [rsp + 0x40]'),(0x30e594,'mov','dword ptr [rsi + rdx*4 + 0xbc], ecx'),
 (0x30e5a7,'movzx','edx, byte ptr [rsp + 0x40]'),(0x30e5ac,'movzx','ecx, dl'),(0x30e5af,'mov','word ptr [rsi + rcx*2 + 0x13c], ax')]
 for p0,m,a in expected:need(ix,p0,m,a)
 if ix[0x2fde1a]['memory'][0]['rip_target']!='0x120000' or ix[0x2fde1a]['memory'][0]['role']!='addr' or ix[0x2fde83]['memory'][0]['role']!='w':raise ValueError('actual address/store role mismatch')
 if struct.unpack('<QQ',bytes.fromhex(tables[0x1eec6a8]['bytes']))!=(0x2fdda0,0x2fdda0):raise ValueError('outer4049/404A handler identity changed')
 # Include the other two physical indirect target sets to check all local incoming
 # edges to the two named status arms, without treating every byte as code.
 other=[0x120000+x for x in struct.unpack_from('<6I',tail,0)]
 last=[0x120000+x for x in struct.unpack_from('<12I',tail,0x90)]
 if any(p0 not in ix or not 0x2fdda0<=p0<0x2fe534 for p0 in other+last):raise ValueError('remaining indirect target outside normal code')
 if {0x2fdf18,0x2fdf5a}&set(other+last):raise ValueError('other switch reaches status arm')
 if any(i['args'] in {'0x2fdf18','0x2fdf5a'} for i in ix.values() if i['mnemonic'].startswith('j')):raise ValueError('unaccounted direct status-arm predecessor')
 mapping=[{'message':hex(0x4046+k),'selector':s0,'target':hex(targets[s0])} for k,s0 in enumerate(selectors)]
 domains={hex(a):[0x4046+k for k,s0 in enumerate(selectors) if targets[s0]==a] for a in [0x2fdf18,0x2fdf5a]}
 if domains!={'0x2fdf18':list(range(0x4051,0x4071)),'0x2fdf5a':list(range(0x4071,0x4091))}:raise ValueError('status arm domain changed')
 # A path through root/first-switch to either status arm contains no CALL or
 # EDX/RDX/DX/DL write after initial WORD load. Native RDX is changed only after LEA.
 for a,b in [(0x2fddb7,0x2fde39),(0x2fdf18,0x2fdf31),(0x2fdf5a,0x2fdf6e)]:
  seq=[i for p0,i in ix.items() if a<=p0<b]
  if any(i['mnemonic']=='call' or (i['args'].split(',')[0] in {'rdx','edx','dx','dl'} and i['mnemonic'] not in {'cmp','test','push'}) for i in seq):raise ValueError('message register changes before status ID')
 arm=[i for p0,i in ix.items() if 0x2fde7b<=p0<0x2fde98]
 if any(i['mnemonic'].startswith('j') or i['mnemonic']=='call' for i in arm) or arm[-1]['mnemonic']!='ret':raise ValueError('4049 local-return arm not closed')
 calls=[hex(p0) for p0,i in ix.items() if 0x2fdda0<=p0<0x2fe534 and i['mnemonic']=='call' and i['args']=='0x30e360']
 if calls!=['0x2fdf40','0x2fdf79']:raise ValueError('named handler status calls changed')
 ids={a:[((msg-(0x51 if a=='0x2fdf18' else 0x71))&0xffffffff)&0xff for msg in msgs] for a,msgs in domains.items()}
 if any(v0!=list(range(32)) for v0 in ids.values()):raise ValueError('byte status bound failed')
 # Algebraic extents under the existing state-record premise, not live addresses.
 offsets=[{'record':k,'last_dword_start':hex(8+0x1c8*k+0xbc+4*31),'last_dword_end':hex(8+0x1c8*k+0xbc+4*31+4),'last_word_start':hex(8+0x1c8*k+0x13c+2*31),'last_word_end':hex(8+0x1c8*k+0x13c+2*31+2)} for k in [38,39]]
 if any(int(r['last_dword_end'],16)>0x4748 or int(r['last_word_end'],16)>0x4748 for r in offsets):raise ValueError('bounded sites still reach region A')
 r={'status':'PRODUCER_CHECKED_STATIC_REFUTATION_INDEPENDENT_PENDING','method':'A original code and exact finite switch data','producer_complete':True,'question':'Do normal4049/404A order handlers reach the two named high-index status calls?','answer':'REFUTED. Both map to2FDE7B, change unit54 to1/2 then locally return1; no direct CALL. Actual status messages4051..4070 and4071..4090 supply lowR8B0..31, notF8/D9.','exe_sha256':SHA,'source_sha256':sha(source/'ov58d-order-switch-source-02.json'),'capture_status_sha256':sha(status),'capture_driver_sha256':st['driver_sha256'],'checker_sha256':sha(pathlib.Path(__file__)),'annotations':annotations,'first_switch_mapping':mapping,'status_arm_domains':{a:[hex(msg) for msg in msgs] for a,msgs in domains.items()},'native_byte_arguments':ids,'conditional_record_extents':offsets,'controls_basis':'Actual table maps4049/404A toselector1 and positive4051/4070/4071/4090 tostatusarms. Complete76 table entries enumerated, not76 native executions.','affected_claims':['SWE2-STRUCT caller-cone high-ID two-site assertion and queued Esper runtime premise','FABLE T3b region-A named reach limit','OPUS status/aux byte caller contract for these two sites'],'limits':['Normal original handler entry, unchanged valid shipping code/table, valid unit+708/backed memory and usualABI required','Handler+6B4!=0 returns before switch; no natural observation or initialized unit/Esper ownership claim','A local arm store is not a player-visible effect or proof of other callback/transitive effects','Status argument bound at these two calls; generic0030E360 remains unmasked and accepts higher byte args from other hypothetical callers','Record k<=39 and retained spilled argument/no-interference are premises for extent calculation; no whole-state/alias/lifetime safety','Other caller-cone bounds are external prior evidence, not a new complete caller census','No whole OV58/OV5/8 closure before independent review and named consumer incorporation'],'native_runs':0,'live_runs':0,'formerly_runtime_propositions_eliminated_without_gameplay':1,'new_whole_runtime_rows_closed':0,'next_discriminator':'Consumers must remove these two false high-ID premises; if another source remains, name its exact original caller/argument provenance before any runtime capture'}
 out.write_text(json.dumps(r,indent=2)+'\n');print('REFUTED queued4049/404A high-index route; actual two status-arm domains bound lowR8B0..31; one live premise eliminated statically')
if __name__=='__main__':main()
