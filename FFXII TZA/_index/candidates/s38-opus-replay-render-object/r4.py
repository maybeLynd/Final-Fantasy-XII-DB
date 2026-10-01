"""S-38 R-4 (OPUS, 2026-09-26): the ready latch +0x4B4's readers executed as shipped code over block 353's world (check.py,
imported: its six cases run first, unchanged) - CONTRACT-character-render-object.md R-4: "seventeen byte-width reads in sixteen
functions, and the latch is consulted two different ways" (an entry precondition in twelve methods; a per-element skip term in
slot 16's submission loop).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub. ALLOWED = block 353's set plus the static closures
of the sixteen readers.
Census (static, re-derived here from the whole image, not carried): every instruction with a one-byte memory operand at
displacement 0x4B4, over every function in the graph's function table.
Per reader, the GATE is the first conditional branch after the read; its two successors are SKIP (the latch-clear side) and WORK.
Cases, on an object built by the shipped constructor 001F4DA0 (latch 0 as constructed; latch 1 written by fixture - the setter
001F6E70 is not run):
 C   the census: 17 byte reads in 16 functions (and the 2 byte writes of R-3);
 E   latch 0: each entry-gated reader returns through SKIP, never reaches WORK, enters no function, and writes the object only
     where an instruction before the gate does (reported per reader); latch 1: WORK is reached. OBSERVATION STOP (disclosed): a
     latch-1 run is stopped when it reaches WORK - the body past the gate is outside R-4 and reads state this world does not plant;
 G   the getter 001F86D0 returns the latch byte (0 / 1);
 P2  001F5D70's second read 001F688E, run to the end with NO stop: with the frame byte [01F7F598]+0xC34, +0x4B6, +0x4A8 >= 0.75
     and +0x480 = -1 planted, the body jumps to 001F688E; with the latch set it clears +0x4B5 (001F6899, the run's only object
     write) and returns; with it clear the first read already skips to 001F68A0 and +0x4B5 is kept.
 L   slot 16 001FA3D0: the latch is NOT an entry condition - with it clear, the method runs its setup calls and its submission loop
     and reaches the read at 001FA5C3 per element, where the element is skipped (001FA61E); with it set, the element proceeds
     (001FA5CF). And with the mode word (001A9930() +0x2CC) = 2, the loop bypasses the read altogether (001FA5C1 je 001FA5E4).
Writes r4_result.json.
"""
import json
import os
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RIP

import check as C

HERE = os.path.dirname(os.path.abspath(__file__))
W, S, uc, pe = C.W, C.S, C.uc, C.pe
OBJ = 0x76600000
uc.mem_map(OBJ, 0x10000)

# ---- C: the census, from the image ----
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
reads, writes_b = [], []
for line in open(os.path.join(W.GRAPH, "functions.tsv"), encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    if not p[0][:1] or p[0][:1] not in "0123456789ABCDEF" or len(p) < 3 or not p[2].isdigit():
        continue
    fa, size = int(p[0], 16), int(p[2])
    try:
        code = pe.get_data(fa - 0x120000, size)
    except Exception:
        continue
    for k, i in enumerate(md.disasm(code, fa)):
        for op in i.operands:
            if op.type == X86_OP_MEM and op.mem.disp == 0x4B4 and op.size == 1:
                is_write = i.mnemonic == "mov" and i.operands[0].type == X86_OP_MEM
                (writes_b if is_write else reads).append(["%08X" % fa, k, "%08X" % i.address, i.mnemonic + " " + i.op_str])
readers = sorted({x[0] for x in reads})
case_c = len(reads) == 17 and len(readers) == 16 and [x[2] for x in writes_b] == ["001F4EC9", "001F7729"]


def gate_of(read_addr):
    for i in md.disasm(pe.get_data(read_addr - 0x120000, 64), read_addr):
        if i.mnemonic.startswith("j") and i.mnemonic != "jmp":
            tgt, fall = int(i.op_str, 16), i.address + i.size
            return {"branch": "%08X" % i.address, "cc": i.mnemonic,
                    "skip": tgt if i.mnemonic == "je" else fall, "work": fall if i.mnemonic == "je" else tgt}
        if i.mnemonic == "ret":
            return None
    return None


GETTER, SLOT16 = 0x1F86D0, 0x1FA3D0
COOKIE = "00808C40"                                     # the epilogue's stack-cookie check, the only call a skip path makes
gates = {}
for fn, k, ra, txt in reads:
    if int(fn, 16) in (GETTER, SLOT16):
        continue
    gates.setdefault(fn, []).append(dict(read=ra, index=k, **gate_of(int(ra, 16))))
W.ALLOWED |= set().union(*(W.closure(int(f, 16)) | {int(f, 16)} for f in readers))

# ---- hooks: gate successors, object writes ----
hits, obj_writes, stop_at = [], [], set()
SUCC = {g["skip"] for v in gates.values() for g in v} | {g["work"] for v in gates.values() for g in v} | \
       {0x1FA5C3, 0x1FA5CF, 0x1FA61E, 0x1FA5E4}


def on_succ(u, a, n, _):
    if a in SUCC:
        hits.append(a)
        if a in stop_at:
            u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_succ)
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: obj_writes.append(["+%X" % (a - OBJ), n, "%08X" % u.reg_read(UC_X86_REG_RIP)]),
            begin=OBJ, end=OBJ + 0x667)
