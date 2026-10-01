"""Check the bounded experiment's receipts and seal every evidence file."""
import hashlib
import json
from pathlib import Path
import struct
import observe_ledger as observer

root = Path(__file__).resolve().parent
raw = bytearray(64 * 24)
struct.pack_into('<QQ', raw, 63 * 24, 1 << 63, (1 << 64) - 1)
raw[63 * 24 + 16] = 1
assert observer.decode_ledger(raw)[63] == dict(group=64, member=1 << 63,
                                             dead=(1 << 64) - 1, flags=1)
try:
    observer.decode_ledger(raw[:-1])
except ValueError:
    pass
else:
    raise AssertionError('short ledger accepted')
control = json.loads((root / 'decoder-control.json').read_text())
assert control['source_sha256'] == hashlib.sha256((root / 'observe_ledger.py').read_bytes()).hexdigest()
assert control['passed']
for name in ['stepping-qualified.json', 'combat-window-1.json', 'combat-window-2.json']:
    data = json.loads((root / name).read_text())
    assert data['status'] == 'OBSERVED' and data['pid'] == 12200
    assert data['module_verdict'] == 'clean' and data['modules']
    assert data['exe_sha256'] == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
    assert data['code_identity'][0]['sha256'] == '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
    for sample in data['samples']:
        assert 0 <= sample['state_index'] < len(data['states'])
        assert sample['end_seconds'] >= sample['start_seconds']
    for state in data['states']:
        assert len(bytes.fromhex(state['ledger_raw'])) == 64 * 24
        assert state['slot3'] == 0
        for unit in state['units']:
            if unit['slot'] == 4 and unit['hp'] is not None:
                assert unit['hp'] == 134 and unit['group'] == 1
inputs = []
for path in root.glob('*.json'):
    data = json.loads(path.read_text())
    if 'stdout' in data and 'source_sha256' in data:
        assert data['status'] == 'COMPLETED' and data['exit_code'] == 0, path
        assert 'polls that lost focus : 0' in data['stdout'], path
        inputs.append(path.name)
restored = json.loads((root / 'save-restored.json').read_text())
before = json.loads((root / 'save-before.json').read_text())
assert restored['after_restore'] == before['files'] and restored['no_extra_files']
assert restored['verified_files'] == 26
closed = json.loads((root / 'close-receipt.json').read_text())
assert closed['exited'] == [12200] and not closed['left'] and not closed['remaining']
files = {str(p.relative_to(root)): dict(bytes=p.stat().st_size,
         sha256=hashlib.sha256(p.read_bytes()).hexdigest())
         for p in sorted(root.rglob('*')) if p.is_file()
         and '__pycache__' not in p.parts and p.name != 'manifest.json'}
(root / 'manifest.json').write_text(json.dumps(dict(files=files, validated_input_receipts=inputs), indent=2) + '\n')
print('PASS: decoder controls, three read loops,', len(inputs), 'input receipts, cleanup;', len(files), 'sealed files')
