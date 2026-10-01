"""cz2_start_waiter_pairing.py - CZ-2: the 77 start-and-return verbs do not pair one-to-one with the 29 poll-only
waiters (FABLE, Claude Opus 5.5, 2026-09-26; found by a delegated read-only pass, re-derived here from the verb table
and the bytes).

  Z1 the census: in scriptvm-verb-table.tsv, 77 verbs have a begin and no poll, and 29 have a poll and neither a begin
     nor a result.
  Z2 many-to-one through shared begins: of the 77, 8 share their begin with a blocking twin whose poll is turnsync's
     00341D50, 10 with a twin polling movesync's 00356A90, and 19 with a twin polling lookatsync's 003435C0.
  Z3 the waiters read what the starts write:
     - turnsync reads the steering byte +0x28 (0026561B), which 0026C120 writes (0026C153);
     - movesync reads +0x29 (00264E2B), which Movement_SetSteeringMode 0026AE90 writes.
     Every turn start reaches 0026C120 and every move start reaches 0026AE90, through direct call/jmp edges at depth 5
     or less.
  Z4 the music fade pairs by a slot field: the fade starters store 0x10001 at [slot+0x1C] (003611AC, 00361296), and
     the waiter's scan walks word [slot+0x1E]
     (a pointer from 022BDEC0 + 0x1E, stride 0x48, 002F1A41..002F1A58) and compares it with 1 (002F1A4E).
  Z5 two poll-only waiters can never report busy: the atrac3 polls are 005C5230 (xor eax, eax; ret).
  Z6 the shipped scripts: every distinct .ebp in the extract, all languages. 28 of the 77 starts are called by no
     shipped script, rturn among them. Every call of the waiter vibsync is preceded, among the script's calls, by
     vibplay, which is an instantaneous verb, not one of the 77. So the waiters are not paired only with the 77:
     instantaneous verbs start work too.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, csv, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return "%s %s" % (x.mnemonic, x.op_str)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
rows = list(csv.DictReader(open(DB / "01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv", encoding="utf-8"), delimiter="\t"))
starts = [r for r in rows if r["begin"] and not r["poll"]]
waits = [r for r in rows if r["poll"] and not r["begin"] and not r["result"]]
check("Z1 77 begin-without-poll verbs and 29 poll-only verbs (no begin, no result)", len(starts) == 77 and len(waits) == 29, "%d / %d" % (len(starts), len(waits)))
by_begin = collections.defaultdict(set)
for r in rows:
    if r["begin"] and r["poll"]: by_begin[r["begin"]].add(r["poll"])
twin = collections.Counter()
for r in starts:
    for p in by_begin.get(r["begin"], ()): twin[p] += 1
check("Z2 shared-begin twins: 8 poll turnsync 00341D50, 10 movesync 00356A90, 19 lookatsync 003435C0",
      twin["00341D50"] == 8 and twin["00356A90"] == 10 and twin["003435C0"] == 19, str(dict(twin)))
def calls(a, size=0x400):
    out = set()
    for x in cs.disasm(d[off(a):off(a) + size], a):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"): out.add(int(x.op_str, 16))
        if x.mnemonic in ("ret", "int3"): break
    return out
def reaches(a, t, depth=5):
    front, seen = {a}, {a}
    for _ in range(depth):
        nxt = set()
        for f in front:
            for c in calls(f):
                if c == t: return True
                if c not in seen: seen.add(c); nxt.add(c)
        front = nxt
    return False
TURN = ["dir", "rturn", "rturn_48", "rturna", "rturnt", "rturnt_4b", "rturnat", "dira", "dir_4e", "rturn_4f", "rturn_50",
        "rturna_244", "raturn", "raturn_25e", "raturna", "raturny", "raturnya", "rturnzx"]
MOVE = ["rcmove", "rcmove_3f", "rcmovea", "rcmovea_41", "rmove", "rmove_43", "rmovea", "rmovea_45", "ramove", "ramove_4cf",
        "ramovea", "ramovea_4d1"]
S = {r["verb"]: r for r in starts}
tr = [v for v in TURN if v in S and reaches(int(S[v]["begin"], 16), 0x26C120)]
mv = [v for v in MOVE if v in S and reaches(int(S[v]["begin"], 16), 0x26AE90)]
check("Z3 turnsync reads steering +0x28 (0026C120 writes it), movesync +0x29; all 18 turn and 12 move starts reach the writers",
      at(0x26561B).endswith("+ 0x28]") and at(0x26C153) == "mov byte ptr [rax + 0x28], dl" and at(0x264E2B).endswith("+ 0x29]")
      and len(tr) == 18 and len(mv) == 12, "turn %d/18 move %d/12 | %s | %s" % (len(tr), len(mv), at(0x26561B), at(0x264E2B)))
check("Z4 the music fade pairs through the slot's +0x1C/+0x1E word",
      at(0x3611AC).endswith("+ 0x1c], 0x10001") and at(0x361296).endswith("+ 0x1c], 0x10001")
      and at(0x2F1A41).startswith("lea rdx, [rip") and 0x2F1A48 + int(at(0x2F1A41).split("+ ")[1].rstrip("]"), 16) == 0x22BDEC0 + 0x1E
      and at(0x2F1A4E) == "movsx ecx, word ptr [rdx]" and at(0x2F1A58) == "add rdx, 0x48",
      "%s | %s" % (at(0x3611AC), at(0x2F1A4E)))
atr = [r for r in waits if r["verb"] in ("atrac3standbysync", "atrac3playsync")]
check("Z5 the two atrac3 waiters' polls are the constant stub 005C5230",
      len(atr) == 2 and all(r["poll"] == "005C5230" for r in atr) and d[off(0x5C5230):off(0x5C5230) + 3] == b"\x33\xc0\xc3")
# Z6 the shipped scripts: every distinct .ebp in the extract, decoded as bf5_inert_opcode_census.py does (1 byte below
# 0x48, 3 at or above; zero anomalies there). CALL-family opcodes 0x58/0x59/0x5D/0x5E carry the verb id as their u16.
import hashlib
EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
vid = {int(r["call_id"], 16): r["verb"] for r in rows}
start_ids = {int(r["call_id"], 16) for r in starts}; wait_ids = {int(r["call_id"], 16) for r in waits}
sites = collections.Counter(); prev_of = collections.defaultdict(collections.Counter); seen = set()
for p in sorted(EX.rglob("*.ebp")):
    b = p.read_bytes(); h = hashlib.md5(b).digest()
    if h in seen or len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
    seen.add(h)
    sec = b[0x80:0x80 + U32(b, 0x84)]; diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
    st = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt)); bounds = sorted(set(st) | {diroff, len(sec)})
    for s0 in st:
        e0 = min((x for x in bounds if x > s0), default=len(sec)); code = sec[s0:e0]; i = 0; last = None
        while i < len(code):
            op = code[i]
            if op > 0x63: break
            if op >= 0x48:
                if op in (0x58, 0x59, 0x5D, 0x5E) and i + 2 < len(code):
                    v = code[i + 1] | (code[i + 2] << 8); sites[v] += 1
                    if v in wait_ids: prev_of[v][last] += 1
                    last = v
                i += 3
            else: i += 1
zero = sorted(vid[v] for v in start_ids if sites[v] == 0)
vs_ = [k for k, v in vid.items() if v == "vibsync"][0]; vp = [k for k, v in vid.items() if v == "vibplay"][0]
nv = sum(prev_of[vs_].values())
check("Z6 in the shipped scripts (every language), 28 of the 77 starts are never called; every vibsync follows vibplay, an instantaneous verb",
      len(zero) == 28 and "rturn" in zero and nv > 0 and prev_of[vs_][vp] == nv and vp not in start_ids,
      "distinct .ebp %d; never called %d; vibsync %d, preceded by vibplay %d; never called: %s" % (len(seen), len(zero), nv, prev_of[vs_][vp], zero))
print("FAILS", fails)
sys.exit(1 if fails else 0)
