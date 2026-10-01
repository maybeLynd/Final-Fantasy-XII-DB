"""subtypes.py - OV-41: the EFX children and their specialized subtypes, as a closed set with a per-subtype relocation map
(FABLE, Claude Opus 5.5, 2026-09-29). STATIC. Writes subtypes.tsv.

  W  THE WALKER 003EDAD0 hands each chunk run to one registrar, each called once in the image and only from the walker:
     0x700 -> 003A7E80 (003EDF97), 0x800 -> 003A9730 (003EE1B7), 0xA00 -> 003A9A70 (003EE0B7)
  G  THE REGISTRARS share one shape: record = chunk + 4; an index (0x700: byte, 0x800/0xA00: word) and a subtype byte
     (chunk +2) stored into the record; the record published at registry[index] (*02EBEFA0 / *02EBEF90 / *02EBEF78); then
     the family's setup switch with the relocation delta; the next chunk address is returned
  S  THE SETUP SWITCHES are bounded: 004FF270 on +0xC2 (subtypes 0-3; anything else returns untouched); 00442460 on +0x282
     (`cmp 8`, a 9-entry table; above 8 returns untouched); 005004C0 on +0x44 (`cmp 0xD1`, a byte-index table into a dword
     table; above 0xD1 -> 00538910). 00538910 is itself a dispatcher for types 0x42-0xAB (+0x44 - 0x42 bounded at 0x69,
     its own tables); any other type it returns untouched, i.e. has no setup (S2). The setup callers besides the registrars are the siblings 003A7DC0 / 003A96A0 /
     003A99F0 and the table-wide refreshes 003A9860 / 003A9BA0 (setup re-run after a move)
  X  EXTRACTION: each setup routine, followed through its field-group helpers, rewrites encoded image-address dwords at
     fixed record offsets - either REBASED (resolve 0020E600, + delta, encode 0020E620) or LINKED (the keyed lookup
     003AA280(id, kind, sub) over the list *02EBEF70, then encode). Per routine: the offset sets, or the reason it did not
     resolve (a loop, a helper called with a computed offset, a store through an untracked base). Written to subtypes.tsv
  C  AGREEMENT: 65 element types have a setup routine and 56 routines serve them - the dispatch page's own census (65
     handled types; setup 38 + sub-setup 18)
  K  KNOWN ANSWER: 00500470 (element subtype 0; the nonempty-registration page executed it) must give exactly the page's
     eight dwords +00/+04/+10/+14/+20/+24/+30/+34. The extractor's first draft gave 4: capstone prints small displacements
     in decimal ([rdi + 4]) and the pattern required 0x
Function bounds come from .pdata (the entry's own RUNTIME_FUNCTION range).
"""
import functools, hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
        for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
PD = [s for s in SECS if s[0] == b".pdata"][0]
FUNCS = {}
for k in range(0, PD[3] - 12, 12):
    b0, e0, u = struct.unpack_from("<III", d, PD[4] + k)
    if b0: FUNCS.setdefault(B + b0, e0 - b0)
TX = [s for s in SECS if s[0] == b".text"][0]
text = d[TX[4]:TX[4] + TX[3]]; tb = B + TX[2]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
def callers(t):
    return [tb + j for j in range(len(text) - 5) if text[j] in (0xE8, 0xE9) and tb + j + 5 + struct.unpack_from("<i", text, j + 1)[0] == t]
# W
check("W", callers(0x3A7E80) == [0x3EDF97] and callers(0x3A9730) == [0x3EE1B7] and callers(0x3A9A70) == [0x3EE0B7],
      "each registrar is called once, from the walker 003EDAD0")
# G
G = {0x3A7E80: ("movzx r8d, byte ptr [rcx]", 0x3A7E9F, "mov byte ptr [rcx + 0xc2], al", 0x3A7EAD, "0x2b170ec", 0x3A7EC3, "call 0x4ff270"),
     0x3A9730: ("movzx r8d, word ptr [rcx]", 0x3A974F, "mov byte ptr [rcx + 0x282], al", 0x3A975D, "0x2b1582c", 0x3A9773, "call 0x442460"),
     0x3A9A70: ("movzx r8d, word ptr [rcx]", 0x3A9A8F, "mov byte ptr [rcx + 0x44], al", 0x3A9A97, "0x2b154da", 0x3A9AAD, "call 0x5004c0")}
