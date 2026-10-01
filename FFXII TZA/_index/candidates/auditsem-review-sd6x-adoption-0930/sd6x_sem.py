"""SWE2-AUDIT-SEM independent check of 583b096f7 (SWE2-DATA: SD-60..SD-67 restatements adopted,
duplicate SD-160..SD-169 rows dropped).

Reads git objects only (never the producer's orphan_tokens.py):
  D1  the dedupe removed exactly one copy of each SD-160..SD-169 and nothing else in the register
  D2  the kept copy is the FIRST copy committed at 4415dba48, byte-identical
  D3  per id: backticked tokens / hex addresses of the dropped copy that the kept copy lacks, and
      whether each still appears on the page the row cites (HEAD) - reported, and unique question
      wording on the dropped copy that the cited page asks (the SD-165 case) is flagged
  D4  EOF: the register ended with a newline before 583b096f7 and has none after it (finding C2)
  R1  each restated SD-60..SD-67 row cites the OPUS commit named in the record, the commit exists
      and touched a record folder named by the row
  R2  the batch-2 review narrowings (auditsem-review-dd-owner-read-2-0930 section 3) appear in
      the restated rows: SD-60 01FD3620/006CAF40/Z bounds; SD-61 +0x18 key BL-5 and the 70-site
      clause; SD-62 registry; SD-66 02CF8580 class descriptor; SD-67 414a737fd section 20
  R3  each restated row's status word equals its OPUS record's own verdict word
  C1  control: a token removed from a kept row is detected by the D3 machinery

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-sd6x-adoption-0930/sd6x_sem.py"
"""
import re
import subprocess
import sys

DB = "Database/FFXII TZA"
OQ = DB + "/_index/OPEN-QUESTIONS.md"
FAILS = []
NOTES = []


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, check=True).stdout.decode("utf-8")


def show(rev, path):
    return git("show", f"{rev}:{path}")


def rows(text, pat):
    out = []
    for ln in text.splitlines():
        m = re.match(r"^\| (SD-\d+) \|", ln)
        if m and re.fullmatch(pat, m.group(1)):
            out.append((m.group(1), ln))
    return out


def toks(s):
    t = set(re.findall(r"`([^`]+)`", s))
    t |= set(re.findall(r"\b[0-9A-F]{8}\b", s))
    return t


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


pre = show("583b096f7^", OQ)
post = show("583b096f7", OQ)
b4 = show("4415dba48", OQ)

# D1 / D2
pre16 = rows(pre, r"SD-16\d")
post16 = rows(post, r"SD-16\d")
b416 = rows(b4, r"SD-16\d")
check("D1 pre has 20 SD-16x rows, post has 10", len(pre16) == 20 and len(post16) == 10,
      f"pre={len(pre16)} post={len(post16)}")
first = pre16[:10]
second = pre16[10:]
check("D2 kept copy == first copy at 4415dba48 (byte-identical)",
      [l for _, l in post16] == [l for _, l in b416[:10]] == [l for _, l in first])
pre_lines = pre.splitlines()
post_lines = post.splitlines()
removed = [l for l in pre_lines if l not in post_lines]
added = [l for l in post_lines if l not in pre_lines]
sd6x_ids = {f"SD-6{i}" for i in range(8)}
other_removed = [l for l in removed if not (l.startswith("| SD-16") or any(l.startswith(f"| {i} ") for i in sd6x_ids))]
other_added = [l for l in added if not any(l.startswith(f"| {i} ") for i in sd6x_ids)]
check("D1 nothing but SD-60..67 and the second SD-16x copy changed", not other_removed and not other_added,
      f"other_removed={len(other_removed)} other_added={len(other_added)}")

# D3 unique content on the dropped copy
PAGES = {
    "steam": DB + "/20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md",
    "mem": DB + "/24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md",
}
page_text = {k: show("HEAD", v) for k, v in PAGES.items()}
lost_total = 0
for (i1, keep), (i2, drop) in zip(first, second):
    assert i1 == i2
    pg = page_text["steam"] if "steam-integration" in drop else page_text["mem"]
    uniq = sorted(toks(drop) - toks(keep))
    uniq = [u for u in uniq if not u.endswith(".md")]
    onpage = [u for u in uniq if u in pg]
    lost = [u for u in uniq if u not in pg]
    lost_total += len(lost)
    print(f"INFO D3 {i1}: dropped-copy-only tokens {len(uniq)}; on cited page {len(onpage)}; nowhere on page {lost}")

# the SD-165 question: the page asks the dropped copy's question
k165 = dict(first)["SD-165"]
d165 = dict(second)["SD-165"]
q_drop = "player-visible message, fallback or crash"
check("D3 SD-165: dropped copy asked the player-visible question", q_drop in d165)
check("D3 SD-165: kept copy does not ask it", q_drop not in k165)
page165 = [l for l in page_text["mem"].splitlines() if "SD-165" in l and q_drop in l]
check("D3 SD-165: the page line citing SD-165 still asks the dropped question (narrowing N1)", len(page165) == 1)

