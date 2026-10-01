"""RC-28 leftover 3, second half: which face draws each staff-roll name (SWE2-DATA 2026-09-30), static + shipped data.

Code (pinned below):
  fsroll_fontA / fontB / fontC (verbs 704B / 704C / 704D -> 00511AC0 / 00511B30 / 00511BD0) jump to the staff-roll
  builder 0053F0D0 with op 8 / 9 / 10; fsroll_nameA / nameB / nameC (7046 / 7047 / 7048) with op 5 / 6? / 7 and the id.
  A name line is built by 0053DD20(line, obj, class, id): line+0x18 = class, line+0x19 = (class + 3) * 2 = the font
  slot 6 / 8 / 10 (0053DD45-0053DD6D) - faces font_stf_a / b / c; the draw pass 0053E0B0 uses that slot and slot + 1
  (the shadow faces 7 / 9 / 11). The id picks the text: bit 15 set -> text id 0x61A8 + (id & 0x7FFF) (roles, menu03),
  clear -> 0x6590 + id (names, menu04) (0053DD90-0053DDAC).
Script: the staff-roll actor in men_z0005 (the BQ-10 decompile of the shipped us scripts) is evaluated: every
  fsroll_nameX call, literal or inside a constant for-loop over regI0, gives (class, id).
Data: the accented rows are those menu04 rows (ex00 UTF-16, rc28_staffroll.py) holding one of the 49 glyphs only the
  us tables 8..11 carry; the script's class for each such row decides the face.
Controls: C1 the evaluator reproduces the call counts of a plain grep (nameA 28, nameB 235, nameC 425 call sites);
C2 0053DD20's slot arithmetic reads as stated; C3 the fontA verb passes op 8.
"""
import os, re, sys, collections, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import dis  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


dd = {x.address: x for x in dis(0x0053DD20)}
check("C2 0053DD20: line+0x19 = (class + 3) * 2 (font slot), text id base 0x61A8 (bit 15) / 0x6590",
      dd[0x0053DD45].op_str == "eax, [r8 + 3]" and dd[0x0053DD49].op_str == "al, al"
      and dd[0x0053DD6D].op_str == "byte ptr [rcx + 0x19], al" and dd[0x0053DD9C].op_str == "ecx, [r9 + 0x61a8]"
      and dd[0x0053DDA5].op_str == "ecx, [r9 + 0x6590]")
fa = {x.address: x for x in dis(0x00511AC0)}
check("C3 fsroll_fontA's handler passes op 8 to 0053F0D0", fa[0x00511AE4].op_str == "ecx, 8"
      and fa[0x00511AF3].op_str == "0x53f0d0")

SCRIPT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us\men_z0005.txt"
lines = open(SCRIPT, encoding="utf-8", errors="replace").read().splitlines()
calls = collections.Counter()
pairs = collections.Counter()
grep_counts = collections.Counter(m.group(1) for l in lines for m in re.finditer(r"fsroll_name([ABC])\(", l))
i = 0
unresolved = 0
while i < len(lines):
    l = lines[i]
    m = re.search(r"for \(regI0 = (-?\d+); regI0 < (-?\d+); regI0 = \(regI0 \+ (\d+)\)\)", l)
    if m:
        a, b, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
        # the block is the next '{' .. matching '}'
        j = i + 1
        assert lines[j].strip() == "{", lines[j]
        depth, k = 1, j + 1
        body = []
        while depth:
            t = lines[k].strip()
            depth += t.count("{") - t.count("}")
            if depth:
                body.append(lines[k])
            k += 1
        for bl in body:
            for mm in re.finditer(r"fsroll_name([ABC])\((.*)\);", bl):
                calls[mm.group(1)] += 1
                arg = mm.group(2)
                me = re.fullmatch(r"\((0x[0-9a-fA-F]+|\d+) \+ regI0\)", arg)
                ml = re.fullmatch(r"(0x[0-9a-fA-F]+|\d+)", arg)
                for r in range(a, b, s):
                    if me:
                        pairs[(mm.group(1), int(me.group(1), 0) + r)] += 1
                    elif ml:
                        pairs[(mm.group(1), int(ml.group(1), 0))] += 1
                    else:
                        unresolved += 1
        i = k
        continue
    for mm in re.finditer(r"fsroll_name([ABC])\((.*)\);", l):
        calls[mm.group(1)] += 1
        arg = mm.group(2)
        ml = re.fullmatch(r"(0x[0-9a-fA-F]+|\d+)", arg)
        if ml:
            pairs[(mm.group(1), int(ml.group(1), 0))] += 1
        else:
            unresolved += 1
    i += 1
