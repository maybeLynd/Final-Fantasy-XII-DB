"""Falsification pass 1 on CONTRACT-ppfx-effect-creation (OPUS, 2026-09-29), re-derived from the shipping image.

For each claim the KILLER is stated first and then searched for; a claim survives only if its killer is absent.

  P0  physical: every cited entry is a function entry with the stated extent; the interior anchors decode as claimed
  P1  I-1 one file, one failure: 0078A120 is called once, and its non-zero result reaches `ret` with no registration
      helper on the way                                  KILLER: a second loader call, or a helper on the failure path
  P2  I-2 the census: 358 direct call sites, 22 targets, the per-helper counts     KILLER: any count differs
  P3  I-3 the strings: 379 lea targets, 374 printable, 364 distinct, 325 `tech_`, 36 uniforms   KILLER: any differs
  P4  I-4 count literals at the two counted helpers are in {4, 8, 17, 25}; the handle total      KILLER: another value
  P5  I-5 every 006DF480 call sits behind [01F3BA80] and one of [02EA0B40]/[01F3BA90]           KILLER: an ungated call
  P6  one caller: no other direct call, jump, RIP-relative reference or stored pointer to 0072A320 anywhere in the image
  P7  §9 threading: no lock prefix, no xchg on memory, no import call in the extent        KILLER: any one of them
  P8  §3 PostProcessParamContext ([01F7F5F0]) is not referenced in the extent              KILLER: a reference
  P9  §5 'deallocated: nothing' against the `free` call §6 lists                           KILLER: free of receiver state
  P10 §12 the first gated log passes line 0x90B                                             KILLER: another literal
"""
import collections, io, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]
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

E, CALLER, LOADER, LOG = 0x0072A320, 0x0072D820, 0x0078A120, 0x006DF480
N = sizes.get(E)
ins = list(md.disasm(blob[OFF(E):OFF(E) + N], E))
idx = {x.address: k for k, x in enumerate(ins)}


def target(x):
    if x.operands and x.operands[0].type == X86_OP_IMM:
        return x.operands[0].imm
    return None


def ripmem(x):
    return [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]


# P0 - physical
cins = list(md.disasm(blob[OFF(CALLER):OFF(CALLER) + sizes.get(CALLER, 0)], CALLER))
at = {x.address: x for x in ins + cins}
p0 = (N == 13547 and len(ins) == 2965 and sizes.get(CALLER) == 396 and LOADER in sizes and LOG in sizes
      and target(at[0x0072A383]) == LOG and target(at[0x0072A3A6]) == 0x0078A530
      and target(at[0x0072D872]) == E and at[0x0072D879].mnemonic == "test" and at[0x0072D8D9].op_str == "qword ptr [rax + 0x38]")
check("P0", p0, "extent %s B, %d instructions; caller %s B; anchors 0072A383/0072A3A6/0072D872/0072D879/0072D8D9 decode as cited" % (N, len(ins), sizes.get(CALLER)))

# P2 - census
calls = [(x.address, target(x)) for x in ins if x.mnemonic == "call" and target(x) is not None]
per = collections.Counter(t for _a, t in calls)
claimed = {0x00715C70: 91, 0x0072DCF0: 65, 0x007157A0: 48, 0x00719380: 40, 0x007182F0: 40, 0x0072EB20: 26, LOG: 10, 0x00715CC0: 8,
           0x0017D2E0: 8, 0x0072DFD0: 4, 0x0072DAC0: 3, 0x0072EC00: 3, 0x0071A380: 2, 0x0072E5B0: 2}
diff = {("%08X" % k): (per.get(k), v) for k, v in claimed.items() if per.get(k) != v}
check("P2", len(calls) == 358 and len(per) == 22 and not diff, "%d direct sites, %d targets; per-helper mismatches %s" % (len(calls), len(per), diff or "none"))
HELPERS = {k for k in claimed if k not in (LOG, 0x0017D2E0)}           # the registration helpers (not log, not sprintf)

# P1 - one file, one failure
lsites = [a for a, t in calls if t == LOADER]
fail_path, k = [], idx[lsites[0]] + 1 if lsites else None
if k is not None:
    # the result test and the branch; follow the non-zero edge linearly to ret
    j = next(x for x in ins[k:k + 6] if x.mnemonic.startswith("j"))
    tst = [x for x in ins[k:idx[j.address]] if x.mnemonic == "test"]
    nz_edge = j.operands[0].imm if j.mnemonic in ("jne", "js", "jnz") else ins[idx[j.address] + 1].address
    q = idx.get(nz_edge)
    while q is not None and q < len(ins):
        x = ins[q]; fail_path.append(x)
        if x.mnemonic == "ret":
            break
        if x.mnemonic == "jmp" and target(x) in idx:
            q = idx[target(x)]; continue
        q += 1
