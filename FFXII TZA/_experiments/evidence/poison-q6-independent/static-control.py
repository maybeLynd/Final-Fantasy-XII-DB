import hashlib,json
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;P=W/'private-source';code=(P/'stage2-00386c70.bin').read_bytes();start=0x386c70;gate=0x386f95;ret=0x387016
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
def analyze(code):
 ii={i.address:i for i in cs.disasm(code,start)};edges={}
 assert sum(i.size for i in ii.values())==len(code) and [a for a,i in ii.items() if i.mnemonic=='ret']==[ret]
 for a,i in ii.items():
  if i.mnemonic=='ret':edges[a]=[]
  elif i.mnemonic=='jmp':edges[a]=[int(i.op_str,16)]
  elif i.mnemonic.startswith('j'):edges[a]=[int(i.op_str,16),a+i.size]
  else:edges[a]=[a+i.size]
 assert all(x in ii for row in edges.values() for x in row),'out-of-body/unknown branch'
 def path(omit):
  todo=[start];seen={start:None}
  for a in todo:
   if a==ret:
    out=[]
    while a is not None:out.append(hex(a));a=seen[a]
    return out[::-1]
   for n in edges[a]:
    if n!=omit and n not in seen:seen[n]=a;todo.append(n)
  return None
 return {'gate':hex(gate),'ret':hex(ret),'reachable_return':path(None) is not None,'return_path_omitting_gate':path(gate),'instruction_count':len(ii),'calls_assumed_to_return':True}
original=analyze(code);assert original['reachable_return'] and original['return_path_omitting_gate'] is None
mut=bytearray(code);off=0x386f85-start;assert mut[off:off+2]==bytes.fromhex('730e');mut[off+1]=0x73
control=analyze(bytes(mut));assert control['return_path_omitting_gate'] is not None
(P/'labelled-critical-skip-mutation.bin').write_bytes(mut)
result={'method':'A byte-derived local control-flow graph; no mutated machine-code execution','original':original,'control':control,'mutation':{'site':'0x386f85','original':'730e','labelled':'7373','effect':'bit8 clear can bypass critical comparison to epilogue at386FFA','original_byte_binding_refuses':hashlib.sha256(mut).hexdigest()!=hashlib.sha256(code).hexdigest()},'limits':'Direct in-body edges, calls treated returning; not proof of live invocation/fault/nonreturning callbacks'}
(W/'static-control.json').write_text(json.dumps(result,indent=2)+'\n');print('STATIC_GATE_POSTDOMINATES_NORMAL_RETURN_AND_SKIP_CONTROL_DETECTED')
