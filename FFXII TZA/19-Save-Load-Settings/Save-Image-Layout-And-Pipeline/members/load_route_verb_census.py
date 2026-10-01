# load_route_verb_census.py (FABLE, Claude Opus 5.5, 2026-09-25)
# FV-2: who sets 02089344 bit 0, the bit 00233C10 turns into block +4 bit 12 (the stash flag). Two writers exist
# in the image: SaveLoad_ControllerLifecycleHandler (00582CC8 / 00582CDE: 00238A30 with (00394450() == 3)) and the
# family-3 verb 0x308F, whose result callback 0050F5A0 is 00238A30(1). The callback of call n sits at
# [01F281B0 + 0x20n + 0x20] (scriptvm-native-dispatch-table.md), and scriptvm-verb-table.tsv agrees. The neighbouring
# verbs 0x308A / 0x308B (btlAtelResetNgPlus / NgMinus) set bits 1 / 2 (00238A20 / 00238A50); 0x308D stores block +4
# bit 12 directly (0050F500 -> 0023A390); 0x308E reads it back (0050F540 -> 00236760).
# This counts, over every shipped section_000 script image (all language copies), the CALL-family sites naming each id.
# Control: verb 0x7067 (the load-mode setter) must be found in ttl_a01 and ttl_c01, as FV-1 established.
import io, os, sys, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
WANT = {0x308F: "sets 02089344 bit 0 (0050F5A0)", 0x308A: "btlAtelResetNgPlus, bit 1",
        0x308B: "btlAtelResetNgMinus, bit 2", 0x308D: "block +4 bit 12 := arg (0023A390)",
        0x308E: "reads block +4 bit 12 (00236760)", 0x7067: "control: load-mode setter"}
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
            sites[imm] += 1
            scripts[imm].add(path)
if calls_total == 0:
    sys.exit("REFUSE: control failed - no CALL-family site decoded")
ctl = {os.path.basename(p).lower() for p in scripts[0x7067]}
if not any("ttl_a01" in p for p in ctl) or not any("ttl_c01" in p for p in ctl):
    sys.exit("REFUSE: control failed - 0x7067 not found in ttl_a01 and ttl_c01 (%s)" % sorted(ctl))
print("scripts read:", n_scripts, "| CALL-family sites decoded:", calls_total)
for cid in sorted(WANT):
    ss = sorted(scripts[cid])
    print("%04X  %-38s sites %6d  scripts %4d  %s" % (cid, WANT[cid], sites[cid], len(ss),
          ", ".join(os.path.basename(s) for s in ss[:12]) + (" ..." if len(ss) > 12 else "")))
