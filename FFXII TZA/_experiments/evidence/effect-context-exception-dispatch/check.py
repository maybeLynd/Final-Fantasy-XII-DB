"""Read-only local exception-metadata check; no execution/reachability claim.

Run from repository root. The normal call identities come from the prior
instruction package, never from the exception-directory range endpoints.
Private altered records are detection controls, not original FF12 evidence.
"""
import hashlib
import json
import struct
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
DEPS = Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
sys.path.insert(0, str((DEPS / 'python-deps').resolve()))
import pefile

EXE = Path('Database/Tools/work/exe/FFXII_TZA.exe')
PRIOR = Path('Database/FFXII TZA/_experiments/evidence/heading-list-identity')
EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
BASE = 0x120000


def sha(b):
    return hashlib.sha256(b).hexdigest()


def require(ok, why):
    if not ok:
        raise ValueError(why)


image = EXE.read_bytes()
require(sha(image) == EXE_SHA, 'shipping image changed')
provider = Path(pefile.__file__)
deps_manifest = json.loads((DEPS / 'manifest.json').read_bytes())
provider_pin = next(m['sha256'] for m in deps_manifest['members']
                    if m['path'] == 'python-deps/pefile.py')
require(sha(provider.read_bytes()) == provider_pin, 'decoder changed')
prior_manifest = json.loads((PRIOR / 'manifest.json').read_bytes())
prior_pin = next(m['sha256'] for m in prior_manifest['members']
                 if m['path'] == 'result.json')
require(sha((PRIOR / 'result.json').read_bytes()) == prior_pin, 'prior result changed')
body_pin = json.loads((PRIOR / 'result.json').read_bytes())['body_identities']['003B3CA0']
p = pefile.PE(data=image)
require(p.OPTIONAL_HEADER.ImageBase == BASE, 'image base changed')


def raw(rva, length):
    require(length > 0 and rva > 0, 'invalid span')
    sections = [s for s in p.sections
                if s.VirtualAddress <= rva
                and rva + length <= s.VirtualAddress + s.SizeOfRawData]
    require(len(sections) == 1, 'span not wholly backed by one raw section')
    s = sections[0]
    off = s.PointerToRawData + rva - s.VirtualAddress
    require(off + length <= len(image), 'truncated image span')
    return image[off:off + length]


body = raw(0x3B3CA0 - BASE, body_pin['bytes'])
require(sha(body) == body_pin['sha256'], 'prior normal instruction identity changed')
calls = []
for pc, target in ((0x3B3CE0, 0x24ED80), (0x3B3CE7, 0x3A9490), (0x3B3CFD, 0x24ED80)):
    b = raw(pc - BASE, 5)
    require(b[0] == 0xE8 and pc + 5 + struct.unpack('<i', b[1:])[0] == target,
            'prior direct call no longer matches')
    calls.append({'pc_va': f'{pc:08X}', 'bytes': b.hex(),
                  'target_va': f'{target:08X}', 'continuation_va': f'{pc+5:08X}'})

directory = p.OPTIONAL_HEADER.DATA_DIRECTORY[3]
require(directory.Size > 0 and directory.Size % 12 == 0, 'bad exception directory size')
table = raw(directory.VirtualAddress, directory.Size)
entries = [struct.unpack_from('<III', table, i) for i in range(0, len(table), 12)]
native_entries = {(e.struct.BeginAddress, e.struct.EndAddress, e.struct.UnwindData): e
                  for e in p.DIRECTORY_ENTRY_EXCEPTION}
require(len(entries) == len(native_entries) and set(entries) == set(native_entries),
        'manual/pefile directory disagreement or duplicate entries')


def decode(entry, overrides=None):
    chain = []
    seen = set()
    overrides = overrides or {}
    while True:
        begin, end, unwind = entry
        require(begin < end and unwind not in seen, 'invalid/cyclic chain')
        seen.add(unwind)
        require(len(seen) <= 8, 'chain budget exceeded')
        head = raw(unwind, 4)
        version, flags, count = head[0] & 7, head[0] >> 3, head[2]
        require(version == 1 and flags <= 7, 'unsupported version/flags')
        require(not (flags & 4 and flags & 3), 'chain and handler flags mixed')
        tail = 4 + 2 * ((count + 1) & ~1)
        size = tail + (12 if flags & 4 else 4 if flags & 3 else 0)
        data = overrides.get(unwind, raw(unwind, size))
        require(len(data) == size and data[:4] == head, 'invalid override/span length')
        record = {'entry_rvas': list(entry), 'unwind_va': f'{BASE+unwind:08X}',
                  'version': version, 'flags': flags, 'code_slots': count,
                  'tail_offset': tail, 'raw_hex': data.hex()}
        chain.append(record)
        if flags & 4:
            entry = struct.unpack_from('<III', data, tail)
        else:
            handler = struct.unpack_from('<I', data, tail)[0] if flags & 3 else None
            record['handler_rva'] = handler
            return {'chain': chain, 'handler_va': f'{BASE+handler:08X}' if handler else None}


