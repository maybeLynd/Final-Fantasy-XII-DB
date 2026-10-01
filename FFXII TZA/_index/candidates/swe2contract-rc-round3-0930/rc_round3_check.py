"""rc_round3_check.py - SWE2-CONTRACT, 2026-09-30. Static reads of the certified image plus the shipped .cl2 files.

Backs the round-3 RC incorporation (RC-37, RC-28, RC-30, RC-25, RC-5, RC-4, RC-13) with the instructions it relies on:

  A  RC-37 / RC-28: the two independent records (OPUS rc37-refused-read-0930, SWE2-DATA rc28-callback-0930) name
     different allocator layers for the .btm sheet. Both are on one chain: 00365810 -> 00249810 / 002497E0 ->
     0036A190 (-> 0036A1A0) / 0036A100 -> 0036BC60, and 0036BC60 clamps a negative size to 0 before rounding to 64
     (cmovns). So the -1 size becomes a 0-byte request (agreement, not a contradiction).
     A5 re-reads the shared core of both records (0046E030 returns 1; 00364380 never reads r8).
  B  RC-30 residue (the palette component order), new here: every palette row 0024A1D0 uploads goes through
     00180E70 / 00181000 -> 0017F3B0, which builds its texture with the fixed format object 02CF7480. That object is
     constructed by 00163D00 with the name 'RGBA8' (00D56100) and the value 0x1C in its four format slots.
     0017F3B0 then rescales byte 3 of every entry as a PS2 alpha: a' = min(255, trunc(a * 255 * (1/128))).
     B7 applies that to the 20 shipped loca_*.cl2 palettes: every entry above 0x80 saturates to 0xFF.
     B5 also pins 00180E70's arguments to 0017F3B0 (edx 0x10, r8d 1, r9d 1) and 0017F3B0's use of r9d as a count
     (cmp r15d, 1 / cmova), not a format: the format is the fixed object 02CF7480.
  C  Regressions that reject the superseded readings: the loca_*.cl2 request site 003C207A / 003C208D exists (RC-30's
     "no constant-request site" / "no traced request route"), and the reader 003C26C0 calls 0024A9E0 on widget +0x118
     ("no reader found").
  D  Register/page state after the edit (run after applying the rows): each row's live status word, each page box.

Controls: K1 a TIM2 file (loca_00.tm2) is not a CLT2 file, so B7's file filter is not vacuous; K2 the kind-0xFF
branch tests its submit result (0032E116), so A5's "no test" reading is not a reader artefact.
"""
import glob, io, os, re, struct, sys
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
FAILS = 0
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))


def ins(a):
    return next(md.disasm(R.at(a, 16), a, 1))


def expect(tag, a, text):
    global FAILS
    i = ins(a)
    got = ("%s %s" % (i.mnemonic, i.op_str)).strip()
    ok = got == text
    FAILS += not ok
    print("%s  %s %08X %s%s" % ("PASS" if ok else "FAIL", tag, a, got, "" if ok else "   (expected: %s)" % text))


def check(tag, ok, detail=""):
    global FAILS
    FAILS += not ok
    print("%s  %s%s" % ("PASS" if ok else "FAIL", tag, (" - " + detail) if detail else ""))


# ---- A: the .btm sheet allocation chain (RC-37 / RC-28 agreement)
expect("A1", 0x00365882, "call 0x32e400")
expect("A1", 0x00365895, "call 0x249810")
expect("A1", 0x0036589C, "call 0x2497e0")
expect("A1", 0x003658A4, "mov r9d, ebx")
expect("A2", 0x002497F4, "call 0x36a100")
expect("A2", 0x00249824, "call 0x36a190")
expect("A2", 0x0036A190, "mov edx, 1")
expect("A2", 0x0036A195, "jmp 0x36a1a0")
expect("A3", 0x0036A11F, "call 0x36bc60")
expect("A3", 0x0036A1C9, "call 0x36bc60")
expect("A4", 0x0036BC89, "xor eax, eax")
expect("A4", 0x0036BC8B, "test edx, edx")
expect("A4", 0x0036BC8D, "cmovns eax, edx")
expect("A4", 0x0036BC92, "add eax, 0x3f")
expect("A4", 0x0036BC9D, "and r14d, 0xffffffc0")


def rounded(size):  # the arithmetic of 0036BC89..0036BC9D (cdq / and 0x3f add is 0 for non-negative eax)
    eax = size if size >= 0 else 0
    eax += 0x3F
    return eax & 0xFFFFFFC0


expect("A4", 0x0036BD03, "cmp dword ptr [rcx + 0x18], r14d")
expect("A4", 0x0036BD31, "cmp dword ptr [rax + 0x18], r14d")
check("A4 size -1 rounds to 0 bytes; control: 1 rounds to 64, 64 stays 64",
      rounded(-1) == 0 and rounded(1) == 64 and rounded(64) == 64)
