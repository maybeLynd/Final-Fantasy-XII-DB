"""pa1_dispatch.py - PA-1: does anything dispatch the application's vtable slots 10, 15, 16, 22, 23 and 24?
(FABLE, Claude Opus 5.5, 2026-09-27.) Static.

The application object is followed from every source the image gives it:
  - the global 02EA5368 its constructor publishes (00792550);
  - the window procedure's GetWindowLongPtrA result (IAT 008C2880);
  - the static GameApplication object 01F7E350 (a `lea` gives the object, a qword load gives its vtable);
  - `this` in every method of the GameApplication (008C5760) and PApplication (01CB2508) vtables.
It is followed through register copies and stack spills, and into callees that receive it in rcx, rdx, r8 or r9, to
depth 4. Every call or jmp through [vtable + 8k], and every call of a register loaded from there, is recorded.
  P1 control: the tracker finds the framework's known dispatches the page names: slot 4 (0079C2D6), slot 8 (0079C655),
     slot 9 (0079C1F1, 0079C526, 007A08C3) and slot 25 (0079D087, 0079D107, 0079D181).
  P2 no traced route dispatches slot 10, 15, 16, 22, 23 or 24.
  P3 the pointer's stores into memory, and what reads them:
     - the tracker finds four: the global (00792550), a callback record (0017CF96) and PApplicationScriptProxy +0x38
       (00792790, 0079F3E4);
     - the callback 0017D150 is a jmp to 0017D000, which makes no virtual call;
     - the 15 script commands 007A0180 registers make virtual calls only through offsets 0x38, 0x40 and 0xE0.
  P4 the null-checked thunks at the six offsets that sit beside the application code (0017F160 +0x78, 0017F170 +0xB8,
     0017F1B0 +0xB0) have one caller, 0053AB50, which passes [r12+0x6B8], a CharacterRenderObject, not the application.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
DIS = {}
def ins(f):
    if f not in DIS:
        o = off(f); DIS[f] = list(cs.disasm(d[o:o + SIZES.get(f, 0)], f)) if o is not None and SIZES.get(f, 0) > 0 else []
    return DIS[f]
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) if m else None
def q(v): return struct.unpack_from("<Q", d, off(v))[0]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

R64 = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", **{"r%dd" % j: "r%d" % j for j in range(8, 16)}}
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}; ARGS = ["rcx", "rdx", "r8", "r9"]
APPG, GWLP, APPOBJ = 0x2EA5368, 0x8C2880, 0x1F7E350
SLOT = re.compile(r"qword ptr \[(r\w+)(?: \+ (0x[0-9a-f]+|\d+))?\]$")
SPILL = re.compile(r"qword ptr \[rsp \+ (0x[0-9a-f]+|\d+)\]$")
hits = collections.defaultdict(set); esc = set(); seen = set()
def run(f, app0, depth):
    key = (f, tuple(sorted(app0)))
    if key in seen or depth < 0: return
    seen.add(key)
    app = set(app0); vt = set(); stk = set(); vstk = set(); loaded = {}
    for x in ins(f):
        s = x.op_str; mn = x.mnemonic; t = rip(x)
        dst = s.split(",")[0].strip(); dst64 = R64.get(dst, dst); src = s.split(",", 1)[1].strip() if "," in s else ""
        if mn in ("call", "jmp"):
            m = SLOT.match(s)
            if m and m.group(1) in vt: hits[int(m.group(2) or "0", 0) // 8].add(x.address)
            if mn == "call" and s in loaded: hits[loaded[s]].add(x.address)
            if s.startswith("0x"):
                c = int(s, 16)
                if not (mn == "jmp" and f <= c < f + SIZES.get(f, 0)):
                    passed = {r for r in ARGS if r in app}
                    if passed and c in SIZES: run(c, passed, depth - 1)
            if mn == "call":
                if t == GWLP: app -= VOL; vt -= VOL; app.add("rax"); continue
                app -= VOL; vt -= VOL; loaded = {k: v for k, v in loaded.items() if k not in VOL}
            continue
        if mn == "lea" and t == APPOBJ: app.add(dst64); vt.discard(dst64); continue
        if mn == "mov":
            if t == APPG and "qword ptr" in src: app.add(dst64); vt.discard(dst64); continue
            if t == APPOBJ and "qword ptr" in src: vt.add(dst64); app.discard(dst64); continue
            if re.fullmatch(r"r\w+", src) and src in app and "ptr" not in dst: app.add(dst64); continue
            m = SPILL.match(dst)
            if m and src in app: stk.add(m.group(1)); continue
            if m and src in vt: vstk.add(m.group(1)); continue
            if src in app and "ptr [" in dst: esc.add(x.address)
            m = SPILL.match(src)
            if m and m.group(1) in stk: app.add(dst64); vt.discard(dst64); continue
            if m and m.group(1) in vstk: vt.add(dst64); app.discard(dst64); continue
            m = re.match(r"qword ptr \[(r\w+)\]$", src)
            if m and m.group(1) in app: vt.add(dst64); app.discard(dst64); continue
            m = SLOT.match(src)
            if m and m.group(1) in vt: loaded[dst64] = int(m.group(2) or "0", 0) // 8; app.discard(dst64); vt.discard(dst64); continue
        if re.fullmatch(r"r\w+|e\w\w", dst) and mn not in ("cmp", "test", "push"):
            app.discard(dst64); vt.discard(dst64); loaded.pop(dst64, None)
for f in sorted(SIZES):
    if 0x121000 <= f < 0x8C0000 and SIZES[f] > 0 and any(rip(x) in (APPG, GWLP, APPOBJ) for x in ins(f)): run(f, set(), 4)
for v0 in (0x8C5760, 0x1CB2508):
    for k in range(31):
        m = q(v0 + 8 * k)
        if m in SIZES: run(m, {"rcx"}, 4)

known = {4: {0x79C2D6}, 8: {0x79C655}, 9: {0x79C1F1, 0x79C526, 0x7A08C3}, 25: {0x79D087, 0x79D107, 0x79D181}}
miss = {k: sorted("%08X" % a for a in v - hits[k]) for k, v in known.items() if v - hits[k]}
check("P1 control: the page's framework dispatches of slots 4, 8, 9 and 25 are found", not miss,
      "missing %s; slots found %s" % (miss, sorted(hits)))
six = {k: sorted("%08X" % a for a in hits[k]) for k in (10, 15, 16, 22, 23, 24) if hits[k]}
check("P2 no traced route dispatches slot 10, 15, 16, 22, 23 or 24", not six, str(six))

cb = [(x.mnemonic, x.op_str) for x in ins(0x17D150)]
cbv = [x for x in ins(0x17D000) if x.mnemonic in ("call", "jmp") and not x.op_str.startswith("0x")]
cmds = []; h = None
for x in ins(0x7A0180):
    if x.mnemonic == "lea" and x.op_str.startswith("rdx"): h = rip(x)
    if x.mnemonic == "call" and x.op_str == "0x7a0090": cmds.append(h)
offs = set()
for h in cmds:
    for x in ins(h):
        m = re.match(r"qword ptr \[(r\w+) \+ (0x[0-9a-f]+)\]$", x.op_str)
        if x.mnemonic in ("call", "jmp") and m and m.group(1) != "rip": offs.add(int(m.group(2), 16))
check("P3 the pointer escapes to four stores; the callback makes no virtual call; the 15 script commands dispatch only +0x38/+0x40/+0xE0",
      esc == {0x792550, 0x17CF96, 0x792790, 0x79F3E4} and cb == [("jmp", "0x17d000")] and not cbv and len(cmds) == 15 and offs <= {0x38, 0x40, 0xE0},
      "escapes %s; commands %d; their virtual offsets %s" % (sorted("%08X" % a for a in esc), len(cmds), sorted(hex(o) for o in offs)))

thunks = {0x17F160: "0x78", 0x17F170: "0xb8", 0x17F1B0: "0xb0"}
ok4 = all(any(x.mnemonic == "jmp" and x.op_str == "qword ptr [rax + %s]" % o for x in ins(t)) for t, o in thunks.items())
callers = collections.defaultdict(list)
for f in sorted(SIZES):
    if not 0x121000 <= f < 0x8C0000: continue
    o = off(f)
    if o is None or SIZES[f] <= 0: continue
    blob = d[o:o + SIZES[f]]
    for t in thunks:
        for i in range(len(blob) - 4):
            if blob[i] == 0xE8 and f + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] == t: callers[t].append((f, f + i))
one = all(len(v) == 1 and v[0][0] == 0x53AB50 for v in callers.values()) and len(callers) == 3
at = {x.address: x for x in ins(0x53AB50)}
rcx_src = all(any(at.get(a - k) is not None and at[a - k].op_str == "rcx, qword ptr [r12 + 0x6b8]" for k in range(1, 40)) for _, a in [v[0] for v in callers.values()])
check("P4 the three thunks at +0x78/+0xB0/+0xB8 have one caller, 0053AB50, passing [r12+0x6B8]", ok4 and one and rcx_src,
      str({"%08X" % t: ["%08X" % a for _, a in v] for t, v in callers.items()}))
print("FAILS", fails)
sys.exit(1 if fails else 0)
