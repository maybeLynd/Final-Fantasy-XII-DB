"""set_self_method.py REC... - record in rows.json that OPUS drafted the rows itself (session opus-self), so the README
states the method instead of a cloud/agent draft (OPUS, 2026-10-03). Re-run after any interior_ingest check, which
rewrites rows.json."""
import io
import json
import os
import sys

C = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "FFXII TZA",
                                  "_index", "candidates"))
METHOD = ("OPUS drafted these rows itself from its F-interior pack (`f_pack.py`: each function the page cites only at its "
          "entry, with its annotated listing) and checked every row mechanically with `interior_ingest.py` (every anchor an "
          "instruction boundary inside the extent with the recorded mnemonic; every address a listing token). No second "
          "agent drafted or verified them, so the non-author check is SWE2-AUDIT-SPEC's.")
for rec in sys.argv[1:]:
    p = os.path.join(C, rec.rstrip("/"), "rows.json")
    d = json.load(io.open(p, encoding="utf-8"))
    assert d.get("session") == "opus-self", (rec, d.get("session"))
    d["method"] = METHOD
    json.dump(d, io.open(p, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
    print(rec, "method set,", len(d["rows"]), "rows")
