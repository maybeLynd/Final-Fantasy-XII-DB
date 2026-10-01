"""OV42: bounded original fragments referencing the two preload-output cells.
Direct RIP-relative discovery only. Indirect aliases/whole logical CFGs remain open.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
import capstone
W=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
raw=C.EXE.read_bytes()
if hashlib.sha256(raw).hexdigest()!=C.SHA:raise ValueError('reference identity changed')
p=struct.unpack_from('<I',raw,0x3c)[0];optional=struct.unpack_from('<H',raw,p+20)[0]
sections=[struct.unpack_from('<IIII',raw,p+24+optional+i*40+8)
 for i in range(struct.unpack_from('<H',raw,p+6)[0])]
def read(va,n):
 for vs,sva,rs,ro in sections:
  if C.BASE+sva<=va and va+n<=C.BASE+sva+rs:return raw[ro+va-C.BASE-sva:ro+va-C.BASE-sva+n]
 raise ValueError('unbacked original range')
va=C.BASE+sections[0][1];blob=read(va,sections[0][2]);targets={0x22c2178,0x22c218c}
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
sites=set()
# disp32 ends at instruction end, or before a trailing imm8/imm32. Candidate
# decoding and then original-fragment alignment reject byte-pattern accidents.
for off in range(len(blob)-4):
 d=struct.unpack_from('<i',blob,off)[0]
 if not any(va+off+4+tail+d in targets for tail in (0,1,4)):continue
 for start in range(max(0,off-10),off):
  ins=next(cs.disasm(blob[start:start+15],va+start,count=1),None)
  if not ins or not (start<=off and off+4<=start+ins.size):continue
  if any(o.type==capstone.CS_OP_MEM and ins.reg_name(o.mem.base)=='rip' and
         ins.address+ins.size+o.mem.disp in targets for o in ins.operands):sites.add(ins.address)
a,n=struct.unpack_from('<II',raw,p+24+112+3*8)
pd=list(struct.iter_unpack('<III',read(C.BASE+a,n)))
fragments={};unresolved=[]
for pc in sorted(sites):
 rows=[(b+C.BASE,e+C.BASE,u+C.BASE) for b,e,u in pd if b+C.BASE<=pc<e+C.BASE]
 if len(rows)!=1:unresolved.append(dict(pc=hex(pc),reason='no unique exception fragment'));continue
 start,end,u=rows[0]
 if end-start>0x5000:raise ValueError('bounded fragment budget exceeded')
 fragments[(start,end)]=u
if not fragments:raise ValueError('missing evidence, never valid empty output')
# Known leaf has no pdata; absence there is not absence of original code.
if not {0x309c00,0x309c22}<=sites:raise ValueError('candidate discovery controls failed before capture')
C.RANGES=sorted(fragments)+[(0x309c00,0x309c32)];C.main()
out=pathlib.Path(sys.argv[1]);r=json.loads(out.read_text());records=[]
for span in r['ranges']:
 for ins in span['instructions']:
  for m in ins['memory']:
   if m['rip_target'] and int(m['rip_target'],16) in targets:
    records.append(dict(pc=ins['pc'],target=m['rip_target'],role=m['role'],bytes=ins['bytes'],
                        mnemonic=ins['mnemonic'],args=ins['args'],fragment=span['start']))
if not any(x['pc']=='0x309c00' and x['role']=='r' for x in records):raise ValueError('read discovery positive missing')
if not any(x['pc']=='0x309c22' and x['role']=='w' for x in records):raise ValueError('immediate-store discovery positive missing')
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
 wrapper_complete=True,direct_rip_references=records,unresolved_candidate_fragments=unresolved,
 known_leaf_control_span=['0x309c00','0x309c32'],
 limits='candidate discovery plus complete original exception fragments, not all indirect aliases, whole logical CFGs or natural initialized reachability')
out.write_text(json.dumps(r,indent=2)+'\n')
print('CAPTURED',len(records),'aligned references in',len(fragments),'fragments; indirect write closure OPEN')
