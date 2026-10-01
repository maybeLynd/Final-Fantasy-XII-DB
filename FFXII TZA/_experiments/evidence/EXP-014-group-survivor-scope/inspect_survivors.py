"""Read-boundary observations for the preserved EXP-012 baseline, not a survivor exemption."""
from pathlib import Path
import hashlib
import importlib.util
import json
import struct
import sys
from collections import Counter

out=Path(__file__).resolve().parent
root=out.parents[4]
sys.path.insert(0,str(root/'Database/Tools/work/ASTRA/python-libs'))
import unicorn
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
reader=out/'initial-instruments/diff_group_completion.py'
spec=importlib.util.spec_from_file_location('captured_group',reader)
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
baseline=out.parent/'EXP-012-mutation-isolation/group-campaign/baseline/differential'
packed=(baseline/'regions.bin').read_bytes()
count=struct.unpack_from('<I',packed,0)[0];offset=4;regions=[]
for i in range(count):
    va,size=struct.unpack_from('<QI',packed,offset);offset+=12
    regions.append((va,bytearray(packed[offset:offset+size])));offset+=size
assert offset==len(packed)
cases=[int(s,16) for s in (baseline/'cases.txt').read_text().splitlines()]
reads=[]
original_uc=d.Uc
def observed_uc(*args,**kwargs):
    uc=original_uc(*args,**kwargs)
    def read(u,access,address,size,value,user):
        reads.append((address,size))
    uc.hook_add(unicorn.UC_HOOK_MEM_READ,read)
    return uc
d.Uc=observed_uc
exe=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe')
rd=d.read_exe(exe)
records,after=d.run_emulated(rd,regions,cases)
assert records==json.loads((baseline/'original-records.json').read_text())
outside=[];image_reads=[];stack_reads=[]
for address,size in reads:
    if any(va<=address and address+size<=va+len(data) for va,data in regions):
        image_reads.append((address,size))
    elif d.STACK_BASE<=address and address+size<=d.STACK_BASE+0x10000:
        stack_reads.append((address,size))
    else:outside.append((address,size))
assert image_reads and stack_reads and not outside
disasm=Cs(CS_ARCH_X86,CS_MODE_64)
instructions={hex(va):[dict(address=i.address,bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str)
                         for i in disasm.disasm(rd(va,size),va)]
              for va,size in [(d.FUNC_VA,d.FUNC_LEN),(d.BKEI_VA,d.BKEI_LEN),(d.LANE_VA,d.LANE_LEN)]}
# These finite predicate controls explain limited distinguishing power, but do not remove
# different-binary survivors from the campaign or award a mutation pass.
arms=[dict(value=a,original=bool(a>=0 and a&1),index64=bool(a>=1 and a&1),index66=bool(a>0 and a&1)) for a in range(-1,256)]
assert all(a['original']==a['index64']==a['index66'] for a in arms)
assert all((hi<<8)>255 and (hi<<9)>255 for hi in range(1,256))
r=dict(status='BASELINE_DATA_READS_WITHIN_EXACT_IMAGE_REGIONS',
       reader_sha256=hashlib.sha256(reader.read_bytes()).hexdigest(),
       script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       reference_sha256=d.REFERENCE_SHA256,unicorn=unicorn.__version__,
       input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [baseline/'regions.bin',baseline/'cases.txt']},
       cases=len(cases),reads=reads,image_reads=len(image_reads),stack_reads=len(stack_reads),
       outside_image_or_stack=outside,instructions=instructions,arm_predicate_controls=arms,
       nonzero_high_bytes_rejected_under_both_shifts=255,
       scope='ret-stub original-code read trace; no native callbacks, C-helper branch coverage, or survivor exemptions')
(out/'survivor-observations.json').write_text(json.dumps(r,indent=2)+'\n')
print(r['status'],len(cases),'calls;',len(image_reads),'data reads;',len(stack_reads),'stack reads')
