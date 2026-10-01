#!/usr/bin/env python3
"""Typed field scan with argument propagation (F-6 prototype, generation 3).

Seeds: --hop DISP   (a register loaded from qword [any + DISP], e.g. 0x698 = BattleUnit->stats)
       --array ADDR:STRIDE (base = *(ADDR) + k*STRIDE)
Propagation: whenever a tracked pointer sits in an argument register (rcx, rdx, r8, r9) at a call,
the callee is queued with that argument index; the callee is then scanned from its entry with the
argument register pre-tracked. --depth bounds the propagation (default 2). Every callee reached is
reported with the chain that reached it. A tracked pointer that is copied with an offset (lea) is
followed with that offset, so a call on (rec + 0x50) is reported as arg base 0x50.
Every [rec + disp] access (0 <= disp < --size) is written to --out with kind r/w/rw and its route.
Control (--control fn:disp) must be found among the results or the scan refuses.

KNOWN DEFECT - REBASING ACROSS MUTUALLY EXCLUSIVE PATHS, found 2026-09-11 in an installed census.
This scan walks each function in ADDRESS order and has no branch structure. When a function
establishes a tracked pointer at one offset of an object and later re-establishes the SAME register
at a DIFFERENT offset, every access belonging to the first path that sits after the second `lea` in
address order is filed at the wrong displacement. Not missing - WRONG, at a displacement the code
never touches on that path.

The case: Movement_ModifyHeadingSpeedForObjectState sets `rdi = record+0x610` at 004240C7 for its
cache path and `rdi = record+0x620` at 00424158 for its arm path; the cache path is entered by jumps
from 00424135, 00424142 and 00424156, all before the second lea. Four of its accesses were filed
0x10 high in character-render-record-accesses.tsv and are corrected there, each row carrying a note.

HOW IT WAS CAUGHT, and the lesson: not by inspection. The census disagreed with a store row whose
width had been read off the disassembly directly, and check_census_widths reported the MISMATCH the
moment the census was registered with it. An unregistered census is checked against nothing, so
register a new census with the width checkers in the same change that creates it.

A CHECKER FOR THIS WAS BUILT AND DISCARDED. Flagging every function that rebases gave 1273 at-risk
accesses against a real defect of four rows; adding a branch test - requiring a jump from before the
pivot to after it - only brought it to 683, because almost every non-trivial function has some jump
skipping some point. Separating the real cases needs actual dataflow, not a heuristic over the census,
and a 0.6 percent instrument is worse than none. Read the disassembly at the pivot instead.

CALLEE-SAVED REGISTERS ACROSS EPILOGUES, fixed 2026-09-11 (FZ-16, FABLE-PUB140). Three record
censuses were bounded by a loss that was first blamed on `mov rdi, rcx` (a callee-saved copy of the
seed register) and was in fact the `pop rdi` of the first early-return epilogue in address order:
`pop` set `dst`, so every callee-saved register died at the first `pop` and every callee reached only
after that point was never queued. Four rules now govern a register loaded from the frame:
  1. `pop reg` is never a kill for a callee-saved register (volatile registers are still dropped).
  2. The restore exemption for `mov reg, [rsp+X]` applies only INSIDE an epilogue run - restores,
     pops, rsp adjustments, the security-cookie sequence (`mov rcx,[rsp+X]; xor rcx,rsp;
     call __security_check_cookie`) and stores the compiler scheduled between restores, ending at
     `ret` OR at a tail `jmp` to a function entry. A frame reload anywhere else is a kill: the
     script VM reloads its CONTEXT into r13 from the first argument's home slot after every handler
     that fetched a record into r13 (0025E61B and eleven more), and the old blanket exemption kept
     r13 "the record" for the rest of a 14 KB function - 24 rows of context reads were filed as
     ActorStorageRecord reads (+0x28, +0x48, +0x58, +0x60, +0x68, +0x70, +0x78, +0x80, +0x98).
  3. The exemption needs a QWORD load. `mov ebx, dword [rsp+0x228]` is an argument, not a restore.
  4. Spill-follow: a qword reload from a frame slot whose last recorded store was a tracked register
     re-establishes that value, for any destination register (0030E360 spills the unit at 0030E3B6,
     loses rbx to a dword load at 0030E69C and takes the unit back at 0030E6D9).
Measured against the committed censuses with the same seeds: battle unit 1836 -> 2203 census rows
(distinct sites +366 / -2; the installer 0023A570's thirty accesses are among the gains, the two
losses are AiOrder_EvaluateTargetSelector's `[rbx + r8 + 8]` with rbx an index, filed at +0xBE0 -
WRONG, not missing), actor storage 954 -> 1042 (+119 / -24, the losses all context reads), spawn
record array census unchanged at 106, spawn hop census 358 -> 362 in 79 functions.
MANUAL PATH CUTS, added 2026-09-13 (FABLE, OPUS-REQ-FABLE-STATEBLOCK-ROUTE-CONTAMINATION). The rebasing defect above
has no automatic repair, but a pivot that has been READ can be declared: `--cut FN:ADDR` drops every tracked register
at ADDR inside FN, for a label reached only by jumps from a path whose state differs. `--routes FILE` writes every
propagated (callee, arg, base) with ALL its routes, where the census column shows only the first. A cut is proven by
a diff: rows that vanish must vanish with every route they had, and the cut run must add nothing. Battle_ProcessActionTarget
00307300 sets rbx = stats record in the loop 003073F0..00307452, which leaves by `jmp 00307B91`. The label 00307457 is
reached only from 003073E0, where rbx = the target unit (r8, 0030733A). The battle-state block census lost 91 rows to
`--cut 00307300:00307457` and gained none.

Every rule was tested by reading the disassembly at the kill site before it was adopted; the
--killlog option prints the sites so the next change can be tested the same way. Still linear:
rule 4 trusts address order, so a slot stored on two paths is read as its later store.

STORED-POINTER FOLLOW, added 2026-09-21 (SWE2-FRONTIER, the "next F-6 step" named in FABLE.md).
`mov [obj+X], reg` where reg is tracked publishes the value into a slot; a later qword load of
the same slot re-establishes it - rec, array-base and container values all follow. The slot is
keyed on (base register, displacement) and is only trusted while the base register's write
version is unchanged: any write to the base, a volatile clobber by a call, or a push/pop moving
rsp invalidates every slot published through it. A slot overwritten with a non-tracked value is
poisoned, not merely forgotten. rip-based slots never version out, so a record stored into a
global and loaded back inside the same function is followed for free. The follow is
INTRA-FUNCTION: a record stored into a container in a caller and loaded by a callee still needs
--ctxseed/--argseed - this does not propagate stores across the call boundary.
"""
import sys, struct, argparse, re, bisect, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM
import kit_paths as KP  # noqa: E402
import os
EXE = os.path.join(KP.ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
BASE = 0x120000
ap = argparse.ArgumentParser()
ap.add_argument("--hop", type=lambda s: int(s, 16))
ap.add_argument("--array")
ap.add_argument("--size", type=lambda s: int(s, 16), required=True)
ap.add_argument("--control", required=True)
ap.add_argument("--depth", type=int, default=2)
ap.add_argument("--retseed", default="", help="comma-separated entries of functions known to return the record in rax")
ap.add_argument("--only", default="", help="debug: scan only this function (hex) and trace tracked registers")
ap.add_argument("--gptr", default="", help="comma-separated global pointer seeds ADDR[:OFFSET]: a qword load from [rip+ADDR] yields record+OFFSET")
ap.add_argument("--ctxseed", default="", help="comma-separated container seeds FUNC:ARGIDX: at FUNC's entry that argument register holds a container whose qword at --recptr is the record")
ap.add_argument("--recptr", type=lambda s: int(s, 16), default=None, help="displacement of the record pointer inside a --ctxseed container")
ap.add_argument("--ctxret", default="", help="comma-separated functions that return the CONTAINER in rax (the record is its qword at --recptr); containers are also followed through argument registers and learned at ret")
ap.add_argument("--argseed", default="", help="comma-separated argument seeds FUNC:ARGIDX[:OFFSET]: at FUNC's entry, argument register ARGIDX (0=rcx,1=rdx,2=r8,3=r9) holds record+OFFSET")
ap.add_argument("--out", required=True)
ap.add_argument("--cut", default="", help="FN:ADDR,...: at ADDR inside FN every tracked register is dropped (a READ label reached only by jumps from a path with different state)")
ap.add_argument("--routes", default="", help="write every propagated (callee,arg,base) with ALL its routes as JSON")
ap.add_argument("--killlog", default="", help="diagnostic: log every non-epilogue home-slot reload that kills a tracked callee-saved register, with the slot's spill history (NEVER_STORED / OTHER_STORE / SPILLED_SAME)")
ap.add_argument("--nospillfollow", dest="spillfollow", action="store_false", help="disable spill-follow: a qword reload from a frame slot last stored from a tracked register no longer re-establishes that value")
a = ap.parse_args()
KILLLOG = open(a.killlog, "w", encoding="utf-8") if a.killlog else None
if KILLLOG: KILLLOG.write(chr(9).join(["function","name","site","reg","slot","offset","class","route"]) + chr(10))
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    vs = struct.unpack_from("<I", d, o + 8)[0]; va = struct.unpack_from("<I", d, o + 12)[0]; ro = struct.unpack_from("<I", d, o + 20)[0]
    secs.append((va, vs, ro))
def off(addr):
    r = addr - BASE
    for va, vs, ro in secs:
        if va <= r < va + vs: return ro + (r - va)
funcs = {}; names = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    if not p or p[0] == "entry": continue
    try: e = int(p[0], 16)
    except ValueError: continue
    funcs[e] = int(p[2]); names[e] = p[1]
ents = sorted(funcs)
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
ARGS = ["rcx", "rdx", "r8", "r9"]
_m = {"eax": "rax", "ax": "rax", "al": "rax", "ecx": "rcx", "cx": "rcx", "cl": "rcx", "edx": "rdx", "dx": "rdx", "dl": "rdx",
      "ebx": "rbx", "bx": "rbx", "bl": "rbx", "esi": "rsi", "si": "rsi", "sil": "rsi", "edi": "rdi", "di": "rdi", "dil": "rdi",
      "ebp": "rbp", "bp": "rbp", "bpl": "rbp", "esp": "rsp", "sp": "rsp"}
def canon(reg):
    if reg in _m: return _m[reg]
    mm = re.match(r"^r(\d+)[dwb]?$", reg)
    return "r" + mm.group(1) if mm else reg
WRITERS = {"mov", "movups", "movaps", "movss", "movsd", "movdqa", "movdqu", "movq", "movd", "movzx", "movsx", "movsxd", "cvttss2si"}
RMW = {"or", "and", "add", "sub", "xor", "inc", "dec", "bts", "btr", "btc", "not", "neg", "shl", "shr", "sar", "adc", "sbb", "xchg", "cmpxchg"}
array_addr = array_stride = None; array_base = 0
if a.array:
    parts = a.array.split(":"); array_addr = int(parts[0], 16); array_stride = int(parts[1], 16)
    if len(parts) > 2: array_base = int(parts[2], 16)   # records start at *(addr) + base
CUTS = set((int(x.split(':')[0], 16), int(x.split(':')[1], 16)) for x in a.cut.split(',') if x)
ctrl_fn, ctrl_disp = [int(x, 16) for x in a.control.split(":")]
rows = []; ctrl_hit = False
calls_out = collections.defaultdict(set)   # (callee, argidx, baseoff) -> set(route)
returns_rec = {}                            # entry -> base offset of the record it returns in rax
gptrs = {}                                  # global address -> base offset of the record its qword points at
for x in [s for s in a.gptr.split(",") if s]:
    if ":" in x:
        ga, go = x.split(":"); gptrs[int(ga, 16)] = -int(go.lstrip("-"), 16) if go.startswith("-") else int(go, 16)
    else:
        gptrs[int(x, 16)] = 0
argseeds = {}                               # entry -> (arg index, base offset) seeded at that function's entry
for x in [s for s in a.argseed.split(",") if s]:
    parts = x.split(":"); ao = 0
    if len(parts) > 2: ao = -int(parts[2].lstrip("-"), 16) if parts[2].startswith("-") else int(parts[2], 16)
    argseeds[int(parts[0], 16)] = (int(parts[1]), ao)
ctxseeds = {}                               # entry -> arg index holding the container
for x in [s for s in a.ctxseed.split(",") if s]:
    parts = x.split(":"); ctxseeds[int(parts[0], 16)] = int(parts[1])
ctxrets = set(int(x, 16) for x in a.ctxret.split(",") if x)   # declared container-returning functions
returns_ctx = set()                          # learned: functions that return a container in rax
ctx_out = collections.defaultdict(set)       # (callee, argidx) -> set(route): a container passed in an argument register
def seed_pre(e):
    return {ARGS[argseeds[e][0]]: argseeds[e][1]} if e in argseeds else {}
def seed_ctx(e):
    return {ARGS[ctxseeds[e]]} if e in ctxseeds else set()
for x in [s for s in a.retseed.split(",") if s]:
    # ADDR or ADDR:OFFSET — the function returns (record + OFFSET) in rax; OFFSET may be negative
    if ":" in x:
        fa, fo = x.split(":"); returns_rec[int(fa, 16)] = -int(fo.lstrip("-"), 16) if fo.startswith("-") else int(fo, 16)
    else:
        returns_rec[int(x, 16)] = 0         # declared record-returning functions (seeds)


_cookie_cache = {}
def is_cookie_check(tgt):
    if tgt in _cookie_cache: return _cookie_cache[tgt]
    r = False
    o = off(tgt)
    if o is not None and tgt in funcs:
        for ins in md.disasm(d[o:o + 16], tgt):
            r = ins.mnemonic == "cmp" and ins.op_str.startswith("rcx, qword ptr [rip")
            break
    _cookie_cache[tgt] = r
    return r

def scan(entry, pre, route, ctx=None):
    """pre: dict reg -> base offset tracked from entry. Returns nothing; appends rows and queued calls."""
    global ctrl_hit
    o = off(entry); size = funcs.get(entry, 0)
    if o is None or size <= 0: return
    code = d[o:o + size]
    rec = dict(pre); arr = set(); offs = set(); ctxr = set(ctx or ())
    stores = {}   # (base, disp) -> last store: ("rec", offset) or ("other", text)
    ptrstores = {}   # (canon base, disp) -> ("rec"/"arr"/"ctx"/"other", offset, base write version)
    regver = collections.Counter()   # write version per register; a slot is trusted only while its base's version matches
    insns = list(md.disasm(code, entry))
    # Epilogue membership: from an instruction forward to the next ret, only restores, pops and
    # stack-pointer adjustments. A `mov reg, [rsp+X]` outside such a run is a home-slot reload of
    # some other value and kills the tracked register (the interpreter reloads its context into r13
    # after using r13 for a record it fetched - 0025E61B and nine more - and the first exemption
    # kept r13 'the record' for the rest of a 14 KB function).
    epi = [False] * len(insns); run_ok = False
    # An epilogue run ends at `ret` OR at a tail `jmp` to a function entry (MSVC tail-calls the
    # last callee; 00233F70/00234200/00300FC0/002E5750 all restore rbx then `jmp callee`). Inside the
    # run: pops, restores from the frame, rsp adjustments, the security-cookie sequence
    # (`mov rcx,[rsp+X]; xor rcx,rsp; call __security_check_cookie`, 002350C0), and plain stores to
    # memory the compiler scheduled between restores (0046BAC0's `mov [r13+0x1f8], ebp`).
    for i in range(len(insns) - 1, -1, -1):
        ins = insns[i]; ops = ins.operands
        if ins.mnemonic == "ret": run_ok = True
        elif ins.mnemonic == "jmp" and ops and ops[0].type == X86_OP_IMM and ops[0].imm in funcs and ops[0].imm != entry: run_ok = True
        elif run_ok and (ins.mnemonic == "pop"
                         or (ins.mnemonic in ("mov", "movaps", "movdqa", "movups") and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM and ops[1].mem.base and ins.reg_name(ops[1].mem.base) in ("rsp", "rbp"))
                         or (ins.mnemonic in ("add", "lea", "sub") and ops and ops[0].type == X86_OP_REG and ins.reg_name(ops[0].reg) == "rsp")
                         or (ins.mnemonic == "xor" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG and (ops[0].reg == ops[1].reg or ins.reg_name(ops[1].reg) == "rsp"))
                         or (ins.mnemonic == "call" and ops and ops[0].type == X86_OP_IMM and is_cookie_check(ops[0].imm))
                         or (ins.mnemonic in ("mov", "movaps", "movdqa", "movups") and len(ops) == 2 and ops[0].type == X86_OP_MEM)):
            pass
        else:
            run_ok = False
        epi[i] = run_ok and ins.mnemonic not in ("ret", "jmp")
    for i_ins, ins in enumerate(insns):
        ops = ins.operands; regs = ins.reg_name
        if (entry, ins.address) in CUTS: rec.clear(); arr.clear(); offs.clear(); ctxr.clear()   # --cut
        if a.only: print(f"    {ins.address:08X} {ins.mnemonic} {ins.op_str}   rec={dict(rec)}")
        for idx, op in enumerate(ops):
            if op.type != X86_OP_MEM: continue
            if ins.mnemonic.startswith("nop"): continue      # a multi-byte NOP's operand is padding, not an access (TWOREG, 2026-09-12: 36 rows)
            b = regs(op.mem.base) if op.mem.base else None
            ix = regs(op.mem.index) if op.mem.index else None
            bc = canon(b) if b else None
            hit = None
            if bc in rec:
                hit = rec[bc] + op.mem.disp
            elif array_addr is not None and bc in arr and ix and op.mem.scale == 1 and canon(ix) in offs:
                hit = op.mem.disp - array_base
            if hit is not None and 0 <= hit < a.size:
                kind = "r"
                if idx == 0 and ins.mnemonic in WRITERS: kind = "w"
                elif idx == 0 and ins.mnemonic in RMW: kind = "rw"
                if ins.mnemonic.startswith(("cmp", "test")) or ins.mnemonic == "bt": kind = "r"
                if ins.mnemonic == "lea": kind = "addr"
                # A second register in the operand. Scaled (idx*4 ...) is ordinary array indexing off
                # the record and the displacement is the array's base. UNSCALED with an index register
                # this scan does not know as an offset is `record + disp + something`: the literal
                # displacement is NOT the field (OPUS-NOTICE-CENSUS-TWOREG, 2026-09-12 - 00386E43's
                # `[r14 + r12 - 0x60]` with r14 = result + 0xBC and r12 = -0x60 + s was filed at the
                # stats record's +0x5C). Such rows are kept, marked `idx?`, and the store importer sets
                # them aside instead of proposing a field.
                if not ix: note = ""
                elif op.mem.scale != 1: note = f"idx*{op.mem.scale}"
                elif canon(ix) in offs: note = "idx*1"
                else: note = "idx?"
                rows.append((entry, names[entry], ins.address, hit, kind, f"{ins.mnemonic} {ins.op_str}", route, note))
                if entry == ctrl_fn and hit == ctrl_disp: ctrl_hit = True
        # calls: propagate tracked pointers sitting in argument registers
        if ins.mnemonic in ("call", "jmp") and ops and ops[0].type == X86_OP_IMM:
            tgt = ops[0].imm
            if tgt in funcs and tgt != entry:
                for ai, r in enumerate(ARGS):
                    if r in rec:
                        calls_out[(tgt, ai, rec[r])].add(f"{route}>{entry:08X}@{ins.address:08X}")
                    elif r in ctxr:
                        ctx_out[(tgt, ai)].add(f"{route}>{entry:08X}@{ins.address:08X}")
        dst = None
        if ops and ops[0].type == X86_OP_REG and ins.mnemonic not in ("cmp", "test", "bt", "push", "bts", "btr", "pop") :
            dst = canon(regs(ops[0].reg))
        # An epilogue restore (mov reg, [rsp+X] / pop reg) is path-insensitive noise for a linear scan:
        # the blocks after an early-return epilogue still hold the record in the callee-saved
        # register on the path that reaches them. Do not treat restores as kills.
        if ins.mnemonic == "mov" and len(ops) == 2 and ops[1].type == X86_OP_MEM and ops[1].mem.base and regs(ops[1].mem.base) in ("rsp", "rbp") and dst in rec and dst not in VOLATILE and epi[i_ins] and ops[0].size == 8:
            dst = None
        spillrestore = None
        if ins.mnemonic == "mov" and len(ops) == 2 and ops[1].type == X86_OP_MEM and ops[1].mem.base and regs(ops[1].mem.base) in ("rsp", "rbp") and not ops[1].mem.index and dst in rec and dst not in VOLATILE and not epi[i_ins]:
            slot = (regs(ops[1].mem.base), ops[1].mem.disp)
            last = stores.get(slot)
            if last is None: cls = "NEVER_STORED"
            elif last[0] == "rec" and last[1] == rec[dst]: cls = "SPILLED_SAME"
            elif last[0] == "rec": cls = f"SPILLED_REC_OFF+0x{last[1]:X}"
            else: cls = "OTHER_STORE:" + last[1]
            if KILLLOG: KILLLOG.write(chr(9).join([f"{entry:08X}", names[entry], f"{ins.address:08X}", dst, f"{slot[0]}+0x{slot[1]:X}", f"0x{rec[dst]:X}", cls, route]) + chr(10))

        # A qword reload from a slot whose last recorded store was a tracked register re-establishes
        # that value for ANY destination register, tracked or not - BattleStats_ChangeStatusAndProcessSideEffects
        # spills the unit at 0030E3B6, loses rbx to a dword argument load at 0030E69C, and takes the unit
        # back from the slot at 0030E6D9 for the rest of the function.
        if a.spillfollow and ins.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[0].size == 8 and ops[1].type == X86_OP_MEM and ops[1].mem.base and regs(ops[1].mem.base) in ("rsp", "rbp") and not ops[1].mem.index:
            last = stores.get((regs(ops[1].mem.base), ops[1].mem.disp))
            if last is not None and last[0] == "rec": spillrestore = last[1]
        if ins.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[0].mem.base and regs(ops[0].mem.base) in ("rsp", "rbp") and not ops[0].mem.index:
            slot = (regs(ops[0].mem.base), ops[0].mem.disp)
            if ops[1].type == X86_OP_REG and canon(regs(ops[1].reg)) in rec and ops[1].size == 8: stores[slot] = ("rec", rec[canon(regs(ops[1].reg))])
            else: stores[slot] = ("other", ins.op_str)
        # Stored-pointer follow: publish tracked values stored into ANY slot, keyed on
        # (base register, disp) + the base's write version. A non-tracked qword or any
        # narrower store poisons the slot; an indexed store form is not a fixed field slot.
        if ins.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[0].mem.base and not ops[0].mem.index:
            pb = canon(regs(ops[0].mem.base))
            sval = ("other", 0, 0)
            if ops[1].type == X86_OP_REG and ops[0].size == 8:
                s = canon(regs(ops[1].reg))
                if s in rec: sval = ("rec", rec[s], regver[pb])
                elif s in arr: sval = ("arr", 0, regver[pb])
                elif s in ctxr: sval = ("ctx", 0, regver[pb])
            ptrstores[(pb, ops[0].mem.disp)] = sval
        newrec = None; newarr = False; newoff = False; newctx = False
        if ins.mnemonic == "mov" and len(ops) == 2:
            if ops[1].type == X86_OP_MEM:
                b = regs(ops[1].mem.base) if ops[1].mem.base else None
                if a.recptr is not None and b and canon(b) in ctxr and ops[1].mem.disp == a.recptr and ops[0].size == 8 and not ops[1].mem.index:
                    newrec = 0                                          # the record pointer, loaded out of a seeded container
                if a.hop is not None and ops[1].mem.disp == a.hop and ops[0].size == 8 and b and canon(b) not in rec:
                    newrec = 0
                if array_addr is not None and b == "rip" and ops[0].size == 8 and ins.address + ins.size + ops[1].mem.disp == array_addr:
                    newarr = True
                if gptrs and b == "rip" and ops[0].size == 8 and (ins.address + ins.size + ops[1].mem.disp) in gptrs:
                    newrec = gptrs[ins.address + ins.size + ops[1].mem.disp]   # a global pointer to the record
                if ops[0].size == 8 and not ops[1].mem.index and b and newrec is None and not newarr:
                    st = ptrstores.get((canon(b), ops[1].mem.disp))
                    if st and st[2] == regver.get(canon(b), 0):   # a value published into this slot, base unwritten since
                        if st[0] == "rec": newrec = st[1]
                        elif st[0] == "arr": newarr = True
                        elif st[0] == "ctx": newctx = True
            elif ops[1].type == X86_OP_REG and ops[0].size == 8:
                s = canon(regs(ops[1].reg))
                if s in rec: newrec = rec[s]
                if s in arr: newarr = True
                if s in offs: newoff = True
                if s in ctxr: newctx = True
        elif ins.mnemonic == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM:
            b = regs(ops[1].mem.base) if ops[1].mem.base else None
            ix = regs(ops[1].mem.index) if ops[1].mem.index else None
            bc = canon(b) if b else None
            if bc in rec and not ix: newrec = rec[bc] + ops[1].mem.disp
            elif array_addr is not None and bc in arr and ix and canon(ix) in offs and ops[1].mem.scale == 1: newrec = ops[1].mem.disp - array_base
            elif array_addr is not None and ix and canon(ix) in arr and bc in offs and ops[1].mem.scale == 1: newrec = ops[1].mem.disp - array_base
        elif ins.mnemonic == "imul" and array_addr is not None and ((len(ops) == 3 and ops[2].type == X86_OP_IMM and ops[2].imm == array_stride) or (len(ops) == 2 and ops[1].type == X86_OP_IMM and ops[1].imm == array_stride)):
            newoff = True
        elif ins.mnemonic == "add" and len(ops) == 2:
            if ops[1].type == X86_OP_REG and array_addr is not None:
                s = canon(regs(ops[1].reg))
                if (dst in offs and s in arr) or (dst in arr and s in offs): newrec = 0
            if ops[1].type == X86_OP_REG and newrec is None:
                s = canon(regs(ops[1].reg))
                if s in rec and dst not in rec: newrec = rec[s]        # idx += record  -> record + idx (index dropped)
                elif dst in rec and s not in rec: newrec = rec[dst]    # record += idx  -> still the record (index dropped)
            elif ops[1].type == X86_OP_MEM and array_addr is not None and dst in offs:
                b = regs(ops[1].mem.base) if ops[1].mem.base else None
                if b == "rip" and ins.address + ins.size + ops[1].mem.disp == array_addr: newrec = 0
            elif ops[1].type == X86_OP_MEM and gptrs and ops[1].mem.base and regs(ops[1].mem.base) == "rip" and (ins.address + ins.size + ops[1].mem.disp) in gptrs:
                newrec = gptrs[ins.address + ins.size + ops[1].mem.disp]   # add idx, [global ptr] -> record + idx (index dropped)
            elif ops[1].type == X86_OP_IMM and dst in rec: newrec = rec[dst] + ops[1].imm
        elif ins.mnemonic == "sub" and len(ops) == 2 and ops[1].type == X86_OP_IMM and dst in rec:
            newrec = rec[dst] - ops[1].imm
        if dst:
            regver[dst] += 1   # any write invalidates slots published through this register
            rec.pop(dst, None); arr.discard(dst); offs.discard(dst); ctxr.discard(dst)
            if newctx: ctxr.add(dst)
            if newrec is None and spillrestore is not None: newrec = spillrestore
            if newrec is not None: rec[dst] = newrec
            if newarr: arr.add(dst)
            if newoff: offs.add(dst)
        if ins.mnemonic.startswith("call"):
            for r in list(rec):
                if r in VOLATILE: rec.pop(r)
            for r in VOLATILE: regver[r] += 1   # the callee may have clobbered it; its published slots are stale
            arr -= VOLATILE; offs -= VOLATILE; ctxr -= VOLATILE
            if ops and ops[0].type == X86_OP_IMM and ops[0].imm in returns_rec:
                rec["rax"] = returns_rec[ops[0].imm]      # the callee returns a record pointer
            if ops and ops[0].type == X86_OP_IMM and (ops[0].imm in ctxrets or ops[0].imm in returns_ctx):
                ctxr.add("rax")                            # the callee returns the container
        if ins.mnemonic in ("push", "pop"): regver["rsp"] += 1   # the stack pointer moved; rsp-keyed slots shifted
        if ins.mnemonic == "pop" and ops and ops[0].type == X86_OP_REG:
            r = canon(regs(ops[0].reg))
            regver[r] += 1
            if r in VOLATILE: rec.pop(r, None); arr.discard(r); offs.discard(r)   # epilogue pops of callee-saved regs are not kills (see above)
        if ins.mnemonic == "ret" and "rax" in rec and entry not in returns_rec:
            returns_rec[entry] = rec["rax"]
        if ins.mnemonic == "ret" and "rax" in ctxr and entry not in ctxrets:
            returns_ctx.add(entry)
        if ins.mnemonic == "jmp" and ops and ops[0].type == X86_OP_IMM and ops[0].imm in returns_rec and "rax" not in rec and entry not in returns_rec and not any(r in rec for r in ARGS):
            pass

if a.only:
    e = int(a.only, 16)
    TRACE = True
    scan(e, seed_pre(e), "seed", seed_ctx(e))
    for r in rows: print(f"  {r[2]:08X} +0x{r[3]:X} {r[4]} {r[5]}")
    print(len(rows), "rows in", a.only, "; returns_rec has", len(returns_rec))
    sys.exit(0)
# pass 0: every function, seeds only — run twice so that record-returning callees found in the
# first pass (returns_rec) seed their callers' rax in the second
for e in ents:
    scan(e, seed_pre(e), "seed", seed_ctx(e))
rows.clear(); calls_out.clear(); ctx_out.clear(); ctrl_hit = False
for e in ents:
    scan(e, seed_pre(e), "seed", seed_ctx(e))
print(f"{len(returns_rec)} record-returning function(s); {len(returns_ctx)} learned container-returning function(s)", file=sys.stderr)
seen = set()
for depth in range(1, a.depth + 1):
    pending = [(k, v) for k, v in calls_out.items() if k not in seen]
    cpending = [(k, v) for k, v in ctx_out.items() if ("ctx",) + k not in seen]
    if not pending and not cpending: break
    for (callee, ai, boff), routes in pending:
        seen.add((callee, ai, boff))
        route = f"arg{ai}+0x{boff:X}<" + sorted(routes)[0].split(">")[-1]
        scan(callee, {ARGS[ai]: boff}, route)
    for (callee, ai), routes in cpending:
        seen.add(("ctx", callee, ai))
        route = f"ctxarg{ai}<" + sorted(routes)[0].split(">")[-1]
        scan(callee, {}, route, {ARGS[ai]})
if a.routes:
    import json
    json.dump({f"{k[0]:08X}:{k[1]}:{k[2]:X}": sorted(v) for k, v in calls_out.items()}, open(a.routes, "w"))
with open(a.out, "w", encoding="utf-8") as f:
    f.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
    for r in rows:
        f.write(f"{r[0]:08X}\t{r[1]}\t{r[2]:08X}\t0x{r[3]:X}\t{r[4]}\t{r[5]}\t{r[6]}\t{r[7]}\n")
print(f"{len(rows)} access(es) in {len(set(r[0] for r in rows))} function(s); {len(seen)} propagated (callee,arg) pairs; control {'FOUND' if ctrl_hit else 'MISSING -- results are not evidence'}")
