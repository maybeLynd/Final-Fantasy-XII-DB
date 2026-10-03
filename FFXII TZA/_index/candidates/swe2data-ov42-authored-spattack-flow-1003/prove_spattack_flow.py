"""prove_spattack_flow.py - SWE2-DATA, 2026-10-03, for ASTRA-REQ-DATA-OV42-AUTHORED-QUEUE-REFERENCE-FLOW-1002.

Read-only, static. Do the shipped authored getspattackskillinfo (029A) out-references feed spattackread (029B) through
integer-tagged, word-preserving loads into valid, byte-disjoint 4-byte cells, or is there a counterexample?

Inputs (all pinned and hashed into the result):
  - the shipping EXE (sha256 73461d08...), read through the section-aware offset map;
  - every language copy of ps2data/plan_master/*/event/spc_z/spc_z0000/spc_z0000.ebp, read from FFXII_TZA.vbf through
    the decoder FABLE's gen_req_channel_census.py uses (the same path script_verb_census.py uses);
  - the verb table (arity column) for the stack-depth bound only.

What it checks (each check prints PASS/FAIL; FAILS 0 is the only passing outcome):
  N*  native facts at fixed addresses (exact instruction text), the bridges' pop order and destination registers, the
      reference decoder's class switch, the pop helper's tag arms, PUSHP's descriptor packing and PUSHV/POPV widths;
  S*  script facts: identical language copies, the descriptor table rows of the variables involved, the function and
      label tables, the three call sites the census lists, and a complete per-variable reader/writer census of the image;
  F*  the two authored flows (init flow A, loop flow B) with their guards, copies and intervening instructions;
  D*  stack depth at each pushed-argument site (capacity 63) by CFG propagation over the label table;
  C*  controls: synthetic mutations of decoded records / descriptors that each MUST make one named check refuse.

Usage (repo root, analysis venv or any Python with capstone):
  python -B "Database/FFXII TZA/_index/candidates/swe2data-ov42-authored-spattack-flow-1003/prove_spattack_flow.py"
         [--out result.json]
"""
import argparse, copy, csv, hashlib, io, json, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))           # Database/FFXII TZA
ROOT = os.path.abspath(os.path.join(DB, "..", ".."))                 # repo root
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
EXE_SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000
VERB_TSV = os.path.join(DB, "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
SCRIPT = "event/spc_z/spc_z0000/spc_z0000.ebp"

FAILS = []
LOG = []
QUIET = [False]


def check(cid, ok, text):
    LOG.append({"id": cid, "pass": bool(ok), "text": text})
    if not QUIET[0]:
        print("%s  %s %s" % ("PASS" if ok else "FAIL", cid, text))
    if not ok:
        FAILS.append(cid)
    return ok


# ------------------------------------------------------------------------------------------------ native
def load_exe():
    d = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    secs = []
    for i in range(nsec):
        o = pe + 24 + opt + i * 40
        secs.append((struct.unpack_from("<I", d, o + 12)[0], struct.unpack_from("<I", d, o + 8)[0],
                     struct.unpack_from("<I", d, o + 20)[0], struct.unpack_from("<I", d, o + 16)[0]))
    return d, secs


def off(secs, addr):
    r = addr - BASE
    for va, vs, ro, rs in secs:
        if va <= r < va + vs:
            if r - va >= rs:
                raise ValueError("%08X is past raw data" % addr)
            return ro + (r - va)
    raise ValueError("%08X not in a section" % addr)


def disasm(d, secs, start, size):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    o = off(secs, start)
    return [(x.address, ("%s %s" % (x.mnemonic, x.op_str)).strip()) for x in md.disasm(d[o:o + size], start)]


# Exact instruction text the claims rest on. Each tuple: (address, expected text).
NATIVE = {
    # 029A bridge 00348330 (165 B): first pop -> decode -> rsi (RDX, action); second pop -> decode -> rbx (RCX, unit)
    "N1-029A-first-pop-to-rdx": [
        (0x00348355, "call 0x267e10"), (0x0034835A, "mov r8d, eax"), (0x00348363, "call 0x2650b0"),
        (0x0034836B, "mov rsi, rax"), (0x0034836E, "call 0x267e10"), (0x0034837C, "call 0x2650b0"),
        (0x00348381, "mov rdx, rsi"), (0x00348384, "mov rcx, rax"), (0x00348387, "mov rbx, rax"),
        (0x0034838A, "call 0x309c00")],
    "N2-029A-one-context-for-both-decodes": [
        (0x0034834A, "call 0x2640c0"), (0x00348352, "mov rbx, rax"), (0x00348360, "mov rcx, rbx"),
        (0x00348379, "mov rcx, rbx")],
    "N3-029A-unconditional-postcall-reads": [
        (0x003483A9, "mov ecx, dword ptr [rbx]"), (0x003483B1, "mov ecx, dword ptr [rsi]")],
    # 029B bridge 00348870: first pop -> ebx -> EDX (action word), second pop -> ECX (unit)
    "N4-029B-first-pop-to-edx": [
        (0x00348880, "call 0x267e10"), (0x00348888, "mov ebx, eax"), (0x0034888A, "call 0x267e10"),
        (0x0034888F, "mov edx, ebx"), (0x00348891, "mov ecx, eax"), (0x00348893, "call 0x30eea0")],
    # the pop helper: tag 1 -> raw dword, tag 2 -> cvttss2si
    "N5-pop-int-tag1-raw-dword": [
        (0x00267E21, "movzx edx, byte ptr [r8 + rcx + 4]"), (0x00267E27, "sub edx, 1"), (0x00267E2A, "je 0x267e51"),
        (0x00267E51, "mov eax, dword ptr [rcx + r8*4 + 0x184]")],
    # the reference decoder: class = (desc >> 24) & 7, 0..5 through a table, else base 0
    "N6-ref-decoder-class-switch": [
        (0x002650BC, "sar eax, 0x18"), (0x002650C2, "and eax, 7"), (0x002650C8, "cmp eax, 5"),
        (0x002650CB, "ja 0x26516c"), (0x002650DA, "mov r8d, dword ptr [rcx + rax*4 + 0x145180]"),
        (0x002650FC, "mov rcx, qword ptr [r9 + 0x40]"), (0x00265102, "and eax, 0xffffff"),
        (0x00265107, "add rax, rcx"), (0x0026516E, "xor ecx, ecx")],
    # PUSHP: offset + scaled index | class | width 7, tag 1
    "N7-pushp-packing-tag1": [
        (0x00268158, "and r8d, 0xffffff"), (0x0026815F, "and r9d, 0x7000000"), (0x00268166, "add r8d, edx"),
        (0x00268169, "or r8d, r9d"), (0x0026816C, "or r8d, 0x70000000"), (0x00268173, "cmp eax, 0x3f"),
        (0x0026817B, "mov byte ptr [rax + rbx + 4], 1"), (0x00268194, "mov dword ptr [rbx + rcx*4 + 0x184], r8d")],
    # PUSHV s32 arm loads a dword; the tag comes from the kind word (bit 27 in the resolver)
    "N8-pushv-s32-dword-load": [(0x00268048, "mov ecx, dword ptr [rax + rcx*4]"),
                                 (0x00262644, "bt r12d, 0x1b")],
    # POPV: a tag-1 entry is taken as its raw dword (no conversion) and the s32 arm stores it unclamped
    "N10-popv-int-raw-s32-store": [(0x00267F07, "je 0x267f57"), (0x00267F57, "mov eax, dword ptr [rbx + rdx*4 + 0x184]"),
                                   (0x00267F37, "call 0x26d530"), (0x0026D5E9, "mov eax, dword ptr [r9 + 0x20]"),
                                   (0x0026D5ED, "mov dword ptr [r8 + rcx*4], eax")],
}
FUNC_SPANS = {0x00348330: 0xA5, 0x00348870: 0x3C, 0x00267E10: 0x4E, 0x002650B0: 0xCE, 0x00268100: 0xA4,
              0x00267FC0: 0x140, 0x00262440: 0x300, 0x00267E60: 0x100, 0x0026D530: 0xC2}


def native_checks(d, secs):
    have = {}
    for fn, size in FUNC_SPANS.items():
        for a, t in disasm(d, secs, fn, size):
            have.setdefault(a, t)
    for cid, rows in NATIVE.items():
        bad = [(hex(a), want, have.get(a)) for a, want in rows if have.get(a) != want]
        check(cid, not bad, "%d instructions as stated%s" % (len(rows), "" if not bad else " - mismatch %s" % bad))
    # jump table of the reference decoder: class 1 -> 002650FC (the +0x40 'file' base)
    o = off(secs, 0x00265180)
    arms = [BASE + struct.unpack_from("<I", d, o + 4 * i)[0] for i in range(6)]
    o2 = off(secs, 0x0026D5F4)
    store_arms = [BASE + struct.unpack_from("<I", d, o2 + 4 * i)[0] for i in range(6)]
    check("N11-popv-store-s32-arm", store_arms[4] == 0x0026D5E9,
          "store jump table 0026D5F4: width 4 (s32) -> %08X" % store_arms[4])
    check("N9-ref-decoder-class1-arm", arms[1] == 0x002650FC,
          "jump table 00265180: class arms %s; class 1 -> %08X (reads [ctx+0x40])" % (
              ",".join("%08X" % a for a in arms), arms[1]))
    return have, arms


# ------------------------------------------------------------------------------------------------ script
def load_script():
    sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
    cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        import gen_req_channel_census as G
        f = io.open(G.VBF, "rb")
        names, blocks = G.V.load_index(f)
        copies = {}
        for p in sorted(n for n in names if n.lower().endswith(SCRIPT)):
            copies[p] = G.V.read_entry(f, names, blocks, p)
    finally:
        os.chdir(cwd)
    return G, copies


U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
CLASSES = {0: "global", 1: "file", 2: "local", 3: "c3", 4: "scratch1", 5: "scratch2", 7: "array"}
WIDTHS = {0: "u8", 1: "s8", 2: "u16", 3: "s16", 4: "s32", 5: "f32"}
WBYTES = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4}


