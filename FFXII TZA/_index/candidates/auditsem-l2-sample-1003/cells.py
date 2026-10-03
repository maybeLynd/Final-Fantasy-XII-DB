"""Mirror goal_gate.check_verdicts row capture; report every captured row (incl. overwrites)
and the leading token of each of the five requirement cells."""
import re
P = r'C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\L2-VERDICTS.md'
lines = open(P, encoding='utf-8', errors='replace').read().splitlines()
width = None
for l in lines:
    if re.match(r"^\|\s*system\b", l, re.I) and "binding gap" in l:
        width = len([c for c in re.split(r"(?<!\\)\|", l) if c.strip()])
print('width', width)
seen = {}
def lead(c):
    c = c.strip().strip('*').strip()
    c = re.sub(r'^~~.*?~~\s*(→|->)?\s*', '', c).strip().strip('*').strip()
    m = re.match(r'([A-Za-z\- ]{2,20}?)(\b|$)', c)
    return c[:14]
for i, l in enumerate(lines, 1):
    m = re.match(r"^\|\s*(?:\*\*)?(S-\d+)\b([^|]*)\|(.*)$", l)
    if not m:
        continue
    cells = [c.strip().strip("*").strip() for c in re.split(r"(?<!\\)\|", m.group(3))]
    cells = [c for c in cells if c]
    if len(cells) == width - 1:
        sid = m.group(1)
        if sid in seen:
            print('OVERWRITE', sid, 'first line', seen[sid], 'now', i)
        seen[sid] = i
        req = [lead(c) for c in cells[:5]]
        flag = '' if all(r.startswith('MET') for r in req) else '  <-- requirement cell not leading MET'
        print(i, sid, '|'.join(req), '| L2:', cells[-2][:10], flag)
