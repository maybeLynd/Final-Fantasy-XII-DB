"""gr12_actions_check.py - GR-12: what battle actions 0x9C and 0x9D do (SWE2-CONTRACT for OPUS, 2026-09-30).
Static: the certified image through the kit's retool.py, plus the shipped battle_pack.bin (action table directory +0x3C,
text bank 0 in the us / de / fr / es / it copies), help_action.bin and the 166 `in` .ard order sets.

S1   the kind-24 menu branch (0027C613): 00273270(own handle), entry == answer or entry == 0xFFFF -> 0x9D, else 0x9C,
     both through 00311CD0 with target = the unit's own handle and r9d = 0.
S2   0027C3D0's container-kind table: kind 11 -> 0027C584, kind 24 -> 0027C613; in kind 11 an entry id of 0x9C / 0x9D is
     issued at once (0027C596-0027C5FE), an entry with flag +0x54 bit 0x20 returns 9 (0027C5AA-0027C5AF).
S3   the submenu opener 0027E050: cmd 8 = kind 11 with category 0xD, cmd 9 = kind 24 (jump table 0x15E384).
S4   0031EB20 builds nothing for kind 24 (0031F70C returns the count it zeroed at 0031EB40); 0027C3D0 returns 0x16 on a
     count <= 0 (0027C3DF), so 0027C613 is never reached with an entry.
S5   0031EB20's kind-11 arm lists actions whose +0x1E == the category; 0x9B and 0x113 skip the 00317BC0 gate
     (0031EFB3 / 0031EFBB), and 0x9B's entry alone gets flag 0x20 (0031F17F).
S6   the gate that 0x9C / 0x9D meet: 003060E0 returns 5 for a party (kind 0) unit whose row +0x1E is outside
     {0,1,2,3,5,6,9,0xFF}; 00306480 turns that into 0x0F; 00317BC0 then answers 0, so the list drops them.
S7   the three rows 0x9B / 0x9C / 0x9D are the only +0x1E == 13 rows and carry no effect fields.
S8   the shipped names of bank 0 entries 155-157 (de / fr real names, us / es / it placeholders), controls 0x95 / 0x113.
S9   image-wide: every 0x9C / 0x9D immediate, and every 0x9B one in the battle band.
S10  submenu 8's openers: 0027C3D0 never returns 8; the kind-8 table ids give 10..14; 0027C730 returns 0x10..0x13;
     00276650 seeds +0x61B8 with 1; the eleven 0x1F / 0x21 posters.
S11  00311CF0 (BattleUnit_IssueCommand): what an issue writes.
S12  00305AB0: the pending command is cleared, gated by 002FFCF0, and committed only on 0.
S13  002FFCF0 passes category 13 through 0031A7B0 (0) and returns 00306480's 0x0F.
S14  every other +0xBA0 reader is gated on the pending bit or compares 0x113 / 0x95 only.
S15  the gambit-enable bit's run-time setter 00311AF0 has two callers, neither in the action pipeline.
S16  00273270: 0xFFFF on both early exits; the 0x0000FFFF preset is overwritten by 00329220's memset; 0 when the record
     is missing; else stats +0x5A.
S17  no authored enemy order record or weighted pick-table entry names 0x9B, 0x9C or 0x9D.
S18  the order-set path (gambits, enemy AI) gates each record through the same cascade before committing it.
Prints PASS/FAIL per step and FAILS n last.
"""
import collections, glob, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, os.path.join(DB, "Tools", "dashboard"))
import retool as T  # noqa: E402
import ff12_content as F  # noqa: E402

R = T.R
SZ = T.sizes()
EXT = "D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/%s/binaryfile/"
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def body(f):
    return [(i.address, "%s %s" % (i.mnemonic, i.op_str)) for i in R.md.disasm(R.at(f, SZ[f]), f)]


def has(a, text):
    return ins(a) == text


def jt(base_bytes, base_dw, n, img=0x120000):
    out = []
    for k in range(n):
        x = R.at(img + base_bytes + k, 1)[0] if base_bytes is not None else k
        out.append(struct.unpack("<I", R.at(img + base_dw + x * 4, 4))[0] + img)
    return out


