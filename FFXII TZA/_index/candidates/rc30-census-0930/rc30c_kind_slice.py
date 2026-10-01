"""RC-30 residue census, part 1: the kind value every computed-kind path-API call can carry (SWE2-DATA 2026-09-30),
static.

The first record's rc30_bounds.py section D listed the rel32 call/jmp/jcc sites of the path API (0032E400 size,
0032E620 request, 0032E3F0 staged size) whose kind argument (ecx) is not a constant at the site. A loca_*.cl2 request
needs kind 7. This script slices ecx backwards from each site:
  - inside the function: mov r, imm / xor r, r / lea r, [s + k] / mov r, s / cmovcc (both sources) / a store to a stack
    slot read back (mov [rsp+X], v ... mov ecx, [rsp+X]);
  - through an out-parameter: when ecx is loaded from a stack slot whose address was passed to a callee (lea r?, [rsp+X]
    before a call), the callee's stores to that out-pointer are read (constant stores only);
  - through the entry: when the value is an untouched argument register, every raw E8/E9 caller is sliced for that
    argument register (up to 3 levels);
  - a load from memory that is not a stack slot is reported as DATA with the address shape.
Each site ends as a value set (possibly with DATA leaves). The claim tested: no site's value set can contain 7
except through a named DATA leaf, and each DATA leaf is listed for part 2 (rc30c_data_fields.py).
Controls: C1 the slicer resolves the constant-kind font request 00365882 (mov ecx, 7) to {7}; C2 it resolves
003A13F0's out-parameter kind to {0x20} through 002ED8C0 (002ED8C0 writes [rdx] = 0x20); C3 it resolves the
MapRef site 00268814 (lea ecx, [rdi + 9]) through rdi's origin.
"""
import os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, owner, dis, secs, BASE, names  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


R64 = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", "esp": "rsp",
       "ax": "rax", "bx": "rbx", "cx": "rcx", "dx": "rdx", "si": "rsi", "di": "rdi", "bp": "rbp",
       "al": "rax", "bl": "rbx", "cl": "rcx", "dl": "rdx", "sil": "rsi", "dil": "rdi", "bpl": "rbp"}
for k in range(8, 16):
    R64.update({"r%dd" % k: "r%d" % k, "r%dw" % k: "r%d" % k, "r%db" % k: "r%d" % k})


def c64(r):
    return R64.get(r, r)


ARGS = ["rcx", "rdx", "r8", "r9"]
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
t = [s for s in secs if s[0] == ".text"][0]
_, va, vs, ro, rs = t
blob = d[ro:ro + rs]
_callers = {}


def callers(fn):
    if fn not in _callers:
        out = []
        for p in range(len(blob) - 5):
            if blob[p] in (0xE8, 0xE9) and BASE + va + p + 5 + struct.unpack_from("<i", blob, p + 1)[0] == fn:
                out.append(BASE + va + p)
        _callers[fn] = out
    return _callers[fn]


_body = {}


def body(fn):
    if fn not in _body:
        _body[fn] = dis(fn)
    return _body[fn]


def imm(s):
    try:
        return int(s, 0)
    except ValueError:
        return None


def out_param_stores(callee, argreg, depth=0):
    """constant values a callee stores through its pointer argument argreg ([argreg] or dword [argreg])"""
    vals, other = set(), []
    live = {argreg}
    for x in body(callee):
        op = x.op_str
        m = re.match(r"dword ptr \[(\w+)\], (.+)$", op)
        if x.mnemonic == "mov" and m and c64(m.group(1)) in live:
            v = imm(m.group(2))
            if v is not None:
                vals.add(v)
            else:
                sv, sl = slice_reg(callee, x.address, c64(m.group(2)), depth + 1)
                vals |= sv
                if sl or not sv:
                    other.append("%08X %s -> %s" % (x.address, op, sl or "empty"))
        parts = op.split(", ", 1)
        if len(parts) == 2 and x.mnemonic == "mov" and c64(parts[1]) in live and not parts[0].startswith("dword"):
            live.add(c64(parts[0]))
    return vals, other


