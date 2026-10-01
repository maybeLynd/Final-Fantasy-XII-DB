"""bq23_tier6.py - BQ-23: the four CxxStandardLibrary sub-labels compared with their upstream sources at tier 6
(FABLE, Claude Opus 5.5, 2026-09-27). Static; upstream = MSVC STL (<xtree>, <xstring>, <xmemory>, <regex>) and EASTL
(rbtree.cpp), both public source.

  T1 EASTL is linked: the image carries "EASTL map", "EASTL set", "EASTL basic_string" and .?AVallocator@eastl@@.
  T2 0016D6D0 / 0016D720 / 0016D840 are EASTL's RBTreeIncrement / RBTreeDecrement / RBTreeInsert line for line: node
     {right +0, left +8, parent +0x10, colour byte +0x18, red = 0}; Decrement's first test is the anchor idiom
     parent->parent == node && colour == red -> right; Insert sets parent, nulls both children, colours red, then
     maintains the anchor's root/leftmost/rightmost. MSVC's _Tree instead keeps _Isnil at +0x19 and never uses the
     anchor idiom.
  T3 MSVC markers: _Isnil byte +0x19 or the head-node word 0x0101 at +0x18 (_Tree); the big-block constants 0x1000 and
     0x27 (_Allocate/_Deallocate); those plus the capacity test against 0xF/0x10 at +0x18 (basic_string).
  T4 per-family partition (a member inherits a class from a classified callee in its own family):
     OrderedContainerRuntime 30 = 18 EASTL rbtree + 3 MSVC _Tree + 9 unmatched;
     ContainerAllocatorSupport 40 = 31 MSVC + 9 unmatched; StringHeapAlgorithms 6 = 6 MSVC;
     StdRegex.Runtime 21: none carries a T3 marker, but the image's RTTI holds MSVC <regex>'s eleven node classes and
     the 19 functions installing their vtables lie in the same span as the 21 members, 12 of which call-link to them.
  T5 control: 400 random functions outside the label match a marker at most 1 % of the time as MSVC, and the EASTL
     hits among them are more EASTL code (the helpers are EASTL's own), not a false signature.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, random, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
W = ROOT / "Database/Tools/work"
d = (W / "exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

check("T1 EASTL is linked", all(s in d for s in (b"EASTL map\0", b"EASTL set\0", b"EASTL basic_string\0", b".?AVallocator@eastl@@")))
inc = dis(0x16D6D0, 0x16D710); dec = dis(0x16D720, 0x16D75F); ins = dis(0x16D840, 0x16D899)
ok_inc = (inc.get(0x16D6D3) == "mov rcx, qword ptr [rcx]" and inc.get(0x16D6DB) == "mov rax, qword ptr [rcx + 8]"
          and inc.get(0x16D6F4) == "mov rcx, qword ptr [rax + 0x10]" and inc.get(0x16D6F8) == "cmp rax, qword ptr [rcx]")
ok_dec = (dec.get(0x16D720) == "mov rax, qword ptr [rcx + 0x10]" and dec.get(0x16D727) == "cmp qword ptr [rax + 0x10], rcx"
          and dec.get(0x16D72D) == "cmp byte ptr [rcx + 0x18], 0" and dec.get(0x16D733) == "mov rax, qword ptr [rcx]"
          and dec.get(0x16D737) == "mov rcx, qword ptr [rcx + 8]")
ok_ins = (ins.get(0x16D842) == "mov qword ptr [rcx + 0x10], rdx" and ins.get(0x16D846) == "mov qword ptr [rcx], rax"
          and ins.get(0x16D849) == "mov qword ptr [rcx + 8], rax" and ins.get(0x16D84D) == "mov byte ptr [rcx + 0x18], al"
          and ins.get(0x16D855) == "mov qword ptr [rdx + 8], rcx" and ins.get(0x16D85E) == "mov qword ptr [r8 + 0x10], rcx"
          and ins.get(0x16D86A) == "mov qword ptr [r8 + 8], rcx" and ins.get(0x16D870) == "mov qword ptr [rdx], rcx"
          and ins.get(0x16D87B) == "cmp rcx, qword ptr [r8 + 0x10]" and ins.get(0x16D894) == "cmp byte ptr [rax + 0x18], 0")
no19 = not any("0x19]" in t for t in list(inc.values()) + list(dec.values()) + list(ins.values()))
check("T2 the three helpers are EASTL RBTreeIncrement / RBTreeDecrement / RBTreeInsert", ok_inc and ok_dec and ok_ins and no19,
      "inc %s dec %s ins %s no-isnil %s" % (ok_inc, ok_dec, ok_ins, no19))

EASTL = {0x16D6D0, 0x16D720, 0x16D840}
VT = {0x905A28, 0x9059D8, 0x9058F0, 0x905910, 0x9058C0, 0x905900, 0x9058E0, 0x905940, 0x905920, 0x905930, 0x905950}
fam = collections.defaultdict(list); allf = []; tags = {}
for l in (W / "graph/functions.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    f = l.split("\t"); a = int(f[0], 16); sz = int(f[2]); allf.append((a, sz)); tags[a] = f[8] if len(f) > 8 else ""
    for t in tags[a].split(";"):
        for key in ("ContainerAllocatorSupport", "StdRegex.Runtime", "OrderedContainerRuntime", "StringHeapAlgorithms"):
            if key in t and "CxxStandardLibrary" in t and (a, sz) not in fam[key]: fam[key].append((a, sz))
feat = {}
def feats(a, sz):
    if a in feat: return feat[a]
    s = set(); callees = set(); o = off(a)
    if o is not None:
        for x in cs.disasm(d[o:o + sz], a):
            t = "%s %s" % (x.mnemonic, x.op_str)
            if re.search(r"byte ptr \[r\w+ \+ 0x19\]", t): s.add("isnil19")
            if re.search(r"word ptr \[r\w+ \+ 0x18\], 0x101$", t): s.add("head0101")
            if re.search(r"(cmp|sub|add|lea).*0x1000\b", t): s.add("x1000")
            if re.search(r"0x27\]|, 0x27$", t): s.add("x27")
            if "cmp" in t and re.search(r"qword ptr \[r\w+ \+ 0x18\], 0x(f|10)$", t): s.add("sso18")
            if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
                c = int(x.op_str, 16); callees.add(c)
                if c in EASTL: s.add("eastl")
            m = re.search(r"\[rip \+ 0x([0-9a-f]+)\]", x.op_str)
            if m and x.address + x.size + int(m.group(1), 16) in VT: s.add("regexvt")
    if a in EASTL: s.add("eastl")
    feat[a] = (s, callees); return feat[a]
def classify(a, sz):
    s, _ = feats(a, sz)
    if "eastl" in s: return "EASTL rbtree"
    if s & {"isnil19", "head0101"}: return "MSVC _Tree"
    if {"x1000", "x27"} <= s: return "MSVC basic_string" if "sso18" in s else "MSVC allocate"
    if "regexvt" in s: return "MSVC regex node"
    return None
part = {}
for k, v in fam.items():
    first = {a: classify(a, sz) for a, sz in v}
    for _ in range(3):
        for a, sz in v:
            if first[a] is None:
                inh = {first[c] for c in feats(a, sz)[1] if first.get(c)}
                if len(inh) == 1: first[a] = next(iter(inh))
    c = collections.Counter(("EASTL" if x and x.startswith("EASTL") else "MSVC" if x else "unmatched") for x in first.values())
    part[k] = (dict(c), sorted(a for a, x in first.items() if x is None))
got = {k: v[0] for k, v in part.items()}
check("T4 the per-family partition",
      got.get("OrderedContainerRuntime") == {"EASTL": 18, "MSVC": 3, "unmatched": 9}
      and got.get("ContainerAllocatorSupport") == {"MSVC": 31, "unmatched": 9}
      and got.get("StringHeapAlgorithms") == {"MSVC": 6}
      and got.get("StdRegex.Runtime") == {"unmatched": 21}, str(got))
for k, (c, um) in part.items(): print("   %s unmatched: %s" % (k, " ".join("%08X" % a for a in um)))
random.seed(7)
ctrl = random.sample([x for x in allf if 40 <= x[1] <= 1200 and "CxxStandardLibrary" not in tags[x[0]]], 400)
cc = collections.Counter(classify(a, sz) or "none" for a, sz in ctrl)
msvc = sum(v for k, v in cc.items() if k.startswith("MSVC"))
check("T5 control: MSVC markers hit at most 1 % of 400 unlabelled functions", msvc <= 4, str(dict(cc)))
import bisect
rtti = [b".?AV_Node_base@std@@", b".?AV?$_Node_class@DV?$regex_traits@D@std@@@std@@", b".?AV?$_Node_str@D@std@@",
        b".?AV_Node_assert@std@@", b".?AV_Node_back@std@@", b".?AV_Node_capture@std@@", b".?AV_Node_end_group@std@@",
        b".?AV_Node_rep@std@@", b".?AV_Node_end_rep@std@@", b".?AV_Node_if@std@@", b".?AV_Node_endif@std@@"]
starts = sorted(a for a, _ in allf); sizes = dict(allf)
def owner(v):
    i = bisect.bisect_right(starts, v) - 1
    return starts[i] if i >= 0 and v < starts[i] + sizes[starts[i]] else None
text = [x for x in secs if x[1] == 0x1000][0]
inst = set()
for m in re.finditer(rb"[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]", d[text[3]:text[3] + text[2]]):
    fo = text[3] + m.start(); va = fo - text[3] + text[1] + BASE
    if va + 7 + struct.unpack_from("<i", d, fo + 3)[0] in VT:
        o = owner(va)
        if o: inst.add(o)
regex = {a for a, _ in fam["StdRegex.Runtime"]}
group = inst | regex
linked = {a for a in regex if (feats(a, sizes[a])[1] & group) or any(a in feats(b, sizes[b])[1] for b in group)}
check("T6 MSVC <regex> node classes are in the image; their vtable installers share the labelled members' span",
      all(r in d for r in rtti) and len(inst) == 19 and min(inst) >= 0x203240 and max(inst) <= 0x209E00
      and not (inst & regex) and len(linked) == 12,
      "installers %d in %08X..%08X, labelled members call-linked %d of %d" % (len(inst), min(inst), max(inst), len(linked), len(regex)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
