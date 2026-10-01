"""@FRP object container (.ca / .cm): the name compare and the padding census (SWE2-DATA 2026-09-30), static + data.

  N1 00408F30 ('NameEquals') compares eight dwords, +0x00..+0x1C of both pointers (32 bytes), returns 0 when all
     match and 1 at the first differing dword.
  N2 FRP_FindEntry 00408FA0 calls it with rcx = blob + 0x10 in both variant loops and takes a NON-zero return as the
     hit (test rax, rax / jne to the hit exit 0040907D), so a supplied name selects files whose 32-byte name field
     differs from it; a NULL name is a hit without the compare.
  N3 every entry to FRP_FindEntry is the thunk 00408F90 (xor r9d = startIndex 0, jmp): raw E8/E9/0F8x and qword
     census over .text finds no other reference; the thunk's four callers all pass r8 = 0 (no name) and the tag
     '@FRM' (0x4D524640). So the name path is never taken in this image.
  A1 archive census over all .ca / .cm under D:/FFXII_TZA_extract: per (extension, variant) group, whether
     contentLength (+0x08) equals the file size, whether every byte past it is zero, and the file-size alignment
     (largest power of two dividing the size, capped at 64 KiB).
  A2 bytes +0x20..+0x2F (the tail of the 32 bytes N1 compares) are zero in every file.
Control C1: the .ca variant-0 group has contentLength == size in every file (the page's own §4 row), so A1 reads the
same field the page tabulates.
"""
import collections, glob, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, dis, owner  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


ne = {x.address: x for x in dis(0x00408F30)}
cmps = [x for x in ne.values() if x.mnemonic == "cmp"]
check("N1 00408F30 compares 8 dwords (+0..+0x1C), 0 on full match, 1 on first mismatch",
      [x.op_str for x in sorted(cmps, key=lambda x: x.address)] ==
      ["dword ptr [rcx], eax"] + ["dword ptr [rcx + %s], eax" % (("%d" % k) if k < 10 else ("0x%x" % k)) for k in range(4, 0x20, 4)]
      and ne[0x00408F6E].op_str == "eax, eax" and ne[0x00408F71].op_str == "eax, 1")
fe = {x.address: x for x in dis(0x00408FA0)}
check("N2 FRP_FindEntry: rcx = blob+0x10; non-zero return -> hit exit 0040907D (both loops)",
      fe[0x00408FFF].op_str == "rcx, [rdi + 0x10]" and fe[0x0040900B].op_str == "rax, rax"
      and fe[0x0040900E].op_str == "0x40907d" and fe[0x0040905F].op_str == "rcx, [rdi + 0x10]"
      and fe[0x0040906E].op_str == "0x40907d" and fe[0x0040907D].op_str == "eax, ebx")
va, vs, fo = 4096, 7996981, 1536
base = 0x120000 + va
T = {0x00408FA0: [], 0x00408F90: []}
for i in range(fo, fo + vs - 6):
    if d[i] in (0xE8, 0xE9):
        t = base + (i - fo) + 5 + struct.unpack_from("<i", d, i + 1)[0]
        if t in T:
            T[t].append(base + (i - fo))
    if d[i] == 0x0F and 0x80 <= d[i + 1] <= 0x8F:
        t = base + (i - fo) + 6 + struct.unpack_from("<i", d, i + 2)[0]
        if t in T:
            T[t].append(base + (i - fo))
qrefs = sum(d.count(struct.pack("<Q", t)) for t in T)
args = []
for h in T[0x00408F90]:
    f = dis(owner(h))
    k = [n for n, x in enumerate(f) if x.address == h][0]
    pre = {x.op_str.split(",")[0]: x for x in f[max(0, k - 10):k]}
    args.append((pre.get("r8d") and pre["r8d"].mnemonic + " " + pre["r8d"].op_str,
                 pre.get("edx") and pre["edx"].op_str))
print("   refs: FindEntry %s ; thunk %s ; qword %d ; thunk-caller args %s"
      % (["%08X" % x for x in T[0x00408FA0]], ["%08X" % x for x in T[0x00408F90]], qrefs, args))
th = dis(0x00408F90)
check("N3 only the zero-start thunk reaches FindEntry; its 4 callers pass no name and the tag @FRM",
      T[0x00408FA0] == [0x00408F93] and len(T[0x00408F90]) == 4 and qrefs == 0
      and th[0].op_str == "r9d, r9d"
      and all(a == ("xor r8d, r8d", "edx, 0x4d524640") for a in args))

groups = collections.defaultdict(lambda: collections.Counter())
tail0 = bad_tail = 0
files = sorted(glob.glob("D:/FFXII_TZA_extract/**/*.ca", recursive=True)
               + glob.glob("D:/FFXII_TZA_extract/**/*.cm", recursive=True))
for f in files:
    b = open(f, "rb").read()
    if b[:4] != b"@FRP":
        continue
    var, clen = struct.unpack_from("<II", b, 4)
    g = groups[(os.path.splitext(f)[1], var)]
    g["files"] += 1
    g["equal"] += clen == len(b)
    g["zero_tail"] += clen < len(b) and not any(b[clen:])
    al = 1
    while al < 65536 and len(b) % (al * 2) == 0:
        al *= 2
    g["align_%d" % al] += 1
    tail0 += not any(b[0x20:0x30])
    bad_tail += any(b[0x20:0x30])
for k in sorted(groups):
    g = groups[k]
    print("   %s variant %d: files %d, size==contentLength %d, zero tail %d, alignment %s"
          % (k[0], k[1], g["files"], g["equal"], g["zero_tail"],
             {a[6:]: n for a, n in sorted(g.items(), key=lambda kv: -kv[1]) if a.startswith("align_")}))
ca0, ca1, cm0 = groups[(".ca", 0)], groups[(".ca", 1)], groups[(".cm", 0)]
check("C1 control: .ca variant 0 has contentLength == size in all its files", ca0["files"] == ca0["equal"] == 1969)
check("A1 every padded file (.ca variant 1, .cm variant 0) has an all-zero tail past contentLength",
      ca1["zero_tail"] == ca1["files"] == 1195 and cm0["zero_tail"] == cm0["files"] == 1066)
check("A2 bytes +0x20..+0x2F are zero in every file", bad_tail == 0 and tail0 == len(files) == 4230)
print("RESULT the name compare covers 32 bytes and hits on a DIFFERING name, but no caller passes a name; padding "
      "alignment per group is printed above")
print("FAILS %d" % FAILS)
