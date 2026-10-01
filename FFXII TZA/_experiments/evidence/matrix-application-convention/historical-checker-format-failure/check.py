import hashlib,json,struct,subprocess
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
COMMIT='fcbffd545c30575039e80afc272680d6d71e9a38'
PREFIX='Database/FFXII TZA/_experiments/evidence/gs-coordinate-conversion/'
def capture():
 ret=HERE/'retained';ret.mkdir(exist_ok=True);refs=[]
 for name in ['source.json','raw-results.json','observation.json','validation.json','manifest.json']:
  b=subprocess.check_output(['git','show',COMMIT+':'+PREFIX+name]);(ret/('gs-'+name)).write_bytes(b)
  assert Path(PREFIX+name).read_bytes()==b,'Current evidence differs from committed receipt'
  refs.append({'path':PREFIX+name,'commit':COMMIT,'retained':'retained/gs-'+name,'bytes':len(b),'sha256':sha(b)})
 p=Path('Database/FFXII TZA/_experiments/EXP-219-kind1C-catchall-emit-internals-exec.md');b=p.read_bytes()
 (ret/p.name).write_bytes(b);refs.append({'path':p.as_posix(),'retained':'retained/'+p.name,'bytes':len(b),'sha256':sha(b)})
 (HERE/'source.json').write_text(json.dumps({'method':'A existing verified original-code capture and fresh consumer interpretation',
  'existing_B_commit':COMMIT,'consumer_origin_commit':'d98879552','references':refs,
  'limits':'No new B/native/live execution or universal matrix type/convention/ordinary renderer claim. Existing original-code execution retains its supplied state and pending independent acceptance.'},indent=2)+'\n')
def derive():
 s=json.loads((HERE/'source.json').read_text());refs=s['references']
 for p in refs:
  b=(HERE/p['retained']).read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256']
  if 'commit' in p:assert subprocess.check_output(['git','show',p['commit']+':'+p['path']])==b
 assert subprocess.run(['git','merge-base','--is-ancestor',COMMIT,'HEAD'],capture_output=True).returncode==0
 gs=json.loads((HERE/'retained'/'gs-source.json').read_text());r=json.loads((HERE/'retained'/'gs-raw-results.json').read_text())
 assert gs['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 b=next(x for x in gs['bodies'] if x['entry']=='0x217060');raw=bytes.fromhex(b['raw_hex'])
 assert b['size']==235 and sha(raw)==b['sha256']=='5c072a689347f4faf38b7944bce418c22ed521bf5e0f531bc9be30cb3fbce678'
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii=list(cs.disasm(raw,0x217060))
 assert sum(i.size for i in ii)==235 and ii[-1].mnemonic=='ret' and not any(i.mnemonic=='call' for i in ii)
 def instruction(pc,op,args):
  i=next(x for x in ii if x.address==pc);assert(i.mnemonic,i.op_str)==(op,args)
 for pc,reg,off in [(0x217075,'xmm0',0),(0x21709C,'xmm2',0x10),(0x21707C,'xmm1',0x20),(0x2170AD,'xmm0',0x30),
  (0x2170C5,'xmm0',4),(0x2170A1,'xmm3',0x14),(0x2170B9,'xmm1',0x24),(0x2170D8,'xmm0',0x34),
  (0x2170FF,'xmm0',8),(0x2170E2,'xmm2',0x18),(0x2170F3,'xmm1',0x28),(0x21711A,'xmm0',0x38),
  (0x217104,'xmm4',0xC),(0x2170DD,'xmm7',0x1C),(0x2170EE,'xmm5',0x2C),(0x217115,'xmm6',0x3C)]:
  instruction(pc,'mulss',reg+', dword ptr [rdx'+(' + '+hex(off) if off else '')+']')
 for pc,reg,off in [(0x217064,'xmm4',0),(0x217090,'xmm7',4),(0x21706C,'xmm5',8),(0x217086,'xmm6',0xC)]:
  instruction(pc,'movss',reg+', dword ptr [r8'+(' + '+hex(off) if off else '')+']')
 assert len(r)==8 and all(x['failure'] is None and not x['faults'] and x['code_unchanged'] for x in r)
 x=next(x for x in r if x['name']=='matrix-and-homogeneous-divide');v=[1.,2.,3.,1.];mat=x['matrix']
 assert x['boundaries'][1]['destination_hex'][:32]==struct.pack('<4f',*v).hex()
 assert x['boundaries'][-1]['pc']=='0x20ead8'
 actual=list(struct.unpack('<4f',bytes.fromhex(x['boundaries'][-1]['destination_hex'])[:16]))
 applied=[sum(v[i]*mat[4*i+j] for i in range(4)) for j in range(4)]
 competing=[sum(mat[4*j+i]*v[i] for i in range(4)) for j in range(4)]
 assert actual==applied==[12.,26.,42.,2.] and competing==[2.,6.,12.,142.] and actual!=competing
 # The demonstration uses exactly representable integer products/sums; no f64/f32 equivalence claim.
 doc=(HERE/'retained'/'EXP-219-kind1C-catchall-emit-internals-exec.md').read_text()
 assert 'out = mat × in' in doc and 'row-major float math' in doc
 formula={hex(j*4):{'X_byte_offset':hex(j*4),'Y_byte_offset':hex(0x10+j*4),
  'Z_byte_offset':hex(0x20+j*4),'W_byte_offset':hex(0x30+j*4)} for j in range(4)}
 return {'method':s['method'],'original_leaf_hash':b['sha256'],'output_component_matrix_byte_offsets':formula,
  'existing_control':{'input':v,'matrix_floats':mat,'original_before_divide':actual,
   'row_major_matrix_left_times_column_vector':competing,'actual_after_divide':x['output_first_ten_floats'][:4]},
  'established':['Output[j] uses X*m[j]+Y*m[4+j]+Z*m[8+j]+W*m[12+j], with indices in floats. Exact shipping SSE products/adds order remains Y+X, then Z, then W.',
   'These bytes support row-vector input multiplied on the left of a row-major matrix, or a column-major matrix multiplied by a column vector on the right. A leaf alone cannot choose a universal engine storage convention.',
   'The paired EXP219 shorthand out=mat×in and row-major needs an explicit vector/storage convention. Interpreted as ordinary row-major left-multiplication of a column vector, it contradicts the existing original control.'],
  'semantic_implication':'Specify operand-index formula and vector side along with storage labels; avoid a transpose error when reproducing the shared helper. Keep type/ownership/normal-caller meanings separate.',
  'limits':s['limits']+' No new fixture/campaign, native rendering or all-engine transpose finding. The competing algebraic calculation is a discriminator, not a new original-code trace.',
  'affected_consumers':['SWE2-ORACLE EXP219 helper semantics','OPUS existing GS coordinate return/representation consumer','FABLE existing GS/glyph matrix consumers if they adopt EXP219 shorthand'],
  'propagation':'PENDING producer/owner qualification and independent review','cleanup':'Read-only committed artifacts and consumer preimage; no game/PC/input/attachment/save/config/reference changes.'}
if __name__=='__main__':
 import sys
 if '--capture' in sys.argv:capture()
 o=derive();(HERE/'observation.json').write_text(json.dumps(o,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS_EXISTING_CAPTURE_QUALIFICATION','existing_B_commit':COMMIT,
  'existing_discriminating_case':'matrix-and-homogeneous-divide','new_original_code_or_live_cases':0,
  'limits':'Exact source/application pairing only. Independent acceptance and owner propagation pending.'},indent=2)+'\n')
 print('PASS exact matrix application formula against retained original nonidentity control; no recapture.')
