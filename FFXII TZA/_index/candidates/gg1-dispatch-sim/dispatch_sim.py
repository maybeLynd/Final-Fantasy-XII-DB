"""dispatch_sim.py - a widget proc's message dispatch, found by running its head once per message id (FABLE, Claude Opus
5.5, 2026-09-28). Library + self-test; used by gg1_sim.py.

A proc reads the message id with `mov R, dword ptr [rdx]` and branches on it: compare trees (cmp / sub / dec / test and
conditional jumps) and MSVC jump tables (`movzx E, byte [base + R + btab]`, `mov E, dword [base + E*4 + dtab]`,
`add rcx, base`, `jmp rcx`). run(f, m) executes only those instructions, with the id register holding m and flags from
the last flag-setting one, and returns the address where control leaves the dispatch: the first instruction that is not
a dispatch instruction. That address is the start of message m's arm.
"""
import re, struct, collections
CACHE = r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt"
EXE = r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe"
FAM = {}
for q, d, w, b in (("rax", "eax", "ax", "al"), ("rbx", "ebx", "bx", "bl"), ("rcx", "ecx", "cx", "cl"), ("rdx", "edx", "dx", "dl"),
                   ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"), ("rbp", "ebp", "bp", "bpl")):
    for n in (q, d, w, b): FAM[n] = q
for k in range(8, 16):
    for n in ("r%d" % k, "r%dd" % k, "r%dw" % k, "r%db" % k): FAM[n] = "r%d" % k
_d = None; _secs = None; body = None; idx = None
def load(cache=CACHE, exe=EXE):
    global _d, _secs, body, idx
    _d = open(exe, "rb").read()
    pe = struct.unpack_from("<I", _d, 0x3c)[0]; nsec = struct.unpack_from("<H", _d, pe + 6)[0]; opt = struct.unpack_from("<H", _d, pe + 20)[0]
    _secs = []; o = pe + 24 + opt
    for i in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", _d, o + 8); _secs.append((va, rs, ra)); o += 40
    body = collections.defaultdict(list)
    for line in open(cache, encoding="utf-8", errors="replace"):
        p = line.rstrip("\n").split(None, 2)
        if len(p) == 3: body[p[1]].append((int(p[0], 16), p[2].split(" ;")[0].strip()))
    for f in body: body[f].sort()
    idx = {f: {a: i for i, (a, s) in enumerate(ins)} for f, ins in body.items()}
def rd(va, n):
    r = va - 0x120000
    for sva, rs, ra in _secs:
        if sva <= r < sva + rs: return _d[ra + r - sva: ra + r - sva + n]
IMM = r"(-?0x[0-9a-f]+|\d+)"
def head(f, limit=80):
    """index of the `mov R, dword ptr [rdx]` that loads the message id, and R's family"""
    alias = {"rdx"}                                   # the message pointer arrives in rdx; follow 64-bit copies of it
    for i, (a, s) in enumerate(body[f][:limit]):
        m = re.match(r"mov (\w+), dword ptr \[(\w+)\]$", s)
        if m and m.group(2) in alias: return i, FAM.get(m.group(1))
        m = re.match(r"mov (r\w+), (r\w+)$", s)
        if m and m.group(2) in alias: alias.add(m.group(1)); continue
        if s.startswith("call"): alias &= {"rbx", "rsi", "rdi", "rbp", "r12", "r13", "r14", "r15"}
        m = re.match(r"\w+ (\w+),", s)
        if m and FAM.get(m.group(1)) in alias and not s.startswith(("cmp", "test")): alias.discard(FAM.get(m.group(1)))
    return None, None
def run(f, m, steps=200):
    i0, R = head(f)
    if i0 is None: return None
    ins = body[f]; ix = idx[f]; regs = {R: m & 0xFFFFFFFF}; base = None; flags = None; i = i0 + 1
    landing = ins[i][0] if i < len(ins) else None   # where control arrived after the last branch decision
    for _ in range(steps):
        if i >= len(ins): return landing
        a, s = ins[i]
        mn, ops = (s.split(None, 1) + [""])[:2]; parts = [x.strip() for x in ops.split(",")]
        dst = FAM.get(parts[0]) if parts else None
        def val(x):
            x = x.strip()
            if re.fullmatch(IMM, x): return int(x, 0) & 0xFFFFFFFF
            return regs.get(FAM.get(x))
        if mn in ("cmp", "sub", "add") and dst in regs and len(parts) == 2 and val(parts[1]) is not None:
            x, y = regs[dst], val(parts[1])
            r = (x - y) & 0xFFFFFFFF if mn != "add" else (x + y) & 0xFFFFFFFF
            flags = (r, x, y, mn)
            if mn != "cmp": regs[dst] = r
            i += 1; continue
        if mn in ("dec", "inc") and dst in regs:
            x = regs[dst]; r = (x - 1 if mn == "dec" else x + 1) & 0xFFFFFFFF; regs[dst] = r; flags = (r, x, 1, "sub" if mn == "dec" else "add"); i += 1; continue
        if mn == "test" and dst in regs and len(parts) == 2 and FAM.get(parts[1]) == dst:
            flags = (regs[dst], regs[dst], 0, "test"); i += 1; continue
        if mn in ("cdqe", "movsxd") or (mn == "mov" and dst and len(parts) == 2 and FAM.get(parts[1]) in regs and "[" not in parts[1]):
            if mn == "cdqe": regs["rax"] = regs.get("rax")
            else:
                src = regs.get(FAM.get(parts[1]))
                if src is None: return landing
                regs[dst] = src
            i += 1; continue
        mm = re.match(r"lea (\w+), \[(\w+) ([+-]) (0x[0-9a-f]+|\d+)\]$", s)
        if mm and FAM.get(mm.group(2)) in regs:              # lea eax, [rcx - 1]: arithmetic on the id, no flags
            k = int(mm.group(4), 0); regs[FAM[mm.group(1)]] = (regs[FAM[mm.group(2)]] + (k if mm.group(3) == "+" else -k)) & 0xFFFFFFFF
            i += 1; continue
        mm = re.match(r"lea (\w+), \[rip [+-] 0x[0-9a-f]+\]$", s)
        if mm and i + 1 < len(ins):
            # the image-base anchor of a jump table (lea r8, [rip - N] = 00120000)
            nxt = ins[i + 1][0]; disp = int(s.split("rip ")[1].split("]")[0].replace(" ", ""), 16) if "+" in s else -int(s.split("- ")[1].split("]")[0], 16)
            if nxt + disp == 0x120000: regs[FAM[mm.group(1)]] = 0x120000; base = FAM[mm.group(1)]; i += 1; continue
        mm = re.match(r"movzx (\w+), byte ptr \[(\w+) \+ (\w+) \+ (0x[0-9a-f]+)\]$", s)
        if mm and base and FAM.get(mm.group(2)) == base and FAM.get(mm.group(3)) in regs:
            regs[FAM[mm.group(1)]] = rd(0x120000 + int(mm.group(4), 16) + regs[FAM[mm.group(3)]], 1)[0]; i += 1; continue
        mm = re.match(r"mov (\w+), dword ptr \[(\w+) \+ (\w+)\*4 \+ (0x[0-9a-f]+)\]$", s)
        if mm and base and FAM.get(mm.group(2)) == base and FAM.get(mm.group(3)) in regs:
            regs[FAM[mm.group(1)]] = struct.unpack("<I", rd(0x120000 + int(mm.group(4), 16) + 4 * regs[FAM[mm.group(3)]], 4))[0]; i += 1; continue
        if mn == "add" and dst in regs and len(parts) == 2 and FAM.get(parts[1]) == base:
            regs[dst] = (regs[dst] + 0x120000) & 0xFFFFFFFFFFFF; i += 1; continue
        mm = re.match(r"jmp (\w+)$", s)
        if mm and FAM.get(mm.group(1)) in regs:
            t = regs[FAM[mm.group(1)]]; landing = t
            if t not in ix: return t
            i = ix[t]; continue
        mm = re.match(r"(j\w+) 0x([0-9a-f]+)$", s)
        if mm:
            t = int(mm.group(2), 16); cc = mm.group(1)
            if cc == "jmp": take = True
            else:
                if flags is None: return landing
                r, x, y, op = flags; sr = (r >> 31) & 1
                zf = r == 0; cf = (x < y) if op in ("sub", "cmp") else (False if op == "test" else (x + y) > 0xFFFFFFFF)
                of = ((((x ^ y) & (x ^ r)) >> 31) & 1) if op in ("sub", "cmp") else 0
                take = {"je": zf, "jz": zf, "jne": not zf, "jnz": not zf, "ja": not cf and not zf, "jae": not cf, "jnb": not cf,
                        "jb": cf, "jc": cf, "jbe": cf or zf, "jg": not zf and sr == of, "jge": sr == of, "jl": sr != of,
                        "jle": zf or sr != of, "js": sr == 1, "jns": sr == 0}.get(cc)
                if take is None: return landing
            if take:
                landing = t
                if t not in ix: return t
                i = ix[t]
            else:
                i += 1; landing = ins[i][0] if i < len(ins) else None
            continue
        # anything else ends the dispatch if it writes a tracked register, calls, returns or jumps through memory;
        # otherwise it is neutral (a store, or a move into an untracked register) and runs on. A neutral instruction
        # that sets flags makes the next conditional jump part of the arm, not of the dispatch.
        srcs = [FAM.get(t) for t in re.findall(r"\b(\w+)\b", ",".join(parts[1:]) if len(parts) > 1 else "")]
        zeroing = len(parts) == 2 and mn in ("xor", "sub") and parts[0] == parts[1]     # xor eax, eax reads nothing
        if not zeroing and any(x in regs and x != base for x in srcs) and landing is not None and a == landing:
            return None                                   # an unmodelled instruction reads the id right at the landing: incomplete
        if mn in ("call", "ret", "jmp") or (dst in regs) or mn.startswith("j"): return landing
        if mn in ("xor", "and", "or", "test", "cmp", "sub", "add", "inc", "dec", "neg", "shl", "shr", "sar", "bt", "comiss", "ucomiss"):
            flags = None
        i += 1
    return landing
def arms(f, ids=range(0, 64)):
    return {m: run(f, m) for m in ids}
if __name__ == "__main__":
    load()
    fails = 0
    def ok(tag, cond, msg):
        global fails
        print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
    a = arms("002778C0"); ok("T1", a[1] == 0x00277925 and a[10] == a[11] == 0x00277A64, "002778C0 (jump table): 1 -> %s, 10/11 -> %s/%s" % (hex(a[1] or 0), hex(a[10] or 0), hex(a[11] or 0)))
    a = arms("0023B6F0"); ok("T2", (a[1], a[4], a[10], a[12], a[13]) == (0x0023BA11, 0x0023B8EA, 0x0023B818, 0x0023B7E7, 0x0023B73E), "0023B6F0 (sub/je chain): %s" % {k: hex(a[k] or 0) for k in (1, 4, 10, 12, 13)})
    a = arms("003CAB00"); ok("T3", a[31] == 0x003CAC6A and a[1] == 0x003CAB54, "003CAB00 (dec + byte/dword table): 31 -> %s, 1 -> %s" % (hex(a[31] or 0), hex(a[1] or 0)))
    a = arms("002284F0"); ok("T4", (a[1], a[2], a[10], a[18], a[3]) == (0x00228641, 0x00228599, 0x0022854C, 0x00228524, 0x00228517), "002284F0 (sub/cmp chain): %s" % {k: hex(a[k] or 0) for k in (1, 2, 10, 18, 3)})
    print("FAILS", fails)
