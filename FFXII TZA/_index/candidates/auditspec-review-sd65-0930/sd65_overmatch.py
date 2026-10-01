"""sd65_overmatch.py - SWE2-AUDIT-SPEC (2026-09-30): is sd65_members.py's join sensitive to a wrong pairing?
Loads the author's script body up to its control section (its corpus read, route-site table and registered()), then:
  N1  negative control: for every class that declares members, every member name that class does NOT declare in any
      file but another class does. A join that over-matches resolves such wrong pairs; count them by form D / S / T.
  N2  ambiguity of the S / T hits on the true pairs: how many of the 177 census class names does the hit function
      reference (S), or how many template instantiations share the registrar (T).
The author's module is exec'd unchanged from its own directory (read-only; its json is only read)."""
import os, sys, collections
SRC = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sd65-dynamic-class-route-0930"))
code = open(os.path.join(SRC, "sd65_members.py"), encoding="utf-8").read()
code = code.split("# control: two schema rows resolve")[0]
g = {"__file__": os.path.join(SRC, "sd65_members.py"), "__name__": "sd65_members_body"}
exec(compile(code, "sd65_members.py(body)", "exec"), g)
import functools
for k in ("descriptors", "fns_ref", "strva"):          # memoise the author's pure lookups (globals resolved at call time)
    g[k] = functools.lru_cache(maxsize=None)(g[k])
decl, registered, CEN, fns_ref, TEMPLATE_FN =g["decl"], g["registered"], g["CEN"], g["fns_ref"], g["TEMPLATE_FN"]

own = {cn: set(m for ml in decl[cn] for m in ml) for cn in decl}
allm = set().union(*own.values())
true_forms = collections.Counter(); st_hits = []
for cn in decl:
    for m in own[cn]:
        hits, _ = registered(cn, m)
        if hits:
            true_forms[hits[0][0][0]] += 1
            if hits[0][0][0] in "ST": st_hits.append((cn, m, hits))
print("true pairs:", sum(len(v) for v in own.values()), "first-form counts:", dict(true_forms))

wrong = collections.Counter(); ex = collections.defaultdict(list); tested = 0
for cn in decl:
    for m in sorted(allm - own[cn]):
        tested += 1
        hits, _ = registered(cn, m)
        if hits:
            f = hits[0][0][0]; wrong[f] += 1
            if len(ex[f]) < 6: ex[f].append("%s::%s via %s" % (cn, m, "; ".join("%s @%08X in %08X" % h for h in hits[:2])))
print("N1 wrong pairs tested: %d; resolved: %d %s" % (tested, sum(wrong.values()), dict(wrong)))
for f in ex:
    for e in ex[f]: print("   e.g. [%s] %s" % (f, e))

names = list(CEN)
fnref = {cn: fns_ref(cn) for cn in names}
print("N2 S/T hits on true pairs: %d" % len(st_hits))
for cn, m, hits in st_hits:
    forms = set()
    for form, site, fn in hits:
        if form.startswith("S"):
            others = sorted(x for x in names if x != cn and fn in fnref[x])
            forms.add("S fn %08X also references %d other class name(s)%s" % (fn, len(others), (": " + ",".join(others[:4])) if others else ""))
        else:
            share = sorted(k for k, v in TEMPLATE_FN.items() if fn in v and k != cn)
            forms.add("T registrar %08X shared with %d other instantiation(s)%s" % (fn, len(share), (": " + ",".join(share[:3])) if share else ""))
    print("   %s::%s -> %s" % (cn, m, " | ".join(sorted(forms))))
