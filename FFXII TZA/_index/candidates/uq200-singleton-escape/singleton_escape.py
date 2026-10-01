"""singleton_escape.py - UQ-200: can anything write the render singleton's +0x1C / +0x1D other than the writers
already found? (FABLE, Claude Opus 5.5, 2026-09-26)

The singleton (0xDD8 bytes) lives at [01F7F598]. The published receiver census followed one hop: calls made with the
getter's result in rcx, 47 functions. This instrument follows the POINTER to a fixpoint instead.
- Entry points: every call of the getter 00189120 (the pointer arrives in rax) and every rip-relative load of
  [01F7F598].
- In each body the pointer is tracked forward:
  - bindings survive register copies and stack spills; a spill slot is tracked and reloaded;
  - a binding dies when its register is redefined, and volatile registers die across a call.
- Every call or tail-jump that carries the pointer in rcx, rdx, r8 or r9 queues the callee with that parameter. The
  callee is tracked the same way, until no new (function, register) pair appears.
- Two conservative rules close blind spots, at the price of false candidates that are read by hand:
  - after a call that carried the pointer, rax is treated as the pointer again, because a callee may return this;
  - one level of indirection is followed. A stack slot holding the pointer, including the {ptr, u32} pair filled by
    005DC190, whose ADDRESS is passed to a callee makes that callee track loads through the parameter.
The instrument records:
  E1 escapes: stores of the pointer to non-stack memory. Each one found was read by hand, and the seven are named in
     the check: three home-space spills through an rsp alias, three stores of a table element that the conservative
     rax rule over-reads, and the stack pair initialiser, which is followed as a pointer-to-pointer.
  E2 every write through the pointer at +0x1C / +0x1D, at byte or word width, with its source operand. There are
     exactly four: 00185A1D writes 1 (pass A), 001860E6 writes 0 (pass B), 0018A0EA writes 0 (the method that runs
     only at 0), and 00189560 is the per-pass +0x1D setter.
  E3 indirect branches that carry the pointer. The two reached are verified slot reuses: memcpy copying a rewritten
     scratch slot, and a callback object stored over the slot before 0060B980.
  C  controls (sensitivity):
     - C1 the same tracker, started at the lazy creator's allocation (00189000, pointer in rax after its allocator
       call), reports the store of the new object into [01F7F598] as an escape;
     - C2 E2 finds the two writers the one-hop receiver census published: the per-pass +0x1D setter and the zeroing
       method;
     - C3 the constructor's zeroing of +0x1C at 00184F59 is matched by the same store test;
     - C4 the pass-command constructor 001F1E80 copies byte +0x1C into the command's +0x20.
Result for UQ-200: the one-hop census keyed on `call` and missed two tail-jump forwarders (001821F0 into 00185A10,
00182340 into 001860E0). Through them +0x1C is set to 1 before pass A's command is built from +0x358, and cleared
before pass B's from +0x690. It is a pass selector, not a count.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, collections, csv, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + optsz + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
F = {}
for r in list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]:
    try: F[int(r[0], 16)] = int(r[2])
    except (ValueError, IndexError): pass
_c = {}
def body(f):
    if f not in _c: _c[f] = list(cs.disasm(d[off(f):off(f) + F[f]], f)) if f in F and off(f) is not None else []
    return _c[f]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
GET, SLOT = 0x189120, 0x01F7F598
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
ARGS = ("rcx", "rdx", "r8", "r9")
FULL = {}
for a, b in (("eax", "rax"), ("ebx", "rbx"), ("ecx", "rcx"), ("edx", "rdx"), ("esi", "rsi"), ("edi", "rdi"), ("ebp", "rbp"),
             ("ax", "rax"), ("al", "rax"), ("bx", "rbx"), ("bl", "rbx"), ("cx", "rcx"), ("cl", "rcx"), ("dx", "rdx"), ("dl", "rdx"),
             ("si", "rsi"), ("di", "rdi"), ("sil", "rsi"), ("dil", "rdi"), ("bp", "rbp"), ("bpl", "rbp")):
    FULL[a] = b
for k in range(8, 16):
    for s in ("d", "w", "b"): FULL["r%d%s" % (k, s)] = "r%d" % k
full = lambda nm: FULL.get(nm, nm)
WRITE = ("mov", "add", "sub", "inc", "dec", "or", "and", "xor", "movzx")
def track(f, start, regs, out, pregs=()):
    """Track the pointer through f's body from instruction index start; append findings to out; return new pairs.
    regs hold the pointer; pregs hold the ADDRESS of a slot whose first qword is the pointer."""
    L = body(f); held = set(regs); spills = set(); nxt = set(); pheld = set(pregs); pslots = set(); lea_of = {}
    for x in L[start:]:
        ops = x.operands; m = x.mnemonic
        if m == "ret": break
        # a load through a pointer-to-pointer re-binds: mov reg, [preg]
        if m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM \
                and full(cs.reg_name(ops[1].mem.base)) in pheld and ops[1].mem.disp == 0 and ops[1].size == 8:
            held.add(full(cs.reg_name(ops[0].reg))); continue
        # lea of a slot known to hold the pointer makes a pointer-to-pointer
        if m == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM and cs.reg_name(ops[1].mem.base) in ("rsp", "rbp") \
                and (cs.reg_name(ops[1].mem.base), ops[1].mem.disp) in pslots | spills:
            pheld.add(full(cs.reg_name(ops[0].reg))); continue
        if m == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM and cs.reg_name(ops[1].mem.base) in ("rsp", "rbp"):
            lea_of[full(cs.reg_name(ops[0].reg))] = (cs.reg_name(ops[1].mem.base), ops[1].mem.disp)
        if m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM \
                and cs.reg_name(ops[1].mem.base) in ("rsp", "rbp") and ops[1].mem.index == 0 \
                and (cs.reg_name(ops[1].mem.base), ops[1].mem.disp) in spills:
            held.add(full(cs.reg_name(ops[0].reg))); continue
        if m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_REG \
                and full(cs.reg_name(ops[1].reg)) in held and ops[1].size == 8:
            base = cs.reg_name(ops[0].mem.base)
            if base in ("rsp", "rbp") and ops[0].mem.index == 0: spills.add((base, ops[0].mem.disp))
            else: out["escape"].append("%08X %s %s" % (x.address, m, x.op_str))
            continue
        if ops and ops[0].type == X86_OP_MEM and full(cs.reg_name(ops[0].mem.base)) in held and ops[0].mem.disp in (0x1C, 0x1D) \
                and ops[0].size <= 2 and m in WRITE:
            out["write"].append("%08X %s %s" % (x.address, m, x.op_str))
        if m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG \
                and full(cs.reg_name(ops[1].reg)) in held and ops[0].size == 8:
            held.add(full(cs.reg_name(ops[0].reg))); continue
        if m in ("call", "jmp"):
            tgt = ops[0].imm if ops and ops[0].type == X86_OP_IMM else None
            internal = m == "jmp" and tgt is not None and f <= tgt < f + F.get(f, 0)
            if not internal:
                carried = [p for p in ARGS if p in held]
                pcarried = [p for p in ARGS if p in pheld]
                # 005DC190(pair, ptr) stores ptr as the pair's first qword: the pair's stack slot now holds the pointer
                if tgt == 0x5DC190 and "rdx" in held and "rcx" in lea_of: pslots.add(lea_of["rcx"])
                if pcarried and tgt is not None:
                    for p in pcarried: nxt.add((tgt, "*" + p))
                if pcarried and tgt is None: out["indirect"].append("%08X %s %s (pointer-to-pointer)" % (x.address, m, x.op_str))
                if carried:
                    if tgt is None: out["indirect"].append("%08X %s %s" % (x.address, m, x.op_str))
                    else:
                        for p in carried: nxt.add((tgt, p))
                if m == "jmp": break
                held -= VOL; pheld -= VOL
                # a callee that received the pointer may return it (a constructor or a fluent method returns this):
                # conservatively treat rax as the pointer again, so a returned alias is followed, not lost
                if carried: held.add("rax")
                if not held and not spills: break
                continue
        try:
            _, wr = x.regs_access()
            for r in wr:
                nm = full(cs.reg_name(r))
                if nm in held: held.discard(nm)
                if nm in pheld: pheld.discard(nm)
                lea_of.pop(nm, None)
        except Exception:
            pass
    return nxt
out = collections.defaultdict(list)
entries = []
for f in F:
    L = body(f)
    for i, x in enumerate(L):
        ops = x.operands
        if x.mnemonic == "call" and ops and ops[0].type == X86_OP_IMM and ops[0].imm == GET:
            entries.append((f, i + 1, "rax"))
        elif x.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM \
                and cs.reg_name(ops[1].mem.base) == "rip" and x.address + x.size + ops[1].mem.disp == SLOT:
            entries.append((f, i + 1, full(cs.reg_name(ops[0].reg))))
seen = set(); work = []
for f, i, r in entries:
    work += list(track(f, i, [r], out))
while work:
    t, p = work.pop()
    if (t, p) in seen or t not in F: continue
    seen.add((t, p))
    work += list(track(t, 0, [] if p.startswith("*") else [p], out, [p[1:]] if p.startswith("*") else []))
print("   entry points %d; callees reached with the pointer %d (functions %d)" % (len(entries), len(seen), len({t for t, _ in seen})))
# Read by hand and named here rather than excused silently:
#  00190263 / 001930F3  mov [rax+0x20], r9 right after mov rax, rsp: a home-space spill through an rsp alias (stack);
#  0018EF3E/4E/90       store the RETURN of 001867B0(singleton), which is a table element, not this (the conservative
#                       rax rule over-approximates here);
#  005DC192             the {ptr, u32} pair initialiser: every caller passes a stack temporary as the pair, and the
#                       pair is followed below as a pointer-to-pointer.
READ = {"00190263 mov qword ptr [rax + 0x20], r9", "001930F3 mov qword ptr [rax + 0x20], r9", "00190763 mov qword ptr [rax + 0x18], r8", "0018EF3E mov qword ptr [rdi], rax",
        "0018EF4E mov qword ptr [rdi + 8], rax", "0018EF90 mov qword ptr [rdi + 0x10], rax", "005DC192 mov qword ptr [rcx], rdx"}
unread = sorted(set(out["escape"]) - READ)
check("E1 every store of the pointer to non-stack memory is one of the seven read by hand", unread == [], str(unread[:6]))
# The tracker's spill slots are flow-insensitive, so a slot that held the pointer once and is later REUSED still
# counts. Two such reuses were read by hand and are verified here, byte for byte:
#  - 00190260 passes &[rbp-0x79] to memcpy at 0019042F and 00190614. The slot is rewritten first, by movss at 001903F1
#    and by a dword 0 at 001905DC, so the copies read scratch. The import thunk's jmp [IAT] (00861EBA) is that memcpy.
#  - 00191560 passes &[rsp+0x60] to 0060B980 at 001918D2 and 00191B25, right after storing a callback object's vtable
#    (008C6C98) there at 001918AE and 00191B01. So the chain 0060B980 -> 006B6410 -> _Init_thread_header carries no
#    singleton, and the latter's import call at 0080930C is not a route.
B1 = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in body(0x190260)}
B2 = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in body(0x191560)}
reuse = (B1.get(0x1903F1) == "movss dword ptr [rbp - 0x79], xmm0" and B1.get(0x1905DC) == "mov dword ptr [rbp - 0x79], 0"
         and B1.get(0x19042B) == "lea rdx, [rbp - 0x79]" and B1.get(0x190610) == "lea rdx, [rbp - 0x79]"
         and B2.get(0x1918A7, "").startswith("lea rcx, [rip + ") and B2.get(0x1918AE) == "mov qword ptr [rsp + 0x60], rcx"
         and B2.get(0x191B01) == "mov qword ptr [rsp + 0x60], rcx" and B2.get(0x1918CA) == "lea r8, [rsp + 0x60]")
KNOWN_IND = {"00861EBA jmp qword ptr [rip + 0x60ba8] (pointer-to-pointer)", "0080930C call qword ptr [rip + 0xb8da6] (pointer-to-pointer)"}
check("E3 the only indirect branches reached are the two explained by verified slot reuse",
      set(out["indirect"]) <= KNOWN_IND and reuse, "%s; reuse verified %s" % (sorted(set(out["indirect"]) - KNOWN_IND), reuse))
W = sorted(set(out["write"]))
for w in W: print("   E2 write:", w)
EXPECT = {"00185A1D mov byte ptr [rcx + 0x1c], 1",    # pass A: set before the +0x358 pass command is built
          "001860E6 mov byte ptr [rcx + 0x1c], 0",    # pass B: cleared before the +0x690 pass command is built
          "0018A0EA mov byte ptr [rsi + 0x1c], 0",    # the 1,083-byte method that runs only while the byte is 0
          "00189560 mov byte ptr [rcx + 0x1d], dl"}   # the per-pass +0x1D setter
check("E2 the writers of +0x1C / +0x1D are exactly the four known sites (one writes 1)", set(W) == EXPECT,
      "extra %s missing %s" % (sorted(set(W) - EXPECT), sorted(EXPECT - set(W))))
# controls
c1 = collections.defaultdict(list)
L = body(0x189000); ai = next((i for i, x in enumerate(L) if x.mnemonic == "call" and x.operands[0].type == X86_OP_IMM
                               and x.operands[0].imm == 0x210EC0), None)
if ai is not None: track(0x189000, ai + 1, ["rax"], c1)
check("C1 sensitivity: started at the lazy creator's allocation, the tracker reports the store into [01F7F598]",
      any("[rip +" in e for e in c1["escape"]), str(c1["escape"][:3]))
check("C2 the two writers the one-hop census published are among them: the +0x1D setter and the zeroing method",
      "00189560 mov byte ptr [rcx + 0x1d], dl" in W and "0018A0EA mov byte ptr [rsi + 0x1c], 0" in W)
# the pass commands capture the flag: 001F1E80 copies byte +0x1C of the singleton into the command's +0x20
X = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in body(0x1F1E80)}
check("C4 the pass-command constructor captures the flag into the command's +0x20",
      X.get(0x1F1EB2) == "call 0x189120" and X.get(0x1F1EB7) == "movzx edx, byte ptr [rax + 0x1c]" and X.get(0x1F1EBB) == "mov byte ptr [rdi + 0x20], dl")
ctor = [x for x in body(0x184F20) if x.address == 0x184F59]
check("C3 the constructor's word zeroing at 00184F59 is matched by the store test",
      bool(ctor) and ctor[0].mnemonic in WRITE and ctor[0].operands[0].mem.disp == 0x1C and ctor[0].operands[0].size == 2)
print("FAILS", fails)
sys.exit(1 if fails else 0)
