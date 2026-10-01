"""Falsification pass 1 on CONTRACT-party-focus-and-control-suppression (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  F0  section 2: commit 00358BC0 156 B; getter 003272A0 55 B and stores nothing to memory; 0025A6A0 395 B; 0023B040 447 B;
      003594C0 is absent from the function list
  F1  PF-1, two instruments: the function-bounded census and a linear .text sweep (every 4-byte window whose rip target is a
      focus global, confirmed by decoding the instruction that ends there). 022C7FE0: 18 accesses, writers exactly 00358C2F,
      00358B6B, 003590FD; 022C7FF8: 5 bounded, 7 linear, the extra two 003594C0 / 003594D4; linear-only = 0 for 022C7FE0,
      022C7FE4, 022C7FE8
  F2  PF-2: the 18 sites lie in 00358A24..00359481; 003272A0 has 28 direct call sites in 25 functions, none inside that span;
      no lea into 022C7FE0; the address stored as a 4- or 8-byte value occurs nowhere in the image
  F3  PF-3: thunk 00358BB0 is 5 B with 7 callers; the requester 003594B0 has 3; the only function calling both is 0050C610, at
      0050C646 (request) then 0050C64B (commit); the requester's three callers are two calls and the tail-jump 003265F6
  F4  PF-4 / PF-5 / section 10: 00358BE4 `je 0x358c2f`; then 00358C24 re-reads pending, 00358C2F stores current, 00358C35 clears
      the kind, 00358C3C resolves, 00358C52 `jmp 0x2681d0`; 00358BC4/00358BCB return on nothing pending; 00358C46/00358C49
      return without the push when the new handle does not resolve
  F5  PF-6: 0025A680 (11 B, r8d = 1) and 0025A690 (8 B, r8d = 0) both jmp 0x25a6a0; r8's saved flag is tested once in 0025A6A0,
      at 0025A800, gating one call to 003D9B80; the alternate path is taken on handle 0 or kind 2 (00358C01 / 00358C05);
      003594C0 uses cmovne on the pending state; 0034ED30 is 10 B `mov ecx, 2; jmp 0x3594c0`, has no direct caller and is
      stored exactly once, at 01EF17C0
  F6  PF-7: 0x80000003 at 0023B0B6 and 0023B1A8; 0x8800403B at 0023B166 and 0x8800003B at 0023B173; their XOR is 0x4000
  F7  PF-8: +0x698 loaded at 0023B0A2, 0023B152, 0023B196; tested at 0023B0AB and 0023B19D; 0023B15E dereferences the middle
      load with no test between; +0x6B7 at 0023B124, +0x6B4 at 0023B146, +0x714 against 0x21E at 0023B13D (eax set at 0023B138)
  F8  section 14: the secondary handle 022C7FE8 has 8 accesses and 3 writers
"""
import collections, io, os, struct
from array import array
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
body = lambda fa, n=None: list(md.disasm(blob[OFF(fa):OFF(fa) + (n or sizes[fa])], fa))
is_w = lambda x: bool(x.operands) and x.operands[0].type == X86_OP_MEM and x.mnemonic not in ("cmp", "test", "lea", "push") \
    and not x.mnemonic.startswith(("j", "call", "ucomis", "comis", "bt"))
text = next(x for x in SECS if x[0] == ".text")
FOCUS = (0x022C7FE0, 0x022C7FE4, 0x022C7FE8, 0x022C7FF8)
GETTER, THUNK, REQ, KTHUNK = 0x003272A0, 0x00358BB0, 0x003594B0, 0x0034ED30

# ---- function-bounded census
bounded = collections.defaultdict(dict)       # global -> {addr: insn}
calls = collections.defaultdict(list)         # target -> [(site, function)]
branches_to = collections.defaultdict(list)
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        ins = body(fa)
    except ValueError:
        continue
    for x in ins:
        for t in rip(x):
            if t in FOCUS:
                bounded[t][x.address] = x
        if x.operands and x.operands[0].type == X86_OP_IMM and (x.mnemonic == "call" or x.mnemonic.startswith("j")):
            tg = x.operands[0].imm
            if tg in (GETTER, THUNK, REQ, KTHUNK, 0x003594C0):
                (calls if x.mnemonic == "call" else branches_to)[tg].append((x.address, fa))

# ---- linear instrument: every 4-byte window of .text whose rip target is a focus global, confirmed by the decoded instruction
raw = blob[text[3]:text[3] + text[4]]
want = {g - t: g for g in FOCUS for t in (0, 1, 2, 4)}
cands = set()
for s in range(4):
    a = array("i"); n = (len(raw) - s) // 4; a.frombytes(raw[s:s + 4 * n])
    base = text[1] + s + 4
    for k, d in enumerate(a):
        if base + 4 * k + d in want:
            cands.add(text[1] + s + 4 * k)
