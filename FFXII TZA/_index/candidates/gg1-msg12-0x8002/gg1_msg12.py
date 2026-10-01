"""gg1_msg12.py - GG-1: 0023FBE0's read of 02F9736A runs only inside message-10 handling (FABLE, Claude Opus 5.5,
2026-09-28). Static. Uses ../gg1-dispatch-sim/ (dispatch_sim.py, and gg1_sim.py's caller walk).

  E1  0023FBE0 reads the word once (0023FFF6), in its message-12 arm under the sub-code (qword [msg+8]) 0x8002:
      sub rax, 0x8001 / je / cmp rax, 1 / jne at 0023FF96-0023FFA6
  E2  every call to the generic notifier 00247510 (window, code = rdx, data = r8) with code 0x8002 is one of seven:
      four ORIGINATE it inside message-10 handling (00557B90 x2 and 0055C740, helpers reached only from message-10 arms;
      0057C480's message-10 arm), and three FORWARD it from a message-12 arm that only fires on an incoming 0x8002
      (002C59D0, 0056F810, 005742D0)
  E3  no other sender of message 12 can carry 0x8002:
      - the other 00247510 calls pass a literal, a lea of a zeroed register plus a small constant, lea [rax+0xC] with
        eax == 3 (0057A507), zero, 003EF050's pass-through of the code it received, 0057C480's code table (written only
        by 0057C140 from 0057C320's five literals 0x8100/0x8101/0x8104/0x8105/0x8106, and reset to 0), or a stack address
        (00293170, and 00292390's create-time replay of 00293170's context: message 1 is {1, ctx+8, ctx+0x10}, 002465F0)
      - the stack-built {12} records: 00241A70 and 005519E0 copy 00915270 (code 0x8101), 00241B40 passes 0x8100 or
        0x8101, 002BF8C0 zero
  E4  00247510 delivers synchronously: it calls the window's proc through [window + 0]
  => every 0x8002 notification starts inside a message-10 handler and reaches 0023FBE0 during it, so the read has the
     message-10 readers' frame placement (../gg1-static-order/)
  C1  control: the simulator's decode of 0023FBE0 puts message 1 at 0023FC23 and message 12 at 0023FEE2
  C2  control: the census resolves the known literal 0x8002 at 002C59D0's site 002C5DBE
"""
import os, re, sys, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "../gg1-dispatch-sim")
src = open(os.path.join(D, "gg1_sim.py"), encoding="utf-8").read()
pre = src.split("for f in readers: print(f, res[f][0], res[f][1])")[0].replace(
    "HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)", "HERE = %r; sys.path.insert(0, HERE)" % D)
g = {"__name__": "gg1_sim_import"}
_so = sys.stdout; sys.stdout = open(os.devnull, "w")
exec(compile(pre, "gg1_sim", "exec"), g)
hs = src.split("callers = collections.defaultdict(set)")[1].split("for f in readers:\n    if res[f][0] == \"no-head\":\n        hits, loose")[0]
exec("callers = collections.defaultdict(set)" + hs, g)
sys.stdout.close(); sys.stdout = _so
ds = g["ds"]; body = ds.body
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
B = {f: dict(ins) for f, ins in body.items()}
reads = sorted(int(l.split(None, 2)[0], 16) for l in open(ds.CACHE, encoding="utf-8", errors="replace") if " 0023FBE0 " in l[:18] and "=>02F9736A" in l)
arms = ds.arms("0023FBE0", range(0, 0x40))
ok("E1", reads == [0x0023FFF6] and arms[12] == 0x0023FEE2 and B["0023FBE0"].get(0x0023FF96) == "sub rax, 0x8001"
   and B["0023FBE0"].get(0x0023FFA2) == "cmp rax, 1" and B["0023FBE0"].get(0x0023FFA6) == "jne 0x24028b",
   "read %s in the message-12 arm (0023FEE2) under sub-code 0x8002" % ["%08X" % a for a in reads])
def code_of(f, i):
    ins = body[f]
    for k in range(i - 1, max(-1, i - 15), -1):
        t = ins[k][1]
        if re.match(r"(call|j[a-z]+|ret)\b", t): return None
        m = re.match(r"(mov|lea|xor|movzx) (edx|rdx|dx), (.+)$", t)
        if m: return (m.group(1), m.group(3), ins[k][0])
    return None
calls = [(f, i, a) for f, ins in body.items() for i, (a, s) in enumerate(ins) if s == "call 0x247510"]
lit = collections.defaultdict(list); other = []
for f, i, a in calls:
    c = code_of(f, i)
    if c and c[0] == "mov" and re.fullmatch(r"0x[0-9a-f]+|\d+", c[1]): lit[int(c[1], 0)].append((f, a))
    else: other.append((f, a, c))
s8002 = sorted(lit[0x8002])
ORIG = {("00557B90", 0x00557CF0), ("00557B90", 0x00557D85), ("0055C740", 0x0055C968), ("0057C480", 0x0057CA60)}
FWD = {("002C59D0", 0x002C5DCA), ("0056F810", 0x0056F953), ("005742D0", 0x005746E7)}
ctx = {}
for f, a in s8002:
    if ds.head(f)[0] is not None: ctx[(f, a)] = ("proc", g["arm_ids"](f, a))
    else:
        hits, loose = g["helper"](f); ctx[(f, a)] = ("helper", tuple(sorted({ids for c, ids in hits})), tuple(loose))
