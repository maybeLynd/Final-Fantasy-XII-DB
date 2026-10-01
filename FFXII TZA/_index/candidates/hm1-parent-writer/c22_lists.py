"""HM-1 (OPUS, 2026-09-27): who requests Fran's bind function and cut function in dgl_g0102 and rsn_z0200, where
c22_order.py found the c:3 bind and the C:22 bindh in different functions of Fran's script.

The requests go through authored REQALL lists (payload +0x30: {count; offset[count]}, each list {count; {u16 actorOrdinal,
u16 functionId}}; section-000-bytecode.md), and the actor ordinal is the script-directory index.
  L1 dgl_g0102: list 0 runs function 5 (set_start_case01, the c:3 bind) on Fran (ordinal 19) and the other party scripts;
     list 16 runs function 17 (cut_15, the C:22 bindh)
  L2 rsn_z0200: list 3 runs function 1 (the bind-on, c:3) on Fran (ordinal 20); list 5 runs function 7 (cut_00, bindh)
  L3 rsn_z0200's director '監督' requests list 3 (REQALL at pc 0x23) before list 5 (REQALL at pc 0x1F5) in one function:
     the only jump between them goes forward (0xCC -> 0x187 through the jump table) and no return lies between, so
     whenever that function runs the bind-on is REQUESTED before cut_00 (request order; execution across channels is
     not claimed)
  L4 dgl_g0102's director requests list 16 (cut_15) from its main (REQALL at pc 0x5BF); list 0 is issued by no REQALL /
     REQIALL / REQWAITALL in the map - its invoker is another mechanism, not read here
Added 2026-09-27 (OPUS, second pass) - list 0 is UNISSUED, not issued by something unseen:
  L5 the engine's only list submitter is the opcode path: 00268B10 (which reads payload +0x30) is entered only from
     00268A80, and 00268A80 only from the VM handler 0025E4C0 (00261C01); no other code resolves [payload + 0x30]
  L6 corpus control: over every us/event .ebp, all but 8 of the authored lists are named by a list opcode, with no
     decode anomaly, and dgl_g0102's lists 0 and 1 are two of the 8 - an unissued list is rare, and the decoder does
     not lose code there
  L7 no single REQ / REQEW / REQSW in dgl_g0102 targets Fran (ordinal 0x13), and the name set_start_case01 is not in the
     executable. REQ's target (003587C0) and a list's ordinal (00358940) index the same {count, ptr[]} table.
  L8 the TRIGGER route does not reach it either. The native submitters take function ids from an actor's trigger slots:
     the override word +0xC8[k] (0xFFFF = none), else element k of the script's authored table (directory entry +0x18:
     {i16 count; i16 fn[count]}), read by 002652D0 and inline. Fran's authored table in dgl_g0102 maps only kinds 1 and
     2 (to functions 1 and 2). The VM rewrites a slot only through opcode 0x34 REQCHG (handler 002615BA -> 0025AF60),
     and dgl_g0102 contains no REQCHG.
  L9 the two remaining NATIVE slot / list routes are off here as well. The case verb 0034FA70 pops a value v and, for
     modes 0-4, has 0025AD10 bind slot 0 / 7 / 10 / 14 to element v of list m+1 of the same +0x18 table (00263D40).
     Fran's lists 1-5 are empty, so the lookup returns -1, and 0025AF60 skips any value with bit 15 set. The loader-time
     list 00266C50 (payload +0x50 actor, +0x58 ids) exits at once, because dgl_g0102's +0x50 is -1.
  L10 the cross-script route is closed too. A target reaches another script's group only with bit 14 set
     (003587C0 / 0025AF60 take the group from the high word, otherwise [ctx + 0x28]). In the us corpus, every
     REQ / REQEW / REQSW with a constant target is untagged, and none with a computed target asks for function 5 or a
     computed function - EXCEPT two REQSW in evt_t0081 (pc 0x8232 / 0x8335) whose target is PUSHACT 0 and whose
     function is PUSHTAG 0 / 1. PUSHACT n (handler 00261806) pushes a TAGGED reference, (group << 16) | n | bit 14,
     with the group read from the script's reference table [ctx + 0x80] entry n +0xE; PUSHTAG takes its function from
     the same table. All 1,884 us REQCHG sites resolve to a constant, untagged target. So, apart from those two
     evt_t0081 sites (not decoded here), no static request route in the shipped us scripts runs Fran's function 5 in
     dgl_g0102.
Not claimed (after L10): the two evt_t0081 PUSHACT / PUSHTAG requests; runtime (what is drawn, which model the
second skeleton holds).
Not claimed (after L9): requests from OTHER scripts through a group-tagged target (bit 14); ids held in registers by
0025C230 / 0025C830 that are not slot reads.
Not claimed (after L8): submitters whose id is not a trigger slot (00266C50's list [rbx], 00266530's function 0 and
some register-held ids); requests from OTHER scripts through a group-tagged target (bit 14); 0025AD10's native slot
write (from 0034FA70).
Not claimed (before L8): whether a NATIVE submitter runs Fran's function 5. 003DBB60 has 11 native callers whose function ids come
from data (for example ActorStorage_InitializeRecord 00266530, 00269AD0 `movzx r8d, ax`), and they are not read here.
"""
import io, os, sys, struct
DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
f = io.open(G.VBF, "rb"); names, blocks = G.V.load_index(f)
def cstr(b, o): return b[o:b.index(b"\0", o)].decode("cp932", "replace")
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
def load(m):
    b = G.V.read_entry(f, names, blocks, "ps2data/plan_master/us/event/%s.ebp" % m)
    return b, b[0x80:0x80 + U32(b, 0x84)]
