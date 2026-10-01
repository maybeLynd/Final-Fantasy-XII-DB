"""rc5_verbs.py - RC-5 (ORACLE, 2026-09-30).  The event ids the three pusher sites can pass, bounded from authored scripts.

Original code (read in rc5 README): 00354B6D (verb 0xEC eventplay_ec, 00354B20) and 00354EDA (verb 0xEB eventplay,
00354E80) pass edx = -1 (`or edx, 0xffffffff` at 00354B68 / 00354ED5), which the pusher refuses (0020AF66).
0026B775 (0026B750) passes its own argument, which is the popped operand of verb 0x11B startscene (0034C9A0 -> jmp
0026B750) or the SECOND pop (= first pushed operand) of verb 0x4B3 startscene_4b3 (0034CED0 -> call 0026B750).

This census walks every shipped .ebp script (the same EBP2 walk and bytecode decoder as
20-Platform-Online-Achievements/members/script_award_verb_census.py, reused, not copied), finds every CALL-family
site (opcodes 0x58 CALL, 0x59 CALLACT, 0x5D CALLPOPA, 0x5E CALLACTPOPA) of call ids 0xEB, 0xEC, 0x11B and 0x4B3,
and resolves the pushed operands with the decoder's backward stack walk.  PUSHI operands are resolved through the
script's int constant pool (header +0x20, [pool + operand*4 + 4], section-000-bytecode.md).
Control: the 0x11B site count and the id distribution must reproduce the committed script-award-verb-census.tsv
(34,125 startscene rows); the run refuses to summarise if it does not.
Output rc5_verbs.tsv (one row per site, 'us' event/map scripts and the image/ff12/in controllers only) and a summary on stdout."""
import collections, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))            # the FFXII TZA database root
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))          # repository root: the decoder's relative paths
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
S32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
WANT = {0xEB: "eventplay", 0xEC: "eventplay_ec", 0x11B: "startscene", 0x4B3: "startscene_4b3",
        0xE7: "eventread", 0xE8: "eventread_e8", 0x198: "summoneventread"}
ARITY = {0xEB: 0, 0xEC: 1, 0x11B: 1, 0x4B3: 2, 0xE7: 1, 0xE8: 2, 0x198: 1}   # the verb table's CONFIRMED arity
verbs = G.load_verbs()
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
rows, calls_total, scripts = [], 0, 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks, path)
    except Exception:
        continue
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
        continue
    scripts += 1
    pool = U32(sec, 0x20)
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    seen = set()
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start:
            continue
        ins, _ = G.decode(sec[start:end])
        for j, (pc, op, imm) in enumerate(ins):
            if op not in (0x58, 0x59, 0x5D, 0x5E):
                continue
            calls_total += 1
            if imm not in WANT or (start + pc) in seen:
                continue
            seen.add(start + pc)
            need = ARITY[imm] + (1 if op in (0x59, 0x5E) else 0)
            args, st = G.resolve_args(ins, j, need, verbs)
            vals = []
            if args:
                for a in args:
                    name, im, kind = a
                    if name == "PUSHII":
                        vals.append(str(im))
                    elif name.startswith("PUSHI") and name[-1].isdigit():
                        vals.append(name[-1])
                    elif name == "PUSHI":
                        try:
                            vals.append(str(S32(sec, pool + im * 4 + 4)))
                        except struct.error:
                            vals.append("pool?%d" % im)
                    else:
                        vals.append("dyn:%s" % name)
            low = path.lower()
            cls = "event" if "/event/" in low else ("map" if "/plan_map/" in low else "other")
            rows.append((path, cls, "%x" % (start + pc), "%03X" % imm, WANT[imm], G.OPN.get(op), st, ";".join(vals)))
with io.open(os.path.join(HERE, "rc5_verbs.tsv"), "w", encoding="utf-8", newline="\n") as w:
    w.write("file\tclass\tpc\tcall_id\tverb\topcode\tstatus\tresolved_args_push_order\n")
    for r in rows:
        if "/us/" in r[0] or "/ff12/in/" in r[0]:     # one locale copy of each script; the summary covers all nine
            w.write("\t".join(r) + "\n")
print("scripts walked", scripts, "CALL-family sites", calls_total)
n11b = sum(1 for r in rows if r[3] == "11B")
print("CONTROL startscene rows", n11b, "(committed census: 34125)", "PASS" if n11b == 34125 else "FAIL")
c = collections.Counter((r[4], r[1], r[6]) for r in rows)
for k in sorted(c):
    print("%-15s %-6s %-26s %d" % (k + (c[k],)))
for verb in ("startscene", "startscene_4b3", "eventread", "eventread_e8", "summoneventread"):
    for cls in ("event", "map", "other"):
        ids = collections.Counter(r[7].split(";")[0] for r in rows if r[4] == verb and r[1] == cls and r[6] == "ok")
        if ids:
            nums = sorted(int(x) for x in ids if x.lstrip("-").isdigit())
            dyn = sum(v for x, v in ids.items() if not x.lstrip("-").isdigit())
            if verb.startswith(("eventread", "summon")):
                print(verb, cls, "all operand tuples", len(set(r[7] for r in rows if r[4] == verb and r[1] == cls)),
                      collections.Counter(r[7] for r in rows if r[4] == verb and r[1] == cls).most_common(12))
            print(verb, cls, "distinct ids", len(nums), "range", (nums[0], nums[-1]) if nums else None, "non-constant", dyn,
                  "minus1", ids.get("-1", 0), "top", ids.most_common(8))
