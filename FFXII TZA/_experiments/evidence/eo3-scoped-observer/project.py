"""Required AMD64 GPR projection from a successful captured context read only."""
import struct

OFFSETS=dict(rax=0x78,rcx=0x80,rdx=0x88,rbx=0x90,rsp=0x98,
             rdi=0xb0,r8=0xb8,r9=0xc0,r10=0xc8,rip=0xf8)
REQUIRED=0x100003  # AMD64, CONTROL, INTEGER; DEBUG alone supplies no GPR evidence.


def project(row):
    assert row['operation']=='full_context' and row['api']=='GetThreadContext' and row['result']==1
    assert row['requested_flags']&REQUIRED==REQUIRED,'required GPR groups not requested'
    raw=bytes.fromhex(row['context_hex'])
    assert row['size']==len(raw)==1232
    flags=struct.unpack_from('<I',raw,0x30)[0]
    assert flags&REQUIRED==REQUIRED,'required GPR groups not returned'
    return {name:struct.unpack_from('<Q',raw,offset)[0] for name,offset in OFFSETS.items()}
