"""sd125_senders.py - SD-125: who sends the battle command dispatcher 002778C0 the message whose first parameter
reaches the bit-0x4000 test at 002795AE, and with what value (FABLE helper, Claude Opus 5.5, 2026-09-30). Static,
read-only on the image.

  P1 002778C0's message dispatch decoded (bound + byte table + dword table): id -> arm.
  P2 forward reachability of 002795AE from every message arm, with and without stopping at writes of r12 (the message
     pointer, 002778EC mov r12, rdx). The question is which arm can arrive at 002795AE with r12 still the message.
  P3 rdi at 002795AE: backward reaching definitions over the same CFG (calls preserve rdi).
  P4 image-wide census of message-31 record builds: (a) RAW .text sweep for `mov dword ptr [mem], 0x1f` (every
     occurrence of the imm32 bytes, decoded back to an instruction start that is on its owner's instruction boundary,
     unlisted code included); (b) `mov r32, 0x1f` later stored as a dword; (c) static .rdata records with first dword
     31 loaded by lea/movdq* from any listed or .pdata function. Controls: the same instrument finds id 30's known
     send 00278CE8, id 33's 0027AA70 (UQ-68 W6), and the static {18} record 00915070 (protocol page section 8).
  P5 for each message-31 site: the call that consumes the record, its receiver and the first-parameter (+8) source.
  P6 00279E20 (the 0x61F0-byte controller): dispatch decoded; which arm holds its message-31 send 0027A5D3; every
     image-wide write of displacement 0x61B8 (the word that send passes).
  P7 what kind 1 is: 0027E050's table (indexed kind - 1) entry 0 stores list code 6 at +0x4C0.
  P8 the consumer: 00276D30's arm that tests bit 0x4000 and what the forced flag gates.
Exit 1 on any FAIL.
"""
import os, sys, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "takebacks"))
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM

FAILS = 0
def check(name, ok, detail=""):
    global FAILS
    if not ok: FAILS += 1
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  " + detail) if detail else ""))

BASE = tk.BASE
ALIAS = {"rax": {"rax", "eax", "ax", "al"}, "rbx": {"rbx", "ebx", "bx", "bl"}, "rcx": {"rcx", "ecx", "cx", "cl"},
         "rdx": {"rdx", "edx", "dx", "dl"}, "rsi": {"rsi", "esi", "si", "sil"}, "rdi": {"rdi", "edi", "di", "dil"},
         "rbp": {"rbp", "ebp", "bp", "bpl"}}
for n in range(8, 16): ALIAS["r%d" % n] = {"r%d" % n, "r%dd" % n, "r%dw" % n, "r%db" % n}
CALLEE_SAVED = {"rbx", "rbp", "rdi", "rsi", "r12", "r13", "r14", "r15"}
NONWRITE = ("cmp", "test", "bt", "push", "jmp", "ucomiss", "comiss", "nop")

def writes(x, reg):
    if x.mnemonic == "call": return reg not in CALLEE_SAVED
    if x.mnemonic.startswith("j") or x.mnemonic.startswith(NONWRITE) or x.mnemonic == "ret": return False
    if x.mnemonic == "xchg": return any(p.strip() in ALIAS[reg] for p in x.op_str.split(","))
    if not x.operands or x.operands[0].type != X86_OP_REG: return False
    return x.reg_name(x.operands[0].reg) in ALIAS[reg]

def jump_table(body, i):
    """targets of the indirect jmp at body[i]: bound from the preceding `cmp e?x, N` / `ja`, optional byte map."""
    bound = btab = dtab = None
    for k in range(i - 1, max(i - 14, -1), -1):
        y = body[k]
        if y.mnemonic == "mov" and "*4 +" in y.op_str and "dword ptr" in y.op_str and dtab is None:
            dtab = BASE + int(y.op_str.rsplit("+", 1)[1].strip(" ]"), 16)
        elif y.mnemonic == "movzx" and "byte ptr" in y.op_str and "+ rax +" in y.op_str and btab is None:
            btab = BASE + int(y.op_str.rsplit("+", 1)[1].strip(" ]"), 16)
        elif y.mnemonic == "cmp" and y.operands[1].type == X86_OP_IMM and bound is None:
            bound = y.operands[1].imm
            break
    if dtab is None or bound is None: return [], None
    if btab is not None:
        bmap = [tk.d[tk.off(btab) + j] for j in range(bound + 1)]
        n = max(bmap) + 1
    else:
        bmap = None; n = bound + 1
    tg = [tk.u32(dtab + 4 * j) + BASE for j in range(n)]
    return tg, (bmap, dtab, btab, bound)

