"""uc1_span_tests.py [--root REPO] [--out DIR] - FABLE family ruling R1 tests 1 and 3 for the UC-1 bodies inside the
library spans (SWE2-EC7, 2026-09-29).  Test 2 (the family's own boundary controls re-run with the UC-1 bodies
included) is run by the families' selectors themselves - see t2_compare.py and README.md.

Families (span as each declaring selector states it, half-open; members file = the family's accepted row):
  PPFX       [006DA880, 007911E0)  ppfx-span.tsv
  SEAD       [007A4380, 007F41A0)  sead-library-span.tsv
  libvorbis  [008800C0, 008958B0)  libvorbis.tsv
  libvpx     [0016DDD0, 0017C890)  libvpx-vp8-decoder.tsv

TEST 1 (per body)  strictly inside the span: at least one listed member of the family below it and one above it,
                   both inside the span.
TEST 3 (per body)  every reference TO the body comes from inside the span or from the family's documented callers
                   (the caller set its own selector allows), and every code target the body reaches outside itself is
                   inside the span or is a target the family's listed members already reach (its outbound control).
  References are taken from a raw index, not from graph/edges.tsv:
    code   - every census body (listed + UC-1) and every unlisted code block is decoded linearly; call / jmp / jcc /
             loop targets and rip-relative operands are indexed by target;
    raw    - an image-wide byte scan of .text for E8/E9 rel32, 0F 80-8F rel32 and EB/70-7F rel8 whose target is a UC-1
             body start; a hit whose source byte lies inside a decoded instruction is dropped (a misaligned
             pattern, not a transfer); a hit whose source is not otherwise a decoded transfer is kept as
             'raw-only' (conservative);
    dir64  - every base-relocation (.reloc DIR64) cell whose 8-byte value is the body's VA;
    rva32  - every 4-byte-aligned cell in .rdata/_RDATA/.data/.text whose value is the body's RVA; .pdata records are
             read separately (an unwind record is a function signal, not a reference).
  A reference is inside when its source address lies in the span.  A dir64/rva32 cell outside .text is attributed to
  the class whose RTTI vtable holds the body (rtti/methods.tsv): a PPFX::/SQEX::Sd class is inside for its family;
  any other data cell is an unattributed outside reference, and fails the body (conservative).

Controls printed (each can fail): TEST 1 - the first census entry below each span edge is refused by the test;
TEST 3 - every listed member of the family is run through the same reference test and its failures counted (the
test must fail somewhere or it measured nothing), and a UC-1 body OUTSIDE every library span with a known game-code
caller is shown failing.
Writes <out>/uc1-span-tests.tsv (one row per UC-1 body in a span) and prints a summary.
"""
import argparse, bisect, collections, csv, io, os, re, struct, sys

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..")))
ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
ap.add_argument("--write", action="store_true")
A = ap.parse_args()
DB = os.path.join(A.root, "Database", "FFXII TZA")
W = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work"          # gitignored inputs (EXE, census, RTTI)
sys.path.insert(0, os.path.join(A.root, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as CD, uc1_band
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

FAM = [
    ("PPFX", 0x6DA880, 0x7911E0, "23-Third-Party-Libraries/PostEffects-Yebis-PPFX/members/ppfx-span.tsv", ("PPFX::",),
     lambda f: (f >> 16) in (0x6C, 0x16) or 0x8A0000 <= f < 0x8C0000,
     "integration client 006Cxxxx, static initialisers 0016xxxx, teardown/unwind 008A-008B (select_ppfx.py expected_caller)"),
    ("SEAD", 0x7A4380, 0x7F41A0, "18-Audio/members/sead-library-span.tsv", ("SQEX::Sd",),
     lambda f: False, "none documented by select_audio_libraries.py for the span"),
    ("libvorbis", 0x8800C0, 0x8958B0, "23-Third-Party-Libraries/members/libvorbis.tsv", (),
     lambda f: f in (0x679600, 0x679A50, 0x679F40), "the WebM audio wrapper 00679600/00679A50/00679F40 (VCLIENT)"),
    ("libvpx", 0x16DDD0, 0x17C890, "23-Third-Party-Libraries/members/libvpx-vp8-decoder.tsv", (),
     lambda f: 0x670000 <= f < 0x680000, "the movie client 0067xxxx (select_libvpx.py CLIENT)"),
]

d = open(os.path.join(W, "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = {}
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs[nm] = (0x120000 + va, vs, ro, rs)
def off(a):
    for va, vs, ro, rs in secs.values():
        if va <= a < va + rs:
            return ro + (a - va)
def sec_of(a):
    for nm, (va, vs, ro, rs) in secs.items():
        if va <= a < va + max(vs, rs):
            return nm
TX = secs[".text"]

sizes = CD.load_functions()
uc1 = uc1_band.frontier_starts() & set(sizes)
ents = sorted(sizes)
blocks = {}
for line in io.open(os.path.join(DB, "99-Unresolved-Residual", "Unlisted-Code", "unlisted-code-blocks.tsv"), encoding="utf-8"):
    p = line.split()
    if len(p) >= 2 and re.fullmatch(r"[0-9A-Fa-f]{8}", p[0]):
        try: blocks[int(p[0], 16)] = int(p[1])
        except ValueError: pass
bodies = dict(sizes)
for b, n in blocks.items():
    bodies.setdefault(b, n)
bstarts = sorted(bodies)
def owner(a):
    """the census entry whose body holds a (else an unlisted block, else None)"""
    i = bisect.bisect_right(ents, a) - 1
    if i >= 0 and ents[i] <= a < ents[i] + max(sizes[ents[i]], 1):
        return ents[i]
    i = bisect.bisect_right(bstarts, a) - 1
    if i >= 0 and bstarts[i] <= a < bstarts[i] + max(bodies[bstarts[i]], 1):
        return bstarts[i]
    return None

cls = collections.defaultdict(set)
for row in csv.DictReader(open(os.path.join(W, "rtti", "methods.tsv"), encoding="utf-8", errors="replace"), delimiter="\t"):
    try: cls[int(row["address"], 16)].add(row["class"])
    except (ValueError, TypeError): pass

md = Cs(CS_ARCH_X86, CS_MODE_64)
RIP = re.compile(r"rip ([+-]) (0x[0-9a-f]+)")
BR = ("call", "jmp", "loop", "loope", "loopne", "jrcxz", "jecxz")
covered = bytearray(secs[".text"][3])        # 1 where a decoded instruction's bytes lie
def targets(a, n):
    """[(insn address, target, kind)] for code transfers and rip-relative operands of the body [a, a+n)"""
    out = []
    o = off(a)
    if o is None or n <= 0:
        return out
    for x in md.disasm(d[o:o + n], a):
        co = x.address - secs[".text"][0]
        if 0 <= co < len(covered):
            covered[co:co + x.size] = b"\x01" * min(x.size, len(covered) - co)
        if (x.mnemonic in BR or x.mnemonic.startswith("j")) and re.fullmatch(r"0x[0-9a-f]+", x.op_str):
            out.append((x.address, int(x.op_str, 16), "call" if x.mnemonic == "call" else "branch"))
        m = RIP.search(x.op_str)
        if m:
            out.append((x.address, x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1), "rip"))
    return out

# ---- the raw reference index (targets: UC-1 bodies and every listed member of the four families)
fam_members = {}
for name, lo, hi, rel, *_ in FAM:
    fam_members[name] = set(CD.read_members(os.path.join(DB, os.path.dirname(rel), "x.md"), os.path.basename(rel)))
want = set(uc1) | set().union(*fam_members.values())
refs = collections.defaultdict(list)          # target -> [(src address, src owner, kind)]
decoded_src = set()
body_targets = {}
for b in sorted(bodies):
    if not (TX[0] <= b < TX[0] + TX[1]):
        continue
    ts = targets(b, bodies[b])
    if b in want:
        body_targets[b] = ts
    for src, t, k in ts:
        decoded_src.add(src)
        if t in want and not (b <= t < b + bodies[b]):
            refs[t].append((src, b, k))
# raw .text byte scan for rel32 / rel8 transfers to UC-1 starts
tlo, tro, trs = TX[0], TX[2], TX[3]
for o in range(tro, tro + trs - 6):
    op = d[o]
    src = tlo + (o - tro)
    hits = []
    if op in (0xE8, 0xE9):
        hits.append((src, src + 5 + struct.unpack_from("<i", d, o + 1)[0]))
    elif op == 0x0F and 0x80 <= d[o + 1] <= 0x8F:
        hits.append((src, src + 6 + struct.unpack_from("<i", d, o + 2)[0]))
    elif op == 0xEB or 0x70 <= op <= 0x7F:
        hits.append((src, src + 2 + struct.unpack_from("<b", d, o + 1)[0]))
    for s, t in hits:
        if t in uc1 and s not in decoded_src:
            if 0 <= s - tlo < len(covered) and covered[s - tlo]:
                continue                      # bytes inside a decoded instruction - a misaligned pattern,
                                              # not a transfer (0016EFCA: '7C 24' inside mov rdi,[rsp+0x18])
            ob = owner(s)
            if ob is not None and ob <= t < ob + bodies.get(ob, 0):
                continue                      # a byte pattern inside the target body itself
            refs[t].append((s, ob, "raw-only"))
# DIR64 relocations
relocs = set()
rl = struct.unpack_from("<II", d, pe + 24 + 112 + 8 * 5)
ro_ = off(0x120000 + rl[0]); end = ro_ + rl[1]
while ro_ < end:
    page, blk = struct.unpack_from("<II", d, ro_)
    if blk < 8: break
    for k in range((blk - 8) // 2):
        e = struct.unpack_from("<H", d, ro_ + 8 + 2 * k)[0]
        if e >> 12 == 10:
            cell = 0x120000 + page + (e & 0xFFF)
            relocs.add(cell)
            oc = off(cell)
            if oc is not None:
                v = struct.unpack_from("<Q", d, oc)[0]
                if v in want:
                    refs[v].append((cell, owner(cell) if sec_of(cell) == ".text" else None, "dir64:" + sec_of(cell)))
    ro_ += blk
# RVA32 cells (4-aligned) outside .pdata
rvas = {t - 0x120000: t for t in want}
for nm in (".rdata", "_RDATA", ".data", ".text"):
    va, vs, ro2, rs = secs[nm]
    for k in range(0, rs - 4, 4):
        v = struct.unpack_from("<I", d, ro2 + k)[0]
        if v in rvas:
            cell = va + k
            if cell in relocs or (cell - 4) in relocs:
                continue      # a half of a relocated 64-bit pointer: its low dword can equal an RVA by coincidence
                              # (00D38900 holds the pointer 005CF670, which is also the RVA of 006EF670)
            if nm == ".text" and any(covered[k:k + 4]):
                continue      # bytes of a decoded instruction (an immediate or displacement), not a jump-table cell
            refs[rvas[v]].append((cell, owner(cell) if nm == ".text" else None, "rva32:" + nm))
pdata = set()
pva, pvs, pro, prs = secs[".pdata"]
for k in range(0, pvs - 12, 12):
    pdata.add(0x120000 + struct.unpack_from("<I", d, pro + k)[0])

# Data tables a family's own note and selector document as its entry mechanism: a cell inside one is the library's
# documented entry point, not an outside caller.  libvpx: vpx_codec_vp8_dx_algo at 01CDB290 and its control map at
# 01CDB320 (12 entries of 16 bytes) - select_libvpx.py asserts both, and the inventory row names them as the fingerprint.
DOCTAB = {"libvpx": [(0x1CDB290, 0x1CDB290 + 0x48), (0x1CDB320, 0x1CDB320 + 12 * 16)]}
def ref_verdict(t, lo, hi, prefixes, expected, fam=None):
    """(ok, outside-reference list) for references TO t"""
    bad = []
    for src, ob, k in refs.get(t, []):
        if lo <= src < hi:
            continue
        if any(a <= src < b for a, b in DOCTAB.get(fam, ())):
            continue
        if k.startswith(("dir64:", "rva32:")) and not k.endswith(".text"):
            if prefixes and cls.get(t) and all(c.startswith(prefixes) for c in cls[t]):
                continue                      # a vtable slot of the family's own classes
            bad.append("%s@%08X" % (k, src)); continue
        if ob is not None and expected(ob):
            continue
        bad.append("%s@%08X(in %s)" % (k, src, "%08X" % ob if ob is not None else "no body"))
    return (not bad), bad

outbound = {}
for name, lo, hi, rel, prefixes, expected, why in FAM:
    s = set()
    for m in fam_members[name]:
        for src, t, k in body_targets.get(m, []):
            if k != "rip" and not (lo <= t < hi) and not (m <= t < m + sizes.get(m, 0)):
                s.add(t)
    outbound[name] = s

def callee_verdict(b, lo, hi, name):
    bad = []
    for src, t, k in body_targets.get(b, []):
        if b <= t < b + sizes.get(b, 0) or lo <= t < hi:
            continue
        if k == "rip" and sec_of(t) != ".text":
            continue                          # a global, not a callee
        if t in outbound[name]:
            continue
        bad.append("%s->%08X" % (k, t))
    return (not bad), bad

rows = []
summary = collections.OrderedDict()
controls = []
for name, lo, hi, rel, prefixes, expected, why in FAM:
    mem = sorted(m for m in fam_members[name] if lo <= m < hi)
    inside = sorted(b for b in uc1 if lo <= b < hi)
    c = collections.Counter()
    for b in inside:
        i = bisect.bisect_left(mem, b)
        t1 = i > 0 and i < len(mem)
        okr, badr = ref_verdict(b, lo, hi, prefixes, expected, name)
        okc, badc = callee_verdict(b, lo, hi, name)
        nref = len(refs.get(b, []))
        rows.append((name, "%08X" % b, sizes[b], "pass" if t1 else "FAIL",
                     "%08X" % mem[i - 1] if i > 0 else "-", "%08X" % mem[i] if i < len(mem) else "-",
                     nref, "pass" if okr else "FAIL", ";".join(badr[:4]), "pass" if okc else "FAIL", ";".join(badc[:4]),
                     "yes" if b in pdata else "no"))
        c["bodies"] += 1; c["t1 pass"] += t1; c["t3 callers pass"] += okr; c["t3 callees pass"] += okc
        c["t1+t3 pass"] += (t1 and okr and okc); c["unreferenced"] += (nref == 0)
    summary[name] = c
    # controls
    below = [e for e in ents if e < lo and e not in uc1][-1:]
    for e in below:
        i = bisect.bisect_left(mem, e)
        controls.append("%s TEST 1 control: census entry %08X just below the span -> %s" % (name, e, "pass (BROKEN CONTROL)" if (i > 0 and i < len(mem)) else "refused"))
    mfail = sum(1 for m in mem if not ref_verdict(m, lo, hi, prefixes, expected, name)[0])
    cfail = sum(1 for m in mem if not callee_verdict(m, lo, hi, name)[0])
    controls.append("%s TEST 3 control: the family's %d listed members through the same test - callers FAIL %d, callees FAIL %d"
                    % (name, len(mem), mfail, cfail))
# TEST 3 sensitivity: UC-1 bodies outside every span that have a game-code caller
outside = [b for b in sorted(uc1) if not any(lo <= b < hi for _, lo, hi, *_ in FAM)]
fails = [b for b in outside if not ref_verdict(b, 0x6DA880, 0x7911E0, ("PPFX::",), FAM[0][5])[0]]
controls.append("TEST 3 sensitivity: of %d UC-1 bodies outside every span, %d fail the PPFX reference test (e.g. %s)"
                % (len(outside), len(fails), " ".join("%08X" % b for b in fails[:4])))

os.makedirs(A.out, exist_ok=True)
with io.open(os.path.join(A.out, "uc1-span-tests.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("family\tbody\tbytes\ttest1\tmember_below\tmember_above\trefs\ttest3_callers\toutside_refs\ttest3_callees\toutside_callees\tpdata\n")
    for r in rows:
        f.write("\t".join(str(x) for x in r) + "\n")
for name, c in summary.items():
    print("%-10s %s" % (name, dict(c)))
# --write: members of the R1 span rows = the bodies passing TEST 1 and TEST 3, for the families whose TEST 2 holds.
# TEST 2 is run by the families' own selectors (t2_compare.py, t2-*.txt in this record): it holds for PPFX, SEAD and
# libvpx and FAILS for libvorbis (its closure control finds 15 of its 17 UC-1 bodies joined by nothing), so libvorbis
# gets no row and its 17 bodies stay frontier.
T2_HOLDS = {"PPFX": "23-Third-Party-Libraries/PostEffects-Yebis-PPFX/members/ppfx-span-uc1.tsv",
            "SEAD": "18-Audio/members/sead-span-uc1.tsv",
            "libvpx": "23-Third-Party-Libraries/members/libvpx-vp8-decoder-uc1.tsv"}
if A.write:
    for name, rel in T2_HOLDS.items():
        lo, hi = next((f[1], f[2]) for f in FAM if f[0] == name)
        keep = [r for r in rows if r[0] == name and r[3] == "pass" and r[7] == "pass" and r[9] == "pass"]
        with io.open(os.path.join(DB, rel), "w", encoding="utf-8", newline="\n") as f:
            f.write("# %s: UC-1 bodies (admitted to frontier 2026-09-28) inside the span %08X up to %08X that pass FABLE "
                    "ruling R1 tests 1 and 3 - _index/candidates/ec7-uc1-span-rows-0929/uc1_span_tests.py --write\n"
                    % (name, lo, hi))
            f.write("address\tbytes\tmember_below\tmember_above\trefs\n")
            for r in keep:
                f.write("%s\t%s\t%s\t%s\t%s\n" % (r[1], r[2], r[4], r[5], r[6]))
        print("wrote %d -> %s" % (len(keep), rel))
for line in controls:
    print(line)
kinds = collections.Counter(k for b in uc1 for _, _, k in refs.get(b, []))
print("reference kinds into UC-1 bodies:", dict(sorted(kinds.items())))