gok = []
for f, (ix, sa, ss, ra, rd, ca, cc) in G.items():
    c = dis(f, f + 0x5A)
    gok.append(c.get(f + 0xA) == ix and c.get(sa) == ss and rd in c.get(ra, "") and c.get(ca) == cc
               and any(s.startswith("mov qword ptr [r8 + r9*8], rcx") for s in c.values()))
check("G", all(gok), "the three registrars: index, subtype byte, registry[index] = record, then the family's setup (%s)" % gok)
# S
s1 = dis(0x4FF270, 0x4FF2A7); s2 = dis(0x442460, 0x4424B2); s3 = dis(0x500510, 0x500530)
arms700 = [0x537C80, 0x537FA0, 0x538350, 0x5387B0]
check("S", at(s1, {0x4FF270: "movzx r8d, byte ptr [rcx + 0xc2]", 0x4FF28F: "mov rax, rcx", 0x4FF2A2: "jmp 0x537c80", 0x4FF29D: "jmp 0x537fa0",
                   0x4FF298: "jmp 0x538350", 0x4FF293: "jmp 0x5387b0"})
      and at(s2, {0x442460: "movzx eax, byte ptr [rcx + 0x282]", 0x442467: "cmp eax, 8", 0x44246A: "ja 0x4424ae", 0x4424AE: "mov rax, rcx"})
      and at(s3, {0x500510: "cmp eax, 0xd1", 0x500515: "ja 0x5006a9"})
      and sorted(callers(0x4FF270)) == [0x3A7E1E, 0x3A7EC3] and sorted(callers(0x442460)) == [0x3A96FD, 0x3A9773, 0x3A9899]
      and sorted(callers(0x5004C0)) == [0x3A9A49, 0x3A9AAD, 0x3A9BD9],
      "bounded setup switches (0-3, 0-8, 0-0xD1) and their only callers")
# X
ENC, RES, LINK = 0x20E620, 0x20E600, 0x3AA280
DISP = r"(?: \+ (0x[0-9a-f]+|\d+))?"
def resolve(a):
    for x in cs.disasm(d[off(a):off(a) + 16], a):
        if x.mnemonic == "jmp" and x.op_str.startswith("0x"): return int(x.op_str, 16)
        if x.mnemonic != "mov": return a
    return a
@functools.lru_cache(None)
def reloc(f):
    if f not in FUNCS: return frozenset(), frozenset(), ("no .pdata entry at %08X" % f,)
    ins = list(cs.disasm(d[off(f):off(f) + FUNCS[f]], f)); probs = []
    if any(x.mnemonic.startswith("j") and x.op_str.startswith("0x") and f <= int(x.op_str, 16) < x.address for x in ins):
        probs.append("loop in %08X" % f)
    base = {"rcx": 0}; rcx = 0; reb = set(); lnk = set(); pend = None; kind = None
    for x in ins:
        o, mn = x.op_str, x.mnemonic
        if mn == "mov" and re.fullmatch(r"(r\w+), (r\w+)", o):
            dst, s = o.split(", ")
            if s in base: base[dst] = base[s]
            elif dst in base: del base[dst]
            if dst == "rcx": rcx = base.get(s)
            continue
        m = re.fullmatch(r"rcx, \[(\w+)" + DISP + r"\]", o) if mn == "lea" else None
        if m:
            rcx = base[m.group(1)] + int(m.group(2) or "0", 0) if m.group(1) in base else None
            continue
        if mn in ("call", "jmp") and o.startswith("0x"):
            t = int(o, 16)
            if f <= t < f + FUNCS[f]: continue
            if t == ENC: pend = kind or "?"; rcx = None; continue
            if t == RES: kind = "rebase"; rcx = None; continue
            if t == LINK: kind = "link"; rcx = None; continue
            if rcx is None: probs.append("%08X called with a computed offset" % t)
            else:
                r2, l2, p2 = reloc(t)
                reb |= {rcx + k for k in r2}; lnk |= {rcx + k for k in l2}; probs += list(p2)
            rcx = None
            if mn == "jmp": break
            continue
        if pend:
            m = re.fullmatch(r"dword ptr \[(\w+)" + DISP + r"\], eax", o) if mn == "mov" else None
            if m and m.group(1) in base:
                (reb if pend == "rebase" else lnk).add(base[m.group(1)] + int(m.group(2) or "0", 0)); pend = None; kind = None
            elif m: probs.append("encoded store through an untracked base at %08X" % x.address); pend = None
        if mn == "ret": break
    return frozenset(reb), frozenset(lnk), tuple(sorted(set(probs)))