linear = collections.defaultdict(dict)
for pos in cands:
    for L in range(1, 12):
        st = pos - L
        x = next(md.disasm(blob[OFF(st):OFF(st) + 16], st), None)
        if x and st < pos < x.address + x.size and any(t in FOCUS for t in rip(x)):
            for t in rip(x):
                if t in FOCUS:
                    linear[t][x.address] = x
            break

L0, K = linear[0x022C7FE0], 0x022C7FF8
w0 = sorted(a for a, x in L0.items() if is_w(x))
check("F1", len(L0) == 18 and w0 == [0x00358B6B, 0x00358C2F, 0x003590FD] and len(bounded[K]) == 5 and len(linear[K]) == 7
      and sorted(set(linear[K]) - set(bounded[K])) == [0x003594C0, 0x003594D4]
      and all(not (set(linear[g]) - set(bounded[g])) for g in (0x022C7FE0, 0x022C7FE4, 0x022C7FE8)),
      "022C7FE0: %d linear / %d bounded, writers %s; 022C7FF8: %d bounded, %d linear, linear-only %s; linear-only on the other three %s"
      % (len(L0), len(bounded[0x022C7FE0]), ["%08X" % a for a in w0], len(bounded[K]), len(linear[K]),
         ["%08X" % a for a in sorted(set(linear[K]) - set(bounded[K]))], [len(set(linear[g]) - set(bounded[g])) for g in FOCUS[:3]]))

gs = calls[GETTER]; gfun = {f for _s, f in gs}
lo, hi = min(L0), max(L0)
lea0 = [a for a, x in L0.items() if x.mnemonic == "lea"]
stored = blob.count(struct.pack("<I", 0x022C7FE0)) + blob.count(struct.pack("<Q", 0x022C7FE0))
check("F2", lo >= 0x00358A24 and hi <= 0x00359481 and len(gs) == 28 and len(gfun) == 25 and not any(lo <= f <= hi or f <= lo < f + sizes[f] for f in gfun)
      and not lea0 and stored == 0,
      "18 sites in %08X..%08X; getter %d call sites in %d functions, none in the span; lea into 022C7FE0 %d; stored address occurrences %d"
      % (lo, hi, len(gs), len(gfun), len(lea0), stored))

reqs = calls[REQ] + branches_to[REQ]                     # a tail-jump is a caller too (00326500 ends in jmp 003594B0)
both = sorted({f for _s, f in calls[THUNK]} & {f for _s, f in reqs})
th = body(THUNK, 5)
check("F3", sizes.get(THUNK) == 5 and th[0].mnemonic == "jmp" and th[0].operands[0].imm == 0x00358BC0 and len(calls[THUNK]) == 7 and not branches_to[THUNK] and len(reqs) == 3 and (0x003265F6, 0x00326500) in branches_to[REQ]
      and both == [0x0050C610] and (0x0050C646, 0x0050C610) in calls[REQ] and (0x0050C64B, 0x0050C610) in calls[THUNK],
      "thunk %s, %d callers; requester %d callers (%s); functions calling both %s" % (S(th[0]), len(calls[THUNK]), len(reqs),
      ", ".join("%08X" % a for a, _f in sorted(reqs)), ["%08X" % f for f in both]))

C = body(0x00358BC0); CI = {x.address: x for x in C}
at = lambda I, a: S(I[a]) if a in I else "?"
check("F4", sizes[0x00358BC0] == 156 and at(CI, 0x00358BE4) == "je 0x358c2f" and rip(CI[0x00358C24]) == [0x022C7FE4] and not is_w(CI[0x00358C24])
      and rip(CI[0x00358C2F]) == [0x022C7FE0] and is_w(CI[0x00358C2F]) and rip(CI[0x00358C35]) == [0x022C7FF8] and is_w(CI[0x00358C35])
      and CI[0x00358C3C].mnemonic == "call" and at(CI, 0x00358C52) == "jmp 0x2681d0"
      and CI[0x00358BCB].mnemonic.startswith("j") and CI[0x00358C49].mnemonic.startswith("j"),
      "%s | %s | %s | %s | %s | %s; nothing pending %s / %s; unresolved %s / %s"
      % tuple(at(CI, a) for a in (0x00358BE4, 0x00358C24, 0x00358C2F, 0x00358C35, 0x00358C3C, 0x00358C52, 0x00358BC4, 0x00358BCB, 0x00358C46, 0x00358C49)))

