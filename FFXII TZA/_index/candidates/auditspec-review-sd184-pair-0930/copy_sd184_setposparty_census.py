"""sd184_setposparty_census.py - SD-184: the facing argument every shipped script passes to setposparty (0x3B1) and
setposparty_mapjump (0x56D) (SWE2-ORACLE, 2026-09-30).

Script-corpus evidence (the shipped .ebp bytecode in FFXII_TZA.vbf). Nothing here is native execution.

Why these two verbs: 0x3B1 -> 003571A0 and 0x56D -> 0033F070 both pop four floats through 00267DB0 and call 0037D000
with the FIRST pop (the last pushed argument) as xmm1 = the facing. 0037D000 passes it raw to 00310920 (only when
r8d != 0, i.e. only from 0x3B1), which stores it into BattleUnit +0x160 (= st+0xE0) with no normalisation.

For every CALL/CALLPOPA (0x58/0x5D) and CALLACT/CALLACTPOPA (0x59/0x5E) of the two verbs, the four argument producers
are resolved with FABLE's backward stack walk (gen_req_channel_census.resolve_args, as sd162 does). The facing is the
last pushed argument (arg 3 of 4). Its producer is classified:
  PUSHF imm        -> the float constant pool: [sec + U32(sec,0x24) + 4 + 4*imm] (PUSHF 0x50 reader 0026187D)
  PUSHII imm       -> a signed 16-bit integer (00267DB0 converts an int slot with cvtdq2ps)
  PUSHI imm        -> the int constant pool: [sec + U32(sec,0x20) + 4 + 4*imm]
  anything else    -> dynamic
A PUSHV facing is then followed one step: every POPV (0x49) in the corpus that writes the same variable (class +
24-bit offset from the descriptor table at header +0x28; the file for class 1 file, the actor's directory entry for
class 2 local, the whole corpus for the shared classes 0 / 4 / 5) is resolved the same way, and every PUSHP (0x4B) reference to it is listed as a possible
write through a verb's out-pointer. getrotangzx (0x12E -> 00349150) returns 00265200(actor) and getangzx (0x12F ->
00349490) returns 00263CC0(actor); both read movement-state angles whose writers wrap (0026B6A0 / 002E5E10 for
+0x38 / +0xA8; 0026A0D0 and 002E45E0 via 003A1AD0 for +0xA4). A class-1 (file) variable with no POPV and no PUSHP in
its file keeps the value authored in the image's file-data area (header +0x38), which is read and bounded.
Output: this script's stdout (sd184_setposparty_census.out) and sd184-setposparty-sites.tsv.
"""
import collections, io, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))           # Database/FFXII TZA
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))               # repository root: the decoder's relative paths
import gen_req_channel_census as G  # noqa: E402

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
I32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
F32 = lambda b, o: struct.unpack_from("<f", b, o)[0]
FAILS = []
PI = 3.14159265
VERBS = {0x3B1: "setposparty", 0x56D: "setposparty_mapjump"}
CALLS = {0x58, 0x59, 0x5D, 0x5E}


def check(tag, ok, msg):
    print("CHECK %-4s %s  %s" % (tag, "PASS" if ok else "FAIL", msg))
    if not ok:
        FAILS.append(tag)


verbs = G.load_verbs()
check("V1", verbs.get(0x3B1, (None,))[0] == 4 and verbs.get(0x56D, (None,))[0] == 4,
      "verb table arity: setposparty %s, setposparty_mapjump %s (both must be 4)"
      % (verbs.get(0x3B1, (None,))[0], verbs.get(0x56D, (None,))[0]))


def value(sec, prod):
    """(class, numeric value or None) of one resolved producer."""
    name, imm, kind = prod
    if kind != "push":
        return (kind + ":" + name, None)
    if name == "PUSHF":
        fp = U32(sec, 0x24)
        return ("PUSHF", F32(sec, fp + 4 + 4 * imm)) if imm < U32(sec, fp) else ("PUSHF-out-of-pool", None)
    if name == "PUSHII":
        return ("PUSHII", float(imm - 0x10000 if imm & 0x8000 else imm))
    if name == "PUSHI":
        ip = U32(sec, 0x20)
        return ("PUSHI", float(I32(sec, ip + 4 + 4 * imm))) if imm < U32(sec, ip) else ("PUSHI-out-of-pool", None)
    if name.startswith("PUSHI") and name[-1].isdigit():
        return ("PUSHIn-register", None)
    if name.startswith("PUSHF") and name[-1].isdigit():
        return ("PUSHFn-register", None)
    return ("dynamic:" + name, None)


def desc(sec, imm):
    vt = U32(sec, 0x28)
    return U32(sec, vt + 4 + 8 * imm) if imm < U32(sec, vt) else None


