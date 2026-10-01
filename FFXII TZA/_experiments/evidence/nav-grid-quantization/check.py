import csv,hashlib,json,math,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins={}
 assert [(x['entry'],x['size']) for x in s['bodies']]==[('0x3924b0',607),('0x383740',252),('0x20e600',10),('0x861f14',6),('0x861f86',6)]
 for b in s['bodies']:
  raw=bytes.fromhex(b['raw_hex']);assert len(raw)==b['size'] and sha(raw)==b['sha256']
  ii=list(cs.disasm(raw,int(b['entry'],16)));assert sum(i.size for i in ii)==len(raw)
  assert ii[-1].mnemonic==('jmp' if b['size']==6 else 'ret')
  assert [{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii]==b['instructions']
  ins.update({i.address:i for i in ii})
 def target(pc):
  i=ins[pc];m=next(o for o in i.operands if o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RIP)
  return i.address+i.size+m.mem.disp
 for k,b in s['bindings'].items():assert target(int(b['site'],16))==int(b['address'],16)
 assert s['constant_hex']==struct.pack('<f',1.).hex() and target(0x39260C)==target(0x39262F)==0x1CEBBA8
 assert s['bindings']['cell_size']['address']=='0x2aee090' and s['bindings']['minA']['address']=='0x2aee070'
 def instr(pc,op,args):
  i=ins[pc];assert(i.mnemonic,i.op_str)==(op,args),(hex(pc),i.op_str)
 instr(0x3924CB,'mov','dword ptr [rip + 0x275bbe3], 0x24')
 instr(0x3924E4,'call','0x383740');instr(0x3924EB,'je','0x3926fa')
 instr(0x3924F9,'mov','eax, 0x2800');instr(0x39250C,'sub','eax, esi')
 instr(0x39252D,'lea','edi, [rsi + 1]');instr(0x392546,'idiv','edi')
 instr(0x392587,'call','0x861f14');instr(0x392600,'maxss','xmm4, xmm3')
 instr(0x392607,'call','0x861f86');instr(0x39260C,'addss','xmm0, dword ptr [rip + 0x1959594]')
 instr(0x39262F,'subss','xmm2, dword ptr [rip + 0x1959571]')
 instr(0x392668,'mov','ecx, ebx');instr(0x39266A,'call','0x384580')
 instr(0x383768,'test','rax, rax');instr(0x38376B,'je','0x383826')
 assert s['bindings']['nav_root']['address']=='0x2aedfb0'
 assert not any(i.mnemonic.startswith('mov') and i.op_str.startswith('eax,') for pc,i in ins.items() if 0x383826<=pc<=0x38383B)
 # Primary qualified-import binding, with sqrtf as the nearby independent name control.
 assert {(x['thunk'],x['iat'],x['name']) for x in s['imports']}=={('0x861f14','0x8c2bb8','sqrtf'),('0x861f86','0x8c2bf0','floorf')}
 for x in s['imports']:
  assert target(int(x['thunk'],16))==int(x['iat'],16)
  assert bytes.fromhex(x['hint_name_hex'])[2:]==x['name'].encode()+b'\0'
  assert bytes.fromhex(x['dll_name_hex'])==x['dll'].encode()+b'\0' and x['dll']=='api-ms-win-crt-math-l1-1-0.dll'
 for p in s['references']:
  b=(HERE/p['retained']).read_bytes();assert len(b)==p['retained_bytes'] and sha(b)==p['retained_sha256']
 fields=list(csv.DictReader((HERE/'retained'/'fields.tsv').open(),delimiter='\t'))
 assert next(x for x in fields if x['name']=='cellSize')['offset']=='0x030'
 assert next(x for x in fields if x['name']=='originAxisA')['offset']=='0x010'
 assert any(x['name']=='vestigialStackCopy074' for x in fields) # Already qualified, no new discovery claimed.
 contract=(HERE/'retained'/'CONTRACT-corridor-query-family.md').read_text()
 page=(HERE/'retained'/'how-a-battle-unit-is-built-from-its-definition.md').read_text()
 types=(HERE/'retained'/'types.tsv').read_text()
 assert '0x2AEE070` cell size' in contract and '0x2800/(n+1)' in page and 'no-op if 00383740 returns zero' in types
 f=lambda v:struct.unpack('<f',struct.pack('<f',v))[0]
 def illustrative(w,h,budget,quantize):
  c0=f(math.sqrt(f(f(w*h)/budget)));nx=math.trunc(f(w/c0));ny=math.trunc(f(h/c0))
  refined=max(f(w/nx),f(h/ny));c=f((math.floor(refined) if quantize else refined)+1.)
  columns=math.trunc(f(f(w+f(c-1.))/c));rows=math.trunc(f(f(h+f(c-1.))/c))
  return {'budget':budget,'initial':c0,'refined':refined,'cell_size':c,'columns':columns,'rows':rows,
   'arithmetic_allocation_argument':columns*rows*37+36,'class':'A conditional arithmetic illustration, not a captured original result/allocation.'}
 illustrations=[]
 for w,h,why in [(100.,100.,'floor omission'),(336.,320.,'working-mask budget subtraction')]:
  a=illustrative(w,h,275,True);wrong=illustrative(w,h,275,False) if w==100 else illustrative(w,h,276,True)
  assert a!=wrong;illustrations.append({'width':w,'height':h,'discriminator':why,'correct_source_formula':a,'omitted_operation_formula':wrong})
 assert illustrations[0]['correct_source_formula']['cell_size']==7. and illustrations[0]['omitted_operation_formula']['cell_size']==7.25
 assert illustrations[1]['correct_source_formula']['cell_size']==22. and illustrations[1]['correct_source_formula']['arithmetic_allocation_argument']==8916
 assert illustrations[1]['omitted_operation_formula']['cell_size']==21. and illustrations[1]['omitted_operation_formula']['arithmetic_allocation_argument']==9508
 return {'method':s['method'],'illustrations':illustrations,'source_bindings':s['bindings'],
  'formula':'n=36; budget=trunc((0x2800-n)/(n+1))=275. w=maxA-minA, h=maxB-minB. c0=sqrtf(f32(w*h)/f32(budget)); nx=trunc(f32(w/c0)), ny=trunc(f32(h/c0)); refined=maxss(f32(w/f32(nx)),f32(h/f32(ny))); c=f32(floorf(refined)+1.0f). cols=trunc(f32(f32(w+f32(c-1.0f))/c)); rows likewise h. Allocation argument uses original32-bit products: cols*rows*(n+1)+n.',
  'established':['Budget subtracts working-mask36B before dividing by37:275, not276. Refined size passes named floorf then adds shipping1.0; the same1.0 is subtracted in cell-count arithmetic. No tiny-epsilon or omitted quantizer.',
   'Cell size is2AEE090;2AEE070/078 are origins A/B and2AEE080 is maximum A. The current field rows already agree, the corridor header labels070 cell size and078/080 eps cells incorrectly.',
   'BitsetBytes2AEE0B8=36 store precedes rectangle call/zero guard. Missing root means no later rectangle/grid/alloc path, apart from this own explicit partial reset and cookie epilogue; no universal no-op.',
   'Existing vestigial stack-copy074/084 meanings are already qualified. This package adds no new uninitialised-data/never-read/lifetime claim.'],
  'limits':s['limits']+' Arithmetic examples are source-derived under named math assumptions, not reconstructed code proving original execution. No zero-dimension, NaN, all-header-space or allocation-capacity/leak conclusion.',
  'affected_consumers':['OPUS NavGridParams types.tsv constructor/no-op and builder formula','OPUS corridor-query contract header global identity','FABLE unit-definition grid-builder budget/formula'],
  'propagation':'PENDING owner corrections and independent review','cleanup':'Read-only image/consumer snapshot; no game/PC/native/input/save/config/reference changes or new live-restoration receipt.'}
if __name__=='__main__':
 s=json.loads((HERE/'source.json').read_text());o=derive(s)
 (HERE/'observation.json').write_text(json.dumps(o,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS_STATIC_ONLY','complete_original_bodies':3,'qualified_import_controls':2,
  'conditional_arithmetic_illustrations':2,'new_original_code_native_or_live_cases':0,
  'limits':'Exact source/formula/identity/guard qualification only; no actual native math/allocation/init, independent acceptance or broad campaign.'},indent=2)+'\n')
 print('PASS exact navigation-grid budget/quantizer/identity and early reset; illustrations not execution.')
