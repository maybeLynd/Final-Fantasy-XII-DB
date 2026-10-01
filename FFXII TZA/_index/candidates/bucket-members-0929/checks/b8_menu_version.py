"""B8 menu_version.bin (kind 7 idx 0x90): layout on every copy; requester/reader absence evidence from the sweeps
(callpairs_kind7.txt, nearcall_imm_run.txt, idtable_scan_kind7.txt) and a literal scan for the version bytes."""
import struct
from common import *
header()
check("kind 7 idx 0x90 path", (kind_path(7, 0x90) or "").endswith(r"Bin_Menu\menu_version.bin"), kind_path(7, 0x90))
check("kind 7 idx 0x8F and 0x91 are empty (no family loop runs across 0x90)", kind_path(7, 0x8F) is None and kind_path(7, 0x91) is None)
files = copies("ps2data/image/ff12/myoshiok/*/bin_menu/menu_version.bin")
check("2 copies (ch, in)", len(files) == 2)
blobs = {open(f, "rb").read() for f in files}
check("identical, 16 bytes = ASCII 'MENUVER' + '200509150' (no terminator)", blobs == {b"MENUVER200509150"})
text = d[0x600:0x7A0E00]
for lit in (b"MENUVER", b"MENU", b"UVER", b"2005", b"0915", b"9150"):
    check(f"literal {lit!r} absent from .text (no immediate compare)", text.find(lit) < 0)
for iv in (200509150, 20050915, 2005091500):
    check(f"integer {iv} absent as a dword in .text", text.find(struct.pack("<I", iv)) < 0)
check("'MENUVER' / '200509' absent from the whole image", d.find(b"MENUVER") < 0 and d.find(b"200509") < 0)
cp = open("callpairs_kind7.txt").read()
check("callpairs: no (7,0x90) constant pair at any call; controls pass", "next=0x90" not in cp and "FAILS 0" in cp)
ni = open("nearcall_imm_run.txt").read()
idhits = [l for l in ni.splitlines() if "0x90" in l.split("<-")[-1] and "rsp" not in l]
check("nearcall_imm: no request call preceded by an id computation with 0x90", not idhits, str(idhits))
it = open("idtable_scan_kind7.txt").read()
check("idtable: no {u32 0x90, u32, ptr->name} menu-resource record other than unrelated resource-name tables; control passes",
      "CONTROL 0xC1 @ 00D237E0: PASS" in it)
print("  idtable 0x90 line:", [l for l in it.splitlines() if l.startswith("0x90")])
finish()
