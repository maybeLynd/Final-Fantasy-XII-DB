"""select_audio_libraries.py - EC-7 member selector for the linked audio libraries (FABLE, 2026-09-13).
Rows: SQEX SEAD, libogg framing.c, Tremor with vorbisfile.c, CRI HCA decoder, libvorbis, libogg bitwise.c.

  sead-library-span.tsv       SQEX SEAD (SQEX::Sd) - every census entry in [007A4380, 007F41A0) except
                              (a) the libogg framing.c object [007B9D70, 007BA970],
                              (b) entries whose RTTI vtable appearances include a class outside SQEX::Sd
                                  (O: SoundObjectManagerCallbackHandler; X: ICF-folded bodies shared with other classes),
                              (c) entries already A-measured or declared by another family;
                              plus nine SEAD entries past the span (SoundObject vtable bodies and installers, PolygonSound's
                              SSE helpers), each asserted by RTTI or by its only callers.
  libogg-framing.tsv          (written beside the inventory page) every census entry in [007B9D70, 007BA970].
  tremor-vorbisfile.tsv       (beside the inventory page) Xiph Tremor with its vorbisfile.c: every census entry in
                              [007F41A0, 007F6FB0) and [007F7680, 007FFBC0); between them sit SEAD objects and an MS ADPCM
                              decoder, not covered.
  cri-hca-decoder.tsv         (beside the inventory page) every census entry in [00121000, 00125740) except the ICF-folded
                              `ret 0` body 001243B0, which FFXII code shares.
For the last two it asserts byte fingerprints and a closure control: every direct caller of a member from outside the
object is a SEAD-span body (or, for Tremor, a libogg body), and every member is joined to the object by a call, a lea,
a registry slot or an _ogg_ hook.

It also prints the two boundary controls the page cites (sec.13):
  outbound   every direct E8/E9 call from a span body to an entry outside the span, grouped by target
  globals    every .data qword referenced rip-relatively from the span AND from outside it (security cookie removed),
             grouped by the outside referencers' address zone

Inputs (gitignored, reproducible): Tools/work/exe/FFXII_TZA.exe, Tools/work/graph/functions.tsv,
Tools/work/rtti/methods.tsv. Needs capstone for the globals control.
Usage: python select_audio_libraries.py [--write]"""
import sys, os, struct, bisect, collections, re
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

SPAN = (0x7A4380, 0x7F41A0)
OGG = (0x7B9D70, 0x7BA971)
COOKIE = 0x1F44830

