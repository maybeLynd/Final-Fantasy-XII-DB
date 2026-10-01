"""Bounded original-byte reader scan; candidate offsets are not receiver proof."""
import hashlib, json, sys, types
from pathlib import Path

import capstone

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
P = Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
X = Path('Database/Tools/work/exe/FFXII_TZA.exe')
OUT = W / 'node-reader-feasibility.json'
TARGETS = [(0x45fd00, 0x45fd10, 0x3d8), (0x529d40, 0x529d50, 0x3d4),
           (0x52a8a0, 0x52a8b0, 0x434), (0x52b5d0, 0x52b5e0, 0x3f8)]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

assert sha(X) == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
manifest = {m['path']: m for m in json.loads((P/'manifest.json').read_bytes())['members']}
for name in ('retained/functions.tsv', 'retained/reg_tracking.py', 'python-deps/pefile.py'):
    assert sha(P/name) == manifest[name]['sha256']
sys.path.insert(0, str((P/'python-deps').resolve()))
import pefile

roles = types.ModuleType('roles')
policy = P/'retained/reg_tracking.py'
exec(compile(policy.read_bytes(), str(policy), 'exec'), roles.__dict__)
cat = {}
for line in (P/'retained/functions.tsv').read_text('utf-8').splitlines()[1:]:
    cells = line.split('\t')
    try: addr = int(cells[0], 16)
    except ValueError: continue
    if addr in {a for row in TARGETS for a in row[:2]}:
        cat[addr] = (int(cells[2]), line)
assert len(cat) == 8

pe = pefile.PE(str(X), fast_load=True)
assert pe.OPTIONAL_HEADER.ImageBase == 0x120000
image = X.read_bytes()
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cs.detail = True

def read_range(addr):
    size, catalogue = cat[addr]
    offset = pe.get_offset_from_rva(addr - pe.OPTIONAL_HEADER.ImageBase)
    code = image[offset:offset+size]
    assert len(code) == size
    ins = list(cs.disasm(code, addr))
    assert ins and ins[0].address == addr and sum(i.size for i in ins) == size
    return code, ins, catalogue

rows = []
for setter, step, displacement in TARGETS:
    setter_code, setter_ins, setter_cat = read_range(setter)
    step_code, step_ins, step_cat = read_range(step)
    stores = [(i.address, i.mnemonic, i.op_str) for i in setter_ins
              if any(o.type == capstone.CS_OP_MEM and o.mem.disp == displacement
                     and roles.op_kind(i, o, j) in ('w', 'rw')
                     for j, o in enumerate(i.operands))]
    assert len(stores) == 1 and stores[0][1] == 'mov', (hex(setter), stores)
    hits = []
    for i in step_ins:
        for j, o in enumerate(i.operands):
            if o.type == capstone.CS_OP_MEM and o.mem.disp == displacement:
                hits.append({'pc': hex(i.address), 'bytes': i.bytes.hex(),
                             'mnemonic': i.mnemonic, 'operands': i.op_str,
                             'operand': j, 'kind': roles.op_kind(i, o, j),
                             'base': cs.reg_name(o.mem.base), 'index': cs.reg_name(o.mem.index)})
    interesting = {int(h['pc'], 16) for h in hits}
    windows = []
    for n, i in enumerate(step_ins):
        if i.address in interesting:
            windows.append([{'pc': hex(q.address), 'bytes': q.bytes.hex(),
                             'instruction': q.mnemonic+' '+q.op_str}
                            for q in step_ins[max(0, n-7):min(len(step_ins), n+5)]])
    first_hit = min(interesting) if interesting else None
    prior_rbx_writes = [{'pc': hex(i.address), 'instruction': i.mnemonic+' '+i.op_str}
                        for i in step_ins if first_hit is not None and i.address < first_hit
                        and 'rbx' in roles.written(i)]
    if first_hit is not None:
        assert len(prior_rbx_writes) == 1 and prior_rbx_writes[0]['instruction'] == 'mov rbx, rcx', prior_rbx_writes
    rows.append({'setter': hex(setter), 'step': hex(step), 'offset': hex(displacement),
                 'setter_bytes_sha256': hashlib.sha256(setter_code).hexdigest(),
                 'step_bytes_sha256': hashlib.sha256(step_code).hexdigest(),
                 'setter_catalogue': setter_cat, 'step_catalogue': step_cat,
                 'store_control': [hex(stores[0][0]), stores[0][1], stores[0][2]],
                 'step_direct_offset_hits': hits,
                 'step_entry_instructions': [{'pc': hex(i.address), 'bytes': i.bytes.hex(),
                                              'instruction': i.mnemonic+' '+i.op_str}
                                             for i in step_ins[:16]],
                 'step_rbx_writes': [{'pc': hex(i.address), 'instruction': i.mnemonic+' '+i.op_str}
                                     for i in step_ins if 'rbx' in roles.written(i)],
                 'step_r13_writes': [{'pc': hex(i.address), 'instruction': i.mnemonic+' '+i.op_str}
                                     for i in step_ins if 'r13' in roles.written(i)],
                 'receiver_source_before_first_hit': prior_rbx_writes,
                 'calls_before_first_hit': [{'pc': hex(i.address), 'target': i.op_str}
                                            for i in step_ins if first_hit is not None
                                            and i.address < first_hit and i.mnemonic == 'call'],
                 'hit_windows': windows,
                 'step_calls': [{'pc': hex(i.address), 'target': i.op_str}
                                for i in step_ins if i.mnemonic == 'call']})
assert sha(X) == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
result = {'status': 'OFFSET_FEASIBILITY_ONLY', 'method': 'A; read-only original-byte decode',
          'exe_sha256': sha(X), 'driver_sha256': sha(Path(__file__)),
          'capstone_version': capstone.__version__, 'pefile_sha256': sha(Path(pefile.__file__)),
          'policy_sha256': sha(policy), 'rows': rows,
          'limits': 'Catalogued range decode and same displacement are not receiver provenance, complete caller effects, initialized lifetime, native execution or live scheduling. A no-hit result excludes only this direct-offset candidate.'}
if '--write-result' in sys.argv:
    OUT.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
