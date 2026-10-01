"""SWE2-AUDIT-SEM, independent static checks on SWE2-DATA's DD owner read batch 3 (71af93479): the 002AF340 return and
the 00916548 stop string, the stepper modes (UQ-173's routed claim, SD-100), the second dispatcher 003CD2C0 (SD-120),
the +0x2FE0 census scope, and whether the database BEFORE the commit already answers parts of SD-124, SD-125 and
SD-128.  Static reads of the certified image through retool.py; page texts from git at 71af93479^ (the parent).
Prints PASS/FAIL per check with controls; exit 1 on any FAIL.  Run: python -B dd3_sem.py"""
import os, re, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
GFZ = os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts")
sys.path.insert(0, GFZ)
import retool as T  # noqa: E402
R = T.R
PARENT = "71af93479^"
DBP = "Database/FFXII TZA/"
fails = 0
def check(name, ok, detail=""):
    global fails
    fails += 0 if ok else 1
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (" - " + str(detail)) if detail != "" else ""))
def page(p):
    return subprocess.run(["git", "-C", REPO, "show", "%s:%s%s" % (PARENT, DBP, p)], capture_output=True).stdout.decode("utf-8", "replace")
SZ = T.sizes()
def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))
def rng(lo, hi):
    return list(R.md.disasm(R.at(lo, hi - lo), lo))
def rip(i):
    for op in i.operands:
        if op.type == 3 and op.mem.base == T.RIP:
            return i.address + i.size + op.mem.disp
C = T.scan()

print("== 002AF340's return and the 00916548 stop string")
ins = body(0x002AF340); ops = {i.address: (i.mnemonic, i.op_str) for i in ins}
check("M1 one ret; eax = -1 (002AF922) only when [rsp+0x3C] != 0 and [rsp+0x20] != 0 and r13d == 0, else eax = r12d (002AF927)",
      [i.address for i in ins if i.mnemonic == "ret"] == [0x002AF95A] and ops[0x002AF902] == ("cmp", "dword ptr [rsp + 0x3c], 0")
      and ops[0x002AF91D] == ("test", "r13d, r13d") and ops[0x002AF922] == ("or", "eax, 0xffffffff") and ops[0x002AF927] == ("mov", "eax, r12d"))
check("M2 r13d (the 'met' flag) is set only by the memcmp result against the context's +0x10C8 string (002AF563 / 002AF56F)",
      ops[0x002AF414] == ("mov", "r15, qword ptr [rax + 0x10c8]") and ops[0x002AF56F] == ("cmove", "r13d, eax"))
check("M3 00916548 is the string 0F 23 00: the '#' escape (0x0F lead, '#' selector)", R.at(0x00916548, 3) == b"\x0f\x23\x00", R.at(0x00916548, 4).hex())

print("== the reveal stepper 002ABF70 (SD-100, and UQ-173's routed mode-5 line)")
tab = [struct.unpack_from("<I", R.at(0x002AC1B4, 32), 4 * k)[0] + 0x120000 for k in range(8)]
check("S1 the mode table at 002AC1B4: 0,1,4 -> 002AC06B; 2 -> 002AC04F; 3 -> 002ABF9F; 5 -> 002ABFFC; 6 -> 002AC1AB (return); 7 -> 002AC18B",
      tab == [0x2AC06B, 0x2AC06B, 0x2AC04F, 0x2ABF9F, 0x2AC06B, 0x2ABFFC, 0x2AC1AB, 0x2AC18B], ["%08X" % t for t in tab])
dec = [i.address for i in body(0x002ABF70) if i.mnemonic == "mov" and i.op_str.startswith("word ptr [rbx + 0x88]")]
check("S2 +0x88 is decremented only in the mode-3 (002ABFB3) and mode-7 (002AC19B) arms; the mode-5 arm 002ABFFC..002AC04E never touches it",
      dec == [0x002ABFB3, 0x002AC19B] and not any("0x88]" in i.op_str for i in rng(0x002ABFFC, 0x002AC04F)), ["%08X" % d for d in dec])
m3 = rng(0x002ABF9F, 0x002ABFFC)
check("S3 wording: mode 3 also steps the target every tick while it counts (a nonzero decrement jumps to the step at 002ABFCA), and at zero sets +0x9B = 0x1E and mode 0",
      any(i.address == 0x002ABFBA and i.op_str == "0x2abfca" for i in m3) and any(i.op_str == "word ptr [rbx + 0x90], ax" for i in m3)
      and any(i.op_str == "byte ptr [rbx + 0xb0], 0" for i in m3))
esc = rng(0x002AD214, 0x002AD252); eo = {i.address: i.op_str for i in esc}
check("S4 the '#' escape: payload 0 -> mode 5, +0x88 = 10000 (0x2710), +0xB0 |= 0x4080000; payload p -> +0x88 = p * 30, mode byte not written in this arm",
      eo.get(0x002AD225) == "byte ptr [r14 + 0xb0], 5" and eo.get(0x002AD22D) == "eax, 0x2710" and eo.get(0x002AD232) == "dword ptr [r14 + 0xb0], 0x4080000"
      and eo.get(0x002AD220) == "eax, eax, 0x1e" and eo.get(0x002AD23D) == "word ptr [r14 + 0x88], ax")

print("== the two byte-opcode dispatchers (SD-120)")
def arms(table):
    return [struct.unpack_from("<I", R.at(table, 32), 4 * k)[0] + 0x120000 for k in range(8)]
