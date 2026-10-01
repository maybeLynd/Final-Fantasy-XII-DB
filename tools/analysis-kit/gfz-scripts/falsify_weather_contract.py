"""Falsification pass 1 on CONTRACT-weather (OPUS, 2026-09-29), re-derived from the shipping image and the shipped archive.

Each check states its KILLER first; a claim survives only if the killer is absent.

  W0  §15 every body's extent and sha256 (8+4 hex) as cited                              KILLER: one differs
  W1  P-1/P-2 the manager-index gate, the init bit, the latched path to 002621A8 and its two posts   KILLER: a skip of the posts
  W2  I-1 every cited domain crossing is an explicit +/-1                                 KILLER: a site that is not
  W3  I-2 the clamps in 0026D910 and 002658B0 saturate (jns/cmovg); the verb clamps 1..3 again   KILLER: a failure branch
  W4  I-3 the restore gate skips the commit store; the flag is cleared on the common tail the bail-out reaches
  W5  I-4/I-5 9*(3*sel+slot) and the -10; the selector bound is the only bound; the weather file's size fits 776x3 zero-based
  W6  I-6 / §7 the resolver's only RNG call is 0025ABB8; the fallbacks keep the current slot
  W7  I-7 gameplay extraction takes edi+1 (edi unmodified since the clamp); presentation takes 00265920()
  W8  §5 image-wide RIP-relative census of 02099DA8/DAC/DB0/DBC: writers and readers as tabled; DB0 unread
  W9  §5 nothing is allocated on the path                                                 KILLER: an allocator call
  W10 §7 the retention tests at 0025ACD4 / 0025ACD8 / 0025ACEC
  W11 §8 probability reader: 33 default at 00265910; container guards; +0x64
  W12 §8 setweatherslot's three guards before the apply
  W13 §9 MT19937: thunk, lazy seed 5489, pre-shifted tempering masks; multiply-high scaling; the 50 split
  W14 §6 the debug override is read by separate test and take calls at every cited site
  W15 §10.4 envIndex >= 16 defaults to 0 at 0026DA1C / 0026DA76
  W16 §11 the combat stage has no arm for 02099DA8 == 4                                    KILLER: a compare with 4 or a default
  W17 §8 the authored populations re-decoded from map_ref.bin (in and ch)
"""
import collections, hashlib, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
MAPREF = {k: os.path.join(ROOT, "Tools", "work", "DATA", "labelscan", "ps2data__image__ff12__%s__common__map_ref.bin" % k) for k in ("in", "ch")}
WEATHERINFO = os.path.join(ROOT, "Tools", "work", "repos-2d", "vbf", "ps2data", "image", "ff12", "in", "common", "gramap_weatherinfo.bin")
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

_cache = {}
def body(a):
    if a not in _cache:
        _cache[a] = list(md.disasm(blob[OFF(a):OFF(a) + sizes[a]], a))
    return _cache[a]
def at(a):
    for f in _cache.values():
        for x in f:
            if x.address == a:
                return x
    x = next(md.disasm(blob[OFF(a):OFF(a) + 16], a))
    return x
def T(x):
    return x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
