import json,struct
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';U=lambda b,o:struct.unpack_from('<I',b,o)[0]
diag=[]
for m in [x for x in ['ctrl','btlctrl','evctrl','mapctrl'] if (R/(x+'.ebp')).exists()]:
 b=(R/(m+'.dbg')).read_bytes();e=(R/(m+'.ebp')).read_bytes();base=U(e,0x10);D=base+U(e,base+0x18);ns=U(b,U(b,0));offs=struct.unpack_from('<%dI'%(4*ns+1),b,U(b,0)+4)
 for sc in range(ns):
  ent=struct.unpack_from('<IHHIIIIIIHH',e,D+4+48*sc);q0,q1,q2,q3=offs[4*sc:4*sc+4];n=(q1-q0)//4
  nonzero=[j for j in range(n) if b[q0+4*j:q0+4*j+4]!=b'\0'*4];length=max(nonzero)+1;start=base+ent[3];pc=0;flags=[];ops=[]
  while pc<length:
   op=e[start+pc];size=1 if op<0x48 else 3;ops.append((pc,op,size));flags.extend([1]+[0]*(size-1));pc+=size
  actual=[b[q0+4*j+3] for j in range(length)];bad=[j for j in range(min(len(flags),len(actual))) if flags[j]!=actual[j]]
  if bad:
   j=bad[0];row=dict(module=m,scope=sc,first_mismatch=j,q0_bytes=n,inferred_length=length,start=start,directory_instruction_count=ent[4],q0_instruction_count=sum(actual),preceding_code=e[start+max(0,j-8):start+j+12].hex(),preceding_records=b[q0+4*max(0,j-8):q0+4*(j+12)].hex(),preceding_ops=[x for x in ops if j-8<=x[0]<=j+12]);diag.append(row);print(row)
assert diag
(W/'diagnostic.json').write_text(json.dumps(diag,indent=2)+'\n')
