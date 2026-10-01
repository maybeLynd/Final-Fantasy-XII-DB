"""UQ-70: filelistlocalin.bin decoded (OPUS, 2026-09-27). Control..

Layout: u32 sectionOffset[38] (the table is 0x98 bytes, so section 0 starts at 0x98); each section is
{u32 count; u32 stringOffset[count]} with ABSOLUTE file offsets into a pool of NUL-terminated PS2 disc paths that start
with '%' (a root placeholder). Section k lists the file family of the file-size table's kind k.
  F1 38 sections; every offset table fits before the next section; every non-zero string offset lands in the file
  F2 the pool: 24,358 entries; each non-empty entry is a NUL-terminated printable path
  F3 family agreement with the FST page's kinds: section 0 system.cnf, 4 map_ctrl, 5 plan_map *\\global\\*.ebp,
     10 c_all/m_all efx, 11 effect_finish magic efx (512), 12 event efx, 13 gadget, 14 chara, 16 weapon, 19 npc,
     21 area .ard, 26 area .nmb, 27 sound wave, 31 music, 32 se blocks, 33 shout, 34 monster
  F4 the ch and in copies are byte-identical
"""
import struct, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12")
b = (ROOT / "ch/bin/filelistlocalin.bin").read_bytes()
fails = 0


def check(nm, ok, d=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, d)); fails += (not ok)


secs = struct.unpack_from("<38I", b, 0)
ok = secs[0] == 0x98 and all(secs[i] < secs[i + 1] for i in range(37))
tables = []
for k, s in enumerate(secs):
    c = struct.unpack_from("<I", b, s)[0]
    offs = struct.unpack_from("<%dI" % c, b, s + 4) if c else ()
    end = s + 4 + 4 * c
    ok &= (k == 37 or end <= secs[k + 1]) and all(o == 0 or o < len(b) for o in offs)
    tables.append(offs)
check("F1 38 sections, tables fit, offsets in file", ok)


def s_at(o):
    return b[o:b.index(b"\0", o)].decode("latin1")


n = sum(len(t) for t in tables)
paths = [[s_at(o) if o else "" for o in t] for t in tables]
printable = all(all(32 <= ord(ch) < 127 for ch in p) for t in paths for p in t)
check("F2 24,358 entries, all printable", n == 24358 and printable, "(%d)" % n)
fam = {4: "\\map_ctrl\\", 5: "\\global\\", 10: "_all.efx", 11: "\\magic\\", 12: "\\event\\", 13: "\\gadget\\",
       14: "\\chara\\", 16: "\\weapon\\", 19: "\\npc\\", 26: ".nmb", 27: "\\wave\\", 31: "\\music\\",
       32: "\\se\\", 33: "\\shout\\", 34: "\\monster\\"}
agree = {k: all(v.lower() in p.lower() for p in paths[k] if p.startswith("%")) and any(p for p in paths[k]) for k, v in fam.items()}
check("F3 section k holds FST kind k's family", all(agree.values()), str([k for k, v in agree.items() if not v]))
check("F3c section 0 starts with system.cnf (FST kind 0 id 0); section 21 alternates .ard / .fpk (FST: stride 2)",
      paths[0][0].endswith("system.cnf") and all(p.endswith((".ard", ".fpk")) for p in paths[21] if p))
check("F3b section 11 is 512 magic efx (m0000..m0511)", len(paths[11]) == 512 and paths[11][0].endswith("m0000.efx") and paths[11][-1].endswith("m0511.efx"))
check("F4 ch and in copies identical", (ROOT / "in/bin/filelistlocalin.bin").read_bytes() == b)
print("FAILS", fails)
sys.exit(1 if fails else 0)
