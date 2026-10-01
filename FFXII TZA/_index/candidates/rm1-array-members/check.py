"""RM-1 harvest: every member registration through 00632A10 (array), 00632A70 (fixed-size) and 00632BE0 (enum),
resolved to (class, name, offset, a6, a7, a8, member class) and classified against _types/fields.tsv."""
import collections, json, re, struct, sys, pathlib, pickle
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
DB = pathlib.Path(r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA")
W = DB.parent / "Tools" / "work"
M = DB / "22-Middleware-PhyreEngine" / "Reflection-And-Class-Metadata" / "members"
pe = pefile.PE(str(W / "exe" / "FFXII_TZA.exe"), fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase; D = pe.__data__
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
F = {}
for l in (W / "graph" / "functions.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    c = l.split("\t")
    if c[2].isdigit(): F[int(c[0], 16)] = int(c[2])
import bisect
_text = next(s for s in pe.sections if s.Name.startswith(b".text"))
_tv, _to, _tl = IB + _text.VirtualAddress, _text.PointerToRawData, _text.Misc_VirtualSize
_tb = D[_to:_to + _tl]; _keys = sorted(F)
calls = collections.defaultdict(list)
for _p in range(len(_tb) - 5):
    if _tb[_p] == 0xE8:
        _t = _tv + _p + 5 + struct.unpack_from("<i", _tb, _p + 1)[0]
        if _t in (0x632A10, 0x632A70, 0x632BE0):
            _k = bisect.bisect_right(_keys, _tv + _p) - 1
            if _k >= 0 and _tv + _p < _keys[_k] + F[_keys[_k]]:
                calls[_t].append((_keys[_k], _tv + _p, "call"))
def body(a):
    o = pe.get_offset_from_rva(a - IB); return list(md.disasm(D[o:o + F.get(a, 0x400)], a))
def rip(i):
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP: return i.address + i.size + op.mem.disp
def cstr(va):
    try:
        o = pe.get_offset_from_rva(va - IB); return D[o:o + 96].split(b"\0")[0].decode("latin-1")
    except Exception: return None
fam = {}
for l in (M / "rtti-class-vtables.tsv").read_text(encoding="utf-8").splitlines():
    c = l.split("\t")
    if len(c) >= 3 and "PClassDataMember" in c[0]:
        try: fam[int(c[2], 16)] = c[0]
        except ValueError: pass
desc2cls = {}
for l in (M / "phyre-class-parent-chain.tsv").read_text(encoding="utf-8").splitlines():
    c = l.split("\t")
    if len(c) > 2 and c[1].startswith("0x"):
        try: desc2cls[int(c[1], 16)] = c[0]
        except ValueError: pass
REG = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", "r8d": "r8",
       "r9d": "r9", "r10d": "r10", "r11d": "r11", "r12d": "r12", "r13d": "r13", "r14d": "r14", "r15d": "r15"}
def resolve(b, k, reg):
    names = {reg, REG.get(reg, reg)}
    for j in b[:k][::-1]:
        ops = [x.strip() for x in j.op_str.split(",")]
        if not ops or ops[0] not in names: continue
        if j.mnemonic == "xor" and len(ops) == 2 and ops[1] in names: return 0
        if j.mnemonic == "mov" and len(ops) == 2:
            try: return int(ops[1], 0)
            except ValueError: return None
        return None
    return None
out = []
for ctor in (0x632A10, 0x632A70, 0x632BE0):
    for caller, site, m in calls.get(ctor, []):
        if m != "call": continue
        b = body(caller); idx = {i.address: n for n, i in enumerate(b)}
        if site not in idx: out.append({"ctor": "%08X" % ctor, "site": "%08X" % site, "caller": "%08X" % caller, "err": "site not decoded"}); continue
        k = idx[site]; a = {"ctor": "%08X" % ctor, "site": "%08X" % site, "caller": "%08X" % caller}
        for j in b[max(0, k - 20):k][::-1]:
            s = j.op_str
            if j.mnemonic == "lea" and s.startswith("r9,") and "name" not in a: a["name"] = cstr(rip(j))
            if j.mnemonic == "lea" and s.startswith("rdx,") and "desc" not in a:
                t = rip(j); a["desc"] = "%08X" % t if t else None; a["cls"] = desc2cls.get(t)
            for off, key in ((0x20, "offset"), (0x28, "a6"), (0x30, "a7"), (0x38, "a8")):
                if s.startswith("dword ptr [rsp + 0x%x]," % off) and key not in a:
                    src = s.split(",")[1].strip()
                    try: a[key] = int(src, 0)
                    except ValueError: a[key] = resolve(b, b.index(j), src)
        for j in b[k + 1:k + 8]:
            if j.mnemonic == "lea":
                t = rip(j)
                if t in fam: a["member_class"] = fam[t]; break
        out.append(a)
# classify against the store
FR = collections.defaultdict(list)
for l in (DB / "_types" / "fields.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    c = l.split("\t")
    if len(c) < 4: continue
    try: FR[c[0]].append((int(c[1], 16), int(c[2]) if c[2].isdigit() else 0, c[3]))
    except ValueError: pass
TYPES = {l.split("\t")[0] for l in (DB / "_types" / "types.tsv").read_text(encoding="utf-8").splitlines()[1:]}
cnt = collections.Counter()
for a in out:
    cls, off = a.get("cls"), a.get("offset")
    if not cls: a["where"] = "class unresolved"
    elif cls not in TYPES: a["where"] = "class not in store"
    elif not isinstance(off, int): a["where"] = "offset unresolved"
    else:
        rows = [r for r in FR[cls] if r[0] <= off < r[0] + max(r[1], 1)]
        if not rows: a["where"] = "no row covers offset"
        elif rows[0][2].startswith("unobserved"): a["where"] = "inside declared gap"
        elif rows[0][0] == off: a["where"] = "lands on named row"
        else: a["where"] = "inside named row"
        a["row"] = rows[0][2] if rows else None
    cnt[(a["ctor"], a["where"])] += 1
json.dump(out, open(pathlib.Path(__file__).with_name("harvest.json"), "w"), indent=1)
# CHECK: the census the carve consumed, and the store now carrying every carved member
EXPECT = {("00632A10", "class unresolved"): 69, ("00632A10", "lands on named row"): 96,
          ("00632A70", "class unresolved"): 10, ("00632A70", "lands on named row"): 19,
          ("00632BE0", "class unresolved"): 14, ("00632BE0", "lands on named row"): 7}
assert dict(cnt) == EXPECT, dict(cnt)
assert len(out) == 215
names = collections.Counter(a.get("name") for a in out if a.get("where") == "class unresolved" and a["ctor"] == "00632A10")
assert names == {"m_els": 60, "m_u": 9}, names
store = {(c, o): n for c, rows in FR.items() for o, s, n in rows if s == 16}
for a in out:
    if a["ctor"] == "00632A10" and a.get("cls") and a.get("a7") in (3, 4) and isinstance(a.get("offset"), int):
        assert (a["cls"], a["offset"]) in store or a["where"] == "lands on named row", (a["cls"], a["offset"])
assert any(n == "m_els" for (c, o), n in [(("PArray", 8), r[2]) for r in FR["PArray"] if r[0] == 8])
print("PASS")
for k, v in sorted(cnt.items()): print(k, v)
print("total", len(out))
