"""ab8_counter17.py - AB-8 correction (FABLE, 2026-09-30): which bodies feed achievement counter 17 (ACH_COUNT_SCORE)?

The 2026-09-18 census (steam-integration-and-achievement-catalogue.md, AB-8 row) enumerated the direct callers of the
counter updater AchievementCounter_UpdateAndMaybeFire 00316A50 and found ids 6, 7, 11 and 19, "never 17". It missed the
tail jumps through the 5-byte thunk 00253770 (`jmp 00316A50`). This lists every raw E8/E9 site that reaches 00316A50
directly or through that thunk, with the counter id (ecx) and amount (edx) the site sets just before it.
Controls: the census's three direct sites (GameState_SetGil 6/7, the defeat rewards 11, 0056D370 19) must be found as
direct sites; the thunk must be exactly `jmp 00316A50`."""
import sys, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
IDX = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
def sites(t):
    return sorted(int(s, 16) for k, v in IDX.items() if k.upper().lstrip("0X").lstrip("0") == ("%X" % t) for s in v)
thunk = list(tk.fdis(0x00253770))
thunk_ok = len(thunk) == 1 and thunk[0].mnemonic == "jmp" and int(thunk[0].op_str, 16) == 0x00316A50
print("thunk 00253770:", ["%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in thunk], "->", "OK" if thunk_ok else "UNEXPECTED")
rows = []
for route, tgt in (("direct", 0x00316A50), ("via thunk 00253770", 0x00253770)):
    for s in sites(tgt):
        o, _ = tk.owner(s)
        pre = [x for x in tk.fdis(o) if x.address < s][-8:]
        ecx = [x.op_str.split(",", 1)[1].strip() for x in pre if x.mnemonic == "mov" and x.op_str.startswith("ecx,")]
        edx = [x.op_str.split(",", 1)[1].strip() for x in pre if x.op_str.startswith("edx,") and x.mnemonic in ("mov", "add", "imul", "movzx")]
        rows.append((route, s, o, ecx[-1] if ecx else "?", edx[-1] if edx else "?"))
        print("  %-20s site %08X in %-44s id(ecx)=%-6s amount(edx)=%s" % (route, s, tk.fname(o)[:44], ecx[-1] if ecx else "?", edx[-1] if edx else "?"))
feeds17 = [r for r in rows if r[3] == "0x11"]
print("sites setting counter 17 (ecx = 0x11): %s" % ["%08X (%s) in %08X" % (r[1], r[0], r[2]) for r in feeds17])
direct = {r[2] for r in rows if r[0] == "direct"}
need = {0x00254EE0, 0x00312280, 0x0056D370}   # GameState_SetGil, the defeat rewards, 0056D370 - the census's direct feeders
ctl = thunk_ok and need <= {r[2] for r in rows if r[0] == "direct"}
print("CONTROL thunk is jmp 00316A50 and the census's three direct feeders (00254EE0, 00312280, 0056D370) are found:", "PASS" if ctl else "FAIL")
print("FAILS %d" % (0 if ctl and feeds17 else 1))
sys.exit(0 if ctl and feeds17 else 1)
