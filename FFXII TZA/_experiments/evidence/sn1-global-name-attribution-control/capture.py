"""A independent retained original descriptor/name pairs and actual predicate."""
import ast,hashlib,json,re,struct,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();u=lambda b,o:struct.unpack_from('<I',b,o)[0]
if (W/'raw.json').exists():subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SN1-GLOBAL-NAME-ATTRIBUTION-CONTROL');assert t['agent']=='ASTRA' and t['status']=='ACTIVE';assert not R.exists();R.mkdir()
P=Path('Database/FFXII TZA/_experiments/evidence/sn1-variable-name-binding');M=json.loads((P/'manifest.json').read_text());ident=[]
for n in ['evctrl.dbg','evctrl.ebp','evctrl.sbn','selected-sbn-functions.py','parent61-raw.json','resolver591.bin']:
 b=(P/'retained'/n).read_bytes();m=next(x for x in M['members'] if x['path']=='retained/'+n);assert sha(b)==m['sha256'] and len(b)==m['bytes'];assert subprocess.check_output(['git','show','ec5e54a990122f7a071cc1d2c811dfd2271e96b3:'+P.as_posix()+'/retained/'+n])==b;(R/n).write_bytes(b);ident.append(dict(path='retained/'+n,sha256=sha(b),bytes=len(b)))
(R/'parent65-publication-correction.json').write_bytes((P/'publication-correction/material-publication.json').read_bytes())
primary=Path('Database/FFXII TZA/_index/candidates/sn1-layouts/sn1_variable_binding.py');src=primary.read_bytes();(R/'opus-variable-binding-primary.py').write_bytes(src);commit=subprocess.check_output(['git','log','-1','--format=%H','--',primary.as_posix()],text=True).strip();assert subprocess.check_output(['git','show',commit+':'+primary.as_posix()])==src
fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='on');(R/'selected-opus-on.py').write_text(ast.unparse(fn)+'\n')
b=(R/'evctrl.dbg').read_bytes();e=(R/'evctrl.ebp').read_bytes();pool=u(b,8);T0=u(b,4);T2=u(b,20);N=u(b,T0);sect=u(e,16);vt=sect+u(e,sect+40)
def name(p):
 a=pool+p;assert b[a-1]==0;z=b.index(b'\0',a);return dict(pool_position=p,offset=a,hex=b[a:z].hex(),text=b[a:z].decode('cp932'))
names=[name(u(b,T0+4+4*i)) for i in range(N)];t2=[]
for j in range(u(b,T2)):
 d,p=struct.unpack_from('<II',b,T2+4+8*j);t2.append(dict(index=j,record_offset=T2+4+8*j,record_hex=b[T2+4+8*j:T2+12+8*j].hex(),descriptor=f'{d:08x}',name=name(p)))
rows=[]
for i in range(1,0x3f):
 a=vt+4+8*i;d=u(e,a);rows.append(dict(index=i,native_record_offset=a,native_record_hex=e[a:a+8].hex(),descriptor=f'{d:08x}',t0_field_offset=T0+4+4*i,t0_field_hex=b[T0+4+4*i:T0+8+4*i].hex(),t0_name=names[i],next_t0_name=names[i+1],t2_matches=[r for r in t2 if r['descriptor']==f'{d:08x}']))
parent=json.loads((R/'parent61-raw.json').read_text());bind=next(x for x in parent['bindings'] if x['module']=='evctrl' and x['scope']==1);cs=e[bind['code_start']:bind['code_start']+bind['validated_code_bytes']];pc=0;first=None
while pc<len(cs):
 op=cs[pc];n=1 if op<0x48 else 3
 if op==0x49 and struct.unpack_from('<H',cs,pc+1)[0]==1:first=dict(scope=1,pc=pc,code_offset=bind['code_start']+pc,code_hex=cs[pc:pc+3].hex(),q0_offset=bind['q0']+4*pc,q0_hex=b[bind['q0']+4*pc:bind['q0']+4*pc+4].hex());break
 pc+=n
assert first is not None
raw=dict(method='A exact original retained metadata/native-descriptor identity and unchanged published OPUS on() predicate selection; no original compiler/VM/native/guest/live execution',reference=dict(original_material_commit='ec5e54a990122f7a071cc1d2c811dfd2271e96b3',publication_correction_commit='b94b449ac08ffecde9c9045f984ab6f64c0b8db7',files=ident,original65_strict_manifest_valid=False,selected_original_files_committed_verified=True,primary_path=primary.as_posix(),primary_commit=commit,primary_sha256=sha(src),predicate_ast_sha256=sha(ast.dump(fn,include_attributes=True).encode())),tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),rows=rows,first_store=first,limits='62 selected original global descriptor/name identities plus first source-attribution discriminator; no universal115 ordering/allscopes/type meanings/native values/lifetime/reachability. OPUS59/0 source counts are its corroboration, not tests rerun here. PC OFF/S19/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE68 independent original T2/T0/native descriptor identities and first source marker',flush=True);subprocess.run([sys.executable,str(W/'check.py')],check=True)
