"""Scoped Phyre observations using the retained EXP079 read/identity method."""
import argparse
import csv
import ctypes
import hashlib
import json
from pathlib import Path
import struct
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
KIT = REPO / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(KIT))
import runtime_probe as rp
import ffxii_runtime as rt
import team


def rows(name):
    return list(csv.DictReader((l for l in (HERE / name).read_text().splitlines()
                               if not l.startswith('#')), delimiter='\t'))


def targets():
    defaults = {r['class_leaf']: r for r in rows('phyre-default-instances.tsv')}
    parents = {r['class_leaf']: r for r in rows('phyre-class-parent-chain.tsv')}
    sized = rows('phyre-class-instance-sizes.tsv')
    assert len(defaults) == 173 and len(sized) == 177
    assert len({r['class_leaf'] for r in sized}) == 177
    result = []
    for row in sized:
        name = row['class_leaf']
        parent = parents[name]
        item = dict(name=name, address=int(parent['descriptor'], 16),
                    size=int(row['instance_size'], 0), expected_parent=parent['parent_descriptor'])
        assert 0 < item['size'] <= 0x10000
        if name in defaults:
            d = defaults[name]
            assert int(d['descriptor'], 16) == item['address']
            assert int(d['instance_size'], 0) == item['size']
            item['default_address'] = int(d['default_instance'], 16)
        result.append(item)
    assert sum(t['size'] for t in result if 'default_address' in t) == 34392
    return result


