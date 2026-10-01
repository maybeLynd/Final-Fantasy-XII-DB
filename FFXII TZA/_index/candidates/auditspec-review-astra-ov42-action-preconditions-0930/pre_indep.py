"""pre_indep.py - SWE2-AUDIT-SPEC independent re-derivation for ASTRA ov42-special-action-preconditions (2026-09-30).

Not the packet's capture/checker. Image via ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha asserted).
Tables read straight from the Steam INSTALL archive with agent_flow/tools/vbfextract.py (read-only), and compared
to the D:/FFXII_TZA_extract copies and the packet's retained tables.

  A  the 11 code witnesses the checker pins, decoded here from image bytes
  B  every writer/reader of the action-table pointer cell 02EBF138 (rip + image-base-relative + data refs)
  C  callers of 0030CE10 / 00306BD0 / 00309230 / 0032FC30 (E8/E9 + jcc + abs64/rva32)
  D  the row-0x113 identity arm: the 13-entry stack table values and their ns8 narrowing
  E  per-pack predicate over all 543 rows, both radix readings of "row113", and the sentinel/bit30 partition
  F  controls: a sensitivity control on the predicate (wrong narrowing +0 instead of +1; wrong width byte)
"""
import hashlib, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
sys.path.insert(0, os.path.join(ROOT, "agent_flow", "tools"))
import vbfextract as V  # noqa: E402

PKG = os.path.join(ROOT, "Database", "FFXII TZA", "_experiments", "evidence", "ov42-special-action-preconditions")
INSTALL_VBF = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf"
EXTRACT = r"D:\FFXII_TZA_extract\ps2data\image\ff12\test_battle"


def p(*a):
    print(" ".join(str(x) for x in a))


def ins_at(va):
    return T.dis(va, va + 16, 1)[0]


p("image sha256", hashlib.sha256(T.raw).hexdigest())
# ---------------- A
p("== A code witnesses (own decode)")
W = [0x30CE93, 0x30CE9A, 0x30CF0D, 0x306C4D, 0x306C52, 0x306C56, 0x3092C5, 0x3092C3, 0x3092B4, 0x30CEC2, 0x30CEEB,
     0x30CEF2, 0x30CEF8, 0x30CEFB, 0x30CEFE, 0x3092C0, 0x3092CB, 0x3092D2, 0x3092D6, 0x3092DB]
for va in W:
    i = ins_at(va)
    p("  %08X %-8s %-40s %s" % (i.address, i.mnemonic, i.op_str, i.bytes.hex()))

# ---------------- B
p("== B action-table pointer cell 02EBF138..02EBF140")
for h in T.rip_refs(0x2EBF138, 0x2EBF140):
    p("  rip  %08X %-6s %s (w%d)" % h)
for h in T.imagebase_refs(0x2EBF138, 0x2EBF140):
    p("  ib   %08X %-6s %s (w%d)" % h)
p("  data", T.data_refs(0x2EBF138))
p("  cell in file bytes?", T.off(0x2EBF138) is not None)

# ---------------- C
p("== C callers")
for tgt in (0x30CE10, 0x306BD0, 0x309230, 0x32FC30):
    p("  %08X rel32:" % tgt, T.rel32_callers(tgt), "jcc:", T.jcc_callers(tgt), "data:", T.data_refs(tgt))

# ---------------- D
p("== D row-0x113 identity arm stack table (rsp+0x20..+0x50)")
tab = list(struct.unpack("<4I", T.rd(0xD103B0, 16))) + list(struct.unpack("<4I", T.rd(0xD103C0, 16))) + \
    list(struct.unpack("<4I", T.rd(0xD103D0, 16))) + [0x4E]
p("  layout: +0x20<-D103B0, +0x30<-D103C0, +0x40<-D103D0, +0x50<-imm 0x4e (see 0030926E/0030927C/00309282/00309266)")
p("  13 entries (index = type_byte - 0x1B):", tab)
p("  ns8 WORD (4v+1)&0xFFFF signed:", [((4 * v + 1) & 0xFFFF) - (0x10000 if (4 * v + 1) & 0x8000 else 0) for v in tab])
p("  any negative:", any((4 * v + 1) & 0x8000 for v in tab))