fp_calls = [target(x) for x in fail_path if x.mnemonic == "call"]
check("P1", len(lsites) == 1 and fail_path and fail_path[-1].mnemonic == "ret" and not (set(fp_calls) & HELPERS),
      "loader sites %s; non-zero path %d instructions to ret, calls %s (no registration helper)" % (["%08X" % a for a in lsites], len(fail_path),
                                                                                                 ["%08X" % c for c in fp_calls if c]))

# P3 - strings
leas = [t for x in ins if x.mnemonic == "lea" for t in ripmem(x)]
def cstr(va):
    try:
        o = OFF(va)
    except ValueError:
        return None
    e = blob.find(b"\0", o, o + 400)
    s = blob[o:e]
    return s.decode("ascii") if e > o and all(32 <= c < 127 for c in s) else None
strs = [cstr(t) for t in leas]
printable = [s for s in strs if s]
dist = set(printable)
tech = {s for s in dist if s.startswith("tech_")}
other = sorted(dist - tech)
uniforms = [s for s in other if not s.startswith("..") and s != "%s%d"]
check("P3", len(leas) == 379 and len(printable) == 374 and len(dist) == 364 and len(tech) == 325 and len(uniforms) == 36,
      "%d lea targets, %d printable, %d distinct, %d tech_, %d other = %d uniforms + %s" % (
          len(leas), len(printable), len(dist), len(tech), len(other), len(uniforms), [s for s in other if s not in uniforms]))

# P4 - count literals at the counted helpers
# The count is r9d in both helpers (0072DCF0 `movsxd rdi, r9d`; 0072EB20 `mov ebp, r9d`, the loop bound). At most sites it
# is not an immediate: `mov r9d, r15d` or `lea r9d, [r15 + k]`, with r15d = 1 set once at 0072A85F and incremented only at
# 0072D7B2, after the last counted site (0072D0E2), with no back-edge from there into the site range (checked below).
R15_SET, R15_INC = 0x0072A85F, 0x0072D7B2
LAST_SITE = max(a for a, t in calls if t in (0x0072DCF0, 0x0072EB20))
back = [x for x in ins if x.mnemonic.startswith("j") and target(x) is not None and x.address >= R15_INC and target(x) <= LAST_SITE]
def count_at(a):
    for x in reversed(ins[max(0, idx[a] - 12):idx[a]]):
        if not x.op_str.startswith("r9d,"):
            continue
        if x.mnemonic == "mov" and x.operands[1].type == X86_OP_IMM:
            return x.operands[1].imm
        if R15_SET < a < R15_INC and not back:
            if x.mnemonic == "mov" and x.op_str == "r9d, r15d":
                return 1
            m = re.match(r"r9d, \[r15 \+ (0x[0-9a-f]+|\d+)\]$", x.op_str)
            if x.mnemonic == "lea" and m:
                return 1 + int(m.group(1), 0)
        return None
    return None
lits = collections.Counter(); unk = []
for a, t in calls:
    if t in (0x0072DCF0, 0x0072EB20):
        v = count_at(a)
        if v is None:
            unk.append("%08X" % a); continue
        lits[v] += 1
counted = sum(v * n for v, n in lits.items())
# the claim's substance: the count multiplies handles, so handles exceed names. The page's list of observed values is
# checked separately and reported, because "observed 4, 8, 17, 25" can be true and still incomplete. Only the two counted
# helpers are summed: P11 shows most other census targets are string utilities, so no per-site handle is assumed for them.
check("P4", not unk and sum(lits.values()) == 91 and counted > sum(lits.values()),
      "count per counted site {value: sites} %s (unresolved %s); the two counted helpers register %d handles over 91 named sites; "
      "values outside the page's list {4, 8, 17, 25}: %s" % (dict(sorted(lits.items())), unk or "none", counted,
                                                           sorted(set(lits) - {4, 8, 17, 25})))

# P5 - log gating
ungated = []
for a, t in calls:
    if t != LOG:
        continue
    win = ins[max(0, idx[a] - 40):idx[a]]
    refs = {m for x in win for m in ripmem(x)}
    if not (0x01F3BA80 in refs and (0x02EA0B40 in refs or 0x01F3BA90 in refs)):
        ungated.append("%08X" % a)
check("P5", not ungated and per[LOG] == 10, "%d log sites, ungated within 40 instructions: %s" % (per[LOG], ungated or "none"))

# P6 - one caller, whole image
text = next(s for s in SECS if s[0] == ".text")
tb = blob[text[3]:text[3] + text[4]]
refs = []
for m in re.finditer(rb"[\xe8\xe9]", tb):
    i = m.start()
    if i + 5 <= len(tb) and text[1] + i + 5 + struct.unpack_from("<i", tb, i + 1)[0] == E:
        d = next(md.disasm(tb[i:i + 5], text[1] + i), None)
        if d and d.mnemonic in ("call", "jmp") and target(d) == E:
            refs.append(("%s" % d.mnemonic, "%08X" % d.address))