def parse(G, sec):
    t28 = U32(sec, 0x28)
    desc = [U32(sec, t28 + 4 + i * 8) for i in range(U32(sec, t28))]
    diroff, pool = U32(sec, 0x18), U32(sec, 0x4C)
    actors = []
    for s in range(U32(sec, diroff)):
        e = diroff + 4 + s * 0x30
        no = pool + U32(sec, e)
        name = sec[no:sec.find(b"\0", no)].decode("cp932", "replace")
        code, ftab, ltab = U32(sec, e + 8), U32(sec, e + 0x10), U32(sec, e + 0x14)
        funcs = [(U32(sec, ftab + 4 + 8 * k), U32(sec, ftab + 8 + 8 * k)) for k in range(U32(sec, ftab))]
        fnames = [sec[pool + n:sec.find(b"\0", pool + n)].decode("cp932", "replace") for n, _ in funcs]
        labels = [U32(sec, ltab + 4 + 4 * k) for k in range(U32(sec, ltab))]
        actors.append({"name": name, "code": code, "funcs": [(fnames[k], funcs[k][1]) for k in range(len(funcs))],
                       "labels": labels})
    starts = sorted(a["code"] for a in actors)
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for a in actors:
        end = min(x for x in bounds if x > a["code"])
        ins, anomaly = G.decode(sec[a["code"]:end])
        a["end"], a["ins"], a["anomaly"] = end, ins, anomaly
    return desc, actors


