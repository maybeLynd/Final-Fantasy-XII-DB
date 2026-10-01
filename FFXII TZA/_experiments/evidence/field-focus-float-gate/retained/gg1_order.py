"""gg1_order.py - where the battle command menu's read of 02F9736A sits relative to the input arbiter, statically
(FABLE, Claude Opus 5.5, 2026-09-28). Direct call-site order and gates only; no execution.

  O1  the reader 00277ACD lies in 002778C0's arm for widget messages 10 and 11 (focus input), decoded from the proc's
      own jump table; message 2 (the per-frame reconcile) goes to a different arm
  O2  every direct sender of messages 10/11 is 002481C0, and its callers are 00250540 (the UI pass), 002506D0 (the
      pause step), 002507C0 (only when its argument is 1: cmp ebx,1 before the send), 00250730 and 002508E0
  O3  in the frame bodies 0022B8C0 and 0022BC20 the order is: snapshot rebuild 002498B0 < world tick 00314020 (which
      reaches the arbiter) < UI pass 00250540 - so their message-10/11 delivery follows the arbiter
  O4  in the field frame 0022A770 the order is: rebuild 002498B0 < [pause step 002506D0 when 0017E4E0 is set, then the
      frame ends] < 002507C0(r15d) at 0022AB83 < world tick 00314020 at 0022ABD8 < 002507C0(edi) at 0022AC17, with
      r15d = 1 (0022A832) and edi = r15d (0022AA10) - so a field frame can deliver the focus-input message both before
      and after the arbiter
  O5  the pre-arbiter send at 0022AB83 is gated by 003583A0 (bit 3 of 022C7F92) and by the step accumulator 02064AC0
      being exactly 0.0 (ucomiss against xmm7, zeroed at 0022A9EF); the post-arbiter send by 003583A0 alone
  O6  00314020 reaches 002E0D90 -> 00253C50 -> the arbiter 00253C70 on two paths, one of them only when esi == 0
  C   control: the same jump-table decoder maps message 1 to the arm at 00277925 and the unused ids to one default arm
"""
import os, re, struct, sys, collections
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
body = collections.defaultdict(list); callers = collections.defaultdict(list)
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) < 3: continue
    body[p[1]].append((p[0], p[2]))
    m = re.match(r"(call|jmp) 0x([0-9a-f]+)$", p[2])
    if m: callers["%08X" % int(m.group(2), 16)].append((p[1], p[0]))
def site(f, target):
    return [a for a, s in sorted(body[f]) if re.match(r"(call|jmp) 0x0*%s$" % target.lstrip("0").lower(), s)]
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []; o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); secs.append((va, vs, ra, rs)); o += 40
def rd(va, n):
    r = va - 0x120000
    for sva, vs, ra, rs in secs:
        if sva <= r < sva + rs: return d[ra + r - sva: ra + r - sva + n]
bidx = rd(0x120000 + 0x159D98, 0x2D)
arm = {mid: 0x120000 + struct.unpack_from("<I", rd(0x120000 + 0x159D60 + bidx[mid - 1] * 4, 4))[0] for mid in range(1, 0x2E)}
starts = sorted(set(arm.values()))
def arm_of(addr): return max(t for t in starts if t <= addr)
a_read = arm_of(0x00277ACD)
ok("O1", arm[10] == arm[11] == a_read and arm[2] != a_read and body["002778C0"] and any("=>02F9736A" in s for a, s in body["002778C0"] if a == "00277ACD"),
   "00277ACD (a read of 02F9736A) is in the arm at %08X, which messages %s reach; message 2 goes to %08X"
   % (a_read, sorted(m for m, t in arm.items() if t == a_read), arm[2]))
snd = sorted({c for c, s in callers["002481C0"]})
gate = [s for a, s in sorted(body["002507C0"])]
i_send = next(i for i, s in enumerate(gate) if s == "call 0x2481c0")
ok("O2", snd == ["00250540", "002506D0", "00250730", "002507C0", "002508E0"] and gate[i_send - 2] == "cmp ebx, 1",
   "002481C0's callers %s; in 002507C0 the send follows 'cmp ebx, 1'" % snd)
ords = {}
for f in ("0022B8C0", "0022BC20"):
    r, w, u = site(f, "002498B0"), site(f, "00314020"), site(f, "00250540")
    ords[f] = (r, w, u)
ok("O3", all(r and w and u and r[0] < w[0] < u[0] for r, w, u in ords.values()),
   "rebuild < world tick < UI pass: %s" % {f: (r[0], w[0], u[0]) for f, (r, w, u) in ords.items()})
F = "0022A770"; fb = dict(body[F])
r, p, s1, w = site(F, "002498B0"), site(F, "002506D0"), site(F, "002507C0"), site(F, "00314020")
ok("O4", r and p and len(s1) == 2 and w and r[0] < p[0] < s1[0] < w[0] < s1[1] and fb.get("0022A832") == "mov r15d, 1"
   and fb.get("0022AB80") == "mov ecx, r15d" and fb.get("0022AC15") == "mov ecx, edi" and fb.get("0022AA10") == "mov edi, r15d",
   "field frame: rebuild %s < pause step %s < 002507C0(r15d=1) %s < world tick %s < 002507C0(edi) %s" % (r[0], p[0], s1[0], w[0], s1[1]))
ok("O5", fb.get("0022AB68") == "call 0x3583a0" and fb.get("0022AC0C") == "call 0x3583a0" and fb.get("0022AB79") == "ucomiss xmm0, xmm7"
   and fb.get("0022A9EF") == "xorps xmm7, xmm7" and "02064AC0" in fb.get("0022AB71", "")
   and [s for a, s in sorted(body["003583A0"])][:3] == ["movzx eax, word ptr [rip + 0x1f6fbeb] ; =>022C7F92", "shr eax, 3", "and eax, 1"],
   "pre-arbiter send gated by 003583A0 (bit 3 of 022C7F92) and 02064AC0 == 0.0; post-arbiter send by 003583A0")
tb = dict(body["00314020"])
ok("O6", site("00314020", "002E0D90") == ["00314137", "003141F2"] and tb.get("003141EE") == "test esi, esi"
   and site("002E0D90", "00253C50") and site("00253C50", "00253C70"),
   "00314020 -> 002E0D90 at %s (the second only when esi == 0) -> 00253C50 -> 00253C70" % site("00314020", "002E0D90"))
dflt = collections.Counter(arm.values()).most_common(1)[0]
ok("C", arm[1] == 0x00277925 and dflt[1] >= 20, "control: message 1 -> %08X; the default arm %08X takes %d ids" % (arm[1], dflt[0], dflt[1]))
print("FAILS", fails); sys.exit(1 if fails else 0)