def cfg(fn, size):
    body = tk.dis(fn, fn + size); by = {x.address: i for i, x in enumerate(body)}
    succ = {x.address: [] for x in body}; tables = {}
    for i, x in enumerate(body):
        m = x.mnemonic; nxt = body[i + 1].address if i + 1 < len(body) else None
        if m.startswith("j"):
            if x.op_str.startswith("0x"):
                t = int(x.op_str, 16)
                if t in succ: succ[x.address].append(t)
            elif m == "jmp":
                tg, info = jump_table(body, i)
                tables[x.address] = (tg, info)
                succ[x.address].extend(t for t in tg if t in succ)
            if m != "jmp" and nxt: succ[x.address].append(nxt)
        elif m in ("ret", "int3"): pass
        elif nxt: succ[x.address].append(nxt)
    pred = {a: set() for a in succ}
    for a, ss in succ.items():
        for s in ss: pred[s].add(a)
    return body, by, succ, pred, tables

def reach(succ, by, body, start, target, kill_reg=None):
    seen = {start}; st = [start]
    while st:
        a = st.pop()
        if a == target: return True
        if kill_reg and a != start and writes(body[by[a]], kill_reg): continue
        if kill_reg and a == start and writes(body[by[a]], kill_reg): continue
        for s in succ[a]:
            if s not in seen: seen.add(s); st.append(s)
    return False

def reaching_defs(pred, by, body, site, reg):
    defs = set(); seen = set(); st = [site]
    while st:
        a = st.pop()
        for p in pred.get(a, ()):
            if p in seen: continue
            seen.add(p)
            if writes(body[by[p]], reg): defs.add(p); continue
            st.append(p)
    return defs

def msg_dispatch(fn, size, jmp_addr):
    body, by, succ, pred, tables = cfg(fn, size)
    tg, (bmap, dtab, btab, bound) = tables[jmp_addr]
    default = None
    for x in body:
        if x.address < jmp_addr and x.mnemonic == "ja" and x.op_str.startswith("0x"): default = int(x.op_str, 16)
    arms = {}
    for idx in range(bound + 1):
        t = tg[bmap[idx]] if bmap else tg[idx]
        if t != default: arms.setdefault(t, []).append(idx + 1)
    return body, by, succ, pred, tables, arms, default

# ---------------------------------------------------------------- P1/P2/P3
F = 0x002778C0; FS = tk.fsize(F)
body, by, succ, pred, tables, arms, default = msg_dispatch(F, FS, 0x00277923)
idarm = {i: a for a, ids in arms.items() for i in ids}
print("P1 002778C0 (%d B) arms: %s ; default %08X" % (FS, ", ".join("%s->%08X" % ("/".join(map(str, ids)), a) for a, ids in sorted(arms.items(), key=lambda t: t[1][0])), default))
check("P1 002778C0 answers 1,2,4,10,11,12,15,18,30,31,32,35,44,45 (OPUS's SD-126 table); 2 -> 00278A3B, 31 -> 00279187",
      sorted(idarm) == [1, 2, 4, 10, 11, 12, 15, 18, 30, 31, 32, 35, 44, 45] and idarm[2] == 0x00278A3B and idarm[31] == 0x00279187)
SITE = 0x002795AE
plain = {i: reach(succ, by, body, a, SITE) for i, a in idarm.items()}
kept = {i: reach(succ, by, body, a, SITE, "r12") for i, a in idarm.items()}
print("P2 arms reaching 002795AE at all: %s ; with r12 unredefined: %s" % ([i for i in sorted(plain) if plain[i]], [i for i in sorted(kept) if kept[i]]))
check("P2 only message 31's arm reaches 002795AE with r12 still the message pointer", [i for i in sorted(kept) if kept[i]] == [31])
r12defs = reaching_defs(pred, by, body, SITE, "r12")
print("    r12 definitions reaching 002795AE: %s" % ", ".join("%08X %s %s" % (a, body[by[a]].mnemonic, body[by[a]].op_str) for a in sorted(r12defs)))
for i in sorted(plain):
    if plain[i] and not kept[i]:
        print("    arm %d (%08X) reaches 002795AE only through an r12 write" % (i, idarm[i]))
rdidefs = reaching_defs(pred, by, body, SITE, "rdi")
print("    rdi definitions reaching 002795AE: %s" % ", ".join("%08X %s %s" % (a, body[by[a]].mnemonic, body[by[a]].op_str) for a in sorted(rdidefs)))
# rdi on the arm-31 path alone: forward from 00279187 killing rdi writes, then ask whether 002795AE is reachable
# without passing a write after 002791A7
check("P3 on arm 31, rdi = 1 from 002791A7 reaches 002795AE with no further rdi write",
      body[by[0x002791A7]].op_str == "edi, 1" and reach(succ, by, body, 0x002791AC, SITE, "rdi") and reach(succ, by, body, 0x002791AC, SITE, "r12"))
