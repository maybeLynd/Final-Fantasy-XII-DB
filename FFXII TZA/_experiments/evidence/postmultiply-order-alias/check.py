import hashlib,json
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;s=json.loads((W/'source.json').read_text())
b=bytes.fromhex(s['raw_hex']);assert len(b)==349 and hashlib.sha256(b).hexdigest()==s['sha256']
assert s['sha256']=='69b03e9207174ab6f16e5d56817186ec446e5348ab0025255fc8a585d064b726'
assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii=list(cs.disasm(b,0x3977B0));assert sum(i.size for i in ii)==349 and ii[-1].address==0x39790C and ii[-1].mnemonic=='ret'
d={i.address:i for i in ii}
assert [(i.address,i.mnemonic) for i in ii if i.mnemonic=='call']==[(0x3978F9,'call')]
assert d[0x3978F9].operands[0].imm==0x808C40 # not executed, native effect unclaimed
assert d[0x39780A].op_str=='r11d, 4' and d[0x3978E0].op_str=='rax, 4'
assert d[0x3978E4].op_str=='r11, 1' and d[0x3978E8].operands[0].imm==0x397810
assert [(d[p].mnemonic,d[p].op_str) for p in (0x3977CD,0x3977D5,0x3977E6,0x3977F6)]==[
 ('movaps','xmm0, xmmword ptr [rcx]'),('movaps','xmm1, xmmword ptr [rcx + 0x10]'),
 ('movaps','xmm0, xmmword ptr [rcx + 0x20]'),('movaps','xmm1, xmmword ptr [rcx + 0x30]')]
assert [(d[p].mnemonic,d[p].op_str) for p in (0x3977DD,0x3977EE,0x3977FD,0x397805)]==[
 ('movaps','xmmword ptr [rsp], xmm0'),('movaps','xmmword ptr [rsp + 0x10], xmm1'),
 ('movaps','xmmword ptr [rsp + 0x20], xmm0'),('movaps','xmmword ptr [rsp + 0x30], xmm1')]
assert [(d[p].mnemonic,d[p].op_str) for p in (0x3977D0,0x3977D9,0x3977E1,0x3977EA,0x3977F3,0x3977FA,0x397802)]==[
 ('lea','r9, [rsp + 0x10]'),('lea','r8, [rsp]'),('lea','r10, [rsp + 0x10]'),('lea','rax, [rcx + 0x20]'),
 ('sub','r9, rcx'),('sub','r8, rcx'),('sub','r10, rcx')]
