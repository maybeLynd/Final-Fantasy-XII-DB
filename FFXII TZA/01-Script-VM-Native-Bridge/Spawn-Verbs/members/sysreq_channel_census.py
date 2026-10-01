# sysreq_channel_census.py (FABLE, Claude Opus 5.5, 2026-09-25)
# UQ-54 / EF-2: the three script VERBS that pass a script value as the request channel to
# ActorResource_SubmitRequestDescriptor (003DBB60), which the REQ-family opcode census does not cover:
#   0x00AA sysreq    (3 args) 0034E5C0 -> 00269A90 -> 00269BA0 : pops class, ordinal, CHANNEL; channel -> r8d -> edx
#   0x0228 sysreqf   (3 args) 0034EC80 -> 00269A90 -> 00269BA0 : the same with the force flag 1
#   0x00AB sysreqall (2 args) 0034F380 -> 00269AD0            : pops class, CHANNEL; channel -> edx
# In every one the channel is the LAST value popped, so it is the FIRST argument pushed (args_push_order[0]).
# Only the class is bounded (cmp 0x12 at 00269AB1 / 00269AD0); the channel reaches the insert's
# upper-only clamp (003DB7C1). Reuses the REQ-family census decoder in 25-EBP-Script-Container/.../members.
# Control: the decoded CALL-family site count must be non-zero, or the run refuses to write a zero.
# Output: sysreq-channel-census.tsv beside this file.
import io, os, sys, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))          # repository root: the decoder's relative paths
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
WANT = {0x0AA: "sysreq", 0x0AB: "sysreqall", 0x228: "sysreqf"}
verbs = G.load_verbs()
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
rows, seen, calls_total, scripts = [], set(), 0, 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks, path)
    except Exception:
        continue
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
        continue
    scripts += 1
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
        for j, (pc, op, imm) in enumerate(ins):
            if op not in (0x58, 0x59, 0x5D, 0x5E):
                continue
            calls_total += 1
            if imm not in WANT:
                continue
            key = (path, start + pc)
            if key in seen:
                continue
            seen.add(key)
            v = verbs.get(imm)
            need = (v[0] if v and v[0] is not None else 1) + (1 if op in (0x59, 0x5E) else 0)
            args, st = G.resolve_args(ins, j, need, verbs)
            rows.append((path, "%x" % (start + pc), WANT[imm], G.OPN.get(op), st,
                         ";".join("%s:%s" % (a[0], a[1]) for a in args) if args else ""))
if calls_total == 0:
    sys.exit("REFUSE: control failed - no CALL-family site decoded")
with open(os.path.join(HERE, "sysreq-channel-census.tsv"), "w", newline="") as w:
    w.write("file\tpc\tverb\topcode\tstatus\targs_push_order\n")
    for r in rows:
        w.write("\t".join(str(x) for x in r) + "\n")
print("scripts read:", scripts, "| CALL-family sites decoded:", calls_total, "| sysreq-family rows:", len(rows))
print("by verb/opcode/status:", dict(collections.Counter((r[2], r[3], r[4]) for r in rows)))
ch = collections.Counter()
for r in rows:
    first = r[5].split(";")[0] if r[5] else "?"
    ch[(r[2], first)] += 1
for k, n in sorted(ch.items()):
    print("%6d  %-10s channel(arg0) = %s" % (n, k[0], k[1]))
