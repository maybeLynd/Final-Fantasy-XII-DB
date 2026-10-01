"""evidence_scan.py - the evidence view's captured inputs that live in directories, not files (OPUS, 2026-09-29).

  receipts   every seal.py receipt (a directory holding RECEIPT.json) under the database: verify() and publishable() from
             seal.py itself, so the dashboard counts exactly what the publication gate would accept
  pending    documents with a live "PENDING PROPAGATION" marker (a line that is not struck through with ~~ ~~): a routed
             correction that has not reached every consumer yet

    python evidence_scan.py --db <FFXII TZA> --out <json>
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "analysis-kit", "gfz-scripts"))
SKIP = {".git", "__pycache__", "node_modules"}


def scan(db):
    import seal as SL
    receipts, pending = [], []
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        if "RECEIPT.json" in files:
            store, rid = os.path.dirname(root), os.path.basename(root)
            try:
                v, p = SL.verify(store, rid), SL.publishable(store, rid)
            except Exception as e:          # a receipt the gate cannot even read is a problem, never a silent pass
                v, p = ["unreadable: %s" % e], ["unreadable"]
            receipts.append({"store": os.path.relpath(store, db).replace(os.sep, "/"), "run_id": rid, "intact": not v,
                             "publishable": not p, "problems": (v + p)[:3]})
            dirs[:] = []
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            if "PENDING PROPAGATION" not in text:
                continue
            live = [l for l in text.splitlines() if "PENDING PROPAGATION" in l
                    and not re.search(r"~~[^~]*PENDING PROPAGATION[^~]*~~", l)]
            if live:
                pending.append({"doc": os.path.relpath(path, db).replace(os.sep, "/"), "lines": len(live)})
    return {"receipts": sorted(receipts, key=lambda r: (r["store"], r["run_id"])), "pending": sorted(pending, key=lambda r: r["doc"])}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        r = scan(a.db)
    except Exception as e:
        r = {"failed": "%s: %s" % (type(e).__name__, e)}
    tmp = a.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(r, f)
    os.replace(tmp, a.out)
    print(r.get("failed") or "receipts %d, pending %d" % (len(r["receipts"]), len(r["pending"])))
    return 1 if "failed" in r else 0


if __name__ == "__main__":
    sys.exit(main())
