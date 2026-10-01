"""SWE2-AUDIT-SEM RC-5 attack (own parse of the us decompile; independent of rc5_constprop.py).
The propagation computes each function's values from its own path, merging other functions' stores only at function
entries. A file variable stepped by TWO OR MORE functions can change while one of them is suspended at a wait, so a
value computed along one function's path is exact only if no other function stores the variable between the store and
the use. For every `startscene(file_var_*)` call: which functions of the file assign that variable, and whether a
wait-type call (wait / sysReq*wait* / sysReqew / sysReqsw / ... any identifier containing 'wait') lies between the
nearest preceding assignment in the same function and the call. Joined per file with rc5_constprop.tsv's exact sites."""
import glob, os, re, collections, csv, io
CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
TSV = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\rc5-operand-dataflow-fable-0929\rc5_constprop.tsv"
exact = collections.Counter()
top = collections.Counter()
for r in csv.DictReader(io.open(TSV, encoding="utf-8"), delimiter="\t"):
    if r["verb"] not in ("startscene", "startscene_4b3"):
        continue
    base = os.path.splitext(os.path.basename(r["file"]))[0]
    if r["values"] == "TOP":
        top[base] += 1
    else:
        exact[base] += 1
FN = re.compile(r"^\s*(?:function|fn_\w+)\s+([^\s(]+)\s*\(")
WAITY = re.compile(r"\b\w*wait\w*\s*\(|\bsysReq(?:ew|sw|ewi|swi)\s*\(", re.I)
risk_sites = collections.Counter()
multi_files = {}
for f in sorted(glob.glob(os.path.join(CORPUS, "*.txt"))):
    base = os.path.splitext(os.path.basename(f))[0]
    if base not in exact and base not in top:
        continue
    L = io.open(f, encoding="utf-8", errors="replace").read().splitlines()
    fn, actor = None, None
    assigns = collections.defaultdict(set)
    calls = []
    fn_of = []
    for i, line in enumerate(L):
        if re.match(r"^actor\s", line):
            actor = line.split()[1]
        m = FN.match(line)
        if m:
            fn = (actor, m.group(1))
        fn_of.append(fn)
        for v in re.findall(r"\b(file_var_\w+)\s*=(?!=)", line):
            assigns[v].add(fn)
        m2 = re.search(r"\bstartscene(?:_4b3)?\((file_var_\w+)\)", line)
        if m2:
            calls.append((i, m2.group(1), fn))
    for i, v, f0 in calls:
        others = assigns[v] - {f0}
        if not others:
            continue
        # nearest preceding assignment of v in the same function, and any wait-type call between it and the call
        j = i - 1
        while j >= 0 and fn_of[j] == f0 and not re.search(r"\b%s\s*=(?!=)" % re.escape(v), L[j]):
            j -= 1
        between = any(WAITY.search(L[k]) for k in range(j + 1, i))
        risk_sites[(base, "wait-between" if between else "no-wait-between")] += 1
        multi_files[base] = len(others)
print("files with exact sites:", len(exact), " exact sites:", sum(exact.values()), " TOP sites:", sum(top.values()))
print("startscene(file_var) calls whose variable other functions also assign, per file (with/without a wait between"
      " the nearest same-function assignment and the call):")
tot_exact_files = 0
for base in sorted(multi_files):
    w = risk_sites[(base, "wait-between")]
    nw = risk_sites[(base, "no-wait-between")]
    print("  %-12s other assigning functions %d | calls: wait-between %d, no-wait %d | constprop exact %d, TOP %d" % (
        base, multi_files[base], w, nw, exact[base], top[base]))
    tot_exact_files += exact[base]
print("exact constprop sites in files whose counter is assigned by more than one function:", tot_exact_files)