# D4 EOF newline
check("D4 register ended with a newline before 583b096f7", pre.endswith("\n"))
check("D4 finding (correction C2): the register has no trailing newline after 583b096f7", not post.endswith("\n"))

# R1 / R2 / R3
recs = {
    "SD-60": ("5f7bd30da", "sd60-gibegineff-blocks-0930"),
    "SD-61": ("73e6ff01f", "sd61-pannotation-fields-0930"),
    "SD-62": ("e2777d3c8", "sd62-static-array-elements-0930"),
    "SD-63": ("ce6a553b2", "sd63-scene-parameter-layout-0930"),
    "SD-64": ("02d334dbe", "sd64-file-only-names-0930"),
    "SD-65": ("49f9a523b", "sd65-dynamic-class-route-0930"),
    "SD-66": ("ba2580021", "sd66-attach-slot-writers-0930"),
    "SD-67": ("aac0f6798", "sd67-stream-bindings-type-0930"),
}
post6 = dict(rows(post, r"SD-6[0-7]"))
for sid, (c, folder) in recs.items():
    r = post6[sid]
    files = git("show", "--name-only", "--format=", c)
    check(f"R1 {sid} cites {c} and record {folder}; commit touched it",
          c in r and folder in r and folder in files)
    readme = show("HEAD", f"{DB}/_index/candidates/{folder}/README.md")
    head = "\n".join(readme.splitlines()[:40])
    rec_word = "PARTIAL" if re.search(r"\bPARTIAL\b|narrowed|identified", head, re.I) and sid == "SD-62" else "ANSWERED"
    row_word = re.search(r"\*\*(ANSWERED|PARTIAL|OPEN)", r.split("|")[3]).group(1)
    check(f"R3 {sid} status {row_word} matches record", row_word == rec_word, f"record~{rec_word}")

need = {
    "SD-60": ["01FD3620", "006CAF40", "Z clamp", "0020EA50", "00210230"],
    "SD-61": ["BL-5", "70 sites", "WriteMask"],
    "SD-62": ["registries", "atexit"],
    "SD-66": ["02CF8580", "class descriptor", "2026-09-14"],
    "SD-67": ["414a737fd", "§20", "005E6860"],
}
for sid, ws in need.items():
    miss = [w for w in ws if w not in post6[sid]]
    check(f"R2 {sid} carries the batch-2 narrowing", not miss, f"missing={miss}")

# C1 control
fake_keep = k165.replace("`0036BFE0`", "")
check("C1 control: removing a token from a kept row is detected",
      "0036BFE0" in (toks(d165 + " `0036BFE0`") - toks(fake_keep)))

# B: byte spot-checks of facts the restated rows assert (certified image through retool.py; not the OPUS checkers)
RT = ["python", "-B", "Database/Tools/analysis-kit/gfz-scripts/retool.py"]


def rt(*a):
    return subprocess.run(RT + list(a), capture_output=True, check=True).stdout.decode("utf-8", "replace")


d = rt("dis", "006CAF40", "--n", "40")
stores = re.findall(r"mov\s+dword ptr \[rcx \+ (0x[0-9a-f]+)\], eax", d)
check("B1 SD-60: 006CAF40 copies 16 dwords to renderer +0x10..+0x4C and sets byte +0x208F3 = 1",
      stores == [hex(0x10 + 4 * k) for k in range(16)] and "byte ptr [rcx + 0x208f3], 1" in d)
d = rt("dis", "0039D1D0", "--n", "3")
check("B2 SD-60: the first resolver 0039D1D0 is lea rax,[02AEEB20]; ret", "-> 02AEEB20" in d.splitlines()[0] and "ret" in d.splitlines()[1])
d = rt("site", "005B4FE3", "--before", "8", "--after", "2")
check("B3 SD-61: first site forms r8 (type), r9d = 0, rdx = 02CF8570 (key) within the 12 before the call",
      "mov      r8, rax" in d and "xor      r9d, r9d" in d and "-> 02CF8570" in d)
d = rt("site", "005E6860", "--before", "16", "--after", "1")
check("B4 SD-67: 005E6860 -> 00632A10 with offset 0x38, kind 4, element size 8",
      "call     0x632a10" in d and "[rsp + 0x20], 0x38" in d and "[rsp + 0x30], 4" in d and "[rsp + 0x38], 8" in d)

print("INFO dropped-copy tokens absent from the cited page:", lost_total)
print("FAILS", len(FAILS))
sys.exit(1 if FAILS else 0)