def rip(x):
    return [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
def s(x):
    return "%s %s" % (x.mnemonic, x.op_str)

B = {0x0026D910: (418, "1703f5dc", "b4d2"), 0x003777C0: (144, "a3688ce2", "cd2e"), 0x0025ABA0: (253, "e667fef7", "ddd4"),
     0x0025ACA0: (107, "1b3c8438", "c464"), 0x002658B0: (112, "9689942f", "c8e7"), 0x002620E0: (231, "7605a770", "182f"),
     0x002E3D40: (116, "064ffe13", "26f0"), 0x003565C0: (99, "5819ab38", "aa9a"), 0x00863BF0: (141, "b158ad91", "3c2d")}
for a in list(B) + [0x0026D8F0, 0x00265920]:
    body(a)

# W0
bad = []
for a, (n, h0, h1) in B.items():
    h = hashlib.sha256(blob[OFF(a):OFF(a) + n]).hexdigest()
    if sizes.get(a) != n or not (h.startswith(h0) and h.endswith(h1)):
        bad.append("%08X size %s hash %s..%s" % (a, sizes.get(a), h[:8], h[-4:]))
check("W0", not bad and sizes.get(0x0026D8F0) == 21 and sizes.get(0x00265920) == 41, "9 cited bodies: mismatches %s; 0026D8F0 %s B, 00265920 %s B" % (
    bad or "none", sizes.get(0x0026D8F0), sizes.get(0x00265920)))

# W1
f = body(0x002620E0); ix = {x.address: k for k, x in enumerate(f)}
g1 = s(at(0x002620E6)); g2 = s(at(0x002620F3)); j = at(0x002620F7); setb = s(at(0x002621A4))
tail = f[ix[0x002621A8]:]
posts = []
for k, x in enumerate(tail):
    if x.mnemonic in ("call", "jmp") and T(x) == 0x003601C0:
        arg = next((s(y) for y in reversed(tail[:k]) if y.op_str.startswith("ecx,")), None)   # the last ecx load before the post
        posts.append((arg, s(x)))
check("W1", "rcx + 0x28" in g1 and "rcx + 0x10], 4" in g2 and T(j) == 0x002621A8 and "4" in setb
      and [p[0] for p in posts] == ["mov ecx, 0xb", "mov ecx, 0xc"] and [p[1].split()[0] for p in posts] == ["call", "jmp"],
      "002620E6 `%s`; 002620F3 `%s`; 002620F7 -> %s; 002621A4 `%s`; from 002621A8: %s" % (g1, g2, "%08X" % T(j) if T(j) else s(j), setb, posts))

# W2
cr = {a: s(at(a)) for a in (0x0026D933, 0x00265942, 0x0025ACC8, 0x002658B8, 0x0026DA04, 0x0026DA2E)}
pm1 = lambda t: bool(re.search(r"^(inc|dec) |^(add|sub) .*, (1|-1|0xffffffff)$|^lea .*[+-] 1\]$", t))
check("W2", all(pm1(t) for t in cr.values()), "crossings: %s" % {("%08X" % k): v for k, v in cr.items()})

# W3
def span(a0, a1, fn):
    return [x for x in body(fn) if a0 <= x.address <= a1]
c1 = [x.mnemonic for x in span(0x0026D936, 0x0026D943, 0x0026D910)]
c2 = [x.mnemonic for x in span(0x002658B8, 0x002658C8, 0x002658B0)]
c3 = [s(x) for x in span(0x003565F6, 0x00356609, 0x003565C0)]
check("W3", "jns" in c1 and "cmovg" in c1 and "jns" in c2 and "cmovg" in c2 and not any(m in ("call", "ret") for m in c1 + c2),
      "0026D936..43 %s; 002658B8..C8 %s; verb 003565F6..609 %s" % (c1, c2, c3))

# W4
g = body(0x0026D910); gi = {x.address: k for k, x in enumerate(g)}
t951 = s(at(0x0026D951)); jg = g[gi[0x0026D951] + 1] if 0x0026D951 in gi else None
store = s(at(0x0026D95E)); clr = s(at(0x0026DA92))
skip = jg is not None and jg.mnemonic in ("jne", "jnz") and T(jg) > 0x0026D95E
bail = [x for x in g if x.mnemonic.startswith("j") and T(x) == 0x0026DA83]
check("W4", "0x1061" in t951 and skip and "0x1060" in store and "0x1061" in clr and 0x0026DA83 < 0x0026DA92 and bail,
      "0026D951 `%s` then `%s`; commit 0026D95E `%s`; clear 0026DA92 `%s`; %d branches reach the bail-out 0026DA83, which falls through to the clear" % (
          t951, s(jg) if jg else None, store, clr, len(bail)))

# W5
w = body(0x003777C0)
arith = [s(x) for x in w if 0x003777DC <= x.address <= 0x003777E9]
minus = [s(x) for x in w if 0x003777F9 <= x.address <= 0x00377809]
bound = s(at(0x003777D3)) + " ; " + s(at(0x003777D8)) + " ; " + s(at(0x003777DA))
edx_tests = [s(x) for x in w if x.mnemonic in ("cmp", "test") and re.match(r"(edx|rdx|dx)\b", x.op_str)]
wi = os.path.getsize(WEATHERINFO) if os.path.exists(WEATHERINFO) else None
zero_based = 8 + (776 * 3 * 9 + 7) // 8
one_based = 8 + ((3 * 775 + 3 + 1) * 9 + 7) // 8
# the -10: r9d = width - 1 (003777F3); start bit = 9*(3*sel+slot) + bitOffset + (width - 1) - 9  (003777EC, 003777F9..00377809)
comp = [s(x) for x in w if 0x003777DC <= x.address <= 0x00377809]
minus10 = ("lea eax, [rdx + rcx*2]" in comp and "add ecx, eax" in comp and "lea eax, [rcx + rcx*8]" in comp and "lea ecx, [rax + r8]" in comp
           and "sub r9d, 1" in comp and "lea r10d, [r9 - 9]" in comp)
check("W5", "+ 6]" in bound and "cmp ecx, eax" in bound and "jge" in bound and minus10 and not edx_tests and wi is not None and zero_based <= wi < one_based,
      "003777DC..E9 %s; 003777F9..809 %s; 003777D3 `%s`; compares on the slot register: %s; gramap_weatherinfo %s B (776x3 zero-based needs %d, one-based %d)" % (
          arith, minus, bound, edx_tests or "none", wi, zero_based, one_based))

# W6
r = body(0x0025ABA0)
rng = [("%08X" % x.address) for x in r if x.mnemonic in ("call", "jmp") and T(x) == 0x00379CD0]
fb = {a: s(at(a)) for a in (0x0025ABF0, 0x0025AC24, 0x0025AC47, 0x0025AC88)}
starts = {x.address for x in r}
# CORRECTED citation (pass 1): 0025AC24 is not an instruction boundary (inside 0025AC20 `mov rbx, [rsp+0x30]`); the slot-2 "stay"
# fallback of the prefer-3 arm is `setle cl` + `lea eax, [rcx+1]` at 0025AC1D - ecx, not edx
check("W6", rng == ["0025ABB8"] and 0x0025AC24 not in starts and s(at(0x0025AC1D)) == "lea eax, [rcx + 1]" and s(at(0x0025AC1A)) == "setle cl"
      and s(at(0x0025ABF0)) == "lea eax, [rcx + 2]" and s(at(0x0025AC47)) == "mov edi, 3" and s(at(0x0025AC88)) == "mov ebx, 1",
      "RNG call sites in the resolver: %s; 0025AC24 an instruction start: %s; 0025AC1A/1D `%s` / `%s`; 0025ABF0 `%s`; 0025AC47 `%s`; 0025AC88 `%s`" % (
          rng, 0x0025AC24 in starts, s(at(0x0025AC1A)), s(at(0x0025AC1D)), s(at(0x0025ABF0)), s(at(0x0025AC47)), s(at(0x0025AC88))))

# W7
gp = [s(x) for x in g if 0x0026DA20 <= x.address <= 0x0026DA31]
edi_w = [s(x) for x in g if 0x0026D943 < x.address < 0x0026DA2E and re.match(r"(edi|rdi|di)\b", x.op_str) and x.mnemonic not in ("cmp", "test", "push")
         and not x.op_str.startswith(("edi, edi", "rdi, rdi")) is False]
edi_w = [s(x) for x in g if 0x0026D943 < x.address < 0x0026DA2E and x.op_str.split(",")[0].strip() in ("edi", "rdi", "di", "dil") and x.mnemonic not in ("cmp", "test")]
pr = [s(x) for x in body(0x002E3D40) if 0x002E3D60 <= x.address <= 0x002E3D79]
check("W7", any("0x377850" in t for t in gp) and not edi_w and any("0x265920" in t for t in pr) and any("0x377850" in t for t in pr),
      "gameplay 0026DA20..31 %s; writes to edi between the clamp and the call: %s; presentation 002E3D60..79 %s" % (gp, edi_w or "none", pr))

# W8
text = next(x for x in SECS if x[0] == ".text")
allins = md.disasm(blob[text[3]:text[3] + text[4]], text[1])
G4 = {0x02099DA8: "DA8", 0x02099DAC: "DAC", 0x02099DB0: "DB0", 0x02099DBC: "DBC"}
fn_of = sorted(sizes)
import bisect
def owner(a):
    k = bisect.bisect_right(fn_of, a) - 1
    return fn_of[k] if k >= 0 and fn_of[k] <= a < fn_of[k] + sizes[fn_of[k]] else None
acc = collections.defaultdict(lambda: {"w": set(), "r": set()})
md.detail = True
# per function body: a linear sweep of .text stops at the first undecodable byte, so decode each listed body instead
for fa in fn_of:
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code_ = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    for x in md.disasm(code_, fa):
        for o in x.operands:
            if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP:
                t = x.address + x.size + o.mem.disp
                if t in G4:
                    wr = x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "movss", "and", "or", "inc", "dec", "add", "sub", "xor")
                    acc[G4[t]]["w" if wr else "r"].add("%08X" % fa)
