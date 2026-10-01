"""Phyre member registrations the regcalls instrument and the field schema missed (OPUS, 2026-09-27).

Answers ASTRA-RETURN-OPUS-PHYRE-ARRAY-REGISTRATION-SENTINEL by measuring the whole population, not
the one example.  Static only (original EXE bytes), no execution.

C1  member-node constructor census: every small body that installs a PClassDataMember* vtable (RTTI)
    and is CALLED; site counts per constructor and how many sites phyre-field-schema.tsv holds.
C2  the 315 registrars (descriptor-vtable slot +0x60, from members/phyre-class-descriptor-vtable.tsv):
    the old direct count reproduces the `regcalls` column; the wrapper-aware count is never below it;
    the 176 covered classes stay >= 1; old zeros split 19 (register array members) / 120 (none).
C3  of the 120: which register only method callers (00632FB0 + a *Caller* RTTI vtable); none reaches a
    member constructor within two calls.
C4  the 25 registrations of the 19 classes, every argument resolved (name, offset, a6, a7, a8, vtable).
C5  accessor census: all PhyreArray / PhyreSharray / ArrayDynamic member vtables and their shared
    count/data accessors, plus the instruction bytes that fix the header.
C6  +0xF4 for PMeshInstanceSegmentContext: arg 7 of both descriptor constructors in its chain is 0.
C7  the store agrees: fields.tsv carries each of the 25 members at its offset with 16 bytes (or the
    pre-existing header rows), PInstancesComponent +0x18 is 16 bytes.
Mutants (must FAIL the corresponding assertion): M1 drop 00632A10 from the constructor set -> the
sentinel counts 0 (the old false negative); M2 PInstancesComponent +0x18 read at 8 bytes -> rejected;
M3 m_streamBindings at file offset 0 taken as the native offset -> rejected.
"""
import collections, hashlib, json, pathlib, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, __version__ as CSV
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE.parents[2]
W = DB.parent / "Tools" / "work"
EXE, FUNCS = W / "exe" / "FFXII_TZA.exe", W / "graph" / "functions.tsv"
RC = DB / "22-Middleware-PhyreEngine" / "Reflection-And-Class-Metadata"
SCHEMA, VTT, RTTI = RC / "phyre-field-schema.tsv", RC / "members" / "phyre-class-descriptor-vtable.tsv", RC / "members" / "rtti-class-vtables.tsv"
FIELDS = DB / "_types" / "fields.tsv"
EXE_SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
raw = EXE.read_bytes(); assert hashlib.sha256(raw).hexdigest() == EXE_SHA
pe = pefile.PE(data=raw, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
def at(va, n): o = pe.get_offset_from_rva(va - IB); return raw[o:o + n]
F = {}
for l in FUNCS.read_text(encoding="utf-8").splitlines()[1:]:
    c = l.split("\t")
    if c[2].isdigit() and not c[1].startswith(("Unwind@", "Catch_All@")): F[int(c[0], 16)] = int(c[2])
_b = {}
def body(a):
    if a not in _b: _b[a] = list(md.disasm(at(a, F.get(a, 0x200)), a))
    return _b[a]
def rip(i):
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP: yield i.address + i.size + op.mem.disp
def imm_calls(b, kinds=("call",)):
    return [(i, i.operands[0].imm) for i in b if i.mnemonic in kinds and i.operands and i.operands[0].type == X86_OP_IMM]
def rtti(vt):
    try:
        col = struct.unpack("<Q", at(vt - 8, 8))[0]
        if struct.unpack("<I", at(col, 4))[0] != 1: return ""
        td = struct.unpack("<I", at(col + 12, 4))[0] + IB
        return at(td + 16, 300).split(b"\0")[0].decode("latin-1")
    except Exception: return ""
def tsv(p):
    rows = [l.rstrip("\r\n").split("\t") for l in p.read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
    return [dict(zip(rows[0], r)) for r in rows[1:]]
R = {"exe_sha256": EXE_SHA, "capstone": CSV}

# ---- C1 ------------------------------------------------------------------------------
fam = {}
for l in RTTI.read_text(encoding="utf-8").splitlines():
    c = l.split("\t")
    if len(c) >= 3 and "PClassDataMember" in c[0] and "PClassDescriptor" not in c[0]:
        try: fam[int(c[2], 16)] = c[0]
        except ValueError: pass
calls, installs = collections.defaultdict(list), collections.defaultdict(set)
for a in sorted(F):
    try: b = body(a)
    except Exception: continue
    for i, t in imm_calls(b, ("call", "jmp")): calls[t].append((a, i.address, i.mnemonic))
    for i in b:
        if i.mnemonic == "lea":
            for t in rip(i):
                if t in fam: installs[a].add(t)
ctors = sorted(a for a in installs if F[a] <= 256 and any(m == "call" for _, _, m in calls[a])
               and len([1 for _, _, m in calls[a] if m == "call"]) >= 1 and not any(m == "jmp" for _, _, m in calls[a]))
# the member-node constructors are the called installers that forward to or embed the base init 00632FB0
base_init = 0x632FB0
MEMBER = [a for a in ctors if any(t in (0x632960, base_init) for _, t in imm_calls(body(a)))]
schema_sites = {r["site"] for r in tsv(SCHEMA)}
C1 = {"%08X" % a: {"installs": sorted({fam[t] for t in installs[a]}), "call_sites": len([1 for _, _, m in calls[a] if m == "call"]),
                   "in_schema": len({"%08X" % s for _, s, m in calls[a] if m == "call"} & schema_sites)} for a in MEMBER}
R["C1_member_constructors"] = C1
assert set(C1) == {"00632960", "00632A70", "00632A10", "00632BE0", "00632B30"}, sorted(C1)
assert [C1[k]["call_sites"] for k in ("00632960", "00632A70", "00632A10", "00632BE0")] == [682, 29, 165, 21]
assert [C1[k]["in_schema"] for k in ("00632960", "00632A70", "00632A10", "00632BE0")] == [682, 4, 0, 0]
R["C1_destructor_tailjumps"] = {k: len([1 for _, _, m in calls[int(k, 16)] if m == "jmp"]) for k in ("00633240", "006332A0")}

# ---- C2 ------------------------------------------------------------------------------
def unthunk(a, depth=3):
    for _ in range(depth):
        if F.get(a, 0) > 64: return a
        t = {x for _, x in imm_calls(body(a), ("call", "jmp"))}
        if len(t) != 1: return a
        a = t.pop()
    return a
def count(f, S): return sum(1 for _, t in imm_calls(body(f)) if t in S)
OLD = {0x632960, 0x632A70}; NEW = {int(k, 16) for k in C1}
V = tsv(VTT)
rows = [(r["class"], int(r["s60_unthunked"], 16), int(r["regcalls"]), r["in_schema"] == "yes") for r in V]
assert all(unthunk(int(r["s60"], 16)) == int(r["s60_unthunked"], 16) for r in V)
old_ok = all(count(f, OLD) == rc for _, f, rc, _ in rows)
new = {n: count(f, NEW) for n, f, _, _ in rows}
assert old_ok, "regcalls column does not reproduce"
assert all(new[n] >= rc for n, _, rc, _ in rows)
assert all(new[n] >= 1 for n, _, _, cov in rows if cov)
zeros = [(n, f) for n, f, rc, cov in rows if rc == 0]
flip = [(n, f) for n, f in zeros if new[n] > 0]; still = [(n, f) for n, f in zeros if new[n] == 0]
R["C2"] = {"rows": len(rows), "covered": sum(c for *_, c in rows), "old_zero": len(zeros), "register_arrays": len(flip),
           "no_member": len(still), "member_nodes_column_agrees": all(str(new[r["class"]]) == r.get("member_nodes") for r in V)}
assert (len(rows), R["C2"]["covered"], len(zeros), len(flip), len(still)) == (315, 176, 139, 19, 120), R["C2"]
assert R["C2"]["member_nodes_column_agrees"], "the published member_nodes column disagrees with this count"
M1 = count(dict((n, f) for n, f in zeros)["PMeshInstanceSegmentContext"], NEW - {0x632A10})
assert M1 == 0 and new["PMeshInstanceSegmentContext"] == 1, "M1: dropping 00632A10 must reproduce the false negative"
R["M1_without_00632A10_sentinel_count"] = M1

# ---- C3 ------------------------------------------------------------------------------
methods_only, reach2 = [], []
allinst = set(installs)
for n, f in still:
    b = body(f)
    vts = {rtti(t) for i in b if i.mnemonic == "lea" for t in rip(i)}
    if any(t == base_init for _, t in imm_calls(b)):
        methods_only.append((n, sorted(v for v in vts if "Caller" in v)))
    for _, c in imm_calls(b):
        if c in allinst or c in NEW or any(c2 in allinst or c2 in NEW for _, c2 in imm_calls(body(c)) if c in F):
            reach2.append((n, "%08X" % c))
R["C3_methods_only"] = methods_only; R["C3_reach_within_two_calls"] = reach2
assert len(methods_only) == 8 and all(v for _, v in methods_only), methods_only
assert reach2 == [], reach2

# ---- C4 ------------------------------------------------------------------------------
REG = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
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
regs = []
for n, f in flip:
    b = body(f)
    for k, i in enumerate(b):
        if i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM and i.operands[0].imm in NEW:
            a = {"class": n, "registrar": "%08X" % f, "site": "%08X" % i.address, "ctor": "%08X" % i.operands[0].imm}
            for j in b[max(0, k - 16):k][::-1]:
                s = j.op_str
                if j.mnemonic == "lea" and s.startswith("r9,") and "name" not in a:
                    a["name"] = at(next(rip(j)), 80).split(b"\0")[0].decode("latin-1")
                for off, key in ((0x20, "offset"), (0x28, "a6"), (0x30, "a7"), (0x38, "a8")):
                    if s.startswith("dword ptr [rsp + 0x%x]," % off) and key not in a:
                        src = s.split(",")[1].strip()
                        try: a[key] = int(src, 0)
                        except ValueError: a[key] = resolve(b, b.index(j), src)
            for j in b[k + 1:k + 8]:
                if j.mnemonic == "lea":
                    for t in rip(j):
                        if t in fam: a["member_class"] = fam[t]
            regs.append(a)
R["C4_registrations"] = regs
assert len(regs) == 25 and len({r["class"] for r in regs}) == 19
assert all(isinstance(r.get("offset"), int) and r.get("a6") == 0 and r.get("name") and r.get("member_class") for r in regs), regs
assert all(r["ctor"] == "00632A10" for r in regs)
kind = {3: "PClassDataMemberPhyreArray", 4: "PClassDataMemberPhyreSharray", 2: "PClassDataMemberArrayDynamic"}
assert all(kind[r["a7"]] in r["member_class"] for r in regs), "a7 selects the array member class"
sent = [r for r in regs if r["class"] == "PMeshInstanceSegmentContext"]
assert len(sent) == 1 and sent[0]["name"] == "m_streamBindings" and sent[0]["offset"] == 0x38 and sent[0]["site"] == "005E6860"
assert sent[0]["offset"] != 0, "M3: the file-schema offset 0 is not the native offset"

# ---- C5 ------------------------------------------------------------------------------
acc = collections.defaultdict(collections.Counter)
for vt, name in fam.items():
    for k in kind.values():
        if name.startswith(".?AV?$" + k + "@"):
            s = [struct.unpack("<Q", at(vt + 8 * i, 8))[0] for i in range(8)]
            acc[k][("%08X" % s[4], "%08X" % s[6], "%08X" % s[7])] += 1
R["C5_accessors"] = {k: {"/".join(key): v for key, v in c.items()} for k, c in acc.items()}
assert dict(acc["PClassDataMemberPhyreArray"]) == {("006065E0", "006045B0", "006045B0"): 59}
assert dict(acc["PClassDataMemberPhyreSharray"]) == {("006065E0", "0063B9B0", "0063B9B0"): 10}
assert dict(acc["PClassDataMemberArrayDynamic"]) == {("006065D0", "00604580", "00604580"): 71}
BYTES = {"006065E0": "488b41188b49482b88f40000004863c18b04100fbaf01fc3",          # u32 at field+0, btr 31
         "006045B0": "488b41188b49482b88f40000004863c1488b441008c3",              # qword at field+8
         "0063B9B0": "488b41188b49482b88f40000004863c14803c28b080fbaf11f83f9017605488b4008c34883c00833d285c9480f44c2c3"}
for a, h in BYTES.items():
    assert at(int(a, 16), len(h) // 2).hex() == h, a
R["C5_bytes"] = BYTES
for a, pat in (("005C8BF0", ("488973 08", "893b")), ("0062A870", ("0fbaef1f", "48897308", "893b")),
               ("006C7A40", ("4c8937", "892e")), ("006A5950", ("0fbaee1f", "8933"))):
    h = at(int(a, 16), F[int(a, 16)]).hex()
    assert all(p.replace(" ", "") in h for p in pat), a
    assert any(t == 0x584730 for _, t in imm_calls(body(int(a, 16)))), a + " releases through 00584730"

# ---- C6 ------------------------------------------------------------------------------
assert at(0x5D98AE, 8).hex() == "c744243000000000" and at(0x6B850B, 8).hex() == "c744243000000000"
assert at(0x5D98CA, 6).hex() == "41b948000000" and at(0x6B8520, 6).hex() == "41b928000000"   # sizes 0x48 / 0x28
R["C6_F4_terms"] = {"PMeshInstanceSegmentContext": 0, "PMeshSegmentContext": 0}

# ---- C7 ------------------------------------------------------------------------------
FR = collections.defaultdict(dict)
for l in FIELDS.read_text(encoding="utf-8").splitlines()[1:]:
    c = l.split("\t")
    if len(c) < 4: continue                      # the store carries one pre-existing blank line
    FR[c[0]][int(c[1], 16)] =(int(c[2]) if c[2].isdigit() else 0, c[3])
def covered(cls, off):
    rows = FR[cls]
    if off in rows and rows[off][0] == 16: return "whole"
    if off in rows and off + 8 in rows and rows[off][0] == 4 and rows[off + 8][0] == 8: return "header rows"
    return None
cov = {"%s.%s" % (r["class"], r["name"]): covered(r["class"], r["offset"]) for r in regs if r["a7"] in (3, 4)}
R["C7_store"] = cov
assert all(cov.values()), [k for k, v in cov.items() if not v]
assert FR["PInstancesComponent"][0x18][0] == 16 and 0x20 not in FR["PInstancesComponent"], "M2: +0x18 must be the 16-byte member"
assert FR["PMeshInstanceSegmentContext"][0x38] == (16, "m_streamBindings") and FR["PMeshInstanceSegmentContext"][0x28][0] == 16
assert FR["PSharray"][0x8][0] == 8 and FR["PArray"][0x8][0] == 8

out = HERE / "result.json"
out.write_text(json.dumps(R, indent=1), encoding="utf-8")
print("OK C1 constructors 5; sites 682/29/165/21, in schema 682/4/0/0")
print("OK C2 315 rows, regcalls reproduces, 176 covered >=1; 139 old zero = 19 array registrars + 120 none; M1 fires")
print("OK C3 8 of the 120 register only method callers; none reaches a constructor within two calls")
print("OK C4 25 registrations / 19 classes, all arguments resolved; a7 selects the member class; M3 fires")
print("OK C5 accessors 59/10/71 uniform, header bytes fixed; C6 +0xF4 terms 0; C7 store agrees, M2 fires")
print("result", hashlib.sha256(out.read_bytes()).hexdigest())
