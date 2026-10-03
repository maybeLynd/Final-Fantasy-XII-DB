#!/usr/bin/env python3
"""test_recon_depgraph.py - isolated-fixture checks C1-C6 for recon_depgraph.py (SWE2-CONTRACT, 2026-10-03).

Every case builds its inputs in a temp dir; no live peer file is read or written. The checks are the design note's
section 7 (_index/candidates/swe2contract-design-reconstruction-dependency-graph-1003/README.md).
"""
import importlib.util
import io
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recon_depgraph as rd  # noqa: E402

FUNCS_HEAD = "entry\tname\tbody_bytes\towner\tfinal_no_owner\tthunk\tnoreturn\tcomment_len\ttags\n"


def fixture(root, world="03-World-Area-Field", combat="07-Combat-Action", formula="08-Combat-Formula",
            note="SERVICE, tier 1 (body read): A calls B.", verdict="CROSSING-ACCOUNTED", vm="01-Script-VM-Native-Bridge"):
    """Owners: World (W), Combat (C), Formula (F); 00004000 unowned. Folder names are parameters so C1 can renumber."""
    files = {
        "functions": FUNCS_HEAD +
        "00001000\tFUN_00001000\t64\tCombat\tfalse\tfalse\tfalse\t0\t\n"
        "00002000\tFUN_00002000\t64\tFormula\tfalse\tfalse\tfalse\t0\t\n"
        "00003000\tFUN_00003000\t64\tWorld\tfalse\tfalse\tfalse\t0\t\n"
        "00004000\tFUN_00004000\t64\t\tfalse\tfalse\tfalse\t0\t\n"
        "00005000\tFUN_00005000\t64\tWorld\tfalse\tfalse\tfalse\t0\t\n",
        "edges": "caller\tcallee\tcallee_external\tcallee_name\n"
                 "00001000\t00002000\tfalse\tFUN_00002000\n"      # Combat -> Formula (S1 hard)
                 "00003000\t00001000\tfalse\tFUN_00001000\n",     # World -> Combat (S1 hard, made MECHANICAL by S2)
        "owner_map": "# map\nchain_label\towner_token\tcategory_dir\tnote\n"
                     "Combat\tCombat\t%s\tx\nFormula\tFormula\t%s\tx\nWorld\tWorld\t%s\tx\nVM\tVM\t%s\tx\n"
                     % (combat, formula, world, vm),
        "dispositions": "# registry\n"
                        # outbound: subject 00001000 (Combat page) calls far 00002000 (Formula)
                        "%s/p.md\tFormula\t1\tsrc\t00001000 callee 00002000\t%s\t%s\n"
                        # inbound, MECHANICAL: far 00003000 (World) calls subject 00001000
                        "%s/p.md\tWorld\t1\tsrc\t00001000 caller 00003000\tGENUINELY-IRRELEVANT\tMECHANICAL: shared accessor\n"
                        # unowned subject 00004000 claimed by pages in two folders -> ambiguous
                        "%s/q.md\tWorld\t1\tsrc\t00004000 callee 00005000\tCROSSING-ACCOUNTED\tSERVICE, tier 2\n"
                        "%s/r.md\tWorld\t1\tsrc\t00004000 callee 00005000\tCROSSING-ACCOUNTED\tSERVICE, tier 2\n"
                        # owned subject 00002000 (Formula) cited on a Combat page -> owner-conflict, from = Formula
                        "%s/s.md\tWorld\t1\tsrc\t00002000 callee 00005000\tCROSSING-ACCOUNTED\tSERVICE, tier 1\n"
                        % (combat, verdict, note, combat, combat, formula, combat),
        "field_access": "type\tdisp\tbase\tkind\tfunction\tsite\tinstruction\tnote\n"
                        "WorldRecord\t0x4\t0x0\tr\t00001000\t00001010\tmov eax, dword ptr [rcx + 4]\t\n",
        "types": "type\tsize\tcategory\tinstance\n"
                 "WorldRecord\t0x10\t%s\tx\n" % world,
        "verbs": "# verbs\ncall_id\tverb\targs\thandler\thandler_name\towner\tbegin_handler\tpoll_handler\n"
                 "0001\tsetpos\t3\t00003000\tFUN_00003000\tWorld\t\t\n",
    }
    paths = {}
    for k, text in files.items():
        p = os.path.join(root, k + ".tsv")
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        paths[k] = p
    return paths


def build(root, **kw):
    inputs = fixture(root, **kw)
    edges, comp, _ = rd.run(inputs, root)
    return inputs, edges, comp


def keyset(edges, rename=None):
    rename = rename or {}
    r = lambda n: rename.get(n, n)
    return {(r(e["frm"]), r(e["to"]), e["kind"], e["basis"], tuple(sorted(e["flags"]))) for e in edges}


