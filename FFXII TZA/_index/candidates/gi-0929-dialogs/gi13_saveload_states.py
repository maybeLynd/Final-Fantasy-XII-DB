#!/usr/bin/env python3
"""gi13_saveload_states.py - GI-13 (FABLE, 2026-09-29): the save/load controller's storage notifications and states.

Checks, from the shipping EXE and the shipped us text:
  * the three sub-command-0x1D producers and the class each posts (3 / 0xD / 0xF), with a scan for every
    `mov edx,0x1d` + call in listed code (positive control: 00581D4D, the save-transaction post);
  * the 15-arm state table of 00580EB0 and the popup id each arm selects;
  * the 31-entry popup table 00D23DA0 resolved to shipped strings (us menu_message.bin);
  * the three handlers' branch constants (00580A80 / 00580B40 / 00580CD0);
  * the call-site census into 00580EB0 (23 E8/E9 sites, 0 jcc, no pointer) and that no site passes state 7;
  * the regression: the old reading "3 / 0xD / 0xF are storage-result codes" fails because the same payload's +8 is
    the storage status, read separately by each handler (cmp dword [rdx+8] at 00580A92, mov edx,[rdx+8] at 00580B5C,
    cmp [rsi+8] at 00580D12).
Exit status is the number of failed checks.
"""
import struct, sys, os, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
FST = r"D:/FFXII MP Mod/FFXII_TestClient1/FileSizeTables/FileSizeTable_US.fst"
BIN = r"D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    secs.append((struct.unpack_from("<I", d, o + 12)[0], struct.unpack_from("<I", d, o + 8)[0], struct.unpack_from("<I", d, o + 20)[0], d[o:o + 8].rstrip(b"\0")))
def off(a):
    r = a - BASE
    for va, vs, ro, _ in secs:
        if va <= r < va + vs: return ro + (r - va)
funcs = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(fn): return list(md.disasm(d[off(fn):off(fn) + funcs[fn]], fn))
def at(a, n=1): return list(md.disasm(d[off(a):off(a) + 16 * n], a))[:n]
def u32(a): return struct.unpack_from("<I", d, off(a))[0]
fails = 0
def check(name, ok, detail=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + (" :: " + detail if detail else ""))
    if not ok: fails += 1
# --- text resolution (002F9860: group = id/1000 -> loader byte 01E09F68 -> FileSizeTable size -> st2e row) ---
fst = open(FST, "rb").read()
sizes = {}
for f in os.listdir(BIN): sizes.setdefault(os.path.getsize(os.path.join(BIN, f)), []).append(f)
def dec(s):
    o = ""
    for c in s:
        if 0x20 <= c <= 0x39: o += chr(65 + c - 0x20)
        elif 0x3A <= c <= 0x53: o += chr(97 + c - 0x3A)
        elif 0x54 <= c <= 0x5D: o += chr(48 + c - 0x54)
        elif c == 4: o += " "
        elif c == 2: o += " / "
        elif c == 0xA8: o += "."
        elif c == 0xA7: o += ","
        elif c == 0x9A: o += "?"
        elif c == 0x99: o += "!"
        else: o += "{%02X}" % c
    return o
def text(tid):
    g, row = divmod(tid, 1000)
    lid = struct.unpack_from("<b", d, off(0x01E09F68 + g))[0]
    size = struct.unpack_from("<i", fst, 4 * (2 * 5000 + lid))[0]
    out = []
    for f in sizes.get(size, []):
        t = open(os.path.join(BIN, f), "rb").read()
        tab = struct.unpack_from("<I", t, 0x14)[0]; cnt = struct.unpack_from("<I", t, tab + 12)[0]
        if row < cnt:
            o = struct.unpack_from("<I", t, tab + 16 + 4 * row)[0]; st = tab + 12 + o
            out.append(dec(t[st:t.index(b"\0", st)]))
    return out[0] if len(out) == 1 else "|".join(out)
check("text resolver control: 0x87E is 'Save complete.'", text(0x87E) == "Save complete.", text(0x87E))

# --- 1. producers of sub-command 0x1D ---
hits = []
for fn in sorted(funcs):
    o = off(fn)
    if o is None: continue
    try: ins = dis(fn)
    except Exception: continue
    for i, x in enumerate(ins):
        if x.mnemonic == "mov" and x.op_str in ("edx, 0x1d", "rdx, 0x1d"):
            for y in ins[i + 1:i + 9]:
                if y.mnemonic in ("call", "jmp") and y.op_str.startswith("0x"):
                    hits.append((fn, x.address, int(y.op_str, 16))); break
