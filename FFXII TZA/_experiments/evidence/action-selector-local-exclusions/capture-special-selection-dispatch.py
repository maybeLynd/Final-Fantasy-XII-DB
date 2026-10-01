"""OV42 next discriminator: which categories queue special actions; fallback id domain.
Only the original caller prefix and complete 234-byte matcher are decoded.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(0x306760,0x3067c2),(0x2f8d60,0x2f8e4a)]
C.main()
p=pathlib.Path(sys.argv[1]);r=json.loads(p.read_text())
b=C.EXE.read_bytes();pe=struct.unpack_from('<I',b,0x3c)[0];opt=struct.unpack_from('<H',b,pe+20)[0]
sections=[struct.unpack_from('<IIII',b,pe+24+opt+i*40+8) for i in range(struct.unpack_from('<H',b,pe+6)[0])]
def read(a,n):
 for vs,va,rs,ro in sections:
  if C.BASE+va<=a and a+n<=C.BASE+va+rs:return b[ro+a-C.BASE-va:ro+a-C.BASE-va+n]
 raise ValueError('unbacked jump table')
ins={int(i['pc'],16):i for s in r['ranges'] for i in s['instructions']}
# The dispatch input is a separate mode dword, not row category+1E.
# Derive the six-entry extent from the actual unsigned guard after DEC.
if (ins[0x3067b7]['mnemonic'],ins[0x3067b7]['args'])!=('cmp','eax, 5') or (ins[0x3067ba]['mnemonic'],ins[0x3067ba]['args'])!=('ja','0x306a9a'):
 raise ValueError('dispatch extent prerequisite')
jt=read(0x306af0,6*4)
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 jump_table=dict(address='0x306af0',bytes=jt.hex(),entries=6,input='mode dword022C215C minus1, unsigned <=5',targets=[hex(C.BASE+x) for x in struct.unpack('<6I',jt)]),
 limits='source prefix/jump-table and matcher only; no initialized codec, authored threshold data/override bounds or natural selection proof',
 wrapper_complete=True)
p.write_text(json.dumps(r,indent=2)+'\n')
print('CAPTURED dispatch prefix, guard-derived6-entry table and original matcher; no gameplay')
