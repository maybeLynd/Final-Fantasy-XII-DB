# spawn_verb_call_census.py (FABLE, Claude Opus 5.5, 2026-09-25)
# UQ-55 / EF-5: how a script reaches this page's seven spawn verbs. They are the `begin`/`result` callbacks of
# seven family-3 records in scriptvm-verb-table.tsv (call ids 3001/3015/3016/304A/304B/305C/305F), reached by the
# CALL-family opcodes whose 16-bit operand is the packed id (family = id >> 12 at 00262205, index = id & 0xFFF).
# This counts, over every shipped section_000 script image, the sites that name each id and the opcode used.
# Reuses the REQ-family census decoder in 25-EBP-Script-Container/.../members (the same walk as
# sysreq_channel_census.py). Control: the decoded CALL-family site count must be non-zero, or the run refuses.
# Output: spawn-verb-call-census.tsv beside this file - a SUMMARY (a per-row table would be ~650,000 lines).
import io, os, sys, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))          # repository root: the decoder's relative paths
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
WANT = {0x3001: "btlAtelSetUnit", 0x3015: "btlAtelSetCallGroup", 0x3016: "btlAtelSetTotalEntryNumber",
        0x304A: "btlAtelGetRespawnTime", 0x304B: "btlAtelDecideEntryGroupByPreviousMap",
        0x305C: "btlAtelSetKeepWorkGroup", 0x305F: "btlAtelDecideEntryGroupByContinuous"}
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
sites = collections.Counter()
scripts = collections.defaultdict(set)
seen = set()
calls_total = n_scripts = 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks, path)
    except Exception:
        continue
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
        continue
    n_scripts += 1
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
        continue
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start:
            continue
        ins, _ = G.decode(sec[start:end])
        for pc, op, imm in ins:
            if op not in (0x58, 0x59, 0x5D, 0x5E):
                continue
            calls_total += 1
            if imm not in WANT or (path, start + pc) in seen:
                continue
            seen.add((path, start + pc))
            key = (imm, G.OPN.get(op, hex(op)))
            sites[key] += 1
            scripts[key].add(path)
if calls_total == 0:
    sys.exit("REFUSE: control failed - no CALL-family site decoded")
with open(os.path.join(HERE, "spawn-verb-call-census.tsv"), "w", newline="") as w:
    w.write("call_id\tverb\topcode\tsites\tscripts\n")
    for (cid, opn) in sorted(sites):
        w.write("%04X\t%s\t%s\t%d\t%d\n" % (cid, WANT[cid], opn, sites[(cid, opn)], len(scripts[(cid, opn)])))
print("scripts read:", n_scripts, "| CALL-family sites decoded:", calls_total, "| spawn-verb sites:", sum(sites.values()))
for (cid, opn) in sorted(sites):
    print("%04X  %-40s %-10s sites %7d  scripts %5d" % (cid, WANT[cid], opn, sites[(cid, opn)], len(scripts[(cid, opn)])))
print("scripts calling any:", len(set().union(*scripts.values())))