post = [(fn, a) for fn, a, t in hits if t == 0x247510]
check("0x1D scan positive control 00581D4D found", any(a == 0x581D4D for _, a in post))
check("0x1D posts through 00247510 in the save/load region are exactly 0057EA0D, 0057EC1F, 0057F48E, 00581D4D",
      sorted(a for fn, a in post if 0x57E000 <= fn < 0x584000) == [0x57EA0D, 0x57EC1F, 0x57F48E, 0x581D4D],
      ",".join(f"{a:08X}" for _, a in post))
cls = {0x57EBFE: (3, "mov dword ptr [rsp + 0x20], 3"), 0x57E983: (0xD, "mov dword ptr [rsp + 0x80], 0xd")}
for a, (v, s) in cls.items():
    x = at(a)[0]
    check(f"class {v:#x} stored at {a:08X}", f"{x.mnemonic} {x.op_str}" == s, f"{x.mnemonic} {x.op_str}")
x = at(0x57EBB0)[0]; check("0057EBB0 acts only for queue kind 3 (cmp ecx,3)", x.op_str == "ecx, 3" and x.mnemonic == "cmp")
check("0057EC60 registers callback 0057EBB0 then queues kind 3",
      [f"{y.mnemonic} {y.op_str}" for y in at(0x57ECE3)] == ["lea rdx, [rip - 0x13a]"] and
      f"{at(0x57ED24)[0].mnemonic} {at(0x57ED24)[0].op_str}" == "mov dword ptr [rsp + 0x20], 3")
check("0057EA40 registers callback 0057E950 then queues kind 4",
      f"{at(0x57EB0F)[0].mnemonic} {at(0x57EB0F)[0].op_str}" == "mov dword ptr [rsp + 0x20], 4")
check("0057E950 queues kind 5 on kind-4 success in save mode",
      f"{at(0x57E9C2)[0].mnemonic} {at(0x57E9C2)[0].op_str}" == "mov dword ptr [rsp + 0x20], 5")
# regression against "the value IS the storage result": each handler reads the status at payload +8
check("00580A80 reads the status at payload+8", f"{at(0x580A92)[0].op_str}" == "dword ptr [rdx + 8], 0")
check("00580B40 reads the status at payload+8", f"{at(0x580B5C)[0].op_str}" == "edx, dword ptr [rdx + 8]")
check("00580CD0 reads the status at payload+8", f"{at(0x580D12)[0].op_str}" == "dword ptr [rsi + 8], edi")
# retail: kinds 3/4 are immediate commands that zero the status qword 02B40E14..1B
for fn, cmd in ((0x3BB2C0, 5), (0x3BB3B0, 4)):
    ins = dis(fn)
    s = [f"{y.mnemonic} {y.op_str}" for y in ins]
    check(f"{fn:08X} arms command {cmd} and zeroes the qword at 02B40E14 (status 02B40E18) and 02B40E10",
          any(f"], {cmd}" in t for t in s) and sum(1 for y in ins if y.mnemonic == "mov" and "qword ptr [rip" in y.op_str and y.address + y.size + int(y.op_str.split("0x")[1].split("]")[0], 16) == 0x2B40E14) == 1)

# --- 2. state table and popup ids ---
tbl = [BASE + u32(BASE + 0x461268 + 4 * i) for i in range(15)]
exp = [0x580F15, 0x580F27, 0x580F41, 0x580F56, 0x580F95, 0x58103D, 0x580F6B, 0x580F80, 0x581052, 0x581141, 0x581149, 0x58115E, 0x5811FF, 0x581218, 0x581218]
check("00580EB0 state table image+0x461268 = 15 published arms", tbl == exp, " ".join(f"{a:08X}" for a in tbl))
popup_of = {2: 0x15, 3: 0x13, 4: 0x10, 5: 0x16, 6: 0x19, 7: 0x1A, 8: 0x11, 9: 0x17, 10: 0x12, 11: 0x0F, 12: 0x18}
sm = dis(0x580EB0)
for st, pid in popup_of.items():
    a = tbl[st]
    seg = [x for x in sm if x.address >= a][:10]
    got = [x for x in seg if x.mnemonic == "mov" and x.op_str.startswith("dil, ")]
    check(f"state {st} arm {a:08X} selects popup {pid:#x}", bool(got) and int(got[0].op_str.split(", ")[1], 16) == pid)
