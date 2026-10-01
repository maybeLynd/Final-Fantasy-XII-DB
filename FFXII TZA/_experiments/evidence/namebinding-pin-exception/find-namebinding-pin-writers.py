"""Positive candidate finder, NOT a complete native writer/absence proof.

Use verified body entries, not guessed interior retool dis addresses. A wrong
interior2EADC0 preview decoded a spurious first instruction; no result used it.
Candidates need subsequent original object identity/dataflow qualification.
"""
import hashlib,importlib.util,json,pathlib,sys
import capstone
from capstone.x86_const import X86_OP_MEM
W=pathlib.Path(__file__).resolve().parent
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
S=module('pin_roles',W/'validate-title-source-annotations.py');root=S.ROOT
if hashlib.sha256(S.ADAPTER.read_bytes()).hexdigest()!=S.ADAPTER_SHA:raise ValueError('reviewed adapter changed')
roles=module('actual_pin_adapter',S.ADAPTER)
sys.path.insert(0,str(root/'Database/Tools/analysis-kit/gfz-scripts'))
import retool
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable candidate result exists')
exe=root/'Database/Tools/work/exe/FFXII_TZA.exe';digest=hashlib.sha256(exe.read_bytes()).hexdigest()
if digest!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('reference identity changed')
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
extents=retool.sizes();selected={a:z for a,z in extents.items() if 0x2e2000<=a<0x2ec000};candidates=[];incomplete=[];control=None
for a,z in sorted(selected.items()):
    blob=retool.R.at(a,z);ins=list(cs.disasm(blob,a));decoded=sum(i.size for i in ins)
    if decoded!=len(blob):incomplete.append(dict(start=hex(a),declared_bytes=z,decoded_bytes=decoded,limits='Partial candidate search, no absence claim'))
    for i in ins:
        for k,op in enumerate(i.operands):
            if op.type!=X86_OP_MEM:continue
            role=roles.op_kind(i,op,k)
            if i.address==0x2e25f2:control=dict(pc=hex(i.address),bytes=i.bytes.hex(),text=i.mnemonic+' '+i.op_str,role=role,displacement=op.mem.disp)
            if role not in ['w','rw'] or op.mem.base==capstone.x86_const.X86_REG_RIP:continue
            if not (op.mem.disp<=0x19<op.mem.disp+op.size) or op.mem.disp<0x10:continue
            candidates.append(dict(entry=hex(a),declared_bytes=z,complete_decode=decoded==len(blob),pc=hex(i.address),bytes=i.bytes.hex(),text=i.mnemonic+' '+i.op_str,base=i.reg_name(op.mem.base),index=i.reg_name(op.mem.index),displacement=op.mem.disp,size=op.size,role=role,limits='Offset candidate only; same displacement can belong to another object'))
if not control or control['bytes']!='806219c8' or control['role']!='rw' or control['displacement']!=0x19:raise ValueError('known original mask-write positive control failed')
result=dict(status='VALID_POSITIVE_WRITER_CANDIDATES_ONLY',method='A STATIC_ONLY',exe_sha256=digest,capstone=capstone.__version__,adapter_sha256=S.ADAPTER_SHA,adapter_actual_invocation=True,catalog_extents_sha256=hashlib.sha256(json.dumps(sorted(extents.items()),separators=(',',':')).encode()).hexdigest(),selected_module='002E2000..002EC000',selected_bodies=len(selected),incomplete_bodies=incomplete,positive_control=control,candidates=candidates,driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='No object identity, universal writer coverage, impossibility, semantic acceptance or native/live execution proof')
with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print('Known original mask write detected; positive candidates only:',len(candidates),'incomplete bodies:',len(incomplete))
for c in candidates:
    if c['displacement']==0x19:print(c['entry'],c['pc'],c['text'],c['role'])
