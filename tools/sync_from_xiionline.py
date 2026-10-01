"""sync_from_xiionline.py [--apply] - refresh this repo's snapshot of the FF12 knowledge database from the COMMITTED
state (HEAD) of the working checkout (C:/Users/Kristian/source/repos/XIIOnline, folder Database/), text only.

This repo is a READ-ONLY SNAPSHOT for cloud sessions and backup. The database is authored in XIIOnline; never edit the
snapshot here. Rules:
  - committed content only: file bytes come from XIIOnline's HEAD blobs, never the working tree, so another lane's
    uncommitted edits are never published (corrected 2026-10-01, OPUS: the first version copied the working tree);
  - only files in Database/FFXII TZA/ and Database/Tools/, minus Tools/work (gitignored game executable, extracted
    data, scratch);
  - only text extensions (TEXT below), and never a file containing a NUL byte;
  - never game data or binaries: images, archives, .bin/.fst/.ebp/.phyre/.vbf/.st2e and other extracted formats,
    objects, compiled bytecode, the generated knowledge.sqlite;
  - not the live team board (_index/_inbox/TEAM.json), which changes every minute;
  - no file over 95 MB (GitHub's limit is 100 MB);
  - repo-owned paths (KEEP) are never touched.
Without --apply it prints what would change. With --apply it writes the changed files, deletes vanished ones, and
prints the summary plus `SOURCE <commit>` for the commit message. Committing and pushing stay manual (see
docs/REPO_MANAGEMENT.md).
"""
import os, subprocess, sys

REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
PREFIX = "Database/"
DST = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOTS = ("FFXII TZA/", "Tools/")
TEXT = {".md", ".json", ".jsonl", ".py", ".tsv", ".txt", ".out", ".stderr", ".stdout", ".err", ".log", ".bat", ".cmd",
        ".ps1", ".sh", ".c", ".h", ".asm", ".java", ".patch", ".diff", ".html", ".ini", ".sha256", ".ids", ".source",
        ".md-before-correction", ".py-before-correction", ""}
EXCLUDE = {"FFXII TZA/_index/_inbox/TEAM.json", "FFXII TZA/_index/knowledge.sqlite"}
MAX = 95 * 2 ** 20
# repo-owned paths the mirror never touches: docs (cloud program, task log, repo management), cloud-input
# (OPUS-generated packs for cloud sessions), cloud-reports (returned reports, archived after ingestion)
KEEP = {".git", "tools", "docs", "cloud-input", "cloud-reports", "README.md", ".gitignore", ".gitattributes"}


def tree(repo, rev, prefix=""):
    """{path relative to prefix: (blob id, size)} for regular files under prefix at rev."""
    out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-l", "-z", "--full-tree", rev] + ([prefix] if prefix else []),
                         capture_output=True, check=True).stdout.decode("utf-8")
    res = {}
    for rec in out.split("\0"):
        if not rec:
            continue
        meta, path = rec.split("\t", 1)
        mode, kind, sha, size = meta.split()
        if kind != "blob" or mode == "120000":
            continue
        res[path[len(prefix):]] = (sha, int(size))
    return res


def blobs(repo, shas):
    """{sha: bytes} read through one git cat-file --batch process."""
    p = subprocess.Popen(["git", "-C", repo, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    res = {}
    for s in shas:
        p.stdin.write((s + "\n").encode()); p.stdin.flush()
        hdr = p.stdout.readline().split()
        n = int(hdr[2])
        res[s] = p.stdout.read(n); p.stdout.read(1)
    p.stdin.close(); p.wait()
    return res


def main():
    apply = "--apply" in sys.argv
    src_rev = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    src = tree(REPO, "HEAD", PREFIX)
    refused, want = [], {}
    for f, (sha, size) in src.items():
        if not f.startswith(ROOTS) or f.startswith("Tools/work/") or f in EXCLUDE:
            continue
        if os.path.splitext(f)[1].lower() not in TEXT:
            refused.append((f, "type")); continue
        if size > MAX:
            refused.append((f, "size")); continue
        want[f] = sha
    have = {}
    try:
        have = tree(DST, "HEAD")
    except subprocess.CalledProcessError:
        pass
    have = {f: v[0] for f, v in have.items() if f.split("/", 1)[0] not in KEEP and f not in KEEP}
    todo = [f for f, sha in want.items() if have.get(f) != sha or not os.path.isfile(os.path.join(DST, f))]
    data = blobs(REPO, sorted({want[f] for f in todo}))
    add = changed = 0
    for f in todo:
        b = data[want[f]]
        if b"\0" in b:
            refused.append((f, "binary")); del want[f]; continue
        d = os.path.join(DST, f)
        if os.path.isfile(d) and open(d, "rb").read() == b:
            continue
        if f in have:
            changed += 1
        else:
            add += 1
        if apply:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            open(d, "wb").write(b)
    # a file already in the snapshot that was refused as binary this time must also go
    gone = sorted(f for f in have if f not in want)
    if apply:
        for g in gone:
            p = os.path.join(DST, g)
            if os.path.exists(p):
                os.remove(p)
    by = {}
    for f, why in refused:
        by[why] = by.get(why, 0) + 1
    print("allowed %d files; add %d, update %d, delete %d; refused %s" % (len(want), add, changed, len(gone), by))
    print("SOURCE %s" % src_rev)
    print("APPLIED" if apply else "dry run (use --apply)")


if __name__ == "__main__":
    main()
