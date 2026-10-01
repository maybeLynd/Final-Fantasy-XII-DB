"""Prepare/check one disposable secondary Start binding; never deploys it."""
import configparser
import hashlib
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent
REPO = EVIDENCE.parents[4]
sha = lambda b: hashlib.sha256(b).hexdigest()
backup = Path(json.loads((EVIDENCE / 'save-before.json').read_text())['backup'])
raw = (backup / '76561198045890736/keymap.ini').read_bytes()
assert sha(raw) == '8d98f85e0b571d819dc155c8774aad553f6e6119d6ede1cdd62245cfb9f6cf6d'
# The protected original uses LF; preserve every byte outside this one value.
needle = b'[Keyboard2]\nSelect=114\nL3=0\nR3=110\nStart=0\n'
assert raw.count(needle) == 1
candidate = raw.replace(needle, needle.replace(b'Start=0', b'Start=43'))
parsed = configparser.ConfigParser(); parsed.read_string(candidate.decode())
assert parsed['Keyboard1']['Start'] == '64' and parsed['Keyboard2']['Start'] == '43'
values = [int(v) for sec in parsed.values() for v in sec.values()]
nonzero = [v for v in values if v]
assert len(values) == 84 and len(nonzero) == len(set(nonzero))

image = (REPO / 'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
assert sha(image) == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I', image, 0x3c)[0]; opt = pe + 24
base = struct.unpack_from('<Q', image, opt + 24)[0]
table = opt + struct.unpack_from('<H', image, pe + 20)[0]
sections = [struct.unpack_from('<IIII', image, table + i * 40 + 8)
            for i in range(struct.unpack_from('<H', image, pe + 6)[0])]


def read(va, size):
    rva = va - base
    for _, start, length, offset in sections:
        if start <= rva and rva + size <= start + length:
            return image[offset + rva - start:offset + rva - start + size]
    raise ValueError(hex(va))


prior = json.loads((EVIDENCE.parent / 's44-rebind-discriminator/observations.json').read_text())
node = next(x for x in prior['registry_nodes'] if x['name'] == 'Key_P')
assert node['value'] == 43 and read(int(node['node'], 16), 32).hex() == node['hex']
assert read(int(node['name_ptr'], 16), 6) == b'Key_P\0'
assert read(0x1F3DAB0 + 15, 1) == b'\x19'
assert read(0x1F3DA30 + ord('P'), 1) == b'\x2b'
reserved = list(struct.unpack('<35I', read(0x1DF13E0, 140)))
assert 43 not in reserved and all(v not in reserved for v in values)
assert all(1 <= int(v) <= 152 for v in parsed['Keyboard1'].values())

receipt = dict(status='PREPARED_NOT_DEPLOYED',
               method='A: exact P node/name, scancode, ASCII and reserved bytes; config inspection only',
               reference_sha256=sha(image), source_sha256=sha(raw), candidate_sha256=sha(candidate),
               only_change='Keyboard2 Start=0 ->43; Keyboard1 Escape=64 retained',
               key_p_node=node, expected_keyboard_array_index=15, expected_virtual_key=80,
               scan_code=25, ascii_mapping=43, reserved_codes=reserved,
               candidate_nonzero_unique=True, primary_range_check=True,
               limits=['Native config acceptance has not executed.',
                       'Registered P does not prove Start/Pause acceptance.',
                       'Take a fresh backup and revalidate current source before deployment.',
                       'No game/control/config mutation in this preparation.'])
outputs = {'original-keymap.ini': raw, 'candidate-keymap.ini': candidate,
           'preflight.json': (json.dumps(receipt, indent=2) + '\n').encode()}
for name, content in outputs.items():
    target = HERE / name
    if target.exists():
        assert target.read_bytes() == content, 'Retained preparation changed: ' + name
    else:
        with target.open('xb') as f:
            f.write(content)
print('Secondary Start=P candidate verified against exact source bytes; NOT deployed or live-qualified.')
