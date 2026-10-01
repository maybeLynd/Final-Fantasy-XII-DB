"""e2_path_census.py - for every (language, kind, id) the FST sizes, does the path ResourcePath_Init installs exist in
FFXII_TZA.vbf under the stream resolver's route-2 normalisation?  (OV-33 E2)

Why: on 002DF780's loose route, 001D6F20 returns null only when the source record stays unset, i.e. route 1 (RAM
cache, 001D6D20) is skipped or misses AND route 2 (package lookup 0019AEE0 at 0059F187-0059F19E) returns null.
Route 2 looks up  lower(replace(path.lstrip('./\\\\'), '\\\\', '/'))  (0059F111-0059F185). If every sized path is in the
archive under that key, route 2 cannot miss for a request that passed E1.

Method: a small symbolic run of ResourcePath_Init 002DF9A0 per language id (0..11, the 01E88B00 order) and per value of
its second argument edx (the 002DFF86 'jne' skips the kind-7 element patches when edx != 0), tracking
lea reg,[rip+X] / mov [rip+slot],reg / mov reg,[rip+slot] / mov [reg+disp],reg2 . Every other instruction that writes
memory is reported as UNHANDLED (must be 0). Then each sized (kind,id) of that language's .fst is resolved to
*(array + 8*id) (patched value if patched, else the file's qword; BSS reads 0 = NULL).

Also reported per path: whether the resolver's extension filter (0059EF4B-0059EFA9) sends it straight to route 2.
Positive controls: (US, kind 0, id 0) -> ps2data/cdi/in/system.cnf present; kind 35's array names ff12menuoverlay (so
arrays are being read); one known-absent key ('ps2data/nonexistent') is reported absent.
Terminal line: FAILS n / STATUS.
"""
import sys, struct, os
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools")
import tk, vbfextract
from capstone.x86 import X86_OP_MEM, X86_OP_REG
FSTDIR = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FileSizeTables"
VBF = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf"
LANGS = ["JP", "US", "FR", "DE", "IT", "ES", "UK", "KR", "CH", "ASIA", "IN", "CN"]
SLOT0, SLOTN = 0x215F000, 0x215F000 + 41 * 8
FN = 0x2DF9A0; STOP = 0x2E03F5
fails = 0
insns = {x.address: x for x in tk.fdis(FN)}
order = sorted(insns)
nxt = {a: order[i + 1] for i, a in enumerate(order[:-1])}
def R(x, reg): return x.reg_name(reg)
def full(r):
    m = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "r8d": "r8", "r9d": "r9", "r10d": "r10", "r11d": "r11"}
    return m.get(r, r)
unhandled = set()
def run(lang, edx):
    regs = {"r8": lang, "rdx": edx, "r10": 0x120000}
    slots = {}; patches = {}
    a = FN; steps = 0
    while a != STOP and steps < 5000:
        steps += 1
        x = insns[a]; ops = x.operands; mn = x.mnemonic
        if a == 0x2DFBAF:                      # lea eax,[r8-1]; cmp eax,0xa; ja 2DFF32; table at 0x120000+0x1c04b0
            k = (lang - 1) & 0xFFFFFFFF
            if k > 10: a = 0x2DFF32
            else: a = 0x120000 + tk.u32(0x120000 + 0x1C04B0 + 4 * k)
            continue
        if a == 0x2DFF86:                      # test edx,edx ; jne 2E03F5
            a = STOP if edx else nxt[nxt[a]]
            continue
        if mn == "jmp" and ops[0].type != X86_OP_MEM and x.op_str.startswith("0x"):
            a = int(x.op_str, 16); continue
        if mn == "lea" and ops[1].type == X86_OP_MEM and ops[1].mem.base and R(x, ops[1].mem.base) == "rip":
            regs[full(R(x, ops[0].reg))] = x.address + x.size + ops[1].mem.disp
        elif mn == "mov" and ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_REG:
            m = ops[0].mem; src = regs.get(full(R(x, ops[1].reg)))
            if m.base and R(x, m.base) == "rip":
                t = x.address + x.size + m.disp
                if SLOT0 <= t < SLOTN + 0x100: slots[t] = src
                elif t < 0x2EC3EE0 or t >= 0x2EC3EE0 + 0xC8320: unhandled.add("%08X %s %s" % (a, mn, x.op_str))
            elif m.base and not m.index and full(R(x, m.base)) in regs:
                patches[regs[full(R(x, m.base))] + m.disp] = src
            elif not (m.base and R(x, m.base) == "rsp"):
                unhandled.add("%08X %s %s" % (a, mn, x.op_str))
        elif mn == "mov" and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM and ops[1].mem.base and R(x, ops[1].mem.base) == "rip":
            t = x.address + x.size + ops[1].mem.disp
            regs[full(R(x, ops[0].reg))] = slots.get(t, 0) if SLOT0 <= t < SLOTN + 0x100 else ("mem", t)
        elif ops and ops[0].type == X86_OP_MEM and mn not in ("cmp", "test"):
            if not (ops[0].mem.base and R(x, ops[0].mem.base) == "rsp"):
                unhandled.add("%08X %s %s" % (a, mn, x.op_str))
        elif mn.startswith("j") and mn != "jmp":
            unhandled.add("%08X unexpected branch %s %s" % (a, mn, x.op_str))
        a = nxt[a]
    return slots, patches
