"""SWE2-AUDIT-SEM: condition U over the whole database - every token matching documented_rule.ID whose prefix is a register
prefix but which is not a register id, with page counts and one context line each, to find legitimate non-register tokens
the rule would fail a page on."""
import sys, os, re, io, collections
R = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\status-currency-ruling-fable"
sys.path.insert(0, R)
import documented_rule as D
state, kind, word, dup = D.register()
pref = collections.Counter(i.split("-")[0] for i in state)
print("register ids", len(state), "prefixes", len(pref))
print("prefixes:", " ".join("%s(%d)" % kv for kv in sorted(pref.items())))
tok = collections.defaultdict(set); ctx = {}
for root, ds, fs in os.walk(D.DB):
    if "_inbox" in root or os.sep + "candidates" in root:
        continue
    for f in fs:
        if not f.endswith(".md"):
            continue
        p = os.path.join(root, f)
        t = io.open(p, encoding="utf-8", errors="replace").read()
        for m in re.finditer(D.ID, t):
            i = m.group(1)
            if i not in state and i.split("-")[0] in pref:
                tok[i].add(os.path.relpath(p, D.DB))
                if i not in ctx:
                    s = t[max(0, m.start() - 60):m.end() + 40].replace("\n", " ")
                    ctx[i] = s
print("unknown register-prefix tokens:", len(tok), " pages touched:", len(set().union(*tok.values())) if tok else 0)
for i, ps in sorted(tok.items(), key=lambda kv: -len(kv[1]))[:60]:
    print("%-8s pages %3d | %s" % (i, len(ps), ctx[i][:140]))
