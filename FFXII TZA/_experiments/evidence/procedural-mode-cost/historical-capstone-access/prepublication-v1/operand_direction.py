"""Restricted decoded source roles for the two verified SSE helper bodies.

Not a general x86 access classifier. Preserve provider flags as metadata;
unsupported forms fail closed instead of silently becoming read-only.
"""
import capstone
def memory_role(i,k):
 assert i.operands[k].type==capstone.CS_OP_MEM
 if i.mnemonic=='lea':return 'address'
 if i.mnemonic in ('mov','movaps','movups','movss','movd','movq'):
  assert len(i.operands)==2
  return 'write' if k==0 else 'read'
 if i.mnemonic in ('movsx','movsxd','movzx','mulss'):
  assert k==1
  return 'read'
 raise ValueError('Unsupported source memory form at %x: %s %s'%(i.address,i.mnemonic,i.op_str))