# ---- S1 ------------------------------------------------------------------------------------------------------------
s1 = [(0x27C619, "mov ecx, dword ptr [rbx + 8]"), (0x27C61C, "movzx edi, word ptr [rdx + 0x50]"),
      (0x27C620, "call 0x273270"), (0x27C625, "cmp di, ax"), (0x27C628, "je 0x27c657"), (0x27C62A, "mov eax, 0xffff"),
      (0x27C62F, "cmp di, ax"), (0x27C632, "je 0x27c657"), (0x27C634, "mov ecx, dword ptr [rbx + 8]"),
      (0x27C637, "mov r8d, 0x9c"), (0x27C63D, "mov edx, ecx"), (0x27C63F, "xor r9d, r9d"), (0x27C642, "call 0x311cd0"),
      (0x27C657, "mov ecx, dword ptr [rbx + 8]"), (0x27C65A, "mov r8d, 0x9d"), (0x27C660, "mov edx, ecx"),
      (0x27C662, "xor r9d, r9d"), (0x27C665, "call 0x311cd0")]
check("S1", all(has(a, t) for a, t in s1),
      "0027C613 arm: entry == 00273270(own handle) or 0xFFFF -> 0x9D (0027C65A), else 0x9C (0027C637); "
      "00311CD0(handle, handle, id, 0) - the target is the unit itself (%d/%d instructions)" %
      (sum(has(a, t) for a, t in s1), len(s1)))
s1b = [(0x311CD4, "mov dword ptr [rsp + 0x20], r9d"), (0x311CD9, "movzx r9d, r8w"), (0x311CDD, "xor r8d, r8d"),
       (0x311CE0, "call 0x311b20"), (0x311BDE, "test ebx, ebx"), (0x311BE0, "je 0x311c93"), (0x311CA0, "mov edx, r12d"),
       (0x311CA6, "call 0x311cf0")]
check("S1b", all(has(a, t) for a, t in s1b),
      "00311CD0 -> 00311B20 with arg5 0 takes the single-unit arm 00311C93 -> 00311CF0(unit, handle, 0, id, 0)")

# ---- S2 ------------------------------------------------------------------------------------------------------------
kinds = jt(0x15C6B8, 0x15C6A0, 0x17)
k = {i + 6: t for i, t in enumerate(kinds)}
s2 = [(0x27C591, "movzx r10d, word ptr [rdx + 0x50]"), (0x27C596, "mov r8d, 0x9c"), (0x27C5A0, "sub ax, r8w"),
      (0x27C5A4, "cmp ax, 1"), (0x27C5A8, "jbe 0x27c5f2"), (0x27C5AA, "test cl, 0x20"), (0x27C5AF, "mov eax, 9"),
      (0x27C5FE, "call 0x311cd0"), (0x27C608, "mov eax, 0x17"), (0x27C3DF, "test eax, eax"), (0x27C3E1, "jg 0x27c3ee"),
      (0x27C3E3, "mov eax, 0x16")]
check("S2", k[11] == 0x27C584 and k[24] == 0x27C613 and all(has(a, t) for a, t in s2),
      "kind 11 -> %08X, kind 24 -> %08X; kind 11 issues an entry id 0x9C/0x9D at once (0027C5FE) and returns 9 for an "
      "entry with +0x54 bit 0x20 (0027C5AF); an empty container returns 0x16 (0027C3E3)" % (k[11], k[24]))

# ---- S3 ------------------------------------------------------------------------------------------------------------
cmds = jt(None, 0x15E384, 0x14)
s3 = [(0x27E2AC, "mov dword ptr [rcx + 0x4c0], 0xb"), (0x27E2B6, "mov qword ptr [rcx + 0x4d4], 0xd"),
      (0x27E2D8, "mov dword ptr [rcx + 0x4c0], 0x18"), (0x27E312, "call 0x31eb20")]
check("S3", cmds[7] == 0x27E29E and cmds[8] == 0x27E2CA and all(has(a, t) for a, t in s3),
      "0027E050 cmd 8 -> %08X (kind 11, category 13), cmd 9 -> %08X (kind 24, display 0027BC10); both built by "
      "0031EB20 at 0027E312" % (cmds[7], cmds[8]))

