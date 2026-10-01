"""alloc_nav_check.py - three ASTRA returns re-derived from the certified image's own bytes (FABLE, Claude Opus 5.5, 2026-09-28).
Instructions are decoded from FFXII_EXE (refused unless it is the certified 73461d image), never from a text view.

  A  allocator (ASTRA-REQ-FABLE-ALLOCATOR-RETRY-RETURN)
     A1 0036A190 = mov edx, 1 / jmp 0036A1A0; 0036A1A0 tests both allocator results (0036A1D3, 0036A1F8) and on null
        jumps to 0036A218, past the header stamps (0036A206, 0036A20E, 0036A214)
     A2 0036BFE0 (261 B) never reads its fifth or sixth stack argument ([rsp+0x50] / [rsp+0x58] after push + sub 0x20)
        and forms no rsp-relative address, so the flag 0036A1A0 stores at [rsp+0x28] has no local effect
     A3 the exit diamond 0036C0AE-0036C0C4, modelled on (edi, esi, rax): returns non-null always; returns null only when
        edi = 0 and esi = 0; otherwise retries at 0036C013. esi is the callback [heap+0xA0]'s eax (0036C043) or 0 (0036C047)
     A4 0036BFFB: a heap whose bit in 022D89B8 is clear spins on 0036C000 (jmp to itself)
  G  nav grid block (ASTRA-REQ-FABLE-NAV-GRID-ALLOC-RETURN)
     G1 00384580 skips its initializer 0036C660 when 0036A190 returns null (test / je 003845BB -> 003845CB) and returns rbx
     G2 003924B0 sizes the block ebx = nx*ny*(n+1) + n (esi = [02AEE0B8] at 00392506, edi = esi + 1 at 0039252D), stores
        the result to 02AEE0A0 (00392677) and memsets it (0039267E) with no test between the call and the memset
     G3 the block is carved: 02AEE0A8 = A0 + nx*ny*n (records), 02AEE0B0 = A8 + nx*ny (occupancy), leaving n bytes of
        mask scratch; with n = 0x24 the budget (0x2800 - n)/(n+1) = 275 is the largest cell count whose block fits 0x2800
  M  mask query (ASTRA-REQ-FABLE-NAV-MASK-RESET)
     M1 003912E0 calls memset(rcx = [02AEE0B0], edx = 0, r8 = movsxd [02AEE0B8]) at 0039130E with no branch or call before it
     M2 its only memory writes are the OR at 003913C4 through rdx = [02AEE0B0] and the prologue saves; it returns
        rax = [02AEE0B0] (003913E8); it takes four integers and no destination pointer
     M3 every function that ORs through 02AEE0B0 resets the mask first: 003912E0 (0039130E before 003913C4), 00391710
        (00391780 before 003918B3), 00391A30 (00391AAB before 00391BD3); the only jumps before each reset are the null-grid
        exits, which land past the OR loop. The six bodies decoded from the image hold all 13 references to 02AEE0B0
  C  controls (in memory; nothing is written or executed): 0036C0B9 JNE -> JE flips A3's (0, nonzero) cell; a planted
     test/je between 0039266A and 0039267E is seen by G2; a planted branch before 0039130E is seen by M1; an early jump
     from 0039173D into 00391710's OR loop fails M3
"""
import hashlib, os, re, struct, sys
import capstone
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
CERT = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != CERT: print("REFUSED  not the certified image"); sys.exit(2)
pe = struct.unpack_from("<I", d, 0x3c)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + 40 * i + 8) for i in range(ns)]
def off(v):
    r = v - 0x120000
    return next(ra + r - va for vs, va, rs, ra in SECS if va <= r < va + rs)
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
def body(img, a, n):
    o = off(a); ins = list(MD.disasm(img[o:o + n], a))
    assert ins and ins[-1].address + ins[-1].size == a + n, "%08X does not decode to its %d-byte extent" % (a, n)
    return [(i.address, i.mnemonic, i.op_str) for i in ins]
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
at = lambda B: {a: (m + " " + o).strip() for a, m, o in B}

# A
T, W, R = body(d, 0x36A190, 10), body(d, 0x36A1A0, 141), body(d, 0x36BFE0, 261)
w = at(W)
ok("A1", at(T) == {0x36A190: "mov edx, 1", 0x36A195: "jmp 0x36a1a0"}
   and w[0x36A1D3] == "test rax, rax" and w[0x36A1D6] == "jne 0x36a1fd" and w[0x36A1F8] == "test rax, rax" and w[0x36A1FB] == "je 0x36a218"
   and w[0x36A1E2] == "mov dword ptr [rsp + 0x28], esi" and all(0x36A1FD <= a < 0x36A218 for a in (0x36A206, 0x36A20E, 0x36A214)),
   "flag 1 tail-jumps into the wrapper; both results tested; null jumps past the stamps at 0036A206/0036A20E/0036A214")
