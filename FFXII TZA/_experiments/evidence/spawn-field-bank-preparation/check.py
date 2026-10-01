"""Verify original field-preparation bytes and cross-package ordering anchors.

Method A only. This checks evidence integrity and the cited instructions; it
does not execute the game or substitute a model for native behavior.
"""
import hashlib
import json
from pathlib import Path

W = Path('Database/Tools/work/ASTRA')
source = W / 'spawn_field_primary.py'
ns = {}
s = source.read_text()
exec(compile(s[:s.index('for a in (0x26C8C0')], str(source), 'exec'), ns)
sha = lambda b: hashlib.sha256(b).hexdigest()
cat = {}
for name in ('primary', 'callees'):
    receipt = json.loads((W / ('spawn-field-' + name + '.json')).read_text())
    assert receipt['exe_sha256'] == ns['sha']
    for b in receipt['bodies']:
        a = int(b['address'], 16)
        assert a not in cat
        cat[a] = b
assert len(cat) == 9

def verify_body(b):
    a = int(b['address'], 16)
    data = b''
    pos = a
    for ins in b['instructions']:
        assert int(ins['address'], 16) == pos
        d = bytes.fromhex(ins['bytes'])
        data += d
        pos += len(d)
    o = ns['off'](a - ns['ib'])
    assert len(data) == b['bytes'] and sha(data) == b['sha256']
    assert data == ns['raw'][o:o + len(data)]
    return data

for body in cat.values():
    verify_body(body)
    assert body['instructions'][-1]['mnemonic'] in ('ret', 'int3')

def at(a, bodies=cat):
    return next(i for b in bodies.values() for i in b['instructions'] if int(i['address'], 16) == a)

proof = cat[0x26C8C0]['extent_proof']
assert proof['end_exclusive'] == '0x26cdf4'
assert proof['raw_hex'] == 'c0c81400f4cd1400442ec301'
assert cat[0x26C8C0]['catalog_body_bytes'] == 1330
assert cat[0x26C8C0]['bytes'] == 1332
assert [i['address'] for i in cat[0x26C8C0]['instructions'] if i['mnemonic'] == 'int3'] == ['0x26cded', '0x26cdf3']
failed = json.loads((W / 'spawn-field-incomplete.json').read_text())
prefix = bytes.fromhex(failed['raw_hex'])
assert sha(prefix) == failed['raw_sha256']
assert prefix == verify_body(cat[0x26C8C0])[:1330]
assert failed['decoded_prefix'] == 1326 and failed['stop'] == '0x26cdee'

# Direct instruction controls: bank identities, flag gates, and caller order.
anchors = {
    0x26CB2D: ('mov', 'qword ptr [rdi + 0x58], rax'),
    0x26CB38: ('mov', 'qword ptr [rdi + 0x60], rax'),
    0x26CD5E: ('jne', '0x26cdbe'),
    0x26CD60: ('call', '0x26db30'),
    0x26DB80: ('call', '0x861ec0'),
    0x26DBEB: ('cmp', 'edi, ebx'),
    0x26DBED: ('je', '0x26dc16'),
    0x26DBF4: ('test', 'byte ptr [rax + 0x1062], 0x20'),
    0x26DBFB: ('jne', '0x26dc02'),
    0x26DBFD: ('call', '0x3149e0'),
    0x26DC11: ('call', '0x861ec0'),
    0x26DC1B: ('test', 'al, 8'),
    0x26DC2E: ('call', '0x861ec0'),
    0x26832B: ('jne', '0x26834a'),
    0x268334: ('je', '0x26834a'),
    0x268345: ('call', '0x861ec0'),
    0x268359: ('call', '0x861ec0'),
    0x268365: ('jne', '0x268373'),
    0x26836C: ('mov', 'byte ptr [rax + 0x1061], 1'),
    0x31467F: ('mov', 'dword ptr [rip + 0x1bd89df], esi'),
    0x3146DE: ('and', 'byte ptr [rax + 0x1062], 0xdf'),
    0x314759: ('mov', 'dword ptr [rip + 0x1af7c89], 1'),
    0x3147BB: ('call', '0x229b40'),
    0x3147DF: ('call', '0x5844a0'),
    0x3147E4: ('call', '0x584580'),
    0x3147E9: ('call', '0x583260'),
    0x3148FB: ('mov', 'eax, dword ptr [rax + 0x1044]'),
    0x314903: ('cmovs', 'eax, ecx'),
    0x314879: ('mov', 'eax, dword ptr [rax + 0x104c]'),
    0x3148D9: ('mov', 'eax, dword ptr [rax + 0x1054]'),
    0x3149E9: ('and', 'byte ptr [rax + 0x1062], 0xfb'),
}
for a, expected in anchors.items():
    ins = at(a)
    assert (ins['mnemonic'], ins['operands']) == expected, (hex(a), ins)
for a, target in ((0x26DB73, 0x2099DF0), (0x26DC04, 0x2099FF0),
                  (0x26DC21, 0x2099FF0), (0x268338, 0x2099FF0),
                  (0x26834C, 0x2099DF0), (0x268324, 0x209AC10),
                  (0x26832D, 0x1E0C3EC), (0x26835E, 0x209AC10)):
    assert int(at(a)['rip_targets'][0]['address'], 16) == target

# Reuse existing whole bodies, preserving file identity and the exact bridge.
reused = []
for rel, address, sites in (
    ('spawn-load-continuation/sequence.json', 0x582860, (0x582E98,)),
    ('spawn-manager-dispatch/primary.json', 0x314020, (0x314078, 0x3140BA)),
):
    p = Path('Database/FFXII TZA/_experiments/evidence') / rel
    r = json.loads(p.read_text())
    assert r['exe_sha256'] == ns['sha']
    b = next(b for b in r['bodies'] if int(b['address'], 16) == address)
    verify_body(b)
    selected = [at(a, {address: b}) for a in sites]
    reused.append(dict(path=str(p).replace('\\', '/'), sha256=sha(p.read_bytes()),
                       body_sha256=b['sha256'], selected_instructions=selected))
assert reused[0]['selected_instructions'][0]['bytes'] == 'c7056e7db10101000000'
assert reused[0]['selected_instructions'][0]['rip_targets'][0]['address'] == '0x209ac10'
assert [i['operands'] for i in reused[1]['selected_instructions']] == ['0x25bfb0', '0x32fc30']

out = dict(exe_sha256=ns['sha'], method='A only', original_bodies=9,
           complete_original_bytes=True, extent_proof=proof,
           incomplete_collection='Retained; rejected contiguous-length assumption, not a semantic pass or a ledger error.',
           selected_anchors=[at(a) for a in anchors], reused_sources=reused,
           limits='Local native stores, calls and guards only. No B/live run, initialized-state proof, exhaustive flag-writer proof, or actual save/load scheduling.',
           checks='pass')
(W / 'spawn-field-check.json').write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('selected_anchors','reused_sources')}, indent=2))
