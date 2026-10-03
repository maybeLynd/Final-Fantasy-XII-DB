"""check_s22.py - FABLE, 2026-10-03, on SWE2-AUDIT-SPEC's L2 expansion (S-22, step table ST-4).

Claim checked: CONTRACT-formula-step-table.md section 3 calls 02AEE054/58/5C "the ONLY channel between steps", and
ST-4 says the steps "communicate only through the scratch record" meaning those three words (section 5: "the three
scratch words"). The corrected reading: the channel is the whole BattleFormulaScratch block (02AEDFB8, 0xA8); the
three words are its preparation-to-finalize part.

Static (S*), census (N*), executed (X*, unicorn 2.1.4, shipped bytes at their own addresses, no stub), controls (C*).
  C1 (sensitivity, executed): the OLD reading predicts that slot 40's outcome cannot depend on another step's write
     outside the three words. Running slot 21 before slot 40 must CHANGE slot 40's outcome with the three words held
     equal, so the old prediction must come out FALSE.
  C2 (positive, census): the census must find the three words themselves as cross-step cells (the known channel).
Prints PASS/FAIL lines and FAILS N last.
"""
import os
import struct
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP  # noqa: E402

DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TABLE = 0x01EFA5C0
SCR, SCR_LEN = 0x02AEDFB8, 0xA8
THREE = (0x02AEE054, 0x02AEE058, 0x02AEE05C)
HIT, ROLL, FAILED = 0x02AEDFE0, 0x02AEDFB8, 0x02AEDFBC
fails = 0


