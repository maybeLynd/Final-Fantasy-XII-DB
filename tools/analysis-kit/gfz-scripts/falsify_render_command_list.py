"""Falsification pass 1 on CONTRACT-render-command-list-and-graphics-handshake (OPUS, 2026-09-29), from the shipping image.

Each check states its KILLER first; a claim survives only if the killer is absent.

  R0  §2 the cited extents                                                                 KILLER: one differs
  R1  I-1 the enqueue appends to both lists; only 0018B810 / 0018C8F0 call slot 0 with edx = 1; the clear touches no object
  R2  I-2 image-wide: every caller of a destroyer (0018B810, 0018C8F0) clears the ordered list FIRST   KILLER: a reversed or unpaired site
  R3  I-3 the 5,000 reserve on the ordered list; no reserve on the owner                    KILLER: either differs
  R4  I-4 the key is ANDed with the masks; no direct call at all in the two walks            KILLER: a comparator
  R5  I-5 two slot-2 calls per entry in the reverse walk, one in the forward walk
  R6  I-6 image-wide: the only +0x10 byte test on list entries is 0018C934; the base store and the four clearing ctors
  R7  I-7 the exit branch and its operands; AO's store on the ran-path only; the arming and the restore
  R8  I-8 the two marks and the clear's resets; each setter has exactly one caller
  R9  I-9 both getters pass their null test to 0016D6A0, a 3-byte `ret 0`
  R10 I-10 the settle-spin shape and mask; the inline copy then the call at 0022B2D0
  R11 §3 the two allocation sizes; the discarded allocator name; 001EDF00 never reads rdx
  R12 §5 image-wide RIP-relative census of 01F7F5E0 / 01F7F5E8 / 01DF08FC / 01F7F594
  R13 §6 0018B1B0 has exactly five callers, the cited ones
"""
import bisect, collections, io, os, re, struct
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
        try: sizes[int(p[0], 16)] = int(p[2])
        except ValueError: pass
FN = sorted(sizes)
_c = {}
def body(a):
    if a not in _c:
        _c[a] = list(md.disasm(blob[OFF(a):OFF(a) + sizes[a]], a))
    return _c[a]
def at(a):
    return next(md.disasm(blob[OFF(a):OFF(a) + 16], a))
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
S = lambda x: "%s %s" % (x.mnemonic, x.op_str)

# whole-image sweep (per listed body)
text = next(x for x in SECS if x[0] == ".text")
calls_to = collections.defaultdict(list)
G = {0x01F7F5E0: "5E0", 0x01F7F5E8: "5E8", 0x01DF08FC: "8FC", 0x01F7F594: "594"}
gacc = collections.defaultdict(lambda: {"w": set(), "r": set()})
for fa in FN:
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    for x in md.disasm(code, fa):
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address, x.mnemonic))
        for t in rip(x):
            if t in G:
                w = x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "and", "or", "xor", "inc", "dec", "add", "sub")
                gacc[G[t]]["w" if w else "r"].add("%08X" % fa)

# R0
want0 = {0x0018B480: 85, 0x0018AD00: 105, 0x0018B4E0: 33, 0x0018C9E0: 95, 0x0018CA40: 8, 0x0018C610: 148, 0x0018B100: 173, 0x0018B1B0: 361,
         0x0018B040: 36, 0x0018B810: 159, 0x0018C8F0: 233, 0x0036F2C0: 43, 0x00187950: 3311, 0x001E0590: 79, 0x0017CCD0: 237,
         0x0018B3F0: 138, 0x0018B510: 35, 0x0018B030: 15, 0x001EDF00: 14}
d0 = {("%08X" % k): (sizes.get(k), v) for k, v in want0.items() if sizes.get(k) != v}
check("R0", not d0, "extent mismatches %s" % (d0 or "none"))

# R1
enq = body(0x0018C610)
# the owner arrives as the argument (rdi); the inline push_back is the capacity test and the store at 0018C65C..0018C673
push = [S(x) for x in enq if 0x0018C65C <= x.address <= 0x0018C673]
owner_push = push[:3] == ["mov rdx, qword ptr [rdi + 8]", "cmp rdx, qword ptr [rdi + 0x10]", "jae 0x18c678"] and "mov qword ptr [rdx], rbx" in push
tail = at(0x0018C69F)
def slot0_free(fn):
    b = body(fn); out = []
    for k, x in enumerate(b):
        if x.mnemonic == "call" and x.op_str.startswith("qword ptr [r") and x.op_str.endswith("]") and "+" not in x.op_str:
            pre = [S(y) for y in b[max(0, k - 4):k]]
            out.append(("%08X" % x.address, "mov edx, 1" in pre))
    return out