def cstr(va):
    o = tk.off(va)
    if o is None: return None
    e = tk.d.index(b"\0", o)
    return tk.d[o:e].decode("latin-1")
def norm(p): return p.lstrip("./\\").replace("\\", "/").lower()
def filter_hit(p):
    b = p.encode("latin-1"); n = len(b)
    if n <= 3: return True
    if b[-4] == 0x2E or b[-3] == 0x6D or b[-2] == 0x61 or b[-1] == 0x62: return True
    if n <= 4: return True
    if b[-5] == 0x2E or b[-4] == 0x77 or b[-3] == 0x65 or b[-2] == 0x62 or b[-1] == 0x6D: return True
    return False
f = open(VBF, "rb"); names, blocks = vbfextract.load_index(f)
arch = set(k.lower() for k in names)
print("archive entries: %d" % len(arch))
print("control absent key reported absent:", "ps2data/nonexistent" not in arch)
tot_absent = 0; absent_rows = []; ctl_sys = False; ctl_35 = False
for li, L in enumerate(LANGS):
    fst = struct.unpack("<205000i", open(os.path.join(FSTDIR, "FileSizeTable_%s.fst" % L), "rb").read())
    for edx in (1, 0):
        slots, patches = run(li, edx)
        n_sized = n_null = n_present = n_absent = n_fhit = 0
        for k in range(41):
            arr = slots.get(SLOT0 + 8 * k)
            for i in range(5000):
                if fst[k * 5000 + i] == -1: continue
                n_sized += 1
                pa = arr + 8 * i if isinstance(arr, int) else None
                v = patches.get(pa) if pa in patches else (tk.u64(pa) if pa is not None else None)
                if not v:
                    n_null += 1; absent_rows.append((L, edx, k, i, "NULL")); continue
                p = cstr(v)
                if p is None: n_null += 1; absent_rows.append((L, edx, k, i, "unreadable %X" % v)); continue
                if k == 35: ctl_35 |= "ff12menuoverlay" in p.lower()
                if L == "US" and k == 0 and i == 0 and norm(p) == "ps2data/cdi/in/system.cnf" and norm(p) in arch: ctl_sys = True
                fh = filter_hit(p); n_fhit += fh
                if norm(p) in arch: n_present += 1
                else: n_absent += 1; absent_rows.append((L, edx, k, i, p))
        tot_absent += n_absent
        print("%-4s edx=%d sized %5d  NULL %d  present %5d  ABSENT %d  (route-2-direct by filter: %d)" % (L, edx, n_sized, n_null, n_present, n_absent, n_fhit))
# kind 35 array names (sized or not) as the array-reading control
slots, patches = run(1, 1)
a35 = slots.get(SLOT0 + 8 * 35)
v = tk.u64(a35) if isinstance(a35, int) else None
s35 = cstr(v) if v else None
ctl_35 = ctl_35 or (s35 is not None and "ff12menuoverlay" in s35.lower())
print("kind 35 array head:", s35)
print("\nNULL / ABSENT rows (language, edx, kind, id, path):")
for r in absent_rows[:200]: print("  ", r)
print("rows listed: %d" % len(absent_rows))
print("UNHANDLED memory-writing or branch instructions in the symbolic run: %d" % len(unhandled))
for u in sorted(unhandled): print("  ", u)
print("control system.cnf present:", ctl_sys); fails += not ctl_sys
print("control kind-35 array names ff12menuoverlay:", ctl_35); fails += not ctl_35
fails += len(unhandled) > 0
print("FAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