def report(ok, label, detail=""):
    global fails
    print("%s %s: %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        fails += 1


def one(img, va):
    return next(img.cs.disasm(img.read(va, 15), va, 1))


def rip_target(i):
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def static(img, slots):
    report(slots[21] == 0x00388F20 and slots[40] == 0x00389670, "S1 table: slot 21 -> 00388F20, slot 40 -> 00389670",
           "%08X %08X" % (slots[21], slots[40]))
    exp = [(0x00388F37, "mov", HIT, "slot 21 stores 100 (ctx +0x1C bit 2 set)"),
           (0x00388FA1, "mov", HIT, "slot 21 stores row+0x12 - target+0x2C + source+0x2B"),
           (0x0038968D, "cmp", HIT, "slot 40 compares the hit chance with draw % 100"),
           (0x00389696, "mov", FAILED, "slot 40 sets failed on a miss"),
           (0x003896A0, "mov", ROLL, "slot 40 sets rollOver on a miss")]
    for va, mn, tgt, why in exp:
        i = one(img, va)
        report(i.mnemonic == mn and rip_target(i) == tgt, "S2 %08X %s [%08X]" % (va, mn, tgt),
               "%s %s  (%s)" % (i.mnemonic, i.op_str, why))
    # the interpreter: the same three arguments are reloaded before every call, rax is not consumed
    loop = list(img.cs.disasm(img.read(0x003863C0, 0x28), 0x003863C0))
    txt = ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in loop]
    ok = (loop[1].mnemonic == "lea" and loop[1].op_str == "r8, [rsp + 0x48]" and loop[2].op_str == "rdx, rsi"
          and loop[3].op_str == "rcx, r14" and loop[4].address == 0x003863D0 and loop[4].mnemonic == "call"
          and loop[5].mnemonic == "cmp" and rip_target(loop[5]) == ROLL and "rax" not in loop[5].op_str
          and loop[0].mnemonic == "movsxd" and loop[0].op_str.startswith("rax"))
    tail = list(img.cs.disasm(img.read(0x003863E8, 0x15), 0x003863E8))
    ok = ok and tail[-1].address == 0x003863F8 and tail[-1].mnemonic == "call" and all(
        "rax" not in i.op_str and "eax" not in i.op_str for i in tail)
    report(ok, "S3 loop 003863C0..003863F8: args reloaded per call, rax overwritten or unread, [02AEDFB8]==1 stops it",
           " | ".join(txt[:7]) + " || exit " + " | ".join("%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in tail))
    # the type store
    types = open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8").read().splitlines()
    row = [r for r in types if r.startswith("BattleFormulaScratch\t")]
    report(len(row) == 1 and row[0].split("\t")[1] == "0xA8" and "02AEDFB8" in row[0],
           "S4 store: BattleFormulaScratch 0xA8 at 02AEDFB8", row[0][:80] if row else "missing")
    f = {}
    for r in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8").read().splitlines():
        c = r.split("\t")
        if c[0] == "BattleFormulaScratch":
            f[int(c[1], 16)] = c[3]
    want = {0x00: "rollOver", 0x04: "failed", 0x28: "hitChance", 0x9C: "multiplier", 0xA0: "attackVariance", 0xA4: "targetDefense"}
    report(all(f.get(k) == v for k, v in want.items()), "S5 store fields: +0x00 rollOver, +0x04 failed, +0x28 hitChance, +0x9C/+0xA0/+0xA4",
           ", ".join("+0x%02X %s" % (k, f.get(k)) for k in sorted(want)))


NOTW = {"cmp", "test", "bt", "ucomiss", "comiss", "lea", "call", "jmp", "push"}


def body(img, t):
    pd = img.pdata(t)
    if pd:
        return list(img.cs.disasm(img.read(pd[0], pd[1] - pd[0]), pd[0]))
    out, maxt = [], t
    for i in img.cs.disasm(img.read(t, 0x1000), t):
        out.append(i)
        if i.mnemonic.startswith("j") and i.operands and i.operands[0].type == X86_OP_IMM:
            if t <= i.operands[0].imm < t + 0x1000:
                maxt = max(maxt, i.operands[0].imm)
        if i.mnemonic in ("ret", "int3", "jmp") and i.address >= maxt:
            break
    return out


def census(img, slots):
    """Own bodies of the 152 distinct targets (callees NOT followed): rip-relative writes and reads per cell."""
    W, R = defaultdict(set), defaultdict(set)
    for t in sorted(set(slots)):
        for i in body(img, t):
            for k, op in enumerate(i.operands):
                if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP or i.mnemonic == "lea":
                    continue
                a = i.address + i.size + op.mem.disp
                w = k == 0 and i.mnemonic not in NOTW and not i.mnemonic.startswith("j")
                if w:
                    W[a].add(t)
                    if i.mnemonic not in ("mov", "movss", "movd"):
                        R[a].add(t)
                else:
                    R[a].add(t)
    cross = sorted(c for c in W if R[c] - W[c] and SCR <= c < SCR + SCR_LEN)
    return cross, W, R


# ---------------- unicorn ----------------
def emu(img):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_MEM_UNMAPPED
    import unicorn
    assert unicorn.__version__ == "2.1.4", unicorn.__version__
    pe = struct.unpack_from("<I", img.d, 0x3C)[0]
    size_img = struct.unpack_from("<I", img.d, pe + 24 + 56)[0]
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    uc.mem_map(img.base, (size_img + 0xFFF) & ~0xFFF)
    uc.mem_write(img.base, img.d[:0x1000])
    for name, sva, vs, ra, rs in img.secs:
        uc.mem_write(img.base + sva, img.d[ra:ra + min(rs, vs if vs else rs)])
    uc.mem_map(0x7FF00000, 0x100000)       # stack
    uc.mem_map(0x10000000, 0x10000)        # planted argument records
    uc.mem_map(0x0DEAD000, 0x1000)         # return sentinel
    st = {"fault": None}

    def unm(uc_, access, addr, size, value, ud):
        st["fault"] = addr
        return False
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, unm)
    return uc, st


def call_step(uc, st, target):
    from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8
    rsp = 0x7FFF0000
    uc.mem_write(rsp, struct.pack("<Q", 0x0DEAD000))
    uc.reg_write(UC_X86_REG_RSP, rsp)
    uc.reg_write(UC_X86_REG_RCX, 0x10000000)   # arg1
    uc.reg_write(UC_X86_REG_RDX, 0x10001000)   # arg2
    uc.reg_write(UC_X86_REG_R8, 0x10002000)    # arg3: context, +0x1C bit 2 set (slot 21's constant arm)
    try:
        uc.emu_start(target, 0x0DEAD000, count=2000000)
    except Exception as e:
        return "error %s fault %s" % (e, st["fault"])
    return "ok"


def rd(uc, va):
    return struct.unpack("<I", bytes(uc.mem_read(va, 4)))[0]


def run_case(img, with_slot21):
    uc, st = emu(img)
    uc.mem_write(0x10002000 + 0x1C, b"\x04")
    slots = [struct.unpack("<Q", bytes(uc.mem_read(TABLE + 8 * i, 8)))[0] for i in (21, 40)]
    r21 = call_step(uc, st, slots[0]) if with_slot21 else "not run"
    hit = rd(uc, HIT)
    three = tuple(rd(uc, a) for a in THREE)
    r40 = call_step(uc, st, slots[1])
    return {"slot21": r21, "hit_before_40": hit, "three_before_40": three, "slot40": r40,
            "rollOver": rd(uc, ROLL), "failed": rd(uc, FAILED)}


REPLAYS = {  # package: {output file: md5 recorded in the package at its commit}
    "s22-opus-replay-steps-and-element-scaling": {"check.py": {"result.json": "99336e052d1e386d671e9cee2c5b5426"}},
    "s22-opus-replay-recipe-resolver": {"check.py": {"result.json": "a226db98765feb8a1a5447f211c1d194"},
                                        "we1.py": {"we1_result.json": "5680857b37dea30c63e4dbdc9d214019"}},
    "s22-opus-replay-severe-weather-gate": {"check.py": {"result.json": "867bbaf3cc23ce50b3d38778aa27afb0"}},
}


def rerun_replays(names):
    """Copy each replay package to a temp dir (its scripts write next to themselves), run it with this interpreter,
    and compare the output's md5 with the committed file's and with the recorded value."""
    import hashlib, shutil, subprocess, tempfile
    cand = os.path.abspath(os.path.join(HERE, ".."))
    tmp = tempfile.mkdtemp(prefix="fable_l2exp_s22_")
    try:
        for name in names:
            src = os.path.join(cand, name)
            dst = os.path.join(tmp, name)
            shutil.copytree(src, dst)
            for script, outs in REPLAYS[name].items():
                pr = subprocess.run([sys.executable, script], cwd=dst, capture_output=True, text=True)
                for out, rec in outs.items():
                    got = hashlib.md5(open(os.path.join(dst, out), "rb").read()).hexdigest()
                    com = hashlib.md5(open(os.path.join(src, out), "rb").read()).hexdigest()
                    report(pr.returncode == 0 and got == com == rec, "RR %s/%s re-run reproduces %s" % (name, script, out),
                           "exit %d, re-run %s, committed %s, recorded %s" % (pr.returncode, got[:8], com[:8], rec[:8]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    img = Img.load()
    head = os.popen('git -C "%s" rev-parse --short HEAD' % DB).read().strip()
    print("check_s22.py  HEAD %s  image sha256 73461d08... (asserted by rvlib)" % head)
    slots = [img.u64(TABLE + 8 * i) for i in range(202)]
    static(img, slots)

    cross, W, R = census(img, slots)
    outside = [c for c in cross if c not in THREE]
    report(len(set(slots)) == 152, "N0 census denominator: 152 distinct targets", str(len(set(slots))))
    report(len(cross) == 15 and len(outside) == 12,
           "N1 census: 15 block cells written by one step and read by a different step, 12 outside the three words",
           "%d / %d: %s" % (len(cross), len(outside), " ".join("+%02X" % (c - SCR) for c in cross)))
    report(HIT in outside and ROLL in outside, "N2 census: +0x28 hit chance and +0x00 rollOver are among them",
           "+0x28 writers %d, other readers %d" % (len(W[HIT]), len(R[HIT] - W[HIT])))
    nonblock = sorted(c for c in W if R[c] - W[c] and not (SCR <= c < SCR + SCR_LEN))
    report(not nonblock, "N3 census: no cell outside the block is written by one step body and read by another",
           " ".join("%08X" % c for c in nonblock) or "none")
    report(all(c in cross for c in THREE), "C2 positive: the census finds the three words themselves",
           " ".join("%08X" % c for c in THREE))

    a = run_case(img, True)
    b = run_case(img, False)
    print("     X data: with slot 21 %s" % a)
    print("     X data: slot 40 alone %s" % b)
    report(a["slot21"] == "ok" and a["hit_before_40"] == 100, "X1 executed: slot 21 writes hit chance 02AEDFE0 = 100",
           "slot21 %s, [02AEDFE0] %d" % (a["slot21"], a["hit_before_40"]))
    report(a["slot40"] == "ok" and b["slot40"] == "ok" and a["three_before_40"] == b["three_before_40"],
           "X2 executed: slot 40 runs in both cases with the three words equal before it",
           "three words %s / %s" % (a["three_before_40"], b["three_before_40"]))
    report(a["rollOver"] == 0 and b["rollOver"] == 1 and b["failed"] == 1,
           "X3 executed: slot 40 stops the recipe only when slot 21 did not run first",
           "rollOver with 21: %d, without: %d (failed %d)" % (a["rollOver"], b["rollOver"], b["failed"]))
    old_prediction = (a["rollOver"], a["failed"]) == (b["rollOver"], b["failed"])
    report(not old_prediction, "C1 sensitivity: the OLD 'only the three words' reading predicts equal outcomes; it is FALSE",
           "outcomes %s vs %s" % ((a["rollOver"], a["failed"]), (b["rollOver"], b["failed"])))
    rerun_replays(list(REPLAYS))
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
