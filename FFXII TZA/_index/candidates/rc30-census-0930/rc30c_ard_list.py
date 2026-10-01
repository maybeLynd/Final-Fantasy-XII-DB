"""RC-30 residue census, supporting: the .ard lookup list behind the 003DC5B0 / 003DC8D0 leaf (SWE2-DATA
2026-09-30), static.

rc30c_kind_slice.py leaves the 003DC5B0 / 003DC8D0 sites at {0x1E}: their kind comes from 003DCA30's first
out-parameter, which that resolver writes as the constant 0x1E at 003DCA49 before it ever consults a list.
This script documents what the lists CAN influence - the id, not the kind - and censuses the one authored
list that ships.

The chain (each link pinned in the disassembly record):
  02B57F70 is a 16-slot request registry (stride 0x14). 003DCD00 installs entries keyed
      (dword+0xC = 002E96B0(obj), word+0x10 = arg id, byte+0x12 = arg sub) through 003DC380
      (the field writes at 003DC3CF/003DC3D6/003DC3DB).
  003DC5B0 (state 1) and 003DC8D0 call 003DCA30(keyA, keyB, keyC, out1, out2): out1 <- 0x1E always;
      out2 <- word[entry+8] of the matched list entry, or -1 on a miss. Both then call
      0032E400(kind=out1, id=out2) / 0032E620(ecx=out1, edx=out2). The kind is 0x1E regardless of the list.
  Three list heads: 02B58188 (A), 02B58178 (B), 02B58180 (C). Head A's setter 003DC330 has no code
      caller; head C's setter 003DCF10 is only invoked with ecx = 0; head B is installed by 003EA710,
      the AREA bind callback registered at 003EA947, as ard_blob + dword[ard + 0x2C].
  The request gate in 003DCD00 also budgets: 003DC8D0 returns 0032E400's size and 003DCD00 admits an
      entry only when (size + 0x7FFF) >> 15 plus the table's other live units stays <= 4 (32 KB units).

So the .ard dword[+0x2C] list is the only authored degree of freedom on this path:
  {u32 count @off; entries {u32 keyA, u16 keyC, u16 keyB, u16 mappedId, u16 pad[3]} stride 0x10}
  keyA matches the site's 002E96B0-derived object key (shipped values 0x6Dxxxx / 0x6Exxxx / 0x73xxxx),
  keyB the original id arg, keyC the sub arg (head A omits keyC). mappedId replaces the id.

RC-30's question - can a computed site produce (kind=7, id in 0xE2..0xE4): this leaf's kind is constant
0x1E, so no. The census below pins the authored id space (and counts mapped ids in 0xE2..0xE4 as
documentation: they would still go out under kind 0x1E).

Claims:
  C1  every .ard carries the 'FF12AR03' magic and dword[+0x2C] is a blob offset or 0
  C2  every non-zero list: count*0x10 + 0x10 fits the file; every entry's pad words are 0 (layout control)
  C3  asp_a.ard's list exists with count 0 (positive parse control)
  C4  the mapped-id census ran over all shipped entries
"""
import sys, os, io, struct, zlib, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
from census_format_magics import load_index

BLOCK = 0x10000
FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


f = io.open(os.environ.get("FF12_VBF", r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"), "rb")
names, blocks = load_index(f)


def read_all(p):
    sb, size, off = names[p]
    n = (size + BLOCK - 1) // BLOCK
    out = b""
    f.seek(off)
    for i in range(n):
        cs = blocks[sb + i] or BLOCK
        exp = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        c = f.read(cs)
        if cs != exp:
            c = zlib.decompress(c)
        out += c
    return out


ards = sorted(p for p in names if p.lower().endswith(".ard"))
# the archive ships 332 paths = 166 distinct .ard resources, each byte-identical under plan_master/in/ and
# plan_master/ch/; census counts are over archive copies (each list is counted twice)
magic_ok = True
list_off_ok = True
bounds_ok = True
pad_ok = True
mapped_ids = collections.Counter()
e2e4 = collections.Counter()
keys_a = collections.Counter()
lists_seen = 0
asp_a_zero = None
for p in ards:
    d = read_all(p)
    if d[:8] != b"FF12AR03":
        magic_ok = False
        continue
    off = struct.unpack_from("<I", d, 0x2C)[0]
    if off >= len(d) and off != 0:
        list_off_ok = False
        continue
    if not off:
        continue
    n = struct.unpack_from("<I", d, off)[0]
    if p.endswith("asp_a.ard"):
        asp_a_zero = (n == 0)
    if off + 0x10 + n * 0x10 > len(d):
        bounds_ok = False
        continue
    lists_seen += 1
    for i in range(n):
        ka, kc, kb, mid, x1, x2, x3 = struct.unpack_from("<IHHHHHH", d, off + 0x10 + i * 0x10)
        if (x1, x2, x3) != (0, 0, 0):
            pad_ok = False
        mapped_ids[mid] += 1
        keys_a[ka] += 1
        if mid in (0xE2, 0xE3, 0xE4):
            e2e4[mid] += 1

check("C1 magic+offset", magic_ok and list_off_ok, f"{len(ards)} .ard parsed")
check("C2 list bounds+pads", bounds_ok and pad_ok, f"{lists_seen} non-empty lists")
check("C3 asp_a count 0", asp_a_zero is True)
check("C4 mapped-id census ran", sum(mapped_ids.values()) > 0,
      f"{sum(mapped_ids.values())} entries, min {min(mapped_ids)} max {max(mapped_ids)}, "
      f"ids in 0xE2..0xE4: {dict(e2e4)} (kind is constant 0x1E regardless)")
import hashlib
bybase = collections.defaultdict(set)
for p in ards:
    bybase[p.split("/")[-1]].add(hashlib.md5(read_all(p)).digest())
dup = sum(1 for v in bybase.values() if len(v) > 1)
check("C5 332 archive paths = 166 distinct resources in identical in/ch copies",
      len(bybase) == 166 and len(ards) == 332 and dup == 0, f"{len(bybase)} basenames, {dup} differing")
print("mapped-id range:", min(mapped_ids), "..", max(mapped_ids), "distinct:", len(mapped_ids))
print("keyA range:", min(keys_a), "..", max(keys_a), "distinct:", len(keys_a))
print("FAILS", FAILS)