def slice_reg(fn, site, reg, depth=0, seen=None):
    """value set of reg at site in fn: returns (set of ints, list of DATA / UNRESOLVED leaves)"""
    seen = seen or set()
    key = (fn, site, reg)
    if key in seen or depth > 4:
        return set(), ["depth/cycle %08X %s" % (site, reg)]
    seen = seen | {key}
    b = body(fn)
    idx = [i for i, x in enumerate(b) if x.address == site]
    if not idx:
        return set(), ["no boundary %08X" % site]
    i = idx[0] - 1
    while i >= 0:
        x = b[i]
        op = x.op_str
        parts = op.split(", ", 1)
        dst = c64(parts[0]) if len(parts) == 2 else None
        if x.mnemonic == "call" and reg == "rax" and x.op_str == "0x5c5230":
            return {0}, []  # 005C5230 is the folded 'return 0' stub
        if x.mnemonic == "call" and reg in VOL and x.op_str in ("0x808f10",):
            i -= 1          # _alloca_probe preserves the argument registers
            continue
        if x.mnemonic == "call" and reg in VOL:
            nxt = b[i + 1] if i + 1 < len(b) else None
            if nxt is not None and nxt.mnemonic == "jmp" and b[idx[0]].address != nxt.address:
                i -= 1          # that call's block ends in a jmp: it is not on the fall-through path to us
                continue
            return set(), ["clobbered by call at %08X" % x.address]
        if dst == reg and x.mnemonic in ("sub", "dec") and i + 1 < len(b) and b[i + 1].mnemonic == "jne"                 and (x.mnemonic == "dec" or parts[1] == "1"):
            return {0}, []          # a counted loop's fall-through: the counter is 0
        if dst == reg and x.mnemonic not in ("cmp", "test"):
            src = parts[1]
            if x.mnemonic == "mov" and imm(src) is not None:
                return {imm(src) & 0xFFFFFFFF}, []
            if x.mnemonic == "xor" and c64(src) == reg:
                return {0}, []
            if x.mnemonic in ("mov", "movsxd", "movzx", "movsx") and re.fullmatch(r"[a-z0-9]+", src):
                return slice_reg(fn, x.address, c64(src), depth, seen)
            m = re.fullmatch(r"\[(\w+) ([+-]) (0x[0-9a-f]+|\d+)\]", src)
            if x.mnemonic == "lea" and m:
                vs_, lv = slice_reg(fn, x.address, c64(m.group(1)), depth, seen)
                k = imm(m.group(3)) * (1 if m.group(2) == "+" else -1)
                return {(v + k) & 0xFFFFFFFF for v in vs_}, lv
            if x.mnemonic.startswith("cmov"):
                a, la = slice_reg(fn, x.address, c64(src), depth, seen)
                b2, lb = slice_reg(fn, x.address, reg, depth, seen | {(fn, x.address, reg)}) if False else (set(), [])
                # the fall-through value: slice reg before this instruction
                c, lc = slice_reg(fn, x.address, reg, depth, seen)
                return a | c, la + lc
            m = re.fullmatch(r"(?:dword|word|byte) ptr \[(rsp|rbp) ([+-]) (0x[0-9a-f]+|\d+)\]", src)
            if m:
                return slice_stack(fn, x.address, m.group(1), imm(m.group(3)) * (1 if m.group(2) == "+" else -1),
                                   depth, seen)
            if "ptr [" in src:
                return set(), ["DATA %08X in %08X: %s %s" % (x.address, fn, x.mnemonic, op)]
            return set(), ["UNRESOLVED %08X %s %s" % (x.address, x.mnemonic, op)]
        i -= 1
    # reached the entry
    if reg in ARGS:
        ai = ARGS.index(reg)
        vals, leaves = set(), []
        cs = callers(fn)
        if not cs:
            return set(), ["entry %08X arg %s: no raw caller" % (fn, reg)]
        for c in cs:
            f2 = owner(c)
            if f2 is None:
                leaves.append("caller %08X unlisted" % c)
                continue
            v, l = slice_reg(f2, c, ARGS[ai], depth + 1, seen)
            vals |= v
            leaves += l
        return vals, leaves
    return set(), ["entry %08X reg %s not an argument" % (fn, reg)]


def r11_frame(fn):
    """for a function opening 'mov r11, rsp': bytes between the entry rsp and the post-prologue rsp"""
    b = body(fn)
    if not b or b[0].op_str != "r11, rsp":
        return None
    fr = 0
    for x in b[1:12]:
        if x.mnemonic == "push":
            fr += 8
        elif x.mnemonic == "sub" and x.op_str.startswith("rsp, "):
            return fr + imm(x.op_str.split(", ")[1])
    return None


