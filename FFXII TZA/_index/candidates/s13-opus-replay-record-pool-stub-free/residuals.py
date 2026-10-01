"""S-13 (OPUS, 2026-09-26): the record-pool closer's three named residuals - kinds 3/4/6 (the region map's layout-class-2 arm),
w[desc] >= 0xA (boundary site 1) and a caller-supplied allocator.

check.py is re-run unchanged in two variants (environment only; its default run and result.json are untouched):
  V0  the published run, recorded again with the gate counter (S13_RESULT=v_default.json);
  V1  a descriptor with one record in each of the 8 groups, kinds 0..7 (S13_GROUPS=1,1,1,1,1,1,1,1; the link on record 5, a kind-5
      record, so the two link callees still run);
  V2  the published descriptor with w[desc] = 0xA (S13_FCOUNT=0xA).
Group -> layout class is the image's own table 01E0C328 (byte 0): 0,1,1,2,2,3,3,3. The published run's groups 0/1/2/5/7 never reach
class 2, the arm groups 3 and 4 take.
And one static read, the caller-supplied allocator: ActorManager_BindLoadedDefinitionPayload 0026C8C0 installs the default
00267930 (0026C8E3) unless r8 is non-zero (0026C8EA / 0026C8FA cmovne r12, r8). Its only caller, ActorResource_OnDefinitionPayloadLoaded
0032F850, passes r8 = lea [rip - 0xC8031] at 0032F95A, which is 00267930 itself.
Cases:
 R1  V1: all 11 of check.py's cases pass over eight records, every layout class 0-3 is carved, and the class-2 records (groups 3, 4)
     get +0xA0 and +0xB8 inside the record and +0xC0 = 0.
 R2  V2: all 11 pass, and the instruction past the >= 0xA gate (002668EC) runs once per constructor call; V0 never reaches it.
 R3  the only caller of 0026C8C0 supplies 00267930, the allocator check.py runs.
Evidence classes NATIVE-REPLAY (R1, R2) and STATIC (R3), live_game false. Writes residuals_result.json.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"))
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"


def variant(name, **env):
    e = dict(os.environ)
    e.update({"S13_RESULT": name, **env})
    p = subprocess.run([sys.executable, os.path.join(HERE, "check.py")], cwd=HERE, env=e, capture_output=True, text=True)
    return p.returncode, json.load(open(os.path.join(HERE, name)))


rc0, v0 = variant("v_default.json")
rc1, v1 = variant("v_all_groups.json", S13_GROUPS="1,1,1,1,1,1,1,1", S13_LINKED="5")
rc2, v2 = variant("v_fcount_A.json", S13_FCOUNT="0xA")
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
pe = struct.unpack_from("<I", raw, 0x3C)[0]
opt = pe + 24
base = struct.unpack_from("<Q", raw, opt + 24)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
o = opt + struct.unpack_from("<H", raw, pe + 20)[0]
secs = []
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, o + 8)
    secs.append((base + va, vs, ra))
    o += 40


def at(va, n):
    for v, vs, ra in secs:
        if v <= va < v + vs:
            return raw[ra + va - v:ra + va - v + n]


md = Cs(CS_ARCH_X86, CS_MODE_64)
bind = [(i.address, i.mnemonic, i.op_str) for i in md.disasm(at(0x26C8E3, 0x1B), 0x26C8E3)]
caller = [(i.address, i.mnemonic, i.op_str) for i in md.disasm(at(0x32F95A, 0x11), 0x32F95A)]
lea = caller[0]
passed = lea[0] + 7 - int(lea[2].split("- ")[1].rstrip("]"), 16) if lea[1] == "lea" and "rip -" in lea[2] else None
edges = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "graph", "edges.tsv"))
callers = sorted({l.split("\t")[0] for l in open(edges) if l.split("\t")[1:2] == ["0026C8C0"]})
R = {
    "V0": {"rc": rc0, "ok": v0["ok"], "site1_hits": v0["variant"]["site1_hits"]},
    "V1": {"rc": rc1, "ok": v1["ok"], "variant": v1["variant"], "pointers": v1["detail"]["POOL_interior_pointers_rel_record"]},
    "V2": {"rc": rc2, "ok": v2["ok"], "variant": v2["variant"]},
    "R3": {"bind_sites": ["%08X %s %s" % x for x in bind], "caller_site": ["%08X %s %s" % x for x in caller], "callers_of_0026C8C0": callers,
           "r8_passed": "%08X" % passed if passed else None},
}
cls = v1["variant"]["layout_class_by_record"]
cases = {
    "R1_all_groups_every_layout_class_carved_class2_pointers_inside": rc1 == 0 and v1["ok"] and sorted(set(cls)) == [0, 1, 2, 3]
        and all(v1["detail"]["POOL_interior_pointers_rel_record"][str(i)]["C0"] == "0" and v1["detail"]["POOL_interior_pointers_rel_record"][str(i)]["ok"]
                for i, c in enumerate(cls) if c == 2),
    "R2_fcount_0xA_takes_site1_on_every_ctor_call_default_never": rc2 == 0 and v2["ok"] and v2["variant"]["site1_hits"] == v2["alloc"]["ctor_calls"] + 1
        and v0["variant"]["site1_hits"] == 0,
    "R3_the_only_caller_supplies_the_default_allocator": callers == ["0032F850"] and passed == 0x267930
        and any(x[1] == "cmovne" and x[2] == "r12, r8" for x in bind),
}
res = {"results": R, "cases": cases, "ok": all(cases.values()), "live_game": False}
json.dump(res, open(os.path.join(HERE, "residuals_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-66s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps({"layout_classes": cls, "site1": [v0["variant"]["site1_hits"], v2["variant"]["site1_hits"]], "R3": R["R3"]}))
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
