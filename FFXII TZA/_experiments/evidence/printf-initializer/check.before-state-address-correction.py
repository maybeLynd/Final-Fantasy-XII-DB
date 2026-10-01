"""Bounded Method-A extraction/replay; never loads or executes native FF12 code."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys

import capstone
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

E = Path(__file__).resolve().parent
ROOT = E.parents[4]
EXE = ROOT / 'Database/Tools/work/exe/FFXII_TZA.exe'
EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
HELPER = ROOT / 'Database/Tools/analysis-kit/gfz-scripts/ext_string_probe.py'
sys.path.insert(0, str(HELPER.parent))
from ext_string_probe import sections

BASE = 0x120000
CODE = {0x16D670: 8, 0x18A320: 8, 0x194EF0: 89, 0x808D4C: 16,
        0x808D78: 0x16C, 0x808EE4: 18, 0x809C50: 27,
        0x862022: 6, 0x86201C: 6}
sha = lambda b: hashlib.sha256(b).hexdigest()


def disasm(raw, va):
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    ins = list(md.disasm(raw, va))
    assert ins and sum(i.size for i in ins) == len(raw), ('incomplete decode', hex(va))
    return ins


def extract():
    b = EXE.read_bytes()
    assert sha(b) == EXE_SHA
    secs = sections(b)
    p = struct.unpack_from('<I', b, 60)[0]
    opt = p + 24
    assert b[p:p+4] == b'PE\0\0'
    assert struct.unpack_from('<H', b, opt)[0] == 0x20B
    assert struct.unpack_from('<Q', b, opt+24)[0] == BASE
    table = opt + struct.unpack_from('<H', b, p+20)[0]
    chunks = {}

    def get(va, n):
        for name, off, size, start in secs:
            if start <= va and va+n <= start+size:
                pos = off+va-start
                raw = b[pos:pos+n]
                assert len(raw) == n
                return raw, pos, name
        raise ValueError(('not wholly raw-backed', hex(va), n))

    def keep(va, n):
        raw, off, name = get(va, n)
        key = f'{va:08X}'
        item = dict(va=va, file_offset=off, section=name, raw=raw.hex(), sha256=sha(raw))
        if key in chunks:
            assert chunks[key] == item
        chunks[key] = item
        return raw

    def string(va):
        # Read only the actual terminated string, including near section end.
        out = bytearray()
        for i in range(256):
            out += get(va+i, 1)[0]
            if out[-1] == 0:
                keep(va, len(out))
                return out[:-1].decode('ascii')
        raise ValueError(('unterminated import name', hex(va)))

    for va, n in CODE.items():
        keep(va, n)
    keep(0x8C5680, 40)
    imports = []
    imp, size = struct.unpack_from('<II', b, opt+120)
    for rva in range(imp, imp+size, 20):
        descriptor = get(BASE+rva, 20)[0]
        ilt, timestamp, forwarder, name, iat = struct.unpack('<IIIII', descriptor)
        if not any((ilt, timestamp, forwarder, name, iat)):
            break
        # Only retain the three named imports and their exact lookup/IAT records.
        for j in range(4096):
            lookup = BASE+(ilt or iat)+j*8
            value = struct.unpack('<Q', get(lookup, 8)[0])[0]
            if not value:
                break
            slot = BASE+iat+j*8
            if slot in (0x8C2DB8, 0x8C2D20, 0x8C2E88):
                assert not value >> 63
                keep(BASE+rva, 20)
                keep(lookup, 8)
                keep(slot, 8)
                keep(BASE+value, 2)
                imports.append(dict(slot=slot, descriptor=BASE+rva, lookup=lookup,
                                    dll=string(BASE+name), symbol=string(BASE+value+2)))
        else:
            raise ValueError('unterminated import lookup')
    else:
        raise ValueError('unterminated import directory')

    storage = []
    for va in (0x2EBA3D0, 0x1F7F5B0, 0x2EAECF4):
        for j in range(struct.unpack_from('<H', b, p+6)[0]):
            q = table+40*j
            virtual, rva, raw_size, off = struct.unpack_from('<IIII', b, q+8)
            if BASE+rva <= va and va+8 <= BASE+rva+virtual:
                storage.append(dict(va=va, section=b[q:q+8].rstrip(b'\0').decode(),
                                    section_va=BASE+rva, virtual_size=virtual,
                                    raw_size=raw_size, raw_end=BASE+rva+raw_size,
                                    zero_fill=va >= BASE+rva+raw_size))
                break
        else:
            raise ValueError(('storage outside virtual sections', hex(va)))

    headers_size = struct.unpack_from('<I', b, opt+60)[0]
    return dict(method='A: offline shipping-image extraction; no code execution',
                executable_sha256=sha(b), image_base=BASE,
                entry=BASE+struct.unpack_from('<I', b, opt+16)[0],
                headers=b[:headers_size].hex(), headers_sha256=sha(b[:headers_size]),
                tool=dict(python=sys.version, capstone=capstone.__version__,
                          sections_helper_sha256=sha(HELPER.read_bytes())),
                chunks=chunks, imports=imports, storage=storage)


def verify(d):
    assert d['method'] == 'A: offline shipping-image extraction; no code execution'
    assert d['executable_sha256'] == EXE_SHA and d['image_base'] == BASE
    assert d['entry'] == 0x808EE4
    assert sha(bytes.fromhex(d['headers'])) == d['headers_sha256']
    all_ins = {}
    for va, n in CODE.items():
        c = d['chunks'][f'{va:08X}']
        raw = bytes.fromhex(c['raw'])
        assert c['va'] == va and len(raw) == n and sha(raw) == c['sha256']
        all_ins.update({i.address: i for i in disasm(raw, va)})

    def exact(va, raw):
        assert all_ins[va].bytes.hex() == raw, ('changed instruction', hex(va))

    def rip(va):
        i = all_ins[va]
        operands = [x for x in i.operands if x.type == X86_OP_MEM and x.mem.base == X86_REG_RIP]
        assert len(operands) == 1
        return i.address+i.size+operands[0].mem.disp

    def direct(va, mnemonic, target):
        i = all_ins[va]
        assert i.mnemonic == mnemonic and i.operands[0].imm == target

    assert rip(0x16D670) == 0x2EBA3D0 and rip(0x18A320) == 0x1F7F5B0
    direct(0x809C54, 'call', 0x16D670)
    exact(0x809C59, '48830804')  # OR qword [RAX], 4; not assignment.
    direct(0x809C5D, 'call', 0x18A320)
    exact(0x809C62, '48830802')  # Separate scanf option word.
    direct(0x808D50, 'call', 0x809C50)
    exact(0x808D55, '33c0')
    exact(0x808D5B, 'c3')
    direct(0x808EF1, 'jmp', 0x808D78)
    assert rip(0x808DD4) == 0x8C5680 and rip(0x808DCD) == 0x8C56A0
    direct(0x808DDB, 'call', 0x862022)
    assert rip(0x862022) == 0x8C2DB8
    exact(0x808DE0, '85c0')
    direct(0x808DE2, 'je', 0x808DEE)
    exact(0x808DE4, 'b8ff000000')
    assert rip(0x808DF5) == 0x8C31D0 and rip(0x808DEE) == 0x8C5678
    direct(0x808DFC, 'call', 0x86201C)
    assert rip(0x86201C) == 0x8C2D20
    state = {rip(a) for a in (0x808DAA, 0x808DC3, 0x808E01)}
    assert state == {0x2EAECF4}
    direct(0x808E8A, 'call', 0x7A3770)
    direct(0x194F11, 'call', 0x16D670)
    exact(0x194F30, '488b08')
    assert rip(0x194F33) == 0x8C2E88
    table = bytes.fromhex(d['chunks']['008C5680']['raw'])
    assert len(table) == 40
    assert struct.unpack('<5Q', table) == (0, 0x808C90, 0x808D4C, 0x809124, 0)
    names = {r['slot']: r['symbol'] for r in d['imports']}
    assert names == {0x8C2DB8: '_initterm_e', 0x8C2D20: '_initterm',
                     0x8C2E88: '__stdio_common_vswprintf_s'}
    assert len(d['storage']) == 3 and all(s['zero_fill'] for s in d['storage'])
    return dict(verdict='STATIC_ROUTE_AND_OR_MASK_VERIFIED',
                printf_options_address='02EBA3D0', printf_initializer='00809C50',
                printf_effect='old_qword OR 4; zero input gives 4, not a sampled live value',
                registration='008C5690 -> 00808D4C -> 00809C50',
                startup='PE entry -> 00808D78 -> C table through _initterm_e before C++ table/game entry',
                scanf_effect='separate 01F7F5B0 qword OR 2',
                startup_state_address='02EAECF4; 026A5EED is only a displacement',
                live_observation=False, original_code_execution=False,
                limitations=['No exhaustive writer census or live initialized-word sample.',
                             'Ordering follows the imported standard CRT initializer walker.',
                             'Startup failure/reentry branches and omitted earlier DLL work are distinct.',
                             'Does not repair the returned-stack pointer lifetime or close UQ146.'])


def mutations(d):
    results = []
    for name in ('wrong-mask', 'wrong-registration', 'wrong-getter-global', 'wrong-import'):
        m = copy.deepcopy(d)
        if name == 'wrong-import':
            m['imports'][0]['symbol'] = 'wrong_function'
        else:
            key, offset, value = {'wrong-mask': ('00809C50', 12, 2),
                                  'wrong-registration': ('008C5680', 16, 0),
                                  'wrong-getter-global': ('0016D670', 3, 0)}[name]
            c = m['chunks'][key]
            raw = bytearray.fromhex(c['raw'])
            assert raw[offset] != value
            raw[offset] = value
            c['raw'], c['sha256'] = raw.hex(), sha(raw)
        try:
            verify(m)
        except (AssertionError, ValueError, KeyError):
            results.append(dict(case=name, rejected=True))
        else:
            raise AssertionError(('accepted corrupt evidence', name))
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--capture', action='store_true')
    ap.add_argument('--mutations', action='store_true')
    args = ap.parse_args()
    if args.capture:
        d = extract()
        verify(d)
        with (E/'reference.json').open('x', encoding='utf-8') as f:
            json.dump(d, f, indent=2); f.write('\n')
    d = json.loads((E/'reference.json').read_text())
    current = extract()
    # Runtime patch version can differ; exact binary/chunks/headers/dependency may not.
    current['tool']['python'] = d['tool']['python']
    assert current == d, 'reference/tool extraction differs'
    result = verify(d)
    if args.mutations:
        result['receipt_mutations'] = mutations(d)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