got = {k: {kk: sorted(v) for kk, v in d.items()} for k, d in acc.items()}
want = {"DA8": {"w": ["0026D910"], "r": ["00263E10"]}, "DAC": {"w": ["0026D910"], "r": ["00263E20"]},
        "DB0": {"w": ["0026D910"], "r": []}, "DBC": {"w": ["0026AB40", "0026D910"], "r": ["00264D50"]}}
check("W8", got == want, "RIP-relative census %s" % got)

# W9
alloc = {0x006DA880, 0x006DA8A0}
path = (0x0026D910, 0x0025ACA0, 0x0025ABA0, 0x002620E0)
ac = [("%08X" % a, "%08X" % T(x)) for a in path for x in body(a) if x.mnemonic == "call" and T(x) in alloc]
names = [("%08X" % a, "%08X" % T(x)) for a in path for x in body(a) if x.mnemonic == "call" and T(x) and T(x) in sizes]
check("W9", not ac, "allocator calls on the path: %s; direct callees %d" % (ac or "none", len(names)))

# W10
nx = lambda a: at(a + at(a).size)
check("W10", s(at(0x0025ACD4)) == "test eax, eax" and nx(0x0025ACD4).mnemonic == "je" and s(at(0x0025ACD8)) == "cmp edi, 0x64" and nx(0x0025ACD8).mnemonic == "jge"
      and s(at(0x0025ACEC)) == "cmp rcx, rdi" and nx(0x0025ACEC).mnemonic == "jb",
      "0025ACD4 `%s` / `%s`; 0025ACD8 `%s` / `%s`; 0025ACEC `%s` / `%s`" % (s(at(0x0025ACD4)), s(nx(0x0025ACD4)), s(at(0x0025ACD8)), s(nx(0x0025ACD8)),
                                                                         s(at(0x0025ACEC)), s(nx(0x0025ACEC))))