x = body[by[0x002791A1]]
check("P3 arm 31 stores the first parameter's low word as the window kind: 002791A1 movzx eax, word [r12+8] / 002791AC mov [rsi+0xd8], ax",
      x.op_str == "eax, word ptr [r12 + 8]" and body[by[0x002791AC]].op_str == "word ptr [rsi + 0xd8], ax")
x1, x2, x3 = body[by[0x002795AE]], body[by[0x002795B5]], body[by[0x002795C2]]
check("P3 002795AE cmp qword [r12+8], rdi ; 002795B5 or [r15+0x2ff0], 0x4000 ; 002795C2 and ... 0xffffbfff",
      x1.op_str == "qword ptr [r12 + 8], rdi" and x2.op_str == "dword ptr [r15 + 0x2ff0], 0x4000" and x3.op_str.endswith("0xffffbfff"))
x = body[by[0x002778EF]]
check("P3 r15 = [rcx+0xd0] (002778EF), the parent menu widget the id-1 arm stores (00277925-00277931)",
      x.op_str == "r15, qword ptr [rcx + 0xd0]" and body[by[0x00277931]].op_str == "qword ptr [rsi + 0xd0], rax")

# ---------------------------------------------------------------- P4 census
TXT = tk.d[tk.TRO:tk.TRO + min(tk.TVS, tk.TRS)]
def raw_id_sites(mid):
    pat = struct.pack("<I", mid); out = {}; regsrc = {}
    p = TXT.find(pat)
    while p >= 0:
        va = tk.TVA + p
        for back in range(1, 11):
            s = va - back
            xx = tk._decode_at(s)
            if xx is None or xx.address + xx.size != va + 4: continue
            if xx.mnemonic != "mov" or len(xx.operands) != 2 or xx.operands[1].type != X86_OP_IMM or xx.operands[1].imm != mid: continue
            b = tk.boundaries(s)
            if b is not None and s not in b: continue
            if xx.operands[0].type == X86_OP_MEM and xx.operands[0].size == 4:
                out[s] = xx
            elif xx.operands[0].type == X86_OP_REG and xx.operands[0].size == 4:
                regsrc[s] = xx
        p = TXT.find(pat, p + 1)
    return out, regsrc

def owner_decode(a):
    o, how = tk.owner(a)
    if o is None: return None
    end = o + tk.fsize(o) if how == "listed" else tk.pdata[__import__("bisect").bisect_right(tk.pstarts, a) - 1][1]
    return tk.dis(o, end)

def reg_store_sites(regsrc):
    """`mov r32, imm` followed within 6 instructions by `mov dword ptr [mem], r32` (no intervening write)."""
    out = {}
    for s, xx in regsrc.items():
        ins = owner_decode(s)
        if not ins: continue
        idx = [k for k, y in enumerate(ins) if y.address == s]
        if not idx: continue
        r = xx.reg_name(xx.operands[0].reg); full = [k for k, v in ALIAS.items() if r in v]
        for y in ins[idx[0] + 1: idx[0] + 7]:
            if y.mnemonic == "mov" and len(y.operands) == 2 and y.operands[0].type == X86_OP_MEM and y.operands[1].type == X86_OP_REG \
                    and y.reg_name(y.operands[1].reg) == r and y.operands[0].size == 4:
                out[y.address] = y; break
            if full and writes(y, full[0]): break
    return out

# static records: decode every listed function once, collect rip loads of .rdata whose first dword is a message id
ALLINS = None
def all_rip_loads():
    global ALLINS
    if ALLINS is not None: return ALLINS
    ALLINS = []
    RD = tk.secs[".rdata"]
    for e, sz in tk.flist:
        if sz <= 0 or sz > 0x40000 or tk.sec_of(e) != ".text": continue
        try: ins = tk.dis(e, e + sz)
        except Exception: continue
        for y in ins:
            if y.mnemonic not in ("lea", "movdqa", "movdqu", "movups", "movaps"): continue
            for op in y.operands:
                if op.type == X86_OP_MEM and op.mem.base != 0 and y.reg_name(op.mem.base) == "rip":
                    t = y.address + y.size + op.mem.disp
                    if RD[0] <= t < RD[0] + RD[1]: ALLINS.append((e, y, t))
    return ALLINS

def static_sites(mid):
    out = []
    for e, y, t in all_rip_loads():
        v = tk.u32(t)
        if v == mid and y.mnemonic == "lea" and y.op_str.startswith("rdx"):
            out.append((e, y, t))
    return out

