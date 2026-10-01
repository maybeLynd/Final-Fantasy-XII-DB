"""RM-1 follow-up: the element types of the twelve reflected PArray members the harvest left as PArray<?> (OPUS, 2026-09-27).

Why the harvest missed them: it looked for the member object's vtable in a `lea` AFTER the registration call. At these
sites the vtable is loaded into a register BEFORE the call and stored into the member object's +0 after it, and one
register serves several members. Two independent witnesses per site, both read from the shipping image:
  E1 the member object's vtable, found by following the store into [member+0] back to its `lea`: its RTTI names
     PClassDataMemberPhyreArray<T>
  E2 the value-type argument r8, the return of the site's own getter: its vtable's RTTI names PClassDescriptor...<PArray<T, N>>
  E3 at every site E1's T equals E2's T, and E2's N equals the harvest's a8 (so a8 is the array's second template argument)
Prints the ctype each row should carry. Not claimed: what the elements are FOR (meaning axis).
"""
import json, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, size=None): return list(cs.disasm(d[off(a):off(a) + (size or sizes.get(a, 0x80))], a))
def rip(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) if m else None
def rtti(vt):
    o = off(vt - 8)
    if o is None: return None
    col = struct.unpack_from("<Q", d, o)[0]; oc = off(col)
    if oc is None: return None
    otd = off(BASE + struct.unpack_from("<I", d, oc + 12)[0])
    return d[otd + 16:otd + 240].split(b"\0")[0].decode("latin-1") if otd else None
PRIM = {"H": "int", "E": "unsigned char", "M": "float", "I": "unsigned int"}
def demangle_t(s):
    if s.startswith("V"): return s[1:].split("@")[0]
    return PRIM.get(s[:1], "?")

H = json.load(open(HERE / "harvest.json"))
todo = [h for h in H if h.get("cls") and not h.get("member_class") and h.get("a8") and h.get("site")
        and h["cls"] in ("PEffectVariant", "PMesh", "PShape", "PScript", "PModifierNetwork")]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
res = []
for h in todo:
    f, site = int(h["caller"], 16), int(h["site"], 16)
    b = dis(f); i = next(k for k, x in enumerate(b) if x.address == site)
    member = next((rip(x) for x in b[i - 8:i][::-1] if x.mnemonic == "lea" and x.op_str.startswith("rcx,")), None)
    store = next((x for x in b[i + 1:i + 12] if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rip") and rip(x) == member), None)
    t1 = None
    if store:
        reg = store.op_str.split(", ")[1]; j = b.index(store)
        src = next((x for x in b[:j][::-1] if x.op_str.startswith(reg + ",")), None)
        if src is not None and src.mnemonic == "lea":
            m = re.match(r"\.\?AV\?\$PClassDataMemberPhyreArray@(.+)@Phyre@@$", rtti(rip(src)) or "")
            t1 = demangle_t(m.group(1)) if m else None
    r8 = next((x for x in b[i - 12:i][::-1] if x.op_str.startswith("r8,")), None)
    t2 = n2 = None
    if r8 is not None and r8.op_str == "r8, rax":
        g = next((x for x in b[b.index(r8) - 8:b.index(r8)][::-1] if x.mnemonic == "call"), None)
        vt = next((rip(x) for x in dis(int(g.op_str, 16)) if x.mnemonic == "lea" and x.op_str.startswith("rax,")), None) if g else None
        m = re.match(r"\.\?AV\?\$PClassDescriptor\w+@V\?\$PArray@(.+)\$0(\d)@Phyre@@@Phyre@@$", rtti(vt) or "") if vt else None
        if m: t2 = demangle_t(m.group(1)); n2 = int(m.group(2)) + 1
    res.append((h["cls"], h["name"], t1, t2, n2, h["a8"]))
check("E1 every site's member vtable names PClassDataMemberPhyreArray<T>", len(res) == 12 and all(r[2] and r[2] != "?" for r in res))
check("E2 every site's value-type getter names PClassDescriptor<PArray<T, N>>", all(r[3] and r[4] for r in res))
check("E3 the two witnesses agree on T at every site, and N equals the harvest's a8", all(r[2] == r[3] and r[4] == r[5] for r in res))
for r in res: print("   %s.%s -> PArray<%s>  (N=%s, a8=%s)" % (r[0], r[1], r[2], r[4], r[5]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
