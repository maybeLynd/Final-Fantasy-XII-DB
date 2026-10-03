import io
p = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\OPUS\cloud\interior_ingest.py"
s = io.open(p, encoding="utf-8").read()
A = '''def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout + r.stderr'''
B = '''_MEMO = None          # apply-batch: tree-wide gate outputs computed once, after every page edit is in place


def run(cmd, cwd):
    key = (tuple(cmd), cwd)
    tree_wide = any(x.endswith(("check_consistency.py", "verify_doc_addresses.py", "check_links.py")) for x in cmd)
    if _MEMO is not None and tree_wide and key in _MEMO:
        return _MEMO[key]
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = r.stdout + r.stderr
    if _MEMO is not None and tree_wide:
        _MEMO[key] = out
    return out'''
if "_MEMO = None" not in s:
    assert s.count(A) == 1
    s = s.replace(A, B)
A2 = '''    if a and a[0] == "apply":
        sys.exit(apply(a[1], "--allow-before-verdict" in a))'''
B2 = '''    if a and a[0] == "apply":
        sys.exit(apply(a[1], "--allow-before-verdict" in a))
    if a and a[0] == "apply-batch":
        # 2026-10-03 (OPUS): every record's page edit first, then the tree-wide gates (check_links, check_consistency,
        # verify_doc_addresses) once for all of them; nb_page, self-contradiction and the queue spec stay per record.
        recs = [x for x in a[1:] if not x.startswith("--")]
        for rec in recs:
            rdir = os.path.join(cl.DB, "_index", "candidates", rec)
            o = run([sys.executable, "-B", "interior_applier.py", "--apply"], rdir)
            print("pre-apply %s: %s" % (rec, o.strip().splitlines()[-1] if o.strip() else "no output"))
        _MEMO = {}
        rc = 0
        for rec in recs:
            rc |= apply(rec, "--allow-before-verdict" in a)
        sys.exit(rc)'''
if '"apply-batch"' not in s:
    assert s.count(A2) == 1
    s = s.replace(A2, B2)
io.open(p, "w", encoding="utf-8", newline="\\n".encode().decode("unicode_escape")).write(s)
print("ok")
