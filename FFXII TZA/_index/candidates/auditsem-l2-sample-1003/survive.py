"""For each file: for each commit touching it since SINCE, the long '+' lines it added; report commits whose
added lines are mostly absent from HEAD, together with the first later commit to the file that dropped them.
Heuristic worklist (rewording also drops lines) - every hit needs a manual read.
usage: survive.py SINCE file..."""
import subprocess, sys
ROOT = r'C:\Users\Kristian\source\repos\XIIOnline'
SINCE = sys.argv[1]


def git(*a):
    return subprocess.run(['git', '-c', 'core.longpaths=true', *a], cwd=ROOT, capture_output=True, text=True,
                          encoding='utf-8', errors='replace').stdout


for f in sys.argv[2:]:
    head = set(l.strip() for l in git('show', 'HEAD:' + f).splitlines())
    commits = git('log', '--format=%h', '--since=' + SINCE, '--', f).split()
    for c in commits:
        d = git('show', '--format=', '-U0', c, '--', f)
        added = [l[1:].strip() for l in d.splitlines() if l.startswith('+') and not l.startswith('+++')]
        added = [a for a in added if len(a) > 50 and '~~' not in a]
        if len(added) < 3:
            continue
        lost = [a for a in added if a not in head]
        if len(lost) >= 0.6 * len(added):
            dropper = ''
            later = git('log', '--format=%h', '--reverse', '--ancestry-path', c + '..HEAD', '--', f).split()
            probe = lost[0]
            for lc in later:
                if probe not in git('show', '%s:%s' % (lc, f)):
                    dropper = lc + ' ' + git('log', '-1', '--format=%ad %s', '--date=short', lc)[:80].strip()
                    break
            subj = git('log', '-1', '--format=%ad %s', '--date=short', c)[:90].strip()
            print('%s\n   %s added %d lost %d | %s\n   dropped by: %s' % (f.split('/')[-1], c, len(added), len(lost), subj, dropper))
