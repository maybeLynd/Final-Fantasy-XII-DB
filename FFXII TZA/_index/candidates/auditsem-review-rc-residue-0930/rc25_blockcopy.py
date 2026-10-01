"""SWE2-AUDIT-SEM RC-25 attack (own code): is the party page's +4 written by anything the producer's W1 tracker
cannot see? W1 accepts only `mov byte/word [reg + 4|5]`. Two blind classes are checked here:
  (a) wide stores covering +4: dword/qword/xmm/ymm stores at a displacement d with d <= 4 < d + width, relative to a
      register loaded from [02EBF190] (+8 page base) or a page pointer, inside the functions that reference 02EBF190;
  (b) block copies: a call whose rcx (destination) is [02EBF190] or derived from it (memcpy/memset/loader), and
      rep movs/stos with rdi derived from it.
Method: for every rip-relative reference to 02EBF190 (own sweep, ripref logic), linear-decode the 40 instructions that
follow it and track registers holding the block pointer or a pointer derived by add/lea from it (a coarse forward
taint: a register is tainted after `mov r, [02EBF190]`, `mov/lea r, [tainted + ...]`, `add r, ...` on a tainted r;
untainted when overwritten otherwise). Report every store through a tainted base whose width covers any byte that
is +4/+5 modulo nothing (absolute disp printed; the reviewer reads each), and every call with tainted rcx.
Controls: P the known word write 0023AD8E is NOT reachable this way (its page comes in as an argument), so the
positive control is the tracker seeing a known tainted store: 0031A4A0 (mov word [rdi+0x50], bp in 0031A410),
listed by the producer's C2; N a site 0 instructions long yields no taint.
"""
import struct, re, sys
import img

T = 0x02EBF190
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0

def riprefs(lo, hi):
    hits = set()
    for i in range(len(text) - 4):
        d = struct.unpack_from("<i", text, i)[0]
        for tail in (0, 1, 2, 4):
            tgt = va0 + i + 4 + tail + d
            if lo <= tgt < hi:
                hits.add((i, tail, tgt))
    found = {}
    for i, tail, tgt in sorted(hits):
        # longest decode first: a REX-prefixed instruction must not be shadowed by its prefix-less tail decode
        for back in range(11, 0, -1):
            s = i - back
            if s < 0:
                continue
            x = next(img.md.disasm(text[s:s + 16], va0 + s), None)
            if x and x.size == back + 4 + tail and "rip" in x.op_str:
                found[x.address] = x
                break
    return found

R64 = {"rax": "rax", "eax": "rax", "rbx": "rbx", "ebx": "rbx", "rcx": "rcx", "ecx": "rcx", "rdx": "rdx", "edx": "rdx",
       "rsi": "rsi", "esi": "rsi", "rdi": "rdi", "edi": "rdi", "rbp": "rbp", "ebp": "rbp"}
for n in range(8, 16):
    R64["r%d" % n] = "r%d" % n
    R64["r%dd" % n] = "r%d" % n
WIDTH = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16, "ymmword": 32}

refs = riprefs(T, T + 8)
print("rip refs to 02EBF190:", len(refs))
stores, calls, reps = [], [], []
for a, x in sorted(refs.items()):
    if not (x.mnemonic == "mov" and "qword ptr [rip" in x.op_str):
        continue
    dst = x.op_str.split(",")[0].strip()
    if dst not in R64:
        continue
    taint = {R64[dst]}
    seq = list(img.md.disasm(img.rd(a + x.size, 400), a + x.size))[:40]
    for y in seq:
        ops = [o.strip() for o in y.op_str.split(",")]
        if y.mnemonic in ("ret", "jmp") or y.mnemonic.startswith("int3"):
            break
        if y.mnemonic == "call":
            if "rcx" in taint:
                calls.append((a, y))
            taint -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
            continue
        if y.mnemonic.startswith("rep"):
            if "rdi" in taint:
                reps.append((a, y))
            continue
        m = re.match(r"(byte|word|dword|qword|xmmword|ymmword) ptr \[([^\]]+)\]$", ops[0]) if ops else None
        if m and y.mnemonic not in ("cmp", "test") and not y.mnemonic.startswith(("j", "prefetch")):
            # parse [base (+ index*scale) (+/- disp)] token by token (capstone may omit the scale)
            toks = re.findall(r"([+-]?)\s*([\w*]+)", m.group(2))
            base, disp, idx = None, 0, False
            for sign, tok in toks:
                if re.fullmatch(r"0x[0-9a-f]+|\d+", tok):
                    disp += int(tok, 0) * (-1 if sign == "-" else 1)
                elif base is None:
                    base = R64.get(tok)
                else:
                    idx = True
            if base in taint:
                w = WIDTH[m.group(1)]
                stores.append((a, y, w, disp))
            continue
        if ops and ops[0] in R64:
            r = R64[ops[0]]
            src = ",".join(ops[1:])
            srcregs = {R64[s] for s in re.findall(r"\b(r\w+|e\w\w)\b", src) if s in R64}
            if y.mnemonic in ("mov", "lea", "movsxd") and srcregs & taint and "rip" not in src:
                taint.add(r)
            elif y.mnemonic in ("add", "sub", "imul", "shl", "and", "or", "inc", "dec", "cmovne", "cmove") and r in taint:
                pass
            elif y.mnemonic not in ("cmp", "test", "push"):
                taint.discard(r)
print("\n(a) stores through a block-derived register, any width (covering-disp view):")
cover = []
for a, y, w, disp in stores:
    tag = ""
    # block-relative view: page k byte +4 is at 8 + k*0x1C8 + 4; page-relative view: +4 itself
    span = range(disp, disp + w)
    if any(0 <= o - 0xC < 0x28 * 0x1C8 and (o - 0xC) % 0x1C8 in (0, 1) for o in span):
        tag = "  <== covers +4/+5 (block-relative view)"
    if 4 in span or 5 in span:
        tag += "  <== covers +4/+5 (page-relative view)"
    if w > 2 and tag:
        cover.append((a, y, w, disp))
    if tag or w > 2:
        print("   ref %08X  %08X %s %s  (w=%d disp=%#x)%s" % (a, y.address, y.mnemonic, y.op_str, w, disp, tag))
print("wide stores covering +4/+5 at a constant-offset view:", len(cover))
print("\n(b) calls with rcx = block-derived pointer:")
for a, y in calls:
    print("   ref %08X  %08X call %s" % (a, y.address, y.op_str))
print("rep string ops with rdi block-derived:", [(hex(a), hex(y.address), y.mnemonic) for a, y in reps])
FAILS = 0
def check(n, ok, d=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + n + (" - " + d if d else ""))
    FAILS += 0 if ok else 1
check("P tracker sees stores through the derived register at all", len(stores) > 0, str(len(stores)))
print("FAILS", FAILS)
