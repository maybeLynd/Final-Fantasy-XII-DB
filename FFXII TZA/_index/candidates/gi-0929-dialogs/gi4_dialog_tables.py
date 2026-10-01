#!/usr/bin/env python3
"""gi4_dialog_tables.py - GI-4 (FABLE, 2026-09-29): the 00D23688 title table, the two single-installer widgets and the
confirm window's +0x630 flag word.

Checks, from the shipping EXE and the shipped text of all nine locales:
  A. the twelve 6-byte records {u16 label, u16 help, u8 key, u8 flag} at 00D23688..00D236D0: every reader's access,
     a full displacement sweep and rip sweep of the table range (with the known reads as positive controls), and the
     REGRESSION against the published framing {kind, flag, u16, u16} from 0xC0368C / 0xC036A4: under the reader
     framing all four menu keys name the handbook page whose title is the menu row's own label; under the published
     framing none does;
  B. what the handbook half's key byte does: 002527B0 is a clamped store into [020927C0]+0x30/+0x70/+0x90 (the
     saved cursor banks), and every call made with a table key passes bank 6;
  C. 0056F810 and 00556F90 each have exactly one installer, and 00556F90 is fed the license-board index;
  D. the confirm window 0057C480's +0x630 producers (exactly three callers of 0057C380) and their flag words, the
     bit test sites, the decide-sound read of the list +0xFC byte, and the INFO / SELECTION header rows.
Exit status is 1 when any check fails.
"""
import struct, sys, os, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
FST = r"D:/FFXII MP Mod/FFXII_TestClient1/FileSizeTables/FileSizeTable_US.fst"
TB = r"D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle"
LANGS = ["us", "de", "es", "fr", "it", "in", "kr", "cn", "ch"]
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    secs.append((struct.unpack_from("<I", d, o + 12)[0], struct.unpack_from("<I", d, o + 8)[0], struct.unpack_from("<I", d, o + 20)[0], d[o:o + 8].rstrip(b"\0"), struct.unpack_from("<I", d, o + 16)[0]))
def off(a):
    r = a - BASE
    for va, vs, ro, _, _ in secs:
        if va <= r < va + vs: return ro + (r - va)
def sec_of_file(fo):
    for va, vs, ro, nm, rs in secs:
        if ro <= fo < ro + rs: return nm.decode()
funcs = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(fn): return list(md.disasm(d[off(fn):off(fn) + funcs[fn]], fn))
def ins(a): x = list(md.disasm(d[off(a):off(a) + 16], a))[0]; return f"{x.mnemonic} {x.op_str}"
def rip_target(a):
    x = list(md.disasm(d[off(a):off(a) + 16], a))[0]
    m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
fails = 0
def check(name, ok, detail=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + (" :: " + str(detail) if detail != "" else ""))
    if not ok: fails += 1
tva, tvs, tro = [(va, vs, ro) for va, vs, ro, nm, _ in secs if nm == b".text"][0]
TEXT = d[tro:tro + tvs]
def branch_sites(target):
    out = []
    for m in re.finditer(rb"[\xE8\xE9]", TEXT):
        i = m.start()
        if i + 5 <= len(TEXT) and BASE + tva + i + 5 + struct.unpack_from("<i", TEXT, i + 1)[0] == target: out.append(BASE + tva + i)
    good = []
    for s in out:
        x = list(md.disasm(d[off(s):off(s) + 5], s))
        if x and x[0].size == 5: good.append(s)
    jcc = [BASE + tva + m.start() for m in re.finditer(rb"\x0F[\x80-\x8F]", TEXT)
           if m.start() + 6 <= len(TEXT) and BASE + tva + m.start() + 6 + struct.unpack_from("<i", TEXT, m.start() + 2)[0] == target]
    return good, jcc
def rip_refs(lo, hi):
    """every instruction in listed functions whose rip-relative operand resolves into [lo, hi)"""
    out = []
    for fn in sorted(funcs):
        if not (0x121000 <= fn < 0x8C2000): continue
        try: xs = dis(fn)
        except Exception: continue
        for x in xs:
            m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
            if m:
                t = x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
                if lo <= t < hi: out.append((x.address, t, fn))
    return out
def disp_refs(lo, hi):
    out = []
    for fn in sorted(funcs):
        if not (0x121000 <= fn < 0x8C2000): continue
        try: xs = dis(fn)
        except Exception: continue
        for x in xs:
            for m in re.finditer(r"[+-] (0x[0-9a-f]+)\]", x.op_str):
                v = int(m.group(1), 16)
                if lo <= v < hi and "rip" not in x.op_str: out.append((x.address, f"{x.mnemonic} {x.op_str}"))
    return out
