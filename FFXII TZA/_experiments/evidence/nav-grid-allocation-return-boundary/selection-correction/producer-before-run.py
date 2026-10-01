"""Focused additive source labels for already-documented arena-selection calls.
Use these labels for this package; original opaque lock/unlock wording is superseded.
"""
import hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'selection-correction';sha=lambda b:hashlib.sha256(b).hexdigest()
CALL_LABELS={0x36C1D0:'push arena/category selection (tail to 0036C1F0)',0x36C1A0:'push auxiliary selection byte',0x36C110:'pop auxiliary selection byte',0x36C140:'pop arena/category selection'}
def label(target):return CALL_LABELS[target]
def verified_labels(labels):
    return labels==CALL_LABELS and all('lock' not in text and 'synchron' not in text for text in labels.values())
def collect():
    R.mkdir(exist_ok=False);(R/'producer-before-run.py').write_bytes(Path(__file__).read_bytes())
    p=W/'retained/shipping-reader.py';sp=importlib.util.spec_from_file_location('rd',p);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image()
    cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
    out=[]
    for a,n in [(0x36C110,38),(0x36C140,84),(0x36C1A0,48),(0x36C1D0,20)]:
        b=rd.img_rd(d,ss,a,n);ii=list(cs.disasm(b,a));assert sum(i.size for i in ii)==n and ii[-1].mnemonic==('jmp' if a==0x36C1D0 else 'ret')
        assert not any(i.mnemonic.startswith('lock ') or i.mnemonic in ('call','xchg','cmpxchg') for i in ii)
        (R/(format(a,'08x')+'.bin')).write_bytes(b)
        out.append(dict(entry=hex(a),bytes=n,sha256=sha(b),label=label(a),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii]))
    wrapper=(W/'retained/wrapper.bin').read_bytes();ii=list(cs.disasm(wrapper,0x384580));calls=[i.operands[0].imm for i in ii if i.mnemonic=='call' and i.operands[0].imm in CALL_LABELS]
    assert calls==[0x36C1D0,0x36C1A0,0x36C110,0x36C140]
    original_labels={a:label(a) for a in calls};wrong=dict(original_labels);wrong[0x36C110]='mutex unlock'
    assert verified_labels(original_labels) and not verified_labels(wrong)
    canon=Path('Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md');b=canon.read_bytes();lines=b.splitlines(keepends=True);i=next(j for j,x in enumerate(lines) if b'The allocation wrappers never take an arena argument.' in x);kept=b''.join(lines[i:i+54]);(R/'known-selection-primary.md').write_bytes(kept)
    r=dict(exe_sha256=sha(d),producer_sha256=sha(Path(__file__).read_bytes()),bodies=out,wrapper_calls=[dict(target=hex(a),label=label(a)) for a in calls],procedure_controls=dict(default_verified=verified_labels(original_labels),wrong_mutex_label_rejected=not verified_labels(wrong)),known_primary=dict(path=canon.as_posix(),full_source_sha256=sha(b),retained_sha256=sha(kept)),limits='Existing documented stack semantics reused, not a new discovery/census. Exact local helpers and tail target support selection labels, not wholeallocator synchronization/thread safety/no locks/atomicity or whole tail target effects. Original null-v-nonnull conditional paths remain valid with returning conforming opaque callees; original lock/unlock terms withdrawn.')
    (R/'result.json').write_text(json.dumps(r,indent=2)+'\n');print('CAPTURE_SELECTION_LABEL_CORRECTION default label table rejects mutex label; original source, no runtime execution')
if __name__=='__main__':collect()