# ---- S4 ------------------------------------------------------------------------------------------------------------
bk = [struct.unpack("<I", R.at(0x120000 + 0x1FFB78 + R.at(0x120000 + 0x1FFBA4 + i, 1)[0] * 4, 4))[0] + 0x120000
      for i in range(0x23)]
s4 = [(0x31EB40, "mov dword ptr [rcx + 0x40], edi"), (0x31EB2E, "xor edi, edi"), (0x31F70C, "mov eax, dword ptr [rbx + 0x40]"),
      (0x31F70F, "jmp 0x31fb65")]
check("S4", bk[23] == 0x31F70C and bk[10] == 0x31ED58 and all(has(a, t) for a, t in s4),
      "0031EB20 kind 24 -> %08X: returns the count zeroed at 0031EB40, so the kind-24 list is always empty and the "
      "0027C613 comparison never runs; kind 11 -> %08X" % (bk[23], bk[10]))

# ---- S5 ------------------------------------------------------------------------------------------------------------
s5 = [(0x31EF0D, "movzx ecx, byte ptr [rbp + 0x1e]"), (0x31EF7A, "cmp eax, edx"), (0x31EFB3, "sub ecx, 0x9b"),
      (0x31EFB9, "je 0x31eff4"), (0x31EFBB, "sub ecx, 0x78"), (0x31EFBE, "je 0x31eff4"), (0x31EFCC, "call 0x317bc0"),
      (0x31EFD1, "test eax, eax"), (0x31EFD3, "je 0x31ef48"), (0x31F17F, "cmp ebp, 0x9b"), (0x31F187, "or word ptr [rbx + rsi*8 + 0x54], 0x20"),
      (0x31ED5E, "mov edx, dword ptr [rbx + 0x14]"), (0x31EF63, "cmp ebp, 0x116")]
check("S5", all(has(a, t) for a, t in s5),
      "kind 11 walks ids 0..0x115 whose +0x1E equals the container category (+0x14); 0x9B / 0x113 skip 00317BC0, every "
      "other id is dropped when 00317BC0 answers 0; only 0x9B's entry gets flag 0x20 (0031F187)")

# ---- S6 ------------------------------------------------------------------------------------------------------------
s6 = [(0x306129, "movzx eax, byte ptr [rdi + 5]"), (0x30612F, "jne 0x30632c"), (0x306181, "movzx eax, byte ptr [rcx + 0x1e]"),
      (0x306185, "cmp eax, 6"), (0x306188, "ja 0x3062f4"), (0x3062F4, "cmp eax, 9"), (0x3062F9, "cmp eax, 0xff"),
      (0x3062FE, "je 0x30630a"), (0x306300, "mov eax, 5"), (0x30619B, "cmp eax, 2"), (0x3061A0, "cmp eax, 3"),
      (0x3061A3, "jne 0x306300"), (0x30632C, "xor eax, eax"),
      (0x3064A6, "call 0x3060e0"), (0x3064AD, "je 0x3064bf"), (0x3064AF, "mov eax, 0xf"),
      (0x317BEC, "call 0x306480"), (0x317BF6, "jne 0x317c1c"), (0x317C1C, "xor eax, eax")]
check("S6", all(has(a, t) for a, t in s6),
      "003060E0: a kind-0 unit with row +0x1E = 13 (> 6, not 9, not 0xFF) returns 5 (00306300); a non-zero-kind unit returns "
      "0 (0030632C); 00306480 collapses it to 0x0F (003064AF); 00317BC0 returns 0 -> 0x9C / 0x9D never enter the list")

# ---- S7 ------------------------------------------------------------------------------------------------------------
bp = open(EXT % "us" + "battle_pack.bin", "rb").read()
act = F.st2e_rows(bp, 0x3C)
cat13 = [i for i, r in enumerate(act) if r[0x1E] == 13]
tally = collections.Counter(r[0x1E] for r in act)
refused = sorted(v for v in tally if not (v in (0, 1, 2, 3, 5, 6, 9, 0xFF)))
ok7 = cat13 == [0x9B, 0x9C, 0x9D]
fx = []
for a in (0x9C, 0x9D):
    r = act[a]
    fx.append((F.u16(r, 0x34) == a, r[0x08] == 0, r[0x10] == 0, r[0x11] == 0, F.u32(r, 0x18) == 0, F.u16(r, 0x22) == 0xFFFF,
               F.u16(r, 0x24) == 0xFFFF, F.u16(r, 0x30) == 0, F.u32(r, 0x0C) == 0x210, F.u16(r, 0x38) == 0xFFFF,
               r[0x1C] == 3, r[0x2D] == 0x20, F.u16(r, 0x36) == 0))
    ok7 = ok7 and all(fx[-1])
