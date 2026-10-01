"""uq194_event_entry.py - UQ-194: what keeps the event getter's render-record fields stable, how an event entry is bound
and owned, and every direct effect of the two event-entry callers 00424550 and 00424D80 (FABLE, Claude Opus 5.5,
2026-09-27). Static.

  U1 initialisation: CharacterRenderRecord_ResetDefaults (0041F730) sets ebp = -1 (0041F768) and stores it into +0xC4
     and +0xC8 (dword) and +0xCC and +0xCE (word) - a fresh record has no bound entry and event -1.
  U2 scheduling: no thread procedure the image starts (the eleven of the F-1 control) reaches the getter 0041FCA0, the
     policy 004235C0, the lookup 0051F240, the event entry 00423B10, the two callers, or any of the seven render-record
     functions that store one of the four fields - so every reader and writer runs on the main thread.
     Control: the two large workers' walks are deep (over 500 functions).
  U3 no writer between the getter's read of +0xCC (0041FCB2) and the policy's re-read (00423605): the only calls on
     that path are 0020E600 and 0051B9E0 (a jmp to 0051F240); over their whole callee closure (0020E600, 0051F240,
     003AB7F0, 0036B130) the only non-stack store is the container entry's cache (0051F2B7 [rbx + 0x18]).
  U4 binding: the render-record code's stores to +0xC4/+0xC8/+0xCC/+0xCE are exactly 22 sites, and the only stores of
     a live id into +0xC4 or +0xC8 take the return of the admission 0051BA80 (004247B2/004247CA, 00425251); +0xCE is
     written only by ResetDefaults and 004247D0.
  U5 00424550: exactly 10 non-stack stores and 12 distinct callees.
  U6 00424D80: exactly 37 non-stack stores and 20 distinct callees; of its stack arguments it reads only the sixth
     (00424DFF, the policy selector).
  U7 re-bind versus fresh bind: 00424550 releases +0xC8 and resets it before admitting (004245CC/004245D1, then 00424798
     passes it), so it always admits a fresh slot; 00424D80 passes the CURRENT +0xC4 (0042522F) and keeps the old id
     (00425249) for its first-bind test (00425333).
  U8 routing: 00423B10 tail-jumps to 00424550 when 00422FD0 answers non-zero (00423C4F/00423C70) and otherwise calls
     00424D80 with sixth argument 0 (00423C96, 00423D73); 0042C410 calls 00424D80 with event 0x2001 and sixth argument 1.
  U9 return codes: 00424550 returns -1 (no source), -2 (admission failed) or 1; 00424D80 returns -1, -2 or 1.
  U10 the policy returns 1 unless both the candidate's and the current event's normalised kinds are 1 or 2, before it
     reaches the selector switch at 00423735 - so the getter's use of +0xCC as the selector cannot change its choice.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
W = ROOT / "Database/Tools/work"
d = (W / "exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(W / "graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: SIZES[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(a): return list(cs.disasm(d[off(a):off(a) + SIZES[a]], a))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
NOWRITE = ("cmp", "test", "bt", "push", "call", "jmp", "ucomiss", "comiss", "j", "nop", "prefetch")
def stores(a):
    out = []
    for x in body(a):
        ops = x.op_str.split(", ")
        if x.mnemonic.startswith(NOWRITE): continue
        if ops and "ptr [" in ops[0] and "[rsp" not in ops[0]:
            out.append((x.address, ("%s %s" % (x.mnemonic, x.op_str))))
    return out
def callees(a): return sorted({int(x.op_str, 16) for x in body(a) if x.mnemonic == "call" and x.op_str.startswith("0x")})

r = dis(0x41F768, 0x41F7BD)
check("U1 ResetDefaults stores -1 into +0xC4, +0xC8 (dword) and +0xCC, +0xCE (word)",
      r.get(0x41F768) == "or ebp, 0xffffffff" and r.get(0x41F7A3) == "mov dword ptr [rbx + 0xc4], ebp"
      and r.get(0x41F7A9) == "mov word ptr [rbx + 0xcc], bp" and r.get(0x41F7B0) == "mov dword ptr [rbx + 0xc8], ebp"
      and r.get(0x41F7B6) == "mov word ptr [rbx + 0xce], bp"
      and not any("ebp" in t and t.split(",")[0].endswith("ebp") for k, t in r.items() if 0x41F768 < k < 0x41F7A3))

F1 = ROOT / "Database/FFXII TZA/_index/candidates/f1-weather-apply-thread/f1_thread_reach.py"
g = {"__file__": str(F1)}
exec(compile(open(F1, encoding="utf-8").read().split("APPLY = 0x26D910")[0], str(F1), "exec"), g)
THREADS = [0x171370, 0x5CCAB0, 0x5CCBA0, 0x7DEC40, 0x7DD950, 0x863500, 0x7A5550, 0x35EA40, 0x368C10, 0x369100, 0x368AE0]
reach = {}
for e in THREADS:
    s = {e}; fr = [e]
    while fr:
        nx = []
        for f in fr:
            for c in g["callees"].get(f, ()):
                if c not in s: s.add(c); nx.append(c)
        fr = nx
    reach[e] = s
WRITERS = [0x41F730, 0x422A30, 0x422C20, 0x423980, 0x423F20, 0x424550, 0x424D80]
TARGETS = [0x41FCA0, 0x4235C0, 0x51F240, 0x423B10] + WRITERS
hits = {"%08X" % e: sorted("%08X" % t for t in TARGETS if t in reach[e]) for e in THREADS if any(t in reach[e] for t in TARGETS)}
check("U2 no thread procedure reaches the getter, the policy, the lookup, the event entry or any of the seven field writers",
      hits == {} and len(reach[0x35EA40]) > 500 and len(reach[0x369100]) > 500,
      "hits %s; control walks %d / %d" % (hits, len(reach[0x35EA40]), len(reach[0x369100])))

gt = dis(0x41FCA0, 0x41FCE4); pol = dis(0x4235C0, 0x42360D)
path_calls = [t for k, t in sorted(pol.items()) if t.startswith("call")]
lk = dis(0x51B9E0, 0x51B9E5)
def closure(a):
    seen = {a}; fr = [a]
    while fr:
        nx = []
        for f in fr:
            for x in body(f):
                if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
                    t = int(x.op_str, 16)
                    if t in SIZES and t not in seen and not f <= t < f + SIZES[f]: seen.add(t); nx.append(t)
        fr = nx
    return seen
cl = closure(0x20E600) | closure(0x51F240)
st20 = stores(0x20E600); st5f = [(k, t) for f in sorted(cl) for k, t in stores(f)]
check("U3 between 0041FCB2 and 00423605 the callee closure stores only the container entry cache (0051F2B7)",
      gt.get(0x41FCB2) == "movsx r8d, word ptr [rcx + 0xcc]" and gt.get(0x41FCC1) == "call 0x4235c0"
      and dis(0x423605, 0x42360D).get(0x423605) == "movsx r9d, word ptr [rsi + 0xcc]"
      and path_calls == ["call 0x20e600", "call 0x51b9e0"] and lk.get(0x51B9E0) == "jmp 0x51f240"
      and st20 == [] and sorted(cl) == [0x20E600, 0x36B130, 0x3AB7F0, 0x51F240]
      and st5f == [(0x51F2B7, "mov qword ptr [rbx + 0x18], rcx")], "%s %s" % (path_calls, st5f))

FIELD = re.compile(r"ptr \[r\w+ \+ 0xc[48ce]\]")
fam = []
for a in WRITERS:
    for k, t in stores(a):
        if FIELD.search(t.split(", ")[0]): fam.append(k)
EXP = [0x41F7A3, 0x41F7A9, 0x41F7B0, 0x41F7B6, 0x422AE4, 0x422AEB, 0x422BBD, 0x422C55, 0x422C5B, 0x422C83, 0x4239B1,
       0x423F6B, 0x423FA0, 0x4245D1, 0x4247B2, 0x4247CA, 0x4247D0, 0x424E61, 0x424E8B, 0x424FAB, 0x425251, 0x425274]
b5 = dis(0x4247AD, 0x4247D8); b6 = dis(0x425244, 0x425257)
ce = [k for k in fam if k in (0x41F7B6, 0x4247D0)]
check("U4 22 render-record stores of the four fields; live ids into +0xC4/+0xC8 come only from 0051BA80's return; +0xCE only at ResetDefaults and 004247D0",
      sorted(fam) == EXP and b5.get(0x4247AD) == "call 0x51ba80" and b5.get(0x4247B2) == "mov dword ptr [rdi + 0xc8], eax"
      and b5.get(0x4247CA) == "mov dword ptr [rdi + 0xc8], eax" and b6.get(0x425244) == "call 0x51ba80"
      and b6.get(0x42524F) == "mov edi, eax" and b6.get(0x425251) == "mov dword ptr [rbx + 0xc4], eax"
      and ce == [0x41F7B6, 0x4247D0], "%d sites" % len(fam))

s5 = stores(0x424550); c5 = callees(0x424550)
check("U5 00424550: 10 non-stack stores, 12 distinct callees",
      [k for k, _ in s5] == [0x4245D1, 0x4247B2, 0x4247CA, 0x4247D0, 0x4247FF, 0x424815, 0x42481F, 0x424832, 0x42483B, 0x424842]
      and c5 == [0x20E600, 0x2ED570, 0x372280, 0x3AB7F0, 0x409090, 0x409FA0, 0x41D4D0, 0x4235C0, 0x51B9E0, 0x51BA40, 0x51BA80, 0x808C40],
      "%d stores, %d callees" % (len(s5), len(c5)))
s6 = stores(0x424D80); c6 = callees(0x424D80)
argreads = [x.address for x in body(0x424D80) if re.search(r"\[rsp \+ 0x1[0-9a-f]{2}\]", x.op_str)]
check("U6 00424D80: 37 non-stack stores, 20 distinct callees, and the sixth stack argument is the only one read",
      len(s6) == 37 and s6[0][0] == 0x424E61 and s6[-1][0] == 0x425386
      and c6 == [0x20E600, 0x20E620, 0x3326C0, 0x372510, 0x3AB7F0, 0x3E57D0, 0x3E7D10, 0x409090, 0x409210, 0x409FA0,
                 0x409FD0, 0x41C760, 0x41F010, 0x420EA0, 0x422D10, 0x422D50, 0x4235C0, 0x51B9E0, 0x51BA80, 0x808C40]
      and argreads == [0x424DFF] and dis(0x424DFF, 0x424E07).get(0x424DFF) == "mov r8d, dword ptr [rsp + 0x118]",
      "%d stores, %d callees, arg reads %s" % (len(s6), len(c6), ["%08X" % a for a in argreads]))

e5 = dis(0x424798, 0x42479E); e6 = dis(0x42522F, 0x425235); e7 = dis(0x425249, 0x42524F); e8 = dis(0x425333, 0x425336)
check("U7 00424550 admits after releasing +0xC8; 00424D80 passes the current +0xC4 and keeps the old id for its first-bind test",
      e5.get(0x424798) == "mov edx, dword ptr [rdi + 0xc8]" and e6.get(0x42522F) == "mov edx, dword ptr [rbx + 0xc4]"
      and e7.get(0x425249) == "mov ebp, dword ptr [rbx + 0xc4]" and e8.get(0x425333) == "cmp ebp, -1")

r1 = dis(0x423C4F, 0x423CAD); r2 = dis(0x423D73, 0x423D8A); r3 = dis(0x42C66D, 0x42C68E)
check("U8 00423B10 routes to 00424550 on 00422FD0 != 0, else 00424D80 with selector 0; 0042C410 passes 0x2001 with selector 1",
      r1.get(0x423C4F) == "call 0x422fd0" and r1.get(0x423C56) == "je 0x423c75" and r1.get(0x423C70) == "jmp 0x424550"
      and r1.get(0x423C96) == "mov dword ptr [rsp + 0x28], 0" and r1.get(0x423CA8) == "call 0x424d80"
      and r2.get(0x423D73) == "mov dword ptr [rsp + 0x28], 0" and r2.get(0x423D85) == "call 0x424d80"
      and r3.get(0x42C66D) == "mov dword ptr [rsp + 0x28], 1" and r3.get(0x42C675) == "mov r9d, 0x2001"
      and r3.get(0x42C689) == "call 0x424d80")

v5 = dis(0x4245ED, 0x4245F0) | dis(0x4247BD, 0x4247C2) | dis(0x42484C, 0x424851)
v6 = dis(0x424DBD, 0x424DC0) | dis(0x42525C, 0x42525F) | dis(0x4250A7, 0x4250AC) | dis(0x425377, 0x42537C)
check("U9 return codes: 00424550 -1 / -2 / 1; 00424D80 -1 / -2 (edi = -1 minus 1) / 1",
      v5.get(0x4245ED) == "or eax, 0xffffffff" and v5.get(0x4247BD) == "mov eax, 0xfffffffe" and v5.get(0x42484C) == "mov eax, 1"
      and v6.get(0x424DBD) == "or eax, 0xffffffff" and v6.get(0x42525C) == "lea eax, [rdi - 1]"
      and v6.get(0x4250A7) == "mov eax, 1" and v6.get(0x425377) == "mov eax, 1")
k = dis(0x4236B0, 0x423737)
check("U10 before the selector switch (00423735) the policy returns 1 unless both normalised kinds are 1 or 2 - so a +0xCC of 0, 1 or 2 (kind 0) never reaches it",
      k.get(0x4236B9) == "cmp eax, 1" and k.get(0x4236E6) == "cmp eax, 2" and k.get(0x4236E9) == "jne 0x4236cc"
      and k.get(0x423715) == "cmp eax, 1" and k.get(0x423724) == "cmp eax, 2" and k.get(0x423727) == "jne 0x4236cc"
      and k.get(0x4236CC) == "mov eax, 1" and k.get(0x42370D) == "mov eax, ecx" and k.get(0x423735) == "test ebx, ebx")
print("FAILS", fails)
sys.exit(1 if fails else 0)
