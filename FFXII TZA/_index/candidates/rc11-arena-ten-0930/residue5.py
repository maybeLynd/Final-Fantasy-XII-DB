"""residue5.py - the five push sites the value-set dataflow (arena_sites.py) leaves unresolved, closed by reading the
instructions that feed them (ORACLE, 2026-09-30, RC-11). Static. Reads only.

Each step below is asserted against the decoded image; a changed byte fails the run (exit 1). The script-driven sites
take their argument from the bytecode census (verb_census.out beside this file).

  002492B4 (in 00249210): arena = its 4th argument (mov edi, r9d at 00249239; mov ecx, edi at 002492B2).
     25 callers: 23 resolve by the dataflow to 2 or 3 (arena_sites.py's per-caller engine, re-run here); the other two
     pass their own r9 through (00249180, 002493D0) and their callers resolve to 2 or 3, except three that read the
     arena from memory, each read here:
       003C1F00 (via the thunk 003C2190: r8 <- rdx): r9d = dword [r14] at 003C1FFD, r14 = the thunk caller's rdx, a
         stack record whose +0 is stored as 2 (002B7CEF, 002BB0F7, 003CB5CB) and not rewritten (003C1F00 only reads
         [r14] and [r14+0x10]);
       003934F0 (one caller, 00574F78): r9d = dword [rbx] at 0039352E, rbx walking the .rdata table 00D23658 by 8
         (0039355D) for count 2 (00574F5C); the table's two dwords at +0 and +8 are 2 and 2;
       003C1D70 (one caller, 00563335): r9d = dword [r11] at 003C1DC9, r11 = the caller's r8 = rsp+0x20, stored as 2
         at 00563325.
  00384466 (in 00384420): arena = its 4th argument (mov ebx, r9d at 00384448; mov ecx, ebx at 00384464). Callers:
       00238260 -> 3 and 003843F0 -> 4 (dataflow); 002385D0 passes the result of 008478A0 (002385FA/002385FF), whose
       whole body is `mov eax, 3; ret` -> 3.
  003E9AC2 (in 003E9AA0): arena = ecx if ecx >= 0 else 6 (003E9AB3-003E9ABF). One caller, the handler of
       setexpandvoicememory 0034D080 (tail jump 0034D0AD), whose ecx is its SECOND pop (0034D09A -> ecx at 0034D0A1),
       the script's first argument. The census finds 10 shipped calls, all `4F:FFFF 4E:0000`, i.e. first argument -1
       (the decompiled corpus prints setexpandvoicememory(-1, 0x100000)) -> 6.
  0050D93F (in 0050D8F0) and 0050DB1F (in 0050DAD0): arena = a popped script int (00267E10 at 0050D934 / 0050DB14,
       via ebx). Reached only from the verbs 0x2003/0x2004 and 0x2008/0x2009 (handlers 0050DA30/0050D8F0 and
       0050DBD0/0050DAD0, each with one abs64 verb-table slot and no other reference). Shipped bytecode calls them 0
       times -> no value on shipped data; any int a script passes otherwise.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "rc9-log-channels-0930"))
import img  # noqa: E402
import rc9_channels as R  # noqa: E402

FAILS = []


def ins_at(a):
    x = img.dis(a, 16)[0]
    return ("%s %s" % (x.mnemonic, x.op_str)).strip()


def expect(a, text):
    got = ins_at(a)
    ok = got == text
    print("%s  %08X  %-40s%s" % ("PASS" if ok else "FAIL", a, got, "" if ok else "   (expected %s)" % text))
    if not ok:
        FAILS.append(a)


def per_caller(g, reg):
    out = {}
    for f in sorted(R.CALLERS[g]):
        st, _ = R.analyse_keep(f)
        for s in R.call_sites_to(f, g):
            v = st.get(s, {}).get(reg, R.UNK) if s in st else R.UNK
            c = R.resolve(f, R.trunc32(v))[0] if v is not R.UNK else None
            out[(f, s)] = c
    return out


def main():
    u32 = lambda a: int.from_bytes(img.rd(a, 4), "little")
    print("-- 002492B4")
    expect(0x00249239, "mov edi, r9d")
    expect(0x002492B2, "mov ecx, edi")
    vals = set()
    pc = per_caller(0x00249210, "r9")
    for (f, s), c in sorted(pc.items()):
        if c:
            vals |= c
    for g in (0x00249180, 0x002493D0):
        for (f, s), c in sorted(per_caller(g, "r9").items()):
            if c:
                vals |= c
    open_callers = sorted("%08X" % f for (f, s), c in pc.items() if not c)
    print("   dataflow-resolved caller values: %s; pass-through callers: %s" % (sorted(vals), open_callers))
    ok = open_callers == ["00249180", "002493D0"]
    print("%s  the only open callers are the two pass-throughs" % ("PASS" if ok else "FAIL"))
    FAILS.extend([] if ok else ["open"])
    expect(0x003C2190, "mov r9d, r8d")
    expect(0x003C2193, "mov r8, rdx")
    expect(0x003C1F2E, "mov r14, r8")
    expect(0x003C1FFD, "mov r9d, dword ptr [r14]")
    expect(0x002B7CE9, "lea rdx, [rbp - 0x70]")
    expect(0x002B7CEF, "mov dword ptr [rbp - 0x70], 2")
    expect(0x002BB0F1, "lea rdx, [rbp - 0x50]")
    expect(0x002BB0F7, "mov dword ptr [rbp - 0x50], 2")
    expect(0x003CB5C3, "lea rdx, [rsp + 0x20]")
    expect(0x003CB5CB, "mov dword ptr [rsp + 0x20], 2")
    expect(0x0039352E, "mov r9d, dword ptr [rbx]")
    expect(0x0039355D, "add rbx, 8")
    expect(0x00574F5C, "mov dword ptr [rsp + 0x20], 2")
    tab = (u32(0x00D23658), u32(0x00D23660))
    print("%s  table 00D23658 arena dwords %s" % ("PASS" if tab == (2, 2) else "FAIL", tab))
    FAILS.extend([] if tab == (2, 2) else ["tab"])
    expect(0x003C1D7D, "mov r11, r8")
    expect(0x003C1DC9, "mov r9d, dword ptr [r11]")
    expect(0x00563315, "lea r8, [rsp + 0x20]")
    expect(0x00563325, "mov dword ptr [rsp + 0x20], 2")
    print("   => 002492B4 arena set %s" % sorted(vals | {2}))
    print("-- 00384466")
    expect(0x00384448, "mov ebx, r9d")
    expect(0x00384464, "mov ecx, ebx")
    pc = per_caller(0x00384420, "r9")
    print("   dataflow per caller: %s" % {"%08X" % f: (sorted(c) if c else None) for (f, s), c in pc.items()})
    expect(0x002385FA, "call 0x8478a0")
    expect(0x002385FF, "mov r9d, eax")
    expect(0x008478A0, "mov eax, 3")
    expect(0x008478A5, "ret")
    v2 = set().union(*[c for c in pc.values() if c]) | {3}
    print("   => 00384466 arena set %s" % sorted(v2))
    print("-- 003E9AC2")
    for a, t in ((0x003E9AAC, "mov ebx, ecx"), (0x003E9AB3, "mov ecx, 6"), (0x003E9AB8, "test ebx, ebx"),
                 (0x003E9ABF, "cmovns ecx, ebx"), (0x0034D098, "mov ebx, eax"), (0x0034D09A, "call 0x267e10"),
                 (0x0034D0A1, "mov ecx, eax"), (0x0034D0AD, "jmp 0x3e9aa0")):
        expect(a, t)
    print("   => shipped: first argument -1 in all 10 calls (verb_census.out) -> arena 6")
    print("-- 0050D93F / 0050DB1F")
    for a, t in ((0x0050D932, "mov ebx, eax"), (0x0050D93B, "mov ecx, ebx"), (0x0050DB12, "mov ebx, eax"),
                 (0x0050DB1B, "mov ecx, ebx"), (0x0050DA8A, "jmp 0x50d8f0"), (0x0050DC2A, "jmp 0x50dad0")):
        expect(a, t)
    print("   => shipped: 0 calls of verbs 0x2003/0x2004/0x2008/0x2009 (verb_census.out)")
    print("RESULT %s" % ("PASS" if not FAILS else "FAIL %s" % FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
