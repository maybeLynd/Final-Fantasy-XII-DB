"""e4_manifest_models.py - OV-33 E4-archive lead (FABLE, 2026-09-30): can a shipped model id reach 002E6700 -> 002EAD50 as
kind 1 with id 127..132 (the archive-missing kind-1 rows US 129-131, UK 131-132, CN 127)?

002ED6F0 maps a model id (letter << 16) + N: letters c n s m b g C N S M t w go to their own kinds; any other letter goes
to kind 1 with index N (default arm 002ED840), and 002E6700 / 002EAD50 add 0x33 (002E676C, 002EAD95). So the lead needs
a model id whose letter is outside those twelve and whose N is 76..81 (+0x33 = 127..132).
Source of model ids examined here: every shipped EBP's section 12, the manifest ({count; u32 id[count]} at the file
offset stored at header +0x40; OPUS's c22_bind.py, 002E9A60 -> 00263F80). Other model-id sources are not covered.
Control: dgl_g0102's manifest must contain C:22 ((0x43 << 16) + 22), the entry OPUS's HM-1 record names."""
import collections, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
KNOWN = set(map(ord, "cnsmbgCNSMtw"))
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
letters = collections.Counter(); hits = []; files = 0; bad = 0; ctl = False
for p in sorted(n for n in names if n.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks, p)
    except Exception:
        bad += 1; continue
    if len(b) < 0x44:
        continue
    o = U32(b, 0x40)
    if not o or o + 4 > len(b):
        continue
    n = U32(b, o)
    if n > 0x2000 or o + 4 + 4 * n > len(b):
        bad += 1; continue
    files += 1
    for i in range(n):
        v = U32(b, o + 4 + 4 * i)
        let, N = (v >> 16) & 0xFF, v & 0xFFFF
        letters[let] += 1
        if "dgl_g0102" in p and v == (0x43 << 16) + 22:
            ctl = True
        if let not in KNOWN and 76 <= N <= 81 and v < 0x1000000:
            hits.append((p, "%08X" % v, chr(let) if 32 < let < 127 else hex(let), N))
print("EBP files with a manifest: %d (unreadable/odd %d)" % (files, bad))
print("letters seen (count):", {(chr(k) if 32 < k < 127 else hex(k)): c for k, c in sorted(letters.items())})
print("CONTROL dgl_g0102 manifest holds C:22:", "PASS" if ctl else "FAIL")
print("manifest model ids with an unknown letter and N in 76..81 (kind-1 ids 127..132): %d" % len(hits))
for h in hits[:30]:
    print("  ", h)
print("FAILS %d" % (0 if ctl else 1))
sys.exit(0 if ctl else 1)
