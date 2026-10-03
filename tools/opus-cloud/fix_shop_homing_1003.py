"""OPUS's re-read corrections to the drafted shop-screens homing rows (opus-the-shop-screens-homing-1003), 2026-10-03.
Idempotent: an entry whose OLD text is gone is skipped."""
import io
import json
import os

P = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\opus-the-shop-screens-homing-1003\rows.json"
FIXES = [
    ("002CCA40", "passes its dword `+4` to `0020E600` and walks that many words of the returned array at stride 2",
     "passes its dword `+4` to `0020E600` and walks the array `0020E600` returns, one word per step, for as many "
     "steps as `00252FA0` counted",
     "the loop bound is 00252FA0's count (ebp, 002CCA5A/002CCAD3), not the dword +4 passed to 0020E600"),
    ("003FD1D0", "and `003FCFE0` at that object's qword `+0x120`",
     "and `003FCFE0` at qword `+0x120` of the object that qword points to",
     "003FD27D loads rax = qword +0x18 and 003FD28F stores to [rax+0x120]: the object written is the one qword +0x18 "
     "points to, not the object at qword +0x20"),
]
d = json.load(io.open(P, encoding="utf-8"))
rows = {r["fn"]: r for r in d["rows"]}
done = []
for fn, old, new, why in FIXES:
    r = rows[fn]
    if old in r["text"]:
        assert r["text"].count(old) == 1, (fn, old)
        r["text"] = r["text"].replace(old, new)
        d.setdefault("corrections", []).append({"fn": fn, "why": "OPUS re-read: " + why})
        done.append(fn)
    elif new not in r["text"]:
        print("WARN %s: neither the old nor the new clause is present" % fn)
if done:
    json.dump(d, io.open(P, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
print("applied", done)
