"""rc20_verbs.py - RC-20: which script verbs the four Movement-filed bodies that call VMValueStack_PushFloat32Bits
(00267F60) serve. ORACLE, 2026-09-30. Static, shipping image (img.py from ../rc8-cascade-count-0930).

Method
 1. Callers of 00267F60: every raw E8/E9 rel32 hit in .text, kept only when the hit decodes as that call/jmp inside its
    .pdata chain-root function. Joined to the ledger (Tools/work/graph/functions.tsv) owner column; the Movement-filed
    set must be exactly four bodies of 88-233 B (the pass-22 crossing's own statement: positive control C1). The
    ledger's edges.tsv caller count for 00267F60 must be reproduced (C2).
 2. Entry routes into each body: direct callers / tail-jumps (raw rel32, decoded), and 5-byte jmp thunks that are
    themselves reached; plus every qword in the image equal to the body or to a thunk of it.
 3. The family tables, derived from VMNativeCommandDispatch_InitializeFamilyTables (003DC2D0): default table for all 16
    families, then families 0/3/5/7 overridden. Control C3: family 0 -> 01EED700 (the dispatch page).
    Record N = table + 8 + 32*N: +0 begin, +8 poll, +0x10 unused, +0x18 result.
    Control C4: the dispatch table's result column for call id 0x0001 is setpos 0034EBC0 (scriptvm-dispatch.tsv).
 4. Verb names from the authored ff12-script catalog (CScriptContainerInitializers.cpp), keyed family<<12 | command.
"""
import io, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc8-cascade-count-0930"))
import img  # noqa: E402

DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))      # Database/
FN = os.path.join(DB, "Tools", "work", "graph", "functions.tsv")
ED = os.path.join(DB, "Tools", "work", "graph", "edges.tsv")
CAT = os.path.abspath(os.path.join(DB, "..", "Collaboration", "tools", "ffxii", "ff12-script-master", "ff12-script",
                                   "CScriptContainerInitializers.cpp"))
PUSHF = 0x00267F60
fails = 0


def check(ok, name):
    global fails
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    fails += not ok


# 1. callers of 00267F60, decoded
def decoded_sites(target):
    out = []
    for a, kind in img.calls_to(target):
        r = img.owner(a)
        if r is None:
            continue
        ins = [x for x in img.fn_ins(r) if x.address == a]
        if ins and ins[0].mnemonic in ("call", "jmp") and ins[0].op_str == hex(target):
            out.append((r, a, ins[0].mnemonic))
    return out


sites = decoded_sites(PUSHF)
callers = sorted(set(r for r, _a, _k in sites))
ledger = {}
for l in io.open(FN, encoding="utf-8").read().splitlines()[1:]:
    c = l.split("\t")
    ledger[int(c[0], 16)] = (c[1], int(c[2]) if c[2].isdigit() else -1, c[3])
edges_callers = sorted(set(int(l.split("\t")[0], 16) for l in io.open(ED, encoding="utf-8").read().splitlines()[1:]
                           if l.split("\t")[1] == "00267F60"))
print("decoded call/jmp sites to 00267F60: %d in %d functions; edges.tsv callers: %d" %
      (len(sites), len(callers), len(edges_callers)))
check(set(callers) == set(edges_callers), "C2 decoded caller set equals edges.tsv caller set (%d)" % len(edges_callers))
mov = [f for f in callers if ledger.get(f, ("", 0, ""))[2] == "Movement"]
print("Movement-filed callers: %s" % ", ".join("%08X (%d B)" % (f, ledger[f][1]) for f in mov))
check(len(mov) == 4 and min(ledger[f][1] for f in mov) == 88 and max(ledger[f][1] for f in mov) == 233,
      "C1 four Movement-filed bodies, 88-233 B (the pass-22 crossing)")

# 2. entry routes
qwords = {}
for name, start, size, raw, rawsz in img.SECS:
    if name in (".data", ".rdata"):
        b = img.blob[raw:raw + rawsz]
        for o in range(0, len(b) - 7, 8):
            v = struct.unpack("<Q", b[o:o + 8])[0]
            qwords.setdefault(v, []).append(start + o)

def pdata_less_thunks(target):
    """5-byte `jmp target` stubs with no .pdata entry of their own (the linker's incremental/ICF thunks sit between
    int3 pads and are invisible to owner()). A raw hit counts when it decodes as that jmp at its own address, starts
    16-aligned or right after an int3, and is followed by an int3."""
    out = []
    for a, kind in img.calls_to(target):
        if kind != "jmp" or img.owner(a) is not None:
            continue
        x = img.dis(a, 5)
        if x and x[0].mnemonic == "jmp" and x[0].op_str == hex(target) and x[0].size == 5 and \
                (a % 16 == 0 or img.rd(a - 1, 1) == b"\xcc") and img.rd(a + 5, 1) == b"\xcc":
            out.append(a)
    return out


