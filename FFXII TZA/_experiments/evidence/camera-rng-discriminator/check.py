"""ASTRA method-A camera/RNG observer preflight; no native or live execution.

Pin shipping identity and retain exact caller/eligibility/scheduling code before
deciding what a live occupancy or cursor measurement could discriminate.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

import capstone
from capstone.x86 import X86_OP_IMM

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
EXE_HASH = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
BODIES = {
    0x263ff0: (21, 'slot getter'),
    0x314370: (85, 'five-slot camera update and view publish'),
    0x3dcfb0: (285, 'four-driver eligibility and evaluation'),
    0x37d1f0: (712, 'sampler entry sentinel and existing float calls'),
    0x3dcf60: (70, 'clear drivers'),
    0x3dd230: (225, 'start driver from authored bank'),
    0x22a770: (2001, 'field-frame scheduling'),
    0x22b8c0: (856, 'update-and-render scheduling'),
}


def collect(path):
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == EXE_HASH, 'wrong original executable'
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    assert data[pe:pe + 4] == b'PE\0\0'
    opt = pe + 24
    assert struct.unpack_from('<H', data, opt)[0] == 0x20b
    base = struct.unpack_from('<Q', data, opt + 24)[0]
    assert base == 0x120000
    table = opt + struct.unpack_from('<H', data, pe + 20)[0]
    count = struct.unpack_from('<H', data, pe + 6)[0]
    sections = [struct.unpack_from('<IIII', data, table + i * 40 + 8) for i in range(count)]

    def read(va, size):
        assert size > 0, 'empty body is not evidence'
        rva = va - base
        for _, start, length, offset in sections:
            if start <= rva and rva + size <= start + length:
                return data[offset + rva - start:offset + rva - start + size]
        raise ValueError(f'not file-backed: {va:08X}+{size:X}')

    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    result = {}
    for va, (size, role) in BODIES.items():
        raw = read(va, size)
        ins = list(md.disasm(raw, va))
        assert ins and sum(i.size for i in ins) == size, 'incomplete decode'
        calls = [{'site': f'{i.address:08X}', 'target': f'{i.operands[0].imm:08X}'} for i in ins
                 if i.mnemonic in ('call', 'jmp') and i.operands[0].type == X86_OP_IMM]
        result[f'{va:08X}'] = dict(bytes=size, role=role, sha256=hashlib.sha256(raw).hexdigest(),
                                 raw_hex=raw.hex(), direct_transfers=calls,
                                 disassembly=[f'{i.address:08X} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in ins])
    # Positive population controls, using independently recorded direct caller sites.
    outer = result['00314370']
    assert outer['sha256'] == '3213b13bf8c8acae8fea9773e24cde1bea29a4b29c5f0d3a756f740a4c41252a'
    assert {'site': '00314385', 'target': '00263FF0'} in outer['direct_transfers']
    assert {'site': '00314396', 'target': '003DA050'} in outer['direct_transfers']
    assert {'site': '0031439E', 'target': '003DCFB0'} in outer['direct_transfers']
    sites = {k: [r['site'] for r in result[k]['direct_transfers'] if r['target'] == '00314370']
             for k in ('0022A770', '0022B8C0')}
    assert [len(v) for v in sites.values()] == [3, 2]
    # These branches change what a live observer must count, so pin their original
    # instructions rather than relying on decoded labels or an occupancy formula.
    for body, lines in {
        '00263FF0': ['00263FFA 4869c088020000 imul rax, rax, 0x288'],
        '00314370': ['0031438D f6401001 test byte ptr [rax + 0x10], 1',
                     '003143A5 83fb05 cmp ebx, 5'],
        '003DCFB0': ['003DCFCB 4885db test rbx, rbx',
                     '003DCFCE 0f84f0000000 je 0x3dd0c4',
                     '003DD044 66833b00 cmp word ptr [rbx], 0',
                     '003DD065 8b53f8 mov edx, dword ptr [rbx - 8]',
                     '003DD06B e88001faff call 0x37d1f0',
                     '003DD0B0 83ff04 cmp edi, 4'],
        '0037D1F0': ['0037D21F 83faff cmp edx, -1',
                     '0037D222 751a jne 0x37d23e',
                     '0037D224 c786e800000002000000 mov dword ptr [rsi + 0xe8], 2',
                     '0037D23D c3 ret '],
    }.items():
        assert all(line in result[body]['disassembly'] for line in lines), body + ' gate mismatch'
    return dict(method='A: shipping instructions; no execution or live occupancy claim',
                executable_sha256=EXE_HASH, image_base=base, capstone_version=capstone.__version__,
                bodies=result, camera_update_static_call_sites=sites)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--exe', type=Path, default=ROOT / 'Database/Tools/work/exe/FFXII_TZA.exe')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    result = collect(args.exe)
    target = HERE / 'original-code.json'
    if args.write:
        assert not target.exists(), 'do not overwrite retained evidence'
        target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    else:
        assert json.loads(target.read_text(encoding='utf-8')) == result, 'retained bytes/decoding changed'
    print('Verified original identity and', len(result['bodies']), 'complete recorded body spans.')
    print('Static camera-update sites:', json.dumps(result['camera_update_static_call_sites']))
    print('This is static site count, NOT executed calls per frame or live RNG consumption.')


if __name__ == '__main__':
    main()
