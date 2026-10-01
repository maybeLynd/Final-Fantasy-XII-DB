"""RC-30 residue census, part 2: the data fields behind the computed-kind leaves, the script verbs, and the
request route the earlier records missed (SWE2-DATA 2026-09-30), static.

Part 1 (rc30c_kind_slice.py) sliced the kind argument at every 0032E400 / 0032E620 / 0032E3F0 call site whose ecx is
not a constant. The leaves it could not bound read (kind, id) out of loaded structures. This script resolves them:

  S1  the structure-field census. For each structure a leaf reads its kind out of, every function holding a raw
      rip reference into the array's first slot (or the whole struct for 02B5E0E0) plus their direct callees is
      scanned, tracking registers derived from those references, and every write to the kind field's displacement
      is listed. Each structure has exactly one filler:
        02B581A0 0x1C-slots, kind word +0x10 (read by 003DDA70): written only at 003DD609 in 003DD4C0, from the
            out-parameters of 0032F170 (constants 1, 8, 5 only).
        02B59360 0x38-slots, kind word +0x2C (read by 003DF550): written only at 003DF4EA in 003DF440, same source.
        02B5D0B0 0x40-slots, kind words +0xC + 2n (read by 003E9EF0): written only at 003EA06B in 003E9F80, from
            the constants 8 / 0x25 at 003E9FED-003E9FFF.
        02B5E0E0 struct, kind dword +0x1C (read by 003EADE0): written only by the qword clear at 003EB088 (+0x18)
            and the constant store 003EB10C (0x24).
  S2  the two script verbs that take (kind, id) from the VM stack: debug_filesize (0x2006) and debug_fileread
      (0x2007). The BQ-10 decompile corpus of every shipped script (1,114 files) calls neither; the control verb
      setposparty is found.
  S3  the request route: 003C1F00 (the location-map pane loader) requests kind 7, id 0xE1 + byte [menumap_common
      entry + 1] through the pool core 00249210 and keeps the buffer at widget +0x118. Over every shipped
      menumap_common.bin (9 language copies, 'cmap' magic, 48 8-byte entries at u32[u16[+8]] + 4), the selector
      byte +1 is non-zero only in entries 40 (= 1 -> 0xE2 Loca_gil.cl2) and 46 (= 2 -> 0xE3 Loca_bhm.cl2).
      Loca_rbl.cl2 (0xE4) is never selected.

Claims: C1 each S1 census lists the expected filler; C2 the corpus read is live (setposparty found); S2 no shipped
script calls debug_filesize or debug_fileread; S3a the 003C1F00 pins decode; C3 menumap_common has 48 entries over
47 distinct persistence groups; S3b the shipped selectors request 0xE2 / 0xE3 and none selects 0xE4.
"""
import os, re, struct, sys, glob, collections, contextlib, io
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-as7-pages-0930"))
sys.path.insert(0, os.path.join(HERE, "..", "rc6-console-map-codes-0930"))
from pe import d, off, owner, dis, raw_rip_refs, funcs, names  # noqa
import arc  # noqa
with contextlib.redirect_stdout(io.StringIO()):
    import rc5_paths as R  # noqa

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
GPR = set(R64.values())
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}


