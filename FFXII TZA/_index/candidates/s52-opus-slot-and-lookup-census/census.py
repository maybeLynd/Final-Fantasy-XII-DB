"""S-52 (OPUS, 2026-09-26): CONTRACT-manager-slot-entry-tables section 13's two remaining debts, answered statically - the
fifth-argument (lookupIndex) domain of every shipped caller, and which slot 002640C0 resolves against the one side B is handed.

Evidence: STATIC (the SHA-asserted image) plus a DATA census over the decompiled shipped field scripts (FABLE's corpus,
Tools/work/FABLE/pub140-scratch/corpus/us/*.txt - 1,114 files, the corpus the navigation page's setmapidfloor count used).
Domain: that corpus; other script sources (battle scripts, other languages) are not censused here.
 T1  the four bind callers are the script verbs camerastart_7d (0034F2F0), camerastart_7e (0034F930), camerashakestart_1a2
     (003492F0) and camerashakestart_1a3 (00349730) - the only callers of 003DA400 (A) and 003DD230 (B). Each takes its slot from
     002640C0, pops three VM values with VMValueStack_PopInt32CoerceFloat32 00267E10, and stores the FIRST pop as the fifth
     argument ([rsp+0x20] = ebx). 7e and 1a3 first push -1 (VMValueStack_PushInt32 00267F90 with edx = -1), so their fifth
     argument is always -1; 7d and 1a2 push nothing, so theirs is the script's last argument (LIFO).
 T2  the natives the scripts use for that last argument: getcamerasubframe 0050D1C0 -> 0053DD10 = mov eax, 1; ret (always 1);
     getcameramainframe 0050F100 -> 005C5230 = xor eax, eax; ret (always 0).
 C1  the corpus: every camerastart_7d / camerashakestart_1a2 call's last argument is getcamerasubframe(), getcameramainframe() or
     an integer literal; the largest value any shipped call can pass is the literal 110.
 C2  so the largest shipped lookupIndex is 110: side A stores the reverse-lookup word at slot + 0x18 + 2 * 110 = slot + 0xF4
     (003DA4B9), inside the 0x200-byte slot. No shipped call leaves the slot. (Index > 1 still writes past the two words the
     reset clears - section 14.3 - which is unchanged.) Side B's callers pass -1 or nothing: 1a2 has no call in the corpus.
 T3  002640C0 is mov rax, [02099D70]; ret - the current-manager-slot context. Side A's reset 003DA370 reads it at 003DA38F; side
     B's reset 003DCF60 has one caller, 0034B100, which reads it at 0034B104 and passes it at 0034B109 with nothing between.
     Both sides therefore resolve the SAME slot, by construction, whenever they run from the same context.
Writes result.json.
"""
import glob
import hashlib
import json
import os
import re
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work"))
EXE = os.path.join(TOOLS, "exe", "FFXII_TZA.exe")
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
CORPUS = os.path.join(TOOLS, "FABLE", "pub140-scratch", "corpus", "us")
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
pe = struct.unpack_from("<I", raw, 0x3C)[0]
BASE = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
o = pe + 24 + struct.unpack_from("<H", raw, pe + 20)[0]
secs = []
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, o + 8)
    secs.append((BASE + va, vs, ra))
    o += 40


def at(va, n):
    for v, vs, ra in secs:
        if v <= va < v + vs:
            return raw[ra + va - v:ra + va - v + n]


md = Cs(CS_ARCH_X86, CS_MODE_64)
dis = lambda va, n: [(i.address, i.mnemonic, i.op_str) for i in md.disasm(at(va, n), va)]
HANDLERS = {"camerastart_7d": (0x34F2F0, 0x3DA400), "camerastart_7e": (0x34F930, 0x3DA400),
            "camerashakestart_1a2": (0x3492F0, 0x3DD230), "camerashakestart_1a3": (0x349730, 0x3DD230)}
SIZES = {int(l.split("	")[0], 16): int(l.split("	")[2]) for l in open(os.path.join(TOOLS, "graph", "functions.tsv"), encoding="utf-8", errors="replace")
         if l.split("	")[0] in ("0034F2F0", "0034F930", "003492F0", "00349730")}
T1 = {}
for name, (h, bind) in HANDLERS.items():
    body = dis(h, SIZES[h])                                    # each handler's own extent (functions.tsv), not a fixed window
    calls = [(a, t) for a, m, t in body if m == "call"]
    pushes_minus1 = any(m == "or" and t == "edx, 0xffffffff" for a, m, t in body) and ("0x267f90" in [t for a, t in calls])
    pops = sum(1 for a, t in calls if t == "0x267e10")
    fifth = [t for a, m, t in body if m == "mov" and t.startswith("dword ptr [rsp + 0x20]")]
    T1[name] = {"slot_from_002640C0": "0x2640c0" in [t for a, t in calls], "pushes_minus1": pushes_minus1, "pops": pops,
                "fifth_store": fifth, "binds": "%08X" % bind if ("0x%x" % bind) in [t for a, t in calls] else None}
