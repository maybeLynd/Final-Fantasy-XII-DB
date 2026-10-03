import io
p = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\OPUS\cloud\interior_ingest.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b, key):
    global s
    if key in s:
        return
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


rep('''    uc1 = rep.get("mode") == "uc1"
    if uc1:''', '''    uc1 = rep.get("mode") == "uc1"
    ee = rep.get("mode") == "ee"
    if ee:
        # engine_explained (OPUS, 2026-10-03): unexplained bodies >= 128 B the page cites only at the entry, F or family
        targets = ee_targets(page)
    elif uc1:''', 'ee = rep.get("mode") == "ee"')
rep('''    rec = "opus-%s-%s-%s" % (slug[:40], "uc1" if uc1 else "homing" if homing else "cloudint", time.strftime("%m%d"))''',
    '''    rec = "opus-%s-%s-%s" % (slug[:40], "ee" if ee else "uc1" if uc1 else "homing" if homing else "cloudint", time.strftime("%m%d"))''',
    '"ee" if ee else "uc1"')
rep('''           "corrections": [], "mode": "uc1" if uc1 else "homing" if homing else "interior"}''',
    '''           "corrections": [], "mode": "ee" if ee else "uc1" if uc1 else "homing" if homing else "interior"}''',
    '"mode": "ee" if ee')
rep('''def uc1_entry_tokens():''', '''EB_JSON = os.path.normpath(os.path.join(cl.HERE, "..", "family", "entry_big.json"))


def ee_targets(page, fresh=False):
    """The page's unexplained entry-only bodies of 128 B or more (entry_big.py; fresh=True re-measures)."""
    if fresh:
        subprocess.run([sys.executable, "-B", os.path.join(os.path.dirname(EB_JSON), "entry_big.py")],
                       capture_output=True, text=True)
    return {int(h, 16) for h in json.load(open(EB_JSON)).get(page, [])}


def uc1_entry_tokens():''', "def ee_targets")
rep('''    still = (uc1_targets() if cfg.get("mode") == "uc1" else homing_targets() if cfg.get("mode") == "homing"
             else f_pack.entry_only_pages().get(page, set()))''',
    '''    still = (ee_targets(page, fresh=True) if cfg.get("mode") == "ee" else
             uc1_targets() if cfg.get("mode") == "uc1" else homing_targets() if cfg.get("mode") == "homing"
             else f_pack.entry_only_pages().get(page, set()))''', "ee_targets(page, fresh=True)")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
