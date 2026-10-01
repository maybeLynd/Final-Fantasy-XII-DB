"""Read retained original metadata; no bytecode or native execution."""
import hashlib,json,shutil,struct,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();u=lambda b,o:struct.unpack_from('<I',b,o)[0]
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SN1-ASSIGNMENT-ATTRIBUTION-BOUNDARY');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
P=Path('Database/FFXII TZA/_experiments/evidence/sn1-variable-name-binding');pub=Path('Database/Tools/work/ASTRA/sn1-variable-name-binding/publication')
commit=None;receipt=None
if (pub/'commit.txt').exists():
 commit=(pub/'commit.txt').read_text().strip();receipt=json.loads((pub/'verification.json').read_text());assert receipt['commit']==commit and receipt['manifest_members_verified']==47 and receipt['exact_owned_blobs_and_body']
parent_status='EXACT_PUBLICATION_VERIFIED' if receipt else 'FROZEN_ORIGINAL_INPUTS_PUBLICATION_PENDING; no automatic acceptance'
assert not R.exists();R.mkdir();manifest=json.loads((P/'manifest.json').read_text());ident=[]
for n in ['evctrl.dbg','evctrl.ebp','evctrl.sbn','selected-sbn-functions.py','parent61-raw.json']:
 b=(P/'retained'/n).read_bytes();m=next(x for x in manifest['members'] if x['path']=='retained/'+n);assert sha(b)==m['sha256'] and len(b)==m['bytes'];(R/n).write_bytes(b);ident.append(dict(path='retained/'+n,sha256=sha(b),bytes=len(b)))
(R/'parent65-result.json').write_bytes((P/'result.json').read_bytes());(R/'parent65-manifest.json').write_bytes((P/'manifest.json').read_bytes())
if receipt:(R/'parent65-publication.json').write_bytes((pub/'verification.json').read_bytes())
cp=Path('Database/FFXII TZA/_index/candidates/sn1-layouts/sn1_logical_lines.py');qp=cp.with_name('sn1_q0_domain.py');(R/'opus-logical-primary-before.py').write_bytes(cp.read_bytes());(R/'opus-lookup-primary-before.py').write_bytes(qp.read_bytes())
b=(R/'evctrl.dbg').read_bytes();e=(R/'evctrl.ebp').read_bytes();parent=json.loads((R/'parent61-raw.json').read_text());cases=[]
for scope,pc,value in [(1,5394,1),(1,5598,0),(5,1278,99),(9,582,99)]:
 bind=next(x for x in parent['bindings'] if x['module']=='evctrl' and x['scope']==scope);a=bind['code_start']+pc-3;qo=bind['q0']+4*(pc-3);line,block,flag=struct.unpack_from('<HBB',b,qo)
 cases.append(dict(scope=scope,push_pc=pc-3,pop_pc=pc,code_offset=a,code_hex=e[a:a+6].hex(),q0_offset=qo,q0_hex=b[qo:qo+24].hex(),tagged_line=line,block=block,value=value,operand=0x61))
raw=dict(method='A verified immutable65 original data; no bytecode/VM/native/guest/live execution',question='Does the tagged logical group contain the assignment to the exact original variable, or point to a following different statement/boundary?',reference=dict(parent_commit=commit,parent_status=parent_status,parent_manifest_sha256=sha((P/'manifest.json').read_bytes()),files=ident,exe_identity_from65=json.loads((P/'raw.json').read_text())['reference']['exe_sha256']),tools=dict(python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),codec_tool_identity_sha256=sha((P/'codec-tool-identity.json').read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),cases=cases,limits='Four new original PUSHII/POPV pairs;63 single example already known and not replayed. Source-coordinate addressability is distinct from statement attribution; original compiler rule, effects/reachability/ev shared-tail unproved. PC OFF/S19 unchanged/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE66 four prepared original assignment boundaries',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
