import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent
s=json.loads((W/'source.json').read_text());m=s['memory_operands']
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((W/'retained/gs-source.json').read_bytes())==s['reference_sha256']
assert s['reference_sha256']=='467e3ea5e5a13015b103585831bfb22adc106aeaac9dcb6f86f453e22e367d9d'
for b in s['bodies']:assert sha(bytes.fromhex(b['raw_hex']))==b['sha256']
assert s['calls']==[dict(pc='0x202b7e',destination='0x217060')]
def select(base,access):return [x for x in m if x['base']==base and x['access']==access]
inputs=select('r8','read');outputs=select('rcx','write');mat=select('rdx','read')
assert [(x['pc'],x['disp'],x['width']) for x in inputs]==[('0x217064',0,4),('0x21706c',8,4),('0x217086',12,4),('0x217090',4,4)]
assert [(x['pc'],x['disp'],x['width']) for x in outputs]==[('0x2170ce',0,4),('0x21710d',4,4),('0x217138',8,4),('0x21713d',12,4)]
assert max(int(x['pc'],16) for x in inputs)<min(int(x['pc'],16) for x in outputs)
assert len(mat)==16 and {x['disp'] for x in mat}==set(range(0,64,4))
hazards=[]
for out in outputs:
 for read in mat:
  if out['disp']+8==read['disp'] and int(out['pc'],16)<int(read['pc'],16):
   hazards.append(dict(write_pc=out['pc'],read_pc=read['pc'],matrix_disp=read['disp']))
assert hazards==[dict(write_pc='0x2170ce',read_pc='0x2170ff',matrix_disp=8)]
assert next(x['pc'] for x in mat if x['disp']==12)=='0x217104'
assert int('217104',16)<int('21710d',16) # m[3] read before Y replaces it
wrapper=next(b for b in s['bodies'] if b['entry']=='0x202b70')
ii={i['pc']:i for i in wrapper['instructions']}
assert ii['0x202b79']['bytes']=='488d4c2420' # out=private rsp+20
assert ii['0x202b83']['bytes']=='0f1000' and ii['0x202b86']['bytes']=='0f1103'
assert int('202b7e',16)<int('202b83',16)<int('202b86',16)
leaf=next(b for b in s['bodies'] if b['entry']=='0x217060')
li={i['pc']:i for i in leaf['instructions']}
assert li['0x217069']['bytes']=='488bc1'
assert ii['0x202b76']['bytes']=='488bd9'
assert not any(i['op']=='mov' and i['args'].startswith('rax,') for i in wrapper['instructions'])
assert (-8-0x30+0x20)==-0x18 # temporary relative to wrapper entry RSP
# Small exact finite arithmetic illustration, NOT original execution or an
# emulator/model agreeing with itself. All products/sums fit exactly in f32.
normal=[1*2+2*0+3*0+1*10,1*0+2*3+3*0+1*20,1*0+2*0+3*4+1*30,1*0+2*0+3*0+1*2]
overlap=[normal[0],normal[1],2*0+1*normal[0]+3*4+1*30,normal[3]]
naive_reloads_w=1*normal[1]+2*0+3*0+1*2
assert normal==[12,26,42,2] and overlap==[12,26,54,2] and naive_reloads_w==28
v=dict(status='PASS_STATIC_ONLY',new_original_code_executions=0,live_cases=0,
 vector_input_snapshot=True,vector_overlap_limit='Matrix disjoint from output; valid/stable source ranges and private frame unaliased.',
 output_matrix_offset8_hazard=hazards,conditional_disjoint=normal,conditional_overlap=overlap,
 incorrect_per_column_reload_w=naive_reloads_w,
 wrapper_rax_residue='Leaf scratch pointer S-0x18; wrapper does not replace with caller out. Copied before frame teardown; not a usable returned-object guarantee or inferred C return type.',
 wrapper='Stages16B in private stack until real leaf returns then copies to original out; alias-safe under stated frame/domain assumptions.',
 source_sha256=sha((W/'source.json').read_bytes()),cleanup='Read-only retained artifacts; PC OFF, no native game/save/config/reference changes.')
if (W/'manifest.json').exists():
 assert json.loads((W/'validation.json').read_text())==v # frozen result immutable
else:
 (W/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
print('PASS A operand ordering: vector snapshot, one matrix+8 read-after-write hazard, cached-W negative control, wrapper staged copy. No alias run.',flush=True)
