"""ask_sites.py - every caller of the ask 0032E520 (raw E8/E9/jcc + relocated pointers) and the ecx it passes
(last linear writer of rcx/ecx/cl before the site in the same owner). Then full listings of the two register-form
owners 0034DB30 and 0050D0C0 (from entry to the ask), for reading the edi / ebx paths by hand.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ind as I  # noqa: E402
import textcache as TC  # noqa: E402

T = TC.load()
pos = {a: k for k, (a, s, m, o, w) in enumerate(T)}
cs = I.calls_to(0x0032E520)
print("callers of 0032E520: %d sites, kinds %s, relocated pointers %s" % (
    len(cs), sorted({k for _, k in cs}), [("%08X" % a) for a, _ in I.abs64_refs(0x0032E520, 0x0032E521)]))
for s, kind in cs:
    k = pos[s]
    v = None
    for j in range(k - 1, max(0, k - 40), -1):
        a, sz, m, o, w = T[j]
        if w != T[k][4]:
            break
        if m == "call":
            v = "(call at %08X first)" % a
            break
        if re.match(r"^(rcx|ecx|cx|cl)\b", o) and m not in ("cmp", "test", "push"):
            v = "%08X %s %s" % (a, m, o)
            break
    print("  %08X %-3s owner %-10s ecx <- %s" % (s, kind, T[k][4], v))
for f, end in ((0x0034DB30, 0x0034DBE0), (0x0050D0C0, 0x0050D150)):
    print("--- %08X .. %08X" % (f, end))
    for i in I.dis(f, end):
        print("  %08X %s" % (i.address, I.txt(i)))
for a in (0x002FC3F0, 0x003B1380, 0x003B1790, 0x003B1970):
    print("--- %08X" % a)
    for i in I.dis(a, a + 0x40):
        print("  %08X %s" % (i.address, I.txt(i)))
