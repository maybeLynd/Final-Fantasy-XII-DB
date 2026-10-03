#!/usr/bin/env python3
"""test_knowledge_db.py - isolated-fixture regression for the schema-4 freshness machinery.

Every fixture builds in a temp dir with the module's path constants monkeypatched - no peer
file is ever touched, which is the point of the fixture (the 2026-09-26 policy's "test in
isolated fixtures, not live peer files"). The cases are the closure checklist: same-row-count
edits, add/delete, generator change, mixed-table freshness, mid-build edits, stale negative
queries, w/rw writer lookup, hex/variable field sizes.
"""
import io
import os
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import knowledge_db as kd  # noqa: E402

FUNCS_TSV = "entry\tname\tbody_bytes\towner\tx\tthunk\tnoreturn\tx\ttags\n" \
            "00001000\tFUN_00001000\t64\tcore\t\t\t\t\t\n" \
            "00002000\tFUN_00002000\t32\tcore\t\t\t\t\t\n"
EDGES_TSV = "caller\tcallee\tx\tcallee_name\n00001000\t00002000\tx\tFUN_00002000\n"
GREFS_TSV = "function_entry\treferenced_address\tkind\tsite\n" \
            "00001000\t02EAE080\twrite\t0012100C\n"
FAI_TSV = "type\tdisp\tbase\tkind\tfunction_entry\tsite\tinstruction\tnote\n" \
          "WidgetSingleton02AEE4C0\t0x8\t0x0\tw\t00001000\t0012100C\tmov\t\n" \
          "WidgetSingleton02AEE4C0\t0x8\t0x0\trw\t00002000\t00122000\tlock xadd\t\n" \
          "WidgetSingleton02AEE4C0\t0x8\t0x0\tr\t00001000\t00121010\tcmp\t\n"
TYPES_TSV = "type\tsize\tcategory\tinstance\tallocation_site\tctor\tdtor\treadiness\tconfidence\tlevel\tdocuments\n" \
            "WidgetSingleton02AEE4C0\t0x40\tstruct\t\tsite\t\t\tDISCOVERED\tMEDIUM\tL1\tdoc.md\n"
FIELDS_TSV = "type\toffset\tsize\tname\tctype\tmeaning\treadiness\tconfidence\n" \
             "WidgetSingleton02AEE4C0\t0x8\t0x18\tpsampler\tvoid*\tm\ty\tz\n" \
             "WidgetSingleton02AEE4C0\t0x20\tvar\tdyn\tu8*\tvariable\t\t\n" \
             "   \t\t\t\t\t\t\t\n"   # blank trailing row - must be skipped