check("states 0xD/0xE show the caller's popup (dil = r8d at 00580ED8)", f"{at(0x580ED8)[0].op_str}" == "edi, r8d")
# --- 3. popup table text ---
POP = {}
for i in range(31):
    tid, kind, flags, se = struct.unpack_from("<IBBB", d, off(0xD23DA0 + 8 * i))
    POP[i] = text(tid)
    print(f"      popup {i:#04x} text {tid:#x} kind {kind} flags {flags:#04x} se {se:#x} :: {POP[i]}")
for i, s in ((0, "No memory card"), (1, "Insufficient disk space"), (3, "Failed to read memory card"), (4, "Failed to format"),
             (5, "Save failed"), (6, "Load failed"), (0x10, "Saving"), (0x11, "Loading"), (0x13, "already exists"),
             (0x15, "Create new save data"), (0x16, "Save complete"), (0x17, "Load complete"), (0x12, "is not formatted"),
             (0x19, "trial mode progress"), (0x1A, "Trial Version")):
    check(f"popup {i:#x} text contains '{s}'", s in POP[i], POP[i][:60])
# --- 4. handler branch constants ---
t2 = [BASE + u32(BASE + 0x460B0C + 4 * k) for k in range(13)]
close = [k + 2 for k, a in enumerate(t2) if a == 0x580AC5]
check("00580A80 closes the popup in states 2,3,5,6,7,0xA,0xC,0xE", close == [2, 3, 5, 6, 7, 10, 12, 14], str(close))
check("00580A80 enters state 0xD with popup 0", [f"{x.mnemonic} {x.op_str}" for x in at(0x580AF2, 3)] == ["xor r8d, r8d", "mov dl, 0xd", "mov rcx, rbx"])
b40 = {0x580B72: "r8d, 3", 0x580B86: "r8d, r8d", 0x580B9A: "r8d, 1", 0x580BB1: "r9b, 0xa", 0x580BDE: "r9b, 4", 0x580BFC: "r9b, 3", 0x580C10: "r9b, 2", 0x580CA2: "r9b, 6", 0x580CA7: "r9b, 8"}
for a, s in b40.items(): check(f"00580B40 constant at {a:08X} = {s}", at(a)[0].op_str == s, at(a)[0].op_str)
check("00580CD0 success -> state 5", [x.op_str for x in at(0x580E81, 2)] == ["r8d, r8d", "dl, 5"])
check("00580CD0 failure -> state 0xD with popup 5", [x.op_str for x in at(0x580E88, 2)] == ["r8d, 5", "dl, 0xd"])
# --- 5. call-site census into 00580EB0 and state 7 ---
sites = []
text_sec = [s for s in secs if s[3] == b".text"][0]
tva, tvs, tro, _ = text_sec
blob = d[tro:tro + tvs]
for m in re.finditer(rb"[\xE8\xE9]", blob):
    i = m.start()
    if i + 5 > len(blob): continue
    src = BASE + tva + i
    if src + 5 + struct.unpack_from("<i", blob, i + 1)[0] == 0x580EB0:
        x = at(src)
        if x and x[0].address == src and x[0].size == 5: sites.append(src)
jcc = []
for m in re.finditer(rb"\x0F[\x80-\x8F]", blob):
    i = m.start(); src = BASE + tva + i
    if i + 6 <= len(blob) and src + 6 + struct.unpack_from("<i", blob, i + 2)[0] == 0x580EB0: jcc.append(src)
check("23 E8/E9 sites reach 00580EB0", len(sites) == 23, str(len(sites)))
check("no conditional jump reaches 00580EB0", not jcc, str(jcc))
check("no absolute qword pointer to 00580EB0 in the file", struct.pack("<Q", 0x580EB0) not in d)
def owner(a): return max(f for f in funcs if f <= a)
states = set(); seven = []
for s in sites:
    f = owner(s); ins = [x for x in dis(f) if x.address < s][-15:]
    vals = []
    for x in ins:
        m = re.match(r"^(dl|r9b|sil), (0x[0-9a-f]+|\d+)$", x.op_str)
        if x.mnemonic == "mov" and m: vals.append(int(m.group(2), 0))
    states.update(vals)
    if 7 in vals: seven.append(s)
check("state scan control: it sees states 6 and 8 (loaded as r9b at 00580CA2 / 00580CA7)", {6, 8} <= states)
check("no call site loads state 7 (dl / r9b / sil)", not seven, str(seven))
print(f"      states loaded as immediates at the sites: {sorted(states)}")
print(f"FAILS {fails}")
sys.exit(1 if fails else 0)
