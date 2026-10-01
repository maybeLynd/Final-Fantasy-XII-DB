"""tt_indep.py - SWE2-AUDIT-SPEC independent re-derivation for ASTRA-REQ-SPEC-TITLE-TRACKER-CALLBACK-0930 (2026-09-30).

Written without the packet's checker or captures: pefile (its own exception-directory parser) + capstone over the
certified image (sha256 asserted). Canonical VAs include the image base 0x120000.

  A  00189120: the 8 bytes, the decode, the rip target, no .pdata row, no RCX use; where its cell 01F7F598 lies
  B  00183720 (52 B): full decode, both getter calls, the single NULL test and the arguments to 00185A90
  C  00185A90 (86 B): queue geometry, the unsigned compare, the store order, every call on every path (own CFG)
  D  0017ECC0 (27 B): RCX to 005DE250 and the tail to 0019C590
  E  001FB660: .pdata rows and .xdata (pefile parse AND a raw parse), chain targets, own entry CFG to 001FB71B,
     every store in the body, the argument set-up at each call
  F  references overlapping the qword cell 01F7F598 (rip / image-base-relative / absolute); writer list only
"""
import hashlib, struct
import numpy as np
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM, CS_OP_IMM
from capstone.x86 import X86_REG_RIP, X86_REG_INVALID

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "image hash mismatch"
pe = pefile.PE(data=raw, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
assert IB == 0x120000
SECS = [(s.Name.rstrip(b"\0").decode(), IB + s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData,
         bool(s.Characteristics & 0x20000000)) for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
FAILS = []
M32 = 0xFFFFFFFF


def off(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def rd(va, n):
    o = off(va)
    return raw[o:o + n]


def dis(a, b):
    return list(md.disasm(rd(a, b - a), a))


def say(*a):
    print(*a)


def check(cond, what):
    say(("PASS " if cond else "FAIL ") + what)
    if not cond:
        FAILS.append(what)


def riptgt(i):
    for op in i.operands:
        if op.type == CS_OP_MEM and op.mem.base == X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def body(a, b):
    L = dis(a, b)
    check(sum(i.size for i in L) == b - a, "decode %08X..%08X: %d B, %d instructions" % (a, b, b - a, len(L)))
    return {i.address: i for i in L}


def want(M, pc, mn, ops):
    i = M.get(pc)
    got = (i.mnemonic, i.op_str) if i else None
    check(got == (mn, ops), "%08X %s %s%s" % (pc, mn, ops, "" if got == (mn, ops) else "   got %r" % (got,)))


def cfg(M, entry):
    """own recursive descent: returns (reached pcs, rets, calls, tails, unresolved)"""
    todo, seen, rets, calls, tails, unres = [entry], set(), [], [], [], []
    while todo:
        a = todo.pop()
        if a in seen:
            continue
        if a not in M:
            unres.append(a)
            continue
        seen.add(a)
        i = M[a]
        if i.mnemonic == "ret":
            rets.append(a)
            continue
        if i.mnemonic == "call":
            calls.append((a, i.op_str))
        if i.mnemonic == "jmp":
            if i.operands[0].type == CS_OP_IMM and i.operands[0].imm in M:
                todo.append(i.operands[0].imm)
            else:
                tails.append((a, i.op_str))
            continue
        if i.mnemonic.startswith("j"):
            todo.append(i.operands[0].imm)
        todo.append(a + i.size)
    return seen, sorted(rets), sorted(calls), tails, unres


PD = []
for n, v, vs, p, rs, x in SECS:
    if n == ".pdata":
        blob = raw[p:p + min(vs, rs)]
        for k in range(0, len(blob) - 11, 12):
            a, b, u = struct.unpack_from("<III", blob, k)
            if a:
                PD.append((a + IB, b + IB, u + IB))


def pdrow(pc):
    return [r for r in PD if r[0] <= pc < r[1]]


say("== A. 00189120")
g = rd(0x189120, 8)
say("  bytes %s" % g.hex())
check(g == bytes.fromhex("488b057164df01c3"), "00189120 is 8 bytes 48 8B 05 71 64 DF 01 C3")
G = body(0x189120, 0x189128)
want(G, 0x189127, "ret", "")
check(riptgt(G[0x189120]) == 0x1F7F598 and G[0x189120].op_str.startswith("rax, qword ptr [rip"),
      "00189120 mov rax, qword [rip+..] -> 01F7F598, then ret: no register input is read (RCX ignored)")
check(pdrow(0x189120) == [], "00189120 has no .pdata row (a leaf)")
d = [s for s in SECS if s[0] == ".data"][0]
check(d[1] + d[4] <= 0x1F7F598 < d[1] + d[2], ".data raw ends at %08X: 01F7F598 is in the zero-initialised virtual tail"
      " (no file value; any non-NULL context is written at run time)" % (d[1] + d[4]))

say("\n== B. 00183720")
check(pdrow(0x183720) == [(0x183720, 0x183754, pdrow(0x183720)[0][2])], ".pdata 00183720..00183754 (52 B)")
H = body(0x183720, 0x183754)
for pc, mn, ops in [(0x183720, "test", "rcx, rcx"), (0x183723, "je", "0x183753"), (0x18372A, "mov", "rbx, rcx"),
                    (0x18372D, "call", "0x189120"), (0x183732, "test", "rax, rax"), (0x183735, "je", "0x18374e"),
                    (0x183737, "call", "0x189120"), (0x18373C, "mov", "rcx, rax"), (0x183746, "mov", "r8, rbx"),
                    (0x183749, "call", "0x185a90"), (0x18374E, "add", "rsp, 0x20"), (0x183753, "ret", "")]:
    want(H, pc, mn, ops)
check(riptgt(H[0x18373F]) == 0x17ECC0 and H[0x18373F].op_str.startswith("rdx,"), "0018373F lea rdx -> 0017ECC0")
tests = [a for a, i in H.items() if i.mnemonic == "test"]
check(tests == [0x183720, 0x183732], "exactly two tests: the argument (183720) and the FIRST context (183732);"
      " the second getter result at 183737 goes to rcx untested")
S, R, C, T, U = cfg(H, 0x183720)
check(len(S) == len(H) and R == [0x183753] and not U, "183720 CFG covers all %d instructions, single ret 183753" % len(H))

say("\n== C. 00185A90")
check([r[:2] for r in pdrow(0x185A90)] == [(0x185A90, 0x185AE6)], ".pdata 00185A90..00185AE6 (86 B)")
Q = body(0x185A90, 0x185AE6)
for pc, mn, ops in [(0x185A94, "movsxd", "rax, dword ptr [rcx + 0xcb8]"), (0x185A9B, "add", "rcx, 0xc38"),
                    (0x185AA2, "shl", "rax, 5"), (0x185AA6, "add", "rcx, rax"),
                    (0x185AA9, "mov", "qword ptr [rsp + 0x20], rdx"), (0x185AAE, "mov", "qword ptr [rsp + 0x28], r8"),
                    (0x185AB3, "mov", "rdx, qword ptr [rcx + 8]"), (0x185AB7, "cmp", "rdx, qword ptr [rcx + 0x10]"),
                    (0x185ABB, "jae", "0x185ad7"), (0x185ABD, "lea", "rax, [rdx + 0x10]"),
                    (0x185AC1, "mov", "qword ptr [rcx + 8], rax"), (0x185AC5, "test", "rdx, rdx"),
                    (0x185AC8, "je", "0x185ae1"), (0x185ACA, "movups", "xmm0, xmmword ptr [rsp + 0x20]"),
                    (0x185ACF, "movups", "xmmword ptr [rdx], xmm0"), (0x185AD2, "add", "rsp, 0x38"),
                    (0x185AD6, "ret", ""), (0x185AD7, "lea", "r8, [rsp + 0x20]"), (0x185ADC, "call", "0x1858a0"),
                    (0x185AE5, "ret", "")]:
    want(Q, pc, mn, ops)
S, R, C, T, U = cfg(Q, 0x185A90)
check(len(S) == len(Q) and R == [0x185AD6, 0x185AE5] and C == [(0x185ADC, "0x1858a0")] and not T and not U,
      "185A90 CFG: all %d instructions reached, two rets, ONE call (185ADC -> 1858A0, on the jae arm only)" % len(Q))
cmps = [(a, i.mnemonic, i.op_str) for a, i in Q.items() if i.mnemonic in ("cmp", "test")]
check(cmps == [(0x185AB7, "cmp", "rdx, qword ptr [rcx + 0x10]"), (0x185AC5, "test", "rdx, rdx")],
      "the only compares are cursor-vs-end and cursor NULL: nothing tests the index dword [ctx+0xCB8]")
check(Q[0x185AC1].address < Q[0x185ACF].address, "store order: cursor+16 to queue+8 (185AC1) precedes the 16-byte"
      " pair copy (185ACF)")
say("  slow arm: rcx = queue, rdx = old cursor (185AB3, unchanged on the jae path), r8 = &pair at rsp+0x20")
check(Q[0x185ABB].mnemonic == "jae", "cursor<end is an UNSIGNED compare (jae)")

say("\n== D. 0017ECC0")
check([r[:2] for r in pdrow(0x17ECC0)] == [(0x17ECC0, 0x17ECDB)], ".pdata 0017ECC0..0017ECDB (27 B)")
K = body(0x17ECC0, 0x17ECDB)
for pc, mn, ops in [(0x17ECC6, "mov", "rbx, rcx"), (0x17ECC9, "call", "0x5de250"), (0x17ECCE, "mov", "rcx, rbx"),
                    (0x17ECD5, "pop", "rbx"), (0x17ECD6, "jmp", "0x19c590")]:
    want(K, pc, mn, ops)
check(not any("rcx" in i.op_str for a, i in K.items() if a < 0x17ECC9 and a != 0x17ECC6),
      "rcx reaches 005DE250 unchanged (only read at 17ECC6 before the call)")

say("\n== E. 001FB660 unwind fragments and entry CFG")
rows = [r for r in PD if 0x1FB660 <= r[0] < 0x1FB71C]
for r in rows:
    say("  .pdata %08X..%08X unwind %08X" % r)
check([r[:2] for r in rows] == [(0x1FB660, 0x1FB6B7), (0x1FB6B7, 0x1FB6F1), (0x1FB6F1, 0x1FB71C)],
      "three RUNTIME_FUNCTION rows 1FB660..1FB6B7 (87 B), ..1FB6F1 (58 B), ..1FB71C (43 B) = 188 B")
check(not pdrow(0x1FB65F) or pdrow(0x1FB65F)[0][1] <= 0x1FB660, "no row straddles the entry")
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXCEPTION"]])
PX = {e.struct.BeginAddress + IB: e for e in pe.DIRECTORY_ENTRY_EXCEPTION}
root = rows[0]
for r in rows:
    u = PX[r[0]].unwindinfo
    codes = [str(c) for c in u.UnwindCodes]
    h = rd(r[2], 4)
    flags, cnt = h[0] >> 3, h[2]
    csize = 4 + 2 * ((cnt + 1) & ~1)
    chained = struct.unpack_from("<III", rd(r[2] + csize, 12)) if flags & 4 else None
    ch = tuple(x + IB for x in chained) if chained else None
    say("  %08X: pefile Version %d Flags %d prolog %d codes %s; raw flags %d count %d chained %s"
        % (r[0], u.Version, u.Flags, u.SizeOfProlog, codes, flags, cnt,
           "(%08X,%08X,%08X)" % ch if ch else None))
    if r is root:
        check(u.Flags == 0 and not u.UNW_FLAG_CHAININFO, "root 1FB660 unwind is unchained, no handler")
    else:
        check(u.UNW_FLAG_CHAININFO and u.FunctionEntry + IB == 0x1FB660 and ch == root,
              "%08X chains to the exact root row (1FB660,1FB6B7,%08X)" % (r[0], root[2]))
B = body(0x1FB660, 0x1FB71C)
S, R, C, T, U = cfg(B, 0x1FB660)
check(len(S) == 52 and len(S) == len(B) and R == [0x1FB71B] and not T and not U,
      "entry CFG reaches all %d of %d instructions (188 B), single ret 1FB71B, no tail, no exit" % (len(S), len(B)))
say("  calls: %s" % ", ".join("%08X->%s" % c for c in C))
check([c[1] for c in C] == ["0x183720", "0x183720", "0x16d6d0", "0x1af2b0", "qword ptr [rax + 0x18]"],
      "five call sites: 183720 x2, 16D6D0, 1AF2B0, and one indirect [rax+0x18]")
for pc, mn, ops in [(0x1FB674, "mov", "rdi, rcx"), (0x1FB677, "mov", "rcx, qword ptr [rcx]"),
                    (0x1FB67A, "call", "0x183720"), (0x1FB687, "xor", "ebp, ebp"), (0x1FB689, "mov", "qword ptr [rdi], rbp"),
                    (0x1FB67F, "mov", "rbx, qword ptr [rdi + 0x18]"), (0x1FB683, "lea", "rsi, [rdi + 0x10]"),
                    (0x1FB68C, "cmp", "rbx, rsi"), (0x1FB691, "mov", "rcx, qword ptr [rbx + 0x28]"),
                    (0x1FB695, "call", "0x183720"), (0x1FB69D, "mov", "qword ptr [rbx + 0x28], rbp"),
                    (0x1FB6A1, "call", "0x16d6d0"), (0x1FB6A9, "cmp", "rax, rsi"), (0x1FB6AC, "jne", "0x1fb691"),
                    (0x1FB6AE, "mov", "rsi, qword ptr [rdi + 0x20]"), (0x1FB6C0, "mov", "rdx, qword ptr [rsi]"),
                    (0x1FB6C3, "lea", "rcx, [rdi + 8]"), (0x1FB6C7, "call", "0x1af2b0"),
                    (0x1FB6CC, "mov", "rax, qword ptr [rdi + 0x38]"), (0x1FB6D0, "lea", "rcx, [rdi + 0x38]"),
                    (0x1FB6D4, "mov", "rbx, qword ptr [rsi + 8]"), (0x1FB6D8, "mov", "r8d, 0x30"),
                    (0x1FB6DE, "mov", "rdx, rsi"), (0x1FB6E1, "call", "qword ptr [rax + 0x18]"),
                    (0x1FB6E4, "mov", "rsi, rbx"), (0x1FB6EA, "jne", "0x1fb6c0"),
                    (0x1FB6F6, "lea", "rax, [rdi + 0x10]"), (0x1FB6FF, "mov", "qword ptr [rdi + 0x20], rbp"),
                    (0x1FB703, "mov", "byte ptr [rdi + 0x28], bpl"), (0x1FB707, "mov", "dword ptr [rdi + 0x30], ebp"),
                    (0x1FB70F, "mov", "qword ptr [rax], rax"), (0x1FB712, "mov", "qword ptr [rdi + 0x18], rax")]:
    want(B, pc, mn, ops)
stores = []
for a in sorted(B):
    i = B[a]
    if i.mnemonic in ("mov", "movups", "movaps") and i.operands and i.operands[0].type == CS_OP_MEM:
        stores.append("%08X %s" % (a, i.op_str))
say("  every store in the body:")
for s in stores:
    say("    " + s)
nonstack = [s for s in stores if "rsp" not in s]
check(len(nonstack) == 7, "7 non-stack stores: [rdi]=0, [node+0x28]=0, and the five normal-return resets")
check(0x1FB6D4 < 0x1FB6E1 and 0x1FB6C7 < 0x1FB6D4, "next link [rsi+8] is loaded after the 1AF2B0 call and before"
      " the indirect call")

say("\n== F. references overlapping the qword cell 01F7F598")
CELL, CEND = 0x1F7F598, 0x1F7F5A0
hits = {}
for n, v, vs, p, rs, x in SECS:
    if not x:
        continue
    blob = raw[p:p + min(vs, rs)]
    b = np.frombuffer(blob, dtype=np.uint8).astype(np.int64)
    u = b[:-3] | (b[1:-2] << 8) | (b[2:-1] << 16) | (b[3:] << 24)
    dd = np.where(u >= 1 << 31, u - (1 << 32), u)
    pos = np.arange(len(dd), dtype=np.int64)
    near = np.zeros(len(dd), dtype=bool)
    for t in (0, 1, 2, 4):
        tg = v + pos + 4 + t + dd
        near |= (tg >= CELL - 16) & (tg < CEND)
    near |= (dd >= CELL - 16 - IB) & (dd < CEND - IB)
    near |= ((dd & M32) >= CELL - 16) & ((dd & M32) < CEND)
    for o in np.nonzero(near)[0].tolist():
        d0 = int(dd[o])
        for st in range(max(0, o - 11), o):
            i = next(md.disasm(blob[st:st + 15], v + st, count=1), None)
            if not i or st + i.size < o + 4:
                continue
            for op in i.operands:
                if op.type != CS_OP_MEM:
                    continue
                m = op.mem
                if m.base == X86_REG_RIP:
                    t, form = i.address + i.size + m.disp, "rip"
                elif m.base != X86_REG_INVALID and m.disp == d0 and CELL - 16 - IB <= d0 < CEND - IB:
                    t, form = IB + m.disp, "imagebase"
                elif m.base == X86_REG_INVALID and m.index == X86_REG_INVALID:
                    t, form = m.disp & M32, "abs"
                else:
                    continue
                if t < CEND and t + op.size > CELL:
                    wr = i.operands[0].type == CS_OP_MEM and i.mnemonic not in ("cmp", "test")
                    hits[i.address] = (i.mnemonic, i.op_str, form, op.size, wr, t, i.size)
inner = [a for a in hits if any(b < a < b + hits[b][6] for b in hits)]
for a in inner:
    del hits[a]
say("  dropped %d decodes that start inside another hit (prefix-skipped duplicates): %s" % (len(inner), ["%08X" % a for a in sorted(inner)]))
misal = []
for a in list(hits):
    r = pdrow(a)
    if r and a not in {i.address for i in dis(r[0][0], a + 16)}:
        misal.append(a)
        del hits[a]
say("  dropped %d hits that are not instruction boundaries when decoded from their .pdata row start: %s"
    % (len(misal), ["%08X" % a for a in sorted(misal)]))
say("  hits with no .pdata row (alignment unverified): %s" % ["%08X" % a for a in sorted(hits) if not pdrow(a)])
w = [(a, h) for a, h in sorted(hits.items()) if h[4]]
say("  overlapping instructions %d, of which destination-memory (writes) %d:" % (len(hits), len(w)))
for a, h in w:
    say("    %08X %s %s  (%s, width %d at %08X)" % (a, h[0], h[1], h[2], h[3], h[5]))
check(0x189120 in hits, "known positive: the getter 00189120 read is found")
say("  (writers listed only; which runs first, and whether the context is stable across 183720's two reads, is"
    " run-time state this list cannot settle)")

say("\nFAILS %d" % len(FAILS))
for f in FAILS:
    say("  " + f)