routes = {}
for f in mov:
    names = {f: "body"}
    frontier = [f]
    while frontier:                         # thunks of the body, thunks of thunks, and every code site reaching any
        t = frontier.pop()
        for a in pdata_less_thunks(t):
            if a not in names:
                names[a] = "thunk (no .pdata) -> %08X" % t
                frontier.append(a)
        for r, a, k in decoded_sites(t):
            if k == "jmp" and r == a and sum(x.size for x in img.fn_ins(r)) == 5 and r not in names:
                names[r] = "thunk -> %08X" % t
                frontier.append(r)
            elif r not in names:
                names[r] = "%s from %08X into %08X" % (k, a, t)
    routes[f] = names
# control C5: amove's begin 0033F850 is a thunk of 00349680 (the verb table tsv names it thunk_FUN_00349680)
check(0x0033F850 in routes.get(0x00349680, {}), "C5 the pdata-less thunk 0033F850 -> 00349680 is found")

# 3. family tables
fam = {}
init = img.fn_ins(0x003DC2D0)
default = img.ripmem(init[1])
for k in range(16):
    fam[k] = default
last = None
for x in init:
    t = img.ripmem(x)
    if x.mnemonic == "lea" and t:
        last = t
    elif x.mnemonic == "mov" and t and 0x02B57EF0 <= t < 0x02B57EF0 + 128 and last:
        fam[(t - 0x02B57EF0) // 8] = last
check(fam[0] == 0x01EED700, "C3 family 0 table = 01EED700 (derived %08X)" % fam[0])
tables = sorted(set(fam.values()))
cat = {}
for m in re.finditer(r'\{\s*0x([0-9a-fA-F]+),\s*\{\s*L"([^"]*)"', io.open(CAT, encoding="utf-8", errors="replace").read()):
    cat[int(m.group(1), 16)] = m.group(2)
SLOT = {0: "begin", 8: "poll", 0x10: "unused", 0x18: "result"}
hits = []
for t in tables:
    n = struct.unpack("<i", img.rd(t, 4))[0]
    fams = [k for k in range(16) if fam[k] == t]
    for c in range(n):
        for off in SLOT:
            p = struct.unpack("<Q", img.rd(t + 8 + 32 * c + off, 8))[0]
            for f in mov:
                if p in routes[f]:
                    hits.append((f, p, t, fams, c, SLOT[off]))
r1 = struct.unpack("<Q", img.rd(0x01EED700 + 8 + 32 * 1 + 0x18, 8))[0]
check(r1 == 0x0034EBC0 and cat.get(1) == "setpos", "C4 call id 0x0001 result = %08X, catalog name %s" % (r1, cat.get(1)))

print("\nentry routes per body (name -> how reached):")
for f in mov:
    for a, how in sorted(routes[f].items()):
        q = [x for x in qwords.get(a, [])]
        print("  %08X  %08X %-22s qword refs in .data/.rdata: %s" % (f, a, how, " ".join("%08X" % x for x in q) or "-"))

print("\nverb table slots holding a body or its thunk:")
seen_q = set()
for f, p, t, fams, c, slot in sorted(hits):
    ids = [(k << 12) | c for k in fams]
    nm = sorted(set(cat.get(i, "?") for i in ids))
    seen_q.add(t + 8 + 32 * c + {"begin": 0, "poll": 8, "unused": 16, "result": 24}[slot])
    print("  body %08X via %08X  table %08X command 0x%03X slot %-6s ids %s  catalog %s" %
          (f, p, t, c, slot, ",".join("%04X" % i for i in ids[:3]) + ("..(%d families)" % len(ids) if len(ids) > 3 else ""),
           "/".join(nm)))
# every qword ref to a body/thunk must be one of the table slots found (no other data route)
other = [(f, a, q) for f in mov for a in routes[f] for q in qwords.get(a, []) if q not in seen_q]
print("\nqword references outside the verb-table slots: %d %s" % (len(other), other))
code_callers = [(f, a, how) for f in mov for a, how in routes[f].items() if not how.startswith(("body", "thunk"))]
print("code routes other than thunks: %d %s" % (len(code_callers), code_callers))

print("\nbodies (push site context):")
for f in mov:
    ins = img.fn_ins(f)
    for k, x in enumerate(ins):
        if x.mnemonic in ("call", "jmp") and x.op_str == hex(PUSHF):
            print("  --- %08X push at %08X" % (f, x.address))
            img.pr(ins[max(0, k - 6):k + 3])
print("\nFAILS %d" % fails)
sys.exit(1 if fails else 0)
