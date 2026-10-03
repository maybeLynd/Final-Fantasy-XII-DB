"""narrowings_1003.py [--apply] - incorporate SWE2-AUDIT-SPEC's ACCEPT-WITH-NARROWING repairs (95d495604) into OPUS's
records (OPUS, 2026-10-03). Parses each review's "Replace:\n\n> OLD\n\nwith:\n\n> NEW" blocks (multi-line quotes kept,
"> " stripped) and applies OLD -> NEW to the record's spec.json `lead` or rows.json row texts, whichever holds OLD
exactly once. Without --apply it prints what it found and where OLD sits. Idempotent: a block whose NEW is already in
place is reported ALREADY."""
import io
import json
import os
import re
import sys

C = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates"
BLOCK = re.compile(r"Replace[^\n]*:\s*\n\s*\n((?:>[^\n]*\n?)+)\s*\n\s*with[^\n]*:\s*\n\s*\n((?:>[^\n]*\n?)+)", re.S)


def unquote(q):
    return "\n".join(l[2:] if l.startswith("> ") else l[1:] for l in q.strip("\n").split("\n"))


def targets(rec):
    """(kind, path, obj, getter/setter) for each text a narrowing may hit."""
    out = []
    sp = os.path.join(C, rec, "spec.json")
    if os.path.isfile(sp):
        s = json.load(io.open(sp, encoding="utf-8"))
        out.append(("spec.lead", sp, s, "lead"))
    rp = os.path.join(C, rec, "rows.json")
    if os.path.isfile(rp):
        d = json.load(io.open(rp, encoding="utf-8"))
        for r in d["rows"]:
            out.append(("row %s" % r["fn"], rp, d, r))
    return out


def main():
    apply = "--apply" in sys.argv
    changed = {}
    for rev in sorted(os.listdir(C)):
        if not rev.startswith("auditspec-review-opus-"):
            continue
        rp = os.path.join(C, rev, "REVIEW.md")
        if not os.path.isfile(rp):
            continue
        t = io.open(rp, encoding="utf-8").read().replace("\r\n", "\n")
        if "verdict: ACCEPT-WITH-NARROWING" not in t:
            continue
        rec = rev[len("auditspec-review-"):]
        for m in BLOCK.finditer(t):
            old, new = unquote(m.group(1)), unquote(m.group(2))
            hits = []
            for kind, path, obj, key in targets(rec):
                text = obj[key] if isinstance(key, str) else key["text"]
                if old in text or new in text:
                    hits.append((kind, path, obj, key, text))
            state = "NOT FOUND"
            if len(hits) == 1:
                kind, path, obj, key, text = hits[0]
                if new in text and old not in text:
                    state = "ALREADY (%s)" % kind
                elif text.count(old) == 1:
                    state = "APPLY (%s)" % kind
                    if apply:
                        text = text.replace(old, new)
                        if isinstance(key, str):
                            obj[key] = text
                        else:
                            key["text"] = text
                        changed[path] = obj
                        if path.endswith("rows.json"):
                            obj.setdefault("corrections", []).append(
                                {"fn": key["fn"], "why": "SWE2-AUDIT-SPEC narrowing (%s), incorporated verbatim" % rev})
                else:
                    state = "AMBIGUOUS"
            elif len(hits) > 1:
                state = "MULTIPLE (%s)" % ", ".join(h[0] for h in hits)
            print("%-62s %-24s %s" % (rec[:62], state, old[:70].replace("\n", " ")))
    if apply:
        for path, obj in changed.items():
            json.dump(obj, io.open(path, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
        print("written", len(changed), "file(s)")


if __name__ == "__main__":
    main()