loop=[i for i in ii if 0x397810<=i.address<0x3978E0]
reads=[(i.address,o.mem.disp) for i in loop for o in i.operands if o.type==capstone.CS_OP_MEM and cs.reg_name(o.mem.base)=='rdx']
assert len(reads)==16 and {off for _,off in reads}==set(range(0,64,4))
stores=[(i.address,i.operands[0].mem.disp) for i in loop if i.mnemonic=='movss' and i.operands[0].type==capstone.CS_OP_MEM]
assert stores==[(0x39785E,-32),(0x39788F,-16),(0x3978B7,0),(0x3978DB,16)]
# Focused symbolic reduction of ORIGINAL decoded straight-line SSE loop. This is
# a source analysis, not execution of FF12 instructions, nor a reconstructed
# implementation presented as original behavior. Trees preserve sum ordering.
def trees(alias=False):
 out={};right={k:('B',k) for k in range(16)};events=[]
 for col in range(4):
  regs={};ptr={'r8':0x7000,'r9':0x7010,'r10':0x7010,'rax':0x1020+col*4,'rdx':0x2000}
  def expr(op):
   if op.type==capstone.CS_OP_REG:return regs[cs.reg_name(op.reg)]
   assert op.type==capstone.CS_OP_MEM
   mo=op.mem;base=cs.reg_name(mo.base);idx=cs.reg_name(mo.index)
   addr=ptr[base]+(ptr[idx]*mo.scale if idx else 0)+mo.disp
   if base=='rdx':
    k=(addr-0x2000)//4;events.append(dict(column=col,pc=hex(i.address),read_right_word=k));return right[k]
   assert 0x8000<=addr<0x8040 and addr%4==0
   return ('A',(addr-0x8000)//4)
  for i in loop:
   a=i.operands[0];z=i.operands[1]
   if i.mnemonic in ('movss','movaps'):
    if a.type==capstone.CS_OP_REG:regs[cs.reg_name(a.reg)]=expr(z)
    else:
     assert cs.reg_name(a.mem.base)=='rax';word=(ptr['rax']+a.mem.disp-0x1000)//4
     out[word]=expr(z);events.append(dict(column=col,pc=hex(i.address),write_output_word=word))
     if alias:right[word]=out[word]
   else:
    assert i.mnemonic in ('mulss','addss')
    r=cs.reg_name(a.reg);regs[r]=(i.mnemonic,regs[r],expr(z))
 return out,events
out,events=trees();selfout,selfevents=trees(True)
def products(t):
 if t[0]=='addss':return products(t[1])+products(t[2])
 assert t[0]=='mulss';assert t[1][0]=='A' and t[2][0]=='B';return [(t[1][1],t[2][1])]
for word,t in out.items():
 row,col=divmod(word,4)
 assert sorted(products(t))==[(k*4+col,row*4+k) for k in range(4)]
assert len(out)==16
def value(t,A,B):
 if t[0]=='A':return A[t[1]]
 if t[0]=='B':return B[t[1]]
 l=value(t[1],A,B);r=value(t[2],A,B);return l*r if t[0]=='mulss' else l+r
A=[2,0,0,0,0,3,0,0,0,0,4,0,0,0,0,1];B=[1,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
actual=[value(out[k],A,B) for k in range(16)]
oldAB=[sum(A[r*4+k]*B[k*4+c] for k in range(4)) for r in range(4) for c in range(4)]
assert actual[1]==3 and oldAB[1]==2 and actual!=oldAB
M=[1,2,0,0,3,4,0,0,0,0,1,0,0,0,0,1]
square=[value(out[k],M,M) for k in range(16)];alias=[value(selfout[k],M,M) for k in range(16)]
assert [square[k] for k in (0,1,4,5)]==[7,10,15,22]
assert [alias[k] for k in (0,1,4,5)]==[7,22,15,46] and alias!=square
identity=[int(r==c) for r in range(4) for c in range(4)]
assert [value(out[k],identity,identity) for k in range(16)]==identity
# Positive identity is explicitly not evidence distinguishing the two equations.
first=next(j for j,x in enumerate(selfevents) if x.get('write_output_word')==0)
late=next(j for j,x in enumerate(selfevents) if x.get('column')==1 and x.get('read_right_word')==0)
assert first<late and selfevents[first]['pc']=='0x39785e' and selfevents[late]['pc']=='0x397829'
v=dict(status='PASS_STATIC_ONLY',equation='C[4*r+c] = sum_k B[4*r+k]*A[4*k+c]; first three rows sum k1+k0+k2+k3, fourth k0+k1+k2+k3',
 source_sha256=hashlib.sha256(b).hexdigest(),new_original_code_executions=0,live_cases=0,
 conditional_noncommuting=dict(A=A,B=B,actual=actual,rejected_AB=oldAB),conditional_selfalias=dict(input=M,disjoint_square=square,selfalias=alias),
 first_hazard=dict(write=selfevents[first],later_read=selfevents[late]),
 limits='A symbolic source reduction/conditional exact finite values, not original-code execution. Snapshot A only, stable disjoint B sufficient; arbitrary overlaps unclassified. Normal ABI/aligned A/private-frame disjoint. No live caller/ownership/matrix convention/lifetime or cookie native effect.',
 source_trees={str(k):t for k,t in out.items()},conditional_selfalias_trees={str(k):t for k,t in selfout.items()})
if (W/'manifest.json').exists():assert json.loads((W/'validation.json').read_text())==json.loads(json.dumps(v))
else:(W/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
print('PASS A: source equation BA, noncommuting AB rejected, left-only snapshot/selfalias hazard; conditional calculations, zero B/C runs.',flush=True)
