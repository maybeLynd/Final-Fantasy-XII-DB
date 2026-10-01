"""sd3_pause.py - SD-3's remainder: the input-side consumer of capability-policy bit 21 opens the PAUSE MENU, and bit 21
decides whether the pause is refused, deferred or immediate; plus a census of every bit-21 writer, which corrects the
'only the Save/Load handlers' premise (OPUS, 2026-09-30). Static, the certified image, via
Database/Tools/analysis-kit/gfz-scripts/retool.py and regval.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import regval as V  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
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
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return a + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)


def cstr(a):
    b = R.at(a, 64)
    return b.split(b"\0")[0].decode("ascii", "replace")


def callers(a):
    return sorted(set(f for f, s in c["calls"].get(a, ())))


# P1 - the widget 002282F0 builds (0xD0 bytes through the factory 00244F50, handler 00229590, kept at 01FD4940) is the pause
#      menu: its construct arm logs "PauseMenu Create" and its open step "PauseMenu Open" through the debug print 0017DB70
check("P1", txt(0x0022833A) == "mov ecx, 0xd0" and rip(0x0022832E) == 0x00229590 and txt(0x0022834A) == "call 0x244f50"
      and rip(0x00228352) == 0x01FD4940 and cstr(rip(0x0022995A)) == "PauseMenu Create\n" and cstr(rip(0x00229864)) == "PauseMenu Open\n"
      and txt(0x00229961) == "call 0x17db70" and txt(0x0022986B) == "call 0x17db70",
      "002282F0 builds the pause menu (handler 00229590)")
# P2 - the construct arm keeps the flag (payload +8) at +0xC8; flag 0 ends the arm in state 0 with nothing posted, flag 1
#      posts overlay request {3, text, 0x64} through 002CCD40 and enters state 1
check("P2", txt(0x00229974) == "mov eax, dword ptr [rbx + 8]" and txt(0x00229979) == "mov dword ptr [rbp + 0xc8], eax"
      and txt(0x00229A47) == "cmp dword ptr [rbp + 0xc8], esi" and txt(0x00229A4D) == "je 0x2297bf"
      and txt(0x002297BF) == "mov dword ptr [rbp + 0xc0], esi" and txt(0x00229A7C) == "mov qword ptr [rsp + 0x38], 3"
      and txt(0x00229A98) == "call 0x2ccd40" and txt(0x00229A9D) == "mov dword ptr [rbp + 0xc0], 1",
      "flag 1 opens at once (request 3, state 1); flag 0 waits in state 0")
# P3 - state 0 waits for 01FD4954; when it is set the menu clears it, posts the same request, sets +0xC8 = 1 and enters
#      state 1 - the deferred open
check("P3", txt(0x00229906).startswith("cmp dword ptr [rip") and rip(0x00229906) == 0x01FD4954 and txt(0x0022990D) == "je 0x2297c5"
      and rip(0x00229923) == 0x01FD4954 and txt(0x0022993C) == "call 0x2ccd40"
      and txt(0x00229941) == "mov dword ptr [rbp + 0xc0], 1" and txt(0x0022994B) == "mov dword ptr [rbp + 0xc8], 1",
      "state 0: wait for 01FD4954, then open")
# P4 - state 1 waits for request 3 to report ready (002CCC70(3) = [+0xE8] of the kind-3 slot), then logs the open, holds
#      audio groups 0-5 (002DF370(0x3F, 1, 1), skipped when 00226BD0(0xF) answers non-zero) and enters state 2
check("P4", txt(0x00229852) == "mov ecx, 3" and txt(0x00229857) == "call 0x2ccc70" and txt(0x0022985E) == "je 0x2297c7"
      and txt(0x00229891) == "call 0x226bd0" and txt(0x002298A7) == "lea ecx, [rax + 0x3f]" and txt(0x002298AD) == "call 0x2df370"
      and txt(0x002298F7) == "mov dword ptr [rbp + 0xc0], 2",
      "state 1 -> 2: the menu opens and audio groups 0-5 are held")
# P5 - the input-side gate 00228380: with bit 21 in the aggregate it reads row 1; row 1 without bit 21 refuses (returns 0,
#      no menu), row 1 with it clears the flag, so the menu is built deferred; without bit 21 the flag stays 1
check("P5", txt(0x002283DA) == "bt esi, 0x15" and txt(0x002283E2) == "call 0x2e1020" and txt(0x002283E7) == "bt eax, 0x15"
      and txt(0x002283EB) == "jae 0x22843a" and txt(0x002283ED) == "xor ebx, ebx" and txt(0x0022843F) == "xor eax, eax"
      and txt(0x00228424) == "mov ecx, ebx" and txt(0x00228435) == "jmp 0x2282f0" and callers(0x00228380) == [0x00253C70],
      "bit 21: row 1 lacks it -> refused; row 1 has it -> deferred; absent -> immediate")
# P6 - who fires the deferred open: 01FD4954's only writers are the menu itself and the setter 00229AE0, whose callers are
#      the movie bring-up 001B7690 / 001B7F30 (1), 001B8400 (its ecx), 001B82A0 (0) and 002CEB40 (1)
w = sorted(set(f for f, s, k in c["refs"][0x01FD4954] if k == "W"))
vals = {f: sorted(x[1] for x in V.value_at(f, s, "rcx", 1) if x[0] == "C") for f, s in c["calls"].get(0x00229AE0, ())}
check("P6", w == [0x00229590, 0x00229AE0] and rip(0x00229AE0) == 0x01FD4954
      and callers(0x00229AE0) == [0x001B7690, 0x001B7F30, 0x001B82A0, 0x001B8400, 0x002CEB40]
      and vals[0x001B7690] == [1] and vals[0x001B7F30] == [1] and vals[0x001B82A0] == [0] and vals[0x002CEB40] == [1],
      "01FD4954 <- 00229AE0: movie bring-up 1, 002CEB40 1, 001B82A0 0, 001B8400 its argument")
# W1 - every writer of policy bit 21 (002E1C20 set / 002E1CA0 clear, row and bit resolved by regval): row 1 is written by
#      the four Save/Load sites AND by the movie player, the script verb 0023FBE0, 002CEB40 and the title consumer 003939B0;
#      row 0 by the title singleton handler 00394070; rows 2 / 8 by the restore loop 00229510 (bits 0..21 from a saved mask)
b21 = {}
for prim, op in ((0x002E1C20, "set"), (0x002E1CA0, "clear")):
    for f, s in c["calls"].get(prim, ()):
        bits = V.value_at(f, s, "rdx", 3)
        if ("C", 21) in bits:
            rows = tuple(sorted(x[1] for x in V.value_at(f, s, "rcx", 3) if x[0] == "C"))
            b21.setdefault((f, rows), set()).add(op)
want = {(0x001B7690, (1,)): {"clear"}, (0x001B7F30, (1,)): {"clear"}, (0x001B8400, (1,)): {"clear"}, (0x001B82A0, (1,)): {"set"},
        (0x0023FBE0, (1,)): {"set", "clear"}, (0x002CEB40, (1,)): {"set", "clear"}, (0x003939B0, (1,)): {"set", "clear"},
        (0x00394070, (0,)): {"set", "clear"}, (0x005823B0, (1,)): {"set", "clear"}, (0x00582860, (1,)): {"set", "clear"}}
loop = txt(0x0022956B) == "cmp edi, 0x16" and txt(0x00229554) == "call 0x2e1ca0" and txt(0x00229562) == "call 0x2e1c20" \
    and txt(0x00229534) == "cmp esi, 2" and txt(0x00229539) == "cmp esi, 8"
check("W1", b21 == want and loop,
      "bit-21 writers: Save/Load x2, movie x4, 0023FBE0, 002CEB40, 003939B0 (row 1); 00394070 (row 0); 00229510 restores rows 2/8")
print("FAILS %d" % fails)