strip = lambda r: bytes(r[2:0x34]) + bytes(r[0x36:])          # all but the help id (+0) and the name word (+0x34)
ok7 = ok7 and strip(act[0x9B]) == strip(act[0x9C]) == strip(act[0x9D])
check("S7", ok7,
      "+0x1E == 13 rows: %s; rows 0x9C / 0x9D: name word = id, recipe +0x08 0, power 0/0, status mask 0, +0x22 / +0x24 "
      "0xFFFF, event +0x30 0, flags 0x210, menu +0x38 0xFFFF, +0x1C 3, +0x2D 0x20, +0x36 0; categories the S6 arm refuses "
      "for a party unit: %s" % ([hex(x) for x in cat13], refused))

# ---- S8 ------------------------------------------------------------------------------------------------------------
names = {}
for L in ("us", "de", "fr", "es", "it"):
    b0 = F.decode_banks(open(EXT % L + "battle_pack.bin", "rb").read())[0]
    names[L] = [F.dec(b0[i]) for i in (0x95, 155, 156, 157, 0x113)]
exp = {"de": ["Absteigen", "Au<84>er Anf<83>hrer An", "Alle An", "Gambit Aus", "Entlassen"],
       "fr": ["Descendre du chocobo.", "leaderigaion", "zeninon", "gambitoff", "Disparition"],
       "us": ["Dismount"] + ["<0F><29><8B><F9><ED><F3>Reserve"] * 3 + ["Dismiss"],
       "es": ["Bajar del chocobo", "DUMMY", "DUMMY", "DUMMY", "Retirada"],
       "it": ["Scendo dal chocobo", "dummy", "dummy", "dummy", "Commiato"]}
ha = open(EXT % "us" + "help_action.bin", "rb").read()
S = 0x528
helps = []
for a in (0x9B, 0x9C, 0x9D):
    k_ = F.u16(act[a], 0) - 4000
    o = S + 0xC + struct.unpack_from("<I", ha, S + 0x10 + 4 * k_)[0]
    helps.append(ha[o:ha.index(b"\0", o)])
cure = S + 0xC + struct.unpack_from("<I", ha, S + 0x10 + 4)[0]
check("S8", names == exp and helps == [b"", b"", b""] and F.dec(ha[cure:ha.index(b"\0", cure)]).startswith("Restore a small"),
      "bank 0 [0x95, 155, 156, 157, 0x113]: de %s; fr %s; us/es/it placeholders; help texts of 0x9B-0x9D (ids %s) empty, "
      "control help 4001 = Cure's" % (names["de"][1:4], names["fr"][1:4], [hex(F.u16(act[a], 0)) for a in (0x9B, 0x9C, 0x9D)]))

# ---- S9 ------------------------------------------------------------------------------------------------------------
rx = re.compile(r"^(cmp|mov|sub|add|lea) .*(, |- )(0x9c|0x9d|-0x9c|-0x9d|0xff64|0xff63)$")
rx9b = re.compile(r"^(cmp|mov|sub|add|lea) .*(, |- )(0x9b|-0x9b|0xff65)$")
hits, hits9b = [], []
for f, n in sorted(SZ.items()):
    d = R.at(f, n)
    if not d:
        continue
    for i in R.md.disasm(d, f):
        t = "%s %s" % (i.mnemonic, i.op_str)
        if rx.search(t) and not t.endswith("0x9c]") and not t.endswith("0x9d]"):
            hits.append((f, i.address, t))
        if rx9b.search(t) and 0x2F0000 <= f < 0x3A0000:
            hits9b.append((f, i.address, t))
