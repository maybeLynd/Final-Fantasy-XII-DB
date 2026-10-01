"""Falsification pass 1 on CONTRACT-developer-tuning-console (OPUS, 2026-09-29), re-derived from the shipping image.

Each check states its KILLER; a claim survives only if the killer is absent.

  D0  physical: the dispatcher's extent and instruction count; the cited anchors decode as the formula says
  D1  I-1  282 image-relative entries at 001D4C1C, every one inside 001D1660..001D4C19      KILLER: one outside
  D2  I-2  the bound is unsigned (`ja`), after `add r9d, -0xC`; out of range reaches the shared arm   KILLER: a signed branch
  D3  I-3  227 distinct arms; 001D4BFA takes exactly 56 ids and does nothing                 KILLER: a write or call in it
  D4  I-4  the scalar-FP step census (addss/subss/movss/mulss, RIP-relative, resolved by section)   KILLER: a count differs
  D5  I-5  id 294 is out of the dispatcher's range by its own arithmetic                     KILLER: 294 - 12 <= 0x119
  D6  I-6  001CDBF7 indexes [image base + 0x1CD6E68]; 01DF6E68 is in .data and 01CD6E68 is not the table   KILLER: either
  D7  I-7  the code table: +0x08 == index+1 for 1,314 entries; 111 populated of ids 0..293; 15 prefixes in 17 bands;
           dst0104 at ids 230 and 232                                                        KILLER: any differs
  D8  §5   per-callee arm counts (001A9930 45, 00193D50 33, 001DF340 13, 001DDAB0 10, 001C2F40 9) and 79 distinct callees
  D9  §9   no lock prefix, no xchg on memory in the body                                     KILLER: either
  D10 §10.5 110 arms carry both addss and subss                                              KILLER: another count
  D11 §11  003058B0 is 10 bytes: mov ecx, 0x5F5E0FF; jmp                                     KILLER: anything else
"""
import collections, io, os, re, struct
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


def sec(va):
    return next((n for n, s, z, _r, _rz in SECS if s <= va < s + z), None)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


def target(x):
    return x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None