def rip_target(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


def field_writes(fn, lo, hi, fields):
    """every store at a listed displacement of a register derived from a reference into [lo, hi), plus every
    rip-relative store into [lo, hi) at a listed displacement."""
    hits = []
    derived = set()
    for x in dis(fn):
        op = x.op_str
        dst = R64.get(op.split(", ")[0], op.split(", ")[0]) if ", " in op else None
        t = rip_target(x)
        if t is not None and lo <= t < hi:
            if x.mnemonic == "mov" and dst is not None and dst.startswith(("byte", "word", "dword", "qword")):
                if (t - lo) in fields:
                    hits.append(x)
                continue
            if dst in GPR:
                derived.add(dst)
                continue
        if dst in GPR and ", " in op:
            src = op.split(", ", 1)[1]
            if x.mnemonic == "mov" and src in derived:
                derived.add(dst)
                continue
            if x.mnemonic in ("lea", "add", "sub", "imul", "shl", "movsxd", "movsx", "movzx", "and") \
                    and any(re.search(r"\b%s\b" % r, src) for r in derived):
                derived.add(dst)
                continue
        mm = re.match(r"(byte|word|dword|qword) ptr \[(\w+)( \+ \w+\*\d+)? \+ (0x[0-9a-f]+|\d+)\], (.+)", op)
        if x.mnemonic == "mov" and mm and mm.group(2) in derived and int(mm.group(4), 0) in fields:
            hits.append(x)
            continue
        if x.mnemonic == "call":
            derived -= VOL
    return hits


def callees(fn):
    out = set()
    for x in dis(fn):
        if x.mnemonic == "call" and x.op_str.startswith("0x"):
            tgt = int(x.op_str, 16)
            out.add(tgt if tgt in funcs else (owner(tgt) or tgt))
    return {c for c in out if c in funcs}


# ---- S1: the four structure fields' writers ----
STRUCTS = [
    ("02B581A0 slots", 0x02B581A0, 0x02B581A0 + 0x1C, [0x10], 0x003DD609),
    ("02B59360 slots", 0x02B59360, 0x02B59360 + 0x38, [0x2C], 0x003DF4EA),
    ("02B5D0B0 slots", 0x02B5D0B0, 0x02B5D0B0 + 0x40, [0xC, 0xE], 0x003EA06B),
    ("02B5E0E0 struct", 0x02B5E0E0, 0x02B5E0E0 + 0x40, [0x1C, 0x18], 0x003EB10C),
]
for label, lo, hi, fields, expected in STRUCTS:
    refs = raw_rip_refs(lo, hi)
    fns = sorted({owner(a) for a, *_ in refs if owner(a)})
    allf = set(fns)
    for fn in fns:
        allf |= callees(fn)
    hits = []
    for fn in sorted(allf):
        hits += field_writes(fn, lo, hi, fields)
    hits = sorted({x.address: x for x in hits}.values(), key=lambda x: x.address)
    print("S1 %s: %d referencing functions, %d with callees; field writes at %s:"
          % (label, len(fns), len(allf), ["0x%x" % f for f in fields]))
    for x in hits:
        o = owner(x.address)
        print("   %08X in %08X %-28s %s %s" % (x.address, o or 0, names.get(o, ""), x.mnemonic, x.op_str))
    check("C1 %s census lists the expected filler %08X" % (label, expected),
          any(x.address == expected for x in hits))

# ---- S2: the two stack-kind script verbs over the decompiled corpus ----
CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
cnt = collections.Counter()
nfiles = 0
for f in glob.glob(os.path.join(CORPUS, "*.txt")):
    nfiles += 1
    for m in re.finditer(r"\b(debug_filesize|debug_fileread|setposparty)\s*\(",
                         open(f, encoding="utf-8", errors="replace").read()):
        cnt[m.group(1)] += 1
print("S2 decompiled scripts %d: debug_filesize %d, debug_fileread %d calls (control setposparty %d)"
      % (nfiles, cnt["debug_filesize"], cnt["debug_fileread"], cnt["setposparty"]))
check("C2 the corpus read is live (setposparty found)", cnt["setposparty"] > 0)
check("S2 no shipped script calls debug_filesize or debug_fileread",
      cnt["debug_filesize"] == 0 and cnt["debug_fileread"] == 0)

# ---- S3: 003C1F00 requests kind 7, id 0xE1 + byte [menumap_common entry + 1] ----
b = {x.address: x for x in dis(0x003C1F00)}
pins = (0x003C2043, 0x003C204A, 0x003C2058, 0x003C2068, 0x003C206F, 0x003C2071, 0x003C2076, 0x003C207A, 0x003C208D,
        0x003C2092, 0x003C209D)
for a in pins:
    print("   %08X %s %s" % (a, b[a].mnemonic, b[a].op_str))
check("S3a 003C1F00 requests kind 7, id 0xE1 + byte [menumap_common entry + 1] (non-zero) and keeps it at "
      "widget +0x118",
      b[0x003C2043].op_str == "rcx, qword ptr [rax + 0xe8]"
      and b[0x003C2068].op_str == "eax, byte ptr [r8 + 1]" and b[0x003C206F].mnemonic == "je"
      and b[0x003C2071].op_str == "edx, 7" and b[0x003C207A].op_str == "r8d, 0xe1"
      and b[0x003C208D].op_str == "0x249210" and b[0x003C209D].op_str == "qword ptr [rax + 0x118], rcx")

arr = R.regions[1][0][7]
kind7names = {i: (R.row(arr, i) or "-").split("\\")[-1] for i in (0xE2, 0xE3, 0xE4)}
selvals = set()
c3ok = None
for p in sorted(arc.find("menumap_common.bin")):
    lang = p.split("/")[4]
    dd = arc.get(p)
    o = struct.unpack_from("<H", dd, 8)[0]
    n = struct.unpack_from("<I", dd, o)[0]
    rows = []
    groups = set()
    for i in range(n):
        b1 = dd[o + 4 + 8 * i + 1]
        groups.add(struct.unpack_from("<I", dd, o + 8 + 8 * i)[0])
        if b1:
            selvals.add(b1)
            rows.append("entry %d = %d -> id 0x%X %s" % (i, b1, 0xE1 + b1, kind7names.get(0xE1 + b1, "?")))
    print("   %s  %s entries %d; byte +1 non-zero: %s" % (lang, dd[:4], n, ", ".join(rows)))
    this = (n, len(groups))
    c3ok = this if c3ok is None else c3ok
check("C3 menumap_common: 48 entries, 47 distinct persistence groups - %d / %d" % c3ok, c3ok == (48, 47))
ids = sorted(0xE1 + v for v in selvals)
print("S3 selector values that ship: %s -> ids %s" % (sorted(selvals), ["0x%x" % i for i in ids]))
check("S3b the shipped selectors request Loca_gil.cl2 (0xE2) and Loca_bhm.cl2 (0xE3); none selects 0xE4",
      ids == [0xE2, 0xE3])
print("FAILS", FAILS)
