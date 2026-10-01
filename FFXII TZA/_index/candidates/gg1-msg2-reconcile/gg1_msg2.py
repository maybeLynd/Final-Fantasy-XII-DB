"""gg1_msg2.py - GG-1: the two message-2 readers are placed through the reconcile walks over their layer
(FABLE, Claude Opus 5.5, 2026-09-28). Static; companion to ../gg1-chain-procs/ (whose decoder this imports),
../gg1-static-order/ and ../gg1-msg31-arbiter/.

  S1  0027AA70 and 005519E0 read 02F9736A only in their message-2 arm (the chain decoder of ../gg1-chain-procs/)
  S2  both readers' windows sit under the layer root [0208EA28]:
      - 0027AA70 is installed once (0027A369, in 00279E20) and its window is linked under 00279E20's own window
        (00244960 with rcx = rbx = this). 00279E20 is installed once (002766D1, in 00276650), whose window is attached by
        00246AC0 at 0027671D
      - 005519E0 has no reference and no caller but the two wrapper procs 00551E00 / 00551F00, which forward every
        message to it. Their windows are linked under 005528C0's own window (005530EE, 005534D4; rdi = this). 005528C0 is
        installed once (00552301, in 00552250), whose window is stored at +0x160 and attached to [0208EA28] at 005524E1
  S3  00246AC0 is 00246AD0([0208EA28], w), and 00246AD0 links a window that has no parent (00248220)
  S4  the reconcile walk 00248030 sends {2} (the .rdata record 00915108) to each window under the root it is given.
      Walks over [0208EA28]: 002507C0 (0025082E), 00250730 (00250775), and the UI pass 00250540's main loop, which walks
      three roots from 0208EA20 (esi = 3). Walks that do not reach it: 002506D0 ([0208EA48]), 002508E0 (EA38, EA40,
      EA48), 00250540's early path ([0208EA48]), and the arbiter-time creation walk in 002284F0 ([0208EA40])
  S5  every pump function starts its own walk generation (002481A0 before its walks, 00248190 after), so each call
      reaches every window under its roots once
  S6  no other {2} reaches a window proc. 002A6190's .rdata {2} goes to 00247570, which only stores it at +0x48. The
      stack-built {2} records go to 003C2190 (a jump to 003C1F00 on [02B457E0]) and through object vtables (+0xC0,
      +0xB0); a window proc is called through [window + 0]
  C1  control for S2: the same tracer finds 003CAB00's window linked under 003CA860's (003CA93A), as ../gg1-msg31-arbiter/
      established
  C2  control for S4: the frame positions ../gg1-static-order/ uses - 002507C0 at 0022AB83 and 0022AC17, 00250540 at
      0022BA45 and 0022BD08
Limit: a window with bit 18 of +0x40 set is walked without the send, and one with bit 10 set takes 002482E0 (not read).
"""
import os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../gg1-chain-procs/gg1_chain_procs.py")
_t = open(SRC, encoding="utf-8").read().split("FIRST16 = ")[0]
_saved = sys.argv; sys.argv = [SRC]
exec(compile(_t.replace("HERE = os.path.dirname(os.path.abspath(__file__))", "HERE = %r" % os.path.dirname(SRC)), SRC, "exec"))
sys.argv = _saved
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
B = {f: {a: s for a, s in ins} for f, ins in body.items()}
def leas_of(t): return sorted((f, "%08X" % a) for f, ins in body.items() for a, s in ins if "=>%s" % t in s)
def calls_to(t): return sorted((f, "%08X" % a) for f, ins in body.items() for a, s in ins if re.match(r"(call|jmp) 0x%x$" % int(t, 16), s))
ok("S1", place.get("0027AA70", (0, 0))[1] == [(2,)] and place.get("005519E0", (0, 0))[1] == [(2,)],
   "0027AA70 %s, 005519E0 %s" % (place.get("0027AA70"), place.get("005519E0")))
first = lambda f: [s for a, s in body[f][:30]]
s2a = (leas_of("0027AA70") == [("00279E20", "0027A369")] and "mov rbx, rcx" in first("00279E20")
       and B["00279E20"].get(0x0027A369, "").startswith("lea r8") and "call 0x245000" in [B["00279E20"].get(a) for a in range(0x0027A369, 0x0027A3A0)]
       and leas_of("00279E20") == [("00276650", "002766D1")] and B["00276650"].get(0x002766DD) == "mov rcx, rsi"
       and B["00276650"].get(0x002766E0) == "call 0x245000" and B["00276650"].get(0x0027671A) == "mov rcx, rsi" and B["00276650"].get(0x0027671D) == "call 0x246ac0")
