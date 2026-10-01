"""layout_key_slots.py: every uisize.json layout key -> the global its value is stored in.
001CA600 reads each key (`lea rdx, key` ... `call 00200B80`) and stores the value through the pointer at
[uiobj + 0x3B00 + slot] (`mov rcx, [rbx + slot]` then `mov [rcx], eax`, rbx = 001B1C00() + 0x3B00).
001AF470 fills those pointers (`lea rax, global; mov [rcx + 0x3B00 + slot], rax`). Joining the two gives key -> global.
The three Variant_ReadFloat keys go through a second object instead (see below).
Run from the repository root; prints key, slot, global, installer (tab-separated)."""
import re, struct, subprocess, sys, os
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 12)[0], struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 8)[0],
         struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 20)[0]) for i in range(ns)]
def off(va):
    r = va - BASE
    for a, vs, ro in secs:
        if a <= r < a + vs: return ro + r - a
def cstr(va):
    o = off(va); return d[o:d.index(b"\0", o)].decode("latin1")
sizes = {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64)
def body(f):
    o = off(f); return list(md.disasm(d[o:o + sizes[f]], f))
def rip(ins):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", ins.op_str)
    return ins.address + ins.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) if m else None
# Corrected 2026-09-27 (FABLE, Claude Opus 5.5). The 2026-09-13 join bound 222 keys; the loader binds 226. Two defects:
# (1) capstone prints a small displacement in decimal - `[rbx + 8]` - which the hex-only pattern skipped, losing
#     mCommandTitleFontHeight; (2) at 001CC572 rbx becomes a SECOND object, 001B5FB0()'s (the singleton at 01F81200),
#     for the three Variant_ReadFloat keys. Their `[rbx + 0x2f8]` overwrote MessageWinMaskBottom's slot +0x2F8, so
#     FontItalicVal was given MessageWinMaskBottom's global and the two other float keys (stored via rax) were lost.
#     The second object's slots are filled by 001B44A0 (tail-jumped from 0017F9E0 with rcx = 001B5FB0()).
# The fourth column names the installer that fills the key's slot: 001AF470 (object 001B1C00() + 0x3B00) or 001B44A0.
def installs(f, base):
    tgt = {}; g = None
    for ins in body(f):
        if ins.mnemonic == "lea" and ins.op_str.startswith("rax, [rip"): g = rip(ins)
        m = re.match(r"qword ptr \[r[bc]x \+ (0x[0-9a-f]+)\], rax$", ins.op_str)
        if ins.mnemonic == "mov" and m and g is not None: tgt[int(m.group(1), 16) - base] = g; g = None
    return tgt
TGT = {0x1AF470: installs(0x1AF470, 0x3B00), 0x1B44A0: installs(0x1B44A0, 0)}
slot = []; key = None; obj = 0x1AF470
for ins in body(0x1CA600):
    if ins.mnemonic == "lea" and ins.op_str.startswith("rdx, [rip"): key = cstr(rip(ins))
    if ins.mnemonic == "call" and ins.op_str == "0x1b5fb0": obj = 0x1B44A0
    m = re.match(r"r[ac]x, qword ptr \[rbx(?: \+ (0x[0-9a-f]+|\d+))?\]$", ins.op_str)
    if ins.mnemonic == "mov" and m and key: slot.append((obj, int(m.group(1) or "0", 0), key)); key = None
for obj, o, k in sorted(slot):
    print("%s\t+0x%X\t%s\t%08X" % (k, o, "%08X" % TGT[obj][o] if o in TGT[obj] else "?", obj))