expect("A5", 0x0046E03E, "call 0x2df780")
expect("A5", 0x0046E043, "mov eax, 1")
body = [("%s %s" % (i.mnemonic, i.op_str)) for i in md.disasm(R.at(0x00364380, 0x1A), 0x00364380)]
check("A5 00364380 never reads r8", not any("r8" in b for b in body), "; ".join(body[:7]))
expect("K2", 0x0032E116, "test eax, eax")

# ---- B: the palette upload's texture format and alpha rescale (RC-30 residue)
expect("B1", 0x00163D0C, "lea rdx, [rip + 0xbf23ed]")
check("B1 00163D00's name argument is 'RGBA8'", R.at(0x00D56100, 6) == b"RGBA8\x00", repr(R.at(0x00D56100, 6)))
expect("B1", 0x00163D1B, "lea rcx, [rip + 0x2b9375e]")
for a in (0x00163D04, 0x00163D13, 0x00163D22, 0x00163D30):
    expect("B1", a, "mov dword ptr [rsp + 0x%x], 0x1c" % {0x00163D04: 0x40, 0x00163D13: 0x38,
                                                          0x00163D22: 0x30, 0x00163D30: 0x28}[a])
expect("B1", 0x00163D46, "call 0x616210")
expect("B2", 0x00616222, "mov dword ptr [rbx + 0x20], eax")
expect("B2", 0x00616230, "mov dword ptr [rbx + 0x28], eax")
expect("B3", 0x0017F419, "lea r9, [rip + 0x2b78060]")
expect("B3", 0x0017F433, "call 0x60dd70")
i = ins(0x0017F419)
check("B3 0017F3B0's format argument is the object 02CF7480", i.address + i.size + i.operands[1].mem.disp == 0x02CF7480)
expect("B4", 0x0017F517, "lea r8, [rdi + 3]")
expect("B4", 0x0017F528, "imul ecx, eax, 0xff")
expect("B4", 0x0017F50F, "movss xmm1, dword ptr [rip + 0x74661d]")
scale = struct.unpack("<f", R.at(0x008C5B34, 4))[0]
check("B4 the scale constant 008C5B34 is 1/128", scale == 1.0 / 128, repr(scale))
expect("B4", 0x0017F53E, "cvttss2si ecx, xmm0")
expect("B4", 0x0017F547, "cmovl edx, eax")
expect("B4", 0x0017F54A, "mov byte ptr [r8 - 4], dl")


def alpha(a):  # 0017F520..0017F54A: ecx = a*255 -> float * (1/128) -> truncate; edx = 255 unless ecx < 255
    c = int(struct.unpack("<f", struct.pack("<f", float(a * 255) * scale))[0])
    return (c & 0xFF) if c < 0xFF else 0xFF


check("B4 rescale: 0x00->0, 0x40->127, 0x80->255, 0x81->255, 0xFF->255",
      [alpha(x) for x in (0, 0x40, 0x80, 0x81, 0xFF)] == [0, 127, 255, 255, 255])
expect("B5", 0x00180F81, "mov r8d, 1")
expect("B5", 0x00180F87, "mov r9d, r8d")
expect("B5", 0x00180F8A, "lea edx, [r8 + 0xf]")
expect("B5", 0x00180F8E, "call 0x17f3b0")
expect("B5", 0x0017F3E9, "mov r15d, r9d")
expect("B5", 0x0017F440, "cmp r15d, esi")
expect("B5", 0x0017F447, "cmova edi, r15d")
expect("B5", 0x00181122, "call 0x17f3b0")
expect("B5", 0x0024A380, "call 0x180e70")
expect("B5", 0x0024A3B2, "call 0x180e70")
expect("B5", 0x0024A422, "call 0x181000")

EX = "D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok"
files = sorted(glob.glob(EX + "/*/bin_menu/loca_*.cl2"))
clt2 = [f for f in files if open(f, "rb").read(4) == b"CLT2"]
check("B6 20 shipped loca_*.cl2, all CLT2", len(files) == 20 and len(clt2) == 20, "%d files" % len(files))
dist = {}
for f in files:
    b = open(f, "rb").read()
    n = struct.unpack_from("<H", b, 0x1E)[0]
    a = [b[0x40 + 4 * k + 3] for k in range(n)]
    name = os.path.basename(f).lower()
    dist[name] = (n, sum(1 for x in a if x > 0x80), sum(1 for x in a if x == 0xFF), max([x for x in a if x != 0xFF] or [0]))
for name, (n, over, ff, mx) in sorted(dist.items()):
    print("   %-14s colours %3d  alpha > 0x80: %3d  alpha 0xFF: %3d  largest other 0x%02X" % (name, n, over, ff, mx))