# W11
p = body(0x002658B0)
d33 = s(at(0x00265910)); refs = {("%08X" % t) for x in p for t in rip(x)}
check("W11", d33 == "mov eax, 0x21" and {"02098E10", "02098E20"} <= refs and any("0x64" in x.op_str for x in p),
      "00265910 `%s`; globals read %s; +0x64 present %s" % (d33, sorted(refs), any("0x64" in x.op_str for x in p)))

# W12
v = [s(x) for x in body(0x003565C0) if 0x003565D7 <= x.address <= 0x003565F4]
check("W12", any("0x28" in t for t in v) and any("0x12" in t for t in v) and any("0x50" in t for t in v),
      "003565D7..F4: %s" % v)

# W13
th = list(md.disasm(blob[OFF(0x00379CD0):OFF(0x00379CD0) + 5], 0x00379CD0))
mt = body(0x00863BF0)
seed = s(at(0x00863C09)); masks = [s(x) for x in mt if "0xff3a58ad" in x.op_str or "0xffffdf8c" in x.op_str]
sc1 = [s(x) for x in body(0x0025ACA0) if 0x0025ACE4 <= x.address <= 0x0025ACE8]
sc2 = [s(x) for x in r if 0x0025ABBF <= x.address <= 0x0025ABC7]
check("W13", th and th[0].mnemonic == "jmp" and T(th[0]) == 0x00863BF0 and "0x1571" in seed and len(masks) == 2
      and any("0x64" in t for t in sc1) and any("shr" in t and "0x20" in t for t in sc1) and any("0x32" in t for t in sc2),
      "00379CD0 `%s`; seed 00863C09 `%s`; masks %s; roll scaling %s; resolver %s" % (s(th[0]) if th else None, seed, masks, sc1, sc2))

# W14
def ovr(a):
    return ["%08X" % x.address for x in body(a) if x.mnemonic in ("call", "jmp") and T(x) == 0x0017D490]
o = {("%08X" % a): ovr(a) for a in (0x002620E0, 0x0026D910, 0x00265920, 0x0025ACA0)}
want14 = {"002620E0": ["0026210E", "00262117", "00262139", "00262142", "00262167", "00262170"], "0026D910": ["0026D921", "0026D92A"],
          "00265920": ["00265924", "00265931"], "0025ACA0": ["0025ACAA", "0025ACB3"]}
check("W14", o == want14 and sizes.get(0x0017D490) == 20, "override reads %s; 0017D490 %s B" % (o, sizes.get(0x0017D490)))

