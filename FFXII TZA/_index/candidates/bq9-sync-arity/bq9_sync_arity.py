"""bq9_sync_arity.py - BQ-9: all 90 verbs without a measured arity; the 33 with no begin and no result callback have arity 0 by the
dispatch ABI (FABLE, Claude Opus 5.5, 2026-09-27). Static.

  A1 the census: in scriptvm-verb-table.tsv, exactly 33 rows have an empty pops_int, and every one has neither a begin
     nor a result callback (29 have a poll, 4 have no callback at all).
  A2 the executor 002621D0 hands the value stack (rbx) only to begin (002622D2 mov r9, rbx) and result (0026226B
     mov r9, rbx); the poll call (002622EE..002622F8) loads rcx, rdx and r8 only.
  A3 none of the 29 poll bodies reads r9 before writing it (linear scan of each body to its first ret), so no poll
     reads the stack either - planted positive: the same scan finds r9 read in a begin handler (wait's 0034CF90).
  A4 so nothing pops an operand for these 33 verbs: their arity is 0, and on the normal path the executor pushes the
     int 0 as their value (phase 0 or 1 at completion).
The other 57 rows (same day), through CE-3's path-sensitive walker (ce3_arity_paths.py summary(), re-used by exec):
  A5 13 have one need that equals the catalog count, 9 have one need and no catalog count, 24 have two needs, and
     11 contain a loop that touches the value stack.
  A6/A10 the two needs of the 24 are one mechanism: each reaches 00357DE0 (turn, 12 rows, need 2 or 3), 00357D10
     (look-at, 8 rows) or 00357C40 (the timed look-at the lookatt/lookatyt handlers tail-jump to, 4 rows), both 3 or 4;
     each helper calls 00263D00 (the class-3 threshold predicate, no stack effect) and, when it answers non-zero, skips
     one pop and uses 0 instead. So the arity is n for most actors and n-1 when the predicate holds.
  A13 of those 24, 15 carry a catalog count: 14 equal the larger need, aturny (02D6) the smaller.
  A7 getpartymember 0034B4B0 pops 6 (edi 5..0); checkbattlemember 0034E7D0 pops 3 (ebx 2..0).
  A8/A11 the party-motion four (0034F060, 0034F890, 00350050, 003507B0) pop 1, 1, 2, 2 before one loop whose pass
     pushes 3 for 003580C0, which pops 3; capturebattleid 003509E0 pops 1 before a loop whose pass pushes 1 for
     00352FA0, which pops 1; the other in-loop callees have no stack effect - so each loop is neutral.
     (setbattlemember 3 and getbattlemember 4 were settled by CE-3 A4.)
  A9 sethpratio_1f9 / setmpratio_1fb share 0034A920: it pushes the int 2 and jumps back to itself - pops 0, never returns.
  A12 over the shipped scripts on the local extract (skipped without it): wait, turnsync and hideparty are called
     (controls); 01F9, 01FB, getpartymember, checkbattlemember, 053F and 0541 are called nowhere.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, re, struct, sys
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
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
rows = list(csv.DictReader(open(DB / "01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv", encoding="utf-8"), delimiter="\t"))
empty = [r for r in rows if r["pops_int"] == ""]
check("A1 33 empty-pops rows, none with a begin or a result",
      len(empty) == 33 and not any(r["begin"] or r["result"] for r in empty)
      and sum(1 for r in empty if r["poll"]) == 29, "%d rows, %d with a poll" % (len(empty), sum(1 for r in empty if r["poll"])))
x = dis(0x262255, 0x2622FA)
poll_setup = [t for k, t in sorted(x.items()) if 0x2622EE <= k < 0x2622F8]
check("A2 the value stack goes only to begin and result; the poll call loads rcx, rdx, r8",
      x.get(0x26226B) == "mov r9, rbx" and x.get(0x262278) == "call rax" and x.get(0x2622D2) == "mov r9, rbx"
      and x.get(0x2622DB) == "call rax" and x.get(0x2622F8) == "call rax"
      and poll_setup == ["lea r8, [rdi + 0x18]", "mov rdx, rbp", "mov rcx, r14"], str(poll_setup))
R9 = re.compile(r"\br9[dwb]?\b")
def reads_r9_first(a):
    for ins in cs.disasm(d[off(a):off(a) + 0x800], a):
        ops = ins.op_str.split(", ")
        if ins.mnemonic == "ret": return False
        dst, srcs = (ops[0], ops[1:]) if ops and ops[0] else ("", [])
        if any(R9.search(s) for s in srcs) or (dst and "[" in dst and R9.search(dst)):
            return True
        if R9.search(dst) and ins.mnemonic in ("mov", "lea", "movzx", "movsxd", "xor", "movsx", "pop"):
            return False
        if R9.search(dst): return True
    return False
polls = sorted({int(r["poll"], 16) for r in empty if r["poll"]})
hits = [p for p in polls if reads_r9_first(p)]
check("A3 no poll body reads r9 before writing it; planted positive: a begin handler does",
      hits == [] and reads_r9_first(0x34CF90), "polls %d, readers %s" % (len(polls), ["%08X" % h for h in hits]))
y = dis(0x262316, 0x262390)
check("A4 with no result the executor pushes an int: phase-0/1 completion stores 1 as the type byte and the value",
      any(t == "mov byte ptr [rax + rbx + 4], 1" for t in x.values()) or any(t == "mov byte ptr [rax + rbx + 4], 1" for t in y.values()))
# ---- the other 57 (added the same day): CE-3's path-sensitive walker, re-used, plus hand-read loops -------------
W = ROOT / "Database/FFXII TZA/_index/candidates/ce3-arity-disagreements/ce3_arity_paths.py"
g = {"__file__": str(W)}
exec(compile(open(W, encoding="utf-8").read().split("fails = 0")[0], str(W), "exec"), g)
need = lambda f: sorted({n for n, _ in g["summary"](f)})
# the 57 BQ-9 rows by identity (SWE2-DATA 2026-09-27): the table now carries the answer in
# arity_status, so select by call_id, not by the pre-answer UNPROVEN/LOWER-BOUND marks
BQ9_57 = {"0147","0148","029D","0359","035B","03BF","03E0","040D","040E","040F",
          "0410","0411","0412","0413","0486","0498","0554","0555","0566","0573",
          "057A","209C","01F9","01FB","0352","0355","0357","0360","03E9","053E",
          "053F","0540","0541","0047","004A","004E","004F","0061","0064","0067",
          "024F","0250","0257","0258","025D","0260","0278","027C","02C8","02C9",
          "02CE","02CF","02D4","02D6","02D8","02DB","02DE"}
open57 = [r for r in rows if r["call_id"] in BQ9_57]
LOOPS = {"01F9", "01FB", "0352", "0355", "0357", "0360", "03E9", "053E", "053F", "0540", "0541"}
single = [r for r in open57 if r["call_id"] not in LOOPS and len(need(int(r["arg_handler"], 16))) == 1]
two = [r for r in open57 if r["call_id"] not in LOOPS and len(need(int(r["arg_handler"], 16))) == 2]
agree = [r for r in single if r["cat_known"] == "True" and need(int(r["arg_handler"], 16)) == [int(r["cat_args"])]]
nocat = [r for r in single if r["cat_known"] != "True"]
check("A5 the 57: 13 single-need rows agree with the catalog, 9 single-need rows have no catalog, 24 two-valued, 11 loops",
      len(open57) == 57 and len(agree) == 13 and len(nocat) == 9 and len(two) == 24 and len(single) + len(two) == 46,
      "57=%d agree %d nocat %d two %d" % (len(open57), len(agree), len(nocat), len(two)))
t1 = dis(0x357D10, 0x357D90)
check("A6 the two-valued need is one mechanism: 00357D10 (look-at) mirrors 00357DE0 (turn) - 00263D00(actor) skips one pop",
      t1.get(0x357D37) == "call 0x267db0" and t1.get(0x357D50) == "call 0x267db0" and t1.get(0x357D5E) == "call 0x263d00"
      and t1.get(0x357D65) == "jne 0x357d77" and t1.get(0x357D6A) == "call 0x267db0" and t1.get(0x357D82) == "call 0x267db0"
      and all(n[1] - n[0] == 1 for n in (need(int(r["arg_handler"], 16)) for r in two)))
l1 = dis(0x34B4D9, 0x34B501); l2 = dis(0x34E7E8, 0x34E823); l3 = dis(0x34A930, 0x34A942)
check("A7 hand-read loops: getpartymember pops 6 (edi 5..0), checkbattlemember 3 (ebx 2..0 step 1)",
      l1.get(0x34B4D9) == "mov edi, 5" and l1.get(0x34B4E3) == "call 0x267e10" and l1.get(0x34B4FB) == "sub rdi, 1"
      and l1.get(0x34B4FF) == "jns 0x34b4e0" and l2.get(0x34E7E8) == "mov esi, 4" and l2.get(0x34E7F5) == "lea ebx, [rsi - 2]"
      and l2.get(0x34E7F8) == "lea edi, [rsi - 3]" and l2.get(0x34E803) == "call 0x267e10" and l2.get(0x34E81F) == "sub ebx, edi"
      and l2.get(0x34E821) == "jns 0x34e800")
check("A8 the stack-neutral loops: 003580C0 pops 3 and 00352FA0 pops 1, matching what each pass pushes",
      sorted(g["summary"](0x3580C0)) == [(3, -3)] and sorted(g["summary"](0x352FA0)) == [(1, -1)])
check("A9 0034A920 (sethpratio_1f9 / setmpratio_1fb) pushes the int 2 forever and pops nothing: arity 0, never returns",
      l3.get(0x34A930) == "mov edx, 2" and l3.get(0x34A938) == "call 0x267f90" and l3.get(0x34A93D) == "jmp 0x34a930")
def reaches(f, tgt, depth=0, seen=None):
    seen = set() if seen is None else seen
    if f in seen or depth > 4 or off(f) is None: return False
    seen.add(f)
    for x in cs.disasm(d[off(f):off(f) + 0x400], f):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if t in tgt: return True
            if t not in (0x267DB0, 0x267E10, 0x267F60, 0x267F90, 0x808C40) and x.mnemonic == "call" and reaches(t, tgt, depth + 1, seen): return True
            if x.mnemonic == "jmp" and not f <= t < f + 0x400 and reaches(t, tgt, depth + 1, seen): return True
        if x.mnemonic == "ret" or x.mnemonic == "int3": break
    return False
via = {0x357DE0: 0, 0x357D10: 0, 0x357C40: 0}
for r in two:
    for k in via:
        if reaches(int(r["arg_handler"], 16), {k}): via[k] += 1; break
t2 = dis(0x357C40, 0x357CB2)
check("A10 each of the 24 reaches one of three helpers with the same 00263D00 skip: 12 through 00357DE0 (turn, need 2 or 3), 8 through 00357D10 (look-at) and 4 through 00357C40 (timed look-at, the lookatt/lookatyt handlers' tail jump), both need 3 or 4; 00263D00 touches no stack",
      via == {0x357DE0: 12, 0x357D10: 8, 0x357C40: 4} and sorted(g["summary"](0x263D00)) == [(0, 0)]
      and t2.get(0x357C8E) == "call 0x263d00" and t2.get(0x357C95) == "jne 0x357ca1" and t2.get(0x357C9A) == "call 0x267db0"
      and sorted(g["summary"](0x357DE0)) == [(2, -2), (3, -3)] and sorted(g["summary"](0x357D10)) == [(3, -3), (4, -4)]
      and sorted(g["summary"](0x357C40)) == [(3, -3), (4, -4)], str({"%08X" % k: v for k, v in via.items()}))
catd = [(r["call_id"], int(r["cat_args"]), need(int(r["arg_handler"], 16))) for r in two if r["cat_known"] == "True"]
check("A13 of the 24, 15 have a catalog count: 14 equal the larger need, one (aturny 02D6) the smaller",
      len(catd) == 15 and sum(c == n[1] for _, c, n in catd) == 14 and [k for k, c, n in catd if c == n[0]] == ["02D6"], str(catd))
POPSET = {0x267DB0, 0x267E10}; PUSHSET = {0x267F60, 0x267F90}
def loop_shape(a):
    ins = []
    for x in cs.disasm(d[off(a):off(a) + 0x300], a):
        ins.append(x)
        if x.mnemonic == "ret": break
    backs = [(int(x.op_str, 16), x.address) for x in ins if x.mnemonic.startswith("j") and x.op_str.startswith("0x") and a <= int(x.op_str, 16) <= x.address]
    lo, hi = backs[0]
    calls = [(x.address, int(x.op_str, 16)) for x in ins if x.mnemonic == "call" and x.op_str.startswith("0x")]
    inl = [t for k, t in calls if lo <= k <= hi]
    return (len(backs), sum(t in POPSET for k, t in calls if k < lo), sum(t in PUSHSET for t in inl),
            sorted({t for t in inl if t not in PUSHSET}), sum(t in POPSET | PUSHSET for k, t in calls if k > hi))
MOT = [0x263750, 0x3580C0, 0x35AE10]
shapes = {a: loop_shape(a) for a in (0x34F060, 0x34F890, 0x350050, 0x3507B0, 0x3509E0)}
check("A11 party-motion x4 pop 1,1,2,2 before one loop whose pass pushes 3 for 003580C0; capturebattleid pops 1, pass pushes 1 for 00352FA0; other in-loop callees touch no stack",
      shapes == {0x34F060: (1, 1, 3, MOT, 0), 0x34F890: (1, 1, 3, MOT, 0), 0x350050: (1, 2, 3, MOT, 0), 0x3507B0: (1, 2, 3, MOT, 0),
                 0x3509E0: (1, 1, 1, [0x233D70, 0x2373A0, 0x263750, 0x352FA0], 0)}
      and all(sorted(g["summary"](f)) == [(0, 0)] for f in (0x263750, 0x35AE10, 0x2373A0, 0x233D70)), str(shapes))
# corpus census: which of the residual verbs ship in any script (needs the local extract; skipped, not failed, without it)
EX = Path("D:/FFXII_TZA_extract")
if EX.exists():
    import hashlib, collections
    U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
    WANT = {0x0000, 0x0046, 0x0147, 0x01F9, 0x01FB, 0x0352, 0x0360, 0x053F, 0x0541}
    sites = collections.Counter(); seen = set(); total = 0
    for p in sorted(EX.rglob("*.ebp")):
        b = p.read_bytes(); h = hashlib.md5(b).digest()
        if h in seen or len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
        seen.add(h)
        sec = b[0x80:0x80 + U32(b, 0x84)]; diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
        if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
        st = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt)); bounds = sorted(set(st) | {diroff, len(sec)})
        for s0 in st:
            code = sec[s0:min((x for x in bounds if x > s0), default=len(sec))]; i = 0
            while i < len(code):
                op = code[i]
                if op > 0x63: break
                if op >= 0x48:
                    if op in (0x58, 0x59, 0x5D, 0x5E) and i + 2 < len(code):
                        v = code[i + 1] | (code[i + 2] << 8); total += 1
                        if v in WANT: sites[v] += 1
                    i += 3
                else: i += 1
    check("A12 shipped scripts: wait/turnsync/hideparty called (controls); sethpratio_1f9, setmpratio_1fb, getpartymember, checkbattlemember, 053F, 0541 never",
          sites[0x0000] > 1000000 and sites[0x0046] > 100000 and sites[0x0147] > 10000
          and all(sites[v] == 0 for v in (0x01F9, 0x01FB, 0x0352, 0x0360, 0x053F, 0x0541)),
          "distinct ebp %d calls %d %s" % (len(seen), total, {"%04X" % k: sites[k] for k in sorted(WANT)}))
else:
    print("SKIP  A12 D:/FFXII_TZA_extract not present")
print("FAILS", fails)
sys.exit(1 if fails else 0)
