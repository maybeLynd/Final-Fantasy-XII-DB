"""ms4_check.py - MS-4: who sends the field-time map container 02B47760 message 14 (its opening), and with which index
(OPUS, 2026-09-30). Static, kit retool.py.

M1  003CB440 builds the container: 00244F50(0x179E0 bytes, procedure 003CB650) into [02B47760]; its callers are 00251F40 and
    00253A30. The container procedure dispatches on (id - 1) through image-base tables: id 14 takes the default arm 003CB9CF,
    id 0x20 the arm 003CB7DB.
M2  the generic activation helper 00246AC0 / 00246AD0 ends by calling the activated widget's procedure with the static
    message at 01E0C0E0 = {14, 0, 0, 0} (00246BFF-00246C09); so every activated widget receives message 14 with index 0.
    Of the eleven rip references to 02B47760 (all listed), none activates the container or hands it to a message call: they
    test it, copy its +0x190 block (002B6570, 002BA040), destroy it (003CB410) or build it (003CB440). The container is
    activated only by its own 0x20 arm (003CB7DE). (003CA2F0, which activates a widget, reads the neighbouring global
    02B47758 - the control that the census tells the two apart.)
M3  the container's 0x20 arm: activates itself, takes the index from 003BC160() when container +0x179D8 == 6 and from
    003BFDF0() otherwise (003BFDF0 = 003C0380 of the field id from 00264790, falling back to 003148F0), stores it at
    +0x179D0, and - when it is not negative - creates the page 00244F50(0xC0, 003CB4F0), then calls the page procedure
    directly with {14, 0, index, 0} (003CB835-003CB85F).
M4  the page procedure 003CB4F0 takes id 14 (r8d - 1 - 0xD == 0) to 003CB581, the preload arm.
M5  image-wide, the only stack-built message 14 handed to a procedure call are 003CB835 and 00292AB2 (an unrelated
    procedure); and the only static message struct with id 14 passed to a procedure is 01E0C0E0 (positive control for M2).
Prints PASS/FAIL per check and FAILS n last.
"""
import os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
BASE = 0x00120000
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins_at(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def txt(a):
    i = ins_at(a)
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(i):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return i.address + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1) if m else None


callers = lambda f: sorted({x for x, _ in c["calls"].get(f, ())})

# M1
idx = R.at(BASE + 0x2ABA24, 0x2C)
case = lambda i: BASE + struct.unpack("<I", R.at(BASE + 0x2AB9EC + 4 * idx[i - 1], 4))[0]
ok = txt(0x003CB476) == "mov ecx, 0x179e0" and rip(ins_at(0x003CB46A)) == 0x003CB650 and txt(0x003CB489) == "call 0x244f50" \
    and rip(ins_at(0x003CB491)) == 0x02B47760 and callers(0x003CB440) == [0x00251F40, 0x00253A30] \
    and txt(0x003CB66C) == "dec eax" and txt(0x003CB66E) == "cmp eax, 0x2b" and rip(ins_at(0x003CB677)) == BASE \
    and case(0x0E) == 0x003CB9CF and case(0x20) == 0x003CB7DB
check("M1", ok, "container 0x179E0 bytes, procedure 003CB650; id 14 -> default %08X, id 0x20 -> %08X" % (case(0x0E), case(0x20)))

# M2
msg = struct.unpack("<IIQQ", R.at(0x01E0C0E0, 24))
refs = []
for f, n in SZ.items():
    try:
        fi = list(R.md.disasm(R.at(f, n), f))
    except Exception:
        continue
    for i in fi:
        if rip(i) == 0x02B47760:
            refs.append((f, i.address))
