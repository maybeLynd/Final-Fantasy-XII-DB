# bank64_verb_census.py (FABLE, Claude Opus 5.5, 2026-09-25)
# DX-1: can an authored path pass a negative id to a Bank64 accessor? The four accessors (0032A9A0, 0032AA00,
# 0032AC70, 0032ACF0) have exactly six call sites in the raw call index, the six "shutoral" verb handlers
# 0x2F8..0x2FD (persistent-flag-banks.md section 8). This counts, over every shipped section_000 script image in
# every language copy, the CALL-family sites naming each of those six ids.
# Controls: settalknpcname 0x399 must be found (57 uses in the us scripts), and so must the load-mode setter
# 0x7067 in ttl_a01 and ttl_c01.
import io, os, sys, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
WANT = {0x2F8: "isshutoralappear (Bank64A query)", 0x2F9: "clearshutoralappear", 0x2FA: "setshutoralappear",
        0x2FB: "isshutoralenable (Bank64B query)", 0x2FC: "clearshutoralenable", 0x2FD: "setshutoralenable",
        0x399: "control: settalknpcname", 0x7067: "control: load-mode setter"}
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
    sys.exit("REFUSE: control failed - 0x7067 not found in ttl_a01 and ttl_c01")
if sites[0x399] == 0:
    sys.exit("REFUSE: control failed - settalknpcname 0x399 not found")
print("scripts read:", n_scripts, "| CALL-family sites decoded:", calls_total)
for cid in sorted(WANT):
    ss = sorted(scripts[cid])
    print("%04X  %-36s sites %6d  scripts %4d  %s" % (cid, WANT[cid], sites[cid], len(ss),
          ", ".join(os.path.basename(s) for s in ss[:8]) + (" ..." if len(ss) > 8 else "")))
