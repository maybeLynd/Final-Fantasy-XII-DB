"""OV42 remaining override: reuse original direct-call discovery and verified capture.
No whole write-set/indirect caller closure is inferred from these bounded prefixes.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
b=C.EXE.read_bytes()
if hashlib.sha256(b).hexdigest()!=C.SHA:raise ValueError('reference identity')
p=struct.unpack_from('<I',b,0x3c)[0];opt=struct.unpack_from('<H',b,p+20)[0]
secs=[struct.unpack_from('<IIII',b,p+24+opt+i*40+8) for i in range(struct.unpack_from('<H',b,p+6)[0])]
def read(a,n):
 for vs,va,rs,ro in secs:
  if C.BASE+va<=a and a+n<=C.BASE+va+rs:return b[ro+a-C.BASE-va:ro+a-C.BASE-va+n]
 raise ValueError('unbacked source')
va=C.BASE+secs[0][1];blob=read(va,secs[0][2])
def callers(target):
 return [va+i for i,x in enumerate(blob[:-4]) if x==0xe8 and va+i+5+struct.unpack_from('<i',blob,i+1)[0]==target]
if 0x25daed not in callers(0x32fc30):raise ValueError('direct discovery positive')
a,n=struct.unpack_from('<II',b,p+24+112+3*8);pd=list(struct.iter_unpack('<III',read(C.BASE+a,n)))
sites=[];unresolved=[];spans={(0x2f79e0,0x2f79f1),(0x2f7a00,0x2f7a07)}
for target in [0x2f79e0,0x2f7a00]:
 for pc in callers(target):
  rows=[(x+C.BASE,y+C.BASE,u+C.BASE) for x,y,u in pd if x+C.BASE<=pc<y+C.BASE]
  if len(rows)!=1:unresolved.append(dict(pc=hex(pc),target=hex(target),reason='no unique pdata prefix'));continue
  x,y,u=rows[0]
  if pc+5-x>0x3000:raise ValueError('source prefix budget')
  spans.add((x,pc+5));sites.append(dict(pc=hex(pc),target=hex(target),fragment_start=hex(x),fragment_end=hex(y)))
C.RANGES=sorted(spans);C.main()
out=pathlib.Path(sys.argv[1]);r=json.loads(out.read_text());ins={int(i['pc'],16):i for s in r['ranges'] for i in s['instructions']}
for x in sites:
 i=ins[int(x['pc'],16)]
 if (i['mnemonic'],i['args'])!=('call',x['target']):raise ValueError('unaligned direct candidate')
if ins[0x2f79e8]['memory'][0]['rip_target']!='0x22be930' or ins[0x2f7a00]['memory'][0]['rip_target']!='0x1eebaf0':raise ValueError('known object controls')
constant=read(0xd0f9e0,16);index=read(0x1eebaf0,4)
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 wrapper_complete=True,direct_calls=sites,unresolved_candidates=unresolved,
 initializer_constant=dict(address='0xd0f9e0',bytes=constant.hex(),words=list(struct.unpack('<8H',constant))),
 file_backed_index=dict(address='0x1eebaf0',bytes=index.hex(),signed_value=struct.unpack('<i',index)[0]),
 limits='bounded direct-call prefixes, original initializer and file-backed value; no complete writer/indirect alias closure, no initialized lifetime/index bound or natural selection proof')
out.write_text(json.dumps(r,indent=2)+'\n')
print('CAPTURED override initializer/setter and',len(sites),'aligned direct-call prefixes; runtime values not inferred from file defaults')