sites31, reg31 = raw_id_sites(31); rs31 = reg_store_sites(reg31); st31 = static_sites(31)
sites30, reg30 = raw_id_sites(30)
sites33, reg33 = raw_id_sites(33); rs33 = reg_store_sites(reg33); st33 = static_sites(33)
st18 = static_sites(18)
print("P4 id 31: %d immediate dword stores, %d register-sourced stores, %d static rdx-records" % (len(sites31), len(rs31), len(st31)))
KNOWN31 = {0x00277C9B, 0x00278030, 0x00278212, 0x00278882, 0x00278F80, 0x0027A5D3}
check("P4 control: the census finds the six id-31 builds already read (002778C0 x5, 00279E20 0027A5D3)", KNOWN31 <= set(sites31),
      "missing %s" % sorted("%08X" % a for a in KNOWN31 - set(sites31)))
check("P4 control: id 30 census finds 00278CE8 (the protocol page's 002778C0 send)", 0x00278CE8 in sites30)
check("P4 control: static-record shape finds {18} at 00915070 (protocol page section 8)", any(t == 0x00915070 for _, _, t in st18))

# ---------------------------------------------------------------- P5 payloads
def xmm_src(ins, j):
    """the 16-byte constant or zero behind the xmm0 stored at ins[j]"""
    for y in reversed(ins[max(0, j - 12):j]):
        if y.mnemonic == "xorps" and y.op_str == "xmm0, xmm0": return "zero"
        if y.mnemonic in ("movdqa", "movdqu", "movaps", "movups") and y.op_str.startswith("xmm0, xmmword ptr [rip"):
            t = y.address + y.size + y.operands[1].mem.disp
            return "%08X=%s" % (t, struct.unpack_from("<4I", tk.d, tk.off(t)))
    return "?"

def consumer(a, mid):
    """from the id store at a: the instruction path to the first call after it (following one direct jmp), the
    receiver, and the +8 writers ON THAT PATH in execution order (the last one is what the receiver reads)."""
    ins = owner_decode(a)
    k = [i for i, y in enumerate(ins) if y.address == a][0]
    st = ins[k]; mem = st.operands[0].mem
    base = st.reg_name(mem.base); disp = mem.disp
    path = list(range(max(0, k - 16), k + 1))      # the straight-line lead-in (same block shape at every site read)
    call = None; i = k + 1; steps = 0; followed = False
    while i < len(ins) and steps < 26:
        y = ins[i]; steps += 1; path.append(i)
        if y.mnemonic == "call": call = y; break
        if y.mnemonic == "jmp" and y.op_str.startswith("0x") and not followed:
            t = int(y.op_str, 16); kk = [n for n, z in enumerate(ins) if z.address == t]
            if not kk: break
            i = kk[0]; followed = True; continue
        if y.mnemonic == "ret": break
        i += 1
    p8 = []
    for n in path:
        y = ins[n]
        if y.operands and y.operands[0].type == X86_OP_MEM and y.mnemonic.startswith("mov")                 and y.reg_name(y.operands[0].mem.base) == base and y.operands[0].mem.disp == disp + 8:
            p8.append((y, xmm_src(ins, n) if y.op_str.endswith("xmm0") else None))
    src = None
    if p8:
        last, xs = p8[-1]
        if xs is None and len(last.operands) == 2 and last.operands[1].type == X86_OP_REG:
            r = last.reg_name(last.operands[1].reg); full = [kk for kk, v in ALIAS.items() if r in v]
            jj = [n for n, y in enumerate(ins) if y.address == last.address][0]
            for y in reversed(ins[max(0, jj - 30):jj]):
                if full and writes(y, full[0]) and y.mnemonic != "call": src = y; break
    rcx = None
    if call is not None:
        cpath = path[:-1]
        for n in reversed(cpath[-12:]):
            y = ins[n]
            if writes(y, "rcx") and y.mnemonic != "call": rcx = y; break
    return st, call, p8, src, rcx

def fmt(y): return "-" if y is None else "%08X %s %s" % (y.address, y.mnemonic, y.op_str)
def p8s(p8): return " | ".join(fmt(y) + ((" <- " + xs) if xs else "") for y, xs in p8) or "-"
print("P5 id-31 builds and their consumers:")
info31 = {}
for a in sorted(set(sites31) | set(rs31)):
    st, call, p8, src, rcx = consumer(a, 31); info31[a] = (st, call, p8, src, rcx)
    print("    %s  in %s" % (fmt(st), tk.fname(a)))
    print("        call %s ; receiver %s" % (fmt(call), fmt(rcx)))
    print("        +8: %s ; register source %s" % (p8s(p8), fmt(src)))
for e, y, t in st31:
    print("    static record %08X = %s  lea %s in %s" % (t, struct.unpack_from("<6I", tk.d, tk.off(t)), fmt(y), tk.fname(y.address)))
RES = (0x00277C9B, 0x00278030, 0x00278212, 0x00278F80)
check("P5 re-sends of the current kind: 00277C9B, 00278030, 00278212, 00278F80 pass movsx word [rsi+0xd8] to the dispatcher's own handler",
      all(info31[a][3] is not None and info31[a][3].op_str == "rax, word ptr [rsi + 0xd8]" for a in RES)
      and all(info31[a][4] is not None and info31[a][4].op_str == "rcx, rsi" for a in RES))
