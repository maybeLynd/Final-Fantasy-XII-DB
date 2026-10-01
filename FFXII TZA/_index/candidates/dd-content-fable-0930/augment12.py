"""augment12.py - which effect id the defeat path's LP->gil test reads, by its shipped text.

00312409 `test byte [rdi+0x69], 0x10` / 0031240F `test byte [rdi+0x79], 0x10`: byte 1, bit 4 of the two 16-byte effect
layers at +0x68 / +0x78 = layer bit 12 = effect (augment) id 12. This prints the augment table row 12 (battle_pack.bin
directory +0xEC, 8-byte rows: +0 descriptionId, +2 nameWord, +4 parameter, +6) and the listhelp_ability.bin string its
descriptionId names (13000 + n -> string id 130000 + n).
Control: rows 27 / 28 must read "Doubles EXP earned" / "Doubles license points earned", the names the award page
resolved for N-2 (29's text starts with a glyph the dashboard decoder does not map, so it is printed raw).
Decoders: Database/Tools/dashboard/ff12_content.py (st2e_rows, st2e_strings, dec)."""
import sys, glob, hashlib
import os
# installed at Database/FFXII TZA/_index/candidates/dd-content-fable-0930/; the decoders are Database/Tools/dashboard
_HERE = os.path.dirname(os.path.abspath(__file__))
for _d in (os.path.join(_HERE, "..", "..", "..", "..", "Tools", "dashboard"),
           r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\dashboard"):
    if os.path.isfile(os.path.join(_d, "ff12_content.py")):
        sys.path.insert(0, _d)
        break
from ff12_content import st2e_strings, st2e_rows, dec, u16, u32

root = r"D:\FFXII_TZA_extract\ps2data\image\ff12\test_battle\us\binaryfile"
bp = open(root + r"\battle_pack.bin", "rb").read()
lh = open(root + r"\listhelp_ability.bin", "rb").read()
print("battle_pack.bin sha256 %s; listhelp_ability.bin sha256 %s" % (hashlib.sha256(bp).hexdigest(), hashlib.sha256(lh).hexdigest()))
aug = st2e_rows(bp, 0xEC)
ids = [u32(lh, 0x20 + 4 * i) for i in range(u32(lh, 4))]
s = st2e_strings(lh)
print("augment rows: %d; listhelp records: %d" % (len(aug), len(s)))
for n in (12, 27, 28, 29):
    r = aug[n]
    desc = u16(r, 0)
    sid = desc + 117000 if desc else None        # 13000 + n  ->  130000 + n
    k = ids.index(sid) if sid in ids else None
    txt = dec(s[k]) if k is not None and k < len(s) else "-"
    print("row %2d: +0 descriptionId %d  +2 nameWord 0x%04X  +4 parameter %d  +6 0x%X  -> string %s: %r   raw %s"
          % (n, desc, u16(r, 2), u16(r, 4), u16(r, 6), sid, txt, s[k][:24].hex() if k is not None else "-"))
