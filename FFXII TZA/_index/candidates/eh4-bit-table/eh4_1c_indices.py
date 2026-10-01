"""EH-4: the producer disposition of every index of the actor storage record's +0x1C request word (OPUS, 2026-09-27).

A bit of +0x1C can become 1 only through a writer. The writers on the actor record are:
  - the initialiser's whole-word kind-row presets (00266BD0; eh4-1c-presets/),
  - the initialiser's and the battle-unit refresh's masked read-modify-writes, which touch only 2, 8, 10 and 13,
  - the index setter 0026B4A0 / clearer 0025D5E0, called with an engine literal or with a script's reqenable /
    reqdisable argument (the census of every shipped script's call, Tools/work/data/census_verb_args.tsv: all literal).
The record block is memset to zero before the initialiser runs (eh4-rekey/, OPUS 2026-09-27).

  W1 every 4-byte non-read-modify-write store at +0x1C on a census receiver (actor-storage-record-flag-bit-writes.tsv,
     in_access_census = y) is either a 00266BD0 preset or one of the interpreter's three call-result stores at
     00261B5E / 00261C5B / 00261D04 - whose base is rsi = the interpreter's THIRD argument (mov rsi, r8 at 0025E4E6),
     while the record is r15 = its second (mov r15, rdx at 0025E4D5): VM state, not the record
  W2 the engine's literal index sites: set 8 and 13 (00355A71 / 00355A7E), set and clear 10 (00238DAE / 00238DDE),
     clear 3 (00355A8B); the other callers pass a register (reqenable 0035555B, reqdisable 0035590B) or load it earlier
  W3 the script census: reqenable literals are exactly {2,3,4,5,7,8,11,12,13,14,16,17}, and no call is non-literal
  N  NEVER SET = the indices no preset, masked writer, engine literal or script literal produces: {1, 9, 15, 18..31}.
     Together with the zeroed block they read zero in every record in the shipped build.
  U  index 12 is set by scripts (1,525 reqenable) and has no reqdisable clear
Not claimed: what any produced index means (the page names 2, 8, 10 and 13), or code outside the listed bodies.
Writes eh4-1c-indices.tsv beside this file.
"""
import csv, os, struct, sys, ast, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, CS_OP_MEM

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DB = ROOT / "Database"
d = (DB / "Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
def ins_at(a, n=16): return next(iter(cs.disasm(d[off(a):off(a) + n], a)))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok

# presets (decoded exactly as eh4-1c-presets/eh4_1c_presets.py C2)
TABLE = 0x266C30; presets = {}
for r in range(8):
    t = BASE + struct.unpack_from("<I", d, off(TABLE) + 4 * r)[0]
    for x in cs.disasm(d[off(t):off(t) + 0x40], t):
        if x.mnemonic == "ret": break
        o = x.operands
        if x.mnemonic == "mov" and o[0].type == CS_OP_MEM and o[0].mem.disp == 0x1C and o[0].size == 4 and o[1].type == CS_OP_IMM:
            presets[r] = o[1].imm & 0xFFFFFFFF; break
preset_bits = {b for v in presets.values() for b in range(32) if v >> b & 1}

# W1 whole-word stores on census receivers
W = DB / "FFXII TZA/04-Actor-Entity/Actor-Storage-Record/actor-storage-record-flag-bit-writes.tsv"
rows = [r for r in csv.DictReader(open(W, encoding="utf-8"), delimiter="\t") if r["disp"] == "0x1C" and r["in_access_census"] == "y"]
whole = [r for r in rows if r["op"] == "copy" and r["width"] == "4"]
interp = {r["site"] for r in whole if r["function"] == "0025E4C0"}
pre = {r["site"] for r in whole if r["function"] == "00266BD0"}
rsi_arg = ins_at(0x25E4E6); r15_arg = ins_at(0x25E4D5)
check("W1 whole-word +0x1C stores: the presets and the interpreter's three VM-state stores",
      len(whole) == len(interp) + len(pre) and interp == {"00261B5E", "00261C5B", "00261D04"} and len(pre) == 5
      and (rsi_arg.mnemonic, rsi_arg.op_str) == ("mov", "rsi, r8") and (r15_arg.mnemonic, r15_arg.op_str) == ("mov", "r15, rdx")
      and all("[rsi + 0x1c]" in r["instruction"] for r in whole if r["function"] == "0025E4C0"),
      "(%d stores: %d presets, %d interpreter)" % (len(whole), len(pre), len(interp)))
rmw = {b for r in rows if r["op"] in ("set", "clear") and r["width"] == "4" and r["source_class"].startswith("imm:")
       for b in range(32) if ((int(r["source_class"][4:], 16) if r["op"] == "set" else ~int(r["source_class"][4:], 16)) >> b) & 1}

# W2 engine literal index sites (decoded from the owning function's entry, so no mid-instruction start)
import bisect
sizes = {}
for l in open(DB / "Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("	")
    try: sizes[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
keys = sorted(sizes)
def before(site, k=8):
    f = keys[bisect.bisect_right(keys, site) - 1]
    xs = list(cs.disasm(d[off(f):off(f) + sizes[f]], f))
    i = next(j for j, x in enumerate(xs) if x.address == site)
    return xs[max(0, i - k):i], xs[i]
LIT = {0x355A71: ("set", 8), 0x355A7E: ("set", 13), 0x238DAE: ("set", 10), 0x238DDE: ("clear", 10), 0x355A8B: ("clear", 3)}
okw2 = True; seen = []
for site, (kind, idx) in LIT.items():
    tgt = 0x26B4A0 if kind == "set" else 0x25D5E0
    prev, call = before(site)
    lits = [x.operands[1].imm for x in prev if x.mnemonic == "mov" and x.operands and x.operands[0].type != CS_OP_MEM
            and x.reg_name(x.operands[0].reg) == "edx" and x.operands[1].type == CS_OP_IMM]
    good = call.mnemonic in ("call", "jmp") and call.operands[0].imm == tgt and bool(lits) and lits[-1] == idx
    okw2 &= good; seen.append("%X:%s" % (site, lits[-1] if lits else None))
check("W2 the engine's literal index sites set 8, 13, 10 and clear 10, 3", okw2, "(%s)" % " ".join(seen))
engine_set = {8, 13, 10, 11}   # 11: verb camerachange (00351F40) loads edx = 11 before its call at 00351F7C
cam = [x for x in cs.disasm(d[off(0x351F40):off(0x351F7C)], 0x351F40) if x.mnemonic == "mov" and x.op_str == "edx, 0xb"]
check("W2b camerachange's index is 11", bool(cam))

# W3 script literals
C = DB / "Tools/work/data/census_verb_args.tsv"
en = collections.Counter(); dis = collections.Counter(); nonlit = 0
for r in csv.DictReader(open(C, encoding="utf-8"), delimiter="\t"):
    if r["verb"] not in ("reqenable", "reqdisable"): continue
    a = ast.literal_eval(r["arg"])
    if a[0] != "lit": nonlit += 1; continue
    (en if r["verb"] == "reqenable" else dis)[a[1]] += 1
script_set = set(en)
check("W3 script reqenable literals are {2,3,4,5,7,8,11,12,13,14,16,17}, none computed",
      script_set == {2, 3, 4, 5, 7, 8, 11, 12, 13, 14, 16, 17} and nonlit == 0, "(%s)" % sorted(script_set))

produced = preset_bits | (rmw & {2, 10}) | engine_set | script_set
never = sorted(set(range(32)) - produced)
check("N never set: {1, 9, 15, 18..31}", never == [1, 9, 15] + list(range(18, 32)), "(%s)" % never)
check("U index 12 is set by scripts and never cleared by one", en[12] > 0 and dis[12] == 0, "(%d enables)" % en[12])

NAMED = {2: "entry-group first slot, superseded by 10 (page, fifteenth pass)", 10: "entry-group second slot (page, fifteenth pass)",
         8: "overhead-display eligibility pair with 13 (page, sixteenth pass)", 13: "overhead-display eligibility pair with 8 (page, sixteenth pass)"}
with open(HERE / "eh4-1c-indices.tsv", "w", newline="") as w:
    w.write("index\tdisposition\tpreset_rows\tengine\tscript_enables\tscript_disables\tmeaning\n")
    for b in range(32):
        rowsb = ",".join(str(r) for r, v in sorted(presets.items()) if v >> b & 1)
        eng = ("set" if b in engine_set or (b in rmw and b in (2, 10)) else "") + ("/clear" if b in (3, 10) or b in rmw else "")
        if b in never: disp = "NEVER-SET"
        elif b in NAMED: disp = "NAMED"
        elif b == 12: disp = "SCRIPT-SET-UNCLEARED"
        else: disp = "PRODUCED-MEANING-NOT-CLAIMED"
        w.write("%d\t%s\t%s\t%s\t%d\t%d\t%s\n" % (b, disp, rowsb, eng.strip("/"), en[b], dis[b], NAMED.get(b, "")))
print("FAILS", fails)
raise SystemExit(1 if fails else 0)
