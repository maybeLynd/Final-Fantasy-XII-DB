import hashlib,json,struct
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;sha=lambda x:hashlib.sha256(x).hexdigest()
r=json.loads((W/'raw.json').read_text());ref=r['reference']
assert ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert r['driver_sha256']==sha((W/'capture.py').read_bytes())
for name,key in [('source.json','parent_source_sha256'),('parent-manifest.json','parent_manifest_sha256'),('shipping-reader.py','reader_sha256')]:assert sha((W/'retained'/name).read_bytes())==ref[key]
s=json.loads((W/'retained/source.json').read_text());b=next(x for x in s['bodies'] if x['entry']=='0x3924b0');body=bytes.fromhex(b['raw_hex'])
assert len(body)==607 and sha(body)==ref['parent_body_sha256']=='0a7ec1000ef3d48a471ff9200675b11ef90717fedcb53b50afa84a4281e236f5'
code=(W/'retained/window.bin').read_bytes();assert len(code)==123 and code==body[0xDC:0x157] and sha(code)==ref['window_sha256']
assert ref['entry']=='0x39258c' and ref['end']=='0x392607'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);ins=list(cs.disasm(code,0x39258C));assert sum(i.size for i in ins)==123
assert r['instructions']==[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ins]
assert not any(i.mnemonic.startswith('j') or i.mnemonic in ('call','ret') for i in ins)
lookup={i.address:i for i in ins}
for pc,raw in [(0x3925A9,'f30f2cc1'),(0x3925CE,'f30f2cc1'),(0x3925E9,'f30f5ee2'),(0x3925FC,'f30f5eda'),(0x392600,'f30f5fe3')]:assert lookup[pc].bytes.hex()==raw
assert len(r['tools']['binaries'])==2 and {x['name'] for x in r['tools']['binaries']}=={'capstone','unicorn'} and all(x['bytes']>0 and len(x['sha256'])==64 for x in r['tools']['binaries'])
assert [c['name'] for c in r['cases']]==['positive-square-count-control','positive-skinny-zero-count','skinny-rounded-conversion-detector']
mut=bytearray(code);mut[0x3925A9-0x39258C+2]=0x2D
expected=[('41800000','41800000','3F76FF83','00000010','00000010','3F800000','3F800000','3F800000'),('3F800000','43C80000','3F9A5FB2','00000000','0000014B','7F800000','3F9AAECB','7F800000'),('3F800000','43C80000','3F9A5FB2','00000001','0000014B','3F800000','3F9AAECB','3F9AAECB')]
for n,(c,e) in enumerate(zip(r['cases'],expected)):
 width,height,c0,nx,ny,wx,hy,floorarg=e;initial=c['initial'];a=c['after']
 assert initial['rsp']=='0x60001800' and initial['mxcsr']=='0x1f80' and initial['sqrt_return_bits']==c0 and initial['width_bits']==width and initial['height_bits']==height
 # Direct initialized register reads retained from the actual provider, not just requested values.
 assert initial['registers']=={'44':'0x60001800','35':'0x0','249':'0x1f80','122':hex(int(c0,16)),'123':'0x0','124':'0x0','125':'0x0','126':'0x0','128':'0x0','129':'0x0','130':hex(int(width,16)),'131':hex(int(height,16)),'132':hex(int(width,16)),'133':hex(int(height,16))}
 stack=bytearray(64)
 for off in (0x24,0x34):stack[off:off+4]=bytes.fromhex('a5a5a5a5')
 assert initial['globals']=='a5'*28 and initial['stack']==stack.hex()
 assert c['running_code_sha256']==sha(bytes(mut) if n==2 else code) and c['mutated']==(n==2)
 assert c['failure'] is None and c['visited']==[hex(i.address) for i in ins] and a['stop_pc']=='0x392607' and a['rsp']==initial['rsp'] and a['stack']==initial['stack']
 assert c['states']==[dict(pc='0x3925ad',eax=nx,xmm4=width,xmm3='00000000'),dict(pc='0x3925d2',eax=ny,xmm4=width,xmm3=height),dict(pc='0x3925ed',eax=ny,xmm4=wx,xmm3=height),dict(pc='0x392600',eax=ny,xmm4=wx,xmm3=hy)]
 assert a['floor_argument_bits']==floorarg
 assert c['reads']==[dict(pc='0x3925d2',address='0x60001824',size=4),dict(pc='0x3925e3',address='0x60001834',size=4)]
 spec=[(0x392590,0x2AEE070,'00000000'),(0x3925A0,0x2AEE078,int(width,16).to_bytes(4,'little').hex()),(0x3925B1,0x2AEE080,'00000000'),(0x3925C1,0x2AEE088,int(height,16).to_bytes(4,'little').hex()),(0x3925DB,0x2AEE074,'a5a5a5a5'),(0x3925F4,0x2AEE084,'a5a5a5a5')]
 assert c['writes']==[dict(pc=hex(pc),address=hex(p),bytes=v) for pc,p,v in spec]
 assert len(c['raw_writes'])==6
 globals_after=bytearray.fromhex(initial['globals'])
 for x,(pc,p,v) in zip(c['raw_writes'],spec):
  assert x['pc']==hex(pc) and x['address']==hex(p) and x['size']==4 and isinstance(x['provider_value'],int)
  globals_after[p-0x2AEE070:p-0x2AEE070+4]=bytes.fromhex(v)
 assert a['globals']==globals_after.hex()
assert r['cases'][1]['initial']==r['cases'][2]['initial'] and r['cases'][1]['after']['floor_argument_bits']!=r['cases'][2]['after']['floor_argument_bits']
assert r['cases'][2]['running_code_sha256']!=ref['window_sha256']
assert r['preparation']['skinny_header_hex']=='0114011400000000'
assert struct.unpack('<4B2h',bytes.fromhex(r['preparation']['skinny_header_hex']))==(1,20,1,20,0,0)
if (W/'manifest.json').exists():
 m=json.loads((W/'manifest.json').read_text());assert m['members']
 for x in m['members']:
  data=(W/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
print('PASS_ORIGINAL_PREFIX positive-square nx=ny16/floorarg1; injected skinny nx0/ny331/floorargInf; labelled rounded conversion nx1/finite detector; exact source/state/writes/stop. No native sqrtf/floorf/builder/live or CPU exception proof.')