def table(base, cnt): return [B + struct.unpack_from("<I", d, off(base + 4 * k))[0] for k in range(cnt)]
idx = [d[off(B + 0x3E0774 + k)] for k in range(0xD2)]
arms800 = [resolve(a) for a in table(B + 0x3224B4, 9)]
armsA00 = [resolve(a) for a in table(B + 0x3E06B4, max(idx) + 1)]
rows = []; clean = 0
# 00538910 is itself a dispatcher (types 0x42-0xAB: +0x44 - 0x42 bounded at 0x69, byte-index then dword table); anything
# else it returns untouched (00538996). A linear walk of it would union all eighteen arms, so route through its table.
subidx = [d[off(B + 0x4189E8 + k)] for k in range(0x6A)]
subarms = [resolve(a) for a in table(B + 0x41899C, max(subidx) + 1)]
NOSETUP = 0x538996
def routeA00(k):
    a = armsA00[idx[k]]
    if a != 0x538910: return a
    return subarms[subidx[k - 0x42]] if 0 <= k - 0x42 <= 0x69 else NOSETUP
s4 = dis(0x538910, 0x53893C)
check("S2", at(s4, {0x538910: "movzx eax, byte ptr [rcx + 0x44]", 0x538914: "add eax, -0x42", 0x538917: "cmp eax, 0x69",
                    0x53891A: "ja 0x538996"}) and dis(0x538996, 0x53899A) == {0x538996: "mov rax, rcx", 0x538999: "ret"},
      "the sub-range dispatcher 00538910: types 0x42-0xAB through its own table, anything else untouched")
fam = [("0x700", {k: a for k, a in enumerate(arms700)}), ("0x800", {k: a for k, a in enumerate(arms800)}),
       ("0xA00", {k: routeA00(k) for k in range(0xD2)})]
seen = {}
for famname, m in fam:
    for sub, a in sorted(m.items()):
        if a in (0x5006A9, NOSETUP):
            rows.append("%s	%#x	-	0	0			no setup: the dispatcher returns the record untouched" % (famname, sub)); continue
        if a not in seen:
            seen[a] = reloc(a); clean += not seen[a][2]
        r, l, p = seen[a]
        rows.append("%s\t%#x\t%08X\t%d\t%d\t%s\t%s\t%s" % (famname, sub, a, len(r), len(l), " ".join("%x" % k for k in sorted(r)),
                    " ".join("%x" % k for k in sorted(l)), "; ".join(p)))
open(os.path.join(HERE, "subtypes.tsv"), "w", encoding="utf-8", newline="\n").write(
    "family\tsubtype\troutine\trebased\tlinked\trebased_offsets\tlinked_offsets\tunresolved\n" + "\n".join(rows) + "\n")
distinct = len(seen)
check("X", distinct >= 50, "%d distinct setup routines over %d (family, subtype) rows; %d resolve cleanly, %d carry a named reason"
      % (distinct, len(rows), clean, distinct - clean))
# C: agreement with the dispatch page's independent census (effect-element-type-dispatch.md section 2.5: 65 handled types;
# setup 38 + sub-setup 18 handlers)
withsetup = [k for k in range(0xD2) if routeA00(k) not in (NOSETUP, 0x5006A9)]
a00routines = {routeA00(k) for k in withsetup}
check("C", len(withsetup) == 65 and len(a00routines) == 56,
      "element types with a setup routine: %d (the dispatch page: 65); distinct element setup routines: %d (38 + 18 = 56)"
      % (len(withsetup), len(a00routines)))
# K
r0, l0, p0 = reloc(0x500470)
check("K", sorted(r0) == [0, 4, 0x10, 0x14, 0x20, 0x24, 0x30, 0x34] and not l0 and not p0,
      "known answer: 00500470 rebases exactly +00/+04/+10/+14/+20/+24/+30/+34")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