stack_refs = [(a, m, o) for a, m, o in R if re.search(r"rsp \+ 0x(50|58)\]", o)]
lea_rsp = [(a, m, o) for a, m, o in R if m == "lea" and "rsp" in o]
saves = [a for a, m, o in R if re.search(r"rsp \+ 0x(30|38)\]", o)]   # the same pattern must see the slots that ARE used
ok("A2", not stack_refs and not lea_rsp and R[2][1:] == ("push", "r14") and R[3][1:] == ("sub", "rsp, 0x20") and len(saves) == 4,
   "no access to [rsp+0x50]/[rsp+0x58] and no lea of rsp in 0036BFE0; the pattern sees the 4 accesses to +0x30/+0x38")
def diamond(B):
    """Walk 0036C0AE..0036C0C4 for (edi, esi, rax) and return 'ret' or 'retry' per cell."""
    b = at(B); out = {}
    for edi in (0, 1):
        for esi in (0, 1):
            for rax in (0, 1):
                pc = 0x36C0AE; zf = None
                for _ in range(12):
                    s = b[pc]; nxt = min(a for a in b if a > pc)
                    m = re.match(r"test (\w+), \1", s)
                    if m: zf = {"edi": edi, "esi": esi, "rax": rax}[m.group(1)] == 0; pc = nxt; continue
                    m = re.match(r"(jne|je|jmp) 0x(\w+)", s)
                    if m:
                        take = m.group(1) == "jmp" or (m.group(1) == "je") == zf
                        pc = int(m.group(2), 16) if take else nxt
                        if pc == 0x36C013: out[(edi, esi, rax)] = "retry"; break
                        if pc == 0x36C0CA: out[(edi, esi, rax)] = "ret"; break
                        continue
                    raise ValueError("unmodelled %08X %s" % (pc, s))
    return out
D0 = diamond(R)
want = {k: ("ret" if k[2] or (k[0] == 0 and k[1] == 0) else "retry") for k in D0}
r = at(R)
ok("A3", D0 == want and len(D0) == 8 and r[0x36C043] == "mov esi, eax" and r[0x36C047] == "xor esi, esi" and r[0x36C03B] == "call rax",
   "non-null returns; null returns only for edi = 0 and esi = 0; esi = callback eax or 0")
ok("A4", r[0x36BFFB] == "jb 0x36c002" and r[0x36C000] == "jmp 0x36c000", "a disabled heap bit spins at 0036C000")
# G
L, G = body(d, 0x384580, 104), body(d, 0x3924B0, 607)
l = at(L); g = at(G)
ok("G1", l[0x3845B0] == "call 0x36a190" and l[0x3845B8] == "test rax, rax" and l[0x3845BB] == "je 0x3845cb" and l[0x3845C6] == "call 0x36c660" and l[0x3845DA] == "mov rax, rbx",
   "the initializer is skipped on null; the null is returned")
seg = [(a, s) for a, s in g.items() if 0x39266A < a < 0x39267E]
ok("G2", g[0x392506].startswith("mov esi, dword ptr [rip") and g[0x39252D] == "lea edi, [rsi + 1]" and g[0x392663] == "imul ebx, edi" and g[0x392666] == "add ebx, esi"
   and g[0x392668] == "mov ecx, ebx" and g[0x39266A] == "call 0x384580" and g[0x392677].startswith("mov qword ptr [rip") and g[0x39267E] == "call 0x861ec0"
   and not any(re.match(r"(test|cmp|j\w+) ", s) for a, s in seg),
   "size = nx*ny*(n+1) + n; stored at 00392677 and memset at 0039267E with nothing tested between (%d instructions)" % len(seg))
n = 0x24; c = (0x2800 - n) // (n + 1)
ok("G3", g[0x3926B5].startswith("imul eax, dword ptr [rip") and g[0x3926E9] == "add rax, rcx" and g[0x3926EC].startswith("mov qword ptr [rip") and g[0x3926F3].startswith("mov qword ptr [rip")
   and c == 275 and c * (n + 1) + n <= 0x2800 < (c + 1) * (n + 1) + n,
   "A8 = A0 + cells*n, B0 = A8 + cells; budget 275 cells: %d bytes fit, 276 would need %d" % (c * (n + 1) + n, (c + 1) * (n + 1) + n))
