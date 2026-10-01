"""Who starts the SECOND widget transition - the one bit 1 of +0x80 drives?

002468A0 starts the first: it sets bit 0 and writes the bases +0x84/+0x86. The stepper 00246C20
reads bases +0x88/+0x8A for the second and clears bit 1 when it finishes, so something sets bit
1 and writes those two. Three instruments have not found it, because all three start from the
widget: the handler census, one level of arg0 callees, and the owner side. This one starts from
the INSTRUCTION SHAPE instead and then has to earn the base.

THE SHAPE. 002468A0's signature moves are `or byte ptr [rbx+0x80], 1` and `mov word ptr
[rbx+0x84], cx`. Its sibling should do the same with 2 and +0x88. So this scans every function
in the image for a write at displacement +0x88 or +0x8A, and separately for an OR of an
immediate into +0x80, and reports the functions that do BOTH - which is a far smaller set than
either alone.

WHY A MATCH IS ONLY A CANDIDATE. A displacement is not a type: plenty of unrelated structures
have a +0x80 and a +0x88. A candidate is confirmed only by the same standard CORE uses - a
caller that provably passes a widget, or an internal act only a widget permits, such as
dispatching through [obj]. Both tests are applied and reported per candidate, and the script
concludes nothing on its own.

THE CONTROL. The same scan, run for bit 0 and +0x84, must return 002468A0 - the function whose
shape the search was built from. If it cannot rediscover the known one, the shape is wrong.

WHAT IT FOUND, 2026-09-19, recorded so the next reader starts from the answer. EXACTLY ONE
function in all 38,161 bodies matches: 00247130, and it mirrors 002468A0 instruction for
instruction on the +0x9C/+0x9E pair - `test byte [rcx+0x80], 0xD` where the other tests 0xE (so
bits 0 and 1 are MUTUALLY EXCLUSIVE), `or byte [rcx+0x80], 2`, bases at +0x88/+0x8A, the same
shared deltas, the same milliseconds-to-frames idiom, the same clock and rate. It also writes
the OTHER pair's bases as sums - base98 = current98 + current9C - which is what makes the
stepper's bit-8 branch preserve `+0x98 + +0x9C` across the transition.

AND IT WAS STILL NOT ADMITTED TO THE CENSUS SEED, which is the part worth keeping. Its only
caller passes RCX through from `mov rcx, qword ptr [rsi + 0xd0]` inside a handler - a field of
the DERIVED widget type, above the shared header, which nothing declares. A body that mirrors an
admitted function exactly is an IDENTIFICATION, not a proof of the argument, and this kit keeps
those apart. Shape finds candidates; only a caller or an internal act confirms one.

THE NAME SAYS `scan_`, NOT `check_`: it is not a gate, and run_gates.py collects `check_*`.
"""
import collections
import io
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP

DB = "C:/Users/Kristian/source/repos/XIIOnline/Database"
EXE = DB + "/Tools/work/exe/FFXII_TZA.exe"
FUNCS = DB + "/Tools/work/graph/functions.tsv"

raw = open(EXE, "rb").read()
pe = struct.unpack_from("<I", raw, 0x3C)[0]
ns = struct.unpack_from("<H", raw, pe + 6)[0]
opt = struct.unpack_from("<H", raw, pe + 20)[0]
ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
off, secs = pe + 24 + opt, []
for _ in range(ns):
    nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
    vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((nm, ib + va, vs, rs, pr))
    off += 40


def fo(x):
    for nm, va, vs, rs, pr in secs:
        if va <= x < va + vs and (x - va) < rs:
            return pr + (x - va)
    return None


funcs = []
with io.open(FUNCS, encoding="utf-8") as fh:
    next(fh)
    for ln in fh:
        c = ln.rstrip("\n").split("\t")
        if len(c) >= 3:
            try:
                funcs.append((int(c[0], 16), int(c[2])))
            except ValueError:
                pass

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def body(entry, n):
    f = fo(entry)
    return [] if (f is None or n <= 0) else list(md.disasm(raw[f:f + n], entry))


def scan(base_disps, or_imm):
    out = []
    for entry, n in funcs:
        ins = body(entry, n)
        base_w, or_hit, dispatches = [], [], False
        for i in ins:
            ops = i.operands
            if not ops:
                continue
            o0 = ops[0]
            if (o0.type == X86_OP_MEM and o0.mem.base and o0.mem.base != X86_REG_RIP
                    and o0.mem.index == 0):
                if o0.mem.disp in base_disps and i.mnemonic == "mov" and o0.size == 2:
                    base_w.append((i.address, "%s %s" % (i.mnemonic, i.op_str)))
                elif (o0.mem.disp == 0x80 and i.mnemonic == "or" and len(ops) == 2
                        and ops[1].type == X86_OP_IMM and ops[1].imm == or_imm):
                    or_hit.append((i.address, "%s %s" % (i.mnemonic, i.op_str)))
            # dispatching through [obj]: `mov rax,[reg]` then `call rax` is the widget proc call
            if (i.mnemonic == "call" and ops and ops[0].type == X86_OP_REG):
                dispatches = True
        if base_w and or_hit:
            out.append((entry, base_w, or_hit, dispatches))
    return out


print("CONTROL  the same shape for bit 0 and +0x84/+0x86 must return 002468A0")
ctrl = scan({0x84, 0x86}, 1)
for e, bw, oh, d in ctrl:
    print("  %08X  %d base write(s), %d `or ..,1`, dispatches-through-register=%s"
          % (e, len(bw), len(oh), d))
print("  002468A0 present: %s" % any(e == 0x2468A0 for e, _, _, _ in ctrl))

print()
print("THE SEARCH  functions that write +0x88 or +0x8A as a word AND `or [reg+0x80], 2`")
hits = scan({0x88, 0x8A}, 2)
if not hits:
    print("  none. The second transition's starter does not have 002468A0's shape.")
for e, bw, oh, d in hits:
    print("  %08X  dispatches-through-register=%s" % (e, d))
    for a, t in oh:
        print("        %08X  %s" % (a, t))
    for a, t in bw:
        print("        %08X  %s" % (a, t))

print()
print("WIDER  any function that writes +0x88 or +0x8A as a word at all")
wide = collections.defaultdict(list)
for entry, n in funcs:
    for i in body(entry, n):
        ops = i.operands
        if (ops and ops[0].type == X86_OP_MEM and ops[0].mem.base
                and ops[0].mem.base != X86_REG_RIP and ops[0].mem.index == 0
                and ops[0].mem.disp in (0x88, 0x8A) and i.mnemonic == "mov"
                and ops[0].size == 2):
            wide[entry].append((i.address, "%s %s" % (i.mnemonic, i.op_str)))
print("  %d functions" % len(wide))
for e in sorted(wide):
    print("  %08X  %s" % (e, " | ".join("%08X %s" % x for x in wide[e][:3])))