# W15
e1 = [s(x) for x in g if 0x0026DA10 <= x.address <= 0x0026DA26]; e2 = [s(x) for x in g if 0x0026DA66 <= x.address <= 0x0026DA7D]
# sharpened (pass 1): the guard is a SIGNED `jge` against the table's own count dword (16 when shipped), not a literal 16; the
# default is ebx, zeroed once at 0026D931 and not written again before 0026DA78
ebx_w = [x.address for x in g if x.op_str.split(",")[0].strip() in ("ebx", "rbx", "bl") and x.address < 0x0026DA78]
check("W15", "cmp eax, dword ptr [rcx]" in e1 and "jge 0x26da24" in e1 and "mov edx, ebx" in e1 and "cmp edx, dword ptr [rcx]" in e2 and "jge 0x26da7d" in e2
      and ebx_w == [0x0026D931] and s(at(0x0026D931)) == "xor ebx, ebx",
      "class lookup %s; boolean lookup %s" % (e1, e2))

# W16
cs = body(0x0038B220)
cmp4 = [s(x) for x in cs if x.mnemonic == "cmp" and x.op_str.endswith(", 4") and x.op_str.startswith(("eax", "ecx", "edx"))]
arms = {a: s(at(a)) for a in (0x0038B2A8, 0x0038B3F4, 0x0038B478, 0x0038B4FE, 0x0038B584)}
jtab = [s(x) for x in cs if x.mnemonic == "jmp" and x.operands[0].type != X86_OP_IMM]
check("W16", not cmp4 and not jtab and arms[0x0038B478] == "cmp eax, 2" and arms[0x0038B4FE] == "cmp eax, 1" and arms[0x0038B584] == "cmp eax, 3",
      "arms %s; compares with 4: %s; computed jumps: %s" % ({("%08X" % k): v2 for k, v2 in arms.items()}, cmp4 or "none", jtab or "none"))

# W17
res = {}
for loc, path_ in MAPREF.items():
    d = open(path_, "rb").read()
    hdr = struct.unpack_from("<8i", d, 0)
    rows_off, blk_off, cls_off, bool_off = hdr[1], hdr[2], hdr[4], hdr[6]
    nrows = (blk_off - rows_off) // 8
    rows = [struct.unpack_from("<HhI", d, rows_off + 8 * i) for i in range(nrows)]
    nblk = (cls_off - blk_off) // 16
    ncls = struct.unpack_from("<I", d, cls_off)[0]; cls = list(struct.unpack_from("<%dI" % ncls, d, cls_off + 4))
    nb = struct.unpack_from("<I", d, bool_off)[0]; bl = list(d[bool_off + 4:bool_off + 4 + nb])
    lanes = [d[blk_off + 16 * b + 4 * sl: blk_off + 16 * b + 4 * sl + 4] for b in range(nblk) for sl in (1, 2, 3)]
    env = collections.Counter(l[0] for l in lanes)
    da8 = collections.Counter(cls[l[0]] if l[0] < ncls else 0 for l in lanes)
    res[loc] = {"sha": hashlib.sha256(d).hexdigest()[:8], "size": len(d), "magic": d[:4], "rows": nrows, "blocks": nblk, "lanes": len(lanes),
                "selectors": len({r_[0] for r_ in rows}), "sel_range": (min(r_[0] for r_ in rows), max(r_[0] for r_ in rows)),
                "blk_range": (min(r_[1] for r_ in rows), max(r_[1] for r_ in rows)), "cls": cls, "bool": bl, "env": dict(sorted(env.items())),
                "da8": dict(sorted(da8.items())), "lane2": collections.Counter(l[2] for l in lanes)}
a_ = res["in"]
ok17 = (res["in"]["sha"] == res["ch"]["sha"] == "7c63552f" and a_["magic"] == b"MRF\x02" and a_["size"] == 12288 and a_["rows"] == 1315 and a_["blocks"] == 93
        and a_["lanes"] == 279 and a_["selectors"] == 531 and a_["sel_range"] == (1, 775) and a_["blk_range"][0] >= 0
        and a_["cls"] == [4, 4, 4, 0, 0, 1, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0] and a_["bool"] == [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        and a_["env"] == {0: 163, 1: 64, 2: 19, 3: 7, 4: 4, 5: 1, 6: 2, 7: 2, 8: 16, 9: 1} and a_["da8"].get(4) == 246 and a_["lane2"] == {0: 279})
check("W17", ok17, "map_ref in/ch sha %s/%s, %d B, %d rows, %d blocks, %d lanes, %d selectors %s, block index %s; class table %s; env %s; 02099DA8 %s; lane+2 %s" % (
    res["in"]["sha"], res["ch"]["sha"], a_["size"], a_["rows"], a_["blocks"], a_["lanes"], a_["selectors"], a_["sel_range"], a_["blk_range"], a_["cls"],
    a_["env"], a_["da8"], dict(a_["lane2"])))

print("BROKEN %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