b2 = body[by[0x00278860]]; f1 = body[by[0x002785F0]]; f0 = body[by[0x00278559]]; f00 = body[by[0x00278423]]
check("P5 00278882's payload rcx has two sources: the back path 00278860 mov eax, [rdx+rax*4+0x70] (the saved kind) and the forward path 002785F0 -> 00278870 with rcx = 0027C3D0's result (00278423 store, 00278559 reload)",
      b2.op_str == "eax, dword ptr [rdx + rax*4 + 0x70]" and f1.op_str == "0x278870" and f0.op_str == "rcx, dword ptr [rbp - 0x39]"
      and f00.op_str == "dword ptr [rbp - 0x39], eax" and body[by[0x0027887E]].op_str == "qword ptr [rbp - 1], rcx"
      and 0x00278860 in pred[0x00278866] | {0x00278860} and 0x002785F0 in pred[0x00278870])
st, call, p8, src, rcx = info31[0x0027A5D3]
check("P5 00279E20 sends {31, (i64)word[controller+0x61B8], [child+0x2FE0]} through the subtree broadcast 002753F0 to the menu child it just built (rcx = rdi)",
      call is not None and call.address == 0x0027A5DA and call.op_str == "0x2753f0" and rcx is not None and rcx.op_str == "rcx, rdi"
      and any(y.address == 0x0027A5C2 for y, _ in p8),
      "call %s receiver %s +8 %s" % (fmt(call), fmt(rcx), p8s(p8)))
x = tk.dis(0x0027A5B6, 0x0027A5C6)
check("P5 the 0027A5D3 payload is 0027A5B6 movsx rax, word [rbx+0x61b8] -> 0027A5C2 mov [rbp-0x38], rax",
      x[0].op_str == "rax, word ptr [rbx + 0x61b8]" and x[2].op_str == "qword ptr [rbp - 0x38], rax")
FOREIGN1 = (0x002BB7C4, 0x002BBA0B); FOREIGN0 = (0x003CA245, 0x00551E32, 0x00551F3D, 0x005541CD)
def has_pay(a, want):
    return bool(info31[a][2]) and (info31[a][2][-1][1] or "").startswith(want)
check("P5 foreign {31, 1} builds: only 002BAF80's two (the location-map page) load the payload from 00915BB0 = (1, 0, 0, 0); both send UP their own parent chain (00275440)",
      all(has_pay(a, "00915BB0=(1, 0, 0, 0)") and info31[a][1] is not None and info31[a][1].op_str == "0x275440" for a in FOREIGN1),
      "; ".join("%08X %s call %s rcx %s" % (a, tk.fname(a), fmt(info31[a][1]), fmt(info31[a][4])) for a in FOREIGN1))
check("P5 foreign {31, 0} builds (003CA200, 00551E00, 00551F00, and 00553F40 - whose record still holds {34, 1} at 005541BC but the shared tail 0055423A zeroes +8 before the send 00554249) carry a zeroed payload",
      all(has_pay(a, "zero") for a in FOREIGN0) and info31[0x005541CD][1].address == 0x00554249)
up = tk.dis(0x00275440, 0x00275484)
check("P5 00275440 delivers to the ancestors only: starts at [rcx+0x10] and follows +0x10 (00275452, 00275470)",
      any(y.address == 0x00275452 and y.op_str == "rbx, qword ptr [rcx + 0x10]" for y in up) and any(y.address == 0x00275470 and y.op_str == "rbx, qword ptr [rbx + 0x10]" for y in up))
check("P5 the 002BAF80 sender object is that procedure's own widget (002BAFC4 mov r14, rcx)", tk.dis(0x002BAFC4, 0x002BAFC7)[0].op_str == "r14, rcx")
others = sorted(a for a in set(sites31) | set(rs31) if a not in KNOWN31 and a not in FOREIGN1 and a not in FOREIGN0)
print("    id-31 immediates not classified above: %s" % (", ".join("%08X (%s) %s" % (a, tk.fname(a), fmt(info31[a][0])) for a in others) or "none"))

# ---------------------------------------------------------------- P5b sensitivity: the earlier record's arm-2 path
def unbounded(dtab):
    out = []
    for e in range(64):
        t = tk.u32(dtab + 4 * e)
        if t is None: break
        t += BASE
        if t not in by: break
        out.append(t)
    return out
ub = unbounded(0x00279DE4)
tg_b = tables[0x00278D86][0]
succ2 = {a: list(v) for a, v in succ.items()}
succ2[0x00278D86] = [t for t in ub if t in succ2]
arm2_ub = reach(succ2, by, body, 0x00278A3B, SITE)
arm2_ub_rdi = reaching_defs({a: set() for a in succ2}, by, body, SITE, "rdi")
pred2 = {a: set() for a in succ2}
for a, ss in succ2.items():
    for s_ in ss: pred2[s_].add(a)
