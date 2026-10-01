"""callers_check.py - SWE2-AUDIT-SPEC (2026-09-30): "only caller" spot checks for RC-15/16/17 and RC-11, from the raw
call index (pub140-scratch/tools/rawcalls.json) AND a fresh raw E8/E9 rel32 sweep of .text (decoded as call/jmp), plus
stored pointers (DIR64 relocations). A claim "X has one caller" passes only if all three agree.
jcc rel32 (0F 8x) forwarders are swept too. Control: 0036A100's rel32 callers must be many (a sweep that found nothing would print 0 and pass every 'only' claim)."""
import json, struct, sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
CLAIMS = [  # (target, claimed sites, source)
    (0x00266530, ["00267B79"], "RC-16 S1: ActorStorage_InitializeRecord has one caller"),
    (0x002679F0, ["0026CEB0"], "RC-16 S2: the pool allocator has one caller"),
    (0x00360880, ["002281B7"], "RC-17 K5: the skip loop has one caller"),
    (0x00285EA0, ["0022917A"], "RC-17 K6: the bit-13 setter has one caller"),
    (0x00504350, ["003AA109", "00500A20"], "RC-11 A1: the 0x59 loader is reached from 003A9EF0 / 00500980"),
    (0x0036A100, None, "control: a common allocator wrapper"),
]
text = tk.d[tk.TRO:tk.TRO + tk.TRS]
want = {t for t, _, _ in CLAIMS}
sweep = {t: [] for t in want}
for i in range(len(text) - 5):
    if text[i] in (0xE8, 0xE9):
        src = tk.TVA + i
        t = (src + 5 + struct.unpack_from("<i", text, i + 1)[0]) & 0xFFFFFFFF
        if t in want:
            x = tk._decode_at(src)
            if x is not None and x.mnemonic in ("call", "jmp"):
                sweep[t].append("%08X" % src)
    if text[i] == 0x0F and 0x80 <= text[i + 1] <= 0x8F and i + 6 <= len(text):   # jcc rel32 forwarders
        src = tk.TVA + i
        t = (src + 6 + struct.unpack_from("<i", text, i + 2)[0]) & 0xFFFFFFFF
        if t in want:
            x = tk._decode_at(src)
            if x is not None and x.mnemonic.startswith("j"):
                sweep[t].append("%08X(%s)" % (src, x.mnemonic))
for t, claim, why in CLAIMS:
    idx = sorted("%08X" % int(s, 16) for s in RAW.get("%X" % t, []))
    rel = tk.reloc_ptrs(t, t + 1)
    if claim is None:
        print("%08X %s: sweep %d, index %d, relocs %d -> %s" % (t, why, len(sweep[t]), len(idx), len(rel),
              "PASS" if len(sweep[t]) > 5 else "FAIL"))
        continue
    ok = sorted(sweep[t]) == sorted(claim) and not rel
    print("%08X %s\n    sweep %s  index %s  relocs %d -> %s" % (t, why, sweep[t], idx, len(rel), "HOLDS" if ok else "DIFFERS"))