idfuncs = sorted({f for f, a, t in hits if f in (0x27C3D0, 0x27CE70)})
other = sorted({f for f, a, t in hits} - {0x27C3D0, 0x27CE70})
exp_other = [0x16E290, 0x175EF0, 0x235AF0, 0x244500, 0x625830, 0x629690, 0x807650]
check("S9", idfuncs == [0x27C3D0, 0x27CE70] and other == exp_other and len(hits) == 12
      and [(f, a) for f, a, t in hits9b] == [(0x31EB20, 0x31EFB3), (0x31EB20, 0x31F17F)],
      "0x9C/0x9D immediates: %d sites; as action ids only in 0027C3D0 (menu classifier) and 0027CE70 (list display); the "
      "rest are other quantities in %s (0016E290 / 00175EF0 test the byte pair 9D 01 - the VP8 key-frame start code -, 00235AF0 a +0x9C offset, 00244500 a frame bound, 00625830 / 00629690 / 00807650 outside the battle code); 0x9B in "
      "002F0000-003A0000 only at 0031EFB3 / 0031F17F" % (len(hits), ["%08X" % x for x in other]))

# ---- S10 -----------------------------------------------------------------------------------------------------------
b = body(0x27C3D0)
movs = sorted({t for a, t in b if t.startswith("mov eax, ")})
no8 = "mov eax, 8" not in movs
tbl = R.at(0xD10680, 12)
ids8 = [tbl[j + 1] for j in range(0, 12, 2)]
b730 = body(0x27C730)
ret730 = sorted({t for a, t in b730 if re.match(r"mov eax, 0x1[0-3]$", t)} |
                {t for a, t in b730 if re.match(r"(mov r15d, 0x1[0-3]|lea r15d, \[r13 \+ 0xd\]|lea r15d, \[rax \+ 0x10\])$", t)})
s10 = [(0x2766A3, "lea r14d, [rbx + 1]"), (0x27670D, "mov word ptr [rsi + 0x61b8], r14w"), (0x27666B, "xor ebx, ebx"),
       (0x27A78E, "movzx eax, word ptr [r14 + 8]"), (0x27A793, "mov word ptr [rbx + 0x61b8], ax")]
post = []
rxm = re.compile(r"^mov dword ptr \[r\w+( [-+] (0x)?[0-9a-f]+)?\], (0x1f|0x21)$")
for f, n in sorted(SZ.items()):
    if not 0x240000 <= f < 0x2A0000:
        continue
    for a, t in body(f):
        if rxm.match(t):
            post.append(a)
check("S10", no8 and ids8 == [0, 1, 2, 3, 4, 2] and all(has(a, t) for a, t in s10) and len(post) == 11,
      "0027C3D0's eax immediates %s hold no 8 (its id + 0xA arm gets kind-8 ids %s -> 10..14); 0027C730 returns only "
      "0x10..0x13; 00276650 seeds +0x61B8 with 1; msg 33 copies a payload word (0027A793); 11 msg 0x1F/0x21 posters: %s" %
      ([m[9:] for m in movs], ids8, " ".join("%08X" % x for x in post)))

# ---- S11 -----------------------------------------------------------------------------------------------------------
s11 = [(0x311D6F, "or ecx, dword ptr [rax + 0x3c]"), (0x311D72, "test ecx, 0x8800203b"), (0x311D78, "jne 0x311ded"),
       (0x311D7A, "mov word ptr [rbx + 0xba0], si"), (0x311D81, "and dword ptr [rbx + 0x6b0], 0xfffffffd"),
       (0x311D88, "test edi, edi"), (0x311D8A, "jne 0x311dae"), (0x311DB0, "mov dword ptr [rbx + 0xbb8], eax"),
       (0x311DBB, "or word ptr [rbx + 0xba4], ax"), (0x311DC2, "or qword ptr [rbx], 0x4000"), (0x311DE8, "call 0x317e60")]
check("S11", all(has(a, t) for a, t in s11),
      "00311CF0: a unit whose record passes (+0x64|+0x3C) & 0x8800203B == 0 gets +0xBA0 = id, +0x6B0 bit 1 cleared, "
      "+0xBB8 = the target handle (its own), +0xBA4 |= 0x8000, unit qword |= 0x4000 (pending), then 00317E60")

