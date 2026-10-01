"""Bounded adapter to the EXISTING pinned reg_tracking.op_kind policy.

No parallel access classifier. Preserve raw provider metadata, restrict this
capture to its verified vocabulary and reject unknown roles/forms.
"""
import capstone,hashlib,importlib.util
from pathlib import Path
P=Path(__file__).resolve().parent/'retained/reg_tracking.py'
assert hashlib.sha256(P.read_bytes()).hexdigest()=='5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38'
spec=importlib.util.spec_from_file_location('pinned_role_policy',P)
policy=importlib.util.module_from_spec(spec);spec.loader.exec_module(policy)
POLICY_ID=dict(commit='8e15ad96d35d3f6bf17e93919b266d3995ce8ce4',path='Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py',sha256=hashlib.sha256(P.read_bytes()).hexdigest(),api='op_kind',retained='retained/reg_tracking.py')
def memory_role(i,k):
 assert i.operands[k].type==capstone.CS_OP_MEM
 if i.mnemonic not in ('lea','mov','movaps','movups','movss','movd','movq','movsx','movsxd','movzx','mulss'):
  raise ValueError('Unsupported capture-profile form at %x: %s %s'%(i.address,i.mnemonic,i.op_str))
 role=policy.op_kind(i,i.operands[k],k)
 if role not in ('addr','r','w','rw'):raise ValueError('Unknown canonical role at %x'%i.address)
 return {'addr':'address','r':'read','w':'write','rw':'readwrite'}[role]
