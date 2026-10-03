"""check.py - re-decode, from the shipping image, every site each new name rests on (FABLE, 2026-10-03), with
sensitivity controls: a wrong expected instruction, and a site moved by one instruction, must each fail.
Owner-block base registers: r11 in 00512F30, rcx / r9 in 00512CD0, rcx in 00512EE0 (slot accesses use other
registers and are not counted). Prints PASS/FAIL lines and FAILS n last."""
import os, sys
import pefile, capstone

EXE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "work", "exe",
                   "FFXII_TZA.exe")
pe = pefile.PE(os.path.normpath(EXE), fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def ins(fn, size):
    return {i.address: "%s %s" % (i.mnemonic, i.op_str) for i in md.disasm(pe.get_data(fn - BASE, size), fn)}


F = {0x00512F30: ins(0x00512F30, 532), 0x00512CD0: ins(0x00512CD0, 162), 0x00512EE0: ins(0x00512EE0, 0x40)}
SITES = [  # (name, fn, offset, exact instruction text)
    ("relationListHead", 0x00512F30, 0x23, "movzx eax, byte ptr [r11 + 0xc]"),
    ("relationListHead", 0x00512F30, 0x160, "cmp byte ptr [r11 + 0xc], 0xff"),
    ("relationListHead", 0x00512F30, 0x16B, "mov byte ptr [r11 + 0xc], cl"),
    ("relationListHead", 0x00512CD0, 0x2D, "mov byte ptr [rcx + 0xc], al"),
    ("relationListTail", 0x00512F30, 0x158, "movzx ecx, byte ptr [r11 + 0xd]"),
    ("relationListTail", 0x00512F30, 0x16F, "movzx ecx, byte ptr [r11 + 0xd]"),
    ("relationListTail", 0x00512F30, 0x191, "mov byte ptr [r11 + 0xd], cl"),
    ("relationListTail", 0x00512CD0, 0x56, "mov byte ptr [rcx + 0xd], al"),
    ("relationListCount", 0x00512F30, 0x10D, "inc byte ptr [r11 + 0xe]"),
    ("relationListCount", 0x00512CD0, 0x97, "dec byte ptr [r9 + 0xe]"),
    ("relationListCount", 0x00512EE0, 0xA, "mov byte ptr [rcx + 0xe], 0"),
    ("relationListHead+Tail reset", 0x00512EE0, 0x4, "mov word ptr [rcx + 0xc], 0xffff"),
    ("inlineRelationKindNibble", 0x00512F30, 0x1B9, "and byte ptr [r11 + 0xf], 0xf3"),
    ("inlineRelationKindNibble", 0x00512F30, 0x1BE, "or byte ptr [r11 + 0xf], 3"),
    ("inlineRelationKindNibble", 0x00512F30, 0x1E0, "and byte ptr [r11 + 0xf], 0xf0"),
    ("inlineRelationKindNibble", 0x00512F30, 0x200, "and byte ptr [r11 + 0xf], 0xf1"),
    ("inlineRelationKindNibble", 0x00512F30, 0x205, "or byte ptr [r11 + 0xf], 1"),
    ("inlineRelationKindNibble", 0x00512EE0, 0x0, "and byte ptr [rcx + 0xf], 0xf0"),
]
fails = 0


def site_ok(fn, off, txt):
    return F[fn].get(fn + off) == txt


for name, fn, off, txt in SITES:
    ok = site_ok(fn, off, txt)
    print("%s  %-28s %08X+0x%X  %s" % ("PASS" if ok else "FAIL", name, fn, off, txt))
    fails += not ok

# no owner-block write to the HIGH nibble of +0xF: every r11-based +0xF write in 00512F30 is an and/or whose
# immediate keeps bits 4-7 (and 0xFx) or sets only bits 0-3 (or 0x0x)
hi = [(a, t) for a, t in F[0x00512F30].items() if "[r11 + 0xf]" in t and not (
      (t.startswith("and ") and t.split(", ")[-1].lower().startswith("0xf")) or
      (t.startswith("or ") and int(t.split(", ")[-1], 16) < 0x10))]
print("%s  high nibble of +0xF untouched by 00512F30's owner-block writes (%d offenders)" % ("PASS" if not hi else "FAIL", len(hi)))
fails += bool(hi)

# controls: each must FAIL to be a control
c1 = site_ok(0x00512F30, 0x10D, "dec byte ptr [r11 + 0xe]")          # wrong instruction
c2 = site_ok(0x00512F30, 0x23 + 4, "movzx eax, byte ptr [r11 + 0xc]")  # site moved
c3 = site_ok(0x00512CD0, 0x97, "dec byte ptr [r11 + 0xe]")           # wrong base register
for nm, v in (("wrong instruction", c1), ("moved site", c2), ("wrong base register", c3)):
    print("%s  control %s is rejected" % ("PASS" if not v else "FAIL", nm))
    fails += bool(v)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