class Checks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_c1_no_folder_order(self):
        _, a, _ = build(self.root)
        other = tempfile.TemporaryDirectory()
        try:
            _, b, _ = build(other.name, world="97-World-Area-Field", combat="13-Combat-Action",
                            formula="05-Combat-Formula", vm="88-Script-VM-Native-Bridge")
        finally:
            other.cleanup()
        back = {"97-World-Area-Field": "03-World-Area-Field", "13-Combat-Action": "07-Combat-Action",
                "05-Combat-Formula": "08-Combat-Formula", "88-Script-VM-Native-Bridge": "01-Script-VM-Native-Bridge"}
        self.assertEqual(keyset(a), keyset(b, back))

    def test_c2_every_edge_cited(self):
        _, edges, _ = build(self.root)
        self.assertTrue(edges)
        self.assertEqual(rd.verify_citations(edges, self.root), [])
        p = os.path.join(self.root, "edges.tsv")
        with io.open(p, encoding="utf-8") as f:
            text = f.read().replace("00001000\t00002000", "00001000\t00009999")
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        self.assertTrue(rd.verify_citations(edges, self.root))

    def test_c3_direction(self):
        _, edges, _ = build(self.root)
        disp = [e for e in edges if e["basis"] == "call-dispositioned" and not e["flags"]]
        out = [e for e in disp if e["kind"] == "hard"]
        self.assertEqual([(e["frm"], e["to"]) for e in out], [("07-Combat-Action", "08-Combat-Formula")])
        inbound = [e for e in disp if e["kind"] == "sequencing"]
        self.assertEqual([(e["frm"], e["to"]) for e in inbound], [("03-World-Area-Field", "07-Combat-Action")])
        # cross-check against the pass-22 label rule (inbound = CLIENT, outbound = SERVICE), imported not copied
        src = os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates",
                           "frontier-pass22-unattributed-0930", "pass22_neighbour_bullets.py")
        if os.path.exists(src):
            spec = importlib.util.spec_from_file_location("p22b", src)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            self.assertEqual(m.label([("00001000", "callee", "00002000")]), "SERVICE")
            self.assertEqual(m.label([("00001000", "caller", "00003000")]), "CLIENT")

    def test_c4_classifier_sensitivity(self):
        _, mech, _ = build(self.root, note="MECHANICAL: named accessor", verdict="GENUINELY-IRRELEVANT")
        hard = lambda es: {(e["frm"], e["to"]) for e in es
                           if e["kind"] == "hard" and e["basis"] in ("call", "call-dispositioned") and not e["flags"]}
        self.assertNotIn(("07-Combat-Action", "08-Combat-Formula"), hard(mech))
        other = tempfile.TemporaryDirectory()
        try:
            _, serv, _ = build(other.name)
        finally:
            other.cleanup()
        self.assertIn(("07-Combat-Action", "08-Combat-Formula"), hard(serv))

    def test_c5_freshness(self):
        inputs, edges, comp = build(self.root)
        prefix = os.path.join(self.root, "out")
        rd.write_outputs(prefix, edges, comp, inputs, self.root, {})
        self.assertEqual(rd.check(prefix + ".tsv", self.root), [])
        with io.open(inputs["types"], "a", encoding="utf-8", newline="\n") as f:
            f.write("Extra\t0x8\t07-Combat-Action\tx\n")
        moved = rd.check(prefix + ".tsv", self.root)
        self.assertEqual(len(moved), 1)
        self.assertIn("types", moved[0])

    def test_c6_flags_listed_not_resolved(self):
        _, edges, comp = build(self.root)
        amb = [e for e in edges if "ambiguous" in e["flags"]]
        self.assertTrue(amb)
        self.assertTrue(all(e["frm"] in ("07-Combat-Action", "08-Combat-Formula") for e in amb))
        conflict = [e for e in edges if "owner-conflict" in e["flags"]]
        self.assertEqual([(e["frm"], e["to"]) for e in conflict], [("08-Combat-Formula", "03-World-Area-Field")])
        # ambiguous rows never shape components; owner-conflict rows do (the ledger is the authority)
        in_comp = {n for c in comp["weak_components"] for n in c}
        self.assertIn("08-Combat-Formula", in_comp)

    def test_script_binding_is_sequencing(self):
        _, edges, _ = build(self.root)
        sb = [e for e in edges if e["basis"] == "script-binding"]
        self.assertEqual([(e["frm"], e["to"], e["kind"]) for e in sb],
                         [("01-Script-VM-Native-Bridge", "03-World-Area-Field", "sequencing")])

    def test_type_layout_is_hard(self):
        _, edges, _ = build(self.root)
        tl = [e for e in edges if e["basis"] == "type-layout"]
        self.assertEqual([(e["frm"], e["to"], e["kind"]) for e in tl],
                         [("07-Combat-Action", "03-World-Area-Field", "hard")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