# ---- S12 -----------------------------------------------------------------------------------------------------------
s12 = [(0x305AD0, "mov ecx, 0x4000"), (0x305ADF, "test rcx, rax"), (0x305AE2, "je 0x305b3c"),
       (0x305AE4, "movzx esi, word ptr [rbx + 0xba0]"), (0x305AEB, "btr rax, 0xe"), (0x305AF0, "mov qword ptr [rbx], rax"),
       (0x305AF6, "sub ax, cx"), (0x305AFE, "cmp ax, cx"), (0x305B01, "jbe 0x305b12"), (0x305B09, "call 0x2ffcf0"),
       (0x305B0E, "test eax, eax"), (0x305B10, "jne 0x305b3c"), (0x305B2F, "call 0x30f760"), (0x305B3C, "call 0x377c20")]
check("S12", all(has(a, t) for a, t in s12),
      "00305AB0: clears the pending bit (00305AEB), sends an id outside 0x4000-0x4166 through 002FFCF0 (00305B09) and "
      "skips BattleUnit_CommitAction (00305B2F) on any non-zero reason, falling through to the unit's own order sets")

# ---- S13 -----------------------------------------------------------------------------------------------------------
s13 = [(0x2FFE87, "call 0x31a7b0"), (0x2FFE8E, "jne 0x2ffd99"), (0x2FFE9D, "call 0x306480"), (0x2FFEA4, "jne 0x2ffd99"),
       (0x2FFD99, "mov r14, qword ptr [rsp + 0x38]"), (0x31A839, "movzx ecx, byte ptr [rcx + 0x1e]"), (0x31A84B, "cmp ecx, 1"),
       (0x31A84E, "jne 0x31a7f0"), (0x31A7F0, "xor eax, eax")]
check("S13", all(has(a, t) for a, t in s13),
      "002FFCF0: 0031A7B0 answers 0 for category 13 (0031A84E -> 0031A7F0); 00306480's 0x0F is returned (002FFEA4), so "
      "a party unit's 0x9C / 0x9D never reach +0x714 (the reason code 0x0F of the availability page)")

# ---- S14 -----------------------------------------------------------------------------------------------------------
rd = []
for f, n in sorted(SZ.items()):
    if not 0x200000 <= f < 0x600000:
        continue
    for a, t in body(f):
        if "+ 0xba0]" in t:
            rd.append((f, a, t))
gated = {0x2FF9EF, 0x3013C1, 0x31390A, 0x329983}
cmp_only = [a for f, a, t in rd if re.search(r"cmp word ptr \[\w+ \+ 0xba0\], (0x113|0x95)$", t)]
issue = [a for f, a, t in rd if f in (0x305AB0, 0x311CF0)]
lea_other = [a for f, a, t in rd if f in (0x28C590, 0x28C620)]
far = [a for f, a, t in rd if f == 0x453150]
gate_ok = has(0x2FF9E7, "and edx, 0x4000") and has(0x3013A7, "bt rax, 0xe") and has(0x313903, "bt rdx, 0xe") and \
    has(0x32997C, "bt rax, 0xe")
covered = set(cmp_only) | gated | set(issue) | set(lea_other) | set(far)
check("S14", gate_ok and covered == {a for f, a, t in rd} and len(rd) == 19,
      "%d +0xBA0 sites: %d compare 0x113 / 0x95 only, 4 generic readers gated on the pending bit (002FF9EF, 003013C1, "
      "0031390A, 00329983), the issuer / consumer, 0028C590 / 0028C620 (lea, a different base) and 00453150 (a store "
      "into another array)" % (len(rd), len(cmp_only)))

# ---- S15 -----------------------------------------------------------------------------------------------------------
c = T.scan()
callers = sorted(a for f, a in c["calls"].get(0x311AF0, ()))
check("S15", callers == [0x27C512, 0x567DDD] and has(0x311B06, "or dword ptr [rax], 4") and has(0x311B0F, "and dword ptr [rax], 0xfffffffb"),
      "the gambit on/off setter 00311AF0 (bit 2 of 00320A40(slot)) is called only by the battle menu's per-character "
      "toggle (0027C512) and 00567DDD; nothing in the action pipeline reaches it")