def lists(sec):
    t = U32(sec, 0x30); n = U32(sec, t); out = []
    for i in range(n):
        lo = U32(sec, t + 4 + 4 * i); c = U32(sec, lo)
        out.append([struct.unpack_from("<HH", sec, lo + 4 + 4 * k) for k in range(c)])
    return out
def scripts(sec):
    diroff = U32(sec, 0x18); n = U32(sec, diroff); npool = U32(sec, 0x4C); ents = []
    for si in range(n):
        e = diroff + 4 + si * 0x30
        nameOff, stype, pcid, start, ninstr, fnOff, listOff = struct.unpack_from("<IHHIIII", sec, e)
        ents.append(dict(si=si, start=start, name=cstr(sec, npool + nameOff), fn=fnOff, jt=listOff))
    starts = sorted({e["start"] for e in ents}); bounds = sorted(set(starts) | {diroff, len(sec)})
    for e in ents:
        end = min((x for x in bounds if x > e["start"]), default=len(sec))
        e["ins"], _ = G.decode(sec[e["start"]:end])
    return ents
def listops(ents, want):
    return [(e["si"], pc, op, imm) for e in ents for pc, op, imm in e["ins"] if op in (0x5F, 0x63, 0x61) and imm in want]

bd, sd = load("dgl_g/dgl_g0102/dgl_g0102"); Ld = lists(sd); Ed = scripts(sd)
check("L1 dgl_g0102: list 0 has (19, 5) set_start_case01; list 16 has (19, 17) cut_15", (19, 5) in Ld[0] and (19, 17) in Ld[16])
br, sr = load("rsn_z/rsn_z0200/rsn_z0200"); Lr = lists(sr); Er = scripts(sr)
check("L2 rsn_z0200: list 3 has (20, 1) the bind-on; list 5 has (20, 7) cut_00", (20, 1) in Lr[3] and (20, 7) in Lr[5])
ops_r = listops(Er, {3, 5}); d = [e for e in Er if e["si"] == 1][0]
jt = [U32(sr, d["jt"] + 4 + 4 * k) for k in range(U32(sr, d["jt"]))]
between = [(pc, op, imm) for pc, op, imm in d["ins"] if 0x23 < pc < 0x1F5]
jumps = [(pc, jt[imm]) for pc, op, imm in between if op in G.JMP_OPS]
rets = [pc for pc, op, imm in between if 0x2D <= op <= 0x31]
check("L3 rsn_z0200's director requests list 3 at 0x23 before list 5 at 0x1F5, only forward jumps between",
      (1, 0x23, 0x5F, 3) in ops_r and (1, 0x1F5, 0x5F, 5) in ops_r and d["name"] == "監督"
      and all(t > pc for pc, t in jumps) and not rets, "(jumps %s)" % [(hex(a), hex(b)) for a, b in jumps])
ops_d = listops(Ed, {0, 16})
check("L4 dgl_g0102: list 16 by the director's main (0x5BF); list 0 by no list opcode",
      (0, 0x5BF, 0x5F, 16) in ops_d and not [o for o in ops_d if o[3] == 0], str(ops_d))