T2 = {"0050D1C0_calls": [t for a, m, t in dis(0x50D1C0, 0x20) if m == "call"], "0053DD10": dis(0x53DD10, 6)[:2],
      "0050F100_calls": [t for a, m, t in dis(0x50F100, 0x20) if m == "call"], "005C5230": dis(0x5C5230, 3)}
files = sorted(glob.glob(os.path.join(CORPUS, "*.txt")))
counts, lastargs = {}, {}
rx = re.compile(r"(camerastart_7d|camerastart_7e|camerashakestart_1a2|camerashakestart_1a3)\((.*)\);")
for p in files:
    for line in open(p, encoding="utf-8", errors="replace"):
        m = rx.search(line)
        if not m:
            continue
        counts[m.group(1)] = counts.get(m.group(1), 0) + 1
        if m.group(1) in ("camerastart_7d", "camerashakestart_1a2"):
            last = m.group(2).rsplit(",", 1)[-1].strip()
            lastargs[last] = lastargs.get(last, 0) + 1
value = {"getcamerasubframe()": 1, "getcameramainframe()": 0}
lit = {k: int(k, 0) for k in lastargs if re.fullmatch(r"-?(0x[0-9a-fA-F]+|\d+)", k)}
max_index = max([value.get(k, lit.get(k)) for k in lastargs if k in value or k in lit] + [0])
T3 = {"002640C0": dis(0x2640C0, 8), "reset_A_reads": [a for a, m, t in dis(0x3DA370, 0x30) if m == "call" and t == "0x2640c0"],
      "reset_B_caller": dis(0x34B100, 0x10)[:3]}
R = {"T1": T1, "T2": T2, "corpus_files": len(files), "C1_counts": counts, "C1_last_args_7d_1a2": lastargs, "C2_max_index": max_index,
     "C2_store_offset": "%X" % (0x18 + 2 * max_index), "T3": T3}
T3_ok = (T3["002640C0"][0][2] == "rax, qword ptr [rip + 0x1e35ca9]" and T3["002640C0"][1][1] == "ret"
         and 0x2640C0 + 7 + 0x1E35CA9 == 0x2099D70 and T3["reset_A_reads"] == [0x3DA38F]
         and T3["reset_B_caller"][1][1:] == ("call", "0x2640c0") and T3["reset_B_caller"][2][1:] == ("mov", "rcx, rax"))
cases = {
    "T1_four_handlers_slot_from_002640C0_three_pops_first_pop_is_arg5": all(v["slot_from_002640C0"] and v["pops"] == 3 and v["fifth_store"] == ["dword ptr [rsp + 0x20], ebx"]
                                                                          and v["binds"] for v in T1.values()),
    "T1_7e_and_1a3_push_minus1_7d_and_1a2_do_not": T1["camerastart_7e"]["pushes_minus1"] and T1["camerashakestart_1a3"]["pushes_minus1"]
        and not T1["camerastart_7d"]["pushes_minus1"] and not T1["camerashakestart_1a2"]["pushes_minus1"],
    "T2_subframe_is_1_mainframe_is_0": T2["0050D1C0_calls"] == ["0x53dd10"] and T2["0053DD10"][0][2] == "eax, 1" and T2["0050F100_calls"] == ["0x5c5230"]
        and T2["005C5230"][0][1:] == ("xor", "eax, eax"),
    "C1_corpus_last_args_are_the_two_natives_or_literal_110": len(files) == 1114 and set(lastargs) <= {"getcamerasubframe()", "getcameramainframe()", "110"}
        and lastargs.get("110") == 1 and counts.get("camerashakestart_1a2", 0) == 0,
    "C2_max_index_110_stores_at_F4_inside_the_0x200_slot": max_index == 110 and 0x18 + 2 * max_index < 0x200,
    "T3_both_resets_read_the_current_slot_context_02099D70": T3_ok,
}
res = {"static": True, "domain": "image sha256 %s; corpus %d decompiled us field scripts" % (SHA[:16], len(files)), "results": R, "cases": cases,
       "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-66s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({"counts": counts, "last_args": lastargs, "max_index": max_index}))
print("ALL PASS" if res["ok"] else "FAILED")
raise SystemExit(0 if res["ok"] else 1)
