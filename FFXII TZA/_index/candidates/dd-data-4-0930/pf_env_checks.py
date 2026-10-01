"""Checks for the environment-variant page (SWE2-DATA 2026-09-30, DD owner read batch 4). Static: the shipping image
through ../rc22-34-resource-readers-0930/pe.py, the shipped map_ref.bin, and the database pages.

  E1 0026D910 ends in `jmp 002E3D40` at 0026DAAD with ecx/edx/r8d/r9d zeroed first (0026DA88..0026DA90)
  E2 the slot is the caller's ecx (0026D91F), replaced by 0017D490's value when that is positive (0026D921..0026D92F);
     0017D490 returns dword [001D50D0() + 0xAAC]
  E3 clamp: slot - 1, negative -> 0 (0026D933..0026D938), above 2 -> 2 (0026D93C..0026D943)
  E4 the body's rip-relative STORES hit exactly four globals {02099DA8, 02099DAC, 02099DB0, 02099DBC}; its
     rip-relative LOADS hit {02099D88, 02099D90} (control: the loads are the map_ref root and its loaded guard)
  E5 0026D976 calls 00180620 with ecx = the committed payload byte +0x1060 (0026D96F)
  E6 the shipped map_ref.bin begins 'MRF' 02 and its header +4 (the field-row array) is 0x30
  E8 raw rip-relative census of 02099DA8..02099DBF (pe.raw_rip_refs, independent of the function list): the getters
     00263E10 / 00263E20 / 00264D50 load 02099DA8 / 02099DAC / 02099DBC, and 02099DB0's only reference is the store at
     0026DA5B (control: 02099DB4's five cmp readers are found by the same sweep)
  E7 count of database pages outside _index/ and _experiments/ that cite 0026D910 (informational; control: this
     page is among them)
"""
import glob, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import dis, raw_rip_refs  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def rip_t(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


b = dis(0x0026D910)
a = {x.address: x for x in b}
check("E1 tail jmp 002E3D40 at 0026DAAD, four argument registers zeroed first",
      a[0x0026DAAD].mnemonic == "jmp" and a[0x0026DAAD].op_str == "0x2e3d40"
      and [a[k].op_str for k in (0x0026DA88, 0x0026DA8B, 0x0026DA8E, 0x0026DA90)]
      == ["r9d, r9d", "r8d, r8d", "edx, edx", "ecx, ecx"])
g = {x.address: x for x in dis(0x0017D490)}
check("E2 slot = ecx unless 0017D490 > 0; 0017D490 = [001D50D0() + 0xAAC]",
      a[0x0026D91F].op_str == "edi, ecx" and a[0x0026D921].op_str == "0x17d490"
      and a[0x0026D928].mnemonic == "jle" and a[0x0026D92F].op_str == "edi, eax"
      and g[0x0017D494].op_str == "0x1d50d0" and g[0x0017D499].op_str == "eax, dword ptr [rax + 0xaac]")
check("E3 clamp slot-1 into 0..2",
      a[0x0026D933].op_str == "edi, 1" and a[0x0026D936].mnemonic == "jns" and a[0x0026D938].op_str == "edi, ebx"
      and a[0x0026D93C].op_str == "eax, 2" and a[0x0026D943].op_str == "edi, eax")
stores, loads = set(), set()
for x in b:
    t = rip_t(x)
    if t is None:
        continue
    if x.mnemonic == "mov" and x.op_str.startswith("dword ptr [rip"):
        stores.add(t)
    elif "ptr [rip" in x.op_str:
        loads.add(t)
print("   stores %s; loads %s" % (" ".join("%08X" % t for t in sorted(stores)), " ".join("%08X" % t for t in sorted(loads))))
check("E4 rip stores = the four published globals", stores == {0x02099DA8, 0x02099DAC, 0x02099DB0, 0x02099DBC})
check("E4 control: rip loads = map_ref root 02099D88 and its guard 02099D90", loads == {0x02099D88, 0x02099D90})
check("E5 0026D976 calls 00180620 with ecx = payload byte +0x1060",
      a[0x0026D96F].op_str == "ecx, byte ptr [rax + 0x1060]" and a[0x0026D976].op_str == "0x180620")
mr = "D:/FFXII_TZA_extract/ps2data/image/ff12/in/common/map_ref.bin"
blob = open(mr, "rb").read()
check("E6 map_ref.bin: magic MRF 02, header +4 = 0x30", blob[:4] == b"MRF\x02" and struct.unpack_from("<i", blob, 4)[0] == 0x30,
      "%d bytes" % len(blob))
refs = raw_rip_refs(0x02099DA8, 0x02099DC0)
by = {}
for addr, mn, ops, t in refs:
    by.setdefault(t, []).append((addr, mn, ops))
ld = lambda t: sorted(a for a, mn, ops in by.get(t, []) if not ops.startswith("dword ptr [rip"))
check("E8 getters load 02099DA8 / 02099DAC / 02099DBC",
      0x00263E10 in ld(0x02099DA8) and 0x00263E20 in ld(0x02099DAC) and 0x00264D50 in ld(0x02099DBC),
      "DA8 readers %s" % ["%08X" % a for a in ld(0x02099DA8)])
check("E8 02099DB0's only reference is the store at 0026DA5B", [a for a, mn, ops in by.get(0x02099DB0, [])] == [0x0026DA5B])
check("E8 control: the sweep finds 02099DB4's cmp readers",
      sum(1 for a, mn, ops in by.get(0x02099DB4, []) if mn == "cmp") >= 5)
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
hits = []
for p in glob.glob(os.path.join(DB, "**", "*.md"), recursive=True):
    rel = os.path.relpath(p, DB).replace("\\", "/")
    if rel.startswith(("_index/", "_experiments/")):
        continue
    if "0026D910" in open(p, encoding="utf-8", errors="replace").read():
        hits.append(rel)
print("   pages citing 0026D910 outside _index/ and _experiments/: %d" % len(hits))
check("E7 control: the environment-variant page is among them",
      "03-World-Area-Field/choosing-the-field-environment-variant.md" in hits)
print("RESULT 0026D910 is the weather-slot apply: slot = requested (or the debug override), clamped to 0..2; it "
      "publishes four globals and the environment bank, then tail-calls the presentation refresh")
print("FAILS %d" % FAILS)
