"""fix_members_1003.py VERIFY_JSON - apply a byte verifier's FIX entries to the opus-member-* records (OPUS, 2026-10-03).
VERIFY_JSON is {"records": {rec: [{"fn", "verdict", "problems", "old", "new"}]}}. Only records whose rows.json exists and
whose rows are not yet applied are touched (a published record needs strike-and-correct on its page instead, and is
listed). Each fix replaces one clause; the reason goes to rows.json 'corrections'. Idempotent like fix_reread_1003."""
import io
import json
import os
import sys

C = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates"


def main():
    v = json.load(io.open(sys.argv[1], encoding="utf-8"))["records"]
    for rec, items in sorted(v.items()):
        fixes = [x for x in items if x["verdict"] == "FIX" and x.get("old")]
        drops = [x["fn"] for x in items if x["verdict"] == "DROP"]
        p = os.path.join(C, rec, "rows.json")
        if not os.path.exists(p):
            print("SKIP %s: no rows.json" % rec)
            continue
        out = os.path.join(C, rec, "interior_applier.out")
        if os.path.exists(out) and "ALREADY" in io.open(out, encoding="utf-8", errors="replace").read().upper():
            print("PUBLISHED %s: %d fix(es) need strike-and-correct on the page, not here" % (rec, len(fixes)))
            continue
        d = json.load(io.open(p, encoding="utf-8"))
        rows = {r["fn"]: r for r in d["rows"]}
        done = []
        for x in fixes:
            r = rows[x["fn"]]
            if x["old"] in r["text"]:
                assert r["text"].count(x["old"]) == 1, (rec, x["fn"], x["old"])
                r["text"] = r["text"].replace(x["old"], x["new"])
                why = "; ".join(x["problems"]) or "same function, further clause"
                d.setdefault("corrections", []).append({"fn": x["fn"], "why": "byte verifier, re-read by OPUS: " + why})
                done.append(x["fn"])
            elif x["new"] not in r["text"]:
                print("WARN %s %s: neither the old nor the new clause is present" % (rec, x["fn"]))
        if drops:
            d["rows"] = [r for r in d["rows"] if r["fn"] not in drops]
            d.setdefault("skipped", []).extend({"fn": f, "why": "dropped by the byte verifier"} for f in drops)
        if done or drops:
            json.dump(d, io.open(p, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
        print(rec, "applied", done, "dropped", drops)


if __name__ == "__main__":
    main()