# --- text ---
fst = open(FST, "rb").read()
def st2e_rows(path):
    t = open(path, "rb").read(); tab = struct.unpack_from("<I", t, 0x14)[0]; cnt = struct.unpack_from("<I", t, tab + 12)[0]
    return t, tab, [struct.unpack_from("<I", t, tab + 16 + 4 * i)[0] for i in range(cnt)]
def dec(s):
    o = ""
    for c in s:
        if 0x20 <= c <= 0x39: o += chr(65 + c - 0x20)
        elif 0x3A <= c <= 0x53: o += chr(97 + c - 0x3A)
        elif 0x54 <= c <= 0x5D: o += chr(48 + c - 0x54)
        elif c == 4: o += " "
        elif c == 0xAC: o += "'"
        elif c == 0xA8: o += "."
        elif c == 0xA2: o += "("
        else: o += "{%02X}" % c
    return o
_sizes = {}
def text(tid, lang="us"):
    g, row = divmod(tid, 1000)
    lid = struct.unpack_from("<b", d, off(0x01E09F68 + g))[0]
    size = struct.unpack_from("<i", fst, 4 * (2 * 5000 + lid))[0]
    b = f"{TB}/us/binaryfile"
    if not _sizes:
        for f in os.listdir(b): _sizes.setdefault(os.path.getsize(os.path.join(b, f)), []).append(f)
    f = _sizes[size][0]
    t, tab, offs = st2e_rows(f"{TB}/{lang}/binaryfile/{f}")
    st = tab + 12 + offs[row]
    if t[st:st + 4] == b"ex00":
        return t[st + 4:st + 4 + 128].decode("utf-16le", "replace").split("\x00")[0]
    return dec(t[st:t.index(b"\0", st)])
check("text resolver control: 0x3E8 is 'Yes'", text(0x3E8) == "Yes", text(0x3E8))

print("== A. the 00D23688 table")
recs = [struct.unpack_from("<HHBB", d, off(0xD23688 + 6 * k)) for k in range(12)]
for k, (lab, hlp, key, flg) in enumerate(recs):
    print(f"      rec {k:2d} @ {0xD23688 + 6 * k:08X} label {lab:#06x} '{text(lab)}' help {hlp:#06x} '{text(hlp)}' key {key:#04x} flag {flg}")
check("the next object starts at 00D236D0 (eight 0x80000000 dwords, lea'd at 0056EB88)",
      all(struct.unpack_from("<I", d, off(0xD236D0 + 4 * i))[0] == 0x80000000 for i in range(8)) and rip_target(0x56EB88) == 0xD236D0)
reads = {0x56F694: "movzx edx, word ptr [r12 + rcx*2 + 2]", 0x56F69A: "movzx ecx, word ptr [r12 + rcx*2]",
         0x56F32B: "movzx ecx, word ptr [rax + rcx*2]", 0x574AAD: "movzx ecx, word ptr [rax + rcx*2]",
         0x56F98D: "movzx eax, byte ptr [r8 + rcx*2 + 0xc0368c]", 0x5732AC: "movzx edx, byte ptr [r9 + rcx*2 + 0xc036a4]",
         0x571ECD: "movzx edx, byte ptr [r9 + rcx*2 + 0xc036a4]", 0x56F795: "movzx ecx, byte ptr [r14 + rcx*2 + 4]",
         0x56EDB4: "movzx edi, byte ptr [rax + rcx*2]", 0x5721EB: "movzx edx, byte ptr [rax + rcx*2]"}
for a, s in reads.items(): check(f"reader {a:08X}: {s}", ins(a) == s, ins(a))
leas = {0x56F678: 0xD23688, 0x56F76C: 0xD23688, 0x56FAEF: 0xD23688, 0x56F324: 0xD236A0, 0x574AA6: 0xD236A0, 0x56EDAD: 0xD236A4, 0x5721E4: 0xD236A4}
for a, t in leas.items(): check(f"lea at {a:08X} -> {t:08X}", rip_target(a) == t, f"{rip_target(a):08X}")
rr = rip_refs(0xD23688, 0xD236D0)
check("rip sweep of 00D23688..00D236D0 finds exactly the seven lea sites above (control: 0056F678 among them)",
      sorted(a for a, _, _ in rr) == sorted(leas), [f"{a:08X}->{t:08X}" for a, t, _ in rr])
dr = disp_refs(0xC03688, 0xC036D0)
check("displacement sweep of 0xC03688..0xC036D0 finds exactly 0056F98D, 00571ECD, 005732AC (all +4 byte reads)",
      sorted(a for a, _ in dr) == [0x56F98D, 0x571ECD, 0x5732AC], [f"{a:08X} {s}" for a, s in dr])
