"""sd21_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for SD-21 (2026-09-30).
(1) the factory 007AEA20's selector is its 10th argument: frame arithmetic from the prologue, and the pool addresses
    each path resolves; (2) what each of the three callers stores as the 10th argument ([rsp + 0x48] at the call);
(3) the start/queue caller list against an independent census: every indirect `call qword ptr [reg + 0x18|0x48]`
    in the image whose reg was loaded, earlier in the same function, from [x + 0x68] or [x + 0x48] - then who among
    those also appear in the author's list, and which extra ones exist (the pattern's blind side)."""
import sys, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
F = 0x007AEA20
ins = tk.fdis(F)
frame = 0
for x in ins[:8]:
    if x.mnemonic == "push": frame += 8
    if x.mnemonic == "sub" and x.op_str.startswith("rsp,"): frame += int(x.op_str.split(",")[1], 0)
sel = next(x for x in ins if x.mnemonic == "cmp" and "rsp +" in x.op_str)
disp = int(re.search(r"rsp \+ (0x[0-9a-f]+)", sel.op_str).group(1), 16)
entry_off = disp - frame            # offset from rsp at entry (return address at +0)
print("prologue frame %#x; selector `%s` at %08X -> entry+%#x = argument %d" % (frame, sel.op_str, sel.address, entry_off, (entry_off - 8) // 8 + 1))
for x in ins:
    if x.mnemonic == "lea" and "rip" in x.op_str:
        print("  %08X lea -> %08X" % (x.address, x.address + x.size + x.operands[1].mem.disp))
    if x.mnemonic == "call": print("  %08X call %s" % (x.address, x.op_str))
for f, site in ((0x007B9050, 0x007B91E7), (0x007DCE20, 0x007DCF92), (0x007EBAD0, 0x007ED332)):
    last = None
    for x in tk.dis(f, site):
        if x.mnemonic in ("mov", "movzx") and x.op_str.startswith("byte ptr [rsp + 0x48],"):
            last = x
    print("caller %08X 10th arg store: %s" % (f, "%08X %s %s" % (last.address, last.mnemonic, last.op_str) if last else None))
# (3) independent pattern census, whole listed-function set
authors = {"start": {0x007B9050, 0x007B9AF0, 0x007DCE20, 0x007EDA60, 0x007EDAB0}, "queue": {0x007B9590, 0x007DCE20, 0x007EAA60}}
found = {"start": set(), "queue": set()}
for e, sz in tk.flist:
    if not (0x007A0000 <= e < 0x00800000): continue     # the SQEX Sd driver region
    try: body = tk.fdis(e)
    except Exception: continue
    loaded = {}
    for x in body:
        m = re.match(r"(r\w+), qword ptr \[(r\w+) \+ (0x68|0x48)\]$", x.op_str) if x.mnemonic == "mov" else None
        if m: loaded[m.group(1)] = x.address; continue
        m = re.match(r"(r\w+), qword ptr \[(r\w+)\]$", x.op_str) if x.mnemonic == "mov" else None
        if m and m.group(2) in loaded: loaded["vt:" + m.group(1)] = x.address; continue
        m = re.match(r"qword ptr \[(r\w+) \+ (0x18|0x48)\]$", x.op_str) if x.mnemonic == "call" else None
        if m and ("vt:" + m.group(1)) in loaded:
            found["start" if m.group(2) == "0x18" else "queue"].add(e)
            continue
        # linear kill: any other write to a 64-bit register drops what it held (first pass counted a reused rcx)
        w = re.match(r"(r\w+),", x.op_str)
        if w and x.mnemonic in ("mov", "lea", "xor", "movzx", "add", "sub", "pop"):
            loaded.pop(w.group(1), None); loaded.pop("vt:" + w.group(1), None)
for k in ("start", "queue"):
    print("%s: census %s | author-only %s | census-only %s" % (k, sorted("%08X" % a for a in found[k]),
          sorted("%08X" % a for a in authors[k] - found[k]), sorted("%08X" % a for a in found[k] - authors[k])))
# vtable slots read directly (not through retool)
for vt, n in ((0x01CB8290, "CoreMasterVoice"), (0x01CB82D0, "CoreSubmixVoice"), (0x01CB8360, "CoreSourceVoice")):
    print("%s %08X slots: %s" % (n, vt, " ".join("%d:%08X" % (i, tk.u64(vt + 8 * i)) for i in range(18))))
