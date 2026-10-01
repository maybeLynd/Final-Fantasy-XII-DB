"""class2_census.py - SD-124 residue / party page 2b: which slot-map classes reach BattleSlotMap_ResolveMappedBattleSlot
0031B9F0 through the wrapper 00320040, which takes the CLASS in ecx and the index in edx (it swaps them: 0032004F
mov edx, ecx; 00320051 mov ecx, ebx) - unlike the resolver's own (index=ecx, class=edx) order. Lists every raw call
site of 00320040 with the constant loaded into ecx before it. Control: 0035BDB9 mov ecx, 2 / 0035BDBE call is found."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "takebacks"))
import tk
IDX = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "pub140-scratch", "tools", "rawcalls.json")))
def sites(t): return sorted(int(s, 16) for k, v in IDX.items() if k.upper().lstrip("0X").lstrip("0") == ("%X" % t) for s in v)
w = {x.address: x for x in tk.fdis(0x00320040)}
swap = w[0x0032004F].op_str == "edx, ecx" and w[0x00320051].op_str == "ecx, ebx" and w[0x00320053].op_str == "0x31b9f0"
print("00320040 forwards ecx as the class (0032004F/00320051 -> 0031B9F0):", "yes" if swap else "NO")
rows = []
for s in sites(0x00320040):
    o, _ = tk.owner(s)
    pre = [x for x in tk.fdis(o) if x.address < s][-8:]
    cls = [x.op_str.split(",", 1)[1].strip() for x in pre if x.mnemonic == "mov" and x.op_str.startswith("ecx,")]
    rows.append((s, o, cls[-1] if cls else "?"))
    print("  %08X in %-44s class(ecx)=%s" % (s, tk.fname(o)[:44], cls[-1] if cls else "?"))
ctl = any(s == 0x0035BDBE and c == "2" for s, o, c in rows)
print("CONTROL 0035BDBE passes class 2:", "PASS" if ctl else "FAIL")
print("FAILS %d" % (0 if (ctl and swap) else 1))
