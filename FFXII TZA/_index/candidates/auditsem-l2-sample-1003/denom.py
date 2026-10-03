"""Runtime cells of MET rows that reach MET by moving named items out of the runtime denominator."""
import re
P = r'C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\L2-VERDICTS.md'
pat = re.compile(r'out of (the|this) (runtime )?denominator|outside the (L2 |runtime )?denominator|static-structure|'
                 r'ruled outside|unreachable from every disclosed|device-gated|not in the denominator', re.I)
n = 0
for l in open(P, encoding='utf-8').read().splitlines():
    if not l.startswith('| **S-'):
        continue
    c = [x.strip() for x in re.split(r'(?<!\\)\|', l)[1:-1]]
    if len(c) < 8:
        continue
    hits = sorted(set(m.group(0).lower() for m in pat.finditer(c[4])))
    if hits:
        n += 1
        print(re.search(r'S-\d+', c[0]).group(0), hits)
print('rows:', n)