# regression: framing agreement
new_ok = sum(1 for k in range(4) if recs[4 + recs[k][2]][0] == recs[k][0])
old_ok = 0
for k in range(4):
    kind = d[off(0xD2368C + 6 * k)]
    old_label = struct.unpack_from("<H", d, off(0xD2368C + 6 * k + 2))[0]
    if kind < 8 and struct.unpack_from("<H", d, off(0xD236A4 + 6 * kind + 2))[0] == old_label: old_ok += 1
check("reader framing: 4 of 4 menu keys name the handbook page titled with the menu row's own label", new_ok == 4, new_ok)
check("REGRESSION: the published framing {kind, flag, u16, u16} at 0xC0368C / 0xC036A4 agrees 0 of 4", old_ok == 0, old_ok)
check("menu option 0 is 'Hunts' with key 6 (the published row paired kind 6 with Bestiary)", text(recs[0][0]) == "Hunts" and recs[0][2] == 6)
check("menu keys 6,5,7,4 = Hunts, Bestiary, Sky Pirate's Den, Traveler's Tips",
      [(text(recs[k][0]), recs[k][2]) for k in range(4)] == [("Hunts", 6), ("Bestiary", 5), ("Sky Pirate's Den", 7), ("Traveler's Tips", 4)])
check("handbook half keys are 0x0B..0x12 and flags 0", sorted(r[2] for r in recs[4:]) == list(range(0x0B, 0x13)) and all(r[3] == 0 for r in recs[4:]))
_, tab0, _ = st2e_rows(f"{TB}/us/binaryfile/penelosdiary.bin")
ph = {}
for lang in LANGS:
    t, tab, offs = st2e_rows(f"{TB}/{lang}/binaryfile/penelosdiary.bin")
    ph[lang] = (len(set(offs[0:4])) == 1, dec(t[tab + 12 + offs[0]:t.index(b"\0", tab + 12 + offs[0])]))
check("page kinds 0-3 titles share one row in all nine locales", all(v[0] for v in ph.values()))
check("the shared row reads 'NOT USED' in fr and 'DUMMY' in es", ph["fr"][1] == "NOT USED" and ph["es"][1] == "DUMMY", {k: v[1] for k, v in ph.items()})

print("== B. the handbook key is a saved-cursor slot")
body = [f"{x.mnemonic} {x.op_str}" for x in dis(0x2527B0)]
check("002527B0 bases on [020927C0]", rip_target(0x2527B0) == 0x20927C0)
check("002527B0 stores word +0x30, byte +0x70, dword +0x90 (banks 6/7/8), clamped",
      "mov word ptr [r9 + rax*2 + 0x30], r8w" in body and "mov byte ptr [rax + r9 + 0x70], r8b" in body and "mov dword ptr [r9 + rax*4 + 0x90], r8d" in body
      and not any(s.startswith("call") for s in body))
for a, s in ((0x5732B5, "lea ecx, [rbx + 6]"), (0x571ED6, "mov ecx, 6"), (0x5721EF, "lea ecx, [r8 + 6]"), (0x56EDCF, "mov ecx, 6")):
    check(f"table-key call at {a:08X} passes bank 6", ins(a) == s, ins(a))

print("== C. single installers")
for proc, site in ((0x56F810, 0x574D28), (0x556F90, 0x556EF3)):
    refs = rip_refs(proc, proc + 1)
    check(f"{proc:08X}: exactly one rip reference, at {site:08X}", [a for a, _, _ in refs] == [site], [f"{a:08X}" for a, _, _ in refs])
    check(f"{proc:08X}: no absolute qword pointer in the file", struct.pack("<Q", proc) not in d)
    rv = struct.pack("<I", proc - BASE); hits = []; i = d.find(rv)
    while i != -1: hits.append(i); i = d.find(rv, i + 1)
    pro = [ro for va, vs, ro, nm, rs in secs if nm == b".pdata"][0]
    def range_record(h):
        if sec_of_file(h) == ".pdata": return (h - pro) % 12 in (0, 4)          # begin or end field of RUNTIME_FUNCTION
        nxt = struct.unpack_from("<I", d, h + 4)[0]                             # chained unwind {begin, end, unwind}
        return sec_of_file(h) == ".rdata" and proc - BASE < nxt <= proc - BASE + funcs[proc]
    ok = all(range_record(h) for h in hits)
    check(f"{proc:08X}: every RVA-dword hit is a {{begin, end}} range record", ok and bool(hits), [f"{h:#x}:{sec_of_file(h)}" for h in hits])
