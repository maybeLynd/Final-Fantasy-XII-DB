import hashlib, importlib.util, json, struct, sys
from pathlib import Path
import capstone, unicorn
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.x86_const import *

W = Path(__file__).resolve().parent
R = W / 'retained'
R.mkdir(exist_ok=True)
original = Path('Database/FFXII TZA/_experiments/evidence/navgrid-query-exec/check.py')
if not (R / 'check.py').exists():
    (R / 'check.py').write_bytes(original.read_bytes())
helper = R / 'check.py'
spec = importlib.util.spec_from_file_location('retained_exp131', helper)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
raw, secs = m.load_image()
sha = lambda b: hashlib.sha256(b).hexdigest()
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cs.detail = True
bodies = []
instructions = {}
for a, n in [(0x383F10, 542), (0x20E600, 10), (0x382D10, 391)]:
    b = m.img_rd(raw, secs, a, n)
    ii = list(cs.disasm(b, a))
    assert sum(i.size for i in ii) == n and ii[-1].mnemonic == 'ret'
    bodies.append(dict(entry=hex(a), size=n, sha256=sha(b), raw_hex=b.hex(),
        instructions=[dict(pc=hex(i.address), bytes=i.bytes.hex(), op=i.mnemonic, args=i.op_str) for i in ii]))
    instructions.update({i.address: i for i in ii})
assert instructions[0x383FAF].mnemonic == instructions[0x383FCD].mnemonic == 'ja'
assert instructions[0x38402C].bytes.hex() == '410fb70c41'
assert m.img_rd(raw, secs, 0x383FB0, 1) == m.img_rd(raw, secs, 0x383FCE, 1) == b'\x87'
iat = m.FDCIAT
source = dict(method='B isolated original code; synthetic EXP131 fixture; finite _fdclass stub disclosed',
    exe_path=m.EXE, exe_sha256=sha(raw), image_base=hex(m.IMG_LO),
    python_version=sys.version, python_executable=sys.executable,
    python_sha256=sha(Path(sys.executable).read_bytes()),
    unicorn_version=unicorn.__version__, capstone_version=capstone.__version__,
    helper_original=original.as_posix(), helper_retained='retained/check.py', helper_sha256=sha(helper.read_bytes()),
    bodies=bodies, fdclass_iat=hex(iat), fdclass_trampoline=hex(m.FDC),
    stub_limits='Existing host fdclass_f32 on finite f32 arguments only; not shipping CRT instructions/effects.',
    declared_cells=8, grid_header_hex=m.mesh_bytes({})[m.GHDR:m.GHDR+16].hex())
(W / 'source.json').write_text(json.dumps(source, indent=2) + '\n')

def frombits(v): return struct.unpack('<f', struct.pack('<I', v))[0]
cases = [
    dict(name='origin-control', x=0.0, z=0.0),
    dict(name='interior-control', x=1.0, z=1.0),
    dict(name='x-upper-minus-ulp', x=frombits(0x40FFFFFF), z=0.0),
    dict(name='x-upper-equal', x=8.0, z=0.0),
    dict(name='x-upper-equal-next-row-list', x=8.0, z=0.0, next_row=True),
    dict(name='x-upper-plus-ulp', x=frombits(0x41000001), z=0.0, guard=True),
    dict(name='guard-last-cell-control', x=7.0, z=3.0, guard=True),
    dict(name='guard-x-upper-equal-last-row', x=8.0, z=3.0, guard=True),
    dict(name='guard-z-upper-minus-ulp', x=1.0, z=frombits(0x407FFFFF), guard=True),
    dict(name='guard-z-upper-equal', x=1.0, z=4.0, guard=True),
    dict(name='guard-z-upper-plus-ulp', x=1.0, z=frombits(0x40800001), guard=True),
    dict(name='guard-corner-equal', x=8.0, z=4.0, guard=True),
    dict(name='mutant-x-ja-to-jae', x=8.0, z=3.0, guard=True, mutation=0x383FB0),
    dict(name='mutant-z-ja-to-jae', x=1.0, z=4.0, guard=True, mutation=0x383FCE),
]
NV = [UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI,
      UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15]
observations = []
for case in cases:
    fixture = dict(ptx=case['x'], pty=case['z'])
    w = m.World(fixture, raw, secs)
    uc = w.uc
    table = m.BASEP + m.CMAP
    if case.get('guard'):
        table = m.HEAP + 0x100000 - 16
        w.gm.w(table, b''.join(m.ww(c) for c in m.CELLS))
        w.gm.w(m.BASEP+m.GHDR+8, m.dw(table-m.BASEP))
    if case.get('next_row'):
        w.gm.w(table+8, m.ww(0x11))
    if case.get('mutation'):
        w.gm.w(case['mutation'], b'\x83')
    pcs, reads = [], []
    def on_code(uc, pc, size, _): pcs.append(pc)
    def on_read(uc, access, address, size, value, _):
        if uc.reg_read(UC_X86_REG_RIP) == 0x38402C:
            try: b = w.gm.r(address, size).hex()
            except KeyError: b = None
            reads.append(dict(pc='0x38402c', address=hex(address), size=size, bytes=b,
                              index=(address-table)//2))
    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_READ, on_read)
    rsp = m.STACK + 0x80008
    w.gm.w(rsp, m.qw(m.RETQ))
    uc.reg_write(UC_X86_REG_RSP, rsp)
    uc.reg_write(UC_X86_REG_RCX, m.PT)
    uc.reg_write(UC_X86_REG_MXCSR, 0x1F80)
    for j, reg in enumerate(NV): uc.reg_write(reg, 0xABC000+j)
    before_nv = [uc.reg_read(reg) for reg in NV]
    try: uc.emu_start(m.GGRID, m.RETQ, count=2000)
    except unicorn.UcError as e:
        if not w.faults: w.faults.append(('emuerr', str(e)))
    obs = dict(case=case, table=hex(table), header_hex=w.gm.r(m.BASEP+m.GHDR,16).hex(),
        table_hex=w.gm.r(table,16).hex(), point_hex=w.gm.r(m.PT,8).hex(),
        starting_rsp=hex(rsp), starting_mxcsr='0x1f80', instruction_budget=2000,
        pcs=[hex(pc) for pc in pcs], instructions=len(pcs), cell_reads=reads,
        stub_trace=w.trace, faults=w.faults, end_pc=hex(uc.reg_read(UC_X86_REG_RIP)),
        rax=uc.reg_read(UC_X86_REG_RAX), ending_rsp=hex(uc.reg_read(UC_X86_REG_RSP)),
        ending_mxcsr=hex(uc.reg_read(UC_X86_REG_MXCSR)),
        nonvolatile_before=[hex(n) for n in before_nv],
        nonvolatile_after=[hex(uc.reg_read(reg)) for reg in NV])
    observations.append(obs)
    print(case['name'], 'read', [(q['index'],q['bytes']) for q in reads],
          'ret',obs['rax'],'faults',obs['faults'],'end',obs['end_pc'], flush=True)
(W/'raw.json').write_text(json.dumps(observations, indent=2)+'\n')
