"""falsify_script_resume.py - falsification pass 1 on 01-Script-VM-Native-Bridge/Interpreter-Core/
the-script-from-bytecode-through-wait-and-resume.md (OPUS, 2026-09-30). Static; reads only the shipping image.

The page's claims rest on SECTION-11's isolated executions. This pass attacks the static facts those executions
depend on, at the interpreter's own instructions and tables:
R1  §2 the evaluation stack depth at 02099AC0 is reset on every interpreter entry
R2  §6 the loop budget is 65,536
R3  §6 the opcode dispatch: 100 opcodes (00..63) through one image-relative table; anything above falls to a default
R4  §6 the length table: 0 for opcodes 00..02, 1 for 03..47, 3 for 48..63
R5  §6 opcode 03 sets actor flag 0x40 and cancels its advance
R6  §6 0025E60A sets a stop request; 0025E613 advances without newly setting it; opcode 19 is the stop marker
R7  §5 a result is appended only while depth < 63
R8  §4 the result writers address the issuing request as actor+0xA8 + sign_extend(actor+0x11) * 0x28
R9  §4 the wait poll reads 02099011 + sign_extend(index) * 0x288
R10 §6 opcode 47 reads PC+2 and PC+1
"""
import collections, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402
from capstone import x86 as X  # noqa: E402

at, md, ext, BASE = R.at, R.md, R.ext, R.b.BASE
INTERP = 0x0025E4C0
DEPTH = 0x02099AC0
results = []


def check(cid, ok, what):
    results.append((cid, ok))
    print("%-4s %-9s %s" % (cid, "SURVIVES" if ok else "BROKEN", what))


def rip(i):
    for op in i.operands:
        if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


body = list(md.disasm(at(INTERP, ext[INTERP]), INTERP))
ix = {i.address: k for k, i in enumerate(body)}

# R1: the first store to the depth global, and that its source register is zero at that point
first = next(i for i in body if rip(i) == DEPTH)
src = first.op_str.split(",")[-1].strip()
zeroed = any(i.mnemonic == "xor" and i.op_str == "%s, %s" % (src, src) for i in body[:ix[first.address]])
check("R1", first.mnemonic == "mov" and first.operands[0].type == X.X86_OP_MEM and zeroed,
      "first reference to 02099AC0 is %08X `%s %s`, source zeroed before it: %s" % (first.address, first.mnemonic, first.op_str, zeroed))

# R2
bud = [i for i in body if i.mnemonic == "mov" and i.op_str.endswith(", 0x10000")]
check("R2", bool(bud), "budget load: %s" % ", ".join("%08X %s" % (i.address, i.op_str) for i in bud))

# R3
d = next(i for i in body if i.mnemonic == "cmp" and i.op_str == "eax, 0x63")
ja = body[ix[d.address] + 1]
tab_ins = next(i for i in body[ix[d.address]:ix[d.address] + 6] if i.mnemonic == "mov" and "*4 +" in i.op_str)
TAB = BASE + tab_ins.operands[1].mem.disp
targets = [BASE + struct.unpack("<I", at(TAB + 4 * k, 4))[0] for k in range(100)]
default = ja.operands[0].imm
check("R3", ja.mnemonic == "ja" and all(INTERP <= t < INTERP + ext[INTERP] for t in targets),
      "cmp eax, 0x63 at %08X, ja -> %08X (default); table %08X, 100 targets all inside the interpreter: %s" % (
          d.address, default, TAB, all(INTERP <= t < INTERP + ext[INTERP] for t in targets)))

# R4: the advance word, read the way 0025E5FE / 0025E631 read it: word at BASE + 0x1DDEA60 + op * 24
adv_ins = next(i for i in body if i.mnemonic == "movsx" and "word ptr" in i.op_str and "*8 +" in i.op_str)
LEN = BASE + adv_ins.operands[1].mem.disp
lens = [struct.unpack("<h", at(LEN + 24 * op, 2))[0] for op in range(100)]
want = [0] * 3 + [1] * (0x48 - 3) + [3] * (0x64 - 0x48)
bad = [(hex(op), lens[op], want[op]) for op in range(100) if lens[op] != want[op]]
check("R4", not bad, "advance words at %08X + op*24 (read at %08X): %s" % (
    LEN, adv_ins.address, "all as stated" if not bad else "differ at %s" % bad[:8]))

# R5: opcode 03's arm
a3 = targets[3]
arm = list(md.disasm(at(a3, 0x40), a3))[:8]
t5 = ["%s %s" % (i.mnemonic, i.op_str) for i in arm]
check("R5", t5[0].startswith("or byte ptr [") and t5[0].endswith("+ 0x14], 0x40") and any(x.startswith("sub r14, ") for x in t5),
      "opcode 03 arm %08X: %s" % (a3, "; ".join(t5[:6])))

# R6: 0025E60A stores the stop request; 0025E613 is the next entry, which advances; opcode 19's arm
i60a, i613 = R.dec(0x0025E60A), R.dec(0x0025E613)
ebp_one = any(i.mnemonic == "mov" and i.op_str == "ebp, 1" for i in body[:ix[0x0025E60A]])
a19 = targets[0x19]
arm19 = list(md.disasm(at(a19, 0x30), a19))[:6]
reaches = a19 == 0x0025E60A or any(i.mnemonic == "jmp" and i.operands[0].type == X.X86_OP_IMM and i.operands[0].imm == 0x0025E60A for i in arm19)
check("R6", i60a.op_str == "dword ptr [rsp + 0xc0], ebp" and ebp_one and default == 0x0025E60A and reaches,
      "0025E60A `%s %s` (ebp = 1 before: %s; also the out-of-range default: %s); 0025E613 `%s %s`; opcode 19 -> %08X reaches 0025E60A: %s" % (
          i60a.mnemonic, i60a.op_str, ebp_one, default == 0x0025E60A, i613.mnemonic, i613.op_str, a19, reaches))