def ripmem(x):
    return [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try: sizes[int(p[0], 16)] = int(p[2])
        except ValueError: pass

D, END, TAB = 0x001D1660, 0x001D4C19, 0x001D4C1C
ins = list(md.disasm(blob[OFF(D):OFF(END) + 1], D))
at = {x.address: x for x in ins}

# D0
anch = {0x001D166F: ("add", "r9d, -0xc"), 0x001D167D: ("cmp", "r9d, 0x119"), 0x001D16AE: ("jmp", "r9")}
bad = {"%08X" % a: (at[a].mnemonic, at[a].op_str) if a in at else None for a, (m, o) in anch.items() if a not in at or (at[a].mnemonic, at[a].op_str) != (m, o)}
lea_base = at.get(0x001D168F)
base_ok = lea_base is not None and lea_base.mnemonic == "lea" and ripmem(lea_base) == [BASE]
check("D0", sizes.get(D) == 13753 and len(ins) == 2861 and not bad and base_ok,
      "extent %s B, %d instructions to 001D4C19; anchors mismatched %s; 001D168F loads image base %s" % (sizes.get(D), len(ins), bad or "none", base_ok))

# D1
ent = [struct.unpack_from("<I", blob, OFF(TAB) + 4 * i)[0] + BASE for i in range(282)]
outside = [("%d" % (i + 12), "%08X" % t) for i, t in enumerate(ent) if not (D <= t <= END)]
nxt = struct.unpack_from("<I", blob, OFF(TAB) + 4 * 282)[0] + BASE
check("D1", not outside, "282 entries, outside the body: %s; the 283rd dword would point to %08X (%s)" % (outside or "none", nxt, "inside" if D <= nxt <= END else "outside - the table ends at 282"))

# D2
ja = at.get(0x001D1684)
ja_t = target(ja) if ja else None
pro = ins[:next(k for k, x in enumerate(ins) if x.address == 0x001D16AE) + 1]      # the dispatch, up to `jmp r9`
signed = [x for x in pro if x.mnemonic in ("jg", "jge", "jl", "jle")]
saved_after = [x.address for x in pro if x.address > 0x001D1684 and x.mnemonic in ("movaps", "mov") and x.op_str.startswith(("xmmword ptr [rsp", "qword ptr [rsp + 0x50]"))]
# sharpened: out of range enters the SHARED EPILOGUE at 001D4C09, after the xmm6/xmm7/rbp restores - those were saved only
# after the check - while the 56 shared ids enter it at 001D4BFA. Both are no-ops; they are not the same entry.
check("D2", ja is not None and ja.mnemonic == "ja" and not signed and ja_t == 0x001D4C09 and len(saved_after) == 3,
      "001D1684 %s %s (unsigned); signed branches before `jmp r9`: %d; out-of-range enters the epilogue at %s, skipping the %d saves made after the check (%s)" % (
          ja.mnemonic if ja else None, ja.op_str if ja else None, len(signed), "%08X" % ja_t if ja_t else None, len(saved_after),
          " ".join("%08X" % a for a in saved_after)))

# D3
cnt = collections.Counter(ent)
shared, n = cnt.most_common(1)[0]
arm = []
for x in md.disasm(blob[OFF(shared):OFF(shared) + 0x40], shared):
    arm.append(x)
    if x.mnemonic in ("ret", "jmp"):
        break
writes = [x for x in arm if x.mnemonic not in ("ret", "jmp", "pop", "add", "lea", "mov") or (x.mnemonic == "mov" and x.op_str.split(",")[0].strip().endswith("]"))]
calls = [x for x in arm if x.mnemonic == "call"]
check("D3", len(cnt) == 227 and shared == 0x001D4BFA and n == 56 and not calls and not [x for x in arm if "ptr [" in x.op_str.split(",")[0]],
      "%d distinct arms; most shared %08X x%d; its body %s; out-of-range target is the shared arm: %s" % (
          len(cnt), shared, n, " ; ".join("%s %s" % (x.mnemonic, x.op_str) for x in arm), ja_t == shared))

# D4
fp = collections.Counter()
for x in ins:
    if x.mnemonic in ("addss", "subss", "movss", "mulss"):
        for t in ripmem(x):
            try:
                v = struct.unpack_from("<f", blob, OFF(t))[0]
            except ValueError:
                continue
            fp[round(v, 6)] += 1
claim = {0.01: 88, -0.01: 28, 0.02: 19, 0.1: 18, 0.001: 13, 0.05: 12, -0.05: 8, -1.0: 3, -0.03: 3, 0.03: 3, 1.0: 11}
dd = {k: (fp.get(k), v) for k, v in claim.items() if fp.get(k) != v}
check("D4", not dd, "mismatches {constant: (image, page)}: %s; full census %s" % (dd or "none", dict(fp.most_common(14))))

# D5
check("D5", (294 - 12) > 0x119 and (293 - 12) <= 0x119 and (11 - 12) & 0xFFFFFFFF > 0x119,
      "294-12 = %d > 281; 293-12 = 281 in range; id 11 wraps to %08X" % (294 - 12, (11 - 12) & 0xFFFFFFFF))

# D6
r = md.disasm(blob[OFF(0x001CDBF7):OFF(0x001CDBF7) + 12], 0x001CDBF7)
x6 = next(r)
disp_ok = "0x1cd6e68" in x6.op_str and "rsi" in x6.op_str
# 001CDBDF..001CDBF7 is a switch case (reached through the renderer's jump table, so it has no direct predecessor); the
# attack is on the reading itself: the RVA reading must give the {ptr, index+1, 0} table and the literal-as-VA must not.
R = 0x001CD0E0
rb = list(md.disasm(blob[OFF(R):OFF(R) + sizes[R]], R))
rsi_base = any(x.address == 0x001CD17F and ripmem(x) == [BASE] for x in rb)
va_hits = sum(1 for i in range(20) if struct.unpack_from("<QII", blob, OFF(0x01CD6E68 + 16 * i))[1] == i + 1)
rva_hits = sum(1 for i in range(20) if struct.unpack_from("<QII", blob, OFF(0x01DF6E68 + 16 * i))[1] == i + 1)
rsi_base = rsi_base and rva_hits == 20 and va_hits == 0
check("D6", disp_ok and sec(0x01DF6E68) == ".data" and rsi_base, "001CDBF7 `%s %s`; rsi = image base at 001CD17F; RVA reading %d/20 entries fit, literal-as-VA %d/20; 01DF6E68 in %s, 01CD6E68 in %s" % (
    x6.mnemonic, x6.op_str, rva_hits, va_hits, sec(0x01DF6E68), sec(0x01CD6E68)))

# D7
T2 = 0x01DF6E68
def entry(i):
    p, s, z = struct.unpack_from("<QII", blob, OFF(T2 + 16 * i))
    return p, s, z
run = 0
while True:
    try:
        p, s, z = entry(run)
    except (ValueError, struct.error):
        break
    if s != run + 1 or z != 0:
        break
    run += 1
def code(p):
    if not p:
        return None
    try:
        o = OFF(p)
    except ValueError:
        return "(unmapped)"
    e = blob.find(b"\0", o, o + 32); return blob[o:e].decode("ascii", "replace")
codes = {i: code(entry(i)[0]) for i in range(294)}
pop = {i: c for i, c in codes.items() if c}
shape = all(re.fullmatch(r"[a-z]{3}\d{4}", c) for c in pop.values())
bands = []
for i in sorted(pop):
    pre = pop[i][:3]
    if bands and bands[-1][0] == pre:            # a band runs until a different prefix; NULL entries do not end it
        bands[-1][2] = i
    else:
        bands.append([pre, i, i])
dup = collections.defaultdict(list)
for i, c in pop.items():
    dup[c].append(i)
dups = {c: v for c, v in dup.items() if len(v) > 1}
check("D7", run == 1314 and len(pop) == 111 and shape and len({b[0] for b in bands}) == 15 and len(bands) == 17 and dups == {"dst0104": [230, 232]},
      "+0x08 == index+1 for %d entries; %d populated of 294, shape ok %s; %d prefixes in %d bands; duplicates %s" % (
          run, len(pop), shape, len({b[0] for b in bands}), len(bands), dups))

# D8/D10 need what an ARM reaches, and arms share tail code: walk each arm's control flow from its entry (direct branches
# followed, `ret` ends it) rather than cutting the body at the next entry.
byaddr = {x.address: x for x in ins}; addrs = [x.address for x in ins]
nx = {a: addrs[i + 1] if i + 1 < len(addrs) else None for i, a in enumerate(addrs)}
succ = {x.address: ([] if x.mnemonic == "ret" else [target(x)] if x.mnemonic == "jmp" else
                    [target(x), nx[x.address]] if x.mnemonic.startswith("j") else [nx[x.address]]) for x in ins}
reach = {}
for s in set(ent):
    seen, st = set(), [s]
    while st:
        a = st.pop()
        if a in seen or a not in byaddr:
            continue
        seen.add(a); st += [t for t in succ[a] if t]
    reach[s] = seen
sites = collections.Counter(target(x) for x in ins if x.mnemonic == "call" and target(x) is not None)
arms_calling = collections.Counter(t for s, seen in reach.items() for t in {target(byaddr[a]) for a in seen if byaddr[a].mnemonic == "call"} if t)
want = {0x001A9930: 45, 0x00193D50: 33, 0x001DF340: 13, 0x001DDAB0: 10, 0x001C2F40: 9}
# CORRECTED reading (pass 1): the page's figures are CALL SITES in the body, not arms
site_ok = all(sites.get(k) == v for k, v in want.items())
check("D8", site_ok and len(sites) == 79,
      "the page's figures are call sites: %s; distinct callees %d; arms that actually reach each: %s" % (
          {("%08X" % k): sites.get(k) for k in want}, len(sites), {("%08X" % k): arms_calling.get(k) for k in want}))

# D9
lock = [x for x in ins if x.prefix and 0xF0 in x.prefix]
xchg = [x for x in ins if x.mnemonic == "xchg" and "ptr" in x.op_str]
check("D9", not lock and not xchg, "lock-prefixed %d, xchg on memory %d" % (len(lock), len(xchg)))

# D10
ms = {s: {byaddr[a].mnemonic for a in seen} for s, seen in reach.items()}
adds = sum(1 for m in ms.values() if "addss" in m); both = sum(1 for m in ms.values() if "addss" in m and "subss" in m)
# CORRECTED reading (pass 1): 110 is the number of arms that reach addss; 59 of them also reach subss
check("D10", adds == 110 and both == 59, "arms reaching addss: %d; reaching both addss and subss: %d; addss only: %d" % (adds, both, adds - both))

# D11
g = list(md.disasm(blob[OFF(0x003058B0):OFF(0x003058B0) + sizes.get(0x003058B0, 0)], 0x003058B0))
check("D11", sizes.get(0x003058B0) == 10 and g and g[0].op_str == "ecx, 0x5f5e0ff" and g[-1].mnemonic == "jmp",
      "003058B0 %s B: %s" % (sizes.get(0x003058B0), " ; ".join("%s %s" % (x.mnemonic, x.op_str) for x in g)))

print("BROKEN %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