t1, t2 = body(0x0025A680, 11), body(0x0025A690, 8)
T = body(0x0025A6A0); TI = {x.address: x for x in T}
# which register/slot carries r8d: find the first move out of r8
save = next((x for x in T if x.mnemonic == "mov" and len(x.operands) == 2 and x.op_str.split(", ")[1] in ("r8d", "r8b", "r8")), None)
dst = save.op_str.split(", ")[0] if save else None
tests = [x.address for x in T if dst and dst in x.op_str and x.address != save.address]
k = body(KTHUNK, 10); stores = blob.count(struct.pack("<Q", KTHUNK)); spos = blob.find(struct.pack("<Q", KTHUNK))
kva = None
for _n, start, size, rw, rs in SECS:
    if rw <= spos < rw + rs:
        kva = start + spos - rw
U = body(0x003594C0, 27)
check("F5", [S(x) for x in t1][-1] == "jmp 0x25a6a0" and [S(x) for x in t2][-1] == "jmp 0x25a6a0" and "mov r8d, 1" in [S(x) for x in t1]
      and any(S(x) in ("xor r8d, r8d", "mov r8d, 0") for x in t2) and sizes.get(0x0025A6A0) == 395 and tests == [0x0025A800]
      and TI[next(a for a in sorted(TI) if a > 0x0025A800 and TI[a].mnemonic == "call")].operands[0].imm == 0x003D9B80
      and CI[0x00358C01].mnemonic.startswith(("j", "cmov", "test", "cmp")) and CI[0x00358C05].mnemonic.startswith(("j", "cmov", "test", "cmp"))
      and any(x.mnemonic == "cmovne" for x in U) and [S(x) for x in k] == ["mov ecx, 2", "jmp 0x3594c0"] and not calls[KTHUNK] and not branches_to[KTHUNK]
      and stores == 1 and kva == 0x01EF17C0,
      "thunks %s / %s; flag held in %s, tested at %s; alternate-path tests %s / %s; 003594C0 cmovne %s; 0034ED30 %s, callers %d, stored %d at %s"
      % ([S(x) for x in t1], [S(x) for x in t2], dst, ["%08X" % a for a in tests], at(CI, 0x00358C01), at(CI, 0x00358C05),
         any(x.mnemonic == "cmovne" for x in U), [S(x) for x in k], len(calls[KTHUNK]), stores, "%08X" % kva if kva else None))

R = body(0x0023B040); RI = {x.address: x for x in R}
imm = lambda a: [o.imm & 0xFFFFFFFF for o in RI[a].operands if o.type == X86_OP_IMM] if a in RI else []
check("F6", sizes[0x0023B040] == 447 and imm(0x0023B0B6) == [0x80000003] and imm(0x0023B1A8) == [0x80000003] and imm(0x0023B166) == [0x8800403B]
      and imm(0x0023B173) == [0x8800003B] and 0x8800403B ^ 0x8800003B == 0x4000,
      "%s | %s | %s | %s" % tuple(at(RI, a) for a in (0x0023B0B6, 0x0023B1A8, 0x0023B166, 0x0023B173)))
ld = [a for a, x in RI.items() if x.mnemonic == "mov" and "+ 0x698]" in x.op_str]
between = [S(RI[a]) for a in sorted(RI) if 0x0023B152 < a < 0x0023B15E]
check("F7", sorted(ld) == [0x0023B0A2, 0x0023B152, 0x0023B196] and RI[0x0023B0AB].mnemonic in ("test", "cmp") and RI[0x0023B19D].mnemonic in ("test", "cmp")
      and not any(b.startswith(("test", "cmp", "j")) for b in between) and "+ 0x6b7]" in at(RI, 0x0023B124) and "+ 0x6b4]" in at(RI, 0x0023B146)
      and "+ 0x714], ax" in at(RI, 0x0023B13D) and at(RI, 0x0023B138) == "mov eax, 0x21e",
      "loads %s; tests %s / %s; between the middle load and 0023B15E %s; %s | %s | %s"
      % (["%08X" % a for a in sorted(ld)], at(RI, 0x0023B0AB), at(RI, 0x0023B19D), between, at(RI, 0x0023B124), at(RI, 0x0023B146), at(RI, 0x0023B13D)))
L8 = linear[0x022C7FE8]
check("F8", len(L8) == 8 and sum(1 for x in L8.values() if is_w(x)) == 3,
      "022C7FE8: %d accesses, %d writers" % (len(L8), sum(1 for x in L8.values() if is_w(x))))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