d = open(os.path.join(W, "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = {}
for i in range(n):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs[nm] = (0x120000 + va, vs, ro, rs)
def off(a):
    for va, vs, ro, rs in secs.values():
        if va <= a < va + rs: return ro + (a - va)

sizes = cd.load_functions()
# UC-1 SERIES BREAK (2026-09-28): the default census now also carries the UC-1 frontier bodies,
# which are frontier BY RULING - never A/B/C, and check_dispositions refuses any members file that
# names one. Leave them out of the selection population, so a re-run reproduces the declared family
# (on 2026-09-29 an unpatched re-run admitted 733 of them into PPFX and failed the libvorbis closure
# assertion). They are also absent from the caller/control attribution below. SWE2-EC7 2026-09-29.
import uc1_band
# FABLE ruling, point 4 (SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930; SWE2-EC7 2026-09-30): the UC-1 bodies stay IN
# the population, so every caller/closure/control test sees calls made by a UC-1 body; they are removed only from
# the written members files (a UC-1 body is frontier by ruling, declared only by an R1 span row).
UC1 = set(uc1_band.frontier_starts())
_out = lambda xs: [e for e in xs if e not in UC1]
ents = sorted(sizes)
a_set = cd.measure_a(DB, sizes)[0]
declared = {}
for doc, parts in cd.parse_families(DB):
    if len(parts) >= 5 and parts[1] in cd.LETTERS and not parts[0].startswith(("SQEX SEAD", "libogg", "Tremor", "CRI HCA", "libvorbis")):
        try:
            for m in cd.read_members(doc, parts[2]): declared[m] = parts[0]
        except Exception:
            pass
cls = collections.defaultdict(set)
for line in open(os.path.join(W, "rtti", "methods.tsv"), encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: cls[int(p[0], 16)].add(p[1])
    except ValueError: pass

# --- libogg fingerprints: the three header[5] flag readers and the OggS capture compare
def body(e): return d[off(e):off(e) + sizes[e]]
for e, bit in ((0x7B9F70, 2), (0x7BA050, 1), (0x7BA060, 4)):
    assert body(e) == bytes([0x48, 0x8B, 0x01, 0x0F, 0xB6, 0x40, 0x05, 0x83, 0xE0, bit, 0xC3]), "%08X" % e
oggs = struct.unpack_from("<I", d, off(0x1CB5780))[0]
assert oggs == struct.unpack("<I", b"OggS")[0]
ogg = [e for e in ents if OGG[0] <= e < OGG[1]]
assert len(ogg) == 22, len(ogg)
assert not (set(ogg) & a_set) and not (set(ogg) & set(declared))

# --- SEAD span
members, excl = [], collections.defaultdict(list)
for e in ents:
    if not (SPAN[0] <= e < SPAN[1]): continue
    c = cls.get(e, set()); other = {x for x in c if not x.startswith("SQEX::Sd")}
    if OGG[0] <= e < OGG[1]: excl["libogg framing.c object (own row)"].append(e)
    elif e in a_set: excl["A-measured"].append(e)
    elif e in declared: excl["declared: " + declared[e][:50]].append(e)
    elif other: excl["RTTI appearance outside SQEX::Sd (" + ("folded" if len(other) < len(c) else "only") + ")"].append(e)
    else: members.append(e)
print("SEAD span %08X-%08X: entries %d, members %d" % (SPAN[0], SPAN[1], len(members) + sum(map(len, excl.values())), len(members)))
for k, v in sorted(excl.items()):
    print("  excluded %-60s %3d  %s" % (k, len(v), " ".join("%08X" % x for x in v)))
print("  members at an SQEX::Sd vtable slot: %d" % sum(1 for e in members if cls.get(e)))

# --- control 1: outbound direct calls
text = secs[".text"]; to = text[2]; tn = text[3]
def owner_of(a):
    i = bisect.bisect_right(ents, a) - 1
    if i >= 0 and ents[i] <= a < ents[i] + max(sizes[ents[i]], 1): return ents[i]
eset = set(ents); out = collections.defaultdict(set); callers = collections.defaultdict(set)
for o in range(to, to + tn - 5):
    if d[o] not in (0xE8, 0xE9): continue
    src = text[0] + (o - to)
    t0 = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t0 in eset:
        f0 = owner_of(src)
        if f0 is not None and f0 != t0: callers[t0].add(f0)
    if not (SPAN[0] <= src < SPAN[1]): continue
    t = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t in eset and not (SPAN[0] <= t < SPAN[1]):
        f = owner_of(src)
        if f is not None: out[t].add(f)
print("control outbound: %d distinct targets outside the span" % len(out))
for t in sorted(out): print("  -> %08X from %d" % (t, len(out[t])))

# --- control 2: shared globals
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
except ImportError:
    Cs = None
if Cs:
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    data = secs[".data"]; refs = collections.defaultdict(set)
    rx = re.compile(r"rip ([+-]) (0x[0-9a-f]+)")
    for e in ents:
        if e < 0x121000 or e >= 0x8C2000 or sizes[e] <= 0: continue
        for x in md.disasm(body(e), e):
            m = rx.search(x.op_str)
            if not m: continue
            g = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
            if data[0] <= g < data[0] + data[1] or 0x1CEB618 <= g < 0x1CEB638: refs[g].add(e)
    shared = collections.Counter(); zones = collections.Counter()
    for g, fs in refs.items():
        if g == COOKIE or 0x1CEB618 <= g < 0x1CEB638: continue
        ins = {f for f in fs if SPAN[0] <= f < SPAN[1]}; outs = fs - ins
        if ins and outs:
            key = ",".join(sorted({"%04X" % (f >> 16) for f in outs}))
            zones[key] += 1
    print("control globals: shared with outside, by outside zone set:", dict(zones))

# --- SEAD entries past the span, between vorbisfile and the Tremor decoder (added 2026-09-13 on OPUS-REQ-FABLE-TREMOR-RESIDUE)
SEAD_SLOTS = (0x7F7390, 0x7F73D0, 0x7F7400, 0x7F7420)          # SQEX::Sd::Lay::SoundObject vtable bodies
SEAD_INSTALLERS = ((0x7F7360, 0x1CBAB68), (0x7F7380, 0x1CB9888))  # install a vtable whose slot 0 is SEAD's
SEAD_HELPERS = (0x7F7440, 0x7F74E0, 0x7F7570)                    # SSE geometry called only by SQEX::Sd methods
for e in SEAD_SLOTS:
    assert cls.get(e) and all(c.startswith("SQEX::Sd") for c in cls[e]), "%08X" % e
for e, vt in SEAD_INSTALLERS:
    b = body(e); disp = struct.unpack_from("<i", b, 3)[0]
    assert b[:3] == b"\x48\x8d\x05" and e + 7 + disp == vt, "%08X" % e
    slot0 = struct.unpack_from("<Q", d, off(vt))[0]
    assert cls.get(slot0) and all(c.startswith("SQEX::Sd") for c in cls[slot0]), "%08X slot0 %08X" % (e, slot0)
for e in SEAD_HELPERS:
    assert callers[e] and all(cls.get(f) and all(c.startswith("SQEX::Sd") for c in cls[f]) for f in callers[e]), "%08X" % e
sead_extra = [e for e in SEAD_SLOTS + tuple(x for x, _ in SEAD_INSTALLERS) + SEAD_HELPERS if e not in a_set and e not in declared]
assert len(sead_extra) == 9
members = sorted(members + sead_extra)
print("SEAD entries past the span added: %d (%s); left out as unestablished upstream: 007F6FB0 (MS ADPCM block decoder), 007F7350 (its samples-per-block helper)" % (
    len(sead_extra), " ".join("%08X" % e for e in sead_extra)))

# --- Tremor + vorbisfile, and the CRI HCA decoder
TREMOR = ((0x7F41A0, 0x7F6FB0), (0x7F7680, 0x7FFBC0))
CRI = (0x121000, 0x125740)
def in_r(e, rs): return any(a <= e < b for a, b in rs)
# fingerprints: ov_pcm_tell / ov_raw_tell return OV_EINVAL (-131) below ready_state OPENED (2)
for e, fld in ((0x7F6280, 0x78), (0x7F6730, 0x10)):
    assert body(e) == bytes.fromhex("83b98000000002 48c7c07dffffff 7c04 488b41%02x c3".replace(" ", "") % fld), "%08X" % e
# the residue registry: three bundles share unpack/look/free_info/free_look and differ in inverse
res = [struct.unpack_from("<5Q", d, off(b)) for b in (0x1F41EC8, 0x1F41EF0, 0x1F41F18)]
assert res[0][:4] == res[1][:4] == res[2][:4] and len({r[4] for r in res}) == 3
assert all(in_r(q, TREMOR) for r in res for q in r)
assert d[off(0x1CEBB50):off(0x1CEBB50) + 6] == b"vorbis"
assert b"CRI Middleware" in d[off(0x1CBA610):off(0x1CBA610) + 60]
# libvorbis (the float decoder the WebM audio wrapper links, unreached) and libogg bitwise.c, shared by both Vorbis copies
VORBIS = (0x8800C0, 0x8958B0)
BITW = (0x17C890, 0x17CC70)
VCLIENT = (0x679600, 0x679A50, 0x679F40)
vres = [struct.unpack_from("<8Q", d, off(b)) for b in (0x1CEB0D0, 0x1CEB110, 0x1CEB150)]
assert vres[0][1:5] == vres[1][1:5] == vres[2][1:5] and len({r[5:] for r in vres}) == 3
assert all(VORBIS[0] <= q < VORBIS[1] for r in vres for q in r if q)
assert [struct.unpack_from("<I", d, off(0x1CEB590) + 4 * k)[0] for k in range(33)] == [(1 << k) - 1 for k in range(33)]
lea_from = collections.defaultdict(set); rip_from = collections.defaultdict(set)
if Cs:
    for e in ents:
        if not (in_r(e, TREMOR) or CRI[0] <= e < CRI[1] or VORBIS[0] <= e < VORBIS[1] or BITW[0] <= e < BITW[1]): continue
        for x in md.disasm(body(e), e):
            m = rx.search(x.op_str)
            if m:
                t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
                rip_from[t].add(e)
                if x.mnemonic == "lea": lea_from[t].add(e)
    assert 0x7F6FB0 not in lea_from and 0x1CBA610 in lea_from and 0x121DB0 in lea_from[0x1CBA610]
    assert 0x8800C0 in rip_from[0x1CEBB50] and 0x7F7FF0 in rip_from[0x1CEBB50]
    assert {0x17C9F0, 0x17CB40} <= rip_from[0x1CEB590]
reg = set(q for b in range(0x1F41E60, 0x1F41F68, 8) for q in [struct.unpack_from("<Q", d, off(b))[0]] if in_r(q, TREMOR))
reg |= set(q for lo, hi in ((0x1CEB070, 0x1CEB190), (0x1CE3080, 0x1CE30B0)) for b in range(lo, hi, 8)
           for q in [struct.unpack_from("<Q", d, off(b))[0]] if VORBIS[0] <= q < VORBIS[1])
hookusers = {e for g in (0x1F41CF8, 0x1F41D00, 0x1F41D08, 0x1F41D10) for e in refs.get(g, ())} if Cs else set()
# libvorbis's own const allocator slots 01CEB618 calloc / 620 realloc / 628 malloc / 630 free: used by nothing but libvorbis and bitwise.c
assert [struct.unpack_from("<Q", d, off(0x1CEB618 + 8 * k))[0] for k in range(4)] == [0x861FBC, 0x861F32, 0x861F2C, 0x861F26]
vslot = {e for g in range(0x1CEB618, 0x1CEB638, 8) for e in refs.get(g, ())} if Cs else set()
if Cs: assert vslot and all(VORBIS[0] <= e < VORBIS[1] or BITW[0] <= e < BITW[1] for e in vslot), sorted("%08X" % e for e in vslot if not VORBIS[0] <= e < VORBIS[1])
hookusers |= vslot
# _float32_unpack: mantissa mask 0x1FFFFF, exponent (v >> 21) & 0x3FF, bias -788 (VQ_FMAN - 1 + VQ_FEXP_BIAS)
fb = body(0x882AC0)
assert fb[8:13] == bytes.fromhex("25ffff1f00") and fb[13:16] == bytes.fromhex("c1fa15") and fb[16:22] == bytes.fromhex("81e2ff030000") and bytes.fromhex("81c2ecfcffff") in fb
reg.add(0x882AC0)
bitw_callers = {f for e in range(BITW[0], BITW[1]) for f in callers.get(e, ())}
def select(rs, skip=()):
    return [e for e in ents if in_r(e, rs) and e not in skip]
def members_of(obj):
    return [e for e in obj if e not in a_set and e not in declared]
for name, obj, allowed in (("Tremor + vorbisfile", select(TREMOR), lambda f: SPAN[0] <= f < SPAN[1] or in_r(f, TREMOR)),
                           ("CRI HCA decoder", select((CRI,), skip=(0x1243B0,)), lambda f: SPAN[0] <= f < SPAN[1] or CRI[0] <= f < CRI[1]),
                           ("libvorbis", select((VORBIS,), skip=(0x887630,)), lambda f: VORBIS[0] <= f < VORBIS[1] or f in VCLIENT),
                           ("libogg bitwise.c", select((BITW,)), lambda f: VORBIS[0] <= f < VORBIS[1] or in_r(f, TREMOR))):
    ms = set(obj)
    foreign = sorted((e, f) for e in obj for f in callers[e] if not allowed(f))
    lonely_all = [e for e in obj if not ((callers[e] & ms) or any(e in callers[t] for t in ms) or (lea_from.get(e, set()) & ms)
                                     or e in reg or e in hookusers or (e in bitw_callers and name == "libvorbis") or any(allowed(f) for f in callers[e]))]
    # a UC-1 body is judged, not asserted: joined by nothing it simply does not qualify (it is never written)
    uc1_lonely = [e for e in lonely_all if e in UC1]
    lonely = [e for e in lonely_all if e not in UC1]
    gone = [e for e in obj if e in a_set or e in declared]
    print("%s: object entries %d, members %d (A-measured or declared elsewhere: %s), callers from outside the object and its client: %d %s, entries joined by nothing: %d %s" % (
        name, len(obj), len(obj) - len(gone), " ".join("%08X" % e for e in gone) or "none", len(foreign),
        " ".join("%08X<-%08X" % p for p in foreign[:6]), len(lonely), " ".join("%08X" % e for e in lonely)))
    if uc1_lonely: print("  %s: UC-1 bodies in the object joined by nothing (not written): %d" % (name, len(uc1_lonely)))
    assert not foreign and not lonely
tremor = members_of(select(TREMOR)); cri = members_of(select((CRI,), skip=(0x1243B0,)))
vorbis = members_of(select((VORBIS,), skip=(0x887630,)))  # 00887630: in the range, referenced by nothing, no fingerprint - left out
bitw = members_of(select((BITW,)))

if "--write" in sys.argv:
    open(os.path.join(HERE, "sead-library-span.tsv"), "w").write(
        "# SQEX SEAD span %08X-%08X less libogg, non-Sd RTTI, A and other families - select_audio_libraries.py\n" % SPAN
        + "\n".join("%08X" % e for e in _out(members)) + "\n")
    inv = os.path.join(DB, "23-Third-Party-Libraries", "members")
    os.makedirs(inv, exist_ok=True)
    open(os.path.join(inv, "libogg-framing.tsv"), "w").write(
        "# libogg framing.c object %08X-%08X - 18-Audio/members/select_audio_libraries.py\n" % (OGG[0], OGG[1] - 1)
        + "\n".join("%08X" % e for e in _out(ogg)) + "\n")
    open(os.path.join(inv, "tremor-vorbisfile.tsv"), "w").write(
        "# Xiph Tremor + vorbisfile.c, 007F41A0-007F6FAF and 007F7680-007FFBBF - 18-Audio/members/select_audio_libraries.py\n"
        + "\n".join("%08X" % e for e in _out(tremor)) + "\n")
    open(os.path.join(inv, "cri-hca-decoder.tsv"), "w").write(
        "# CRI HCA decoder, 00121000-0012573F less the folded 001243B0 - 18-Audio/members/select_audio_libraries.py\n"
        + "\n".join("%08X" % e for e in _out(cri)) + "\n")
    open(os.path.join(inv, "libvorbis.tsv"), "w").write(
        "# Xiph libvorbis float codec, 008800C0 up to 008958B0 less 00887630 and A-measured - 18-Audio/members/select_audio_libraries.py\n"
        + "\n".join("%08X" % e for e in _out(vorbis)) + "\n")
    open(os.path.join(inv, "libogg-bitwise.tsv"), "w").write(
        "# libogg bitwise.c, 0017C890 up to 0017CC70 - 18-Audio/members/select_audio_libraries.py\n"
        + "\n".join("%08X" % e for e in _out(bitw)) + "\n")
    print("wrote", *(len(_out(x)) for x in (members, ogg, tremor, cri, vorbis, bitw)))