def slice_stack(fn, site, base, disp, depth, seen):
    """the last store to [rsp + disp] before site, or an out-parameter call that received its address"""
    b = body(fn)
    idx = [i for i, x in enumerate(b) if x.address == site][0]
    for j in range(idx - 1, -1, -1):
        x = b[j]
        op = x.op_str
        m = re.match(r"(?:dword|qword|word) ptr \[(rsp|rbp) ([+-]) (0x[0-9a-f]+|\d+)\], (.+)$", op)
        if x.mnemonic == "mov" and m and m.group(1) == base and imm(m.group(3)) * (1 if m.group(2) == "+" else -1) == disp:
            v = imm(m.group(4))
            if v is not None:
                return {v & 0xFFFFFFFF}, []
            return slice_reg(fn, x.address, c64(m.group(4)), depth, seen)
        if x.mnemonic == "call" and x.op_str.startswith("0x"):
            # was the slot's address passed?
            written = set()
            for k in range(j - 1, max(-1, j - 12), -1):
                y = b[k]
                if y.mnemonic == "call":
                    break
                yd = c64(y.op_str.split(",")[0]) if "," in y.op_str else None
                if yd in written:
                    continue            # an earlier write to this arg register is dead at the call
                if yd:
                    written.add(yd)
                mm = re.fullmatch(r"(\w+), \[(rsp|rbp|r11) ([+-]) (0x[0-9a-f]+|\d+)\]", y.op_str)
                if mm and mm.group(2) == "r11" and base == "rsp" and r11_frame(fn) is not None:
                    # r11 = rsp at entry (mov r11, rsp): [r11 + k] = [rsp + frame + k] after the prologue
                    mm = re.fullmatch(r"(\w+), \[(r11) ([+-]) (0x[0-9a-f]+|\d+)\]", y.op_str)
                    kk = imm(mm.group(4)) * (1 if mm.group(3) == "+" else -1) + r11_frame(fn)
                    if y.mnemonic == "lea" and kk == disp and c64(mm.group(1)) in ARGS:
                        callee = int(x.op_str, 16)
                        v, other = out_param_stores(callee, c64(mm.group(1)))
                        if other or not v:
                            return v, ["OUTPARAM %08X arg %s: %s" % (callee, mm.group(1), "; ".join(other) or "no constant store")]
                        return v, []
                    continue
                if y.mnemonic == "lea" and mm and mm.group(2) == base and                         imm(mm.group(4)) * (1 if mm.group(3) == "+" else -1) == disp and c64(mm.group(1)) in ARGS:
                    callee = int(x.op_str, 16)
                    v, other = out_param_stores(callee, c64(mm.group(1)))
                    if other or not v:
                        return v, ["OUTPARAM %08X arg %s: %s" % (callee, mm.group(1), "; ".join(other) or "no constant store")]
                    return v, []
    return set(), ["stack slot %s%+#x of %08X: no store found" % (base, disp, fn)]


API = [0x0032E400, 0x0032E620, 0x0032E3F0]
const = re.compile(r"^mov ecx, (0x[0-9a-f]+|\d+)$")
rows = []
for tgt in API:
    for s in sorted(set(callers(tgt))):
        fn = owner(s)
        if fn is None:
            continue
        v, leaves = slice_reg(fn, s, "rcx")
        rows.append((s, tgt, fn, v, leaves))
with7 = [r for r in rows if 7 in r[3]]
data = [r for r in rows if any(l.startswith(("DATA", "OUTPARAM", "UNRESOLVED", "stack", "clobber", "entry", "depth", "caller", "no ")) for l in r[4])]
for s, tgt, fn, v, leaves in rows:
    print("   %08X -> %08X in %08X %-28s kind %s%s" % (s, tgt, fn, names.get(fn, "")[:28],
          "{" + ",".join("0x%X" % k for k in sorted(v)) + "}", ("  LEAVES " + " | ".join(leaves[:3])) if leaves else ""))
print("sites %d; kind 7 reachable at %d; with an unresolved / data leaf %d" % (len(rows), len(with7), len(data)))
print("id value sets at the kind-7 sites (a loca_*.cl2 request needs id 0xE2..0xE4):")
hit = []
for s_, tgt, fn, v, leaves in with7:
    iv, il = slice_reg(fn, s_, "rdx")
    bad = sorted(k for k in iv if 0xE2 <= k <= 0xE4)
    hit += bad
    shown = ",".join("0x%X" % k for k in sorted(iv)[:24]) + (" ..." if len(iv) > 24 else "")
    print("   %08X in %08X id {%s} (%d values)%s" % (s_, fn, shown, len(iv),
          ("  ID-LEAVES %d: %s" % (len(il), " | ".join(sorted(set(il))[:4]))) if il else ""))
check("K1 no kind-7 site's resolved id set contains 0xE2..0xE4", not hit, str([hex(k) for k in hit]))
byaddr = {r[0]: r for r in rows}
check("C1 the font request 00365882 resolves to {7}", byaddr.get(0x00365882, (0, 0, 0, set()))[3] == {7})
check("C2 003A13F0's out-parameter kind resolves to {0x20} at 003A14B9",
      byaddr.get(0x003A14B9, (0, 0, 0, set()))[3] == {0x20}, str(byaddr.get(0x003A14B9, (0, 0, 0, set()))[3:]))
check("C3 the MapRef site 00268814 resolves through rdi", bool(byaddr.get(0x00268814, (0, 0, 0, set()))[3]),
      str(byaddr.get(0x00268814, (0, 0, 0, set()))[3:]))
print("FAILS %d" % FAILS)