# L5-L7 (second pass)
import re, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = open("Database/Tools/work/exe/FFXII_TZA.exe", "rb").read()
pe = struct.unpack_from("<I", EXE, 0x3C)[0]; nsec = struct.unpack_from("<H", EXE, pe + 6)[0]; opt = struct.unpack_from("<H", EXE, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", EXE, pe + 24 + opt + i * 40 + 8) for i in range(nsec)]
def off(v):
    for vs, va, rs, ro in SECS:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
SIZES = {}
for l in open("Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: SIZES[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(fn): return list(cs.disasm(EXE[off(fn):off(fn) + SIZES[fn]], fn))
callers = collections.defaultdict(set); p30 = []
for fn in SIZES:
    if not (0x121000 <= fn < 0x900000) or off(fn) is None: continue
    xs = dis(fn)
    for i, x in enumerate(xs):
        if x.mnemonic in ("call", "jmp") and x.op_str in ("0x268b10", "0x268a80"): callers[x.op_str].add(fn)
        if x.mnemonic == "call" and x.op_str == "0x20e600":
            for y in xs[max(0, i - 4):i]:
                if y.mnemonic == "mov" and re.match(r"ecx, dword ptr \[\w+ \+ 0x30\]$", y.op_str):
                    z = xs[i + 1:i + 3]
                    if len(z) == 2 and z[0].op_str.endswith(", eax") and z[0].mnemonic == "movsxd" and z[1].mnemonic == "add": p30.append(fn)
check("L5 lists are submitted only by the VM opcode path (00268B10 <- 00268A80 <- 0025E4C0); nothing else resolves payload +0x30",
      callers["0x268b10"] == {0x268A80} and callers["0x268a80"] == {0x25E4C0} and set(p30) <= {0x25E4C0, 0x268B10},
      "(%s; payload+0x30 resolvers %s)" % ({k: sorted("%08X" % v for v in s) for k, s in callers.items()}, sorted({"%08X" % v for v in p30})))
tot = collections.Counter(); unref = []
evn = [n for n in names if str(n).startswith("ps2data/plan_master/us/event/") and str(n).endswith(".ebp")]
for nm in evn:
    try:
        b = G.V.read_entry(f, names, blocks, nm); sec = b[0x80:0x80 + U32(b, 0x84)]
        t = U32(sec, 0x30); n = U32(sec, t); diroff = U32(sec, 0x18); ns = U32(sec, diroff)
        starts = sorted({U32(sec, diroff + 4 + si * 0x30 + 8) for si in range(ns)})
    except Exception: continue
    if n > 4096: continue
    bnd = sorted(set(starts) | {diroff, len(sec)}); ref = set()
    for s0 in starts:
        ins, a = G.decode(sec[s0:min(x for x in bnd if x > s0)])
        tot["anomaly"] += a is not None
        ref |= {imm for pc, op, imm in ins if op in (0x5F, 0x63, 0x61)}
    tot["maps"] += 1; tot["lists"] += n; un = sorted(set(range(n)) - ref); tot["unissued"] += len(un)
    if un: unref.append((nm.split("/")[-1], un))
check("L6 corpus: all but 8 authored lists are named by a list opcode, no decode anomaly; dgl_g0102's lists 0 and 1 are among the 8",
      tot["unissued"] == 8 and tot["anomaly"] == 0 and ("dgl_g0102.ebp", [0, 1]) in unref,
      "(%d maps, %d lists, %d unissued: %s)" % (tot["maps"], tot["lists"], tot["unissued"], unref))
census = os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members", "req-channel-census.tsv")
single = [l.split("\t") for l in io.open(census, encoding="utf-8") if "plan_master/us/event/dgl_g/dgl_g0102/" in l]
tg = [r[5].split(";")[1] for r in single if r[4] in ("REQ", "REQEW", "REQSW") and len(r[5].split(";")) == 3]
r358 = [(x.mnemonic, x.op_str) for x in dis(0x358940)][:6]
check("L7 no single REQ-family request in dgl_g0102 targets Fran (0x13); set_start_case01 is not an executable string; "
      "003587C0 and 00358940 index the same {count, ptr[]} table",
      tg and "PUSHII:13" not in tg and all(t.startswith("PUSHII:") for t in tg) and EXE.find(b"set_start_case") < 0
      and r358[0] == ("mov", "r8, qword ptr [rcx + 8]") and any(x.op_str == "rcx, qword ptr [rax + 8]" for x in dis(0x3587C0)),
      "(%d single requests, targets %s)" % (len(tg), sorted(set(tg))))
fran = [e for e in Ed if e["si"] == 19][0]
e19 = U32(sd, 0x18) + 4 + 19 * 0x30; trt = U32(sd, e19 + 0x18)
cnt = struct.unpack_from("<h", sd, trt)[0]; trig = [struct.unpack_from("<h", sd, trt + 2 + 2 * k)[0] for k in range(cnt)]
reqchg = [(e["si"], pc) for e in Ed for pc, op, imm in e["ins"] if op == 0x34]
h = dis(0x25E4C0); base = 0x120000
jt = [x for x in h if x.address == 0x25E5DD]
op34 = base + struct.unpack_from("<I", EXE, off(base + 0x141DF8 + 4 * 0x34))[0]
w25 = [x for x in dis(0x25AF60) if x.op_str.startswith("word ptr [rax + rbx*2 + 0xc8]")]
check("L8 Fran's authored trigger table maps only kinds 1 / 2 (to functions 1 / 2); the VM's slot writer is opcode 0x34 "
      "REQCHG (-> 0025AF60), and dgl_g0102 has no REQCHG",
      fran["name"] == "フラン" and trig == [-1, 1, 2] + [-1] * 15 and not reqchg and op34 == 0x2615BA and w25
      and any(x.address == 0x2615EB and x.op_str == "0x25af60" for x in h) and jt and "0x141df8" in jt[0].op_str,
      "(table %s; REQCHG sites %s; opcode 0x34 -> %08X)" % (trig, reqchg, op34))
p = trt; lists = []
for L in range(6):
    c = struct.unpack_from("<h", sd, p)[0]
    lists.append([struct.unpack_from("<h", sd, p + 2 + 2 * k)[0] for k in range(c)]); p += 2 + 2 * c
v34 = [(x.mnemonic, x.op_str) for x in dis(0x34FA70)]
modes = sorted({int(o.split(", ")[1], 0) for mn, o in v34 if mn == "mov" and o.startswith("r8d, ")} |
               ({0} if ("xor", "r8d, r8d") in v34 else set())) if sum(x in (("call", "0x25ad10"), ("jmp", "0x25ad10")) for x in v34) == 5 else []
g263 = [x.op_str for x in dis(0x263D40)]
guard = [x.op_str for x in dis(0x25AF60)][:8]
check("L9 the case verb 0034FA70 (modes 0-4 -> 0025AD10 -> 00263D40 list m+1) finds Fran's lists 1-5 empty (-1, skipped by "
      "0025AF60's bit-15 test); 00266C50's loader list is off (+0x50 = -1)",
      lists[0] == trig and all(L == [] for L in lists[1:6]) and sorted(modes) == [0, 1, 2, 3, 4]
      and "eax, word ptr [rcx + rdi*2 + 2]" in g263 and "r9d, 0xf" in guard
      and struct.unpack_from("<h", sd, 0x50)[0] == -1,
      "(lists 1-5 %s; modes %s; +0x50 = %d)" % (lists[1:6], sorted(modes), struct.unpack_from("<h", sd, 0x50)[0]))
tagged_const = 0; comp5 = 0; nreq = 0; pact = []
for l in io.open(census, encoding="utf-8"):
    r = l.rstrip("\n").split("\t")
    if len(r) < 6 or r[4] not in ("REQ", "REQEW", "REQSW") or "/us/" not in r[0]: continue
    a = r[5].split(";")
    if len(a) != 3: comp5 += 1; continue
    nreq += 1
    if a[1].startswith("PUSHII:"):
        tagged_const += bool(int(a[1].split(":")[1], 16) & 0x4000)
    elif a[2] == "PUSHII:5" or not a[2].startswith("PUSHII:"):
        comp5 += 1; pact.append((r[0].split("/")[-1], r[2], a[1], a[2]))
verbs = G.load_verbs(); chg = collections.Counter()
for nm in [n for n in names if "/us/" in str(n) and str(n).endswith(".ebp")]:
    try:
        b = G.V.read_entry(f, names, blocks, nm); sec = b[0x80:0x80 + U32(b, 0x84)]
        diroff = U32(sec, 0x18); ns = U32(sec, diroff)
        starts = sorted({U32(sec, diroff + 4 + si * 0x30 + 8) for si in range(ns)})
    except Exception: continue
    bnd = sorted(set(starts) | {diroff, len(sec)})
    for s0 in starts:
        ins, a_ = G.decode(sec[s0:min(x for x in bnd if x > s0)])
        for j, (pc, op, imm) in enumerate(ins):
            if op != 0x34: continue
            ar, st = G.resolve_args(ins, j, 3, verbs)
            if not ar: chg["unresolved"] += 1; continue
            tgt = ar[1]
            chg["const-untagged" if tgt[0] == "PUSHII" and not tgt[1] & 0x4000 else "other"] += 1
check("L10 no cross-script route but two named ones: us REQ-family constant targets are untagged; the only computed-target "
      "requests with a non-constant or 5 function are evt_t0081's two PUSHACT / PUSHTAG REQSW; every us REQCHG has a "
      "constant untagged target",
      nreq > 1000 and tagged_const == 0 and pact == [("evt_t0081.ebp", "8232", "PUSHACT:0", "PUSHTAG:0"), ("evt_t0081.ebp", "8335", "PUSHACT:0", "PUSHTAG:1")]
      and comp5 == 2 and chg["const-untagged"] > 1000 and chg["other"] == 0 and chg["unresolved"] == 0,
      "(%d us REQ-family sites, %d tagged, %d computed-target to fn 5 / computed fn; REQCHG %s)" % (nreq, tagged_const, comp5, dict(chg)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
