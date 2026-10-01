"""Exercise the actual CLI main with fake process boundaries; never attach to a process."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
HEADER = 'id\taddress\tkind\texpect\tmeaning\n'


def run(source, kind='u32', expect='81', raw=struct.pack('<I', 81), body=None):
    spec = importlib.util.spec_from_file_location('probe_under_test', source)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    events = []
    class Reader:
        def __init__(self, handle):
            assert handle == 123
        def read(self, address, size):
            events.append(['read', address, size])
            if address == mod.CONTROL_ADDR:
                return mod.CONTROL_BYTES
            assert address == 0x1000
            return raw
    mod.find_process = lambda _: [(456, 'OFFLINE-FAKE.exe')]
    mod.module_base = lambda _: mod.IMAGE_BASE
    mod.Probe = Reader
    mod.k32 = SimpleNamespace(OpenProcess=lambda *args: 123,
                              CloseHandle=lambda h: events.append(['close', h]))
    output = io.StringIO()
    with tempfile.TemporaryDirectory() as temp:
        tsv = Path(temp) / 'input.tsv'
        tsv.write_text(HEADER + (body if body is not None else
                       f'T1\t0x1000\t{kind}\t{expect}\tfixture\n'), encoding='utf-8')
        with patch.object(sys, 'argv', ['runtime_probe.py', '--check', str(tsv)]), \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                code = mod.main()
            except SystemExit as exc:
                code = exc.code
    assert events[-1] == ['close', 123]
    return {'exit': code, 'stdout': output.getvalue(), 'events': events}


def main():
    source = Path(sys.argv[1])
    mode = sys.argv[2]
    cases = [
        ('exact', {}, 0),
        ('substring', {'raw': struct.pack('<I', 181)}, 1),
        ('unreadable', {'raw': None}, 1),
        ('empty', {'body': ''}, 1),
        ('hex', {'expect': '0x51'}, 0),
        ('u8', {'kind': 'u8', 'expect': '255', 'raw': b'\xff'}, 0),
        ('u16', {'kind': 'u16', 'expect': '65535', 'raw': b'\xff\xff'}, 0),
        ('signed', {'kind': 'i32', 'expect': '-81', 'raw': struct.pack('<i', -81)}, 0),
        ('sign-mismatch', {'kind': 'i32', 'expect': '81', 'raw': struct.pack('<i', -81)}, 1),
        ('pointer', {'kind': 'ptr', 'expect': '0xFEDCBA9876543210',
                     'raw': struct.pack('<Q', 0xFEDCBA9876543210)}, 0),
        ('float', {'kind': 'f32', 'expect': '0.1', 'raw': struct.pack('<f', 0.1)}, 0),
        ('float-prefix', {'kind': 'f32', 'expect': '1', 'raw': struct.pack('<f', 1.5)}, 1),
        ('wildcard', {'expect': '*'}, 0),
        ('wildcard-unreadable', {'expect': '*', 'raw': None}, 1),
    ]
    if mode == 'after':
        cases += [
            ('short-read', {'raw': b'\x51'}, 1),
            ('unknown-kind', {'kind': 'typo'}, 1),
            ('blank-expect', {'expect': ''}, 1),
            ('out-of-range', {'kind': 'u8', 'expect': '256', 'raw': b'\0'}, 1),
            ('nan', {'kind': 'f32', 'expect': 'nan', 'raw': struct.pack('<f', float('nan'))}, 1),
            ('malformed-row', {'body': 'T1\t0x1000\tu32\t81\n'}, 2),
            ('extra-column', {'body': 'T1\t0x1000\tu32\t81\tfixture\textra\n'}, 2),
            ('mixed-error', {'raw': None, 'body': 'T1\t0x1000\tu32\t*\tfixture\nT2\t0x1000\tu32\t81\tfixture\n'}, 1),
        ]
    result = {'mode': mode, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'method': 'actual main; process enumeration/open/read/close replaced; no native process calls', 'cases': {}}
    for name, args, expected in cases:
        record = run(source, **args)
        record['required_exit'] = expected
        result['cases'][name] = record
        if mode == 'after':
            assert record['exit'] == expected, (name, record)
    if mode == 'before':
        for name in ('substring', 'unreadable', 'empty', 'sign-mismatch', 'float-prefix', 'wildcard-unreadable'):
            assert result['cases'][name]['exit'] == 0, name
    (HERE / (mode + '.json')).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(mode, len(cases), 'cases verified')


if __name__ == '__main__':
    main()
