"""Census of the three experiment-frontmatter schema gaps, and the section-13 back-links.

`OPUS-EXP-CORPUS-SCHEMA` asks for "which contracts have live evidence" to be a QUERY rather than a
reading. Three keys make that possible and each has to be present on every record:

  method:     which of A/B/C the record's conclusions rest on   (rule: EVIDENCE-STANDARD 2026-09-13i)
  live_game:  whether the running game was touched at all
  contract:   the contract the record bears on, or an explicit `none - <reason>`

A missing key is not a neutral blank. `live_game:` absent reads as false to any filter that treats
absence as the default, so an unlabelled live record is invisible to exactly the query the field
exists for - which is why the seven 2026-09-12/13 records were repaired rather than left.

Also reports the reverse direction: a record naming a contract whose §13 does not name it back. A
one-directional link is a claim that only one side of the pair believes.

Exit 1 if any record is missing a key. Run from the repo root.
"""
import io, os, re, sys, collections

E = 'Database/FFXII TZA/_experiments'
DB = 'Database/FFXII TZA'

def frontmatter(text):
    if not text.startswith('---'):
        return {}
    end = text.find('\n---', 3)
    if end < 0:
        return {}
    fm = {}
    for line in text[3:end].split('\n'):
        m = re.match(r'([a-z_]+):\s*(.*)$', line.strip())
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm

records = []
for fn in sorted(os.listdir(E)):
    if not (fn.startswith('EXP-') and fn.endswith('.md')):
        continue
    path = os.path.join(E, fn)
    text = io.open(path, encoding='utf-8', errors='replace').read()
    records.append((fn, frontmatter(text)))

missing = collections.defaultdict(list)
for fn, fm in records:
    for key in ('method', 'live_game', 'contract'):
        if not fm.get(key):
            missing[key].append(fn)

print('experiment records: %d' % len(records))
for key in ('method', 'live_game', 'contract'):
    n = len(missing[key])
    print('  %-10s present on %d of %d%s' % (key, len(records) - n, len(records),
                                             '' if not n else '   MISSING: ' + ', '.join(
                                                 f[:12] for f in missing[key])))

print()
vals = collections.Counter(fm.get('method', '(none)').split(' - ')[0] for _, fm in records)
print('method: %s' % ', '.join('%s %d' % kv for kv in sorted(vals.items())))
live = collections.Counter(fm.get('live_game', '(none)') for _, fm in records)
print('live_game: %s' % ', '.join('%s %d' % kv for kv in sorted(live.items())))
st = collections.Counter(fm.get('status', '(none)').split(' ')[0] for _, fm in records)
print('status: %s' % ', '.join('%s %d' % kv for kv in st.most_common()))

# ---- the reverse direction: does the named contract name the record back? ----
print()
oneway, ok, nocontract = [], 0, 0
for fn, fm in records:
    c = fm.get('contract', '')
    if not c or c.lower().startswith('none'):
        nocontract += 1
        continue
    rel = c.split(' ')[0].split('#')[0]
    target = os.path.normpath(os.path.join(E, rel))
    eid = fn.split('-')[1]
    if not os.path.isfile(target):
        oneway.append((fn, 'contract path does not exist: ' + rel))
        continue
    body = io.open(target, encoding='utf-8', errors='replace').read()
    if ('EXP-' + eid) in body or ('EXP' + eid) in body:
        ok += 1
    else:
        oneway.append((fn, os.path.basename(target) + ' never names EXP-' + eid))

print('contract back-links: %d named and reciprocated, %d one-directional, %d declared none'
      % (ok, len(oneway), nocontract))
for fn, why in oneway:
    print('   %-46s %s' % (fn[:46], why))

live_docs = sorted({fm.get('contract', '').split(' ')[0] for _, fm in records
                    if fm.get('live_game') == 'true' and fm.get('contract')
                    and not fm.get('contract', '').lower().startswith('none')})
print()
print('contracts with live evidence (the query this schema exists to answer): %d' % len(live_docs))
for d in live_docs:
    print('   ' + d)

sys.exit(1 if any(missing.values()) else 0)
