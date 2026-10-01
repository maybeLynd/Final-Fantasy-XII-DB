"""gr19_drop_gate_check.py - GR-19: what the defeat body's drop gate decides about the death position (OPUS, 2026-09-30).
Static, the certified image (kit retool.py, regval.py).

D1  00319490 (only caller BattleUnit_ProcessDefeatRewardsAndLoot 00312280) resolves the party focus unit
    (PartyFocus_GetCurrentPackedActorHandle 003590D0 -> 003588B0 -> 00263E30) only while byte 02089340 bit 4 (0x10) is set
    and the unit's flag byte bit 3 is set, else passes NULL; it hands that unit and the defeated unit's position (x, y, z,
    w = [01CEBBA8]) to 003377C0.
D2  003377C0 (a shared 'is this spot free and standable for the unit' test: its other callers are movement bodies
    00334E00, 00339630, 0033BD70) returns 0 for a NULL unit or a unit without an actor (+0x10); takes the unit's collision
    extent pair (ActorRuntime_GetClass3FloatPair 00265090); and, when 002EA7F0 accepts the unit, gathers up to 0x1C
    actors around the position (00391D10, or 003920F0 when a coordinate is NaN).
D3  every gathered actor other than the unit itself (skipping a class-1 actor when the unit is class 4, +0xE68 byte +0x18
    bits 1-3) for which 00314EB0(unit, actor) holds - the two actors' +0xC0 -> +0x138 records share byte +6 and do not
    share a non-zero byte +0x119 - is counted, and ANY count makes 003377C0 return 0 (0033798D-0033799A): the
    00313F80 relation result only splits the tally, it never saves the drop.
D4  with nothing counted (or 002EA7F0 refusing), 00337700 decides: 0 unless 00391410 rejects the position (returns 0),
    Navigation_FindRegionForPositionXZ 00384130 finds a region (not 0xFF), and 00336390 accepts - it tests 0032A6A0 with the
    unit's movement-class byte +0x1F4 at the point and at the four points one radius (the larger extent) away in x and z.
D5  the defeat body rolls the drop only on a non-zero answer (00312588-00312597).
Prints PASS/FAIL per check and FAILS n last.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return a + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)


callers = lambda f: sorted({x for x, _ in c["calls"].get(f, ())})
check("D1", callers(0x00319490) == [0x00312280] and txt(0x003194A8) == "call 0x3590d0" and rip(0x003194AD) == 0x02089340
      and txt(0x003194AD).endswith(", 0x10") and txt(0x003194B8) == "call 0x3588b0" and txt(0x003194C5) == "call 0x263e30"
      and txt(0x003194CF) == "test byte ptr [rax], 8" and txt(0x003194D4) == "xor eax, eax" and txt(0x0031950C) == "call 0x3377c0",
      "focus unit only under 02089340 bit 4 and unit flag bit 3, else NULL; position -> 003377C0")
check("D2", callers(0x003377C0) == [0x00319490, 0x00334E00, 0x00339630, 0x0033BD70]
      and txt(0x003377E8) == "xor eax, eax" and txt(0x003377EF) == "mov rcx, qword ptr [rcx + 0x10]" and txt(0x00337832) == "call 0x265090"
      and txt(0x00337858) == "call 0x2ea7f0" and txt(0x0033785F) == "je 0x33799e" and txt(0x00337897) == "mov r9d, 0x1c"
      and txt(0x003378B2) == "call 0x391d10" and txt(0x003378E6) == "call 0x3920f0",
      "003377C0: NULL / actorless -> 0; collision extent 00265090; gather up to 0x1C actors (00391D10 / 003920F0)")
ok = txt(0x00337915) == "cmp rbp, rdx" and txt(0x00337934) == "cmp eax, 1" and txt(0x0033794E) == "cmp eax, 4" \
    and txt(0x00337956) == "call 0x314eb0" and txt(0x0033796F) == "call 0x313f80" and txt(0x0033797B) == "inc esi" \
    and txt(0x0033797F) == "inc edi" and txt(0x0033798D) == "test esi, esi" and txt(0x0033798F) == "jne 0x33799a" \
    and txt(0x00337991) == "neg edi" and txt(0x00337995) == "and eax, 2" and txt(0x0033799A) == "xor eax, eax" \
    and txt(0x00314EF3) == "movzx eax, byte ptr [r9 + 6]" and txt(0x00314EF8) == "cmp byte ptr [r10 + 6], al" \
    and txt(0x00314EFE) == "movzx eax, byte ptr [r10 + 0x119]" and txt(0x00314F0A) == "cmp al, byte ptr [r9 + 0x119]"
check("D3", ok, "any gathered actor sharing the unit's +0x138 byte +6 group (not the same non-zero +0x119) makes the answer 0")
ok = txt(0x00337724) == "xor eax, eax" and txt(0x0033774C) == "call 0x391410" and txt(0x00337753) == "jne 0x337724" \
    and txt(0x0033776F) == "call 0x384130" and txt(0x00337774) == "cmp eax, 0xff" and txt(0x00337784).startswith("maxss xmm1") \
    and txt(0x0033778A) == "movzx r8d, byte ptr [rdi + 0x1f4]" and txt(0x00337792) == "call 0x336390" \
    and sum(1 for x in R.md.disasm(R.at(0x00336390, SZ[0x00336390]), 0x00336390) if x.mnemonic == "call" and x.op_str == "0x32a6a0") >= 4
check("D4", ok, "00337700: 00391410 must pass, 00384130 must find a region, 00336390 tests 0032A6A0 at the point and four offsets")
ok = any(x.mnemonic == "call" and x.op_str == "0x319490" and 0x00312570 <= x.address <= 0x003125A0
         for x in R.md.disasm(R.at(0x00312280, SZ[0x00312280]), 0x00312280))
check("D5", ok, "the defeat body calls the gate at 00312588-00312597 and rolls the drop only on a non-zero answer")
print("FAILS %d" % fails)