clr = [S(x) for x in body(0x0018B040)] + [S(x) for x in body(0x0018B3F0)]
# an import call (memmove through its IAT slot [008C2A40], substrate per §6) is not an object call
indirect_in_clear = [S(x) for f in (0x0018B040, 0x0018B3F0) for x in body(f) if x.mnemonic == "call" and x.op_str.startswith("qword ptr") and rip(x) != [0x008C2A40]]
check("R1", owner_push and tail.mnemonic == "jmp" and T(tail) == 0x0018AFF0 and slot0_free(0x0018B810) and all(v for _a, v in slot0_free(0x0018B810))
      and slot0_free(0x0018C8F0) and not indirect_in_clear,
      "owner push in 0018C610: %s; 0018C69F `%s`; slot-0 calls with edx=1 in 0018B810 %s, 0018C8F0 %s; indirect calls in the clear path %s" % (
          owner_push, S(tail), slot0_free(0x0018B810), slot0_free(0x0018C8F0), indirect_in_clear or "none"))

# R2
pairs = {}
for d in (0x0018B810, 0x0018C8F0):
    for f, a, m in calls_to[d]:
        b = body(f); k = next(i for i, x in enumerate(b) if x.address == a)
        before = [x.address for x in b[:k] if x.mnemonic == "call" and T(x) == 0x0018B040]
        after = [x.address for x in b[k:] if x.mnemonic == "call" and T(x) == 0x0018B040]
        pairs["%08X@%08X" % (f, a)] = ("%08X" % before[-1] if before else None, "%08X" % after[0] if after else None)
ok2 = all(v[0] is not None and v[1] is None for v in pairs.values())
check("R2", ok2 and len(pairs) == 3, "destroy/flush sites and the preceding clear: %s (%d sites; the page body still says 'two' in places)" % (pairs, len(pairs)))

# R3
r3a = [S(x) for x in body(0x0018AD00) if 0x0018AD38 <= x.address <= 0x0018AD48]
own = [S(x) for x in body(0x0018C9E0)]
check("R3", "mov edx, 0x1388" in r3a and "call 0x18b320" in r3a and not any("0x18b320" in t for t in own),
      "ordered ctor %s; owner ctor calls the reserve: %s" % (r3a, any("0x18b320" in t for t in own)))

# R4 / R5
fw = body(0x0018B100); rv = body(0x0018B1B0)
direct = [S(x) for x in fw + rv if x.mnemonic == "call" and T(x) is not None and T(x) not in (0x00193D50, 0x0018D630)]   # the render-param getter and the +0x49C reader
s2f = sum(1 for x in fw if x.mnemonic == "call" and x.op_str == "qword ptr [rax + 0x10]")
s2r = sum(1 for x in rv if x.mnemonic == "call" and x.op_str == "qword ptr [rax + 0x10]")
check("R4", S(at(0x0018B167)) == "test dword ptr [rsi + 0x20], eax" and not direct,
      "0018B167 `%s`; direct calls in the two walks: %s" % (S(at(0x0018B167)), direct or "none"))
# sharpened (pass 1): 0018B1B0 has two arms split on r9b (0018B1CB); BOTH call slot 2 twice per entry
arms = sorted("%08X" % x.address for x in rv if x.mnemonic == "call" and x.op_str == "qword ptr [rax + 0x10]")
check("R5", s2f == 1 and arms == ["0018B247", "0018B258", "0018B2D3", "0018B2E4"] and S(at(0x0018B1CB)) == "test r9b, r9b",
      "slot-2 calls: 0018B100 %d; 0018B1B0 %s - two per entry in each arm of the r9b split" % (s2f, arms))

# R6
fam = (0x0018B100, 0x0018B1B0, 0x0018C8F0, 0x0018B810, 0x0018B040, 0x0018B3F0, 0x0018AFF0, 0x0018C610)
tests10 = [("%08X" % x.address, S(x)) for f in fam for x in body(f) if x.mnemonic in ("cmp", "test") and re.search(r"byte ptr \[r\w+ \+ 0x10\]", x.op_str)]
base = S(at(0x00212CD5))
clears = {a: S(at(a)) for a in (0x001F1799, 0x001F196A, 0x001F1CE4, 0x001F1E3E)}
vts = {}
for a in clears:
    f = next(fa for fa in reversed(FN) if fa <= a)
    vts["%08X" % f] = sorted("%08X" % t for x in body(f) for t in rip(x) if 0x00900000 <= t < 0x00910000)
# CORRECTED citation (pass 1): the reader starts at 0018C933; 0018C934 is inside it
starts = {x.address for x in body(0x0018C8F0)}
check("R6", tests10 == [("0018C933", "cmp byte ptr [rdi + 0x10], bpl")] and 0x0018C934 not in starts and S(at(0x0018C937)) == "jne 0x18c94c" and "+ 0x10], 1" in base and all("+ 0x10], 0" in v or "0x10], bl" in v or "0x10], " in v for v in clears.values())
      and all(any(v_ in ("009030B0", "00903390", "009030D0", "009033B0") for v_ in lst) for lst in vts.values()),
      "byte tests of +0x10 in the family %s; base 00212CD5 `%s`; clearing stores %s; vtables in those ctors %s" % (
          tests10, base, {("%08X" % k): v for k, v in clears.items()}, vts))