uc.ctl_flush_tb()


def build():
    uc.mem_write(OBJ, bytes(0x10000))
    return S.call(C.CTOR, OBJ)


def run(fn, latch, stop=()):
    C.w(OBJ + 0x4B4, "<B", latch)
    del hits[:]
    del obj_writes[:]
    stop_at.clear()
    stop_at.update(stop)
    S.st["entered"] = set()
    ok = S.call(fn, OBJ, 0, 0, 0, stack=(0,) * 6)
    return {"returned": ok, "stopped_at": (S.st["bad"] or S.st["faults"])[:2], "rip": "%08X" % uc.reg_read(UC_X86_REG_RIP),
            "hits": ["%08X" % h for h in hits], "entered": sorted("%08X" % e for e in S.st["entered"] if e != fn),
            "object_writes": list(obj_writes), "rax": uc.reg_read(UC_X86_REG_RAX)}


built = build()
res, cases = {"census": {"reads": reads, "byte_writes": writes_b, "readers": readers}}, {}
cases["C_census_17_reads_16_functions_2_writes"] = case_c

# ---- E: the entry-gated readers ----
ent = {}
PASS_FN = "001F5D70"                                    # its first read follows calls and a scene test: case P
for fn, gl in sorted(gates.items()):
    if fn == PASS_FN:
        continue
    g = gl[0]                                           # the first read in the function (001F5D70's second read: below)
    f = int(fn, 16)
    build()
    r0 = run(f, 0)
    build()
    r1 = run(f, 1, stop=(g["work"],))
    ent[fn] = {"gate": {k: ("%08X" % v if isinstance(v, int) and k in ("skip", "work") else v) for k, v in g.items()},
               "latch0": r0, "latch1": r1,
               "latch0_skips": r0["returned"] and "%08X" % g["skip"] in r0["hits"] and "%08X" % g["work"] not in r0["hits"]
               and set(r0["entered"]) <= {COOKIE},
               "latch1_works": "%08X" % g["work"] in r1["hits"]}
res["entry_readers"] = ent
cases["E_entry_readers_skip_when_clear_and_proceed_when_set"] = all(v["latch0_skips"] and v["latch1_works"] for v in ent.values())

# ---- G: the getter ----
g0, g1 = run(GETTER, 0), run(GETTER, 1)
res["getter"] = {"latch0": g0["rax"] & 0xFF, "latch1": g1["rax"] & 0xFF}
cases["G_getter_returns_the_latch"] = g0["returned"] and g1["returned"] and (g0["rax"] & 0xFF, g1["rax"] & 0xFF) == (0, 1)

# ---- planted singletons for cases P and L (data only) ----
SCENE, MODE, LAZY, RECS, LIST, REC = OBJ + 0x2000, OBJ + 0x3000, OBJ + 0x4000, OBJ + 0x6000, OBJ + 0x8000, OBJ + 0x8100
for cell, blk in ((0x1F811C8, SCENE), (0x1F81168, MODE), (0x1F81428, LAZY), (0x1F7F5E0, OBJ + 0x5000)):
    C.w(cell, "<Q", blk)                                # 001AD440 / 001A9930 / 001D50D0's lazy cell / 0018B4E0


def clear_blocks():
    uc.mem_write(OBJ + 0x2000, bytes(0xE000))


# ---- P: 001F5D70 - the latch read follows three lookups and a scene test ----
pas = {}
for nm, a8, latch in (("scene_a8_ge_minus1", 0, 1), ("latch0", -2, 0), ("latch1", -2, 1)):
    build()
    clear_blocks()
    C.w(SCENE + 0xA8, "<i", a8)
    pas[nm] = run(0x1F5D70, latch, stop=(0x1F5E14,))