def varkey(path, d, actor):
    """class 1 (file) is per image, class 2 (local) per actor (directory entry), the others shared."""
    cls = (d >> 24) & 7
    return (cls, d & 0xFFFFFF, path if cls == 1 else ("%s#%X" % (path, actor)) if cls == 2 else "*")


writers = collections.defaultdict(list)     # varkey -> [(path, off, class, value)]
pointer_refs = collections.defaultdict(list)
initval = {}                                 # class-1 facing variable -> its authored initial value
f = io.open(G.VBF, "rb")
names, blocks_idx = G.V.load_index(f)
rows = []
files = scripts = 0
ctrl_pushf = 0            # positive control: PUSHF producers of ANY verb's last argument decode to finite floats
ctrl_pushf_bad = 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks_idx, path)
    except Exception:
        continue
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18)
    cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
        continue
    files += 1
    starts = sorted(set(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt)))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start:
            continue
        scripts += 1
        ins, _ = G.decode(sec[start:end])
        for j, (pc, op, imm) in enumerate(ins):
            if op == 0x49:
                d = desc(sec, imm)
                if d is not None:
                    a, st = G.resolve_args(ins, j, 1, verbs)
                    w = (value(sec, a[0]) if st == "ok" else ("unresolved:" + st, None))
                    if (j >= 3 and ins[j - 1][1] in (0x12, 0x13) and ins[j - 3][1] == 0x48 and ins[j - 3][2] == imm
                            and ins[j - 2][1] == 0x48):     # PUSHV v; PUSHV r; OPADD/OPSUB; POPV v: v += r each pass
                        w = ("accumulator:v%s=v%sr" % (imm, "+" if ins[j - 1][1] == 0x12 else "-"), None)
                    writers[varkey(path, d, start)].append((path, start + pc) + w)
                continue
            if op == 0x4B:
                d = desc(sec, imm)
                if d is not None:
                    pointer_refs[varkey(path, d, start)].append((path, start + pc))
                continue
            if op not in CALLS:
                continue
            if imm not in VERBS:
                if op == 0x58 and ctrl_pushf < 20000 and j and ins[j - 1][1] == 0x50:
                    ctrl_pushf += 1
                    v = value(sec, ("PUSHF", ins[j - 1][2], "push"))[1]
                    ctrl_pushf_bad += v is None or v != v or abs(v) > 1e9
                continue
            act = op in (0x59, 0x5E)
            need = 4 + act
            args, st = G.resolve_args(ins, j, need, verbs)
            if st != "ok":
                rows.append((path, start + pc, VERBS[imm], "%02X" % op, "unresolved:" + st, None, "", None))
                continue
            fac = args[need - 1]                  # the last pushed argument = the first pop = the facing
            cls, v = value(sec, fac)
            if cls == "dynamic:PUSHV":
                d = desc(sec, fac[1])
                cls = "PUSHV:%d:%06X" % ((d >> 24) & 7, d & 0xFFFFFF) if d is not None else cls
                vk = varkey(path, d, start) if d is not None else None
                if vk is not None and vk[0] == 1:
                    initval[vk] = F32(sec, U32(sec, 0x38) + vk[1])
            else:
                vk = None
            xyz = [value(sec, a) for a in args[need - 4:need - 1]]
            rows.append((path, start + pc, VERBS[imm], "%02X" % op, cls, v,
                         ",".join("%s=%s" % (c, "%.3f" % x if x is not None else "?") for c, x in xyz), vk))

out = os.path.join(HERE, "sd184-setposparty-sites.tsv")
with io.open(out, "w", encoding="utf-8", newline="\n") as t:
    t.write("file\tsection_offset\tverb\topcode\tfacing_producer\tfacing_value\txyz_producers\n")
    for r in rows:
        t.write("%s\t0x%X\t%s\t%s\t%s\t%s\t%s\n" % (r[0], r[1], r[2], r[3], r[4], "" if r[5] is None else "%.6f" % r[5], r[6]))

print("corpus: %d script files (EBP2 magic 0x8000000B), %d scripts decoded" % (files, scripts))
by = collections.Counter((r[2], r[4]) for r in rows)
for k in sorted(by):
    print("  %-20s facing producer %-24s %5d sites" % (k[0], k[1], by[k]))