def first_op(a, stop):
    for i in R.md.disasm(R.at(a, 0x200), a):
        if i.address >= stop or i.mnemonic == "ret":
            break
        if i.mnemonic == "call" and i.op_str.startswith("0x50"):
            return int(i.op_str, 16)
A1, A2 = arms(0x003CD298), arms(0x003CD570)
def opmap(a):
    s = sorted(a) + [max(a) + 0x60]
    return [first_op(x, s[s.index(x) + 1]) for x in a]
M1, M2 = opmap(A1), opmap(A2)
d1 = {i.address: i.op_str for i in rng(0x003CD0E6, 0x003CD0F6)}; d2 = {i.address: i.op_str for i in rng(0x003CD3DD, 0x003CD3ED)}
check("D1 both dispatchers index their 8-entry tables by (opcode byte - 1)", "eax" in d1.get(0x003CD0E9, "") and "eax" in d2.get(0x003CD3E0, "")
      and d1.get(0x003CD0EB) == "eax, 7" and d2.get(0x003CD3E2) == "eax, 7")
check("D2 per opcode 1..8 the 0050xxxx operation each arm calls is the same in 003CCF20 and 003CD2C0",
      M1 == M2 and all(M1), ["%d:%08X" % (k + 1, m) for k, m in enumerate(M1)])
check("C1 control: 003CCF20's map is the page's section 16 table (1 0050AC20 ... 8 00507120)",
      M1 == [0x50AC20, 0x506B40, 0x5080A0, 0x50A100, 0x509BB0, 0x507490, 0x508C90, 0x507120])

print("== the +0x2FE0 census scope")
out = subprocess.run([sys.executable, "-B", os.path.join(GFZ, "retool.py"), "grep", r"0x2fe0\]"], capture_output=True, cwd=GFZ).stdout.decode()
fs = {}
for l in out.splitlines():
    p = l.split()
    if len(p) > 2 and re.fullmatch(r"[0-9A-F]{8}", p[0]):
        fs.setdefault(p[0], []).append(p[1])
check("P1 image-wide, every literal +0x2FE0 displacement is one of the page's fourteen sites in the three named functions",
      {k: len(v) for k, v in fs.items()} == {"002778C0": 9, "00279E20": 4, "00276D30": 1}, {k: len(v) for k, v in fs.items()})

print("== SD-124: 0035BB20 and the records 002732E0 matches")
bb = {i.address: (i.mnemonic, i.op_str, rip(i)) for i in body(0x0035BB20)}
check("Q1 0035BB20 is read: i < word[022C8064] -> 022C8080 + i*0xC0, else 0",
      bb[0x0035BB20][2] == 0x022C8064 and bb[0x0035BB2E][2] == 0x022C8080 and bb[0x0035BB39][1] == "rax, 6" and bb[0x0035BB41][1] == "eax, eax")
f = {i.address: (i.op_str, rip(i)) for i in rng(0x0035BDB0, 0x0035BE70)}
check("Q2 the slot walk 0035BC50: slot +4 is the handle 003588B0 resolves and the one compared with the focus handle 022C806C; 022C8064 counts accepted slots",
      f[0x0035BDCF][0] == "ecx, dword ptr [rdi - 0x5c]" and f[0x0035BE0D][0] == "dword ptr [rdi - 0x5c], eax" and f[0x0035BE00][1] == 0x022C806C
      and f[0x0035BE4C][1] == 0x022C8064)
ld = page("00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md")
lp = page("16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md")
check("Q3 at the parent, the ladder page names the four 0xC0 slots at 022C8080..022C82C0 and the packed actor handle at +0x04, and the layout page reads 0035BB20",
      "The slots\n> are at `022C8080`, `022C8140`, `022C8200` and `022C82C0`" in ld and "**packed actor handle at `+0x04`**" in ld
      and "**0035BB20** (36 B, 4 A-measured callers) — bounded indexed getter" in lp)

print("== SD-125: who sets +0x2FF0 bit 0x4000")
out = subprocess.run([sys.executable, "-B", os.path.join(GFZ, "retool.py"), "grep", r"0x2ff0\], 0x4000"], capture_output=True, cwd=GFZ).stdout.decode()
w = [l.split()[:2] for l in out.splitlines() if re.match(r"[0-9A-F]{8} ", l)]
s = {i.address: i.op_str for i in rng(0x002795AE, 0x002795CD)}
check("K1 image-wide the only immediate 0x4000 op on +0x2FF0 besides the confirm arm's test is 002778C0's set at 002795B5; the clear at 002795C2 is its else",
      sorted(tuple(x) for x in w) == [("00276D30", "00276FD8"), ("002778C0", "002795B5")]
      and s.get(0x002795AE) == "qword ptr [r12 + 8], rdi" and s.get(0x002795C2) == "dword ptr [r15 + 0x2ff0], 0xffffbfff", w)

print("== SD-128: 002C7660")
ud = page("04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md")
cl = {i.op_str for i in body(0x002C7660) if i.mnemonic == "call"}
check("U1 002C7660 calls 002C8310 and 002C7B10 (the row's two callees)", {"0x2c8310", "0x2c7b10"} <= cl)
check("U2 at the parent, it has a page row: the unit-display-record page lists it as the display-record channel evaluation (caller 002C62B0), interior verified",
      "| `002C7660` | 1190 | display-record channel evaluation (caller `002C62B0`)" in ud)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
