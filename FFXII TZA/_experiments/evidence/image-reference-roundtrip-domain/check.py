"""Readonly retained-source and conditional-control checker; no image or machine execution."""
import hashlib, json
from pathlib import Path
import capstone
W = Path(__file__).resolve().parent
R = W / 'retained'
sha = lambda b: hashlib.sha256(b).hexdigest()
r = json.loads((W / 'result.json').read_text())
assert r['reference']['exe_sha256'] == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert r['driver_sha256'] == sha((W / 'derive.py').read_bytes())
assert sha((R / 'shipping-reader.py').read_bytes()) == r['reference']['reader_sha256'] == '4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cs.detail = True
allins = []
for name, entry, raw, digest in [('decode.bin',0x20E600,'8bc1480305274fd701c3','decode_sha256'),('encode.bin',0x20E620,'2b0d0a4fd7018bc1c3','encode_sha256')]:
    data = (R / name).read_bytes()
    assert data.hex() == raw and sha(data) == r['reference'][digest]
    ins = list(cs.disasm(data, entry))
    assert len(ins) == 3 and sum(i.size for i in ins) == len(data) and ins[-1].mnemonic == 'ret'
    i = ins[1] if name == 'decode.bin' else ins[0]
    assert i.mnemonic == ('add' if name == 'decode.bin' else 'sub')
    assert i.operands[0].size == i.operands[1].size == (8 if name == 'decode.bin' else 4)
    assert i.address + i.size + i.operands[1].mem.disp == 0x1F83530
    allins.extend(ins)
assert r['instructions'] == [dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in allins]
assert allins[0].op_str == allins[4].op_str == 'eax, ecx'
M32, M64 = (1 << 32) - 1, (1 << 64) - 1
assert len(r['cases']) == 7
for c in r['cases']:
    b, p = int(c['base'],16), int(c['pointer'],16)
    u = (p - b) & M32
    q = (b + u) & M64
    assert u == int(c['encoded'],16) and q == int(c['decoded'],16)
    assert int(c['relative_delta'],16) == (p - b) & M64
    assert c['pointer_roundtrip'] == (q == p) == (((p-b) & M64) < (1 << 32))
assert [c['pointer_roundtrip'] for c in r['cases']] == [True,True,True,False,False,True,True]
assert r['cases'][4]['decoded'] == '0000000100000000'
assert len(r['reference_controls']) == 4
for c in r['reference_controls']:
    b, u = int(c['base'],16), int(c['reference'],16)
    p = (b + u) & M64
    assert p == int(c['resolved'],16) and ((p-b)&M32) == u == int(c['encoded_again'],16)
m = r['mutation_control']
raw = (R / 'encode.bin').read_bytes()
mut = bytes.fromhex(m['encode_hex'])
assert [i for i,(a,b) in enumerate(zip(raw,mut)) if a != b] == [0] and mut[0] == 3 and len(mut) == 9 and m['exact_binding_rejected']
mi = next(cs.disasm(mut,0x20E620))
assert mi.mnemonic == 'add' and mi.address + mi.size + mi.operands[1].mem.disp == 0x1F83530
for c in (m['zero_base_control'],m['nonzero_base_discriminator']):
    b,p = int(c['base'],16),int(c['pointer'],16)
    assert int(c['original'],16) == (p-b)&M32 and int(c['private_add_model'],16) == (p+b)&M32
assert m['zero_base_control']['original'] == m['zero_base_control']['private_add_model']
assert m['nonzero_base_discriminator']['original'] != m['nonzero_base_discriminator']['private_add_model']
c = r['base_change_control']
assert (((int(c['decode_base'],16)+int(c['input_reference'],16))&M64)-int(c['encode_base'],16))&M32 == int(c['encoded_again'],16) == 0x1233
for x in r['consumer_preimages']:
    assert sha((R / x['retained_name']).read_bytes()) == x['sha256']
assert '["0020E602", "0020E620"]' in (R / 'image_address_base_writer_bounds.py').read_text()
assert {x['entry']:x['body_bytes'] for x in json.loads((R/'catalog-identity.json').read_text())['rows']} == {'0020E600':'10','0020E620':'9'}
if (W / 'manifest.json').exists():
    members = json.loads((W / 'manifest.json').read_text())['members']
    assert members
    for x in members:
        data = (W / x['path']).read_bytes()
        assert len(data) == x['bytes'] and sha(data) == x['sha256']
print('PASS_SOURCE_REFERENCE_DOMAIN exact10/9B/RIP widths, stable-base u32 inverse window, null/width/base-change and source-mutation controls; no machine/live proof')
