"""Static correction: one pre-call stop retains original and staged pointers."""
import argparse
import hashlib
import json
from pathlib import Path
import capstone

E=Path(__file__).resolve().parent;ROOT=E.parents[4]
prior=ROOT/'Database/FFXII TZA/_experiments/evidence/eo3-pointer-observation-preflight/observation.json'
d=json.loads(prior.read_text());body=next(b for b in d['bodies'] if int(b['address'],16)==0x32e7c0)
raw=bytes.fromhex(body['raw']);assert hashlib.sha256(raw).hexdigest()==body['sha256']
begin=0x32e846-int(body['address'],16);staging=raw[begin:begin+7]
assert staging.hex()=='8bd7b9ff000000'
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
ins=list(md.disasm(staging,0x32e846))
assert [(i.address,i.mnemonic,i.op_str) for i in ins]==[(0x32e846,'mov','edx, edi'),(0x32e848,'mov','ecx, 0xff')]
assert ins[-1].address+ins[-1].size==0x32e84d
effects=[]
for i in ins:
    reads,writes=i.regs_access();names=[i.reg_name(r) for r in writes]
    assert not set(names)&{'rdi','edi','di','dil'}
    effects.append(dict(address=i.address,bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str,
                        reads=[i.reg_name(r) for r in reads],writes=names))
out=dict(method='A - exact shipping instruction analysis',original_code_executed=False,live_game=False,
         reference_executable_sha256=d['executable_sha256'],body_sha256=body['sha256'],
         source_observation_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),capstone=capstone.__version__,
         effects=effects,
         established='Immediately before 0032E84D executes, RDI still holds P, RDX is zero_extend(low32(P)), and ECX is FF. Neither intervening instruction writes RDI. One stopped full-GPR observation can compare P and the staged low half.',
         affected='FABLE resource queue EO3 table says RDI at0032E846 is the only place the original exists and a trace needs both sites. Those requirements are false for this verified sequence.',
         limits=['No actual allocator value, caller or queue issuance observed.',
                 'A call-boundary hit still does not prove call execution/completion.',
                 'This corrects the necessary observation sites; it does not establish historical crash cause.'])
parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
if args.write:
    with (E/'staging.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
else:assert json.loads((E/'staging.json').read_text())==out
print('Original staging writes EDX/ECX only: RDI and staged low32 coexist at0032E84D; no execution.')
