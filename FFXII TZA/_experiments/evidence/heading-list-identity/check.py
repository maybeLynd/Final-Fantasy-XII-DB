"""Read-only original-code check of the two effect-instance list walks.

Run from the repository root with the pinned analysis Python. This checks
structural paths, never live reachability or a surviving individual pointer.
"""
import hashlib
import json
import sys
from pathlib import Path

import capstone

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PARENT = Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
sys.path.insert(0, str((PARENT / 'python-deps').resolve()))
import pefile

EXE = Path('Database/Tools/work/exe/FFXII_TZA.exe')
CAT = PARENT / 'retained/functions.tsv'
PRIOR = Path('Database/FFXII TZA/_experiments/evidence/heading-class-effects-slice/raw-commit-operation.json')
PRIOR_PUBLISH = Path('Database/FFXII TZA/_experiments/evidence/heading-class-effects-slice/raw-render-position-commit-boundaries.json')
S47 = Path('Database/FFXII TZA/_index/candidates/s47-opus-replay-24ed80/result.json')
EFFECT_PAGE = Path('Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md')
EXPECTED_EXE = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
TARGETS = (0x3A8D80, 0x3A8390, 0x3A9490, 0x3B3CA0, 0x43EF40, 0x43EE70, 0x2F3910)


def sha(data):
    return hashlib.sha256(data).hexdigest()


image = EXE.read_bytes()
assert sha(image) == EXPECTED_EXE, 'certified shipping image mismatch'
manifest = {m['path']: m for m in json.loads((PARENT / 'manifest.json').read_bytes())['members']}
assert sha(CAT.read_bytes()) == manifest['retained/functions.tsv']['sha256'], 'catalogue changed'
assert sha(Path(pefile.__file__).read_bytes()) == manifest['python-deps/pefile.py']['sha256']
cat = {}
for line in CAT.read_text(encoding='utf-8').splitlines()[1:]:
    cells = line.split('\t')
    try:
        address = int(cells[0], 16)
    except ValueError:
        continue
    if address in TARGETS:
        cat[address] = int(cells[2])
assert set(cat) == set(TARGETS)
pe = pefile.PE(str(EXE), fast_load=True)
assert pe.OPTIONAL_HEADER.ImageBase == 0x120000
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cs.detail = True
ins = {}
bodies = {}
for entry in TARGETS:
    size = cat[entry]
    offset = pe.get_offset_from_rva(entry - pe.OPTIONAL_HEADER.ImageBase)
    body = image[offset:offset + size]
    decoded = list(cs.disasm(body, entry))
    assert len(body) == size and decoded and decoded[0].address == entry
    assert sum(row.size for row in decoded) == size, f'short decode at {entry:08X}'
    ins.update((row.address, row) for row in decoded)
    bodies[f'{entry:08X}'] = {'bytes': size, 'sha256': sha(body), 'decoded_instructions': len(decoded)}
    if entry in (0x3A8390, 0x43EF40) and '--write' in sys.argv:
        (HERE / f'{entry:08X}.bin').write_bytes(body)

prior = json.loads(PRIOR.read_bytes())
retained = next(row for row in prior['callees'] if row['entry'] == '0x3a9490')
assert bodies['003A9490']['sha256'] == retained['code_sha256'], 'prior source differs'
prior_publish = json.loads(PRIOR_PUBLISH.read_bytes())
retained_publish = next(row for row in prior_publish['callees'] if row['entry'] == '0x3b3ca0')
assert bodies['003B3CA0']['sha256'] == retained_publish['code_sha256'], 'prior publication source differs'
assert S47.exists(), 'S-47 original-code publication dependency missing'


def row(pc, mnemonic):
    item = ins[pc]
    assert item.mnemonic == mnemonic, (hex(pc), item.mnemonic, mnemonic)
    return item


def reg(pc, op_index):
    item = ins[pc]
    op = item.operands[op_index]
    assert op.type == capstone.CS_OP_REG
    return item.reg_name(op.reg)


def mem(pc, op_index):
    item = ins[pc]
    op = item.operands[op_index]
    assert op.type == capstone.CS_OP_MEM
    return item.reg_name(op.mem.base), op.mem.disp


def rip(pc, op_index):
    base, disp = mem(pc, op_index)
    assert base == 'rip'
    return pc + ins[pc].size + disp


def call(pc):
    item = row(pc, 'call')
    assert item.operands[0].type == capstone.CS_OP_IMM
    return item.operands[0].imm


# Original register flow into each list. The 003A8D80 path is a pre-existing
# positive control; 003A8390 is the update path; 003A9490 is the flag path.
roots = [rip(0x3A8D84, 1), rip(0x3A83BD, 1), rip(0x3A949A, 1)]
heads = [mem(0x3A8D8B, 1), mem(0x3A83C4, 1), mem(0x3A94A3, 1)]
currents = [rip(0x3A8DA4, 0), rip(0x3A83E0, 0)]
owner_next = [mem(0x3A8DA0, 1), mem(0x3A83D6, 1), mem(0x3A94F7, 1)]
node_heads = [mem(0x3A94D0, 1), mem(0x43EF9B, 1)]
node_next = [mem(0x3A94EE, 1), mem(0x43EFB0, 1)]
assert roots == [0x2EBEF88] * 3 and currents == [0x2EBEF80] * 2
assert heads == [('rcx', 8), ('rax', 8), ('rax', 8)]
assert owner_next == [('rcx', 8), ('rbx', 8), ('rdi', 8)]
assert node_heads == [('rdi', 0x118), ('rdi', 0x118)]
assert node_next == [('rbx', 0x30), ('rcx', 0x30)]