rdi2 = reaching_defs(pred2, by, body, SITE, "rdi")
print("P5b table at 00278D86: bounded (cmp eax, 7) %d entries; read until a target leaves the function: %d entries %s" % (len(tg_b), len(ub), ["%08X" % t for t in ub[len(tg_b):]]))
check("P5b sensitivity: the unbounded read runs into the next table 00279E04 (whose targets 0027956B.. flow to 002795AE), and with those edges arm 2 reaches 002795AE and 00278A5B becomes an rdi definition - the earlier record's 'arm 2' path is that artefact",
      len(tg_b) == 8 and len(ub) > 8 and arm2_ub and 0x00278A5B in rdi2 and not plain[2],
      "rdi defs unbounded: %s" % ", ".join("%08X" % a for a in sorted(rdi2)))

# ---------------------------------------------------------------- P6 controller
C = 0x00279E20; CS = tk.fsize(C)
cb, cby, csucc, cpred, ctables, carms, cdef = msg_dispatch(C, CS, 0x00279E76)
cid = {i: a for a, ids in carms.items() for i in ids}
print("P6 00279E20 (%d B) arms: %s" % (CS, ", ".join("%d->%08X" % (i, cid[i]) for i in sorted(cid))))
holders = [i for i in sorted(cid) if reach(csucc, cby, cb, cid[i], 0x0027A5D3)]
check("P6 the controller's {31} send 0027A5D3 is reached from its message-2 arm only (GENERATION RECONCILE)", holders == [2], "holders %s" % holders)
def disp_sites(v, width_bytes=2):
    """raw sweep of .text for the disp32 value v, decoded back to an instruction start on its owner's boundary
    (tk.disp_refs leaves 66h-prefixed word accesses unverified, so this verifies them itself)"""
    out = {}
    pat = struct.pack("<I", v); p = TXT.find(pat)
    while p >= 0:
        va = tk.TVA + p
        for back in range(1, 13):
            xx = tk._decode_at(va - back)
            if xx is None or not (xx.address < va and xx.address + xx.size >= va + 4): continue
            if not any(op.type == X86_OP_MEM and (op.mem.disp & 0xFFFFFFFF) == v and op.mem.base != 0 and xx.reg_name(op.mem.base) != "rip" for op in xx.operands): continue
            b = tk.boundaries(xx.address)
            if b is not None and xx.address not in b: continue
            out[xx.address] = xx
        p = TXT.find(pat, p + 1)
    return out
s61 = disp_sites(0x61B8)
w61 = {a: x for a, x in s61.items() if x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith("mov")}
print("    displacement 0x61B8: %d sites; writes: %s" % (len(s61), "; ".join("%s in %s" % (fmt(x), tk.fname(a)) for a, x in sorted(w61.items()))))
check("P6 control: the 0x61B8 sweep finds the read 0027A5B6 that feeds the send", 0x0027A5B6 in s61)
check("P6 the word has three writers: 00276650 at 0027670D (the controller's builder), the controller's message-33 arm at 0027A793 (<- 0027A78E movzx eax, word [r14+8], the message's first parameter) and its message-2 arm at 0027A6F0",
      set(w61) == {0x0027670D, 0x0027A6F0, 0x0027A793} and cid.get(33) == 0x0027A78E and tk.dis(0x0027A78E, 0x0027A793)[0].op_str == "eax, word ptr [r14 + 8]",
      "writers %s" % ["%08X" % a for a in sorted(w61)])
bb, bby, bsucc, bpred, _ = cfg(0x00276650, tk.fsize(0x00276650))
r14d = reaching_defs(bpred, bby, bb, 0x0027670D, "r14"); ebx = reaching_defs(bpred, bby, bb, 0x002766A3, "rbx")
check("P6 00276650 builds the controller with +0x61B8 = 1: r14 at 0027670D is 002766A3 lea r14d, [rbx+1] only, and rbx there is 0027666B xor ebx, ebx only",
      r14d == {0x002766A3} and ebx == {0x0027666B}, "r14 defs %s, rbx defs %s" % (["%08X" % a for a in r14d], ["%08X" % a for a in ebx]))
rsi_d = reaching_defs(cpred, cby, cb, 0x0027A6F0, "rsi")
check("P6 the message-2 arm zeroes the word after the open: 0027A6F0 is reached from the send 0027A5DA, and rsi there is 0027A058 xor esi, esi only",
      rsi_d == {0x0027A058} and reach(csucc, cby, cb, 0x0027A5DA, 0x0027A6F0), "rsi defs %s" % ["%08X" % a for a in rsi_d])

