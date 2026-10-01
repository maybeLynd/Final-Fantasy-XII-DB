#!/usr/bin/env python3
"""S-24 probe (OPUS draft, 2026-09-25): does un-stubbing EXP-100's scripted
callees change what 0030FED0 leaves behind?

Reuses EXP-100's own fixture builder (World) from
_experiments/evidence/auto-status-gates-exec/check.py, read-only, and runs
the shipped 0030FED0 in three configurations:

  STUB   EXP-100's boundary: FIND, APPLY 0030E130, CASCADE 0030E360,
         NOTIFY 002FEF30, TAIL 0030E060 all `ret` stubs.
  APPLY  as STUB, but APPLY 0030E130 runs as shipped bytes, together with
         its closure (00322C50 arm 0x1D, 00386AE0/00386A50 builders,
         003848E0, 00384B10, 0030EA40, cookie). Bridges/stubs added:
           - IAT 008C2A60 (VCRUNTIME140!memset)  -> fixture rep-stosb   [import bridge]
           - IAT 008C3098 (ucrt!rand)            -> fixture `mov eax,0x1234; ret` [import bridge]
           - 003112F0 (the mega-dispatcher APPLY reaches when the builder
             leaves result+0x2C bit0 set)         -> logged ret-0        [application stub]
           - [02EBF040] -> fixture table, count 0x80 (APPLY's arm-0x1D gate)  [fixture]
  NOTIFY as STUB, but NOTIFY 002FEF30 runs as shipped bytes (its closure
         0020E600/00322C50/0031E9A0/002F8E50/002F9180 real; FIND stays the
         EXP-100 stub returning the planted unit).

For every run it prints: final RIP, whether the return sentinel RETQ was
reached, the emulator fault list, entry counts for the functions of
interest, and the record fields the question is about.
"""
import importlib.util, json, os, struct, sys
sys.dont_write_bytecode = True   # do not leave a __pycache__ in the evidence dir
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RIP, UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RAX

HERE = os.path.dirname(os.path.abspath(__file__))
EXP100 = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "_experiments", "evidence",
    "auto-status-gates-exec", "check.py"))
spec = importlib.util.spec_from_file_location("exp100", EXP100)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

HOOKS0 = dict(m.HOOKS)
BRIDGE = 0x63000000
F22T = m.HEAP + 0x380000
IAT_MEMSET, IAT_RAND = 0x8C2A60, 0x8C3098
MEMSET_CODE = bytes.fromhex("57" "4889cf" "4989c9" "89d0" "4c89c1" "f3aa" "4c89c8" "5f" "c3")
RAND_CODE = bytes.fromhex("b834120000" "c3")
WATCH = {0x30FED0: "FED(rebuild)", 0x30E130: "APPLY", 0x2FEF30: "NOTIFY",
         0x3112F0: "3112F0", 0x386AE0: "builder_AE0", 0x386A50: "builder_A50",
         0x3105D0: "RESET", 0x307D10: "SINK", 0x384B10: "384B10",
         0x30E360: "CASCADE", 0x30E060: "TAIL"}


def run(case, real):
    stubs = [m.FIND, m.CASCADE, m.TAIL]
    hooks = dict(HOOKS0)
    for name, va in (("APPLY", m.APPLY), ("NOTIFY", m.NOTIFY)):
        if name in real:
            hooks.pop(va, None)
        else:
            stubs.append(va)
    m.STUBS, m.HOOKS = tuple(stubs), hooks
    w = m.World(case, m.RAW, m.SECS)
    uc, gm = w.uc, w.gm
    gm.map(BRIDGE, 0x1000)
    gm.w(BRIDGE, MEMSET_CODE)
    gm.w(BRIDGE + 0x40, RAND_CODE)
    gm.w(IAT_MEMSET, m.qw(BRIDGE))
    gm.w(IAT_RAND, m.qw(BRIDGE + 0x40))
    gm.w(0x2EBF040, m.qw(F22T))
    gm.w(F22T + 4, m.dw(0x80))
    counts = {}
    x78_writes = []

    def cnt(uc_, addr, size, _):
        counts[WATCH[addr]] = counts.get(WATCH[addr], 0) + 1
        if addr == 0x3112F0:
            w._ret(0)
    for a in WATCH:
        uc.hook_add(UC_HOOK_CODE, cnt, begin=a, end=a)

    def on_w(uc_, access, addr, size, value, _):
        x78_writes.append(("%X" % addr, size, value & 0xFF,
                           "%X" % uc_.reg_read(UC_X86_REG_RIP)))
    uc.hook_add(UC_HOOK_MEM_WRITE, on_w, begin=m.REC + 0x78, end=m.REC + 0x87)

    sp = m.STACK + 0x80000
    gm.w(sp, m.qw(m.RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, m.REC)
    uc.reg_write(UC_X86_REG_RDX, case.get("flags", 0))
    err = None
    try:
        uc.emu_start(m.SUBJ, m.RETQ, count=5_000_000)
    except Exception as e:
        err = str(e)
    rip = uc.reg_read(UC_X86_REG_RIP)
    return {
        "config": "+".join(sorted(real)) or "STUB",
        "final_rip": "%X" % rip,
        "reached_return_sentinel": rip == m.RETQ,
        "emu_error": err,
        "faults": w.faults,
        "rax": "%X" % uc.reg_read(UC_X86_REG_RAX),
        "entries": counts,
        "trace": " ".join(w.trace),
        "rec+0x24_maxhp": struct.unpack("<i", gm.r(m.REC + 0x24, 4))[0],
        "rec+0x28_w": struct.unpack("<h", gm.r(m.REC + 0x28, 2))[0],
        "rec+0x3C": "%08X" % struct.unpack("<I", gm.r(m.REC + 0x3C, 4))[0],
        "rec+0x48_hp": struct.unpack("<i", gm.r(m.REC + 0x48, 4))[0],
        "rec+0x4C_mp": struct.unpack("<h", gm.r(m.REC + 0x4C, 2))[0],
        "rec+0x68": gm.r(m.REC + 0x68, 16).hex(),
        "rec+0x78": gm.r(m.REC + 0x78, 16).hex(),
        "writes_to_rec+0x78..0x87": x78_writes,
    }


def main():
    m.RAW, m.SECS = m.load_image()
    W = dict(m.W, owns=1, has_spawn=True)
    pr = [0] * 16
    pr[0] = 0x0F
    cases = [
        # Q1: does +0x78 equal the accumulation on return once APPLY is real?
        dict(W, name="diff-add-rem (EXP-100 case)", kind=0, prior=pr, def_m0=0x3),
        dict(W, name="def-masks (EXP-100 case)", kind=0, row_idx=0, def_m0=0x5, def_m1=0x3),
        # Q2: do the clamp caps come from NOTIFY once NOTIFY is real?
        dict(W, name="clamp-hp (EXP-100 case)", kind=0, hp=100, maxhp=50),
        dict(W, name="clamp-hp, planted maxhp 500", kind=0, hp=100, maxhp=500),
        dict(W, name="clamp-mp (EXP-100 case)", kind=0, mp=100, stat28=0x20),
    ]
    plan = [(0, ["STUB", "APPLY"]), (1, ["STUB", "APPLY"]),
            (2, ["STUB", "NOTIFY"]), (3, ["STUB", "NOTIFY"]), (4, ["STUB", "NOTIFY"])]
    out = []
    for ci, cfgs in plan:
        for cfg in cfgs:
            real = set() if cfg == "STUB" else {cfg}
            r = run(cases[ci], real)
            r["case"] = cases[ci]["name"]
            out.append(r)
            print(json.dumps(r, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