def fields(dsc):
    return {"class": (dsc >> 24) & 7, "offset": dsc & 0xFFFFFF, "float": (dsc >> 27) & 1, "width": dsc >> 28}


VAR_OPS = {0x48: "PUSHV", 0x49: "POPV", 0x4A: "PUSHDBG", 0x4B: "PUSHP"}


def census(actors):
    """Every instruction in the image whose operand is a variable index, by variable."""
    out = {}
    for a in actors:
        for pc, op, imm in a["ins"]:
            if op in VAR_OPS:
                out.setdefault(imm, []).append((a["name"], a["code"] + pc, VAR_OPS[op]))
    return out


def find(actor, rel, op, imm=None):
    for pc, o, i in actor["ins"]:
        if pc == rel:
            return o == op and (imm is None or i == imm)
    return False


# stack effects for the opcodes present in the functions examined (see the interpreter page's opcode table)
def effect(op, imm, arity):
    if op in (0x48, 0x4B, 0x4E, 0x4F, 0x50, 0x4C, 0x4D) or 0x3E <= op <= 0x45:
        return 0, 1                               # pushes one
    if op == 0x49 or 0x36 <= op <= 0x3D or op == 0x1C:
        return 1, 0                               # pops one
    if op == 0x04:
        return 1, 0                               # sysSystem(n): pops its one operand
    if 0x05 <= op <= 0x16:
        return 2, 1
    if 0x17 <= op <= 0x1A:
        return 1, 1
    if 0x21 <= op <= 0x29:
        return 3, 0                               # REQ family: priority, actor, function
    if op in (0x5A, 0x5B, 0x5C):
        return 1, 0                               # pop X, conditional jump
    if op == 0x51:
        return 0, 0
    if op == 0x58:
        return arity[imm], 1                      # CALL leaves the result
    if op == 0x5D:
        return arity[imm], 0                      # CALLPOPA pops it into A
    if op == 0x5E:
        return arity[imm] + 1, 0                  # CALLACTPOPA pops an actor id first
    if op == 0x59:
        return arity[imm] + 1, 1
    if op in (0x2D, 0x2E, 0x2F, 0x30, 0x31):
        return 0, 0
    return None


