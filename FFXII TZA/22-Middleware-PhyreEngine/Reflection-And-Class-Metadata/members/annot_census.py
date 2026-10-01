"""annot_census.py: every annotation the image attaches (calls to PAnnotatable add 006B67D0), with
- the annotation object (rdx), its key (the rdx passed to the annotation ctor 006B66C0 for that object) and key name
  (the string the key object was built with through 006B66F0),
- the immediate stored at annotation +0x30 (the PAnnotationWithValue<unsigned> value), if any,
- the member (rcx - 0x38) and its name (r9 at the 00632960 call that built it)."""
import struct, re
from collections import Counter
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(nsec)]
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    if d[o:o + 8].rstrip(b"\0") == b".text": vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
def cstr(v):
    for s_vs, s_va, s_rs, s_ro in secs:
        if BASE + s_va <= v < BASE + s_va + s_rs:
            o = v - BASE - s_va + s_ro; return d[o:o + 64].split(b"\0")[0].decode(errors="replace")
    return "?"
md = Cs(CS_ARCH_X86, CS_MODE_64)
def rip(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m: return None
    v = int(m.group(2), 16); return x.address + x.size + (v if m.group(1) == "+" else -v)
allins = []
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.split("\t")
    try: fs, sz = int(p[0], 16), int(p[2])
    except (ValueError, IndexError): continue
    if sz <= 0 or sz > 0x20000: continue
    off = fs - BASE - va + ro
    if off < ro or off + sz > ro + rs: continue
    allins.append((fs, list(md.disasm(d[off:off + sz], fs))))
def argsrc(ins, k, reg):
    for z in reversed(ins[max(0, k - 14):k]):
        if z.op_str.startswith(reg + ", "):
            return rip(z) if z.mnemonic == "lea" else None
    return None
keyname = {}; annkey = {}; annval = {}; membname = {}
for fs, ins in allins:
    for k, x in enumerate(ins):
        if x.mnemonic not in ("call", "jmp") or not x.op_str.startswith("0x"): continue
        t = int(x.op_str, 16)
        if t == 0x6B66F0:
            obj, nm = argsrc(ins, k, "rcx"), argsrc(ins, k, "rdx")
            if obj and nm: keyname[obj] = cstr(nm)
        elif t == 0x6B66C0:
            obj, key = argsrc(ins, k, "rcx"), argsrc(ins, k, "rdx")
            if obj:
                annkey[obj] = key
                for y in ins[k + 1:k + 8]:
                    if y.mnemonic == "mov" and rip(y) == obj + 0x30 and re.search(r", (0x[0-9a-f]+|\d+)$", y.op_str):
                        annval[obj] = y.op_str.split(", ")[1]; break
        elif t == 0x632960:
            obj, nm = argsrc(ins, k, "rcx"), argsrc(ins, k, "r9")
            if obj and nm: membname[obj] = cstr(nm)
rows = []
for fs, ins in allins:
    for k, x in enumerate(ins):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x") and int(x.op_str, 16) == 0x6B67D0:
            tgt, ann = argsrc(ins, k, "rcx"), argsrc(ins, k, "rdx")
            m = tgt - 0x38 if tgt else None
            key = annkey.get(ann)
            rows.append((keyname.get(key, "?"), annval.get(ann, "-"), membname.get(m, "?"), "%08X" % x.address))
print("attaches:", len(rows))
for (kn, v), n in Counter((r[0], r[1]) for r in rows).most_common():
    print("  key %-14s value %-12s x%d" % (kn, v, n))
print("members:", Counter(r[2] for r in rows).most_common(12))
