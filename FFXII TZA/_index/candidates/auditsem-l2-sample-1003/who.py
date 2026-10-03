"""Which lane wrote the decisive (re-)score in each requirement cell of the verdict table."""
import re, collections
P = r'C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\L2-VERDICTS.md'
L = open(P, encoding='utf-8').read().splitlines()
names = ['contract', 'types', 'relationships', 'runtime', 'script/data', 'L2']
LANE = re.compile(r'\((?:[^()]*?)(SWE2-[A-Z0-9-]+|OPUS|FABLE|ASTRA)\b')
tot = collections.Counter()
rows_sem_runtime = []
sample = {'S-02', 'S-13', 'S-28', 'S-43', 'S-36', 'S-49'}
for i, l in enumerate(L, 1):
    if not l.startswith('| **S-'):
        continue
    c = [x.strip() for x in re.split(r'(?<!\\)\|', l)[1:-1]]
    if len(c) < 8:
        continue
    sid = re.search(r'S-\d+', c[0]).group(0)
    who = []
    for n, v in zip(names, c[1:7]):
        m = LANE.search(v[:300])
        w = m.group(1) if m else ('bare' if v.strip('* ').startswith(('MET', 'N/A', 'LIVE')) else '?')
        who.append(w)
        tot[(n, w)] += 1
    if who[3] == 'SWE2-AUDIT-SEM':
        rows_sem_runtime.append(sid)
    if sid in sample:
        print(sid, dict(zip(names, who)))
print()
for n in names:
    print(n, {w: k for (nn, w), k in tot.items() if nn == n})
print('runtime cell last scored by SWE2-AUDIT-SEM:', len(rows_sem_runtime), 'of 52')
