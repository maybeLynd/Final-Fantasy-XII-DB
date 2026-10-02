"""Exercise the actual collector main with explicitly fake input services."""
import hashlib,json,runpy,struct,sys,types
from pathlib import Path
q=Path(sys.argv[1]).resolve();cfg=json.loads((q/'case.json').read_text())
driver=q/'Database/Tools/analysis-kit/gfz-scripts/script_verb_census.py'
if hashlib.sha256(driver.read_bytes()).hexdigest()!=cfg['collector_sha256']:raise RuntimeError('original collector bytes changed')
attempted=[];failed=[];returned=[]
def blob(verb,name):
 # Synthetic section exercises the real collector's basic container/directory/name
 # checks. Fake decode returns one CALL; this is not a decoder correctness test.
 b=bytearray(0x80+0xe0);sec=memoryview(b)[0x80:]
 struct.pack_into('<II',sec,0,0x8000000b,0xe0);struct.pack_into('<I',sec,0x18,0xa0)
 struct.pack_into('<I',sec,0x4c,0x70);struct.pack_into('<I',sec,0xa0,1)
 struct.pack_into('<I',sec,0xa4,0);struct.pack_into('<I',sec,0xac,0x60)
 sec[0x60:0x63]=bytes([0x58,verb&255,verb>>8]);s=name.encode();sec[0x70:0x70+len(s)]=s;return bytes(b)
inputs={'fixture/a.ebp':blob(0x29a,'fixture_first'),'fixture/b.ebp':blob(0x29b,'fixture_second')}
def read_entry(f,names,blocks,path):
 attempted.append(path)
 if cfg['fail_mode']=='all' or (cfg['fail_mode']=='second' and path=='fixture/b.ebp'):failed.append(path);raise OSError('LABELLED synthetic extraction failure')
 returned.append(path);return inputs[path]
G=types.ModuleType('gen_req_channel_census')
G.VBF=str(q/'fixture-archive.bin');G.V=types.SimpleNamespace(load_index=lambda f:(dict.fromkeys(inputs),[]),read_entry=read_entry)
G.load_verbs=lambda:{0x29a:(2,None,'getspattackskillinfo'),0x29b:(2,None,'spattackread')}
G.decode=lambda code:([(0,0x58,int.from_bytes(code[1:3],'little'))],None)
G.resolve_args=lambda ins,j,need,verbs:([('synthetic-reference',1),('synthetic-reference',2)],'ok')
G.OPN={0x58:'CALL'};sys.modules['gen_req_channel_census']=G
sys.argv=[str(driver),'--verbs','0x29A,0x29B','--out',str(q/'calls.tsv')]
try:
 runpy.run_path(str(driver),run_name='__main__')
finally:
 (q/'fixture-effects.json').write_text(json.dumps(dict(case=cfg['case'],attempted=attempted,failed=failed,returned=returned,
 input_identities=[dict(path=n,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)) for n,b in inputs.items()],
 limits=cfg['limits'],collector_sha256=cfg['collector_sha256'],wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))