def depths(actor, fstart, fend, arity):
    """Worklist propagation of value-stack depth over one function; returns {pc: depth} or raises on a join conflict
    or an unknown effect."""
    ins = [x for x in actor["ins"] if fstart <= x[0] < fend]
    by = {pc: k for k, (pc, _, _) in enumerate(ins)}
    dep = {fstart: 0}
    work = [fstart]
    while work:
        pc = work.pop()
        k = by[pc]
        _, op, imm = ins[k]
        e = effect(op, imm, arity)
        if e is None:
            raise ValueError("unknown stack effect for op %02X at %X" % (op, pc))
        pops, pushes = e
        if dep[pc] < pops:
            raise ValueError("underflow at %X" % pc)
        nd = dep[pc] - pops + pushes
        succ = []
        if op in (0x2D, 0x2E, 0x2F, 0x30, 0x31):
            succ = []
        elif op == 0x51:
            succ = [actor["labels"][imm]]
        elif op in (0x5A, 0x5B, 0x5C):
            succ = [actor["labels"][imm]] + ([ins[k + 1][0]] if k + 1 < len(ins) else [])
        else:
            succ = [ins[k + 1][0]] if k + 1 < len(ins) else []
        for s in succ:
            if s not in by:
                raise ValueError("branch from %X leaves the function (%X)" % (pc, s))
            if s in dep:
                if dep[s] != nd:
                    raise ValueError("depth conflict at %X: %d vs %d" % (s, dep[s], nd))
            else:
                dep[s] = nd
                work.append(s)
    return dep


