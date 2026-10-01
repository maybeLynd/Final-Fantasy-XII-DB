"""rc20_refs.py - SWE2-AUDIT-SPEC (2026-09-30): RC-20 spot check with tk.py, independent of rc20_verbs.py.
Every stored pointer (DIR64 relocation target, and raw unaligned qword) equal to one of the four bodies or the thunk,
and every raw E8/E9 rel32 into them. Claim under test: the only data references are seven begin slots, and no code
calls or jumps into the bodies (only the thunk 0033F850 jumps to 00349680).
Control: the thunk's own jmp must be found by the rel32 sweep (sensitivity: a sweep that missed jmp thunks would print
zero code refs for 00349680 and wrongly look 'clean')."""
import struct, sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
T = [0x003548B0, 0x003488B0, 0x00349680, 0x00345430, 0x0033F850]
text = tk.d[tk.TRO:tk.TRO + tk.TRS]
for t in T:
    rel = tk.reloc_ptrs(t, t + 1)
    raw = tk.raw_q(t, t + 1)
    code = []
    for i in range(len(text) - 5):
        if text[i] in (0xE8, 0xE9):
            src = tk.TVA + i
            if (src + 5 + struct.unpack_from("<i", text, i + 1)[0]) & 0xFFFFFFFF == t:
                x = tk._decode_at(src)
                if x is not None and x.mnemonic in ("call", "jmp"):
                    code.append("%08X %s in %s" % (src, x.mnemonic, tk.fname(src)))
    print("%08X relocs %d raw-qwords %d code %d" % (t, len(rel), len(raw), len(code)))
    for r in rel:
        site = r[0]
        q, m = divmod(site - 0x01EED700 - 8, 32)   # family-0 table: record N at +8+32N; +0 begin, +8 poll, +0x18 result
        print("    reloc at %08X -> family-0 record 0x%04X, slot +0x%X" % (site, q, m))
    for c in code:
        print("    code ", c)