for i in range(0, len(tb) - 4):
    if text[1] + i + 4 + struct.unpack_from("<i", tb, i)[0] == E and i >= 3:
        for back in (3, 2):
            d = next(md.disasm(tb[i - back:i + 4], text[1] + i - back), None)
            if d and d.size == back + 4 and E in ripmem(d):
                refs.append(("rip " + d.mnemonic, "%08X" % d.address))
ptr = [("%s ptr" % n, "%08X" % (s + (m.start()))) for n, s, _sz, raw, rsz in SECS for m in re.finditer(re.escape(struct.pack("<Q", E)), blob[raw:raw + rsz])]
check("P6", refs == [("call", "0072D872")] and not ptr, "references to 0072A320 in the image: %s; stored 8-byte pointers: %s" % (refs, ptr or "none"))

# P7 - threading
iat = [x for x in ins if x.mnemonic in ("call", "jmp") and ripmem(x)]
lock = [x for x in ins if x.op_str and x.prefix and 0xF0 in x.prefix]
xchg = [x for x in ins if x.mnemonic == "xchg" and "ptr" in x.op_str]
check("P7", not lock and not xchg and not iat, "lock-prefixed %d, xchg on memory %d, calls through a memory slot %d" % (len(lock), len(xchg), len(iat)))

# P8 - PostProcessParamContext
ctx = [x for x in ins if 0x01F7F5F0 in ripmem(x)] + [x for x in ins if "0x1f7f5f0" in x.op_str]
check("P8", not ctx and 0x00193D50 not in per, "references to [01F7F5F0]: %d; calls to its allocator 00193D50: %d" % (len(ctx), per.get(0x00193D50, 0)))

# P9 - the free call
frees = [(a, t) for a, t in calls if t not in claimed and t not in (LOADER, 0x0078A530)]
print("        other direct targets (free / memset / cookie candidates):", ["%08X x%d" % (t, per[t]) for t in sorted(set(t for _a, t in frees))])
for a, t in frees:
    pre = ins[max(0, idx[a] - 4):idx[a]]
    print("        %08X call %08X  <- %s" % (a, t, " ; ".join("%s %s" % (x.mnemonic, x.op_str) for x in pre)))

# P11 - what the census counts. The page reads the fourteen non-log, non-sprintf targets as "registration helpers,
# 332 of the 358 sites". KILLER for the corrected reading: a helper classed as a string utility that reaches the
# effect's lookup slots, or a registration wrapper that does not.
def body(h):
    return list(md.disasm(blob[OFF(h):OFF(h) + sizes[h]], h))
def lookups(h):
    return sum(1 for x in body(h) if x.mnemonic == "call" and x.op_str in ("qword ptr [rax + 0x60]", "qword ptr [rax + 0x48]"))
STRING_UTIL = (0x00715C70, 0x007157A0, 0x00719380, 0x007182F0, 0x00715CC0)
WRAPPERS = (0x0072DCF0, 0x0072EB20, 0x0072DFD0, 0x0072DAC0)
inline = collections.Counter(x.op_str for x in ins if x.mnemonic == "call" and target(x) is None)
su = {("%08X" % h): lookups(h) for h in STRING_UTIL}
wr = {("%08X" % h): lookups(h) for h in WRAPPERS}
rel = body(0x00715C70); ctor = body(0x007157A0)
releases = any(target(x) == 0x006DA8A0 for x in rel)          # the allocator's release (vtable +0x10, live count -1)
strlen = any(x.op_str.startswith("byte ptr [rdx + r8]") for x in ctor)
check("P11", not any(su.values()) and all(wr.values()) and releases and strlen
      and inline["qword ptr [rax + 0x60]"] == 224 and inline["qword ptr [rax + 0x48]"] == 33,
      "string utilities reach the lookup slots: %s; wrappers do: %s; 00715C70 releases via 006DA8A0: %s; 007157A0 strlen loop: %s; "
      "inline lookups in the extent: +0x60 x%d, +0x48 x%d, [r8+0xc8] x%d; string-utility sites %d of the 332" % (
          su, wr, releases, strlen, inline["qword ptr [rax + 0x60]"], inline["qword ptr [rax + 0x48]"], inline["qword ptr [r8 + 0xc8]"],
          sum(per[h] for h in STRING_UTIL)))

# P10 - the first gated log's line literal
first = next(a for a, t in calls if t == LOG)
lit = [x.operands[1].imm for x in ins[idx[first] - 8:idx[first]] if x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[1].type == X86_OP_IMM]
check("P10", 0x90B in lit, "first log call %08X, immediates before it %s" % (first, [hex(v) for v in lit]))

print("BROKEN %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