res["pass_1F5D70"] = pas
cases["P_1F5D70_reads_latch_after_its_scene_test"] = pas["scene_a8_ge_minus1"]["returned"] and "001F68A0" in pas["scene_a8_ge_minus1"]["hits"]     and pas["latch0"]["returned"] and pas["latch0"]["hits"][:1] == ["001F68A0"] and "001F5E14" not in pas["latch0"]["hits"]     and "001F5E14" in pas["latch1"]["hits"]


# ---- P2: 001F5D70's second read 001F688E, run to the function's end with no stop ----
# 001F5E3A: with the frame byte [01F7F598]+0xC34 set, +0x4B6 set, +0x4A8 >= 0.75 and +0x480 == -1 the body jumps straight to
# 001F688E (001F5E4B); there the latch is read again and, when set, +0x4B5 is cleared (001F6899).
SUCC.update({0x1F688E, 0x1F6899})
p2 = {}
for nm, latch in (("latch1", 1), ("latch0", 0)):
    build()
    clear_blocks()
    C.w(SCENE + 0xA8, "<i", -2)
    C.w(C.FRAME + 0xC34, "<B", 1)
    C.w(OBJ + 0x4B5, "<B", 1)
    C.w(OBJ + 0x4B6, "<B", 1)
    C.w(OBJ + 0x4A8, "<f", 1.0)
    C.w(OBJ + 0x480, "<i", -1)
    x = run(0x1F5D70, latch)
    x["4B5_after"] = C.r(OBJ + 0x4B5, 1)[0]
    p2[nm] = x
C.w(C.FRAME + 0xC34, "<B", 0)
res["pass_1F5D70_second_read"] = p2
cases["P2_1F5D70_second_read_clears_4B5_when_set"] = p2["latch1"]["returned"] and p2["latch1"]["hits"][:3] == ["001F5E14", "001F688E", "001F6899"] \
    and p2["latch1"]["4B5_after"] == 0 and p2["latch0"]["returned"] and "001F688E" not in p2["latch0"]["hits"] and p2["latch0"]["4B5_after"] == 1


# ---- L: slot 16 - the latch is a per-element term inside the submission loop ----
def slot16(latch, mode):
    build()
    clear_blocks()
    C.w(SCENE + 0x244, "<B", 1)                         # 001ABF50 takes its early exit
    C.w(MODE + 0x2CC, "<i", mode)
    C.w(OBJ + 0x49C, "<I", 7)
    C.w(OBJ + 0x4AC, "<f", 1.0)                         # above the 0.9 threshold (008FCC8C)
    C.w(OBJ + 0x30, "<QQ", LIST, LIST + 8)              # one entry
    C.w(LIST, "<Q", OBJ + 0x8080)
    C.w(OBJ + 0x8080, "<Q", REC)
    C.w(REC, "<IIQ", 1, 0, RECS)                        # one element; element table at RECS (stride 0xC0)
    C.w(RECS + 0x1C, "<III", 7, 1, 2)
    uc.mem_write(OBJ + 0x9000, bytes([1, 2, 5]))        # the pass's (key, key, kind < 0x11)
    C.w(OBJ + 0x4B4, "<B", latch)
    del hits[:]
    del obj_writes[:]
    stop_at.clear()
    stop_at.update({0x1FA5CF, 0x1FA5E4})
    S.st["entered"] = set()
    ok = S.call(SLOT16, OBJ, 1, OBJ + 0x9000, 0, stack=(0,) * 6)
    return {"returned": ok, "stopped_at": (S.st["bad"] or S.st["faults"])[:2], "rip": "%08X" % uc.reg_read(UC_X86_REG_RIP),
            "hits": ["%08X" % h for h in hits], "entered": sorted("%08X" % e for e in S.st["entered"] if e != SLOT16)}


l0, l1, lm = slot16(0, 0), slot16(1, 0), slot16(1, 2)
res["slot16"] = {"latch0": l0, "latch1": l1, "mode2": lm}
cases["L_slot16_latch_is_a_per_element_term_not_an_entry_gate"] =     l0["hits"][:2] == ["001FA5C3", "001FA61E"] and "001FA5CF" not in l0["hits"] and len(l0["entered"]) > 0     and l1["hits"][:2] == ["001FA5C3", "001FA5CF"]     and lm["hits"][:1] == ["001FA5E4"] and "001FA5C3" not in lm["hits"]

out = {"ok": all(cases.values()), "cases": cases, "constructed": built, "allowed_functions": len(W.ALLOWED), **res}
json.dump(out, open(os.path.join(HERE, "r4_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-60s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