# ---- S16 -----------------------------------------------------------------------------------------------------------
s16 = [(0x27328D, "test ecx, ecx"), (0x27328F, "je 0x2732c1"), (0x273291, "call 0x3588b0"), (0x273299, "je 0x2732c1"),
       (0x2732C1, "mov eax, 0xffff"), (0x27329B, "mov eax, 0xffff"), (0x2732A7, "mov dword ptr [rsp + 0xcc], eax"),
       (0x2732A0, "lea r8, [rsp + 0x20]"), (0x2732B0, "call 0x31ff70"), (0x2732B5, "mov eax, dword ptr [rsp + 0xcc]"),
       (0x2732BC, "shr eax, 0x10"), (0x320010, "mov r9d, 1"), (0x320032, "jmp 0x329220"),
       (0x329231, "mov rdi, r8"), (0x32923C, "mov rcx, rdi"), (0x32923A, "xor edx, edx"), (0x32923F, "mov r8d, 0xc0"),
       (0x329248, "call 0x861ec0"), (0x329265, "test r14, r14"), (0x329268, "je 0x32999d"), (0x3296A3, "test ebp, ebp"),
       (0x329738, "movzx eax, word ptr [r14 + 0x5a]"), (0x32973D, "shl eax, 0x10"), (0x329740, "mov dword ptr [rdi + 0xac], eax")]
w_ac = [a for a, t in body(0x329220) if re.search(r"ptr \[rdi \+ 0xac\]", t)]
check("S16", all(has(a, t) for a, t in s16) and w_ac == [0x329740] and 0xCC - 0x20 == 0xAC,
      "00273270 returns 0xFFFF for a zero handle or an unresolved one (002732C1); otherwise 00329220 memsets the 0xC0-byte "
      "record (00329248), so the 0x0000FFFF preset at +0xAC is dead; a null stats record exits with +0xAC = 0 (00329268) -> 0; "
      "else +0xAC = stats +0x5A << 16 (00329740, its only writer) -> saved[0]")

# ---- S17 -----------------------------------------------------------------------------------------------------------
sec = F.u32(bp, 0x2C)
cnt = F.u16(bp, sec)
offs = [F.u32(bp, sec + 4 + 4 * i) for i in range(cnt + 1)]
pick = [F.u16(bp, o) for i in range(cnt) for o in range(sec + offs[i], sec + offs[i + 1], 4)]
recs, lit = 0, []
for fn in sorted(glob.glob("D:/FFXII_TZA_extract/ps2data/plan_master/in/plan_map/*/area/*.ard")):
    d = open(fn, "rb").read()
    s1 = F.u32(d, 0x14)
    n = F.u16(d, s1)
    of = struct.unpack_from("<%dI" % (n + 1), d, s1 + 4)
    for i in range(n):
        o = s1 + of[i]
        for r in range(sum(d[o:o + 12])):
            recs += 1
            lit.append(F.u16(d, o + 0x20 + 24 * r))
bad = [w for w in pick + lit if w in (0x9B, 0x9C, 0x9D)]
check("S17", recs == 50050 and pick.count(0x96) > 0 and not bad and has(0x308ED4, "cmp dx, ax") and has(0x308FDC, "movzx eax, dx"),
      "%d order records (word +0 read by 00308EC0: < 0x8000 literal, else a weighted pick from registry 02EBF160 = "
      "directory +0x2C, %d tables / %d entries, control Attack 0x96 x%d): no 0x9B / 0x9C / 0x9D" %
      (recs, cnt, len(pick), pick.count(0x96)))

# ---- S18 -----------------------------------------------------------------------------------------------------------
s18 = [(0x3015F7, "movzx ecx, word ptr [r12]"), (0x3015FC, "mov rdx, rdi"), (0x3015FF, "call 0x2ffcf0"),
       (0x301604, "test eax, eax"), (0x301606, "jne 0x3015e3"), (0x3015E3, "xor eax, eax"),
       (0x305DD2, "call 0x3014c0"), (0x305DD9, "je 0x305dfd"), (0x305DF4, "call 0x30f760")]
check("S18", all(has(a, t) for a, t in s18),
      "the order-set path (gambits and enemy AI) runs the same cascade: 003014C0 rejects a record whose action id gets a "
      "non-zero 002FFCF0 answer (00301606 -> 003015E3), and 00305CC0 commits (00305DF4) only records 003014C0 accepts")

print("FAILS %d" % fails)