link_a = [(a, s) for a, s in body["00279E20"] if 0x0027A369 <= a <= 0x0027A3C0 and s in ("call 0x244960", "mov rcx, rbx")]
s2b = (leas_of("005519E0") == [] and calls_to("005519E0") == [("00551E00", "00551ED8"), ("00551F00", "0055201B")]
       and "mov rdi, rcx" in first("005528C0") and B["005528C0"].get(0x005530EE) == "mov rcx, rdi" and B["005528C0"].get(0x005530F4) == "call 0x244960"
       and B["005528C0"].get(0x005534D4) == "mov rcx, rdi" and B["005528C0"].get(0x005534DA) == "call 0x244960"
       and leas_of("005528C0") == [("00552250", "00552301")] and B["00552250"].get(0x0055231B) == "mov qword ptr [rbx + 0x160], rax"
       and B["00552250"].get(0x005524D3) == "mov rdx, qword ptr [rbx + 0x160]" and "=>0208EA28" in B["00552250"].get(0x005524DA, "")
       and B["00552250"].get(0x005524E1) == "call 0x246ad0")
ok("S2", s2a and link_a and s2b, "0027AA70: window under 00279E20's, which 00276650 attaches with 00246AC0 (0027671D); 005519E0: base of 00551E00/00551F00, windows under 005528C0's, attached to [0208EA28] at 005524E1")
a0 = [s for a, s in body["00246AC0"]]; a1 = B["00246AD0"]
ok("S3", a0 == ["mov rdx, rcx", "mov rcx, qword ptr [rip + 0x1e47f5e] ; =>0208EA28", "jmp 0x246ad0"] and a1.get(0x00246AE5) == "cmp qword ptr [rdx + 0x10], 0" and a1.get(0x00246AF5) == "call 0x248220",
   "00246AC0 = 00246AD0([0208EA28], w); a parentless window is linked (00246AF5)")
def root_of(f, i):
    for k in range(i - 1, max(-1, i - 5), -1):
        s = body[f][k][1]
        if s.startswith("mov rcx,"): m = re.search(r"=>([0-9A-F]{8})", s); return m.group(1) if m else s
    return "?"
def walks(f): return [(a, root_of(f, i)) for i, (a, s) in enumerate(body[f]) if s == "call 0x248030"]
W = {f: walks(f) for f in ("002507C0", "00250730", "002506D0", "002508E0", "00250540", "002284F0")}
loop = B["00250540"].get(0x002505FE) == "mov esi, 3" and "=>0208EA20" in B["00250540"].get(0x0025061C, "") and B["00250540"].get(0x00250630) == "mov rcx, qword ptr [rdi]"
reach = {f: any(t == "0208EA28" for a, t in w) for f, w in W.items()}
ok("S4", reach == {"002507C0": True, "00250730": True, "002506D0": False, "002508E0": False, "00250540": False, "002284F0": False} and loop
   and any("=>00915108" in s for a, s in body["00248030"]),
   "direct walks of [0208EA28]: %s; 00250540's loop walks 3 roots from 0208EA20 (esi = 3); other walks: %s" % ({f: r for f, r in reach.items() if r}, {f: [t for a, t in w] for f, w in W.items() if not reach[f]}))
gen = {}
for f in ("002507C0", "00250730", "002506D0", "002508E0"):
    seq = [s for a, s in body[f] if s in ("call 0x2481a0", "call 0x248030", "call 0x248190")]
    gen[f] = seq[0] == "call 0x2481a0" and seq[-1] == "call 0x248190"
seq540 = [s for a, s in body["00250540"] if s in ("call 0x2481a0", "call 0x248030", "call 0x248190")]
ok("S5", all(gen.values()) and seq540.count("call 0x2481a0") == 2 and B["002481A0"].get(0x002481A0, "").startswith("xor dword ptr [rip") ,
   "each pump function opens (002481A0) and closes (00248190) its own generation: %s; 00250540 opens two, one per path" % gen)
s6 = (B["002A6190"].get(0x002A61F6) == "call 0x247570" and [s for a, s in body["00247570"]][5] == "mov qword ptr [rcx + 0x48], rax"
      and B["003CB4F0"].get(0x003CB5E7) == "call 0x3c2190" and "=>02B457E0" in [s for a, s in body["003C2190"]][3]
      and B["00615790"].get(0x006157E3) == "call qword ptr [rax + 0xc0]" and B["0061DE20"].get(0x0061DEE9) == "call qword ptr [rax + 0xb0]")
ok("S6", s6, "the other {2} builders: 002A6190 -> 00247570 (stores +0x48); 003CB4F0 -> 003C2190 ([02B457E0]); 00615790 / 0061DE20 -> object vtables")
ok("C1", B["003CA860"].get(0x003CA930) == "lea rdx, [rdi + 0x2a0]" and B["003CA860"].get(0x003CA93A) == "call 0x244960", "control: 003CAB00's window linked under 003CA860's at 003CA93A")
fc = calls_to("002507C0") + calls_to("00250540")
ok("C2", {("0022A770", "0022AB83"), ("0022A770", "0022AC17"), ("0022B8C0", "0022BA45"), ("0022BC20", "0022BD08")} <= set(fc), "control: frame call sites %s" % fc)
print("FAILS", fails); sys.exit(1 if fails else 0)
