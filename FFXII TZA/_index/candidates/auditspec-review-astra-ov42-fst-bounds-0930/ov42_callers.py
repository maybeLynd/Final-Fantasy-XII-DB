"""SWE2-AUDIT-SPEC independent caller census for the OV-42 path (raw call/jmp/jcc index + rip refs).
Targets: mapper 0032F170, size helper 0032E400, thunk 0046DE70, FST lookup 002DF960, requester 0032E620,
and the flat table 02EC3EE0 (every rip reference, with access width and store/load)."""
import sys, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
def callers(t):
    return RAW.get("%X" % t, RAW.get("%08X" % t, []))
for t in (0x32F170, 0x32E400, 0x46DE70, 0x2DF960, 0x32E620, 0x32F290):
    cs = callers(t)
    print("raw callers of %08X: %d" % (t, len(cs)))
    for s in cs:
        a = int(s, 16)
        print("   %08X in %s" % (a, tk.fname(a)))
# independent byte sweep for E8/E9/jcc rel32 to the lookup and thunk (control against rawcalls.json)
import struct
d = tk.d; TVA, TVS, TRS, TRO = tk.TVA, tk.TVS, tk.TRS, tk.TRO
def sweep(t):
    hits = []
    for o in range(TRO, TRO + TRS - 5):
        b = d[o]
        if b in (0xE8, 0xE9):
            rel = struct.unpack_from("<i", d, o + 1)[0]; va = TVA + (o - TRO)
            if va + 5 + rel == t: hits.append(("%02X" % b, va))
        elif b == 0x0F and 0x80 <= d[o + 1] <= 0x8F:
            rel = struct.unpack_from("<i", d, o + 2)[0]; va = TVA + (o - TRO)
            if va + 6 + rel == t: hits.append(("0F%02X" % d[o + 1], va))
    out = []
    for k, va in hits:   # keep only hits on a decoded instruction boundary of their owner
        try:
            if va in tk.boundaries(va): out.append((k, va))
        except Exception:
            out.append((k + "?", va))
    return out
for t in (0x2DF960, 0x46DE70, 0x32E400, 0x32F170):
    h = sweep(t)
    print("byte sweep E8/E9/0F8x -> %08X: %d  %s" % (t, len(h), " ".join("%s@%08X" % (k, v) for k, v in h)))
T = 0x2EC3EE0
res, raw_only = tk.rip_refs(T, T + 820000)
print("rip refs into flat table [02EC3EE0, +820000): %d verified, %d raw-only" % (len(res), len(raw_only)))
for x, k, tgt in res:
    print("   %08X %-6s %-40s tgt=%08X store=%s width=%d owner=%s" % (x.address, x.mnemonic, x.op_str[:40], tgt, tk.is_store(x, k), tk.memsize(x, k), tk.fname(x.address)))
dr = tk.disp_refs(T, T + 820000)
dr0 = dr[0] if isinstance(dr, tuple) else dr
print("image-base-relative disp refs into the table: %d" % len(dr0))
for h in dr0[:10]:
    x = h[0]; print("   %08X %s %s owner=%s" % (x.address, x.mnemonic, x.op_str[:40], tk.fname(x.address)))