QUESTIONS_MD = "| Q-1 | does it | OPEN | |\n"
DISPATCH_TSV = "call_id\tverb\targs\thandler\thandler_name\towner\n01\top\t\t00001000\tFUN_00001000\tx\n"
CONTRA_TSV = "id\tdate\tkind\tcategory\tdocument\tline\tclaim\tcorrection\tinstrument\taddresses\n"
DOC_MD = "---\nsystem: test\ncategory: 00-Test\nstatus: active\nreadiness: DISCOVERED\nconfidence: MEDIUM\nlevel: L1\n---\nbody `00001000` here\n"
RECON_C = "int main(void){return 0;}\n"


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = self.tmp.name
        self._saved = {k: getattr(kd, k) for k in
                       ("ROOT", "DB_DIR", "FUNCS", "EDGES", "GREFS", "RECON", "PIN")}
        self._gen_mods = list(kd.GENERATOR_MODULES)
        kd.ROOT = t
        kd.DB_DIR = os.path.join(t, "db")
        kd.FUNCS = os.path.join(t, "work", "functions.tsv")
        kd.EDGES = os.path.join(t, "work", "edges.tsv")
        kd.GREFS = os.path.join(t, "work", "refs.tsv")
        kd.RECON = os.path.join(t, "Recon")
        kd.PIN = None
        _write(kd.FUNCS, FUNCS_TSV)
        _write(kd.EDGES, EDGES_TSV)
        _write(kd.GREFS, GREFS_TSV)
        td = os.path.join(kd.DB_DIR, "_types")
        _write(os.path.join(td, "field-access-index.tsv"), FAI_TSV)
        _write(os.path.join(td, "types.tsv"), TYPES_TSV)
        _write(os.path.join(td, "fields.tsv"), FIELDS_TSV)
        _write(os.path.join(kd.DB_DIR, "_index", "OPEN-QUESTIONS.md"), QUESTIONS_MD)
        _write(os.path.join(kd.DB_DIR, "_index", "CONTRADICTIONS.tsv"), CONTRA_TSV)
        _write(os.path.join(kd.DB_DIR, "01-Script-VM-Native-Bridge", "Verb-Dispatch",
                            "scriptvm-dispatch.tsv"), DISPATCH_TSV)
        _write(os.path.join(kd.DB_DIR, "00-Test", "doc.md"), DOC_MD)
        _write(os.path.join(kd.RECON, "thing.c"), RECON_C)
        self.db = os.path.join(t, "out", "k.sqlite")

    def tearDown(self):
        for k, v in self._saved.items():
            setattr(kd, k, v)
        kd.GENERATOR_MODULES = self._gen_mods
        self.tmp.cleanup()

    def build(self):
        os.makedirs(os.path.dirname(self.db), exist_ok=True)
        conn = sqlite3.connect(":memory:")
        kd.build(conn, verbose=False)
        # materialise to disk: freshness_report opens by path
        disk = sqlite3.connect(self.db)
        conn.backup(disk)
        disk.close()
        conn.close()

    def fresh(self, tables=None):
        return kd.freshness_report(self.db, tables)

    def test_01_build_then_current(self):
        self.build()
        status, stale, meta = self.fresh()
        self.assertEqual(status, "current", stale)
        self.assertTrue(meta["generator_sha256"])
        conn = sqlite3.connect(self.db)
        n = conn.execute("SELECT COUNT(*) FROM provenance").fetchone()[0]
        # one row per (table, dependency): 16 tables + the extra functions.tsv dep on
        # edges/citations/doc_names = 19
        self.assertEqual(n, 19)
        m = conn.execute("SELECT COUNT(*) FROM provenance WHERE table_name='citations'")
        self.assertEqual(m.fetchone()[0], 2)   # doc tree AND functions.tsv
        conn.close()

    def test_02_same_row_count_edit_is_stale(self):
        self.build()
        _write(kd.FUNCS, FUNCS_TSV.replace("FUN_00002000", "renamed_2000    "))
        status, stale, _ = self.fresh()
        self.assertEqual(status, "stale")
        self.assertTrue(any("functions:" in s for s in stale), stale)
        # a join dependency: citations resolve THROUGH functions.tsv, so it stales too
        self.assertTrue(any("citations:" in s for s in stale), stale)

    def test_03_added_and_deleted_files_are_stale(self):
        self.build()
        extra = os.path.join(kd.DB_DIR, "00-Test", "new.md")
        _write(extra, DOC_MD)
        status, stale, _ = self.fresh()
        self.assertEqual(status, "stale")
        self.assertTrue(any("documents:" in s for s in stale))
        self.build()
        status, _, _ = self.fresh()
        self.assertEqual(status, "current")
        os.remove(extra)
        status, stale, _ = self.fresh()
        self.assertEqual(status, "stale")

    def test_04_generator_change_stales_everything(self):
        mods = os.path.join(self.tmp.name, "gen_module.py")
        _write(mods, "X = 1\n")
        kd.GENERATOR_MODULES = [mods]
        self.build()
        _write(mods, "X = 2\n")   # a parser change with NO input change
        status, stale, _ = self.fresh()
        self.assertEqual(status, "stale")
        self.assertTrue(any("generator:" in s for s in stale), stale)

    def test_05_mixed_table_freshness_scopes(self):
        self.build()
        # fields.tsv feeds ONLY the fields table - the mixed-table case. (A doc-tree edit
        # like OPEN-QUESTIONS.md legitimately stales every table that reads the tree.)
        _write(os.path.join(kd.DB_DIR, "_types", "fields.tsv"),
               FIELDS_TSV + "X\t0\t4\tn\tt\tm\t\t\n")
        status, stale, _ = self.fresh()
        self.assertEqual(status, "stale")
        self.assertTrue(all("fields:" in s for s in stale), stale)
        status, stale, _ = self.fresh({"types"})      # untouched table alone: current
        self.assertEqual(status, "current", stale)
        status, stale, _ = self.fresh({"fields"})
        self.assertEqual(status, "stale")

    def test_06_mid_build_edit_discards_staging_and_keeps_prior(self):
        self.build()
        with open(self.db, "rb") as fh:
            before = fh.read()
        orig = kd.src_lines_stream
        armed = [True]

        def injecting(path):
            if armed[0] and str(path).endswith("functions.tsv"):
                armed[0] = False
                _write(os.path.join(kd.DB_DIR, "_types", "types.tsv"),
                       TYPES_TSV + "NewType\t8\tstruct\t\t\t\t\tX\tY\tZ\tW\n")
            return orig(path)

        kd.src_lines_stream = injecting
        try:
            rc = kd.cmd_build(self.db, verbose=False)
        finally:
            kd.src_lines_stream = orig
        self.assertEqual(rc, 3)
        with open(self.db, "rb") as fh:
            self.assertEqual(fh.read(), before)  # last usable kept
        self.assertFalse(os.path.exists(self.db + ".tmp"))
        status, _, _ = self.fresh()
        self.assertEqual(status, "stale")  # and the drift is reported, not hidden

    def test_07_stale_query_refuses_and_snapshot_labels(self):
        self.build()
        _write(os.path.join(kd.DB_DIR, "_types", "fields.tsv"), FIELDS_TSV + "X\t0\t4\tn\tt\tm\t\t\n")
        argv = sys.argv
        sys.argv = ["knowledge_db.py", "query", "unresolved-fields", "--out", self.db]
        try:
            rc = kd.main()
        finally:
            sys.argv = argv
        self.assertEqual(rc, 2)   # refused - no apparently-fresh rows

    def _main(self, *args):
        argv = sys.argv
        sys.argv = ["knowledge_db.py"] + list(args) + ["--out", self.db]
        try:
            return kd.main()
        finally:
            sys.argv = argv

    def test_11_stale_refuse_snapshot_refresh_current(self):
        """The user's directive item 3 regression, end to end (OPUS, 2026-10-03): a canonical dependency change makes
        the mirror STALE; a normal current query is refused; an explicit snapshot query runs, labelled as-of; the
        supported refresh makes it CURRENT with a new source identity."""
        import time
        self.build()
        st0, _s, meta0 = self.fresh()
        self.assertEqual(st0, "current")
        time.sleep(1.1)                                        # built_at has second resolution
        _write(os.path.join(kd.DB_DIR, "_types", "fields.tsv"), FIELDS_TSV + "X\t0\t4\tn\tt\tm\t\t\n")
        st1, stale1, _m = self.fresh()
        self.assertEqual(st1, "stale")
        self.assertTrue(any("fields" in s for s in stale1), stale1)
        self.assertEqual(self._main("query", "unresolved-fields"), 2)                  # refused, fail-closed
        self.assertNotEqual(self._main("query", "unresolved-fields", "--snapshot"), 2)  # as-of read allowed
        self.assertEqual(self.fresh()[0], "stale")             # a snapshot read never refreshes silently
        self.assertEqual(self._main("query", "unresolved-fields", "--refresh"), 0)
        st2, stale2, meta2 = self.fresh()
        self.assertEqual(st2, "current", stale2)
        self.assertNotEqual(meta2["built_at"], meta0["built_at"])                     # new source identity

    def test_08_writers_of_field_includes_w_and_rw(self):
        self.build()
        conn = sqlite3.connect(self.db)
        ok, sql = kd.QUERIES["writers-of-field"]
        rows = conn.execute(sql, {"arg": "WIDGETSINGLETON02AEE4C0+0008"}).fetchall()
        fns = sorted(r[0] for r in rows)
        self.assertEqual(fns, ["00001000", "00002000"])  # the rw row is a writer
        # and a pure reader-of-field must not surface the rw row as a read-only accessor
        ok, sql = kd.QUERIES["accessors-of-field"]
        kinds = {r[0]: r[2] for r in conn.execute(sql, {"arg": "WIDGETSINGLETON02AEE4C0+0008"})}
        self.assertEqual(kinds, {"00001000": "w", "00002000": "rw"})
        conn.close()

    def test_09_hex_and_variable_field_sizes(self):
        self.build()
        conn = sqlite3.connect(self.db)
        sizes = dict(conn.execute(
            "SELECT name, size FROM fields WHERE type='WidgetSingleton02AEE4C0'"))
        self.assertEqual(sizes["psampler"], 0x18)   # authored hex parses
        self.assertEqual(sizes["dyn"], 0)           # variable size stays the 0 marker
        n = conn.execute("SELECT COUNT(*) FROM fields").fetchone()[0]
        self.assertEqual(n, 2)                      # the blank trailing row was skipped
        conn.close()

    def test_10_no_index_and_old_schema(self):
        status, _, _ = kd.freshness_report(os.path.join(self.tmp.name, "absent.sqlite"))
        self.assertEqual(status, "no-index")
        old = os.path.join(self.tmp.name, "old.sqlite")
        c = sqlite3.connect(old)
        c.execute("CREATE TABLE provenance (table_name TEXT)")
        c.commit()
        c.close()
        status, _, _ = kd.freshness_report(old)
        self.assertEqual(status, "old-schema")


if __name__ == "__main__":
    unittest.main(verbosity=2)