selected = []
for call in calls:
    continuation = int(call['continuation_va'], 16) - BASE
    matches = [e for e in entries if e[0] <= continuation < e[1]]
    require(len(matches) == 1, 'ambiguous/uncovered continuation')
    entry = matches[0]
    result = decode(entry)
    for r in result['chain']:
        ne = native_entries[tuple(r['entry_rvas'])].unwindinfo
        require((ne.Version, ne.Flags, ne.CountOfCodes) ==
                (r['version'], r['flags'], r['code_slots']), 'pefile header disagreement')
        if r['flags'] & 4:
            ce = ne._chained_entry.struct
            require([ce.BeginAddress, ce.EndAddress, ce.UnwindData] ==
                    result['chain'][1]['entry_rvas'],
                    'pefile chain target disagreement')
    require(len(result['chain']) == 2 and result['handler_va'] is None,
            'local no-handler hypothesis refuted')
    selected.append({'call': call, 'metadata': result})

positive_entry = next(e for e in entries if e[0] == 0x1F40)
positive = decode(positive_entry)
positive_pe = native_entries[positive_entry].unwindinfo
require(positive['handler_va'] == '00808BA8'
        and (positive_pe.Version, positive_pe.Flags, positive_pe.CountOfCodes) ==
            (positive['chain'][0]['version'], positive['chain'][0]['flags'],
             positive['chain'][0]['code_slots'])
        and positive_pe.Flags == 3
        and positive_pe.ExceptionHandler + BASE == int(positive['handler_va'], 16),
        'real handler positive control failed')
first = selected[0]['metadata']['chain'][0]
changed = bytearray.fromhex(first['raw_hex'])
struct.pack_into('<III', changed, first['tail_offset'], *positive_entry)
redirect = decode(tuple(first['entry_rvas']), {first['entry_rvas'][2]: bytes(changed)})
require(redirect['handler_va'] == positive['handler_va'], 'chain redirect not detected')
cycle = bytearray.fromhex(first['raw_hex'])
struct.pack_into('<III', cycle, first['tail_offset'], *first['entry_rvas'])
try:
    decode(tuple(first['entry_rvas']), {first['entry_rvas'][2]: bytes(cycle)})
except ValueError as exc:
    require(str(exc) == 'invalid/cyclic chain', 'unexpected cycle refusal')
else:
    raise ValueError('cycle accepted')
require(sha(EXE.read_bytes()) == EXE_SHA, 'reference changed during read')
out = {
    'status': 'PRODUCER_CHECKED_STATIC_METADATA_ONLY',
    'question': 'Does local exception metadata at the three prior-proven call continuations name a language handler?',
    'reference': {'exe_sha256': EXE_SHA, 'image_base': BASE,
                  'pefile_sha256': provider_pin, 'driver_sha256': sha(Path(__file__).read_bytes()),
                  'prior_result_sha256': prior_pin, 'prior_body': body_pin,
                  'exception_directory_rva': directory.VirtualAddress,
                  'exception_directory_bytes': directory.Size,
                  'exception_directory_sha256': sha(table)},
    'observations': selected,
    'controls': {'actual_shipping_handler': positive,
                 'PRIVATE_CHAIN_REDIRECT_NOT_SHIPPING': redirect,
                 'private_cycle_refused': True},
    'interpretation': 'All three continuations select the same chained record ending in flags=0; this local metadata names no language handler.',
    'limits': ['No execution, exception occurrence or normal reachability measured.',
               'No claim of full function extent from exception metadata.',
               'Outer handlers and restoration by other code remain open.',
               'No lifetime, scheduling, initialized live identity or presentation claim.',
               'Producer controls are not independent acceptance.'],
    'cleanup': {'reference_hash_unchanged': True, 'game_launched': False,
                'live_input_or_instrumentation': False, 'save_config_written': False}
}
print(json.dumps(out, indent=2))
