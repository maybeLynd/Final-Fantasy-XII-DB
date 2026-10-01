"""Audit every contract's Runtime-validation section against the experiment records, both ways.

Direction A: a contract's section 13 names EXP-0NN -> does that record exist, and does it name the
             contract back (by file basename)?
Direction B: an experiment's `contract:` frontmatter names a contract -> does that contract's
             section 13 mention the experiment?

Positive controls are printed FIRST, because every number below is a property of two extractors:
  C1 the section extractor must find a Runtime-validation section in (nearly) every contract;
  C2 the EXP-id regex must find the ids in a record known to carry them;
  C3 a pair known to agree must come out AGREE.

ONE-WAY is ADVISORY, not a defect. A contract may cite an experiment as a *methodological
precedent* ("EXP-013 has already demonstrated the harness for exactly this shape") without the
record naming the contract back, and a link added to a contract after the record was written is
one-way by construction. Only DIRECTION B misses are defects: there the record itself declares
which contract it tests, and the contract does not reflect it.

Reported method is taken from the record's declared `method:` field, never inferred from prose.
Only 39 of 82 records carried that field when this check was written, so a record without one is
reported as unknown rather than guessed at.

Run with the database root as argv[1] (default: cwd).
"""
import re, os, io, sys, collections

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'

CONTRACTS = []
for dp, dn, fn in os.walk(ROOT):
    d = dp.replace(os.sep, '/')
    if '_experiments' in d or '/.git' in d:
        continue
    for f in fn:
        if f.startswith('CONTRACT-') and f.endswith('.md'):
            CONTRACTS.append(os.path.join(dp, f))
CONTRACTS.sort()

EXPDIR = os.path.join(ROOT, '_experiments')
EXPS = sorted(f for f in os.listdir(EXPDIR) if re.match(r'EXP-\d+.*\.md$', f))

EXPID = re.compile(r'EXP[-\s]?0*(\d{2,3})\b', re.I)


def ids(text):
    return set(int(m) for m in EXPID.findall(text))


SEC = re.compile(r'^##\s*13[.)]\s*(.*)$', re.M)

# Not every contract uses the 17-section template. A SHORT-FORM contract has a handful of numbered
# mechanism sections, a "What this contract does not establish" section, and a section 15 Evidence.
# Its runtime statement lives in that section, not in a section 13. Reporting those five as "no
# section 13" (as the 2026-09-13 audit first did) states a true fact and implies a false one: that
# they cannot be audited. They can; the section is named rather than numbered.
SHORT = re.compile(r'^##\s*\d+[.)]\s*(?:What\s+)?(?:this contract |is )?[Nn]ot established.*$|'
                   r'^##\s*\d+[.)]\s*What this contract does not establish.*$', re.M)


def _span(text, m):
    nxt = re.search(r'^##\s+', text[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(text) - m.end())
    return m.group(0).strip('# ').strip(), text[m.start():end]


def sec13(text):
    m = SEC.search(text)
    if m:
        nxt = re.search(r'^##\s+(?!13[.)])', text[m.end():], re.M)
        end = m.end() + (nxt.start() if nxt else len(text) - m.end())
        return m.group(1).strip(), text[m.start():end]
    m = SHORT.search(text)
    if m:
        title, body = _span(text, m)
        return '[short form] ' + title, body
    return None, None


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, '/')


ctext = {c: io.open(c, encoding='utf-8', errors='replace').read() for c in CONTRACTS}
etext = {e: io.open(os.path.join(EXPDIR, e), encoding='utf-8', errors='replace').read() for e in EXPS}
expnum = {}
for e in EXPS:
    expnum[int(re.match(r'EXP-(\d+)', e).group(1))] = e

# ---- controls -------------------------------------------------------------
missing13 = [c for c in CONTRACTS if sec13(ctext[c])[0] is None]
short = sum(1 for c in CONTRACTS
            if (sec13(ctext[c])[0] or '').startswith('[short form]'))
print('C1 section extractor: %d/%d contracts expose a runtime-validation section '
      '(%d numbered 13, %d short-form "not established")'
      % (len(CONTRACTS) - len(missing13), len(CONTRACTS),
         len(CONTRACTS) - len(missing13) - short, short))
for c in missing13:
    print('     no section 13: %s' % rel(c))
probe = 'EXP-080-older-save-live-load.md'
found = sorted(ids(etext.get(probe, '')))
print('C2 EXP-id regex on a record known to carry ids: %s -> %s'
      % (probe, found or 'NONE -- regex blind, stop'))
print()

# ---- direction A ----------------------------------------------------------
rows = []
for c in CONTRACTS:
    title, body = sec13(ctext[c])
    if body is None:
        rows.append((c, 'NO-SEC13', set(), ''))
        continue
    cited = ids(body)
    if not cited:
        rows.append((c, 'NO-EXP', set(), title))
        continue
    bad = []
    base = os.path.basename(c).lower()[:-3]
    stem = base.replace('contract-', '')
    for n in sorted(cited):
        e = expnum.get(n)
        if e is None:
            bad.append('EXP-%03d MISSING RECORD' % n)
            continue
        low = etext[e].lower()
        if base not in low and stem not in low:
            bad.append('EXP-%03d does not name this contract' % n)
    rows.append((c, 'AGREE' if not bad else 'ONE-WAY', cited, '; '.join(bad)))

print('=== DIRECTION A: contract section 13 -> experiment record ===')
print('   ', dict(collections.Counter(r[1] for r in rows)))
for c, st, cited, note in rows:
    if st == 'ONE-WAY':
        print('  ONE-WAY  %-58s %s' % (rel(c), note))
print()
print('   contracts whose section 13 names NO experiment at all:')
for c, st, cited, title in rows:
    if st == 'NO-EXP':
        print('     %-58s (13: %s)' % (rel(c), title[:38]))
print()

# ---- direction B ----------------------------------------------------------
print('=== DIRECTION B: experiment frontmatter -> contract section 13 ===')
unmatched = []
linked = 0
for e in EXPS:
    m = re.search(r'^contract:\s*(.+)$', etext[e], re.M)
    if not m:
        continue
    val = m.group(1).strip()
    if val.lower().startswith('none') or val in ('-', ''):
        continue
    n = int(re.match(r'EXP-(\d+)', e).group(1))
    hits = []
    for c in CONTRACTS:
        b = os.path.basename(c).lower()[:-3]
        if b in val.lower() or b.replace('contract-', '') in val.lower():
            hits.append(c)
    if not hits:
        unmatched.append((e, 'no contract file matches frontmatter value: %s' % val[:60]))
        continue
    for c in hits:
        linked += 1
        title, body = sec13(ctext[c])
        if body is None:
            unmatched.append((e, '%s has no section 13' % rel(c)))
        elif n not in ids(body):
            unmatched.append((e, '%s section 13 does not mention EXP-%03d' % (rel(c), n)))
print('   %d experiment->contract links resolved; %d not reflected in the contract:'
      % (linked, len(unmatched)))
for e, why in unmatched:
    print('     %-42s %s' % (e, why))
