"""Specific 0x6B source proof; calls abstract only their normal-return edge."""
import hashlib
import json
import struct
import sys
from collections import deque
from pathlib import Path

import capstone

sys.dont_write_bytecode = True
DEPS = Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
PRIOR = Path('Database/FFXII TZA/_experiments/evidence/heading-source-consumers')
POLICY = Path('Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py')
sys.path.insert(0, str(POLICY.parent.resolve()))
import reg_tracking as roles
sys.path.insert(0, str((DEPS / 'python-deps').resolve()))
import pefile

EXE = Path('Database/Tools/work/exe/FFXII_TZA.exe')
EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
ENTRY, ZERO, COMPARE, STORE = 0x529D50, 0x529FEC, 0x52A063, 0x52A06C


def sha(b):
    return hashlib.sha256(b).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


image = EXE.read_bytes()
require(sha(image) == EXE_SHA, 'shipping image changed')
dep_members = {m['path']: m for m in json.loads((DEPS / 'manifest.json').read_bytes())['members']}
prior_members = {m['path']: m for m in json.loads((PRIOR / 'manifest.json').read_bytes())['members']}
prior_bytes = (PRIOR / 'node-reader-feasibility.json').read_bytes()
require(sha(prior_bytes) == prior_members['node-reader-feasibility.json']['sha256'],
        'prior source receipt changed')
require(sha(POLICY.read_bytes()) == dep_members['retained/reg_tracking.py']['sha256'],
        'shared adapter differs from reviewed policy')
require(Path(roles.__file__).resolve() == POLICY.resolve(), 'wrong adapter imported')
require(sha(Path(pefile.__file__).read_bytes()) == dep_members['python-deps/pefile.py']['sha256'],
        'PE reader differs from pinned provider')
row = next(r for r in json.loads(prior_bytes)['rows'] if r['step'] == '0x529d50')
size = int(row['step_catalogue'].split('\t')[2])
require(size == 917, 'prior captured size changed')
p = pefile.PE(data=image, fast_load=True)
require(p.OPTIONAL_HEADER.ImageBase == 0x120000, 'image base changed')
code = p.get_data(ENTRY - 0x120000, size)
require(sha(code) == row['step_bytes_sha256'], 'original body no longer matches prior capture')
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cs.detail = True


def decoded(data):
    ins = list(cs.disasm(data, ENTRY))
    require(ins and sum(i.size for i in ins) == size and ins[0].address == ENTRY,
            'incomplete original/control decode')
    return {i.address: i for i in ins}


def graph(ins):
    edges = {}
    exits = []
    for pc, i in ins.items():
        nxt = pc + i.size
        if i.mnemonic.startswith('j'):
            require(len(i.operands) == 1 and i.operands[0].type == capstone.CS_OP_IMM,
                    'unresolved indirect branch')
            dest = i.operands[0].imm
            if dest not in ins:
                require(i.mnemonic == 'jmp', 'conditional branch leaves captured body')
                exits.append({'pc': f'{pc:08X}', 'tail_target': f'{dest:08X}'})
                edges[pc] = []
            else:
                edges[pc] = [dest] if i.mnemonic == 'jmp' else [dest, nxt]
        elif i.mnemonic == 'ret':
            edges[pc] = []
        else:
            require(nxt in ins, 'nonterminal fallthrough leaves captured body')
            # Calls can fail/throw/not return. Only their normal-return edge is modelled.
            edges[pc] = [nxt]
        require(all(dst in ins for dst in edges[pc]), 'edge is not instruction aligned')
    return edges, exits


def path(edges, start, goal, omit=None):
    pending = deque([start])
    parents = {start: None}
    while pending:
        pc = pending.popleft()
        if pc == omit:
            continue
        if pc == goal:
            out = []
            while pc is not None:
                out.append(pc)
                pc = parents[pc]
            return out[::-1]
        for dst in edges[pc]:
            if dst not in parents:
                parents[dst] = pc
                pending.append(dst)
    return None


def zero_premise(ins, edges):
    i = ins[ZERO]
    return (i.mnemonic == 'xor' and i.op_str == 'r13d, r13d'
            and all(path(edges, ENTRY, pc) is not None
                    and path(edges, ENTRY, pc, omit=ZERO) is None
                    for pc in (COMPARE, STORE)))


original = decoded(code)
edges, exits = graph(original)
require(zero_premise(original, edges), 'original zero definition does not dominate both uses')
on_region = [pc for pc in original if path(edges, ZERO, pc) is not None
             and path(edges, pc, COMPARE) is not None and pc != ZERO]
local_r13_writes = [pc for pc in on_region if 'r13' in roles.written(original[pc])]
require(not local_r13_writes, 'local R13 definition before comparison')
require(original[COMPARE].mnemonic == 'cmp' and original[STORE].mnemonic == 'mov',
        'selected read/write instruction changed')
require(roles.op_kind(original[COMPARE], original[COMPARE].operands[0], 0) == 'r'
        and roles.op_kind(original[STORE], original[STORE].operands[0], 0) == 'w',
        'actual capture path read/store roles failed')
