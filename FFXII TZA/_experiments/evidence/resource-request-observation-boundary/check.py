"""Method A: original instruction/ABI boundaries and calculated examples only."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import capstone

E=Path(__file__).resolve().parent
R=E.parents[4]
sys.path.insert(0,str(R/'Database/Tools/analysis-kit/gfz-scripts'))
from disasm_fn import Image
EXE='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda b:hashlib.sha256(b).hexdigest()


def analyze():
    image=Image(R/'Database/Tools/work/exe/FFXII_TZA.exe')
    assert sha(image.d)==EXE and image.base==0x120000
    prior_path=E.parent/'eo3-pointer-observation-preflight/observation.json'
    prior=json.loads(prior_path.read_text())
    assert prior['executable_sha256']==EXE
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
    bodies,ins=[],{}
    for address,size in [(0x32E400,80),(0x32E620,340),(0x32E7C0,173),(0x32E870,285),(0x32E070,605)]:
        raw=image.read(address,size);assert raw and len(raw)==size
        decoded=list(md.disasm(raw,address));assert decoded and sum(i.size for i in decoded)==size
        reused=next((b for b in prior['bodies'] if int(b['address'],16)==address),None)
        if reused: assert raw.hex()==reused['raw'] and sha(raw)==reused['sha256']
        rows=[dict(address=f'{i.address:08X}',bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in decoded]
        ins.update({i.address:(i.mnemonic,i.op_str) for i in decoded})
        bodies.append(dict(address=f'{address:08X}',bytes=size,raw=raw.hex(),sha256=sha(raw),
                           reused_prior_body=bool(reused),instructions=rows))
    anchors={
      0x32E41F:('cmp','rdx, 0x400'),0x32E428:('mov','eax, dword ptr [r8 + rdx*4]'),
      0x32E438:('or','eax, 0xffffffff'),
      0x32E64A:('test','edx, edx'),0x32E64C:('jns','0x32e656'),
      0x32E64E:('or','eax, 0xffffffff'),0x32E651:('jmp','0x32e75e'),
      0x32E7DA:('mov','r14, rdx'),0x32E7DD:('mov','rbx, rcx'),
      0x32E7E5:('mov','rsi, r9'),0x32E7E8:('mov','ebp, r8d'),
      0x32E800:('cmp','byte ptr [rbx + rax + 1], 0'),
      0x32E833:('mov','r9d, ebp'),0x32E83E:('mov','r8, r14'),
      0x32E846:('mov','edx, edi'),0x32E848:('mov','ecx, 0xff'),
      0x32E84D:('call','0x32e870'),
      0x32E8DB:('mov','eax, dword ptr [rcx]'),0x32E8FB:('cdq',''),
      0x32E8FC:('and','edx, 0x7ff'),0x32E90B:('add','eax, edx'),
      0x32E913:('and','eax, 0xfffff800'),0x32E918:('mov','dword ptr [r10 + 0x2c], eax'),
      0x32E88A:('mov','esi, r9d'),0x32E92C:('mov','dword ptr [r10 + 0x28], esi'),
      0x32E721:('mov','eax, dword ptr [rcx + 0x2c]'),0x32E724:('cdq',''),
      0x32E725:('mov','qword ptr [rcx], r14'),0x32E728:('and','edx, 0x7ff'),
      0x32E72E:('add','eax, edx'),0x32E730:('and','eax, 0xfffff800'),
      0x32E735:('mov','dword ptr [rcx + 0x2c], eax'),
      0x32E0CA:('mov','r8d, dword ptr [rbx + 0x28]'),0x32E0CE:('test','r8d, r8d'),
      0x32E0D1:('je','0x32e130'),0x32E133:('call','0x32e330'),0x32E13F:('call','0x32ec40'),
      0x32E943:('mov','byte ptr [r10 + 0x21], r14b'),0x32E965:('mov','dword ptr [r10 + 0x64], eax'),
      0x32E8C9:('call','0x32e990'),0x32E8D3:('mov','r10, rax'),
      0x32E974:('mov','dword ptr [r10 + 0x5c], 0'),
    }
    for address,expected in anchors.items():assert ins[address]==expected,(hex(address),ins[address],expected)
    examples=[]
    values=[0,1,0x7FF,0x800,0x801,0xFFF,0x1000,-1,-0x7FF,-0x800,-0x801,-0xFFF,-0x1000,-0x80000000,0x7FFFFFFF]
    for signed in values:
        bits=signed & 0xFFFFFFFF
        bias=0x7FF if bits & 0x80000000 else 0
        observed=((bits+bias)&0xFFFFFFFF)&0xFFFFF800
        mathematical=(abs(signed)//0x800)*0x800*(-1 if signed<0 else 1)
        assert observed==mathematical & 0xFFFFFFFF
        examples.append(dict(input=signed,input_hex=f'{bits:08X}',bias=bias,
                             result_hex=f'{observed:08X}',signed_result=mathematical))
    by_value={r['input']:r for r in examples}
    assert by_value[0x801]['signed_result']==0x800
    assert by_value[-0x801]['signed_result']==-0x800
    assert by_value[0x800]['signed_result']==0x800 and by_value[-1]['signed_result']==0
    return dict(method='A: complete original bodies, exact anchors and calculated arithmetic examples; no execution',
                executable_sha256=EXE,capstone=capstone.__version__,bodies=bodies,
                prior_eo3_sha256=sha(prior_path.read_bytes()),anchors_checked=len(anchors),
                offset_examples=examples,limits=['No FF12 or isolated machine-code execution.',
                'Counterexamples are calculations of the displayed instruction sequence, not live values.',
                'No claim about which nonaligned offsets occur during ordinary gameplay.',
                'No request arrival, completion, caller scheduling or global absence was observed.'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();r=analyze()
    if a.write:
        with (E/'observation.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
    else:
        retained=json.loads((E/'observation.json').read_text())
        assert r==retained,'Retained observation differs from current original-code analysis'
    print(f'Verified {len(r["bodies"])} complete original bodies, {r["anchors_checked"]} anchors and {len(r["offset_examples"])} calculated boundaries against the retained observation. Offset 0x801 becomes 0x800; -0x801 becomes -0x800. Slot +0x5C has a dword zero write. No execution.')
