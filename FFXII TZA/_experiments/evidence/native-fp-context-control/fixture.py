"""A tiny owned x64 fixture, not FF12 instructions or a gameplay simulation."""
import hashlib
import json
from pathlib import Path
import struct

SENTINEL = 0x5A17C0DE
MXCSR = 0x3F80
FCW = 0x077F


def seed():
    data = bytearray(0x200)
    for i in range(64):
        struct.pack_into('<f', data, i * 4, (i + 1) / 8)
    struct.pack_into('<I', data, 0x100, MXCSR)
    struct.pack_into('<H', data, 0x104, FCW)
    # Exact powers of two in explicit-integer-bit 80-bit format.
    for i in range(8):
        struct.pack_into('<QH', data, 0x120 + i * 16, 1 << 63, 0x3fff + i)
    return bytes(data)


def make(mode):
    assert mode in ('preserve', 'change')
    p32 = lambda n: struct.pack('<I', n)
    code = bytearray(bytes.fromhex('53 48 81 ec 00 02 00 00 48 89 cb'))
    code += bytes.fromhex('48 0f ae 04 24')  # FXSAVE64 [rsp], aligned caller backup
    code += bytes.fromhex('48 0f ae 83') + p32(0x600)
    for i in range(16):
        code += b'\xf3' + (b'\x44' if i >= 8 else b'')
        code += bytes([0x0f, 0x6f, 0x83 | ((i & 7) << 3)]) + p32(i * 16)
    code += bytes.fromhex('db e3 d9 ab') + p32(0x104)  # FNINIT; FLDCW
    for i in range(8):
        code += bytes.fromhex('db ab') + p32(0x120 + i * 16)  # FLD tbyte
    code += bytes.fromhex('0f ae 93') + p32(0x100)  # LDMXCSR
    code += bytes.fromhex('48 0f ae 83') + p32(0x200)
    gate = len(code)
    code += b'\x90' if mode == 'preserve' else bytes.fromhex('66 0f ef c0')
    code += bytes.fromhex('48 0f ae 83') + p32(0x400)
    code += bytes.fromhex('48 0f ae 0c 24')  # FXRSTOR64 original caller state
    code += bytes.fromhex('48 0f ae 83') + p32(0x800)
    code += b'\xb8' + p32(SENTINEL)
    code += bytes.fromhex('48 81 c4 00 02 00 00 5b c3')
    return bytes(code), gate


def state(raw):
    """Defined FXSAVE64 fields; retain but do not interpret reserved padding."""
    assert len(raw) == 512
    return dict(fcw=struct.unpack_from('<H', raw)[0],
                fsw=struct.unpack_from('<H', raw, 2)[0], ftw=raw[4],
                fop=struct.unpack_from('<H', raw, 6)[0] & 0x7ff,
                fip=struct.unpack_from('<Q', raw, 8)[0],
                fdp=struct.unpack_from('<Q', raw, 16)[0],
                mxcsr=struct.unpack_from('<I', raw, 24)[0],
                mxcsr_mask=struct.unpack_from('<I', raw, 28)[0],
                x87=[raw[32+i*16:42+i*16].hex() for i in range(8)],
                xmm=[raw[160+i*16:176+i*16].hex() for i in range(16)])


def verify_sample(sample, mode, *, allow_fip_truncation=False):
    assert sample['returned'] == SENTINEL, 'missing native sentinel return'
    raw = bytes.fromhex(sample['buffer_hex'])
    assert len(raw) == 0xa00 and raw[:0x200] == seed(), 'seed/extent mismatch'
    before, after, original, restored = [state(raw[n:n+512]) for n in (0x200,0x400,0x600,0x800)]
    assert before['fcw'] == FCW and before['mxcsr'] == MXCSR
    assert before['fsw'] == 0 and before['ftw'] == 255
    assert before['xmm'] == [seed()[i*16:i*16+16].hex() for i in range(16)]
    assert before['x87'] == [seed()[0x120+i*16:0x12a+i*16].hex() for i in reversed(range(8))]
    assert original == restored, 'caller FP restoration mismatch'
    expected = dict(before)
    if mode == 'change':
        expected['xmm'] = ['00'*16] + before['xmm'][1:]
    truncated = after['fip'] != before['fip']
    if allow_fip_truncation and truncated:
        assert before['fip'] > 0xffffffff and after['fip'] == (before['fip'] & 0xffffffff)
        expected['fip'] = after['fip']
    assert after == expected, 'defined FP state changed outside the specified gate'
    assert (before == after) == (mode == 'preserve' and not truncated)
    return dict(before=before, after=after, restored=True, fip_truncated=truncated)


if __name__ == '__main__':
    import capstone
    root = Path(__file__).resolve().parent
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    records = {}
    for mode in ('preserve', 'change'):
        code, gate = make(mode)
        ins = list(md.disasm(code, 0))
        assert sum(i.size for i in ins) == len(code)
        assert ins[0].mnemonic == 'push' and ins[-1].mnemonic == 'ret'
        assert sum(i.mnemonic == 'movdqu' for i in ins) == 16
        assert sum(i.mnemonic == 'fld' for i in ins) == 8
        assert sum(i.mnemonic == 'fxsave64' for i in ins) == 5
        assert sum(i.mnemonic == 'fxrstor64' for i in ins) == 1
        g = next(i for i in ins if i.address == gate)
        assert g.mnemonic == ('nop' if mode == 'preserve' else 'pxor')
        assert not any(i.mnemonic in ('call','jmp','syscall','int3') for i in ins)
        path = root / (mode + '.bin')
        with path.open('xb') as out: out.write(code)
        records[mode] = dict(size=len(code), gate=gate, sha256=hashlib.sha256(code).hexdigest(),
                            instructions=[dict(offset=i.address, bytes=i.bytes.hex(),
                                               text=i.mnemonic+' '+i.op_str) for i in ins])
    with (root/'fixture-decode.json').open('x') as out:
        json.dump(dict(capstone=capstone.__version__, fixtures=records), out, indent=2)
    print('Decoded both complete fixtures; native execution has not occurred.')
