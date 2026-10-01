"""ASTRA: reproduce the S-44 proposed-rebind preflight from shipping file bytes.

Method A only. No game execution, process access, settings edits or derived live claim.
Run from any cwd: python check.py [--exe PATH] [--write]. Default checks retained output.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import struct

import capstone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
EXPECTED = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def collect(path):
    data = path.read_bytes()
    assert sha(data) == EXPECTED, 'wrong executable identity'
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    assert data[pe:pe + 4] == b'PE\0\0'
    n, optlen = struct.unpack_from('<H', data, pe + 6)[0], struct.unpack_from('<H', data, pe + 20)[0]
    opt = pe + 24
    assert struct.unpack_from('<H', data, opt)[0] == 0x20b
    base = struct.unpack_from('<Q', data, opt + 24)[0]
    assert base == 0x120000
    sections = [struct.unpack_from('<IIII', data, opt + optlen + i * 40 + 8) for i in range(n)]
    raw = {}

    def read(va, size):
        rva = va - base
        for _, start, count, offset in sections:
            if start <= rva and rva + size <= start + count:
                return data[offset + rva - start:offset + rva - start + size]
        raise ValueError(f'not file backed: {va:08X}+{size:X}')

    def string(va):
        result = bytearray()
        for i in range(256):
            byte = read(va + i, 1)
            if byte == b'\0':
                return result.decode('ascii')
            result += byte
        raise ValueError('unterminated name')

    def span(name, va, count):
        b = read(va, count)
        raw[name] = b
        return {'va': f'{va:08X}', 'bytes': count, 'sha256': sha(b), 'hex': b.hex()}

    tables = {}
    for name, va, count in [('value_a', 0x1dfda10, 81), ('value_b', 0x1dfdb60, 81),
                            ('value_c', 0x1dfdcb0, 81), ('keymap_buttons', 0x1df09c0, 48),
                            ('keymap_axis_records', 0x1df0a80, 192), ('keymap_extra', 0x1df1470, 4)]:
        tables[name] = span(name, va, count * 4)
        tables[name]['u32'] = list(struct.unpack('<' + 'I' * count, raw[name]))
    registry_path = ROOT / 'Database/FFXII TZA/15-Input/Input-Name-Registry/input-name-registry.tsv'
    registry_source = registry_path.read_bytes()
    nodes = []
    for row in csv.DictReader(registry_source.decode('utf-8-sig').splitlines(), delimiter='\t'):
        va = int(row['node'], 16)
        b = read(va, 32)
        type_ptr, name_ptr, next_ptr, value = struct.unpack('<QQQi', b[:28])
        name = string(name_ptr)
        assert name == row['name'] and type_ptr == int(row['type_ptr'], 16)
        nodes.append({'registry': row['registry'], 'node': row['node'], 'type_ptr': f'{type_ptr:08X}',
                      'name_ptr': f'{name_ptr:08X}', 'name': name, 'value': value,
                      'next': next_ptr, 'hex': b.hex(), 'name_hex': read(name_ptr, len(name) + 1).hex()})
    assert len(nodes) == 240 and len({r['node'] for r in nodes}) == 240
    by_name = {r['name']: r for r in nodes if r['registry'] == '00876C80'}
    assert len(by_name) == 97
    assert [(name, by_name[name]['value']) for name in ('Key_A', 'Key_B', 'Key_Enter', 'Key_Up')] == [
        ('Key_A', 28), ('Key_B', 29), ('Key_Enter', 77), ('Key_Up', 93)]
    # Reproduce the rival framing in the old keymap page, not merely our decoder.
    # It starts at one node's value (+18) and borrows the NEXT node's name (+08).
    rival = []
    for start in range(0x1f45700, 0x1f462c0 + 1, 32):
        value, type_ptr, name_ptr, zero = struct.unpack('<QQQQ', read(start, 32))
        name = string(name_ptr)
        actual = by_name[name]
        assert int(actual['node'], 16) == start + 8 and type_ptr == int(actual['type_ptr'], 16)
        assert value == actual['value'] + 1 and zero == 0
        rival.append((name, value, actual['value']))
    assert len(rival) == 95
    lookup = {}
    for row in nodes:
        lookup.setdefault(row['value'], set()).add(row['name'])
    values = sorted(set(sum((tables[k]['u32'] for k in ('value_a', 'value_b', 'value_c')), [])))
    joins = [{'value': v, 'registry_names_at_same_integer': sorted(lookup.get(v, []))} for v in values]
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code = {}
    # Exact recorded bodies, not arbitrary interior decode starts.
    for va, size in [(0x1df240, 110), (0x1dfa70, 8), (0x198b60, 782),
                     (0x1dfd40, 214), (0x1dee90, 944)]:
        key = f'{va:08X}'
        record = span(key, va, size)
        ins = list(md.disasm(raw[key], va))
        assert sum(i.size for i in ins) == size, 'partial body decode'
        record['instructions'] = [f'{i.address:08X} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in ins]
        code[key] = record
    auxiliary = {'keyboard_scancodes': span('keyboard_scancodes', 0x1f3dab0, 125),
                 'ascii_key_codes': span('ascii_key_codes', 0x1f3da30, 128)}
    assert raw['ascii_key_codes'][ord('A')] == raw['ascii_key_codes'][ord('a')] == 28
    assert raw['ascii_key_codes'][13] == 77
    assert raw['keyboard_scancodes'][77 - 28] == 0x1c
    key_table = []
    for index in range(31):
        ptr = struct.unpack('<Q', read(0x1dfd050 + index * 8, 8))[0]
        key_table.append({'index': index, 'pointer': f'{ptr:08X}', 'name': string(ptr)})
    assert read(0x1dfd050 + 31 * 8, 8) == bytes(8)
    modes = {f'{va:08X}': string(va) for va in (0x901010, 0x901018)}
    return {'method': 'A: exact shipping file bytes; no execution or live intervention',
            'exe_sha256': EXPECTED, 'image_base': base, 'capstone_version': capstone.__version__,
            'registry_tsv_sha256': sha(registry_source), 'tables': tables, 'registry_nodes': nodes,
            'integer_join_only_not_domain_proof': joins, 'code': code, 'auxiliary': auxiliary,
            'settings_key_table': key_table, 'file_modes': modes}


def reduce_pulse(pulse):
    assert pulse['pid'] == 22784 and pulse['key'] == 'Enter'
    assert pulse['read_handle_closed'] and pulse['null_read_rejected']
    for boundary in ('before', 'after'):
        assert pulse[boundary]['exe_sha256'] == EXPECTED
        assert pulse[boundary]['module_verdict'] == 'clean'
    phases = {k: [] for k in ('baseline', 'held', 'release')}
    for sample in pulse['samples']:
        assert sample['status'] == 'STABLE_CHAIN'
        assert sample['array_address'] == sample['array_address_after'] == 0xe623e00
        b = bytes.fromhex(sample['raw'])
        assert len(b) == 256
        indices = [i for i, value in enumerate(b) if value]
        assert indices == sample['nonzero_indices']
        phases[sample['phase']].append(indices)
    assert [len(phases[p]) for p in phases] == [35, 34, 1], 'missing observation phases'
    assert all(not r for r in phases['baseline'] + phases['release'])
    assert all(r in ([], [49]) for r in phases['held'])
    positive = sum(r == [49] for r in phases['held'])
    assert positive == 32, 'detection control lost'
    return {'pid': 22784, 'baseline': 35, 'held': 34, 'release': 1,
            'positive': positive, 'observed_index': 49, 'corresponding_code': 77}


def retained_control():
    source = HERE.parent / 'input-registration-live-title/reuse'
    data = (source / 'title-enter.json').read_bytes()
    digest = sha(data)
    assert digest == '3c5ad2507a7fb4692d8b398518a74ddd8465ec2c4aa61889e3d62867a0f4a02b'
    assert json.loads((source / 'manifest.json').read_text())['files']['title-enter.json']['sha256'] == digest
    pulse = json.loads(data)
    result = reduce_pulse(pulse)
    # Small regression controls against the precise invalid/zero-case failure class.
    for tag in ('empty_samples', 'no_detection'):
        bad = json.loads(data)
        if tag == 'empty_samples':
            bad['samples'] = []
        else:
            for s in bad['samples']:
                s['raw'], s['nonzero_indices'] = '00' * 256, []
        try:
            reduce_pulse(bad)
        except AssertionError:
            continue
        raise AssertionError('invalid control accepted: ' + tag)
    return dict(result, sha256=digest, empty_samples_rejected=True, no_detection_rejected=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--exe', type=Path, default=ROOT / 'Database/Tools/work/exe/FFXII_TZA.exe')
    p.add_argument('--write', action='store_true')
    args = p.parse_args()
    result = collect(args.exe)
    target = HERE / 'observations.json'
    if args.write:
        assert not target.exists(), 'do not overwrite retained observations'
        target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    else:
        assert json.loads(target.read_text(encoding='utf-8')) == result, 'retained observations differ'
    nonzero = [r for r in result['integer_join_only_not_domain_proof'] if r['value']]
    tables = result['tables']
    active_codes = set(tables['keymap_buttons']['u32'] + tables['keymap_extra']['u32'] +
                       [v for i, v in enumerate(tables['keymap_axis_records']['u32']) if i % 4 >= 2]) - {0}
    common = sorted(active_codes & {r['value'] for r in nonzero})
    assert len(active_codes) == 42 and len(common) == 19
    assert not (active_codes & set(range(11, 27)))
    print('Exact source identity and complete named spans verified; registry nodes:', len(result['registry_nodes']))
    print('S44 distinct nonzero integers:', len(nonzero), 'named at same integer:', sum(bool(r['registry_names_at_same_integer']) for r in nonzero))
    print('The integer join does not prove the meaning of the S44 slots or a consumer relationship.')
    print('Rival framing verified: all95 old records borrow the next node name and are high by one.')
    print('Bounded active source codes:', len(active_codes), 'intersection:', common)
    print('Retained live control, re-reduced only:', json.dumps(retained_control(), sort_keys=True))


if __name__ == '__main__':
    main()