# R7
ex = [S(x) for x in fw if 0x0018B16C <= x.address <= 0x0018B17C]
ao = body(0x001F28B0)
store = S(at(0x001F29A3))
eo = {a: S(at(a)) for a in (0x001F28C5, 0x001F28D2)}
arm = [S(x) for x in body(0x00187950) if 0x00188103 <= x.address <= 0x00188144]
exit_ok = any(t.startswith("jne 0x18b192") or t.startswith("je 0x18b192") for t in ex)
eo_ok = all(T(at(a)) and T(at(a)) > 0x001F29A3 for a in eo)
check("R7", exit_ok and rip(at(0x001F29A3)) == [0x01F7F594] and "1" in store and eo_ok and len(arm) >= 4,
      "exit test %s; AO store `%s`; early-outs %s (both past 001F29A3: %s); arming/restore %s" % (ex, store, eo, eo_ok, arm[:8]))

# R8
m24 = [S(x) for x in body(0x0018B510)]; m2c = [S(x) for x in body(0x0018B030)]; c = [S(x) for x in body(0x0018B040)]
one = {("%08X" % t): sorted(set("%08X" % f for f, a, m in calls_to[t])) for t in (0x0018B510, 0x0018B030)}
check("R8", any("+ 0x24]" in t for t in m24) and any("+ 0x2c]" in t for t in m2c) and any("+ 0x24]" in t for t in c) and any("+ 0x2c]" in t for t in c)
      and one == {"0018B510": ["0018CB10"], "0018B030": ["001829F0"]}, "setters' callers %s; clear resets %s" % (one, [t for t in c if "0x24" in t or "0x2c" in t]))

# R9
check("R9", blob[OFF(0x0016D6A0):OFF(0x0016D6A0) + 3] == b"\xc2\x00\x00" and T(at(0x0018B4F0)) == 0x0016D6A0 and T(at(0x0018B49D)) == 0x0016D6A0,
      "0016D6A0 bytes %s; 0018B4F0 `%s`; 0018B49D `%s`" % (blob[OFF(0x0016D6A0):OFF(0x0016D6A0) + 3].hex(), S(at(0x0018B4F0)), S(at(0x0018B49D))))

# R10
sp = [S(x) for x in body(0x0036F2C0)]
inl = list(md.disasm(blob[OFF(0x0022B2C0):OFF(0x0022B2C0) + 0x18], 0x0022B2C0))
check("R10", any("0xfffffef3" in t for t in sp) and sum(1 for x in body(0x0036F2C0) if 0x02EBA3F8 in rip(x)) >= 3 and any(T(x) == 0x0036F2C0 for x in inl if x.address == 0x0022B2D0),
      "spin %s; 0022B2C0.. %s" % (sp, [S(x) for x in inl][:6]))

# R11
g11 = {a: S(at(a)) for a in (0x0018B4AB, 0x0018C9F9)}
alloc = body(0x001EDF00)
reads_rdx = [S(x) for x in alloc if re.search(r"\b(rdx|edx|dx|dl)\b", x.op_str)]
nm = []
for a in (0x0018AD2C, 0x0018CA21):
    x = at(a); t = rip(x)
    if t:
        o = OFF(t[0]); nm.append(blob[o:blob.find(b"\0", o)].decode("latin-1"))
check("R11", g11[0x0018B4AB] == "lea ecx, [rbx + 0x30]" and g11[0x0018C9F9] == "mov ecx, 0x20" and nm == ["EASTL vector", "EASTL vector"] and not reads_rdx
      and any(0x00902720 in rip(x) for x in alloc), "sizes %s; names %s; 001EDF00 reads rdx: %s" % (g11, nm, reads_rdx or "never"))

# R12
got = {k: {kk: sorted(v) for kk, v in d.items()} for k, d in gacc.items()}
want12 = {"5E0": {"w": ["0018B480"], "r": ["0018B480", "0018B4E0"]}, "5E8": {"w": ["0018C9E0"], "r": ["0018C9E0", "0018CA40"]},
          "8FC": {"w": ["00187950"], "r": ["00187950", "0018B100"]}, "594": {"w": ["00187950", "001F28B0"], "r": ["0018B100"]}}
check("R12", got == want12, "census %s" % got)

# R13
c13 = sorted(set("%08X" % f for f, a, m in calls_to[0x0018B1B0]))
check("R13", c13 == ["001F06D0", "001F3510", "001F3570", "001F3650", "001F36B0"], "0018B1B0 callers %s" % c13)

print("BROKEN %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