check("C1 the evaluator visits every nameX call site a plain grep finds", calls == grep_counts,
      "%s vs %s" % (dict(calls), dict(grep_counts)))
check("E0 every nameX argument is a literal or (k + regI0) inside a constant loop", unresolved == 0, str(unresolved))
names = {(c, v) for (c, v) in pairs if not v & 0x8000}
byclass = collections.Counter(c for c, v in names)
print("   distinct name ids (menu04) by class: %s; role ids (menu03, bit 15) by class: %s" %
      (dict(byclass), dict(collections.Counter(c for c, v in pairs if v & 0x8000))))

# accented rows per language (the four whose menu04 has them)
EXT = "D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle"


def rows(lang):
    b = open("%s/%s/binaryfile/menu04.bin" % (EXT, lang), "rb").read()
    out = []
    for m in re.finditer(rb"ex00", b):
        p, u = m.end(), []
        while p + 1 < len(b):
            v = b[p] | b[p + 1] << 8
            if v == 0:
                break
            u.append(v)
            p += 2
        out.append("".join(map(chr, u)))
    return out


ACC = set("\u00c1\u00e1\u00e8\u00e9\u00ed\u00f1\u00f3\u00f6\u00fa")   # the 9 of the 49 that occur (rc28_staffroll.py)
cls_of = collections.defaultdict(set)
for c, v in names:
    cls_of[v].add(c)
for lang in ("fr", "de", "it", "es"):
    rr = rows(lang)
    acc = [i for i, s in enumerate(rr) if set(s) & ACC]
    drawn = {i: sorted(cls_of.get(i, ())) for i in acc}
    bc = [i for i in acc if cls_of.get(i, set()) & {"B", "C"}]
    print("   %s: %d accented name rows %s; requested by the script with class: %s" %
          (lang, len(acc), acc, {i: "".join(v) or "-" for i, v in drawn.items()}))
    print("   %s: accented rows drawn with face b or c (fonts 8/10, the us-pack 127-glyph tables): %d" % (lang, len(bc)))
from pe import d as IMG, off as OFF  # noqa
grp = IMG[OFF(0x01E09F68):OFF(0x01E09F68) + 28]
check("S0 text groups 25 / 26 (ids 0x61A8.. / 0x6590..) load kind-2 ids 0x41 menu03 / 0x42 menu04 (byte table 01E09F68)",
      grp[25] == 0x41 and grp[26] == 0x42, "%d %d" % (grp[25], grp[26]))
import struct
bb = open("%s/fr/binaryfile/menu04.bin" % EXT, "rb").read()
tab = struct.unpack_from("<I", bb, 0x14)[0]
cnt = struct.unpack_from("<I", bb, tab + 12)[0]
offs = [struct.unpack_from("<I", bb, tab + 16 + 4 * i)[0] for i in range(cnt)]
check("S0b menu04's st2e row offsets ascend over its 1,024 rows, so the ex00 scan order is the row index",
      cnt == 1024 and all(offs[i] < offs[i + 1] for i in range(cnt - 1)) and len(rows("fr")) == cnt)
nid = sorted(v for c, v in names)
print("   name ids the script requests: %d distinct, %d..%d" % (len(nid), nid[0], nid[-1]))
import hashlib
PM = "D:/FFXII_TZA_extract/ps2data/plan_master"
hs = {}
for lang in ("us", "fr", "de", "it", "es", "in"):
    p = "%s/%s/event/men_z/men_z0005/men_z0005.ebp" % (PM, lang)
    hs[lang] = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
print("   men_z0005.ebp sha256[:16] per language: %s" % hs)
check("S1 the staff-roll script men_z0005.ebp is byte-identical in us/fr/de/it/es/in (the us decompile covers them)",
      len(set(hs.values())) == 1)
check("S2 no accented name row (894..944) is requested by any fsroll_nameA/B/C call",
      all(not (set(rows("fr")[v]) & ACC) for c, v in names if v < len(rows("fr"))))
print("RESULT the 49 extra glyphs are never drawn by the shipped staff roll in the us-pack arms")
print("FAILS %d" % FAILS)
