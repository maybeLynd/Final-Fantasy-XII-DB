"""New range cases through the retained original-window observer; no live FF12."""
import ast,datetime,hashlib,importlib.util,json,math,struct,subprocess,sys
from pathlib import Path
import capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
from unicorn.x86_const import *
W=Path(__file__).resolve().parent;R=W/'retained';R.mkdir(exist_ok=True)
assert not (W/'raw.json').exists(),'Capture once; never replace retained observations'
sha=lambda b:hashlib.sha256(b).hexdigest()
tools=dict(recorded_before_capture_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,unicorn=unicorn.__version__,unicorn_module_sha256=sha(Path(unicorn.__file__).read_bytes()),binaries=[])
for label,p in [('unicorn',Path(backend.uclib._name)),('capstone',Path(capstone._cs._name))]:tools['binaries'].append(dict(label=label,path=str(p),bytes=p.stat().st_size,sha256=sha(p.read_bytes())))
parent=Path('Database/FFXII TZA/_experiments/evidence/procedural-mode-cost');manifest=json.loads((parent/'manifest.json').read_text())
assert manifest['members']
for x in manifest['members']:
 raw=(parent/x['path']).read_bytes();assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
pb=(parent/'source.json').read_bytes();s=json.loads(pb);body=bytes.fromhex(s['raw_hex']);assert sha(body)=='32f4c93324e6c153518b5b42e85597f75495de8f66171fd58daf355e7b9a063a'
pc='0bcc3d620c620234f2f987b00e70ffe8f6d0c08e'
assert subprocess.check_output(['git','show',pc+':'+(parent/'source.json').as_posix()])==pb
rp=Path(s['reader']['path']);assert sha(rp.read_bytes())==s['reader']['sha256']
spec=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
image,sections=reader.load_image();assert sha(image)==s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert reader.img_rd(image,sections,0x3D8E50,418)==body
one=reader.img_rd(image,sections,0x1EF93FC,4);assert one==bytes.fromhex('0000803f')
ENTRY,END,SAMPLE=0x3D8F3F,0x3D8F79,0x3FFFFFFF
code=body[ENTRY-0x3D8E50:END-0x3D8E50];assert len(code)==58 and sha(code)=='f35064469004fa9448432dd22dc7c46767058dbb4c833ab86c8063ea4bc3cdd8'
base=Path('Database/FFXII TZA/_experiments/evidence/scaled-random-float-order')
bm=json.loads((base/'manifest.json').read_text());assert bm['members']
for x in bm['members']:
 raw=(base/x['path']).read_bytes();assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
oldraw=json.loads((base/'raw.json').read_text());driver=(base/'capture.py').read_bytes();assert sha(driver)==oldraw['driver_sha256']
# Reuse the exact already-controlled observer function, without importing or
# re-executing the old capture's top-level cases. Only new input cases follow.
tree=ast.parse(driver);nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='run'];assert len(nodes)==1
function_text=ast.get_source_segment(driver.decode(),nodes[0])
f32=lambda x:struct.unpack('<f',struct.pack('<f',x))[0]
floating=lambda x:struct.unpack('<f',struct.pack('<I',x))[0]
bits=lambda x:struct.unpack('<I',struct.pack('<f',x))[0]
def rounded(x):
 try:return f32(x)
 except OverflowError:return math.copysign(math.inf,x) # Host prediction, NOT original evidence.
def model(a,sample):
 a,v=floating(a),floating(sample)
 return dict(original_order=bits(rounded(rounded(a*v)-rounded(a*1.0))),factored=bits(rounded(a*rounded(v-1.0))))
exec(compile(ast.Module(body=nodes,type_ignores=[]),'retained original-window observer','exec'),globals())
for n,b in [('parent-source.json',pb),('parent-manifest.json',(parent/'manifest.json').read_bytes()),('shipping-reader.py',rp.read_bytes()),('window.bin',code),('one.bin',one),('prior-capture.py',driver),('reused-observer.txt',function_text.encode())]:
 assert not (R/n).exists();(R/n).write_bytes(b)
page=Path('Database/FFXII TZA/21-RNG-And-Determinism/rng-streams.md');pagebytes=page.read_bytes();(R/'rng-streams.md').write_bytes(pagebytes)
cases=[run('smallest-positive-subnormal-endpoint',0x00000001),run('ordinary-normal-strict-interior-control',0x3F000000),run('largest-positive-finite-product-overflow',0x7F7FFFFF),run('normal-subtract-to-add-detector',0x3F000000,True)]
for t in tools['binaries']:assert sha(Path(t['path']).read_bytes())==t['sha256'],'Tool binary changed during capture'
receipt=dict(method='B isolated original58B, injected arithmetic entry state; new strict-range boundary question',reference=dict(exe_sha256=s['exe_sha256'],image_base=s['image_base'],parent_commit=pc,parent_entry=s['entry'],parent_body_sha256=sha(body),parent_source_sha256=sha(pb),parent_manifest_sha256=sha((parent/'manifest.json').read_bytes()),window_sha256=sha(code),reader_sha256=sha(rp.read_bytes()),one_va='0x1ef93fc',one_hex=one.hex()),tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),observer_reuse=dict(prior_capture_sha256=sha(driver),exact_function_sha256=sha(function_text.encode()),prior_cases_not_rerun=True,changes='Only new sample/amplitude cases; host prediction handles overflow explicitly. Retained observer code unchanged.'),cases=cases,consumer=dict(path=page.as_posix(),sha256=sha(pagebytes),head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()),preflight=dict(method='Host source prediction only, no original execution',sample_bits='0x3fffffff',subnormal_amplitude_bits='0x1',predicted_product_bits='0x2',predicted_output_bits='0x1',normal_amplitude_bits='0x3f000000',predicted_normal_output_bits='0x3efffffe'),limits='Injected sample/stack/scratch/MXCSR1F80 (masked exceptions, nearest, no DAZ/FTZ). Entry omits recurrence/nativeSave/initial amplitude guard; stop omits nativeRestore/full return/caller. No proof samplemax or amplitude boundaries occur in normal gameplay, actual game MXCSR, native CPU exception/status semantics, universal subnormal handling or full-function range. No old0.3f order case rerun.',cleanup='Disposable emulator instances only; no game/PC controls, process attach, save/config/reference writes; no live health/cleanup claimed.')
(W/'raw.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Retained new original-window range observations and normal detector; acceptance requires check.py.',flush=True)