between_calls = [pc for pc in on_region if original[pc].mnemonic == 'call']
require(between_calls == [0x52A03A, 0x52A05E], 'unexpected zero-to-use call boundary')
require(all(original[pc].operands[0].imm == 0x533B20 for pc in between_calls),
        'normal-return dependency changed')

# The actual source conditional branch is privately redirected past the definition.
bypass = bytearray(code)
branch = 0x529E48
require(original[branch].bytes[:2] == b'\x0f\x84' and original[branch].size == 6,
        'wrong mutation preimage')
struct.pack_into('<i', bypass, branch - ENTRY + 2, COMPARE - (branch + 6))
bypass_ins = decoded(bypass)
bypass_edges, _ = graph(bypass_ins)
bypass_path = path(bypass_edges, ENTRY, COMPARE, omit=ZERO)
require(bypass_path is not None and not zero_premise(bypass_ins, bypass_edges),
        'same-size branch bypass control missed')
wrong_register = bytearray(code)
require(original[ZERO].bytes.hex() == '4533ed', 'wrong zero-instruction preimage')
wrong_register[ZERO - ENTRY:ZERO - ENTRY + 3] = bytes.fromhex('4533e4')
wrong_ins = decoded(wrong_register)
wrong_edges, _ = graph(wrong_ins)
require(not zero_premise(wrong_ins, wrong_edges), 'same-size wrong-register control missed')
require(len(original) == len(bypass_ins) == len(wrong_ins), 'control instruction counts differ')

# These use the identical imported adapter invoked on the actual source above.
role_controls = []
for encoded, expected in (('0f1101', 'w'), ('488d4108', 'addr'), ('f00fc101', 'rw')):
    i = next(cs.disasm(bytes.fromhex(encoded), 0x1000))
    observed = [roles.op_kind(i, o, n) for n, o in enumerate(i.operands)
                if o.type == capstone.CS_OP_MEM]
    require(observed == [expected], 'shared access-role detection control failed')
    role_controls.append({'bytes': encoded, 'instruction': i.mnemonic+' '+i.op_str,
                          'expected': expected, 'observed': observed})
require(sha(EXE.read_bytes()) == EXE_SHA, 'reference changed during read')
result = {
    'status': 'PRODUCER_CHECKED_STATIC_CONDITIONAL_ZERO', 'method': 'A',
    'question': 'Does the local zero definition dominate both request-field uses?',
    'identity': {'exe_sha256': EXE_SHA, 'prior_receipt_sha256': sha(prior_bytes),
                 'body_sha256': sha(code), 'body_size': size, 'body_hex': code.hex(),
                 'driver_sha256': sha(Path(__file__).read_bytes()),
                 'python': sys.version, 'capstone_version': capstone.__version__,
                 'pefile_sha256': sha(Path(pefile.__file__).read_bytes()),
                 'shared_policy_sha256': sha(POLICY.read_bytes()),
                 'shared_policy_actual_import': str(POLICY)},
    'normal_graph': {'instructions': len(original), 'edges': {f'{pc:08X}': [f'{d:08X}' for d in ds] for pc, ds in edges.items()},
                     'external_tail_boundaries': exits,
                     'zero_dominates_compare_and_store': True,
                     'local_r13_writes_zero_to_compare': [],
                     'zero_to_compare_call_dependencies': [f'{pc:08X}:00533B20' for pc in between_calls]},
    'selected_original': [{'pc': f'{pc:08X}', 'bytes': original[pc].bytes.hex(),
                          'instruction': original[pc].mnemonic+' '+original[pc].op_str}
                         for pc in (ZERO, COMPARE, 0x52A06A, STORE, 0x52A073, 0x52A08A, 0x52A08F, 0x52A093)],
    'private_controls_not_shipping_execution': {
        'branch_bypass': {'pc': f'{branch:08X}', 'before': original[branch].bytes.hex(),
                          'after': bypass_ins[branch].bytes.hex(), 'image_sha256': sha(bypass),
                          'bypass_path': [f'{pc:08X}' for pc in bypass_path], 'zero_premise_rejected': True},
        'wrong_register': {'pc': f'{ZERO:08X}', 'before': original[ZERO].bytes.hex(),
                           'after': wrong_ins[ZERO].bytes.hex(), 'image_sha256': sha(wrong_register),
                           'zero_premise_rejected': True}, 'roles': role_controls},
    'interpretation': 'Under normal entry/returns and callee R13 preservation, the local comparison uses zero and its unequal arm writes zero before the fixed-count extra transform loop.',
    'limits': ['The graph overapproximates direct branches; no concrete branch feasibility or execution measured.',
               'Calls supply only assumed normal-return edges, not proofs of native effects or ABI preservation.',
               'Valid node layout/receiver continuity, callee preservation, memory aliasing, scheduling and later field persistence remain conditions.',
               'Captured catalogue body is not inferred as a universal function extent from metadata.',
               'No live instance, visual result, class preservation or full L1/L2 completion established.',
               'Independent acceptance and authorized canonical incorporation remain pending.'],
    'cleanup': {'reference_unchanged': True, 'live_or_save_config_controls': False}}
print(json.dumps(result, indent=2))
