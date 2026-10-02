"""title_astra_check.py - FABLE, 2026-10-02: re-read from the shipping image every instruction fact that
README.md (and the title-page subsection it drafts) cites for the seven consumed ASTRA title packets.

Every body is decoded by the kit's own Database/Tools/analysis-kit/gfz-scripts/disasm_fn.py ADDR LEN (a subprocess,
the tool's own Capstone decode and RIP resolution); the checks compare the decoded line at an exact address.
One extra non-instruction check reads the PE import descriptor that binds the IAT slot 008C2B48.
Control: the RNG page's anchor claim ("0062BCBE is a 0062EC70 call") must be REFUSED by the same matcher while the
line at 0062BCBE is present - a matcher that accepted anything would fail the control.
Run from anywhere; prints PASS/FAIL per check and FAILS n. Read-only."""
import hashlib, os, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DBROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))          # .../Database
DIS = os.path.join(DBROOT, "Tools", "analysis-kit", "gfz-scripts", "disasm_fn.py")
EXE = os.path.join(DBROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
fails = 0


def check(name, ok, why=""):
    global fails
    print("%-58s %s" % (name, "PASS" if ok else "FAIL " + why))
    fails += 0 if ok else 1


_cache = {}


def body(addr, length):
    key = (addr, length)
    if key not in _cache:
        out = subprocess.run([sys.executable, DIS, "%08X" % addr, str(length)], capture_output=True, text=True,
                             cwd=os.path.dirname(DIS)).stdout
        lines = {}
        for ln in out.splitlines():
            m = re.match(r"^([0-9A-F]{8})\s+[0-9a-f]+\s+(.*)$", ln)
            if m:
                lines[int(m.group(1), 16)] = m.group(2).strip()
        _cache[key] = lines
    return _cache[key]


def has(b, a, *subs):
    t = b.get(a)
    return t is not None and all(s.lower() in t.lower() for s in subs)


def expect(name, b, rows):
    bad = [("%08X" % a, b.get(a)) for a, *s in rows if not has(b, a, *s)]
    check(name, not bad, str(bad[:3]))


def calls_in(b, lo, hi):
    return [a for a, t in b.items() if lo <= a <= hi and t.startswith("call")]


# image identity
check("I0 image sha256", hashlib.sha256(open(EXE, "rb").read()).hexdigest() == SHA)

# --- tracker / getter / enqueue (title-tracker-callback-boundary, -qualification) ---
G = body(0x00189120, 8)
expect("T1 00189120 global getter (no argument read)", G,
       [(0x00189120, "mov rax, qword ptr [rip", "01F7F598"), (0x00189127, "ret")])
check("T1b getter is exactly two instructions", sorted(G) == [0x00189120, 0x00189127], str(sorted(G)))
H = body(0x00183720, 52)
expect("T2 00183720 null return, two reads, first tested, enqueue", H,
       [(0x00183720, "test rcx, rcx"), (0x00183723, "je 0x183753"), (0x0018372D, "call 0x189120"),
        (0x00183732, "test rax, rax"), (0x00183735, "je 0x18374e"), (0x00183737, "call 0x189120"),
        (0x0018373C, "mov rcx, rax"), (0x0018373F, "lea rdx", "0017ECC0"), (0x00183746, "mov r8, rbx"),
        (0x00183749, "call 0x185a90")])
check("T2b only one test of a getter result", sum(1 for t in H.values() if t.startswith("test rax")) == 1)
Q = body(0x00185A90, 86)
expect("T3 00185A90 queue address, unsigned end test, store order", Q,
       [(0x00185A94, "movsxd rax, dword ptr [rcx + 0xcb8]"), (0x00185A9B, "add rcx, 0xc38"),
        (0x00185AA2, "shl rax, 5"), (0x00185AB3, "mov rdx, qword ptr [rcx + 8]"),
        (0x00185AB7, "cmp rdx, qword ptr [rcx + 0x10]"), (0x00185ABB, "jae 0x185ad7"),
        (0x00185AC1, "mov qword ptr [rcx + 8], rax"), (0x00185AC5, "test rdx, rdx"),
        (0x00185ACF, "movups xmmword ptr [rdx], xmm0"), (0x00185AD6, "ret"), (0x00185ADC, "call 0x1858a0")])
check("T3b fast arm 00185ABD..00185AD6 makes no call", calls_in(Q, 0x00185ABD, 0x00185AD6) == [])
check("T3c whole body has exactly one call (00185ADC)", calls_in(Q, 0x00185A90, 0x00185AE5) == [0x00185ADC])
GR = body(0x001858A0, 367)
check("T4 001858A0 calls only allocator slots +0x10 / +0x18",
      has(GR, 0x00185956, "call qword ptr [rax + 0x10]") and has(GR, 0x001859DD, "call qword ptr [r9 + 0x18]")
      and calls_in(GR, 0x001858A0, 0x00185A0E) == [0x00185956, 0x001859DD], str(calls_in(GR, 0x001858A0, 0x00185A0E)))
T = body(0x001FB660, 188)
expect("T5 001FB660 queues value+0 and node+0x28, clears after", T,
       [(0x001FB677, "mov rcx, qword ptr [rcx]"), (0x001FB67A, "call 0x183720"), (0x001FB687, "xor ebp, ebp"),
        (0x001FB689, "mov qword ptr [rdi], rbp"), (0x001FB691, "mov rcx, qword ptr [rbx + 0x28]"),
        (0x001FB695, "call 0x183720"), (0x001FB69D, "mov qword ptr [rbx + 0x28], rbp"),
        (0x001FB6A1, "call 0x16d6d0"), (0x001FB6C7, "call 0x1af2b0"), (0x001FB6D8, "mov r8d, 0x30"),
        (0x001FB6E1, "call qword ptr [rax + 0x18]"), (0x001FB6FF, "mov qword ptr [rdi + 0x20], rbp"),
        (0x001FB703, "mov byte ptr [rdi + 0x28], bpl"), (0x001FB707, "mov dword ptr [rdi + 0x30], ebp"),
        (0x001FB712, "mov qword ptr [rdi + 0x18], rax"), (0x001FB71B, "ret")])
check("T5b 001FB660 makes exactly five calls", len(calls_in(T, 0x001FB660, 0x001FB71B)) == 5,
      str(calls_in(T, 0x001FB660, 0x001FB71B)))
CB = body(0x0017ECC0, 27)
expect("T6 0017ECC0 keeps data for 005DE250 then tails 0019C590", CB,
       [(0x0017ECC6, "mov rbx, rcx"), (0x0017ECC9, "call 0x5de250"), (0x0017ECCE, "mov rcx, rbx"),
        (0x0017ECD6, "jmp 0x19c590")])

# --- message 18 to the tracker (FABLE's own read; README marks it so) ---
R = body(0x0024A680, 141)
expect("T7 0024A680 calls 00181610", R, [(0x0024A6C9, "call 0x181610")])
check("T7b it is the first call in 0024A680", sorted(calls_in(R, 0x0024A680, 0x0024A70C))[:1] == [0x0024A6C9],
      str(sorted(calls_in(R, 0x0024A680, 0x0024A70C))))
expect("T8 00181610 manager getter then tail 001B1960", body(0x00181610, 30),
       [(0x00181619, "call 0x1b1c00"), (0x0018161E, "mov rcx, rax"), (0x00181621, "mov rdx, rbx"),
        (0x00181629, "jmp 0x1b1960")])
expect("T9 001B1960 found node: 001FB660(node+0x28), else skip", body(0x001B1960, 182),
       [(0x001B196D, "call 0x1b1440"), (0x001B1979, "lea rcx, [rdi + 0x2208]"), (0x001B19AB, "lea rax, [rdi + 0x2208]"),
        (0x001B19B2, "cmp rbx, rax"), (0x001B19B5, "je 0x1b1a0b"), (0x001B19B7, "mov rcx, qword ptr [rbx + 0x28]"),
        (0x001B19BB, "call 0x1fb660")])

# --- consumer and pump (title-queue-consumption, title-queue-pump-boundary) ---
C = body(0x00186230, 125)
expect("T10 00186230 bank advance, snapshot loop, reread + reset", C,
       [(0x0018623F, "mov eax, dword ptr [rcx + 0xcb8]"), (0x00186248, "inc eax"), (0x0018624A, "and eax, 3"),
        (0x0018624D, "mov dword ptr [rcx + 0xcb8], eax"), (0x00186256, "lea rax, [rbx + 0x62]"),
        (0x00186262, "mov rbx, qword ptr [rbx + rcx + 0xc38]"), (0x0018626A, "mov rdi, qword ptr [rax + rcx]"),
        (0x00186273, "mov rcx, qword ptr [rbx + 8]"), (0x00186277, "call qword ptr [rbx]"),
        (0x00186279, "add rbx, 0x10"), (0x00186282, "movsxd rcx, dword ptr [rsi + 0xcb8]"),
        (0x00186292, "mov rax, qword ptr [rcx + rsi + 0xc38]"), (0x0018629A, "mov qword ptr [rcx + rsi + 0xc40], rax")])
check("T10b 00186230 has one call (the pair function)", calls_in(C, 0x00186230, 0x001862AC) == [0x00186277])
expect("T11 00185C20 is a jump to 00186230", body(0x00185C20, 5), [(0x00185C20, "jmp 0x186230")])
P = body(0x0017D6E0, 404)
expect("T12 0017D6E0 zero gate, getter, flush, repeat edge", P,
       [(0x0017D6EF, "xor ebx, ebx"), (0x0017D6F6, "cmp dword ptr [rip", "01FD4A68", "ebx"),
        (0x0017D70C, "jne 0x17d71b"), (0x0017D70E, "call 0x189120"), (0x0017D713, "mov rcx, rax"),
        (0x0017D716, "call 0x185c20"), (0x0017D723, "call 0x22cb90"), (0x0017D853, "jmp 0x17d723")])
check("T12b 0017D6E0 has one flush call", [a for a, t in P.items() if "0x185c20" in t] == [0x0017D716])

# --- callback teardown and free import (title-cleanup-import-boundary) ---
D = body(0x005DE250, 50)
expect("T13 005DE250 guard 00625F00, conditional 0062BCB0, tail 00616C60", D,
       [(0x005DE262, "call 0x625f00"), (0x005DE268, "test al, al"), (0x005DE26A, "je 0x5de275"),
        (0x005DE26F, "call 0x62bcb0"), (0x005DE274, "nop"), (0x005DE275, "mov rcx, rbx"),
        (0x005DE27D, "jmp 0x616c60")])
expect("T14 00625F00 tests DWORD +0xBC", body(0x00625F00, 11),
       [(0x00625F00, "cmp dword ptr [rcx + 0xbc], 0"), (0x00625F07, "setne al"), (0x00625F0A, "ret")])
expect("T15 0019C590 jumps through IAT slot 008C2B48", body(0x0019C590, 7),
       [(0x0019C590, "jmp qword ptr [rip", "008C2B48")])


def import_name(va):
    d = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    secs, o = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, sva, rs, ra = struct.unpack_from("<IIII", d, o + 8); secs.append((sva, max(vs, rs), ra)); o += 40

    def off(rva):
        for sva, sz, ra in secs:
            if sva <= rva < sva + sz:
                return rva - sva + ra
        raise ValueError(hex(rva))

    imp_rva = struct.unpack_from("<I", d, pe + 24 + 112 + 8)[0]          # DataDirectory[1] (PE32+)
    want, p = va - base, off(imp_rva)
    while True:
        ilt, _, _, name_rva, iat = struct.unpack_from("<IIIII", d, p)
        if not iat:
            return None
        dll = d[off(name_rva):].split(b"\0")[0].decode()
        k = 0
        while True:
            ent = struct.unpack_from("<Q", d, off(ilt or iat) + 8 * k)[0]
            if not ent:
                break
            if iat + 8 * k == want:
                if ent >> 63:
                    return dll, "#%d" % (ent & 0xFFFF)
                return dll, d[off(ent & 0x7FFFFFFF) + 2:].split(b"\0")[0].decode()
            k += 1
        p += 20


nm = import_name(0x008C2B48)
check("T15b IAT slot 008C2B48 binds api-ms-win-crt-heap free",
      nm is not None and nm[0].lower() == "api-ms-win-crt-heap-l1-1-0.dll" and nm[1] == "free", str(nm))

# --- guard scope and count selector (title-cleanup-guard-..., title-cleanup-count-selector) ---
F = body(0x00616C60, 96)
expect("T16 00616C60 unconditional 0062B100 + 0062BCB0, guarded 00584730", F,
       [(0x00616C72, "call 0x62b100"), (0x00616C7B, "call 0x62bcb0"), (0x00616C80, "nop"),
        (0x00616C81, "mov ecx, dword ptr [rbx + 0x30]"), (0x00616C86, "shr eax, 0x1f"), (0x00616C8D, "je 0x616ca7"),
        (0x00616C8F, "btr ecx, 0x1f"), (0x00616C93, "cmp ecx, 1"), (0x00616C96, "jbe 0x616ca7"),
        (0x00616C98, "mov rcx, qword ptr [rbx + 0x38]"), (0x00616C9F, "je 0x616ca7"), (0x00616CA1, "call 0x584730"),
        (0x00616CA9, "mov qword ptr [rbx + 0x38], rax"), (0x00616CAD, "mov dword ptr [rbx + 0x30], eax"),
        (0x00616CB8, "jmp 0x5de290")])
check("T16b no +0xBC test in 00616C60 before 00616C7B",
      not any("0xbc" in t for a, t in F.items() if a < 0x00616C7B))
B = body(0x0062BCB0, 647)
expect("T17 0062BCB0 delegate, clear +0xBC, conditional 0062B870", B,
       [(0x0062BCBE, "call 0x62b100"), (0x0062BCC3, "mov rcx, qword ptr [rbx + 0x20]"), (0x0062BCC7, "xor r14d, r14d"),
        (0x0062BCCA, "mov dword ptr [rbx + 0xbc], r14d"), (0x0062BCD4, "je"), (0x0062BCD6, "call 0x62b870"),
        (0x0062BCDB, "test eax, eax"), (0x0062BCDD, "jne 0x62bf2b"), (0x0062BD75, "call 0x62ec70"),
        (0x0062BF29, "xor eax, eax"), (0x0062BF2B, "mov rbx, qword ptr [rsp + 0x48]"), (0x0062BF36, "ret")])
S = body(0x0062B100, 112)
expect("T18 0062B100 bound max(1,n), select, read, service loop", S,
       [(0x0062B10A, "mov edx, dword ptr [rcx + 0x30]"), (0x0062B10F, "and edx, 0x7fffffff"), (0x0062B115, "mov eax, 1"),
        (0x0062B11D, "cmovne eax, edx"), (0x0062B124, "mov edx, ebx"), (0x0062B129, "call 0x623df0"),
        (0x0062B12E, "mov ecx, dword ptr [rax]"), (0x0062B132, "jle 0x62b14e"), (0x0062B134, "mov ecx, 1"),
        (0x0062B139, "call 0x5ccb80"), (0x0062B143, "call 0x623df0"), (0x0062B14C, "jg 0x62b134"),
        (0x0062B14E, "mov ecx, dword ptr [rdi + 0x30]"), (0x0062B163, "jb 0x62b124")])
E = body(0x00623DF0, 56)
expect("T19 00623DF0 returns base + 0x58*k + 0x38", E,
       [(0x00623DF0, "mov eax, dword ptr [rcx + 0x30]"), (0x00623DF3, "btr eax, 0x1f"), (0x00623DF7, "cmp eax, 1"),
        (0x00623DFA, "jbe 0x623e0e"), (0x00623DFC, "mov r8, qword ptr [rcx + 0x38]"), (0x00623E00, "mov eax, edx"),
        (0x00623E02, "imul rax, rax, 0x58"), (0x00623E06, "add rax, 0x38"), (0x00623E0D, "ret"),
        (0x00623E0E, "lea r8, [rcx + 0x38]"), (0x00623E12, "xor ecx, ecx"), (0x00623E14, "test eax, eax"),
        (0x00623E18, "cmove r8, rcx"), (0x00623E27, "ret")])
check("T19b 00623DF0 writes no memory", not any(re.match(r"mov (byte|word|dword|qword) ptr \[", t) for t in E.values()))

# --- control: the matcher must refuse a wrong call target at a present line ---
check("K1 control: 0062BCBE present and 'call 0x62ec70' refused",
      0x0062BCBE in B and not has(B, 0x0062BCBE, "call 0x62ec70") and has(B, 0x0062BCBE, "call 0x62b100"))

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
