"""Focused producer controls, explicitly not native/live FF12 experiments."""
import hashlib,importlib.util,json,pathlib,shutil,struct,subprocess,sys
W=pathlib.Path(__file__).resolve().parent
SOURCE=W/'softedges-resource-source-01'
OUT=W/'softedges-field-extent-controls-01'
if OUT.exists():raise ValueError('immutable control directory exists')
OUT.mkdir()
spec=importlib.util.spec_from_file_location('reducer',W/'reduce-softedges-field-extent.py')
R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
original=(SOURCE/'phyretext.fx.phyre').read_bytes()
result=R.analyze(original);selected=result['selected'];checks=[]
def retain(name,data):
 p=OUT/(name+'.phyre');p.open('xb').write(data)
 return dict(path=p.name,sha256=hashlib.sha256(data).hexdigest())
def fail_control(name,data):
 record=retain(name,data)
 try:R.analyze(data)
 except (ValueError,IndexError) as e:
  checks.append(dict(name=name,status='PASS_EXPECTED_REFUSAL',input=record,exception=type(e).__name__,message=str(e)))
 else:raise AssertionError('corrupt prerequisite accepted: '+name)
assert selected['name']=='softEdges' and selected['masked_size']==8
assert not result['conditional_copy']['reads_any_AE0']
checks.append(dict(name='shipping_named_extent',status='PASS',input_sha256=R.sha(original),
 observations=dict(softEdges=8,textColor=16,alphaThreshold=4,reads_AE0=False)))
# A deliberately altered byte extent must reverse the conditional read result;
# it remains a disposable-file discriminator and is refused by shipping CLI hash.
large=bytearray(original);struct.pack_into('<H',large,selected['record_file_start']+7,0x9c4)
large=bytes(large);r=R.analyze(large);record=retain('synthetic-enlarged-extent',large)
assert r['conditional_copy']['reads_whole_AE0'] and r['selected']['masked_size']==0x9c4
checks.append(dict(name='enlarged_extent_crosses_AE0',status='PASS_SYNTHETIC_DISCRIMINATOR',input=record,
 observation=r['conditional_copy'],limits='Mutated retained bytes, not authored shipping data or original-code/game execution'))
bad=bytearray(original);bad[selected['name_file_start']]=ord('X')
fail_control('changed-name',bytes(bad))
h=struct.unpack_from('<21I',original);nt=struct.unpack_from('<I',original,h[1]+8)[0]
bad=bytearray(original);parent_word=h[1]+32+4*nt+36*(result['namespace']['nested_type_class_id']-1)
struct.pack_into('<I',bad,parent_word,0)
fail_control('broken-inherited-offset-parent',bytes(bad))
bad=bytearray(original);header=h[1]+h[2]+36*result['list']['index'];struct.pack_into('<I',bad,header+12,154)
fail_control('wrong-objects-extent',bytes(bad))
fail_control('truncated-array-table',original[:-1])

def cli_case(name,alter):
 d=OUT/name;d.mkdir()
 for p in SOURCE.iterdir():
  if p.is_file():shutil.copyfile(p,d/p.name)
 alter(d);output=d/'MUST-NOT-EXIST.json'
 args=[sys.executable,str(W/'reduce-softedges-field-extent.py'),str(d),str(output)]
 r=subprocess.run(args,capture_output=True,timeout=15)
 (d/'stdout.txt').open('xb').write(r.stdout);(d/'stderr.txt').open('xb').write(r.stderr)
 if r.returncode==0 or output.exists():raise AssertionError('actual prerequisite CLI incorrectly passed: '+name)
 rec=dict(name=name,status='PASS_EXPECTED_UPSTREAM_FAIL',argv=args,exit=r.returncode,result_exists=output.exists(),
   stdout_sha256=R.sha(r.stdout),stderr_sha256=R.sha(r.stderr))
 (d/'status.json').open('x').write(json.dumps(rec,indent=2)+'\n');checks.append(rec)
def incomplete(d):
 p=d/'original-code-raw-01.json';r=json.loads(p.read_text());r['wrapper_complete']=False;p.write_text(json.dumps(r)+'\n')
def missing(d):(d/'constructor-source-retained-01.json').unlink()
def wrong_asset(d):(d/'phyretext.fx.phyre').write_bytes(large)
cli_case('incomplete-source-cli',incomplete)
cli_case('missing-caller-cli',missing)
cli_case('changed-shipping-asset-cli',wrong_asset)
r=dict(status='PASS_PRODUCER_CONTROLS',driver_sha256=R.sha(pathlib.Path(__file__).read_bytes()),
 reducer_sha256=R.sha((W/'reduce-softedges-field-extent.py').read_bytes()),checks=checks,
 limits='Private producer regressions and disclosed disposable file mutations. No independent acceptance, native execution or live samples.')
(OUT/'result.json').open('x').write(json.dumps(r,indent=2)+'\n')
print('PASS focused extent, name, inheritance, payload/fixup and actual CLI prerequisite controls; all children terminal')