const = [r for r in rows if r[5] is not None]
dyn = [r for r in rows if r[5] is None]
vals = collections.Counter(round(r[5], 4) for r in const)
print("distinct constant facings (value: sites): " + ", ".join("%.4f: %d" % (k, vals[k]) for k in sorted(vals)))
mx = max((abs(r[5]) for r in const), default=0.0)
print("max |constant facing| = %.6f rad (pi = %.6f, 4pi = %.6f)" % (mx, PI, 4 * PI))
over_pi = [r for r in const if abs(r[5]) > PI + 1e-6]
over_4pi = [r for r in const if abs(r[5]) > 4 * PI]
print("constant facings outside [-pi, pi]: %d; beyond 4pi: %d" % (len(over_pi), len(over_4pi)))
for r in over_pi[:40]:
    print("   out of [-pi,pi]: %s +0x%X %s %.6f" % (r[0], r[1], r[2], r[5]))
print("non-constant facings: %d" % len(dyn))
BOUNDED_CALLS = {"call:call:getrotangzx_12e", "call:call:getangzx_12f"}
vk_sites = collections.Counter(r[7] for r in dyn if r[7] is not None)
var_verdict = {}
for vk in sorted(vk_sites, key=str):
    ws = writers.get(vk, [])
    wv = [w[3] for w in ws]
    kinds = collections.Counter(w[2] if w[3] is None else "const" for w in ws)
    mxw = max((abs(x) for x in wv if x is not None), default=None)
    bounded = bool(ws) and all(w[3] is not None or w[2] in BOUNDED_CALLS for w in ws) and not pointer_refs.get(vk)
    if not ws and vk[0] == 1 and not pointer_refs.get(vk) and vk in initval:
        bounded = abs(initval[vk]) <= 4 * PI
        kinds["authored initial value %.4f" % initval[vk]] = 1
    var_verdict[vk] = bounded
    print("   var class %d offset 0x%06X %s: %d facing sites; writers %d (%s); max |const write| %s; pointer refs %d -> %s"
          % (vk[0], vk[1], vk[2].split("/")[-1] if vk[2] != "*" else "(shared)", vk_sites[vk], len(ws),
             ", ".join("%s %d" % kv for kv in sorted(kinds.items())), "%.4f" % mxw if mxw is not None else "-",
             len(pointer_refs.get(vk, [])), "BOUNDED by its writers" if bounded else "NOT BOUNDED here"))
call_dyn = [r for r in dyn if r[4] in BOUNDED_CALLS]
other_dyn = [r for r in dyn if r[7] is None and r[4] not in BOUNDED_CALLS]
unb_var = [r for r in dyn if r[7] is not None and not var_verdict[r[7]]]
wmax = max((abs(w[3]) for vk in var_verdict for w in writers.get(vk, []) if w[3] is not None), default=0.0)
print("non-constant split: getrotangzx %d, variable %d (%d on variables not bounded here), other %d"
      % (len(call_dyn), len(dyn) - len(call_dyn) - len(other_dyn), len(unb_var), len(other_dyn)))
print("max |constant write| into any facing variable = %.6f" % wmax)
acc_only = all(any(w[2].startswith("accumulator:") for w in writers.get(r[7], [])) for r in unb_var)
for r in unb_var:
    if "/us/" in r[0]:
        print("   unbounded variable site (us copy): %s +0x%X %s" % (r[0], r[1], r[4]))
        for w in writers.get(r[7], []):
            print("        writer %s +0x%X %s %s" % (w[0].split("/")[-1], w[1], w[2], "" if w[3] is None else "%.4f" % w[3]))
for r in other_dyn[:40]:
    print("   other non-constant site: %s +0x%X %s" % (r[0], r[1], r[4]))

check("C1", files > 1000 and scripts > 10000, "the corpus is the full script set (%d files, %d scripts)" % (files, scripts))
check("C2", ctrl_pushf > 1000 and ctrl_pushf_bad == 0,
      "positive control: %d PUSHF operands feeding other CALLs decode to finite floats in range (bad %d)"
      % (ctrl_pushf, ctrl_pushf_bad))
check("C3", len(rows) > 0 and any(r[2] == "setposparty" for r in rows),
      "setposparty call sites exist in the shipped corpus (%d sites of the two verbs)" % len(rows))
check("A1", acc_only, "every facing variable not bounded here has an accumulator writer (v += r each pass): %d sites, "
      "files %s" % (len(unb_var), sorted(set(r[0].split("/")[-1] for r in unb_var))))
check("R2", wmax <= 4 * PI, "no constant written into a facing variable reaches |x| > 4pi (max %.4f)" % wmax)
check("R1", not over_4pi, "no constant facing reaches |x| > 4pi (the only range 0033CB70 mis-normalises)")
print("SITES %d CONSTANT %d NONCONSTANT %d OVER_PI %d OVER_4PI %d UNBOUNDED_VARIABLE_SITES %d OTHER %d"
      % (len(rows), len(const), len(dyn), len(over_pi), len(over_4pi), len(unb_var), len(other_dyn)))
print("FAILS %d" % len(FAILS))