check("B7 every alpha byte is 0xFF or at most 0x7F (the PS2 0..0x80 range the rescale expects, plus 0xFF, which saturates)",
      all(v[1] == v[2] and v[3] <= 0x7F for v in dist.values()))
tm2 = glob.glob("D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok/*/worldmap/bin/areatim2/loca_00.tm2")
check("K1 a TIM2 file is not CLT2 (the B6 filter discriminates)", bool(tm2) and open(tm2[0], "rb").read(4) != b"CLT2")

# ---- C: regressions against the superseded readings
expect("C1", 0x003C207A, "add r8d, 0xe1")
i = ins(0x003C208D)
check("C1 003C208D is a call (the kind-7 request)", i.mnemonic == "call", "%s %s" % (i.mnemonic, i.op_str))
expect("C2", 0x003C2794, "mov rcx, qword ptr [r13 + 0x118]")
expect("C2", 0x003C27A9, "call 0x24a9e0")

# ---- D: the register rows and page boxes after the edit
OQ = io.open(os.path.join(DB, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8").read().splitlines()


def row(rid):
    for l in OQ:
        if l.startswith("| %s |" % rid):
            return l
    return ""


def live(rid):
    cells = [c.strip() for c in row(rid).split(" | ")]
    return re.sub(r"^~~.*?~~\s*", "", cells[-1]).lstrip("*~ ").upper() if cells else ""


APPLIED = "swe2contract-rc-round3-0930" in row("RC-30")
print("   register rows applied: %s" % APPLIED)
if not APPLIED:
    # First publish (OPUS adjudication 2026-09-30): the register is held dirty by another lane, so the rows are not yet
    # restated. Then the rows keep their prior status and the boxes must stay unticked (check_questions consistency).
    check("D0 rows not yet restated: RC-37 and RC-30 still OPEN", live("RC-37").startswith("OPEN")
          and live("RC-30").startswith("OPEN"))
    for rel, rid in (("02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/btm-exfont-bitmaps.md", "RC-37"),
                     ("02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cl2-menu-colour-tables.md", "RC-30")):
        t = io.open(os.path.join(DB, rel), encoding="utf-8").read()
        m = re.search(r"^- \[( |x)\] \*\*%s\.\*\*" % re.escape(rid), t, re.M)
        check("D0 %s box unticked while its row is OPEN" % rid, bool(m) and m.group(1) == " ")
    cl2 = io.open(os.path.join(DB, "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cl2-menu-colour-tables.md"),
                  encoding="utf-8").read()
    check("D8 cl2 page names the request site and the reader", "003C208D" in cl2 and "003C26C0" in cl2)
    print("FAILS %d" % FAILS)
    sys.exit(1 if FAILS else 0)
check("D1 RC-37 ANSWERED, both records cited", live("RC-37").startswith("ANSWERED")
      and "rc37-refused-read-0930" in row("RC-37") and "rc28-callback-0930" in row("RC-37"))
check("D2 RC-28 carries the answered leftover (0046E030, 00364380)", "0046E030" in row("RC-28") and "00364380" in row("RC-28"))
check("D3 RC-30 ANSWERED on 003C1F00 with the RGBA8 upload", live("RC-30").startswith("ANSWERED")
      and "003C1F00" in row("RC-30") and "RGBA8" in row("RC-30"))
check("D4 RC-30 no longer states 'cannot produce' as live text",
      "index-computed sites cannot produce" not in row("RC-30"))
check("D5 RC-25 carries the mirror proviso (02166480)", live("RC-25").startswith("ANSWERED") and "02166480" in row("RC-25"))
check("D6 RC-5 narrowed to the event_menu prompt (1 to 9999), disposition proposed",
      live("RC-5").startswith("OPEN, NARROWED") and "9999" in row("RC-5") and "rc5b-event-slot-residue-0930" in row("RC-5"))

PAGES = {
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/btm-exfont-bitmaps.md": [("RC-37", True)],
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cl2-menu-colour-tables.md": [("RC-30", True)],
    "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/as7-menu-graphics-containers.md": [("RC-25", True)],
    "00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md": [("RC-5", False)],
}
for rel, want in PAGES.items():
    t = io.open(os.path.join(DB, rel), encoding="utf-8").read()
    for rid, ticked in want:
        m = re.search(r"^- \[( |x)\] \*\*%s\.\*\*" % re.escape(rid), t, re.M)
        check("D7 %s box on %s is %s" % (rid, os.path.basename(rel), "ticked" if ticked else "open"),
              bool(m) and (m.group(1) == "x") == ticked)
cl2 = io.open(os.path.join(DB, "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cl2-menu-colour-tables.md"),
              encoding="utf-8").read()
check("D8 cl2 page names the request site and the reader", "003C208D" in cl2 and "003C26C0" in cl2)

print("FAILS %d" % FAILS)
sys.exit(1 if FAILS else 0)
