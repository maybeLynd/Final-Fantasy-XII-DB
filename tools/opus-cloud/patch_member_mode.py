"""Add the `member` mode to interior_ingest.py and interior_applier.py (OPUS, 2026-10-03). Idempotent.
member: rows for unexplained members of a family the host page declares (mem_pack.py packs). Targets are those members;
after apply each must measure explained (the same check, fresh)."""
import io

P = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\OPUS\cloud"


def patch(fn, pairs):
    p = P + "\\" + fn
    s = io.open(p, encoding="utf-8", newline="").read()
    for key, a, b in pairs:
        if key in s:
            continue
        assert s.count(a) == 1, (fn, a[:60])
        s = s.replace(a, b)
    io.open(p, "w", encoding="utf-8", newline="").write(s)


patch("interior_ingest.py", [
    ('member = rep.get("mode") == "member"',
     '''    ee = rep.get("mode") == "ee"
    if ee:''',
     '''    ee = rep.get("mode") == "ee"
    member = rep.get("mode") == "member"
    if member:
        # family members (OPUS, 2026-10-03, mem_pack.py): unexplained members of a family the page declares
        targets = member_targets(page)
    elif ee:'''),
    ('def member_targets',
     '''def ee_targets(page, fresh=False):''',
     '''def member_targets(page):
    """Unexplained members of every family the page declares (mem_pack.py), measured now."""
    import mem_pack
    return {f for fs in mem_pack.unexplained_members(page).values() for f in fs}


def ee_targets(page, fresh=False):'''),
    ('"member" if member else "ee" if ee',
     '''    rec = "opus-%s-%s-%s" % (slug[:40], "ee" if ee else "uc1" if uc1 else "homing" if homing else "cloudint", time.strftime("%m%d"))''',
     '''    rec = "opus-%s-%s-%s" % (slug[:40], "ee" if ee else "uc1" if uc1 else "homing" if homing else "cloudint", time.strftime("%m%d"))
    if member:
        # one record per pack part: the report name carries the family slug and part number
        part = os.path.splitext(os.path.basename(report))[0]
        rec = "opus-%s-%s" % ("member" if member else "ee" if ee else "", part[-56:].strip("-"))'''),
    ('"mode": "member" if member',
     '''"corrections": [], "mode": "ee" if ee else "uc1" if uc1 else "homing" if homing else "interior"}''',
     '''"corrections": [], "mode": "member" if member else "ee" if ee else "uc1" if uc1 else "homing" if homing else "interior",
           "family": rep.get("family", "")}'''),
    ('member_targets(page) if cfg.get("mode") == "member"',
     '''    still = (ee_targets(page, fresh=True) if cfg.get("mode") == "ee" else''',
     '''    still = (member_targets(page) if cfg.get("mode") == "member" else
             ee_targets(page, fresh=True) if cfg.get("mode") == "ee" else'''),
    ('if cfg.get("mode") == "member":\n        readme[0]',
     '''    if cfg.get("mode") == "homing":
        # F homing (2026-10-03): say what these rows are; the entry-cited wording above does not apply.''',
     '''    if cfg.get("mode") == "member":
        readme[0] = "# Family members explained one by one: %d %s members on %s (OPUS, %s)" % (
            n, cfg.get("family", ""), os.path.basename(page), cfg["date"])
        readme[2] = ("The page declares the family `%s` (a classification family: ordinary functions grouped by module, not "
                     "template copies). No page explained these members. %s drafted one sentence and 1-5 interior anchors per "
                     "body from OPUS's pack (`mem_pack.py`); OPUS checked every row mechanically with `interior_ingest.py` "
                     "(member mode: the body is an unexplained member of a family this page declares) and re-read every "
                     "sentence against the bytes before applying." % (cfg.get("family", ""),
                         ("A local drafting agent (%s)" % cfg["session"]) if str(cfg.get("session", "")).startswith("local")
                         else "A session (%s)" % cfg.get("session", "")))
    if cfg.get("mode") == "homing":
        # F homing (2026-10-03): say what these rows are; the entry-cited wording above does not apply.'''),
    ('if cfg.get("mode") == "member":\n        title',
     '''    if cfg.get("mode") == "homing":
        title = ''',
     '''    if cfg.get("mode") == "member":
        title = "OPUS: %d %s members explained one by one on %s (drafted locally, OPUS-verified, %d anchors)" % (
            n, cfg.get("family", ""), os.path.basename(page), na)
    if cfg.get("mode") == "homing":
        title = '''),
])

patch("interior_applier.py", [
    ('if CFG.get("mode") == "member":',
     '''if CFG.get("mode") == "uc1":''',
     '''if CFG.get("mode") == "member":
    # family members (OPUS, 2026-10-03): one block per family part; the heading names the family and the record
    HEAD = ("## Family members explained one by one: %s (OPUS, %s, %s)\\n\\n" % (CFG.get("family", ""), CFG["date"], REC)
            + "*Members of the family `%s`, which this page declares, that no page explained. Each sentence states what "
            "the body does (access and representation, not purpose), and the anchors are instructions inside it that do "
            "it. Drafted locally from OPUS's pack and re-read by OPUS against the certified image; verified by "
            "[`%s`](%s_index/candidates/%s/%s): every anchor is an instruction boundary inside its function and decodes "
            "to the recorded mnemonic.*\\n\\n" % (CFG.get("family", ""), os.path.basename(__file__), DEPTH, REC,
                                                  os.path.basename(__file__))
            + "| function | size | what the body does | interior anchors |\\n|---|---|---|---|\\n")
if CFG.get("mode") == "uc1":'''),
])
print("ok")
