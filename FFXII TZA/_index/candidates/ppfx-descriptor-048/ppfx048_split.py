"""ppfx048_split.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.

PpfxInitDescriptor (0x118, embedded at CPostEffect +0x210) +0x48 was 'mixed048 u8[8]', width NOT resolved. The read
side settles its first four bytes:
  R  CPostEffect's own body reads it as an unsigned dword: 007006FC `cmp dword ptr [rsi + 0x258], r14d` / 00700703 `jbe`
     (0x258 = 0x210 + 0x48), in the committed flow census cpe-flow-accesses.tsv
  W  006CBD20 builds its transient copy at rsp+0x50 and stores dword 0x780 (1920) at 006CBDF3 `mov dword ptr [rsp + 0x98]`
     (0x98 = 0x50 + 0x48); 006CBBC0 zero-initialises the slot with one qword (006CBBE1 `mov qword ptr [rcx + 0x48], rax`)
  C  in the flow census, nothing touches CPostEffect +0x25C..+0x25F except that qword and 16-byte block copies
  S  REGRESSION: the store has +0x48 uint32 (4) and +0x4C DISCOVERED u8[4] (FAILS before the patch)
+0x20 and +0x88 stay 'mixed': they are written (a movss store, dword stores) and block-copied, never read at a width.
Usage: python ppfx048_split.py [--patch]
"""
import csv, hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.abspath(os.path.join(DB, ".."))
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
FIELDS = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/ppfx-descriptor-048/ppfx048_split.py"
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
fl = open(FIELDS, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")

if "--patch" in sys.argv:
    i = next(i for i, l in enumerate(fl) if cells(l)[0] == "PpfxInitDescriptor" and cells(l)[1] == "0x048")
    c = cells(fl[i]); eol = fl[i][len(fl[i].rstrip("\r\n")):]; w = len(c)
    if c[4] != "u8[8]": print("already"); sys.exit(0)
    def row(r): return "\t".join(r + [""] * (w - len(r))) + eol
    fl[i:i + 1] = [
        row(["PpfxInitDescriptor", "0x048", "4", "dword048", "uint32",
             "read as an unsigned dword through CPostEffect's embed (007006FC cmp dword [rsi+0x258] / jbe); 006CBD20 stores "
             "0x780 (1920) into its stack copy (006CBDF3). MEANING NOT CLAIMED unless the contract is cited",
             "TYPE RESOLVED", "PROVEN", "SPLIT 2026-09-28 (OPUS, %s R W C): the read settles the first four bytes; the "
             "006CBBE1 qword is the zero-initialiser. || WAS 0x048 8 mixed048 u8[8]: %s || %s" % (REC, c[5], c[8])]),
        row(["PpfxInitDescriptor", "0x04C", "4", "unobservedSpan04C", "u8[4]",
             "the unread half of the former mixed048: only the 006CBBE1 zero qword and 16-byte copies touch it",
             "DISCOVERED", "UNKNOWN", "SPLIT REMAINDER 2026-09-28 (OPUS, %s)" % REC])]
    open(FIELDS, "wb").write("".join(fl).encode("utf-8")); print("split +0x48"); sys.exit(0)

check("R", at(0x7006FC) == ("cmp", "dword ptr [rsi + 0x258], r14d") and at(0x700703)[0] == "jbe",
      "007006FC reads CPostEffect +0x258 (= +0x210 + 0x48) as a dword, unsigned compare")
check("W", at(0x6CBDF3) == ("mov", "dword ptr [rsp + 0x98], 0x780") and at(0x6CBBE1) == ("mov", "qword ptr [rcx + 0x48], rax"),
      "006CBDF3 dword 1920 into the stack copy (rsp+0x50 + 0x48); 006CBBE1 the zero qword")
R = list(csv.DictReader(open(os.path.join(DB, "_index", "candidates", "type-flow-census", "cpe-flow-accesses.tsv"),
                             encoding="utf-8"), delimiter="\t"))
tail = sorted({(r["field"], r["width"], r["kind"], r["site"]) for r in R if not r["field"].startswith("-") and r["kind"] != "addr"
               and int(r["field"], 16) < 0x260 and int(r["field"], 16) + int(r["width"]) > 0x25C and r["width"] != "16"})
check("C", tail == [("0x258", "8", "w", "006CBBE1")], "non-16-byte accesses reaching CPostEffect +0x25C..+0x25F: %s" % tail)
F = {cells(l)[1]: cells(l) for l in fl if cells(l)[0] == "PpfxInitDescriptor"}
check("S", F.get("0x048", [0] * 5)[2:5] == ["4", "dword048", "uint32"] and F.get("0x04C", [0] * 7)[6] == "DISCOVERED",
      "the store has +0x48 uint32 and +0x4C DISCOVERED (now %s)" % F.get("0x048", [0] * 5)[2:5])
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
