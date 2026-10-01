"""bank_sead_calls.py - control for BD-2 (FABLE, Claude Opus 5.5, 2026-09-26): what the audio bank classes do with sound.

For every slot body of the five concrete bank vtables and the AudioBank base (found by RTTI), follow direct calls and
jumps to depth 2 inside the bank range 00210000-00227000 and list every call/jump into SEAD's handle API
(007A4380-007AB460). Each API entry is classified by the command type it stamps into a queued command (the first
`mov dword ptr [rax], imm` after 007AB460 / 007BAD60), and each command type by the Sound vtable slot its drain arm
(jump table 007AC080 in 007AB5C0) calls. Sound's slots 2/3/4 are identified by the sequence state their per-sequence
step sets at +0x9C: slot 2 -> 3/4 (stop), slot 3 -> 5 (pause), slot 4 -> 2 (resume).
Known positive: the base slot 9 (00222340) must be found reaching 007A8590 and 007A7A20.

Revised 2026-09-26 (FABLE, Claude Opus 5.5). A body is now read only up to the next function start (functions.tsv).
The first version read to the first `ret`, which ran past Seb slot 2's tail `jmp` into the next functions and credited
that slot with the play wrapper 007A78B0 (N1 reproduces the defect as a sensitivity check). Checks N2-N6 identify the
two start commands: 007A78B0 posts 0xA for a type-2 handle and 0x1C for a type-8 handle. The drain starts a ready
Sound (007BDFA0, state +0x54 1 -> 2) or a ready Music (007C8370, state +0xC8 1 -> 2) with a fade-in ramp. The
wrapper's bank-range callers are five non-virtual functions, none of them a vtable slot.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
def q(v): return struct.unpack_from("<Q", d, off(v))[0]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
import bisect
STARTS = sorted(int(l.split("\t")[0], 16) for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8",
                errors="replace") if re.match(r"[0-9A-Fa-f]{8}\t", l))
def body(a, lim=0x400):
    """a's instructions up to its first ret/int3, and never past the next function start (functions.tsv): a body that
    ends in a tail jmp has no ret, and reading on would attribute the NEXT function's calls to it (2026-09-26 defect:
    Seb slot 2, a teardown ending in `jmp 00222000`, was credited with the play wrapper 007A78B0 that way)."""
    i = bisect.bisect_right(STARTS, a)
    end = min(a + lim, STARTS[i] if i < len(STARTS) else a + lim)
    out = []
    for x in cs.disasm(d[off(a):off(end)], a):
        out.append(x)
        if x.mnemonic in ("ret", "int3"): break
    return out
VT = {"AudioBank": 0x9078B0, "MusicAudioBank": 0x907910, "SepAudioBank": 0x907B48, "SebAudioBank": 0x907D80,
      "ShoutAudioBank": 0x907F90, "StreamAudioBank": 0x9081A0}
def targets(a):
    t = set()
    for x in body(a):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"): t.add(int(x.op_str, 16))
    return t
api = {}
for name, vt in VT.items():
    for s in range(11):
        f = q(vt + 8 * s)
        if not (0x210000 <= f < 0x227000): continue
        seen = {f}; frontier = [f]
        for depth in range(2):
            nxt = []
            for g in frontier:
                for t in targets(g):
                    if 0x7A4380 <= t < 0x7AB460: api.setdefault(t, set()).add("%s.slot%d" % (name, s))
                    elif 0x210000 <= t < 0x227000 and t not in seen: seen.add(t); nxt.append(t)
            frontier = nxt
def cmd_types(a):
    L = body(a, 0x200); types = []
    for i, x in enumerate(L):
        if x.mnemonic == "call" and x.op_str in ("0x7ab460", "0x7bad60"):
            for y in L[i + 1:i + 8]:
                m = re.match(r"dword ptr \[rax\], (0x[0-9a-f]+|\d+)$", y.op_str)   # capstone prints < 10 in decimal
                if y.mnemonic == "mov" and m: types.append((x.op_str, int(m.group(1), 0))); break
    return types
def arm_slot(t):
    a = BASE + struct.unpack_from("<I", d, off(0x7AC080) + 4 * t)[0]
    for x in body(a, 0x60):
        if x.mnemonic == "jmp": break          # the arm ends at its jmp to the drain's loop tail
        m = re.match(r"qword ptr \[rdx \+ (0x[0-9a-f]+)\]", x.op_str)
        if x.mnemonic == "call" and m: return int(m.group(1), 16) // 8
    return None
MEANING = {2: "stop (sequence state 3/4)", 3: "pause (sequence state 5)", 4: "resume (sequence state 2)"}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
for a in sorted(api):
    ts = cmd_types(a)
    desc = ", ".join("cmd %#x -> Sound slot %s = %s" % (t, arm_slot(t), MEANING.get(arm_slot(t), "?")) for via, t in ts if via == "0x7ab460")
    print("  %08X  from %-60s %s" % (a, ", ".join(sorted(api[a]))[:60], desc or "(no queued command: a direct call)"))
check("known positive: base slot 9 reaches 007A8590 and 007A7A20",
      "AudioBank.slot9" in api.get(0x7A8590, set()) and "AudioBank.slot9" in api.get(0x7A7A20, set()))
seqstate = {}
for slot, f in ((2, 0x7BED30), (3, 0x7BEF30), (4, 0x7BE0B0)):
    states = set()
    for t in targets(f):
        for y in body(t, 0x80):
            m = re.match(r"dword ptr \[r[a-z0-9]+ \+ 0x9c\], (\d+)$", y.op_str)
            if y.mnemonic == "mov" and m: states.add(int(m.group(1)))
    seqstate[slot] = states
check("Sound slots 2/3/4 set sequence states within {3,4} / {5} / {2} (slot 2 read to its first ret)",
      seqstate[2] and seqstate[2] <= {3, 4} and seqstate[3] == {5} and seqstate[4] == {2}, str(seqstate))
check("Sound's vtable (01CB5A30) slots 2/3/4 are 007BED30/007BEF30/007BE0B0",
      (q(0x1CB5A30 + 16), q(0x1CB5A30 + 24), q(0x1CB5A30 + 32)) == (0x7BED30, 0x7BEF30, 0x7BE0B0))
# --- the start commands (added 2026-09-26, FABLE, Claude Opus 5.5) ---
def txts(a, n=0x200): return ["%s %s" % (x.mnemonic, x.op_str) for x in body(a, n)]
def whole(a):
    """every instruction of a up to the next function start, early rets included (007C8370 returns early first)."""
    i = bisect.bisect_right(STARTS, a)
    return ["%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(STARTS[i])], a)]
# N1 sensitivity: the defect this revision fixes. Read unbounded (to the first ret), Seb's slot 2 (a teardown ending in
# `jmp 00222000`) runs into the next functions and "reaches" the play wrapper; bounded by functions.tsv it does not.
def reach2(f, bounded):
    seen, frontier, hit = {f}, [f], set()
    for depth in range(2):
        nxt = []
        for g in frontier:
            ins = body(g) if bounded else list(cs.disasm(d[off(g):off(g) + 0x400], g))
            if not bounded:
                cut = next((i for i, x in enumerate(ins) if x.mnemonic in ("ret", "int3")), len(ins))
                ins = ins[:cut + 1]
            for x in ins:
                if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
                    t = int(x.op_str, 16)
                    if 0x7A4380 <= t < 0x7AB460: hit.add(t)
                    elif 0x210000 <= t < 0x227000 and t not in seen: seen.add(t); nxt.append(t)
        frontier = nxt
    return hit
seb2 = q(0x907D80 + 16)
check("N1 sensitivity: unbounded, Seb slot 2 (%08X) 'reaches' 007A78B0; bounded, it does not" % seb2,
      0x7A78B0 in reach2(seb2, False) and 0x7A78B0 not in reach2(seb2, True))
check("N1 no bank vtable slot reaches 007A78B0 within depth 2 (bounded)", 0x7A78B0 not in api)
# N2 the play wrapper dispatches on the handle's type byte
T = txts(0x7A78B0, 0x170)
order = [s for s in T if s in ("cmp al, 2", "cmp al, 8", "cmp al, 7")]
check("N2 007A78B0 posts 0xA for type 2, 0x1C for type 8, command 5 (other queue) for type 7",
      order == ["cmp al, 2", "cmp al, 8", "cmp al, 7"] and cmd_types(0x7A78B0) == [("0x7ab460", 0xA), ("0x7ab460", 0x1C), ("0x7bad60", 5)],
      str(cmd_types(0x7A78B0)))
# N3 the drain arms: resolver, then the start method
def arm_calls(t):
    a = BASE + struct.unpack_from("<I", d, off(0x7AC080) + 4 * t)[0]
    out = []
    for x in body(a, 0x60):
        if x.mnemonic == "jmp": break
        if x.mnemonic == "call" and x.op_str.startswith("0x"): out.append(int(x.op_str, 16))
    return out
check("N3 arm 0xA: 007B44C0 then 007BDFA0; arm 0x1C: 007B77E0 then 007C8370",
      arm_calls(0xA) == [0x7B44C0, 0x7BDFA0] and arm_calls(0x1C) == [0x7B77E0, 0x7C8370], str((arm_calls(0xA), arm_calls(0x1C))))
check("N3 the resolvers take type byte 2 (007B44C0) and 8 (007B77E0)",
      "cmp byte ptr [rcx], 2" in txts(0x7B44C0, 0x40) and "cmp byte ptr [rcx], 8" in txts(0x7B77E0, 0x40))
# N4 both start methods: accept state 1, ramp a gain block to 1.0, set state 2
S, M = whole(0x7BDFA0), whole(0x7C8370)
check("N4 007BDFA0: +0x54 == 1 -> ramp (007CA560) -> +0x54 = 2",
      "cmp dword ptr [rcx + 0x54], 1" in S and "call 0x7ca560" in S and "mov dword ptr [rbx + 0x54], 2" in S)
check("N4 007C8370: +0xC8 == 1 -> ramp +0x190 (007CA560) -> +0xC8 = 2",
      "cmp dword ptr [rcx + 0xc8], 1" in M and "add rcx, 0x190" in M and "call 0x7ca560" in M and "mov dword ptr [rbx + 0xc8], 2" in M)
# N5 class ownership: each class's slot 21 (status) reads that state field and compares it with 7
s21, m21 = q(0x1CB5A30 + 21 * 8), q(0x1CB5E38 + 21 * 8)
check("N5 Sound (01CB5A30) slot 21 reads +0x54; Music (01CB5E38) slot 21 reads +0xC8; both compare with 7",
      txts(s21, 0x30)[:2] == ["mov eax, dword ptr [rcx + 0x54]", "cmp eax, 7"]
      and txts(m21, 0x30)[:2] == ["mov eax, dword ptr [rcx + 0xc8]", "cmp eax, 7"], "%08X %08X" % (s21, m21))
# N6 who calls the play wrapper: raw E8/E9 index over .text, each hit confirmed as an instruction by a linear decode of
# its function
tva, trs, tro = [(va, rs, ro) for vs, va, rs, ro in secs if va <= 0x1000 < va + rs][0]
callers = set()
p = tro
while True:
    p = d.find(b"\xe8", p, tro + trs)
    if p < 0: break
    for op in (0xE8,):
        va_ = BASE + tva + p - tro
        rel = struct.unpack_from("<i", d, p + 1)[0]
        if va_ + 5 + rel == 0x7A78B0:
            f = STARTS[bisect.bisect_right(STARTS, va_) - 1]
            if any(x.address == va_ and x.mnemonic == "call" for x in cs.disasm(d[off(f):off(va_) + 5], f)): callers.add(f)
    p += 1
bank_callers = sorted(c for c in callers if 0x210000 <= c < 0x227000)
slots = {q(vt + 8 * s) for vt in VT.values() for s in range(11)}
check("N6 the bank-range callers of 007A78B0 are 00223190, 00224570, 00224E40, 00224F10, 002252C0, none a vtable slot",
      bank_callers == [0x223190, 0x224570, 0x224E40, 0x224F10, 0x2252C0] and not (set(bank_callers) & slots),
      "all callers %s" % ["%08X" % c for c in sorted(callers)])
# N7 the branch direction of the arm step (regression for the G-16 table correction): after vcall +0x128, a non-zero
# answer jumps to the stepper 007BD120; state 2 is stored only on the zero fall-through.
I = [x for x in cs.disasm(d[off(0x7BDFA0):off(STARTS[bisect.bisect_right(STARTS, 0x7BDFA0)])], 0x7BDFA0)]
k = next(i for i, x in enumerate(I) if x.mnemonic == "call" and x.op_str == "qword ptr [rax + 0x128]")
tgt = int(I[k + 2].op_str, 16) if I[k + 2].mnemonic == "jne" else None
land = [x for x in I if tgt is not None and x.address >= tgt][:2]
check("N7 007BDFA0: vcall +0x128, test al / jne -> stepper 007BD120; the fall-through stores state 2",
      I[k + 1].mnemonic == "test" and I[k + 1].op_str == "al, al" and tgt is not None
      and ("%s %s" % (I[k + 3].mnemonic, I[k + 3].op_str)) == "mov dword ptr [rbx + 0x54], 2"
      and any(x.mnemonic == "call" and x.op_str == "0x7bd120" for x in land), "jne target %s" % (hex(tgt) if tgt else None))
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
