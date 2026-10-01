"""Method A: exact original leaf source and integer-width proof; no machine execution."""
import csv, datetime, hashlib, importlib.util, json, sys
from pathlib import Path
import capstone

W = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
sys.path.insert(0, 'Database/Tools/analysis-kit/gfz-scripts')
import team
ok, detail = team.board_status(team.BOARD)
assert ok, detail
t = next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id'] == 'ASTRA-IMAGE-REFERENCE-ROUNDTRIP-DOMAIN')
assert t['status'] == 'ACTIVE' and t['agent'] == 'ASTRA'
assert not (W / 'result.json').exists()
rp = Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
assert sha(rp.read_bytes()) == '4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp = importlib.util.spec_from_file_location('shipping_reader', rp)
rd = importlib.util.module_from_spec(sp)
sp.loader.exec_module(rd)
image, ss = rd.load_image()
assert sha(image) == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cs.detail = True
decode = rd.img_rd(image, ss, 0x20E600, 10)
encode = rd.img_rd(image, ss, 0x20E620, 9)

def bind(d, e):
    di = list(cs.disasm(d, 0x20E600))
    ei = list(cs.disasm(e, 0x20E620))
    assert d.hex() == '8bc1480305274fd701c3'
    assert e.hex() == '2b0d0a4fd7018bc1c3'
    assert len(di) == len(ei) == 3
    assert sum(i.size for i in di) == 10 and sum(i.size for i in ei) == 9
    assert di[0].op_str == ei[1].op_str == 'eax, ecx'
    assert di[1].mnemonic == 'add' and di[1].operands[0].size == di[1].operands[1].size == 8
    assert ei[0].mnemonic == 'sub' and ei[0].operands[0].size == ei[0].operands[1].size == 4
    for i in (di[1], ei[0]):
        assert i.operands[1].mem.base == capstone.x86.X86_REG_RIP
        assert i.address + i.size + i.operands[1].mem.disp == 0x1F83530
    assert di[2].mnemonic == ei[2].mnemonic == 'ret'
    return di + ei

ins = bind(decode, encode)
M32, M64 = (1 << 32) - 1, (1 << 64) - 1

def resolve(b, u):
    return (b + (u & M32)) & M64

def encode_prediction(b, p, op='sub'):
    return ((p & M32) - (b & M32) if op == 'sub' else (p & M32) + (b & M32)) & M32

def case(name, b, p):
    u = encode_prediction(b, p)
    q = resolve(b, u)
    delta = (p - b) & M64
    assert (q == p) == (delta < (1 << 32))
    assert encode_prediction(b, resolve(b, u)) == u
    return dict(name=name, base=f'{b:016X}', pointer=f'{p:016X}', encoded=f'{u:08X}', decoded=f'{q:016X}', relative_delta=f'{delta:016X}', pointer_roundtrip=q == p)

cases = [case('zero-base in-window', 0, 0x1234),
         case('nonzero-base in-window', 0x120000, 0x121234),
         case('translated upper edge', 0x120000, 0x10011FFFF),
         case('just outside translated window', 0x120000, 0x100120000),
         case('null at nonzero base', 0x120000, 0),
         case('conditional high base', 0x7FF600120000, 0x7FF600121234),
         case('modulo64 wrapping translated window', 0xFFFFFFFFFFFFFFF0, 0x10)]
assert cases[1]['encoded'] == '00001234' and cases[2]['encoded'] == 'FFFFFFFF'
assert cases[3]['encoded'] == '00000000' and not cases[3]['pointer_roundtrip']
assert cases[4]['encoded'] == 'FFEE0000' and cases[4]['decoded'] == '0000000100000000'
assert all(c['pointer_roundtrip'] for c in (cases[0], cases[1], cases[2], cases[5], cases[6]))
references = []
for b, u in ((0, 0xFFFFFFFF), (0x120000, 0), (0x7FF600120000, 0xFFFFFFFF), (0xFFFFFFFFFFFFFFF0, 0x20)):
    p = resolve(b, u)
    assert encode_prediction(b, p) == u
    references.append(dict(base=f'{b:016X}', reference=f'{u:08X}', resolved=f'{p:016X}', encoded_again=f'{encode_prediction(b,p):08X}'))
mutant = bytearray(encode)
mutant[0] = 0x03  # ADD ECX,[RIP+disp32], same width and target
mi = next(cs.disasm(mutant, 0x20E620))
assert mi.mnemonic == 'add' and mi.operands[1].size == 4 and mi.address + mi.size + mi.operands[1].mem.disp == 0x1F83530
rejected = False
try:
    bind(decode, mutant)
except AssertionError:
    rejected = True
assert rejected
zero = dict(base='0000000000000000', pointer='0000000000001234', original=f'{encode_prediction(0,0x1234):08X}', private_add_model=f'{encode_prediction(0,0x1234,"add"):08X}')
nonzero = dict(base='0000000000120000', pointer='0000000000121234', original=f'{encode_prediction(0x120000,0x121234):08X}', private_add_model=f'{encode_prediction(0x120000,0x121234,"add"):08X}')
assert zero['original'] == zero['private_add_model'] and nonzero['original'] != nonzero['private_add_model']
changing = dict(decode_base='0000000000120000', encode_base='0000000000120001', input_reference='00001234', encoded_again=f'{encode_prediction(0x120001,resolve(0x120000,0x1234)):08X}')
assert changing['encoded_again'] == '00001233'
R = W / 'retained'
R.mkdir(exist_ok=False)
for name, data in [('decode.bin', decode), ('encode.bin', encode), ('shipping-reader.py', rp.read_bytes())]:
    (R / name).write_bytes(data)
