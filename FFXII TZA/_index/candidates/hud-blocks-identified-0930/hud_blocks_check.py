"""hud_blocks_check.py - five embedded blocks of the battle HUD singleton ManagerSingleton0209BE80 identified, plus
GR-3 (what the combo popup draws). SWE2-ORACLE for OPUS, 2026-09-30. Static: the certified image through
Database/Tools/analysis-kit/gfz-scripts/retool.py, the layout-key reader table, and the shipped text files for the
text ids (the size-match method of GE-1).

  _5380  the battle number popups: EXP / LP gains (pool A), the combo count (pool B), a third pool C (not identified)
  GR-3   the combo popup: count, lifetime, animation tracks, sprites and layout keys
  _57E0  the enemy chain counter
  _A0D0  the key-signal (button legend) strip
  _7EA0  the 2D side cursor (two cross-fading lanes that follow an actor)
  _00A0  the area-name markers (partytop_8_c sprites plus area-name labels near the leader)

Prints PASS/FAIL per step and FAILS n last.
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DBROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.abspath(os.path.join(DBROOT, "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
from capstone import CS_OP_MEM  # noqa: E402

R, SZ, C = T.R, T.sizes(), T.scan()
CALLS = C["calls"]
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(a):
    i = ins(a)
    for op in i.operands:
        if op.type == CS_OP_MEM and op.mem.base == T.RIP:
            return i.address + i.size + op.mem.disp
    return None


def callers(a):
    return sorted(set(CALLS.get(a, ())))


def at(a, pairs):
    return all(txt(x) == s for x, s in pairs)


def page(rel):
    return open(os.path.join(DBROOT, rel), encoding="utf-8").read()


# the layout-key reader table (key -> reader)
KEYS = {}
for ln in open(os.path.join(DBROOT, "16-UI", "Layout-Parameter-System", "members", "layout-key-readers.tsv"), encoding="utf-8"):
    c = ln.rstrip("\r\n").split("\t")
    if len(c) >= 3 and c[0] != "key":
        KEYS.setdefault(c[2], set()).add(c[0])

# the shipped text (GE-1 method: group = id / 1000 -> byte table 01E09F68 -> kind-2 loader id -> file by FST size)
FSTDIR = r"D:/FFXII MP Mod/FFXII_TestClient1/FileSizeTables"
TB = r"D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle"
LOC = {"us": "US", "de": "DE", "es": "ES", "fr": "FR", "it": "IT", "in": "IN", "kr": "KR", "cn": "CN", "ch": "CH"}


def fst_size(loc, lid):
    return struct.unpack_from("<i", open("%s/FileSizeTable_%s.fst" % (FSTDIR, LOC[loc]), "rb").read(), 4 * (2 * 5000 + lid))[0]


def dec(s):
    o = ""
    for ch in s:
        if 0x20 <= ch <= 0x39: o += chr(65 + ch - 0x20)
        elif 0x3A <= ch <= 0x53: o += chr(97 + ch - 0x3A)
        elif 0x54 <= ch <= 0x5D: o += chr(48 + ch - 0x54)
        elif ch == 4: o += " "
        elif ch == 0x9A: o += "?"
        elif ch == 0xA2: o += "("
        else: o += "{%02X}" % ch
    return o


def row(loc, fname, r):
    t = open("%s/%s/binaryfile/%s" % (TB, loc, fname), "rb").read()
    tab = struct.unpack_from("<I", t, 0x14)[0]
    st = tab + 12 + struct.unpack_from("<I", t, tab + 16 + 4 * r)[0]
    if t[st:st + 4] == b"ex00":
        return t[st + 4:st + 132].decode("utf-16le", "replace").split("\x00")[0]
    return dec(t[st:t.index(b"\0", st)])


def group_loader(g):
    return R.at(0x01E09F68 + g, 1)[0]


# ---------------------------------------------------------------- _5380: the battle number popups
check("A1", at(0x0028E2AB, [(0x0028E2AB, "add rcx, 0x5380"), (0x0028E2B2, "call 0x289970")])
      and at(0, [(0x00289979, "call 0x28a550"), (0x00289981, "call 0x28a350"), (0x0028998E, "jmp 0x28a620")])
      and txt(0x0028A55A) == "mov rbx, qword ptr [rcx + 0x420]" and txt(0x0028A368) == "mov rbx, qword ptr [rcx + 0x428]"
      and txt(0x0028A638) == "mov rbx, qword ptr [rcx + 0x430]",
      "gate group 0x0001 runs 00289970(hud + 0x5380): one tick pass per list - 0028A550 on +0x420, 0028A350 on +0x428, 0028A620 on +0x430")
check("A2", callers(0x00289A10) == [(0x0028EE10, 0x0028EEC5)] and txt(0x0028EEBB) == "add rcx, 0x5380"
      and at(0, [(0x00289A56, "mov rdi, qword ptr [r15 + 0x420]"), (0x00289AE7, "call 0x28b140"), (0x00289B2D, "call 0x28b140"),
                 (0x00289B54, "mov rbx, qword ptr [r15 + 0x428]"), (0x00289B7C, "call 0x28aaa0"),
                 (0x00289B8A, "mov rbx, qword ptr [r15 + 0x430]"), (0x00289BAC, "call 0x28a790")]),
      "the draw pass 00289A10 (only from 0028EE10, rcx = hud + 0x5380) draws +0x420 with 0028B140 (twice), +0x428 with 0028AAA0, +0x430 with 0028A790")
check("A3", KEYS.get("0028B140") == {"EXPLPNumOffsetX", "EXPLPNumOffsetY", "ExpLpPositionOffsetX", "ExpLpPositionOffsetY",
                                     "ExpNumOffsetX", "LpNumOffsetX", "NumEffectLPOffsetY", "mExpEffectOffsetY"}
      and KEYS.get("0028AAA0") == {"NumEffectOffsetY1", "NumEffectOffsetY2", "mNumEffectOffsetX1", "mNumEffectOffsetX2"}
      and "0028A790" not in KEYS,
      "layout keys: 0028B140 reads the eight ExpLp/ExpNum/LpNum/NumEffectLP keys, 0028AAA0 the four NumEffectOffset keys, 0028A790 none")
check("A4", callers(0x00289BD0) == [(0x00289D00, 0x00289D4C)] and callers(0x00289D00) == [(0x0028FB80, 0x0028FBAA), (0x0028FB80, 0x0028FBC8)]
      and txt(0x0028FBA7) == "xor r9d, r9d" and txt(0x0028FBB6) == "mov r9d, 1" and callers(0x0028FB80) == [(0x00312280, 0x00312518)],
      "pool A's only producer: 00312280 (defeat rewards) -> 0028FB80 -> 00289D00 twice, flag 0 then 1 (the EXP and the LP entry) -> 00289BD0")
check("A5", callers(0x0028E920) == [(0x00307300, 0x00307676)] and txt(0x0028E92E) == "add rcx, 0x5380" and txt(0x0028E935) == "jmp 0x289d70"
      and txt(0x00307651) == "mov eax, 0x96" and txt(0x0030765C) == "movzx eax, byte ptr [rdi + 0x6b8]"
      and callers(0x00290540) == [(0x0030AF30, 0x0030B03D)] and txt(0x00290577) == "add rcx, 0x5380" and txt(0x00290585) == "jmp 0x289f50",
      "pool B's producer: 00307300 on action 0x96 with the tally +0x6B8 -> 0028E920 -> 00289D70; pool C's: 0030AF30 -> 00290540 -> 00289F50")

# ---------------------------------------------------------------- GR-3: the combo popup
check("G1", txt(0x00289D70) == "cmp r8d, 2" and T.cstr(0x00915FA4) == "%2.2d" and rip(0x00289DD6) == 0x00915FA4
      and at(0, [(0x00289DF6, "shl r8d, 4"), (0x00289E00, "mov eax, 0x12"), (0x00289E08, "cmovg r8d, eax"),
                 (0x00289E1D, "mov dword ptr [rbx + 0xc], r9d"), (0x00289E51, "call 0x289d70"), (0x00289E5B, "mov eax, 0x80"),
                 (0x00289E6A, "mov word ptr [rbx + 0x10], ax"), (0x00289ED2, "or word ptr [rbx + 0x16], 1"),
                 (0x00289EEB, "mov dword ptr [rbx + 0xc], edi"), (0x00289F24, "mov word ptr [rbx + 0x14], r8w"),
                 (0x00289F29, "mov word ptr [rbx + 0x12], r9w")]),
      "recorder: counts below 2 are dropped; '%2.2d' -> one digit per nibble, capped at 0x12; a repeat below the cap pulls the clock back to 0x80 "
      "and zeroes the age; at the cap the old entry is detached (+0xC = 0) and a new one recorded")
check("G2", at(0, [(0x0028A37F, "mov ebp, 0x100"), (0x0028A3B6, "mov eax, 0x10"), (0x0028A3C1, "add word ptr [rbx + 0x10], ax"),
                   (0x0028A3CB, "inc word ptr [rbx + 0x12]"), (0x0028A3DD, "imul ecx, edx, 0x3c"), (0x0028A3FE, "call 0x2718e0"),
                   (0x0028A477, "call 0x275490"), (0x0028A393, "mov r15d, 0xfffe"), (0x0028A4F4, "and word ptr [rbx + 0x16], r15w")])
      and txt(0x0028A3BB).startswith("div dword ptr [rip") and rip(0x0028A3BB) == 0x01DFE0B4,
      "lifetime: clock +0x10 climbs 0x10 / [01DFE0B4] a frame to 0x100, then age +0x12 counts to 60 x [01DFE0B4]; the entry follows its unit "
      "(002718E0, eased by 00275490) and is freed when the unit is gone or the age runs out")


def keys(base, n):
    return [struct.unpack("<hhHBBHH", R.at(base + 12 * k, 12)) for k in range(n)]


check("G3", keys(0x00915F28, 3) == [(0, 0, 0, 0, 255, 0, 512), (0, 0, 128, 128, 128, 2, 256), (0, 0, 256, 128, 128, 0, 256)]
      and keys(0x00915F50, 2) == [(0, 0, 128, 128, 128, 0, 256), (0, 0, 256, 0, 255, 1, 512)]
      and txt(0x00271AF8) == "add r10, 0xc" and txt(0x00271BBF) == "movzx eax, byte ptr [rsi + rdi*4 + 6]",
      "two keyframe tracks {x, y, t, alpha, bright, curve, scale}: 00915F28 slams in (t 0-0x80: scale 2.0 -> 1.0, alpha 0 -> 0x80), "
      "00915F50 is the echo (t 0x80-0x100: scale 1.0 -> 2.0, alpha 0x80 -> 0)")
check("G4", rip(0x0028AAD7) == 0x00915F28 and rip(0x0028AAE8) == 0x00915F50 and txt(0x0028ABEE) == "cmp bx, di"
      and at(0, [(0x0028AB31, "shr edx, 2"), (0x0028AB71, "mov dword ptr [rbp - 0x79], 0x6e"), (0x0028AB78, "mov dword ptr [rsp + 0x24], 0x64"),
                 (0x0028AB8F, "cmp word ptr [r14 + 0x14], 0x12"), (0x0028ABB8, "call 0x861f0e"), (0x0028ABD4, "mov eax, 0x78"),
                 (0x0028AC17, "call 0x35d460"), (0x0028AE7F, "call 0x35d470"), (0x0035D467, "mov rax, qword ptr [rax + 0x338]"),
                 (0x0035D477, "mov rax, qword ptr [rax + 0x360]"), (0x0028AE5F, "mov dword ptr [rsp + 0x28], 1"),
                 (0x0028AE77, "mov dword ptr [rsp + 0x28], 2"), (0x0028AE9E, "and edi, 0xf"), (0x0028B0DD, "cmp esi, 2"),
                 (0x0028AC06, "call 0x3f0040"), (0x0028AE44, "call 0x3f1290"), (0x0028B0D6, "call 0x3f1290")])
      and rip(0x0028AE51) == 0x01E0C448 and rip(0x0028AE58) == 0x0209BA64 and rip(0x0028AE69) == 0x01E0C44C and rip(0x0028AE70) == 0x0209BA68,
      "0028AAA0: fades over the last quarter of the age; draws a label sprite ([0209AC30]+0x338) and one or two digits ([0209AC30]+0x360); "
      "at the cap: digit group 1, keys mNumEffectOffsetX1 / NumEffectOffsetY1, 120 % and a sine pulse; below it: group 2, X2 / Y2, 100 / 110 %")

# ---------------------------------------------------------------- _57E0: the enemy chain counter
w = {}
for f, n in SZ.items():
    b = R.at(f, n)
    if not b:
        continue
    for i in R.md.disasm(b, f):
        for op in i.operands:
            if op.type == CS_OP_MEM and op.mem.base != T.RIP and op.mem.disp in (0x7C7C, 0x7C82, 0x249C, 0x24A2):
                w.setdefault(op.mem.disp, set()).add(f)
check("C1", w.get(0x7C7C, set()) | w.get(0x7C82, set()) == {0x0028EF00, 0x0028EF50, 0x0028EF70, 0x0028F0C0}
      and w.get(0x249C, set()) | w.get(0x24A2, set()) == {0x003F9F40},
      "image-wide: only 0028EF00 / 0028EF50 / 0028EF70 / 0028F0C0 touch the request word hud+0x7C7C (= _57E0 +0x249C) and +0x7C82 (+0x24A2); "
      "only 003F9F40 reads them block-relative")
check("C2", callers(0x0028EF00) == [(0x00317ED0, 0x00318083)] and callers(0x0028EF70) == [(0x00317ED0, 0x00318065)]
      and callers(0x0028EF50) == [(0x003183D0, 0x003184F6)]
      and rip(0x00318050) == 0x022C3158 and rip(0x00318059) == 0x022C315C and rip(0x00318071) == 0x022C3158 and rip(0x00318077) == 0x022C315C
      and "`022C315C` / `022C3170` | chain count and base" in page("13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md")
      and "`022C3158` | chain-rank index" in page("13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md"),
      "the requesters: EnemyChain_UpdateOnDefeat 00317ED0 (-> 0028EF00 / 0028EF70) and EnemyChain_TryAdvanceRank 003183D0 (-> 0028EF50), "
      "handing the chain count 022C315C and the chain rank 022C3158")
check("C3", at(0, [(0x0028F0E3, "call 0x253770"), (0x0028F0EF, "mov word ptr [rax + 0x7c78], bx"), (0x0028F144, "add rcx, 0x57e0"),
                   (0x0028F16B, "call 0x244f00"), (0x0028F177, "add rcx, 0x58b0"), (0x0028F1AB, "add rcx, 0x5980"), (0x0028F1D8, "jmp 0x244f00")]),
      "0028F0C0(count): a live count is stored at +0x2498; count 0 releases all three widgets (+0x000, +0xD0, +0x1A0) - the chain broke")
check("C4", rip(0x003F9F91) == 0x003FACF0 and rip(0x003F9FD9) == 0x003FC3F0
      and at(0, [(0x003F9F51, "test byte ptr [rcx + 0x249c], 4"), (0x003F9FBC, "test byte ptr [rbx + 0x249c], 0x10"),
                 (0x003FA0C3, "mov ecx, 0xbf"), (0x003FA0CA, "mov ecx, 0xc2"), (0x003FA0D1, "mov ecx, 0xc1"), (0x003FA0D8, "mov ecx, 0xc0"),
                 (0x003FA0DD, "call 0x2dd7e0")]) and rip(0x002DD7EC) == 0x0215E6C8
      and "`fontcolor.bin`'s face colours at\n`0215E6C8`" in page("00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md"),
      "003F9F40: the rank advance (bit 2, 0028EF50) builds the 003FACF0 widget at +0xD0; the count is drawn in fontcolor.bin colour 0xBF-0xC2 by rank")

# ---------------------------------------------------------------- _A0D0: the key-signal strip
check("K1", at(0, [(0x0028E43D, "lea rcx, [rbx + 0xa0d0]"), (0x0028E444, "call 0x3f80d0"), (0x003F80D0, "test byte ptr [rcx + 0x984], 1"),
                   (0x003F80D7, "jne 0x3f7e80"), (0x003F7EAA, "lea rax, [rdi + 0x220]"), (0x003F7EFE, "mov edx, 0x110"),
                   (0x003F7F0D, "call 0x245000")]) and rip(0x003F7F03) == 0x003F8250,
      "gate group 0x0040: when +0x984 bit 0 is set, 003F7E80 builds a 0x110-byte strip widget (procedure 003F8250) bound to the block's +0x220")
check("K2", at(0, [(0x003F83C6, "mov qword ptr [rdi + 0xe0], rax"), (0x003F83D2, "mov ecx, 6"), (0x003F83D7, "call 0x2735e0"),
                   (0x003F840F, "mov dword ptr [rdi + 0xec], 0x5000b4"), (0x003F8452, "add eax, -0x5c")]) and rip(0x003F844C) == 0x01E0C1DC
      and txt(0x003F8820) == "cmp r9d, dword ptr [r8 + rdx*4 + 0x740]" and txt(0x003F88EE) == "call 0x3f8640",
      "003F8250: a 180 x 80 strip 92 px above the screen bottom, under root 6; 003F8790 keeps one row per non-zero entry of the block's "
      "four-entry queue +0x960 (bound +0x740)")
check("K3", rip(0x003F86A3) == 0x003F8510 and rip(0x003F86D0) == 0x00D11D50
      and at(0, [(0x003F86AF, "mov edx, 0xe8"), (0x003F86E6, "movsx ecx, word ptr [rbp + rdi*4 + 2]"), (0x003F86EB, "call 0x2f9860"),
                 (0x003F86F0, "movsx ecx, word ptr [rbp + rdi*4]"), (0x003F86F8, "add ecx, 0x4662"), (0x003F86FE, "call 0x2f9860"),
                 (0x003F8757, "mov dword ptr [rsi + 0x9c], 0x1200b4")]),
      "003F8640: each row is a 0xE8-byte widget (003F8510), 180 x 18, holding two texts from the 00D11D50 pair table: a label id and "
      "0x4662 + a button-template index")
lbl = [struct.unpack("<hh", R.at(0x00D11D50 + 4 * k, 4))[1] for k in range(12)]
ok = group_loader(5) == 1 and group_loader(18) == 55 and lbl[1:11] == [5001, 5002, 5003, 5004, 5006, 5008, 5009, 5010, 5011, 5012]
sizes_ok = all(fst_size(l, 1) == os.path.getsize("%s/%s/binaryfile/key_signal.bin" % (TB, l)) for l in LOC)
other = any(fst_size(l, 1) != os.path.getsize("%s/%s/binaryfile/listhelp_gambit.bin" % (TB, l)) for l in LOC)
tmpl = fst_size("us", 55) == os.path.getsize("%s/us/binaryfile/menu_command_template.bin" % TB)
ok = ok and sizes_ok and other and tmpl and row("us", "key_signal.bin", 11).endswith(" Shuffle") \
    and [row("us", "key_signal.bin", r) for r in (1, 2, 3, 4, 6)] == [""] * 5 and row("de", "key_signal.bin", 1).startswith("(Unused")
check("K4", ok, "the texts: group 5 -> loader 1 = key_signal.bin (its size in all nine locales' FSTs; the US size twin listhelp_gambit.bin "
      "fails in the others), group 18 -> loader 55 = menu_command_template.bin; row 11 is ' Shuffle', and the rows the modes queue "
      "(1-4, 6) ship empty in US and '(Unused' in German")
modes = [struct.unpack("<4I", R.at(0x00D11D80 + 16 * k, 16)) for k in range(6)]
check("K5", rip(0x003F80E0) == 0x00D11D80 and txt(0x003F80EE) == "lea r9, [rcx + 0x960]"
      and modes == [(1, 1, 1, 1), (4, 3, 2, 1), (4, 0, 0, 0), (4, 0, 0, 0), (4, 0, 0, 0), (5, 0, 0, 0)]
      and txt(0x0029045E) == "add rcx, 0xa0d0" and txt(0x00290465) == "jmp 0x3f80e0",
      "00290450(mode) -> 003F80E0(hud + 0xA0D0, mode) copies the mode's four row values from 00D11D80 into +0x960")
cs = callers(0x00290450)
check("K6", {f for f, _ in cs} == {0x0035C630, 0x0035D060, 0x0035D6B0, 0x0035D8D0, 0x0035D980, 0x0035DA80}
      and at(0, [(0x0035D77B, "mov ecx, 2"), (0x0035D780, "call 0x290450"), (0x0035DA25, "mov ecx, 2"), (0x0035DA2A, "call 0x290450"),
                 (0x0035D8E1, "mov ecx, 1"), (0x0035DA8D, "mov ecx, 1"), (0x0035C648, "mov ecx, 1"), (0x0035C651, "jmp 0x290450"),
                 (0x002D617A, "mov ecx, 5"), (0x002D617F, "call 0x35d060")])
      and "| 3 | `0035D980` | 24 | `0035D080` |" in page("16-UI/Request-Router/ui-request-router.md")
      and "with proc **`0035D6B0`**" in page("16-UI/Request-Router/ui-request-router.md"),
      "the requesters: request 24's widget procedure 0035D6B0 (party incapacitated) and request 3's route 0035D980 (leader selection) "
      "ask for mode 2; 0035C630 / 0035D8D0 / 0035DA80 for mode 1; 002D5EB0 for mode 5 through the thunk 0035D060")
setters = set()
for f, n in SZ.items():
    b = R.at(f, n)
    if not b:
        continue
    for i in R.md.disasm(b, f):
        for op in i.operands:
            if op.type == CS_OP_MEM and op.mem.base != T.RIP and op.mem.disp in (0x984, 0xAA54) and not i.mnemonic.startswith(("movs", "cvt", "adds", "subs", "muls", "divs", "comis", "ucomis")):
                setters.add((f, i.address))
check("K7", sorted(setters) == [(0x003F7E80, 0x003F7EA3), (0x003F7E80, 0x003F7EF0), (0x003F7E80, 0x003F7F23), (0x003F80D0, 0x003F80D0)],
      "LIMIT, measured: no integer instruction outside 003F7E80 / 003F80D0 addresses +0x984 (or hud + 0xAA54; the other +0x984 "
      "users are float loads / stores on other objects), so the build flag's first setter is not a displacement write")

# ---------------------------------------------------------------- _7EA0: the 2D side cursor
check("S1", at(0, [(0x00291794, "lea rcx, [rdi + 0x7ea0]"), (0x002917A5, "call 0x28ca30"), (0x0028CA32, "mov r8d, 0x80"),
                   (0x0028CA38, "jmp 0x861ec0"), (0x0028E55A, "lea rcx, [rbx + 0x7ea0]"), (0x0028E56A, "jmp 0x28c870")]),
      "00291750 clears the block (0028CA30: 0x80 bytes via 00861EC0); gate group 0x0800 tail-jumps 0028C870 on it")
check("S2", at(0, [(0x0028EDBE, "add rcx, 0x7ea0"), (0x0028EDC9, "call 0x28c970"), (0x0028C9B3, "lea rcx, [rdi + 0x30]"),
                   (0x0028C9B7, "shl rax, 5"), (0x0028C9C7, "call 0x28d8a0"), (0x0028C9CE, "cmp ebx, 2"), (0x0028D8E9, "call 0x28d460")])
      and KEYS.get("0028D460") == {"m2DSideCursorCenterX", "m2DSideCursorCenterY"},
      "the draw: 0028EAB0 -> 0028C970(hud + 0x7EA0) -> 0028D8A0 per lane (+0x30, +0x50) -> 0028D460, the reader of "
      "m2DSideCursorCenterX / m2DSideCursorCenterY")
check("S3", callers(0x0028CA40) == [(0x00290370, 0x00290388)] and txt(0x00290381) == "add rcx, 0x7ea0"
      and callers(0x00290370) == [(0x002BF0E0, 0x002BF1D9)] and {f for f, _ in callers(0x002BF0E0)} == {0x002BE080, 0x002BE300}
      and txt(0x002BF17F) == "lea edi, [rax - 2]" and txt(0x002BF1D5) == "mov edx, edi"
      and {f for f, _ in callers(0x0028C940)} == {0x00290990, 0x002909F0} and 0x002BE1A0 in {f for f, _ in callers(0x00290990)},
      "the requester: the target-info family - 002BF0E0 (from the pane's open path 002BE300) arms it on an actor through 00290370; "
      "00290990, which the pane router 002BE1A0 calls, clears it")
check("S4", at(0, [(0x0028CB38, "shl rsi, 5"), (0x0028CB5A, "or word ptr [rsi + 0x44], 1"), (0x0028CB5F, "mov dword ptr [rsi + 0x48], edi"),
                   (0x0028CB62, "mov byte ptr [rsi + 0x42], 0x80"), (0x0028CB70, "lea rdx, [rsi + 0x30]"), (0x0028CB77, "call 0x2e7f70")]),
      "ManagerSub7EA0Entry: one lane, re-armed alternately (+0x74 bit 1): live flag +0x14 bit 0, actor id +0x18, level +0x12 = 0x80, "
      "position +0x00 from the actor (002E7F70)")

# ---------------------------------------------------------------- _00A0: the area-name markers
check("N1", at(0, [(0x0028E4B3, "test dword ptr [rbx + 0x10f68], 0x100"), (0x0028E4BF, "lea rcx, [rbx + 0xa0]"), (0x0028E4C6, "call 0x3f8ec0"),
                   (0x0028FB47, "add rcx, 0xa0"), (0x0028FB4E, "jmp 0x3f8d20"), (0x003F8D51, "mov qword ptr [rdi + 0x52b8], rax")])
      and rip(0x003F8D45) == 0x01E0C208 and T.cstr(struct.unpack("<Q", R.at(0x01E0C208, 8))[0]) == "partytop_8_c"
      and callers(0x0028FB40) == [(0x00253780, 0x00253825)],
      "003F8D20 (from 00253780 through 0028FB40) loads the texture named by [01E0C208] = 'partytop_8_c' into +0x52B8")
check("N2", txt(0x003F8ED8) == "call 0x35bad0" and rip(0x0035BAD0) == 0x022C806C and txt(0x003F8F90) == "call 0x3f9720"
      and txt(0x003F8F9D) == "call 0x3f9720" and at(0, [(0x003F9527, "cmp eax, 0x40"), (0x003F9530, "shl rax, 8"), (0x003F9534, "lea rdi, [rsi + 0x20]"),
                                                        (0x003F95CB, "mov rax, qword ptr [rsi + 0x52b8]"), (0x003F98E8, "call 0x3f9390")]),
      "003F8EC0 follows the focus actor 022C806C and runs 003F9720 twice; 003F9390 fills up to 64 sprites parent + 0x20 + (i << 8) "
      "on the partytop_8_c texture (ManagerSub00A0Entry)")
check("N3", at(0, [(0x003F99D5, "call 0x377a40"), (0x003F99E7, "call 0x377870"), (0x003F99EE, "mov ecx, 0x3ec"), (0x003F99F3, "call 0x2f9860"),
                   (0x00377A6C, "shr edx, 0xe")])
      and "| `00377870` | `MapName_GetAreaNameById` |" in page("03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md")
      and group_loader(1) == 20 and fst_size("us", 20) == os.path.getsize("%s/us/binaryfile/menu_command.bin" % TB)
      and row("us", "menu_command.bin", 4) == "???",
      "003F9720 labels each group with MapName_GetAreaNameById (planmapname.bin) when the field's bit 14 or the link's flag allows, "
      "else text 1004 = '???' (menu_command.bin row 4)")
check("N4", callers(0x003F8C70) == [(0x0028EAB0, 0x0028EBDF)]
      and at(0, [(0x003F8C7F, "test byte ptr [rcx + 0x52c6], 1"), (0x003F8CB3, "lea rdx, [rdi + 0x20]"), (0x003F8CB7, "shl rax, 8"),
                 (0x003F8CC1, "call 0x3f1290"), (0x003F8CF3, "call 0x3f14d0")]),
      "the draw 003F8C70 (from 0028EAB0) queues the +0x52C0 sprites through 003F1290 and the labels whose +0x23C bits 0-1 are set "
      "through 003F14D0")
print("FAILS %d" % fails)
