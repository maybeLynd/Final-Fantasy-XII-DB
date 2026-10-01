# HM-1 attach census (OPUS, 2026-09-27): every shipped call of script verb 0xD9 attach / 0xDA attachoff, with the
# resolved pushed arguments. Reuses FABLE's decoder pattern (20-Platform-Online-Achievements/members/
# script_award_verb_census.py, over 25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py).
# Control: the decoded CALL-family site count must be non-zero, or the run refuses.
# Output: a TSV at ATTACH_CENSUS_OUT (default %TEMP%/attach-census.tsv) - not published; the counts are the claim.
import io, os, sys, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
WANT = {0xD9: "attach", 0xDA: "attachoff"}
verbs = G.load_verbs()
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
rows, seen, calls_total, files = [], set(), 0, 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try: b = G.V.read_entry(f, names, blocks, path)
    except Exception: continue
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B: continue
    files += 1
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        ins, _ = G.decode(sec[start:end])
        for j, (pc, op, imm) in enumerate(ins):
            if op not in (0x58, 0x59, 0x5D, 0x5E): continue
            calls_total += 1
            if imm not in WANT: continue
            key = (path, start + pc)
            if key in seen: continue
            seen.add(key)
            v = verbs.get(imm)
            need = (v[0] if v and v[0] is not None else 1) + (1 if op in (0x59, 0x5E) else 0)
            args, st = G.resolve_args(ins, j, need, verbs)
            rows.append((path, "%x" % (start + pc), WANT[imm], G.OPN.get(op), st,
                         ";".join("%s:%s" % (a[0], a[1]) for a in args) if args else ""))
if calls_total == 0: sys.exit("REFUSE: control failed - no CALL-family site decoded")
out = os.environ.get("ATTACH_CENSUS_OUT") or os.path.join(os.environ.get("TEMP", "."), "attach-census.tsv")
with open(out, "w", newline="") as w:
    w.write("file\tpc\tverb\topcode\tstatus\targs_push_order\n")
    for r in rows: w.write("\t".join(str(x) for x in r) + "\n")
print("ebp files", files, "| CALL-family sites", calls_total, "| rows", len(rows), dict(collections.Counter(r[2] for r in rows)))
print("files with attach:", len({r[0] for r in rows if r[2] == "attach"}), "| wrote", out)
