#!/usr/bin/env python3
"""field_disp_scan.py - every instruction whose memory operand displacement is one of the given
values, decoded from every function entry in functions.tsv (never a linear sweep).

Bounded, single-offset instrument for FABLE-EE2: who reads/writes unit +0xE98 / +0xE99 / +0x6A0.
A control displacement whose reader/writer is already known must be found or the scan is refused.

Usage: field_disp_scan.py --funcs functions.tsv --disp 0xe98 0xe99 --control 0xe98:00239710:w
"""
import argparse, csv, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402
from disasm_fn import Image, DEFAULT_EXE
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP

ap = argparse.ArgumentParser()
ap.add_argument("--exe", default=DEFAULT_EXE)
ap.add_argument("--funcs", required=True)
ap.add_argument("--disp", nargs="+", required=True)
ap.add_argument("--control", required=True, help="disp:entry:r|w that must be found")
ap.add_argument("--out", required=True)
a = ap.parse_args()

disps = {int(x, 16) for x in a.disp}
img = Image(a.exe)
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

funcs = []
with open(a.funcs, encoding="utf-8", newline="") as f:
    rd = csv.reader(f, delimiter="\t")
    hdr = next(rd)
    ie = hdr.index("entry"); ib = hdr.index("body_bytes") if "body_bytes" in hdr else hdr.index("size")
    for row in rd:
        try:
            funcs.append((int(row[ie], 16), int(row[ib])))
        except ValueError:
            continue

# The chained-tails extent rule (2026-09-30): the shared function list's extents grow to their adjudicated errata ends
# (uc1_band.apply_extents); a fixture list is scanned exactly as given.
EXTENT_INFO = None
if os.path.realpath(a.funcs) == os.path.realpath(os.path.join(KP.WORK, "graph", "functions.tsv")):
    import uc1_band
    _g, EXTENT_INFO = uc1_band.apply_extents(dict(funcs))
    funcs = sorted(_g.items())

# ---- r/w classifier ---------------------------------------------------------
# Capstone folds prefixes into the mnemonic ("lock xadd"); strip them before lookup.
_MNEM_PREFIXES = ("lock ", "rep ", "repe ", "repne ", "repz ", "repnz ",
                  "bnd ", "notrack ", "xacquire ", "xrelease ")


def _base_mnem(mn):
    again = True
    while again:
        again = False
        for p in _MNEM_PREFIXES:
            if mn.startswith(p):
                mn = mn[len(p):]
                again = True
    return mn


# memory operand at position 0 is a pure store destination
_STORE = {"mov", "movss", "movsd", "movaps", "movapd", "movups", "movupd",
          "movdqa", "movdqu", "movd", "movq", "movhps", "movlps", "movhpd", "movlpd",
          "movntps", "movntpd", "movntdq", "movntq", "movntss", "movntsd", "movnti",
          "movbe", "maskmovdqu", "maskmovq",
          "pextrw", "pextrb", "pextrd", "pextrq", "extractps",
          "stmxcsr", "vstmxcsr", "fstcw", "fnstcw", "fstenv", "fnstenv",
          "fnsave", "fsave", "xsave", "xsavec", "xsaveopt", "xsaves",
          "fst", "fstp", "fist", "fistp", "fisttp", "fbstp", "pop", "stos", "movs",
          "sgdt", "sidt", "sldt", "str", "smsw", "vmptrst", "vmwrite",
          "vmovss", "vmovsd", "vmovaps", "vmovapd", "vmovups", "vmovupd",
          "vmovdqa", "vmovdqu", "vmovd", "vmovq", "vmovhps", "vmovlps",
          "vmovhpd", "vmovlpd", "vmovntps", "vmovntpd", "vmovntdq", "vmovnti",
          "vpextrw", "vpextrb", "vpextrd", "vpextrq", "vextractps"}
# memory operand at position 0 is read-modified-written
_RMW = {"and", "or", "xor", "add", "sub", "adc", "sbb", "inc", "dec", "not", "neg",
        "shl", "shr", "sar", "rol", "ror", "rcl", "rcr", "btr", "bts", "btc",
        "xadd", "xchg", "cmpxchg", "cmpxchg8b", "cmpxchg16b"}