preimages = []
for name, path in [('shared-neighbours.md', 'Database/FFXII TZA/00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md'),
                   ('encoded-id-contract.md', 'Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md'),
                   ('image_address_base_writer_bounds.py', 'Database/FFXII TZA/02-Resource-And-Asset-Pipeline/members/image_address_base_writer_bounds.py')]:
    data = Path(path).read_bytes()
    (R / name).write_bytes(data)
    preimages.append(dict(path=path, sha256=sha(data), retained_name=name))
assert 'exact inverses' in (R / 'shared-neighbours.md').read_text()
assert '["0020E602", "0020E620"]' in (R / 'image_address_base_writer_bounds.py').read_text()
fpath = Path('Database/Tools/work/graph/functions.tsv')
fb = fpath.read_bytes()
rows = [r for r in csv.DictReader(fb.decode().splitlines(), delimiter='\t') if r['entry'] in ('0020E600', '0020E620')]
assert {r['entry']: r['body_bytes'] for r in rows} == {'0020E600': '10', '0020E620': '9'}
(R / 'catalog-identity.json').write_text(json.dumps(dict(path=fpath.as_posix(), sha256=sha(fb), rows=rows, limits='Catalog corroboration only; original bytes and complete leaves checked separately'), indent=2) + '\n')
dll = Path(capstone._cs._name)
result = dict(question='Unqualified exact inverses/null preservation versus stable-base translated unsigned32 reference domain', method='A verified complete original10/9-byte source and integer-width/modular proof with selected conditional calculations; zero original/native/emulator/live executions',
    reference=dict(exe_sha256=sha(image), decode_entry='0x20e600', encode_entry='0x20e620', decode_sha256=sha(decode), encode_sha256=sha(encode), shared_cell='0x1f83530', reader_sha256=sha(rp.read_bytes())),
    tools=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), python=sys.version, interpreter=sys.executable, interpreter_sha256=sha(Path(sys.executable).read_bytes()), capstone=capstone.__version__, capstone_dll=dict(path=str(dll), sha256=sha(dll.read_bytes()))), driver_sha256=sha(Path(__file__).read_bytes()),
    instructions=[dict(pc=hex(i.address), bytes=i.bytes.hex(), op=i.mnemonic, args=i.op_str) for i in ins],
    proof=dict(decode='D_B(u)=(B+u32(u)) mod2^64', encode='E_B(p)=u32(u32(p)-u32(B))', reference_roundtrip='E_B(D_B(u))=u for all unsigned32 u at fixed B, by reduction mod2^32', pointer_roundtrip='D_B(E_B(p))=p iff ((p-B) mod2^64)<2^32, since E is that delta reduced mod2^32 and D adds it to B mod2^64', collision='Pointers with same low32 encode identically at fixed B, including p and p+2^32 modulo2^64', null='D_B(0)=B; E_B(0)=u32(-B). No intrinsic null-preserving or signed-offset rule.'),
    cases=cases, reference_controls=references, base_change_control=changing,
    mutation_control=dict(name='private source SUB-to-ADD', encode_hex=mutant.hex(), exact_binding_rejected=rejected, zero_base_control=zero, nonzero_base_discriminator=nonzero, limits='Source mutation/conditional Python calculation only. No changed code executed. Zero-base-only insufficiency is a control observation, not allegation against an unnamed existing checker.'),
    consumer_preimages=preimages,
    prior_base_findings='Reuse owner contract and writer R6: cell BSS zero at image load; computed texture-id=-5 writer undriven not absent; process-lifetime zero supported not proven. Existing R1 source names20E602/20E620 correctly. Contract citations20E626 name MOV not RIP SUB. No writer census/replay rerun.',
    implication='Qualify both exact-inverse phrases and image-base terminology in FABLE summary. OPUS representation domain needs stableB/unsigned32 translated window/null semantics; repair only wrong inverse-site citations, retain full-width consumer and prior writer findings. No bulk disposition/caller classification.',
    limits='All B/p values here conditional injected numbers, not observed game addresses. Shared B is not established as PE/module base. Readable cell and instruction execution completion assumed; stableB required across calls, not guaranteed atomically. No process-lifetime base value, actual callers, initialization beyond retained prior image-load finding, mapped-memory validity, ownership/lifetime, allocation, relocation portability, normal reachability or native effects proved.',
    cleanup='Read-only original image and retained peer preimages, Python source calculations only. PC OFF; no game/input/process/instrument/save/config/reference/peer writes. Consumer propagation and independent review pending.')
(W / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
print('Derived reference codec stable-base width/null domain; corrected inverse-site20E620. Original source and modular calculations only, no machine/live execution.', flush=True)