# R7: the lifecycle receives the stack by pointer (the interpreter's only call passes `lea` 02099AC0), reads depth as
# dword [rbx] and skips the append with `cmp eax, 0x3f` / `jge`
LIFE = 0x002621D0
lb = list(md.disasm(at(LIFE, ext[LIFE]), LIFE))
lx = {i.address: k for k, i in enumerate(lb)}
bounds = [i for i in lb if i.mnemonic == "cmp" and i.op_str == "eax, 0x3f" and lb[lx[i.address] + 1].mnemonic == "jge"]
depth_read = [i for i in lb if i.mnemonic == "movsxd" and i.op_str == "rax, dword ptr [rbx]"]
# the stack pointer argument at each of the interpreter's calls, by the value-flow engine (r8 is often a copy of r10,
# loaded by `lea r10, [02099AC0]` far earlier)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "k14-closure-stores-0930"))
import k14_actorflow as KF  # noqa: E402
arg_at = {}


class ArgSpy(KF.Analysis):
    def summary(self, f, ctx, depth, stack):
        return (KF.UNK, ())

    def call(self, f, st, i, t, depth, stack, caller_writes):
        if t == LIFE:
            v = st.r.get("r8", KF.UNK)
            arg_at[i.address] = KF.join(arg_at[i.address], v) if i.address in arg_at else v
        return KF.Analysis.call(self, f, st, i, t, depth, stack, caller_writes)


ArgSpy().run(INTERP, {}, 0, (INTERP,))
calls = sorted(arg_at)
passes = [arg_at[a] == KF.vs(("G%08X" % DEPTH, 0)) for a in calls]
check("R7", len(bounds) >= 2 and bool(depth_read) and calls and all(passes),
      "002621D0: depth read `movsxd rax, dword [rbx]` at %s; bounds `cmp eax, 0x3f / jge` at %s; the interpreter's %d call(s) pass lea 02099AC0: %s" % (
          " ".join("%08X" % i.address for i in depth_read), " ".join("%08X" % i.address for i in bounds), len(calls), passes))

# R8: image-wide, the request address actor+0xA8 + sx(actor+0x11)*0x28
hits = []
for f in sorted(ext):
    b = list(md.disasm(at(f, ext[f]), f))
    for k, i in enumerate(b):
        if i.mnemonic == "movsx" and "byte ptr [" in i.op_str and i.op_str.endswith("+ 0x11]"):
            win = b[k + 1:k + 8]
            s28 = any(("0x28" in w.op_str and w.mnemonic in ("imul", "lea")) or (w.mnemonic == "lea" and "*4]" in w.op_str) or
                      (w.mnemonic == "shl" and w.op_str.endswith(", 3")) for w in win)
            a8 = any("+ 0xa8]" in w.op_str for w in b[max(0, k - 8):k + 10])
            if s28 and a8:
                hits.append((f, i.address))
check("R8", bool(hits), "sites loading sx(byte [r + 0x11]) with a 0x28 stride beside [r + 0xA8]: %d in %d functions (%s)" % (
    len(hits), len(set(f for f, _ in hits)), " ".join("%08X" % f for f in sorted(set(f for f, _ in hits))[:10])))

# R9: the wait poll's indexed byte
w = []
for f in sorted(ext):
    for i in md.disasm(at(f, ext[f]), f):
        t = rip(i)
        if t is not None and t in (0x02099011, 0x02099000, 0x02099010):
            w.append((f, i.address, i.mnemonic, i.op_str, t))
has288 = set()
for f, a, *_ in w:
    b = list(md.disasm(at(f, ext[f]), f))
    if any("0x288" in i.op_str for i in b):
        has288.add(f)
check("R9", any(t == 0x02099011 for *_, t in w) and bool(has288),
      "references to 02099011: %d in %d functions; functions pairing it with a 0x288 stride: %s" % (
          sum(1 for *_, t in w if t == 0x02099011), len(set(f for f, *_ , t in w if t == 0x02099011)),
          " ".join("%08X" % f for f in sorted(has288)[:8])))

# R10: opcode 47 reads PC+2 and PC+1: the operand decode before dispatch runs for every opcode >= 0x47 while the
# length table gives 0x47 an advance of 1 (R4); its table entry is the default arm
dec = [i for i in body if i.mnemonic == "cmp" and i.op_str == "r12b, 0x47"]
k = ix[dec[0].address] if dec else None
nxt = ["%s %s" % (i.mnemonic, i.op_str) for i in body[k + 1:k + 5]] if dec else []
ok10 = bool(dec) and nxt[0].startswith("jb ") and "movzx ebx, byte ptr [r14 + 2]" in nxt and "movzx eax, byte ptr [r14 + 1]" in nxt and lens[0x47] == 1
check("R10", ok10, "pre-dispatch decode at %s: %s; advance of opcode 47 = %d; its table entry %08X" % (
    "%08X" % dec[0].address if dec else "-", "; ".join(nxt), lens[0x47], targets[0x47]))

broken = [c for c, ok in results if not ok]
print("BROKEN %d: %s" % (len(broken), " ".join(broken) or "none"))
sys.exit(0)
