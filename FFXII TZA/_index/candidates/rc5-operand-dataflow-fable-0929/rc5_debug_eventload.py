"""rc5_debug_eventload.py - RC-5 residue item "the operands of the battle-family verb 0x202D debug_eventload (0050D0C0)"
(FABLE, 2026-09-29). Census every CALL-family site of call id 0x202D in every shipped .ebp (all languages, all folders),
with its operands resolved by the shared decoder's backward stack walk (resolve_args; constants through the int pool).
Arity comes from the verb table; if the table has none, the census reports the sites and the pushes before them.
Control: the same walk finds call id 0x11B (startscene) sites; their 'us' count must equal ORACLE's rc5_verbs.tsv row
count for startscene (the same population rule: 'us' event/map scripts plus image/ff12/in controllers)."""
import collections, csv, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
S32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
TSV = os.path.join(DB, "_index", "candidates", "rc5-event-slot-routes-0930", "rc5_verbs.tsv")
verbs = G.load_verbs()
print("verb table entry for 0x202D:", verbs.get(0x202D))
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
sites = []; ss_us = set(); files = 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks, path)
    except Exception:
        continue
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B:
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
        continue
    files += 1
    pool = U32(sec, 0x20)
    starts = sorted(set(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt)))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    low = path.lower()
    for st in starts:
        end = min((x for x in bounds if x > st), default=len(sec))
        if st >= len(sec) or end <= st:
            continue
        ins, _ = G.decode(sec[st:end])
        for j, (pc, op, imm) in enumerate(ins):
            if op not in (0x58, 0x59, 0x5D, 0x5E):
                continue
            if imm == 0x11B and ("/us/" in low or "/image/ff12/in/" in low):
                ss_us.add((path, st + pc))
            if imm != 0x202D:
                continue
            v = verbs.get(0x202D)
            vals, stt = [], "no-arity"
            if v and v[0] is not None:
                need = v[0] + (1 if op in (0x59, 0x5E) else 0)
                args, stt = G.resolve_args(ins, j, need, verbs)
                for a in args or []:
                    n, im, k = a
                    if n == "PUSHII":
                        vals.append(str(im))
                    elif n.startswith("PUSHI") and n[-1].isdigit():
                        vals.append(n[-1])
                    elif n == "PUSHI":
                        vals.append(str(S32(sec, pool + im * 4 + 4)))
                    else:
                        vals.append("dyn:" + n)
            pre = " ".join(G.OPN.get(o, hex(o)) + ("" if i is None else "(%d)" % i) for _, o, i in ins[max(0, j - 4):j])
            sites.append((path, "%X" % (st + pc), G.OPN.get(op), stt, ";".join(vals), pre))
oracle = sum(1 for r in csv.DictReader(io.open(TSV, encoding="utf-8"), delimiter="\t") if r["verb"] == "startscene")
print("scripts read: %d; debug_eventload (0x202D) sites: %d" % (files, len(sites)))
for s in sites[:40]:
    print("  " + " | ".join(s))
print("operand values:", collections.Counter(s[4] for s in sites).most_common(20))
with io.open(os.path.join(HERE, "rc5_debug_eventload.tsv"), "w", encoding="utf-8", newline="\n") as w:
    w.write("file\tpc\topcode\tstatus\toperands_push_order\tpreceding\n")
    for s in sites:
        w.write("\t".join(s) + "\n")
print("status:", dict(collections.Counter(s[3] for s in sites)),
      " non-constant operand sites:", sum(1 for s in sites if "dyn:" in s[4] or not s[4]))
print("files:", dict(collections.Counter(s[0].rsplit("/", 1)[-1] for s in sites)))
print("folders (language dirs):", sorted(set(s[0].split("/")[3] for s in sites)))
firsts = collections.Counter(s[4].split(";")[0] for s in sites if ";" in s[4])
seconds = sorted(set(int(s[4].split(";")[1]) for s in sites if ";" in s[4] and s[4].split(";")[1].lstrip("-").isdigit()))
print("first operand values:", dict(firsts), " second operand distinct:", len(seconds), seconds)
print("CONTROL startscene sites in ORACLE's population: mine %d vs rc5_verbs.tsv %d -> %s" % (
    len(ss_us), oracle, "PASS" if len(ss_us) == oracle else "MISMATCH"))
print("FAILS %d" % (0 if len(ss_us) == oracle else 1))