# reads the memory operand even when it sits at position 0
# (one-operand forms div/idiv/mul/imul, indirect branches, push, compares, loads)
_READ = {"cmp", "test", "bt", "comiss", "comisd", "ucomiss", "ucomisd",
         "div", "idiv", "mul", "imul", "call", "jmp", "push",
         "movzx", "movsx", "movsxd", "cvtsi2ss", "cvtsi2sd", "cvttss2si", "cvttsd2si",
         "ldmxcsr", "vldmxcsr", "fldcw", "fldenv", "fxrstor", "xrstor", "xrstors", "lddqu",
         "fld", "fild", "fbld", "fadd", "fmul", "fsub", "fdiv", "fsubr", "fdivr",
         "fiadd", "fimul", "fisub", "fidiv", "fisubr", "fidivr",
         "fcom", "fcomp", "fcompp", "fucom", "fucomp", "fucompp", "ficom", "ficomp",
         "faddp", "fmulp", "fsubp", "fdivp", "fsubrp", "fdivrp",
         "prefetchnta", "prefetcht0", "prefetcht1", "prefetcht2", "prefetchw", "prefetch",
         "clflush", "clflushopt", "clwb", "clzero", "invlpg",
         "lgdt", "lidt", "lldt", "ltr", "lmsw", "vmread", "vmptrld", "vmclear", "vmxon",
         "scas", "lods", "cmps"}
# does not access memory at all (lea computes an address)
_NOACCESS = {"lea"}


def _kind(ins, i, mn):
    """kind for the memory operand at operand index i."""
    if mn in _NOACCESS:
        return "a"
    if mn in _RMW:
        return "rw" if i == 0 else "r"
    if mn in _STORE or mn.startswith("set"):
        return "w" if i == 0 else "r"
    if mn in _READ or mn.startswith("cmov"):
        return "r"
    # neither list: count it (printed below); '?' so no claim can consume it silently
    return "?" if i == 0 else "r"


rows = []
unknown = {}
for entry, size in funcs:
    if size <= 0:
        continue
    code = img.read(entry, size)
    if not code:
        continue
    for ins in md.disasm(code, entry):
        for i, op in enumerate(ins.operands):
            if op.type != X86_OP_MEM:
                continue
            m = op.mem
            if m.base in (X86_REG_RIP, X86_REG_RSP, X86_REG_RBP) or m.disp not in disps:
                continue
            mn = _base_mnem(ins.mnemonic)
            kind = _kind(ins, i, mn)
            if kind == "?":
                unknown.setdefault(mn, [0, "%08X" % ins.address])
                unknown[mn][0] += 1
            rows.append(("%08X" % entry, "%08X" % ins.address, "0x%x" % m.disp, kind,
                         ins.mnemonic + " " + ins.op_str, "reg%d" % m.base, "idx" if m.index else ""))

with open(a.out, "w", encoding="utf-8", newline="\n") as f:
    f.write("function\tsite\tdisp\tkind\tinstruction\tbase\tindexed\n")
    for r in rows:
        f.write("\t".join(r) + "\n")

cd, ce, ck = a.control.split(":")
hit = [r for r in rows if r[2] == "0x%x" % int(cd, 16) and r[0] == ce.upper() and ck in r[3]]
if not hit:
    sys.stderr.write("CONTROL MISSING: %s -- scan refused\n" % a.control)
    sys.exit(2)
print("control ok:", hit[0])
print("rows:", len(rows), "functions scanned:", len(funcs))
if EXTENT_INFO is not None:
    print(uc1_band.describe_extents(EXTENT_INFO))
for d in sorted(disps):
    sub = [r for r in rows if r[2] == "0x%x" % d]
    print("disp 0x%x: %d sites in %d functions; writers: %s" % (
        d, len(sub), len({r[0] for r in sub}),
        sorted({r[0] for r in sub if "w" in r[3]})))
print("unclassified op0 mnemonics (kind '?'):", sum(n for n, _ in unknown.values()))
for mn, (n, first) in sorted(unknown.items(), key=lambda kv: -kv[1][0]):
    print("  %-24s %5d  first at %s" % (mn, n, first))