# ---------------- E
p("== E tables")
with open(INSTALL_VBF, "rb") as f:
    names, blocks = V.load_index(f)
    paths = sorted(q for q in names if "/test_battle/" in q and q.endswith("/binaryfile/battle_pack.bin"))
    allpacks = sorted(q for q in names if q.endswith("battle_pack.bin"))
    p("  install archive: battle_pack.bin entries total", len(allpacks), "under /test_battle/:", len(paths))
    for q in allpacks:
        if q not in paths:
            p("    other:", q)
    first = None
    for q in paths:
        lang = q.split("/test_battle/")[1].split("/")[0]
        inst = V.read_entry(f, names, blocks, q)
        ext = open(os.path.join(EXTRACT, lang, "binaryfile", "battle_pack.bin"), "rb").read()
        t = struct.unpack_from("<I", inst, 0x3C)[0]
        magic = inst[t:t + 4]
        count, stride, roff = struct.unpack_from("<III", inst, t + 4)
        table = inst[t:t + roff + count * stride]
        ret = open(os.path.join(PKG, "action-selectors-01", "tables", "action_data_%s.st2e" % lang), "rb").read()
        rows = [inst[t + roff + i * stride:t + roff + (i + 1) * stride] for i in range(count)]
        words = [struct.unpack_from("<H", r, 0x24)[0] for r in rows]
        flags = [struct.unpack_from("<I", r, 0x0C)[0] for r in rows]
        ffff = [i for i, w in enumerate(words) if w == 0xFFFF]
        neg_ns = [i for i, w in enumerate(words) if w != 0xFFFF and (4 * w + 1) & 0x8000]
        b30 = [i for i in ffff if flags[i] & 0x40000000]
        p("  %s: install==extract %s install-table==retained %s pack sha %s magic %s count %d stride %d roff %d"
          % (lang, inst == ext, table == ret, hashlib.sha256(inst).hexdigest()[:16], magic, count, stride, roff))
        p("     FFFF rows %d; non-FFFF with negative ns8 %d; max non-FFFF word %d; FFFF+bit30 rows %s"
          % (len(ffff), len(neg_ns), max(w for w in words if w != 0xFFFF), b30))
        if first is None:
            first = (words, flags, ffff, b30)
            p("     flags of 511..534:", sorted(set("%08X" % flags[i] for i in range(511, 535))))
            p("     row 0x113 (dec 275): word %04X flags %08X ; row dec 113 (0x71): word %04X flags %08X"
              % (words[0x113], flags[0x113], words[113], flags[113]))
            p("     FFFF rows in 0xD0..0xF1:", [i for i in ffff if 0xD0 <= i <= 0xF1],
              "FFFF+bit30 rows in 0xD0..0xF1:", [i for i in b30 if 0xD0 <= i <= 0xF1])
            p("     bit30 rows total (any word):", sum(1 for x in flags if x & 0x40000000))
            # ---------------- F sensitivity
            p("== F predicate sensitivity (same rows)")
            p("   ns8 +1 (packet)       non-FFFF negatives:", len(neg_ns))
            p("   wrong: 4v (+0)        non-FFFF negatives:", sum(1 for w in words if w != 0xFFFF and (4 * w) & 0x8000))
            p("   wrong: 3v+1 (kind 5)  non-FFFF negatives:", sum(1 for w in words if w != 0xFFFF and (3 * w + 1) & 0x8000))
            p("   wrong: word at +0x26  non-FFFF negatives:",
              sum(1 for r in rows for w in [struct.unpack_from("<H", r, 0x26)[0]] if w != 0xFFFF and (4 * w + 1) & 0x8000))
            p("   non-FFFF words >= 0x2000 (distinct):", sorted(set(w for w in words if w != 0xFFFF and w >= 0x2000)),
              "-> their (w mod 0x4000):", sorted(set(w % 0x4000 for w in words if w != 0xFFFF and w >= 0x2000)))
            p("   non-FFFF words with bit15 set:", sorted(set(w for w in words if w != 0xFFFF and w & 0x8000)))
