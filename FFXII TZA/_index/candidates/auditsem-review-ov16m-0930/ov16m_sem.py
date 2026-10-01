"""SWE2-AUDIT-SEM: semantic review of FABLE's OV-16 narrowing (61600dc24): 00268EA0 files talkhold / talkterm, and of
every such function in the shipped scripts exactly one waits.
  I-checks (static, capstone/pefile on Tools/work/exe/FFXII_TZA.exe): the footer reads, the override words, the two
  submits' kinds, and the kind-4/5 submitters (own rel32 sweep).
  D-checks (data, the shipped scripts through the kit decoder gen_req_channel_census.py, read from the VBF, md5-deduped):
  the function partition the census rests on is attacked directly - does every footer slot-16/17 body END in a
  terminator (else it falls through into the next function), and does every JMP-family operand (an index into the
  actor's jump table, section-000-bytecode BW-5) land inside the body? A corpus-wide pass over the us copy is the
  positive control that the containment test can see an out-of-body jump or a fall-through.
F-checks are findings this review adds (PASS when the finding reproduces).

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-ov16m-0930/ov16m_sem.py"
"""
import bisect, collections, csv, hashlib, io, os, struct, sys
import capstone, pefile

ROOT = os.getcwd()
DB = os.path.join(ROOT, "Database")
EXE = os.path.join(DB, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(DB, "Tools", "work", "graph", "functions.tsv")
pe = pefile.PE(EXE, fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
X86 = capstone.x86
FAILS = []
FT = {int(r["entry"], 16): (int(r["body_bytes"] or 0), r["name"]) for r in csv.DictReader(open(FUNCS, encoding="utf-8"), delimiter="\t")}
size = {k: v[0] for k, v in FT.items()}
starts = sorted(size)
TEXT = [s for s in pe.sections if s.Name.rstrip(b"\0") == b".text"][0]
TVA = BASE + TEXT.VirtualAddress
TDATA = TEXT.get_data()


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def raw(va, n):
    o = pe.get_offset_from_rva(va - BASE)
    return bytes(pe.__data__[o:o + n])


def s(i): return f"{i.mnemonic} {i.op_str}"
def body(fn):
    n = size[fn]
    return {i.address: i for i in md.disasm(raw(fn, n + 16), fn) if i.address < fn + n}
def tgt(i):
    if (i.mnemonic == "call" or i.mnemonic.startswith("j")) and i.operands and i.operands[0].type == X86.X86_OP_IMM:
        return i.operands[0].imm
    return None
def fn_of(a):
    k = bisect.bisect_right(starts, a) - 1
    f = starts[k] if k >= 0 else None
    return f if f is not None and a < f + max(size[f], 1) else None
def rel_sites(t):
    out = []
    for op in (b"\xe8", b"\xe9"):
        p = 0
        while True:
            k = TDATA.find(op, p)
            if k < 0: break
            p = k + 1
            if k + 5 <= len(TDATA) and TVA + k + 5 + struct.unpack("<i", TDATA[k + 1:k + 5])[0] == t:
                f = fn_of(TVA + k)
                if f is None or (TVA + k) in body(f): out.append((TVA + k, f))
    return sorted(out)


# =============================== image ================================================================================
e = body(0x00268EA0)
check("I1 00268EA0 reads override word +0xEA bounded by 0x11 and footer +0x24 (slot 17), override +0xE8 bounded by 0x10 "
      "and footer +0x22 (slot 16)", "0xea]" in s(e[0x00268EF8]) and "0x24]" in s(e[0x00268F21])
      and "0xe8]" in s(e[0x00268F3F]) and "0x22]" in s(e[0x00268F68]))
check("I1 the slot-16 submit files kind ebx = 5 (00268FB3 / 00268FDD) and the slot-17 submit kind 4 (00269017), both "
      "through 003DBBE0 (00268FF2 / 00269033)", s(e[0x00268FB3]) == "mov ebx, 5" and "ebx" in s(e[0x00268FDD])
      and s(e[0x00269017]).endswith(", 4") and tgt(e[0x00268FF2]) == 0x003DBBE0 and tgt(e[0x00269033]) == 0x003DBBE0,
      "%s / %s / %s" % (s(e[0x00268FB3]), s(e[0x00268FDD]), s(e[0x00269017])))
sub = rel_sites(0x003DBBE0); sub2 = rel_sites(0x003DBBF0)
check("I2 CONTROL own rel32 sweep: 003DBBE0 has four call sites, 00268C83 (00268B10), 00268DD4 (00268D10), 00268FF2 and "
      "00269033 (00268EA0); 003DBBF0 is reached only by the thunk's jmp",
      [a for a, _ in sub] == [0x00268C83, 0x00268DD4, 0x00268FF2, 0x00269033] and len(sub2) == 1 and sub2[0][0] == 0x003DBBE0,
      "%s ; %s" % (["%08X" % a for a, _ in sub], ["%08X" % a for a, _ in sub2]))

r = rel_sites(0x00268EA0)
fs = sorted({fn for _, fn in r})
check("F3 00268EA0 has 14 raw call / jmp sites in 9 functions (the record says 11): 0025AD10, 0025AE00, the interpreter "
      "0025E4C0 (REQCHG), 00266530 x2, 00267CC0 x4, 00268D10, 00269FE0 x2, 0026B4A0 (jmp), 0026CE60",
      len(r) == 14 and fs == [0x0025AD10, 0x0025AE00, 0x0025E4C0, 0x00266530, 0x00267CC0, 0x00268D10, 0x00269FE0, 0x0026B4A0, 0x0026CE60],
      "%d sites, %d functions" % (len(r), len(fs)))
rb = rel_sites(0x0026B4A0); rd = rel_sites(0x0025D5E0)
check("F4 the reqenable tail 0026B4A0 (which re-runs 00268EA0 when +0x0B bit 3 is set) is also called by the unit refresh "
      "BattleUnit_RefreshActorRuntimeFromDefinition (00238DAE), besides reqenable 0035555B, setupbattle 00351F7C and "
      "fieldsign 00355A71 / 00355A7E; the reqdisable tail 0025D5E0 by 00238DDE, 003558BF, 0035590B and 00355A8B",
      [a for a, _ in rb] == [0x00238DAE, 0x00351F7C, 0x0035555B, 0x00355A71, 0x00355A7E]
      and [a for a, _ in rd] == [0x00238DDE, 0x003558BF, 0x0035590B, 0x00355A8B],
      "%s ; %s" % (["%08X" % a for a, _ in rb], ["%08X" % a for a, _ in rd]))

# =============================== data =================================================================================
sys.path.insert(0, os.path.join(DB, "FFXII TZA", "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
import gen_req_channel_census as G  # noqa: E402
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
JMPS = {0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x5A, 0x5B, 0x5C, 0x60}
TERM = {0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x51}          # RET RETN RETT RETTN DRET, and an unconditional JMP
WAITP = {0x24, 0x25, 0x26, 0x27, 0x28, 0x29}
WAITS = {0x32, 0x5F, 0x61, 0x63}
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
seen = set(); nfiles = 0
slot = {16: collections.Counter(), 17: collections.Counter()}
slot_waits = {16: [], 17: []}
slot_out = []          # (file, actor, k, fn, reason)
corpus = collections.Counter()
named = collections.Counter(); named_w = []; named_out = []
corpus_ex = []
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks, path)
    except Exception:
        continue
    h = hashlib.md5(b).digest()
    if h in seen: continue
    seen.add(h)
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
    nfiles += 1
    pool = U32(sec, 0x4C)
    ents = [diroff + 4 + a * 0x30 for a in range(cnt)]
    bounds = sorted(set(U32(sec, x + 8) for x in ents) | {diroff, len(sec)})
    us = "/us/" in path
    for ai, en in enumerate(ents):
        start = U32(sec, en + 8)
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        code = sec[start:end]
        ft = U32(sec, en + 0x10); nf = U32(sec, ft)
        foffs = [U32(sec, ft + 4 + 8 * i + 4) for i in range(nf)]
        fnames = [sec[pool + U32(sec, ft + 4 + 8 * i):sec.find(b"\0", pool + U32(sec, ft + 4 + 8 * i))].decode("cp932", "replace") for i in range(nf)]
        lt = U32(sec, en + 0x14); nj = U32(sec, lt)
        joffs = [U32(sec, lt + 4 + 4 * i) for i in range(nj)]
        sepa = U32(sec, en + 0x18)
        special = [U16(sec, sepa + 2 + 2 * k) for k in range(18)]
        uniq = sorted(set(o for o in foffs if o < len(code)))
        def examine(fi):
            o = foffs[fi]
            nxt = min((x for x in uniq if x > o), default=len(code))
            ins, _ = G.decode(code[o:nxt])
            outs = []
            for pc, op, imm in ins:
                if op in JMPS:
                    if imm >= nj: outs.append("jump index %d >= %d" % (imm, nj))
                    elif not (o <= joffs[imm] < nxt): outs.append("jump to +%X outside [%X, %X)" % (joffs[imm], o, nxt))
            last = ins[-1][1] if ins else None
            fall = nxt < len(code) and last not in TERM
            return ins, outs, fall
        for k in (16, 17):
            fi = special[k]
            if fi == 0xFFFF or fi >= nf: continue
            ins, outs, fall = examine(fi)
            slot[k]["actors"] += 1
            w = [G.OPN[op] for _pc, op, _i in ins if op in WAITP | WAITS]
            if w: slot_waits[k].append((path, ai, fnames[fi], w))
            if outs or fall: slot_out.append((path, ai, k, fnames[fi], outs, fall))
        for fi in range(nf):
            nm = fnames[fi]
            if (nm.startswith("talkhold") or nm.startswith("talkterm") or nm == "catrine_talk_term") and foffs[fi] < len(code):
                ins, outs, fall = examine(fi)
                named["functions"] += 1
                w = [G.OPN[op] for _pc, op, _i in ins if op in WAITP | WAITS]
                if w: named_w.append((path.split("/")[-1], ai, nm, w))
                if outs or fall: named_out.append((path.split("/")[-1], ai, nm, outs[:1], fall))
        if us:
            for fi in range(nf):
                if foffs.index(foffs[fi]) != fi or foffs[fi] >= len(code): continue
                ins, outs, fall = examine(fi)
                corpus["functions"] += 1
                corpus["jumps"] += sum(1 for _pc, op, _i in ins if op in JMPS)
                if outs: corpus["with_out_of_body_jump"] += 1
                if fall: corpus["falls_through"] += 1
                if (outs or fall) and len(corpus_ex) < 3: corpus_ex.append((path.split("/")[-1], ai, fnames[fi], outs[:1], fall))
check("D1 CONTROL the footer population reproduces the record: %d slot-16 and %d slot-17 actors (record: 15,934 each) over "
      "%d md5-distinct files" % (slot[16]["actors"], slot[17]["actors"], nfiles),
      slot[16]["actors"] == 15934 and slot[17]["actors"] == 15934)
check("D1 waits in footer slot functions: none in slot 16; slot 17 only asp_a03 actor 25 ラバナ_通常_NPC01 talkterm (one "
      "REQEW per language copy)", not slot_waits[16] and len(slot_waits[17]) == 9
      and all(x[0].endswith("asp_a03.ebp") and x[1] == 25 and x[2] == "talkterm" and x[3] == ["REQEW"] for x in slot_waits[17]),
      "%d / %d" % (len(slot_waits[16]), len(slot_waits[17])))
check("F1 CONTROL the containment test can fire: over the us copy, %d functions and %d JMP-family operands; %d functions "
      "jump outside their partition body and %d fall through into the next function (examples %s)"
      % (corpus["functions"], corpus["jumps"], corpus["with_out_of_body_jump"], corpus["falls_through"], corpus_ex),
      corpus["jumps"] > 0 and (corpus["with_out_of_body_jump"] + corpus["falls_through"]) > 0)
check("F1 the partition is sound for every footer slot-16/17 function: each ends in a terminator and no JMP-family operand "
      "leaves its body (so no wait is reachable outside the body the census decoded)", not slot_out,
      "; ".join("%s a%d k%d %s %s%s" % (p.split("/")[-1], a, k, n, o[:1], " FALLS" if fl else "") for p, a, k, n, o, fl in slot_out[:6]))

nw = sorted({(a, b, c, tuple(d)) for a, b, c, d in named_w})
check("F2 every talkhold* / talkterm* / catrine_talk_term function in any actor (%d bodies, a superset of the 450 REQCHG "
      "override targets) is contained and terminated, and the only one that waits is asp_a03's NPC01 talkterm"
      % named["functions"], not named_out and nw == [("asp_a03.ebp", 25, "talkterm", ("REQEW",))],
      "waits %s ; out %s" % (nw, named_out[:4]))

print("FAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