# M
M = body(d, 0x3912E0, 292); mm = at(M)
pre = [s for a, s in mm.items() if a < 0x39130E]
ok("M1", mm[0x39130E] == "call 0x861ec0" and mm[0x391302].startswith("mov rcx, qword ptr [rip") and mm[0x391309] == "xor edx, edx" and mm[0x3912F9].startswith("movsxd r8, dword ptr [rip")
   and not any(re.match(r"(j\w+|call) ", s) for s in pre), "memset(scratch, 0, n) is the first branch-or-call in the body")
writes = [(a, s) for a, s in mm.items() if re.match(r"(mov|or|add|and) (byte|word|dword|qword) ptr \[", s)]
ok("M2", [a for a, s in writes if "rsp" not in s] == [0x3913C4] and mm[0x3913C4] == "or byte ptr [rdx + rax - 1], cl" and mm[0x3913B1].startswith("mov rdx, qword ptr [rip")
   and mm[0x3913E8].startswith("mov rax, qword ptr [rip") and mm[0x3912F4] == "mov edi, r8d" and mm[0x3912F7] == "mov ebx, edx" and mm[0x391300] == "mov esi, ecx" and mm[0x39130B] == "mov ebp, r9d",
   "one non-stack write, the OR into the shared scratch; returns the scratch pointer; the four arguments are integers")
# M3: every function that writes through the mask pointer resets the mask first on the path that reaches the write
def resets_before_write(B):
    b = at(B); addrs = sorted(b)
    ms = [a for a in addrs if b[a] == "call 0x861ec0"]
    loads = [a for a in addrs if re.match(r"mov r\w+, qword ptr \[rip", b[a])]
    ors = [a for a in addrs if re.match(r"or byte ptr \[r\w+ \+ r\w+ - 1\], \w+", b[a])]
    if not ms or not ors: return None
    m0, w0 = ms[0], ors[0]
    early = [(a, int(re.search(r"0x(\w+)", b[a]).group(1), 16)) for a in addrs if a < m0 and re.match(r"j\w+ 0x", b[a])]
    return all(not (m0 <= t <= ors[-1]) for a, t in early) and m0 < w0, m0, ors
M3 = {0x3912E0: 292, 0x391710: 0x3919A3 - 0x391710, 0x391A30: 0x391D01 - 0x391A30}
m3 = {"%08X" % a: resets_before_write(body(d, a, n)) for a, n in M3.items()}
refs = []
for a, n in {0x391410: 0x391710 - 0x391410, 0x391D90: 0x3920D0 - 0x391D90, 0x3924B0: 607, **M3}.items():
    try: B = body(d, a, n)
    except AssertionError: B = [(x.address, x.mnemonic, x.op_str) for x in MD.disasm(d[off(a):off(a) + n], a)]
    for x, mn, op in B:
        if "rip" in op:
            # resolve rip-relative targets to find the mask pointer 02AEE0B0
            L = next(i for i in MD.disasm(d[off(x):off(x) + 15], x))
            disp = re.search(r"rip \+ 0x(\w+)\]", op)
            if disp and x + L.size + int(disp.group(1), 16) == 0x2AEE0B0: refs.append(x)
ok("M3", all(v and v[0] for v in m3.values()) and len(refs) == 13,
   "each OR writer resets first: %s; references to 02AEE0B0 found in the six bodies: %d (the cache census counts 13)"
   % ({k: (v[0], "%08X" % v[1], ["%08X" % o for o in v[2]]) for k, v in m3.items()}, len(refs)))
# C
dm = bytearray(d); dm[off(0x36C0B9) + 1 if d[off(0x36C0B9)] == 0x0F else off(0x36C0B9)] ^= 0x01; Dm = diamond(body(bytes(dm), 0x36BFE0, 261))
c1 = Dm != D0 and Dm[(0, 1, 0)] == "ret" and Dm[(0, 0, 0)] == "retry"
g2 = dict(g); g2[0x392670] = "test rax, rax"
c2 = any(re.match(r"(test|cmp|j\w+) ", s) for a, s in g2.items() if 0x39266A < a < 0x39267E)
m2 = dict(mm); m2[0x391305] = "je 0x391313"
c3 = any(re.match(r"(j\w+|call) ", s) for a, s in m2.items() if a < 0x39130E)
Bp = body(d, 0x391710, 0x3919A3 - 0x391710); Bp = [(a, "jne", "0x391870") if a == 0x39173D else (a, m, o) for a, m, o in Bp]
c4 = resets_before_write(Bp)[0] is False
ok("C", c1 and c2 and c3 and c4, "JNE->JE at 0036C0B9 flips the diamond %s; planted test seen %s; planted branch seen %s; "
   "an early jump into the OR loop past the reset fails M3 %s" % (c1, c2, c3, c4))
print("FAILS", fails); sys.exit(1 if fails else 0)