def decode_header(raw):
    if len(raw) != 0x108:
        raise ValueError('short descriptor; never zero-fill a read failure')
    q = lambda off: struct.unpack_from('<Q', raw, off)[0]
    return dict(vtable=q(0), name_pointer=q(0x30), size=struct.unpack_from('<I', raw, 0x38)[0],
                parent=q(0x78), default_pointer=q(0xC0), second_buffer=q(0xC8),
                third_buffer=q(0xD0), flags=struct.unpack_from('<I', raw, 0xFC)[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pid', type=int, required=True)
    ap.add_argument('--label', required=True)
    ap.add_argument('--pilot', action='store_true')
    ap.add_argument('--defaults-only', action='store_true')
    a = ap.parse_args()
    assert a.label.replace('-', '').isalnum()
    out = HERE / (a.label + '.json')
    assert not out.exists(), 'preserve earlier raw evidence'
    result = dict(status='INVALID', pid=a.pid, label=a.label, pilot=a.pilot,
                  start_unix=time.time(), command=sys.argv, reads=[], descriptors=[],
                  defaults_only=a.defaults_only,
                  method='C: read-only process observation after ordinary startup',
                  intervention='Ordinary process launch/UI; no memory writes, debugger or native calls',
                  tool_hashes={str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (Path(__file__), KIT/'runtime_probe.py', KIT/'ffxii_runtime.py')})
    h = None
    code = 1
    try:
        board = json.loads(team.BOARD.read_text())
        assert any(t['id'] == 'OPUS-REQ-ASTRA-PHYRE-DEFAULT-INSTANCE-BYTES'
                   and t['status'] == 'ACTIVE' and t['agent'] == 'ASTRA' for t in board['tasks'])
        for inp in json.loads((HERE/'input-sources.json').read_text()):
            assert hashlib.sha256((HERE/inp['copy']).read_bytes()).hexdigest() == inp['sha256']
            assert (REPO/inp['source']).read_bytes() == (HERE/inp['copy']).read_bytes(), 'source changed; re-review'
        owner = json.loads((HERE/'process.json').read_text())
        assert owner['pid'] == a.pid and rt.list_processes() == [owner], 'wrong process'
        raw_exe = Path(owner['path']).read_bytes()
        result['exe'] = owner['path']
        result['exe_sha256'] = hashlib.sha256(raw_exe).hexdigest()
        assert result['exe_sha256'] == rt.AUTHORITY_SHA256
        verdict, hits, modules = rt.classify(a.pid)
        result.update(module_verdict=verdict, watched_modules=hits, modules_before=modules)
        assert verdict == 'clean' and modules
        rp.k32.OpenProcess.restype = ctypes.c_void_p
        rp.k32.CloseHandle.argtypes = [ctypes.c_void_p]
        rp.k32.ReadProcessMemory.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                                           ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
        rp.psapi.EnumProcessModules.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong,
                                               ctypes.POINTER(ctypes.c_ulong)]
        h = rp.k32.OpenProcess(rp.PROCESS_QUERY_INFORMATION | rp.PROCESS_VM_READ, False, a.pid)
        assert h
        reader = rp.Probe(h)
        result['image_base'] = rp.module_base(h)
        assert result['image_base'] == rp.IMAGE_BASE

        def read(addr, size, purpose):
            start = time.time()
            got = reader.read(addr, size)
            result['reads'].append(dict(address=addr, size=size, purpose=purpose,
                                        start_unix=start, end_unix=time.time(),
                                        hex=None if got is None else got.hex()))
            assert got is not None and len(got) == size, ('failed read', hex(addr), size, purpose)
            return got

        assert read(rp.CONTROL_ADDR, len(rp.CONTROL_BYTES), 'nonzero positive') == rp.CONTROL_BYTES
        result['null_read_rejected'] = reader.read(0, 16) is None
        assert result['null_read_rejected']
        rp.k32.CheckRemoteDebuggerPresent.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
        debug = ctypes.c_int()
        assert rp.k32.CheckRemoteDebuggerPresent(h, ctypes.byref(debug))
        result['debugger_present'] = bool(debug.value)
        assert not debug.value
        pe = struct.unpack_from('<I', raw_exe, 0x3C)[0]
        count = struct.unpack_from('<H', raw_exe, pe+6)[0]
        table = pe+24+struct.unpack_from('<H', raw_exe, pe+20)[0]
        sections = []
        for n in range(count):
            off = table+n*40
            if raw_exe[off:off+8].rstrip(b'\0') == b'.text':
                vs, rva, size, ro = struct.unpack_from('<4I', raw_exe, off+8)
                sections.append((rp.IMAGE_BASE+rva, raw_exe[ro:ro+min(size,vs)]))
        assert len(sections) == 1

        def identity(label):
            addr, expected = sections[0]
            actual = reader.read(addr, len(expected))
            result['text_'+label] = dict(address=addr, bytes=len(expected), matches=actual == expected,
                                         disk_sha256=hashlib.sha256(expected).hexdigest(),
                                         live_sha256=None if actual is None else hashlib.sha256(actual).hexdigest())
            assert actual == expected, 'live .text differs'

        def name_at(ptr):
            assert ptr, 'uninitialized/null class name'
            data = bytearray()
            for n in range(256):
                c = read(ptr+n, 1, 'class-name-byte')
                if c == b'\0':
                    return data.decode('ascii')
                data += c
            raise ValueError('unterminated class name')

        identity('before')
        selected = targets()
        if a.defaults_only:
            selected = [t for t in selected if 'default_address' in t]
            assert len(selected) == 173
        if a.pilot:
            wanted = {'PAnimatableComponent', 'PAnimationChannel', 'PDeferredLightingBase'}
            selected = [t for t in selected if t['name'] in wanted]
            assert len(selected) == 3
        result['requested_descriptors'] = len(selected)
        result['requested_default_spans'] = sum('default_address' in t for t in selected)
        for target in selected:
            before = read(target['address'], 0x108, 'descriptor-before')
            fields = decode_header(before)
            item = dict(target=target, fields=fields, name=name_at(fields['name_pointer']))
            result['descriptors'].append(item)
            assert item['name'].split('::')[-1] == target['name'], ('name disagreement', item)
            assert fields['size'] == target['size'], ('size disagreement', item)
            if 'default_address' in target:
                item['pointer_matches'] = fields['default_pointer'] == target['default_address']
                assert item['pointer_matches'], ('default pointer disagreement', item)
                value = read(fields['default_pointer'], fields['size'], 'default-buffer')
                item.update(default_hex=value.hex(), nonzero_bytes=sum(x != 0 for x in value),
                            prepared_bit31=bool(fields['flags'] & 0x80000000))
            after = read(target['address'], 0x108, 'descriptor-after')
            item['header_bracket_matches'] = before == after
        # Bounded ancestry, without interpreting a base link as a subobject offset.
        pending = [(d['fields']['parent'], 1) for d in result['descriptors'] if d['fields']['parent']]
        seen = {d['target']['address'] for d in result['descriptors']}
        result['extra_parents'] = []
        while pending:
            address, depth = pending.pop()
            if address in seen:
                continue
            assert depth <= 32 and len(seen) < 512, 'parent walk bound exceeded'
            seen.add(address)
            b = read(address, 0x108, 'ancestor-descriptor')
            f = decode_header(b)
            result['extra_parents'].append(dict(address=address, fields=f, name=name_at(f['name_pointer'])))
            if f['parent']:
                pending.append((f['parent'], depth+1))
        identity('after')
        assert read(rp.CONTROL_ADDR, len(rp.CONTROL_BYTES), 'positive-after') == rp.CONTROL_BYTES
        verdict, hits, modules = rt.classify(a.pid)
        result.update(module_verdict_after=verdict, watched_modules_after=hits, modules_after=modules)
        assert verdict == 'clean' and modules
        assert rt.list_processes() == [owner]
        assert len(result['descriptors']) == result['requested_descriptors']
        result['status'] = 'OBSERVED'
        code = 0
    except BaseException as exc:
        result['error'] = repr(exc)
        import traceback
        result['traceback'] = traceback.format_exc()
    finally:
        if h:
            result['read_handle_closed'] = bool(rp.k32.CloseHandle(h))
        result['end_unix'] = time.time()
        if not result.get('read_handle_closed'):
            code = 1
        with out.open('x', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
        print(json.dumps({k: result.get(k) for k in ('status','error','requested_descriptors',
              'requested_default_spans','read_handle_closed','start_unix','end_unix')}))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
