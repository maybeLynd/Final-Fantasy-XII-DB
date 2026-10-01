import io, re, collections, os
import kit_paths as KP  # noqa: E402
import os

G = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph")
DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")

GEN = ("CompilerGeneratedEH", "CompilerGeneratedCFG", "CompilerGeneratedCpp",
       "Runtime.Callback.", "Reflection.PClassDescriptorForType",
       "Reflection.DataMemberMetadataStaticTeardown", "Reflection.ClassDescriptorStaticTeardown",
       "Reflection.AnnotationStaticTeardown", "Reflection.ReflectionStaticTeardown",
       "Reflection.ObjectTraversalAdapter", "ScriptVM.ObjectPushAdapter",
       "ScriptVM.NullableObjectPushAdapter", "Thunk.")

fns = {}
eh = set()
for ln in io.open(os.path.join(G, "functions.tsv"), encoding="utf-8", errors="replace"):
    p = ln.rstrip("\n").split("\t")
    if len(p) < 9 or not re.match(r"^[0-9A-F]{8}$", p[0]):
        continue
    fns[p[0]] = {"sz": int(p[2]), "nm": p[1], "own": p[3], "tags": p[8],
                 "gen": any(g in p[8] for g in GEN), "thunk": p[5].lower() == "true"}
    if "CompilerGeneratedEH" in p[8]:
        eh.add(p[0])

authored = {k for k, v in fns.items() if not v["gen"] and not v["thunk"]}

callers = collections.defaultdict(set)
eh_targets = set()
for ln in io.open(os.path.join(G, "edges.tsv"), encoding="utf-8", errors="replace"):
    p = ln.rstrip("\n").split("\t")
    if len(p) < 2 or p[0] == "caller":
        continue
    a, b = p[0].upper(), p[1].upper()
    if a in eh:
        eh_targets.add(b)
        continue
    callers[b].add(a)

pop = {t for t in eh_targets if t in authored and not callers.get(t)}
print("EC-1 population (authored, zero non-EH callers, >=1 EH caller): %d" % len(pop))

RE = re.compile(r"(?<![0-9A-Za-z_])(?:0[xX])?([0-9A-Fa-f]{8})(?![0-9A-Za-z_])")
cites = collections.defaultdict(set)
sep = chr(92)
for root, dirs, files in os.walk(DB):
    dirs[:] = [d for d in dirs if d != "_templates"]
    for f in files:
        if not f.endswith(".md"):
            continue
        rel = os.path.relpath(os.path.join(root, f), DB).replace(sep, "/")
        if rel.startswith("_index/"):
            continue
        t = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
        for m in RE.finditer(t):
            a = m.group(1).upper()
            if a in pop:
                cites[a].add(rel)

print("of those, cited by at least one system document: %d" % len(cites))
print()
for a in sorted(cites):
    print("%s %-30s %6dB  %-24s" % (a, fns[a]["nm"], fns[a]["sz"], fns[a]["own"] or "-"))
    for d in sorted(cites[a]):
        print("        %s" % d)
