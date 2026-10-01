"""Method A: tie the observer's frame identities to exact shipping instructions."""
import hashlib
import json
import sys
from pathlib import Path
import struct
import capstone

W=Path(__file__).resolve().parent
ROOT=W.parents[4]
EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
raw=EXE.read_bytes();digest=hashlib.sha256(raw).hexdigest()
assert digest=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24;base=struct.unpack_from('<Q',raw,opt+24)[0]
table=opt+struct.unpack_from('<H',raw,pe+20)[0]
def read(address,n):
    for i in range(struct.unpack_from('<H',raw,pe+6)[0]):
        _,rva,size,offset=struct.unpack_from('<IIII',raw,table+i*40+8)
        if rva<=address-base and address-base+n<=rva+size:
            return raw[offset+address-base-rva:offset+address-base-rva+n]
    raise AssertionError('unmapped reference bytes')

prior=json.loads((ROOT/'Database/FFXII TZA/_experiments/evidence/eo3-pointer-observation-preflight/observation.json').read_text())
for body in prior['bodies']:
    b=read(int(body['address'],16),body['bytes'])
    assert b.hex()==body['raw'] and hashlib.sha256(b).hexdigest()==body['sha256']
anchors={0x32e7d4:('push','r14'),0x32e7d6:('sub','rsp, 0x30'),
         0x32e87f:('push','rdi'),0x32e880:('push','r12'),0x32e882:('push','r14'),
         0x32e884:('sub','rsp, 0x20'),0x32e84d:('call','0x32e870'),
         0x377f82:('call','0x32e7b0'),0x32e7b0:('jmp','0x32e7c0'),
         0x32e965:('mov','dword ptr [r10 + 0x64], eax'),0x32e983:('add','rsp, 0x20')}
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);checked=[]
for address,expected in anchors.items():
    i=next(md.disasm(read(address,15),address));assert (i.mnemonic,i.op_str)==expected,(hex(address),i.mnemonic,i.op_str)
    checked.append(dict(address=address,bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
assert next(x for x in checked if x['address']==0x32e84d)['bytes'].startswith('e8')
out=dict(method='A',original_code_executed=False,executable_sha256=digest,capstone=capstone.__version__,anchors=checked,
         producer_parent_return_offset='one push8 + sub30 =38; read [producer RSP+38]',
         builder_parent_rsp='producer RSP - call8 - pushes18 - sub20 = producer RSP-40',
         builder_return_offset='pushes18 + sub20 =38; read [builder RSP+38] ==32E852',
         parent_identity='377F82 calls the tail thunk32E7B0; caller return remains377F87',
         limits=['Static instructions plus synthetic correlation tests do not qualify native capture or game health.'])
if '--write' in sys.argv:
    with (W/'boundaries.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
else:
    assert json.loads((W/'boundaries.json').read_text()) == out, 'recorded evidence differs'
print('Pinned original frame/return boundaries agree; no original code executed.')