def script_checks(G, copies, arity, desc_override=None, actors_override=None, quiet=False):
    """Returns a dict of derived facts; the controls call it again with mutated inputs."""
    global LOG, FAILS
    sec = next(iter(copies.values()))[0x80:]
    sec = sec[:U32(sec, 4)]
    desc, actors = parse(G, sec)
    if desc_override:
        desc = desc_override(list(desc))
    if actors_override:
        actors = actors_override(copy.deepcopy(actors))
    A = {a["name"]: a for a in actors}
    sup, tek = A["監督"], A["技読み込み"]
    facts = {}

    # S3: the variables involved
    rows = {}
    for v in (0, 1, 3, 4, 5, 6):
        rows[v] = fields(desc[v])
    facts["vars"] = {v: dict(r, descriptor="%08X" % desc[v]) for v, r in rows.items()}
    ok = all(rows[v]["class"] == 1 and rows[v]["width"] == 4 and rows[v]["float"] == 0 for v in (0, 1, 5, 6))
    check("S3-four-cells-file-s32-int", ok, "vars 0,1,5,6: " + ", ".join(
        "%d=%s %s off 0x%X float %d" % (v, CLASSES.get(rows[v]["class"]), WIDTHS.get(rows[v]["width"], rows[v]["width"]),
                                         rows[v]["offset"], rows[v]["float"]) for v in (0, 1, 5, 6)))

    def disjoint(a, b):
        ra = (rows[a]["offset"], rows[a]["offset"] + WBYTES.get(rows[a]["width"], 0))
        rb = (rows[b]["offset"], rows[b]["offset"] + WBYTES.get(rows[b]["width"], 0))
        same_home = rows[a]["class"] == rows[b]["class"] == 1
        return same_home and (ra[1] <= rb[0] or rb[1] <= ra[0]), ra, rb
    for (act, unit), cid in (((0, 1), "S4-init-outputs-disjoint"), ((5, 6), "S5-loop-outputs-disjoint")):
        ok, ra, rb = disjoint(act, unit)
        d = rows[unit]["offset"] - rows[act]["offset"]
        check(cid, ok, "action var %d [0x%X,0x%X) unit var %d [0x%X,0x%X) in one 'file' home, RCX-RDX = %+d" % (
            act, ra[0], ra[1], unit, rb[0], rb[1], d))
        facts["d_%d_%d" % (act, unit)] = d

    # S6: function and label tables
    check("S6-function-tables", sup["funcs"][0] == ("init", 0) and ("全体処理", 0x4C) in sup["funcs"]
          and ("技読み込み", 1) in tek["funcs"] and sup["anomaly"] is None and tek["anomaly"] is None,
          "監督 functions %s; 技読み込み functions %s; linear decode anomaly-free in both" % (sup["funcs"], tek["funcs"]))

    # S7: the census sites
    sites = [(sup, 0x3D, 0x5D, 0x29A), (sup, 0x19B, 0x58, 0x29A), (tek, 0x2A, 0x5D, 0x29B)]
    ok = all(find(a, rel, op, imm) for a, rel, op, imm in sites)
    check("S7-census-sites", ok, "029A CALLPOPA at 0x%X, 029A CALL at 0x%X, 029B CALLPOPA at 0x%X (image offsets; the "
          "census lists 4ad / 60b / 744)" % (sup["code"] + 0x3D, sup["code"] + 0x19B, tek["code"] + 0x2A))

    # F1: flow A (init) - PUSHP 1; PUSHP 0; CALLPOPA 029A
    fa = find(sup, 0x37, 0x4B, 1) and find(sup, 0x3A, 0x4B, 0) and find(sup, 0x3D, 0x5D, 0x29A)
    check("F1-init-call-pushes", fa, "init: PUSHP var1 (pushed first -> second pop -> RCX unit), PUSHP var0 (top -> "
          "first pop -> RDX action), CALLPOPA 029A; result to A, never tested")
    # F2: flow B (loop) - PUSHP 6; PUSHP 5; CALL 029A; OPNOT; POPV 3; PUSHV 5; POPV 0; PUSHV 6; POPV 1; REQEW(3,1,1)
    seq = [(0x195, 0x4B, 6), (0x198, 0x4B, 5), (0x19B, 0x58, 0x29A), (0x19E, 0x17, None), (0x19F, 0x49, 3),
           (0x1A2, 0x48, 5), (0x1A5, 0x49, 0), (0x1A8, 0x48, 6), (0x1AB, 0x49, 1), (0x1AE, 0x4F, 3), (0x1B1, 0x4F, 1),
           (0x1B4, 0x4F, 1), (0x1B7, 0x27, None)]
    fb = all(find(sup, rel, op, imm) for rel, op, imm in seq)
    check("F2-loop-call-copy-request", fb, "loop: PUSHP var6, PUSHP var5, CALL 029A, OPNOT, POPV var3, PUSHV var5, "
          "POPV var0, PUSHV var6, POPV var1, REQEW(3, actor 1, function 1) - straight line, no branch between")
    # F3: the reader side - PUSHV 3; OPNOT; POPXNCJMP L2 (=RET); ...; PUSHV 1; PUSHV 0; CALLPOPA 029B
    rd = [(0x1, 0x48, 3), (0x4, 0x17, None), (0x5, 0x5C, 2), (0x24, 0x48, 1), (0x27, 0x48, 0), (0x2A, 0x5D, 0x29B),
          (0x2D, 0x2D, None)]
    fr = all(find(tek, rel, op, imm) for rel, op, imm in rd) and tek["labels"][2] == 0x2D
    check("F3-reader-guard-and-pushes", fr, "技読み込み::技読み込み: skips to RET (label 2 = 0x%X) unless var3 == 0; then "
          "PUSHV var1 (second pop -> ECX unit), PUSHV var0 (first pop -> EDX action), CALLPOPA 029B" % tek["labels"][2])
    # F4: request targets - REQEW(2,1,1) before the loop and REQEW(3,1,1) after the copy both name 技読み込み function 1
    req0 = find(sup, 0x52, 0x4F, 2) and find(sup, 0x55, 0x4F, 1) and find(sup, 0x58, 0x4F, 1) and find(sup, 0x5B, 0x27)
    check("F4-request-targets", req0 and fb and [a["name"] for a in actors].index("技読み込み") == 1
          and tek["funcs"][1][0] == "技読み込み",
          "全体処理 0x52..0x5B REQEW(2, actor 1, fn 1) and 0x1AE..0x1B7 REQEW(3, actor 1, fn 1); actor 1 = 技読み込み, fn 1 = 技読み込み")

    # S9: every request in the image that names 技読み込み::技読み込み (operands pushed priority, actor, function)
    reqs = []
    for a in actors:
        ins = a["ins"]
        for k, (pc, op, imm) in enumerate(ins):
            if 0x21 <= op <= 0x29 and k >= 3 and all(ins[k - j][1] in (0x4E, 0x4F) for j in (1, 2, 3)):
                if (ins[k - 2][2], ins[k - 1][2]) == (1, 1):
                    reqs.append((a["name"], "%X" % (a["code"] + pc), ins[k - 3][2]))
            elif 0x21 <= op <= 0x29:
                reqs.append((a["name"], "%X" % (a["code"] + pc), "operands not immediate"))
    facts["requests_to_reader"] = reqs
    check("S9-reader-requests", sorted(reqs) == sorted([("監督", "%X" % (sup["code"] + 0x5B), 2),
                                                         ("監督", "%X" % (sup["code"] + 0x1B7), 3)]),
          "requests naming actor 1 function 1 (and any request with non-immediate operands): %s" % json.dumps(
              reqs, ensure_ascii=False))

    # S8: complete per-variable census of the image
    cen = census(actors)
    facts["census"] = {v: cen.get(v, []) for v in (0, 1, 3, 5, 6)}
    writers = {v: [(n, "%X" % pc, op) for n, pc, op in cen.get(v, []) if op in ("POPV", "PUSHP")] for v in (0, 1, 3, 5, 6)}
    facts["writers"] = writers
    expect = {0: [("監督", "%X" % (sup["code"] + 0x3A), "PUSHP"), ("監督", "%X" % (sup["code"] + 0x1A5), "POPV")],
              1: [("監督", "%X" % (sup["code"] + 0x37), "PUSHP"), ("監督", "%X" % (sup["code"] + 0x1AB), "POPV")],
              3: [("監督", "%X" % (sup["code"] + 0x3), "POPV"), ("監督", "%X" % (sup["code"] + 0x19F), "POPV")],
              5: [("監督", "%X" % (sup["code"] + 0x198), "PUSHP")],
              6: [("監督", "%X" % (sup["code"] + 0x195), "PUSHP")]}
    ok = all(sorted(writers[v]) == sorted(expect[v]) for v in expect)
    check("S8-image-writer-census", ok and all(a["anomaly"] is None for a in actors),
          "every POPV/PUSHP naming vars 0,1,3,5,6 in all %d actors: %s" % (len(actors), json.dumps(writers, ensure_ascii=False)))

    # D1: stack depth at the pushed-argument sites
    try:
        # init carries PUSHDBG/DVAR pairs, whose stack effects this script does not model. init has no branch, so
        # its depth at 0x37 is bounded by the number of instructions before it (no opcode pushes more than one).
        pre = [x for x in sup["ins"] if 0 <= x[0] < 0x37]
        if any(op in (0x51, 0x5A, 0x5B, 0x5C) or 0x52 <= op <= 0x57 for _, op, _ in pre):
            raise ValueError("init is not straight-line before 0x37")
        dinit = {0x37: len(pre)}
        dloop = depths(sup, 0x4C, 0x1F2, arity)
        dread = depths(tek, 1, 0x2E, arity)
        facts["depth"] = {"init_0x37": dinit[0x37], "loop_0x195": dloop[0x195], "read_0x24": dread[0x24]}
        check("D1-stack-depth", dinit[0x37] <= 61 and dloop[0x195] <= 61 and dread[0x24] <= 61,
              "depth before the first pushed argument: init <= %d (straight-line bound), loop %d, reader %d (both "
              "pushes stored while depth < 63)"
              % (dinit[0x37], dloop[0x195], dread[0x24]))
    except (ValueError, KeyError) as e:
        facts["depth"] = str(e)
        check("D1-stack-depth", False, "depth propagation refused: %s" % e)
    return facts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    args = ap.parse_args()
    global LOG, FAILS

    d, secs = load_exe()
    exe_sha = hashlib.sha256(d).hexdigest()
    check("N0-exe-identity", exe_sha == EXE_SHA, "EXE sha256 %s" % exe_sha)
    native_checks(d, secs)

    G, copies = load_script()
    hashes = {p: hashlib.sha256(b).hexdigest() for p, b in copies.items()}
    check("S1-language-copies", len(copies) == 9 and len(set(hashes.values())) == 1,
          "%d copies of %s, %d distinct sha256 (%s)" % (len(copies), SCRIPT, len(set(hashes.values())),
                                                      next(iter(hashes.values()))))
    b = next(iter(copies.values()))
    check("S2-ebp2-magic", U32(b, 0x80) == 0x8000000B, "EBP2 script magic at +0x80")
    sec = b[0x80:0x80 + U32(b, 0x84)]
    farea = sec[U32(sec, 0x38):U32(sec, 0x40)]
    check("S2b-file-area-zero-in-image", farea[0xC:0x10] == b"\0" * 4 and farea[0x10:0x14] == b"\0" * 4,
          "file area +0x%X..+0x%X (to the msp region): cells 0xC..0x14 hold %s in the shipped image" % (
              U32(sec, 0x38), U32(sec, 0x40), farea[0xC:0x14].hex()))

    arity = {}
    for r in csv.DictReader(open(VERB_TSV, encoding="utf-8"), delimiter="\t"):
        try:
            arity[int(r["call_id"], 16)] = int(r["arity"])
        except ValueError:
            pass
    check("S0-verb-arity", arity.get(0x29A) == 2 and arity.get(0x29B) == 2,
          "verb table: 029A arity %s, 029B arity %s" % (arity.get(0x29A), arity.get(0x29B)))

    facts = script_checks(G, copies, arity)

    # ---------------------------------------------------------------------------------------- controls
    print("-- controls (each must refuse the named check)")
    controls = []

    def run_control(name, target, **kw):
        global LOG, FAILS
        saved_log, saved_fails = LOG, FAILS
        LOG, FAILS = [], []
        QUIET[0] = True
        try:
            script_checks(G, copies, arity, **kw)
        except Exception as e:
            FAILS.append("exception:%s" % e)
        QUIET[0] = False
        refused = target in FAILS
        LOG, FAILS = saved_log, saved_fails
        controls.append({"control": name, "target": target, "refused": refused})
        check("C-" + name, refused, "synthetic mutation must make %s refuse" % target)

    def overlap_unit(ds):
        ds[6] = (ds[6] & ~0xFFFFFF) | 0x1A        # unit cell 0x1A..0x1E overlaps action 0x18..0x1C
        return ds

    def unit_local(ds):
        ds[6] = (ds[6] & ~0x07000000) | 0x02000000   # unit cell in the 'local' home - no shared base
        return ds

    def action_s16(ds):
        ds[5] = (ds[5] & 0x0FFFFFFF) | 0x30000000    # action cell s16 - not word-preserving
        return ds

    def extra_writer(actors):
        for a in actors:
            if a["name"] == "PC00":
                a["ins"].append((0x7FF0, 0x49, 0))    # a POPV var0 in another actor
        return actors

    def swapped_pushes(actors):
        for a in actors:
            if a["name"] == "監督":
                a["ins"] = [(pc, op, {6: 5, 5: 6}.get(imm, imm) if pc in (0x195, 0x198) else imm)
                            for pc, op, imm in a["ins"]]
        return actors

    def reader_unguarded(actors):
        for a in actors:
            if a["name"] == "技読み込み":
                a["ins"] = [(pc, 0x00 if pc == 0x5 else op, imm) for pc, op, imm in a["ins"]]
        return actors

    run_control("overlapping-unit-cell", "S5-loop-outputs-disjoint", desc_override=overlap_unit)
    run_control("unit-cell-other-home", "S5-loop-outputs-disjoint", desc_override=unit_local)
    run_control("action-cell-s16", "S3-four-cells-file-s32-int", desc_override=action_s16)
    run_control("extra-writer-in-another-actor", "S8-image-writer-census", actors_override=extra_writer)
    run_control("swapped-loop-pushes", "F2-loop-call-copy-request", actors_override=swapped_pushes)
    run_control("reader-guard-removed", "F3-reader-guard-and-pushes", actors_override=reader_unguarded)

    print("FAILS %d" % len(FAILS))
    res = {"script": os.path.relpath(__file__, ROOT).replace("\\", "/"),
           "script_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
           "exe_sha256": exe_sha, "ebp_copies": hashes, "facts": facts, "checks": LOG, "controls": controls,
           "fails": FAILS}
    if args.out:
        json.dump(res, open(args.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
