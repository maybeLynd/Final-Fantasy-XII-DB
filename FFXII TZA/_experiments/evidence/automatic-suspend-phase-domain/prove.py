"""Finite original copy-address proof. No machine-code execution or gameplay."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
for f,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
 if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py')
status=json.loads((P/'capture-01.status.json').read_text())
if status.get('terminal') is not True or status.get('exit')!=0 or status.get('exception') is not None or status['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required capture status failed')
x=json.loads((P/'source-01.json').read_text())
if x.get('wrapper_complete') is not True or x.get('driver_sha256')!=sha(P/'capture-index-path.py') or x.get('invocation_driver_sha256')!=sha(P/'capture.py'):raise RuntimeError('actual capture incomplete')
roles=V.validate(x)
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(raw).hexdigest()!=PIN or x['exe_sha256']!=PIN:raise RuntimeError('original image changed')
pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,sz,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise RuntimeError('unbacked source')
required_ranges=[('0x30eda0','0x30ee9a'),('0x30eff0','0x30f121'),('0x30dfa0','0x30e010')]
if[(r['start'],r['end_exclusive']) for r in x['ranges']]!=required_ranges:raise RuntimeError('required source population changed')
ix={};graphs=[]
for r in x['ranges']:
 a,b=int(r['start'],16),int(r['end_exclusive'],16)
 if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
 local={int(i['pc'],16):i for i in r['instructions']};ix.update(local)
 g=G.graph(local,a,b)
 if set(local)!=g['visited']:raise RuntimeError('unaccounted source instructions')
 graphs.append({'entry':hex(a),'visited':len(g['visited']),'returns':[hex(t) for t in g['returns']],'calls':g['calls']})
req=[(0x30effa,'mov','eax, dword ptr [rcx]'),(0x30efff,'bt','rax, 0x18'),
 (0x30f004,'jb','0x30f114'),(0x30f00a,'mov','eax, 0x21e'),
 (0x30f00f,'cmp','word ptr [rcx + 0x714], ax'),(0x30f016,'ja','0x30f025'),
 (0x30f018,'cmp','byte ptr [rcx + 0x6b4], 6'),(0x30f01f,'jae','0x30f114'),
 (0x30f02a,'call','0x30dfa0'),(0x30f032,'test','rax, rax'),
 (0x30f035,'jne','0x30f047'),(0x30f0ec,'call','0x861ec0'),
 (0x30f0f1,'mov','qword ptr [rbx + 0xb88], rdi'),
 (0x30f0f8,'mov','eax, 1'),(0x30f114,'xor','eax, eax'),(0x30f120,'ret','')]
for pc,m,a in req:
 if (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('required guard changed '+hex(pc))
mp=P/'parent-manifest.json'
if sha(mp)!='625d19648d361068d2a60fb8e5abeb7928e20411223564051242b6200ebd78a7':raise RuntimeError('parent manifest changed')
lineage=json.loads((P/'lineage.json').read_text());parent=json.loads(mp.read_text())
if lineage['parent_commit']!='d7500f9f91183c3f48f749d345fb8a35bdb16644' or lineage['capture_reexecuted'] is not False:raise RuntimeError('retained provenance changed')
for m in lineage['reused_members']:
 if m not in parent['members'] or sha(P/m['path'])!=m['sha256']:raise RuntimeError('retained member changed')
local={pc:i for pc,i in ix.items() if 0x30eff0<=pc<0x30f121}
parts=[]
# Complete categorical partition of bit24 x unsigned-id band x unsigned-byte
# phase band. Values within one category take the same original guard edges.
for flag in [False,True]:
 for ordinary in [False,True]:
  for late in [False,True]:
   eligible=not flag and(not ordinary or not late)
   fixed={0x30f004:flag,0x30f016:not ordinary,0x30f01f:late}
   g=G.graph(local,0x30eff0,0x30f121,fixed=fixed)
   calls=[(pc,t) for pc,t in g['calls']]
   allocator=any(t=='0x30dfa0' for pc,t in calls)
   if allocator!=eligible:raise RuntimeError('guard allocation domain differs')
   if not eligible:
    if calls or g['returns']!=[0x30f120] or 0x30f114 not in g['visited']:raise RuntimeError('refusal path not closed')
    writes=[(hex(pc),m) for pc in g['visited'] for m in ix[pc]['memory'] if 'w' in m['role'] and m['base']!='rsp']
    if writes:raise RuntimeError('refusal modifies nonstack memory')
   elif 0x30f035 not in g['visited'] or 0x30f0f1 not in g['visited']:
    raise RuntimeError('eligible allocation outcome boundaries missing')
   parts.append({'flag24':flag,'current_u16_le542':ordinary,'phase_u8_ge6':late,
                 'allocator_attempt_reachable':allocator,'input_refusal_returns_zero':not eligible,
                 'eligible_does_not_guarantee_allocator_success':eligible,
                 'visited':len(g['visited']),'calls':[{'pc':hex(pc),'target':t} for pc,t in calls]})
if len(parts)!=8 or sum(p['allocator_attempt_reachable'] for p in parts)!=3:raise RuntimeError('incomplete partition')
result={'producer_complete':True,'method':'A retained STATIC_ONLY original guard-domain proof',
 'driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'source-01.json','sha256':sha(P/'source-01.json')}],
 'annotation_prerequisites':[roles],'parent_manifest_sha256':sha(mp),'capture_reexecuted':False,
 'instruction_assertions':len(req),'partitions':parts,
 'allocator_attempt_domain':'!flag24 && (current_u16 > 542 || phase_u8 < 6)',
 'refusal_domain':'flag24 || (current_u16 <= 542 && phase_u8 >= 6)',
 'answer':'A same-unit ordinary current action at phase6..255 cannot enter this snapshot/automatic-commit success leg under stable entry state. This excludes that particular post-queue interruption explanation, not all queued/current/global-kind mismatch.',
 'countermodel_limits':'Globalkind262 does not imply thisunit current262. Other units, different writers/callers, copied/restored state and prephase6 transitions remain independent. Do not transform conditional sameunit exclusion into a universal identity/lifetime invariant.',
 'boundaries':{'ordinary_ids':'0..542 inclusive','outside_ordinary_ids':'543..65535 inclusive','early_phases':'0..5','late_phases':'6..255'},
 'limitations':['No native/emulated/live execution; eight categorical CFG partitions are mathematical path accounting',
  'Retained d750 original capture reused, not credited as another capture; no independent acceptance inferred',
  'Helper input reads and branch effects assume valid same-unit private state/noninterference; caller already cleared retaliation target28 before this helper, so helper refusal does not imply whole caller side-effect freedom',
  'Eligibility only reaches allocator; empty8slot pool may still returnNULL and refuse; normal copy/memset return additionally required for success',
  'No whole OV21/OV42, allcallers, initialized reachability, ownership or scheduler closure']}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json');out=out if out.is_absolute() else P/out
if out.exists():raise RuntimeError('immutable output exists')
out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED ordinary phase>=6 snapshot refusal; eligible allocation can still fail; no recapture/native/game')