# ---------------------------------------------------------------- P4b id 33
print("P4b id 33 builds: %d immediate, %d register-sourced, %d static" % (len(sites33), len(rs33), len(st33)))
info33 = {}
for a in sorted(set(sites33) | set(rs33)):
    st, call, p8, src, rcx = consumer(a, 33); info33[a] = (st, call, p8, src, rcx)
    print("    %s in %s ; call %s ; receiver %s ; +8 %s ; reg source %s" % (fmt(st), tk.fname(a), fmt(call), fmt(rcx), p8s(p8), fmt(src)))
check("P4b control: id 33 census finds 0027AA70's two sends", sum(1 for a in info33 if tk.owner(a)[0] == 0x0027AA70) == 2)
check("P4b 0027AA70 sends {33, 1} (00915BB0) at 0027AB88 up its parent chain",
      (info33[0x0027AB88][2][-1][1] or "").startswith("00915BB0=(1, 0, 0, 0)") and info33[0x0027AB88][1].op_str == "0x275440")
check("P4b the dispatcher reports the kind it opened to its ancestors: 002788C0 {33} via 00275440, +8 = the same rcx the 31-send carried (0027887E / 002788CD)",
      info33[0x002788C0][1].op_str == "0x275440" and any(y.address == 0x002788CD and y.op_str == "qword ptr [rbp - 1], rcx" for y, _ in info33[0x002788C0][2]))

# ---------------------------------------------------------------- P6b where the {33, 1} senders sit
x = tk.dis(0x0027A369, 0x0027A370)[0]
check("P6b the controller builds a 0x4A0-byte child with handler 0027AA70 in its child slot +0xC0 + i*0x3010 (0027A369-0027A392) and attaches it under itself (0027A3B7, parent rbx)",
      x.op_str == "r8, [rip + 0x700]" and tk.dis(0x0027A376, 0x0027A37B)[0].op_str == "edx, 0x4a0" and tk.dis(0x0027A392, 0x0027A397)[0].op_str == "0x245000"
      and tk.dis(0x0027A3AB, 0x0027A3AE)[0].op_str == "rcx, rbx" and tk.dis(0x0027A3B7, 0x0027A3BC)[0].op_str == "0x244960")
hold_aa = [i for i in sorted(cid) if reach(csucc, cby, cb, cid[i], 0x0027A392)]
print("    controller arms reaching the 0027AA70 build: %s" % hold_aa)
AA = 0x0027AA70; AAS = tk.fsize(AA)
aab, aaby, aasucc, aapred, _ = cfg(AA, AAS)
first_id = [y for y in aab[:40] if y.op_str.endswith("dword ptr [rdx]")]
print("    0027AA70 (%d B) loads the id at %s" % (AAS, fmt(first_id[0]) if first_id else "?"))
for site in (0x0027AB88, 0x0027AC65):
    print("    0027AA70 {33, 1} build %08X reachable from entry: %s" % (site, reach(aasucc, aaby, aab, AA, site)))
x2 = tk.dis(0x0027B474, 0x0027B47E)
check("P6b 0027B430 sends {33, 0027C730's result} up from rdi (0027B474 call 0027C730 -> 0027B47B movsxd rbp, eax -> 0027B4EF +8 = rbp -> 0027B4F4 00275440); rdi carries the dispatcher's +0xD8 (0027B483)",
      x2[0].op_str == "0x27c730" and x2[2].op_str == "rbp, eax" and tk.dis(0x0027B4EF, 0x0027B4F4)[0].op_str == "qword ptr [rsp + 0x30], rbp"
      and tk.dis(0x0027B483, 0x0027B48A)[0].op_str == "edx, word ptr [rdi + 0xd8]")

# ---------------------------------------------------------------- P9 the dispatcher's subtree: attach census
def raw_calls(targets):
    out = []
    for i in range(len(TXT) - 5):
        b = TXT[i]
        if b in (0xE8, 0xE9): ln, k = 5, 1
        elif b == 0x0F and 0x80 <= TXT[i + 1] <= 0x8F: ln, k = 6, 2
        else: continue
        if i + ln > len(TXT): continue
        rel = struct.unpack_from("<i", TXT, i + k)[0]
        va = tk.TVA + i; t = va + ln + rel
        if t in targets:
            bb = tk.boundaries(va)
            out.append((va, t, bb is not None and va in bb))
    return out
att = raw_calls({0x00244960, 0x00248220})
onb = [(a, t) for a, t, ok in att if ok]
print("P9 raw rel32 index (E8/E9/0F8x) to the attach entries 00244960 / 00248220: %d hits, %d on an instruction boundary" % (len(att), len(onb)))
for a, t in onb:
    o = tk.owner(a)[0]
    if o in (0x002778C0, 0x0027AD70, 0x00276D30, 0x00279E20, 0x002B9D30):
        ins = owner_decode(a); j = [i for i, y in enumerate(ins) if y.address == a][0]
        rc = next((y for y in reversed(ins[max(0, j - 10):j]) if writes(y, "rcx") and y.mnemonic != "call"), None)
        rd = next((y for y in reversed(ins[max(0, j - 10):j]) if writes(y, "rdx") and y.mnemonic != "call"), None)
        print("    %08X -> %08X in %s ; parent %s ; child %s" % (a, t, tk.fname(a), fmt(rc), fmt(rd)))
