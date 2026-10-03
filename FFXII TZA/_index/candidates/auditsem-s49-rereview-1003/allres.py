"""Resolve EVERY backticked .data/.bss address anywhere in the given contracts (not only Types/State sections),
through the census's own resolver. Prints per-contract counts and each UNDECLARED with its section heading."""
import io, os, re, sys, collections
sys.path.insert(0, r'C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts')
import contract_named_state_census as C
DB = r'C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA'
spans, fields, sizes = C.load_store()
A = re.compile(r"`\[?(?:0x)?(0[0-9A-Fa-f]{7})\]?(?:\+0x[0-9A-Fa-f]+)?`")
for rel in sys.argv[1:]:
    txt = io.open(os.path.join(DB, rel), encoding='utf-8', errors='replace').read()
    cnt = collections.Counter()
    seen = {}
    sec = ''
    for line in txt.splitlines():
        if line.startswith('#'):
            sec = line.strip('# ')[:50]
        live = re.sub(r'~~.*?~~', '', line)
        for m in A.finditer(live):
            v = int(m.group(1), 16)
            if not (C.DATA_LO <= v < C.DATA_HI) or v in seen:
                continue
            r = C.resolve(v, spans, fields, sizes)
            seen[v] = (r, sec)
            cnt[r[0]] += 1
    print('==', rel, dict(cnt))
    for v, (r, s) in sorted(seen.items()):
        if r[0] != 'FIELD':
            print('   %08X %s %s | %s' % (v, r[0], (r[1] + ' ' + r[2]).strip(), s))