orig_ok = all((ctx[k] == ("proc", (10,))) or (ctx[k][0] == "helper" and ctx[k][1] == ((10,),) and not ctx[k][2]) for k in ORIG)
fwd_guard = (B["002C59D0"].get(0x002C5DA2) == "sub rax, 0x8000" and B["002C59D0"].get(0x002C5DAA) == "cmp rax, 2"
             and B["0056F810"].get(0x0056F939) == "cmp rax, 1" and B["0056F810"].get(0x0056F933) == "sub rax, 1"
             and B["005742D0"].get(0x005746CE) == "cmp qword ptr [rdx + 8], 0x8002")
ok("E2", set(s8002) == ORIG | FWD and orig_ok and all(ctx[k] == ("proc", (12,)) for k in FWD) and fwd_guard,
   "seven 0x8002 sends: originators %s; forwarders (message-12 arm, guarded by an incoming 0x8002) %s"
   % (sorted("%s@%08X %s" % (f, a, ctx[(f, a)][1]) for f, a in ORIG), sorted("%s@%08X" % k for k in FWD)))
def small_ok(f, a, c):
    if c is None:
        return (f, a) in {("00284450", 0x002844A4), ("00284450", 0x002844BA), ("0057C480", 0x0057CBF1)}
    mn, src, at = c
    if mn == "xor": return True
    if mn == "lea" and re.fullmatch(r"\[r8 \+ (0x[0-9a-f]+|\d+)\]", src): return True       # r8 zeroed just before
    if (f, a) == ("0057A4E0", 0x0057A527): return B[f].get(0x0057A507) == "cmp eax, 3" and B[f].get(0x0057A50A) == "jne 0x57a611"
    if (f, a) == ("003EF050", 0x003EF1E9): return src == "qword ptr [rdx + 8]"                  # pass-through
    if (f, a) == ("0057C480", 0x0057CBF1): return src == "word ptr [rsi + r9*8 + 0x5b8]"      # the code table (E3)
    if (f, a) == ("00292390", 0x00292AD9): return src == "qword ptr [rbx]" and B[f].get(0x00292A58) == "mov rbx, qword ptr [rdx + 8]"
    if (f, a) == ("00293170", 0x0029329F): return src == "[rsp + 0x60]"                        # a stack address
    return False
bad = [(f, "%08X" % a, c) for f, a, c in other if not small_ok(f, a, c)]
lit_other = sorted(k for k in lit if k != 0x8002)
tab = sorted(int(code_of(f, i)[1], 0) for f, i, a in [(f, i, a) for f, ins in body.items() for i, (a, s) in enumerate(ins) if re.match(r"(call|jmp) 0x57c320$", s)])
q = struct.unpack("<Q", ds.rd(0x00915270, 8))[0]
b41 = B["00241B40"]
ok("E3", not bad and 0x8002 not in lit_other and tab == [0x8100, 0x8101, 0x8104, 0x8105, 0x8106] and q == 0x8101
   and b41.get(0x00241B5A) == "mov r9d, 0x8100" and b41.get(0x00241B96) == "mov eax, 0x8101" and B["002BF8C0"].get(0x002BFA29) == "xorps xmm0, xmm0"
   and B["002465F0"].get(0x00246726) == "mov rax, qword ptr [rsi + 8]" and B["0057C480"].get(0x0057C4CD) == "xor r14d, r14d",
   "%d other 00247510 calls resolved away from 0x8002 (literals %s); 0057C320 feeds %s; 00915270 = %#x" % (len(other), [hex(x) for x in lit_other], [hex(x) for x in tab], q))
st12 = set()
for f, ins in body.items():
    for i, (a, s) in enumerate(ins):
        m = re.match(r"mov dword ptr \[rsp \+ (0x[0-9a-f]+)\], 0xc$", s)
        if m and any(re.match(r"lea rdx, \[rsp \+ %s\]$" % m.group(1), s2) for a2, s2 in ins[i + 1:i + 14]): st12.add(f)
ok("E3b", st12 == {"00241A70", "00241B40", "00247510", "002BF8C0", "005519E0"}, "the stack-built {12} builders are exactly %s" % sorted(st12))
b75 = [s for a, s in body["00247510"]]
ok("E4", "mov rax, qword ptr [rcx]" in b75 and "call rax" in b75, "00247510 calls [window + 0] synchronously")
ok("C1", arms[1] == 0x0023FC23 and arms[12] == 0x0023FEE2, "control: 0023FBE0 decodes message 1 -> 0023FC23, 12 -> 0023FEE2")
ok("C2", ("002C59D0", 0x002C5DCA) in s8002 and B["002C59D0"].get(0x002C5DBE) == "mov edx, 0x8002", "control: the literal at 002C5DBE is found")
print("FAILS", fails); sys.exit(1 if fails else 0)