s, j = branch_sites(0x574D00); check("00574D00 is called only from 00574E80 (005750CD)", s == [0x5750CD] and not j, [f"{a:08X}" for a in s])
s, j = branch_sites(0x556EC0); check("00556EC0 is called only from 00557DB0 (00557E76, 00557EE5)", s == [0x557E76, 0x557EE5] and not j, [f"{a:08X}" for a in s])
check("00557DB0 writes the requested board to +0x3D1 at 00558549", ins(0x558549) == "mov byte ptr [rcx + 0x3d1], al")
check("00556F90 id 2 builds the title from 0x3ED + index and the body from 0x838 + index",
      ins(0x556FE7) == "add ecx, 0x3ed" and ins(0x557010) == "add ecx, 0x838")
check("0x3ED..0x3F8 are the twelve board names (White Mage .. Shikari)", text(0x3ED) == "White Mage" and text(0x3F8) == "Shikari")
check("0x838 is a board description ending 'Preview License Board'", "Preview License Board" in text(0x838), text(0x838)[-40:])

print("== D. the confirm window's +0x630 word")
s, j = branch_sites(0x57C380)
check("0057C380 has exactly three callers (002CE08E, 002CE6BF, 00566941) and no jcc", s == [0x2CE08E, 0x2CE6BF, 0x566941] and not j, [f"{a:08X}" for a in s])
check("0057C380 is the only rip reference to 0057C480", [a for a, _, _ in rip_refs(0x57C480, 0x57C481)] == [0x57C39F])
check("0057C480 copies record +0x20 into +0x630", ins(0x57C4E4) == "mov eax, dword ptr [r13 + 0x20]" and ins(0x57C4E8) == "mov dword ptr [rsi + 0x630], eax")
check("Yes/No producer 002CDF20 passes 0xC812", ins(0x2CE086) == "mov dword ptr [rsp + 0x48], 0xc812")
check("sort producer 00566680 passes 0x8036", ins(0x566939) == "mov dword ptr [rsp + 0x40], 0x8036")
edis = sorted({int(x.op_str.split(", ")[1], 16) for x in dis(0x2CE370) if x.mnemonic == "mov" and x.op_str.startswith("edi, 0x")})
check("notice producer 002CE370 uses flag words 0x411A/0x511A/0x611A/0x1411A/0x1511A", edis == [0x411A, 0x511A, 0x611A, 0x1411A, 0x1511A], [hex(v) for v in edis])
check("notice passes edi as the flag word (002CE6BB)", ins(0x2CE6BB) == "mov dword ptr [rsp + 0x40], edi")
union = 0xC812 | 0x8036
for v in edis: union |= v
check("positive control: the producers' union sets the used sound classes 0x4 and 0x100", union & 0x104 == 0x104, hex(union))
check("no producer sets 0x40 / 0x80 / 0x200 / 0x400", union & 0x6C0 == 0, hex(union))
tests = {0x57C506: "test byte ptr [rsi + 0x630], 0x20", 0x57C6F3: "test byte ptr [rsi + 0x630], 8", 0x57C7C0: "test dword ptr [rsi + 0x630], 0x800",
         0x57C93E: "test dword ptr [rsi + 0x630], 0x8000", 0x57C9E1: "bt ecx, 0xc", 0x57CA16: "bt ecx, 0x10", 0x57CAD1: "test al, 2",
         0x57CB8F: "test dl, 4", 0x57CB9B: "test dl, 0x40", 0x57CBA7: "test dl, dl", 0x57CBB2: "bt edx, 8", 0x57CBBF: "bt edx, 9",
         0x57CBCC: "bt edx, 0xa", 0x57C7F6: "bt eax, 0xd", 0x57CD77: "test dword ptr [rbx + 0x630], 0x4000", 0x57C34A: "test dword ptr [rcx + 0x630], 0x4000"}
for a, t in tests.items(): check(f"bit test at {a:08X}: {t}", ins(a) == t, ins(a))
check("0x800 sets the list child's +0xE4 bit 0x80 (0057C7CC), which 002D2DB0 tests at 002D3829",
      ins(0x57C7CC) == "or dword ptr [rcx + 0xe4], 0x80" and ins(0x2D3829) == "test byte ptr [rbx + 0xe4], 0x80")
check("the list plays its +0xFC byte as the decide sound (002D4114 read, 00249C60 at 002D4234)",
      ins(0x2D4114) == "movzx ecx, byte ptr [rbx + 0xfc]" and ins(0x2D4234) == "call 0x249c60")
check("0057CB16 writes the list's +0xFC (0057CBD7)", ins(0x57CBD7) == "mov byte ptr [r8 + 0xfc], al")
check("header rows: 0x4B48 is 'HINWEIS' and 0x4B42 'AUSWAHL' in de", text(0x4B48, "de") == "HINWEIS" and text(0x4B42, "de") == "AUSWAHL",
      (text(0x4B48, "de"), text(0x4B42, "de")))
print(f"FAILS {fails}")
sys.exit(1 if fails else 0)