# Follow the two real call boundaries. The 003A8390 caller loads its instance
# into RBX, then RCX; 0043EF40 preserves it in RDI and passes each node as RCX.
assert (reg(0x3A83DD, 0), reg(0x3A83DD, 1), call(0x3A83E7)) == ('rcx', 'rbx', 0x43EF40)
assert (reg(0x43EF60, 0), reg(0x43EF60, 1)) == ('rdi', 'rcx')
assert (reg(0x43EFB7, 0), reg(0x43EFB7, 1), call(0x43EFBA)) == ('rdx', 'rdi', 0x2F3910)
assert mem(0x2F3910, 1) == ('rcx', 0)
assert (reg(0x3A94E3, 0), reg(0x3A94E3, 1)) == ('rdx', 'rdi')
assert (reg(0x3A94E6, 0), reg(0x3A94E6, 1), call(0x3A94E9)) == ('rcx', 'rbx', 0x43EE70)
assert mem(0x43EE70, 1) == ('rcx', 0)
assert mem(0x3A94BD, 1) == ('rax', 0x44)
assert (call(0x3B3CE0), call(0x3B3CE7), call(0x3B3CFD)) == (0x24ED80, 0x3A9490, 0x24ED80)
assert (reg(0x3B3CEC, 0), reg(0x3B3CEC, 1)) == ('rcx', 'rdi')

# These are private in-memory instruction-byte controls, not modified game
# input. Re-decode altered bytes through the same Capstone path so the actual
# parser plus discriminator reject same-count alternative operands.
def equal_values(values):
    return len(set(values)) == 1


wrong_root_bytes = bytearray(ins[0x3A949A].bytes)
assert wrong_root_bytes.hex() == '488b05e75ab102'
wrong_root_bytes[3] += 8
wrong_root = next(cs.disasm(bytes(wrong_root_bytes), 0x3A949A))
assert wrong_root.size == ins[0x3A949A].size
wrong_root_operand = wrong_root.operands[1]
assert wrong_root_operand.type == capstone.CS_OP_MEM
wrong_root_target = wrong_root.address + wrong_root.size + wrong_root_operand.mem.disp

wrong_link_bytes = bytearray(ins[0x3A94EE].bytes)
assert wrong_link_bytes.hex() == '488b5b30'
wrong_link_bytes[-1] += 8
wrong_link = next(cs.disasm(bytes(wrong_link_bytes), 0x3A94EE))
assert wrong_link.size == ins[0x3A94EE].size
wrong_link_operand = wrong_link.operands[1]
assert wrong_link_operand.type == capstone.CS_OP_MEM

controls = {
    'known_registry_root': roots[0] == 0x2EBEF88,
    'same_count_wrong_root_rejected': not equal_values([roots[0], roots[1], wrong_root_target]),
    'same_count_wrong_link_rejected': not equal_values([node_next[0][1], wrong_link_operand.mem.disp]),
}
assert all(controls.values())

selected = (0x3A8D84, 0x3A8DA4, 0x3A83BD, 0x3A83C4, 0x3A83D6, 0x3A83DD,
            0x3A83E0, 0x3A83E7, 0x3A949A, 0x3A94A3, 0x3A94BD, 0x3A94D0,
            0x3A94E3, 0x3A94E6, 0x3A94E9, 0x3A94EE, 0x3A94F7,
            0x3B3CBE, 0x3B3CE0, 0x3B3CE7, 0x3B3CEC, 0x3B3CFD, 0x43EF60,
            0x43EF9B, 0x43EFB0, 0x43EFB7, 0x43EFBA, 0x43EE70, 0x2F3910)
evidence = [{'pc': f'{pc:08X}', 'bytes': ins[pc].bytes.hex(),
             'instruction': ins[pc].mnemonic + ' ' + ins[pc].op_str} for pc in selected]
result = {
    'status': 'STATIC_SHARED_REGISTRY_AND_CHAIN', 'method': 'A; original shipping bytes read-only',
    'exe_sha256': EXPECTED_EXE, 'catalogue_sha256': sha(CAT.read_bytes()),
    'prior_raw_sha256': sha(PRIOR.read_bytes()),
    'prior_publish_raw_sha256': sha(PRIOR_PUBLISH.read_bytes()),
    'prior_s47_original_code_result_sha256': sha(S47.read_bytes()),
    'effect_page_sha256': sha(EFFECT_PAGE.read_bytes()),
    'driver_sha256': sha(Path(__file__).read_bytes()),
    'python_sha256': sha(Path(sys.executable).read_bytes()),
    'capstone_version': capstone.__version__, 'capstone_sha256': sha(Path(capstone.__file__).read_bytes()),
    'pefile_sha256': sha(Path(pefile.__file__).read_bytes()),
    'body_identities': bodies, 'roots': [f'{x:08X}' for x in roots],
    'current_instance_slots': [f'{x:08X}' for x in currents],
    'instance_head_offsets': [x[1] for x in heads],
    'instance_next_offsets': [x[1] for x in owner_next],
    'element_head_offsets': [x[1] for x in node_heads],
    'element_next_offsets': [x[1] for x in node_next],
    'selected_original_instructions': evidence, 'controls': controls,
    'limit': ('Static structural alias of registry/list paths. 003B3CA0 calls 0024ED80 '
              'before and after the setter, and that publisher can change the slot contents. '
              'Not same pointer at two times, '
              'initialized identity, scheduling, native effects, full-body semantic closure or live consequence.'),
}
if '--write' in sys.argv:
    (HERE / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'roots': result['roots'],
                  'element_heads': result['element_head_offsets'],
                  'element_next': result['element_next_offsets'], 'controls': controls,
                  'selected_instructions': len(evidence)}, indent=2))