check("P9 control: the index finds 00276DF1 (menu attaches the dispatcher), 0027A568 (controller attaches the menu) and 002B9F6A",
      {0x00276DF1, 0x0027A568, 0x002B9F6A} <= set(a for a, _ in onb))
in_disp = [a for a, _ in onb if tk.owner(a)[0] == 0x002778C0]
in_win = [a for a, _ in onb if tk.owner(a)[0] == 0x0027AD70]
check("P9 the dispatcher attaches only its two 0027AD70 windows (00277A25 / 00277A34, children rsi+0xF0 / rsi+0x1710), and each window attaches only its 002D14E0 list (0027AEC3)",
      in_disp == [0x00277A25, 0x00277A34] and in_win == [0x0027AEC3], "002778C0 %s, 0027AD70 %s" % (["%08X" % a for a in in_disp], ["%08X" % a for a in in_win]))

# ---------------------------------------------------------------- P7 kind 1
kt = tk.u32(0x0027E384) + BASE
seg = tk.dis(kt, kt + 0x30)
code = None
for y in seg:
    if y.mnemonic == "mov" and "+ 0x4c0]" in y.op_str and y.operands[1].type == X86_OP_IMM:
        code = y.operands[1].imm; break
    if y.mnemonic.startswith("j") or y.mnemonic == "ret": break
print("P7 0027E050 table 0027E384[0] (kind 1; index kind - 1 at 0027E06B) -> %08X: %s" % (kt, " ; ".join("%s %s" % (y.mnemonic, y.op_str) for y in seg[:4])))
check("P7 kind 1 stores list code 6 (the top command list: Attack, Magicks & Technicks, Mist, Dismiss, Gambits, Items per UQ-68 W9) at +0x4C0",
      code == 6 and tk.dis(0x0027E06B, 0x0027E06E)[0].op_str == "eax, [rdx - 1]")
x = tk.dis(0x00278BA6, 0x00278BAB)[0]; x0 = body[by[0x00278B9F]]
check("P7 +0xD8 is the kind the window is sized from: 00278B9F movsx edx, word [rsi+0xd8] -> 00278BA6 call 0027DED0", x0.op_str == "edx, word ptr [rsi + 0xd8]" and x.op_str == "0x27ded0")

# ---------------------------------------------------------------- P8 consumer
seg = tk.dis(0x00276FA0, 0x00277068)
ops = {y.address: (y.mnemonic, y.op_str) for y in seg}
check("P8 00276D30: 00276FD8 test [rdi+0x2ff0], 0x4000 / 00276FF2 cmovne r14d, r15d(=1) over 00253BA0's result / 00277031 test r14d -> 0027704E or +0x2ff0, 0x200 -> 0027705B call 00244F00",
      ops.get(0x00276FD8) == ("test", "dword ptr [rdi + 0x2ff0], 0x4000") and ops.get(0x00276FF2) == ("cmovne", "r14d, r15d")
      and ops.get(0x00276FD3) == ("call", "0x253ba0") and ops.get(0x00276FE2) == ("mov", "r14d, eax")
      and ops.get(0x00277031) == ("test", "r14d, r14d"))
check("P8 r14d = 0 goes straight to the close (00277034 je 0027704E); r14d != 0 closes only when bit 17 is clear and edx (00277036-00277047) or r15d (member record byte & 9, 00277022-0027702E) - else 0027704C je 00277067 (no close)",
      ops.get(0x00277034) == ("je", "0x27704e") and ops.get(0x00277042) == ("cmovae", "eax, edx") and ops.get(0x00277047) == ("jne", "0x27704e")
      and ops.get(0x00277027) == ("test", "byte ptr [r12], 9") and ops.get(0x0027704C) == ("je", "0x277067"))
_, _, _, _, t2, a2, df2 = msg_dispatch(0x00276D30, tk.fsize(0x00276D30), 0x00276D83)
id2 = {i: a for a, ids in a2.items() for i in ids}
print("P8 00276D30 arms: %s" % ", ".join("%d->%08X" % (i, id2[i]) for i in sorted(id2)))
check("P8 the 0x4000 test sits in 00276D30's message-2 arm (GENERATION RECONCILE, sent every frame by 00248030)", id2.get(2) == 0x00276FA0)
print("FAILS %d" % FAILS)
sys.exit(1 if FAILS else 0)