fns = sorted({f for f, _ in refs})
ok = rip(ins_at(0x00246BFF)) == 0x01E0C0E0 and txt(0x00246C09) == "call rax" and msg == (14, 0, 0, 0)     and txt(0x00246AC3).startswith("mov rcx, qword ptr [rip") and txt(0x00246ACA) == "jmp 0x246ad0"     and len(refs) == 11 and fns == [0x002B6570, 0x002BA040, 0x003CB3D0, 0x003CB3E0, 0x003CB410, 0x003CB440]     and rip(ins_at(0x003CA2F0)) == 0x02B47758 and txt(0x003CA2FA) == "jne 0x246ac0" and txt(0x003CB7DE) == "call 0x246ac0"
check("M2", ok, "activation delivers static message %s; the %d references to 02B47760 (in %s) never activate or message it; "
      "003CA2F0 activates 02B47758 (control); the container activates itself only at 003CB7DE"
      % (msg, len(refs), " ".join("%08X" % f for f in fns)))

# M3
ok = txt(0x003CB7E3) == "cmp byte ptr [rdi + 0x179d8], 6" and txt(0x003CB7EC) == "call 0x3bc160" and txt(0x003CB7F3) == "call 0x3bfdf0" \
    and txt(0x003CB7F8) == "mov word ptr [rdi + 0x179d0], ax" and txt(0x003CB802) == "jl 0x3cb868" \
    and rip(ins_at(0x003CB807)) == 0x003CB4F0 and txt(0x003CB80E) == "mov ecx, 0xc0" and txt(0x003CB813) == "call 0x244f50" \
    and txt(0x003CB826) == "movsx rcx, word ptr [rdi + 0x179d0]" and txt(0x003CB830) == "mov qword ptr [rsp + 0x28], rcx" \
    and txt(0x003CB835) == "mov dword ptr [rsp + 0x20], 0xe" and txt(0x003CB85A) == "lea rdx, [rsp + 0x20]" and txt(0x003CB85F) == "call rax" \
    and txt(0x003BFDF4) == "call 0x264790" and txt(0x003BFDFD) == "call 0x3148f0" and txt(0x003BFE08) == "jmp 0x3c0380"
check("M3", ok, "the 0x20 arm sends the page {14, 0, index, 0}, index = 003BC160() in mode 6 else 003C0380(field)")

# M4
ok = txt(0x003CB505) == "mov r8d, dword ptr [rdx]" and txt(0x003CB50B) == "sub r8d, 1" and txt(0x003CB515) == "sub r8d, 0xd" \
    and txt(0x003CB519) == "je 0x3cb581"
check("M4", ok, "the page procedure 003CB4F0 takes id 14 to its preload arm 003CB581")

# M5
stack14, static14 = [], []
for f, n in SZ.items():
    try:
        ins = list(R.md.disasm(R.at(f, n), f))
    except Exception:
        continue
    for k, i in enumerate(ins):
        m = re.match(r"dword ptr \[rsp \+ (0x[0-9a-f]+)\], 0xe$", i.op_str)
        if i.mnemonic == "mov" and m:
            for j in ins[k + 1:k + 10]:
                if j.mnemonic == "call":
                    if any(("lea rdx, [rsp + %s]" % m.group(1)) == (x.mnemonic + " " + x.op_str) for x in ins[k:ins.index(j)]):
                        stack14.append(i.address)
                    break
        if i.mnemonic == "lea" and i.op_str.startswith("rdx, [rip"):
            t = rip(i)
            if t and 0x01E00000 <= t < 0x01F00000 and any(j.mnemonic in ("call", "jmp") for j in ins[k + 1:k + 5]):
                try:
                    if struct.unpack("<I", R.at(t, 4))[0] == 0x0E:
                        static14.append((i.address, t))
                except Exception:
                    pass
ok = sorted(stack14) == [0x00292AB2, 0x003CB835] and static14 == [(0x00246BFF, 0x01E0C0E0)]
check("M5", ok, "stack-built message 14 sends: %s; static message-14 structs passed: %s"
      % (["%08X" % a for a in sorted(stack14)], ["%08X->%08X" % x for x in static14]))
print("FAILS %d" % fails)
