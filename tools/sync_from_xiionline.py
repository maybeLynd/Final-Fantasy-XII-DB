"""sync_from_xiionline.py [--apply] - refresh this repo's snapshot of the FF12 knowledge database from the working
checkout (C:/Users/Kristian/source/repos/XIIOnline/Database), text only.

This repo is a READ-ONLY SNAPSHOT for cloud sessions and backup. The database is authored in XIIOnline; never edit the
snapshot here. Rules:
  - only files git tracks in XIIOnline/Database, minus Tools/work (gitignored game executable, extracted data, scratch);
  - only text extensions (TEXT below), and never a file containing a NUL byte;
  - never game data or binaries: images, archives, .bin/.fst/.ebp/.phyre/.vbf/.st2e and other extracted formats,
    objects, compiled bytecode, the generated knowledge.sqlite;
  - not the live team board (_index/_inbox/TEAM.json), which changes every minute;
  - no file over 95 MB (GitHub's limit is 100 MB).
Without --apply it prints what would change. With --apply it mirrors the allowed files into this repo (adding, updating
and deleting snapshot files) and prints a summary. Committing and pushing stay manual.
"""
import os, shutil, subprocess, sys

SRC = r"C:\Users\Kristian\source\repos\XIIOnline\Database"
DST = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOTS = ("FFXII TZA/", "Tools/")
TEXT = {".md", ".json", ".jsonl", ".py", ".tsv", ".txt", ".out", ".stderr", ".stdout", ".err", ".log", ".bat", ".cmd",
        ".ps1", ".sh", ".c", ".h", ".asm", ".java", ".patch", ".diff", ".html", ".ini", ".sha256", ".ids", ".source",
        ".md-before-correction", ".py-before-correction", ""}
EXCLUDE = {"FFXII TZA/_index/_inbox/TEAM.json", "FFXII TZA/_index/knowledge.sqlite"}
MAX = 95 * 2 ** 20
KEEP = {".git", "tools", "README.md", ".gitignore", ".gitattributes"}


def allowed():
    files = subprocess.run(["git", "-C", SRC, "ls-files", "-z"], capture_output=True).stdout.decode("utf-8").split("\0")
    out, refused = [], []
    for f in files:
        if not f or not f.startswith(ROOTS) or f.startswith("Tools/work/") or f in EXCLUDE:
            continue
        ext = os.path.splitext(f)[1].lower()
        p = os.path.join(SRC, f)
        if ext not in TEXT or not os.path.isfile(p):
            refused.append((f, "type")); continue
        if os.path.getsize(p) > MAX:
            refused.append((f, "size")); continue
        with open(p, "rb") as fh:
            if b"\0" in fh.read():
                refused.append((f, "binary")); continue
        out.append(f)
    return out, refused


def main():
    apply = "--apply" in sys.argv
    files, refused = allowed()
    want = set(files)
    have = set()
    for root, dirs, fs in os.walk(DST):
        rel_root = os.path.relpath(root, DST).replace("\\", "/")
        if rel_root == "." :
            dirs[:] = [d for d in dirs if d not in KEEP]
            continue
        for f in fs:
            have.add((rel_root + "/" + f) if rel_root != "." else f)
    add = changed = 0
    for f in files:
        s, d = os.path.join(SRC, f), os.path.join(DST, f)
        if not os.path.exists(d):
            add += 1
        elif os.path.getsize(s) != os.path.getsize(d) or open(s, "rb").read() != open(d, "rb").read():
            changed += 1
        else:
            continue
        if apply:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copyfile(s, d)
    gone = sorted(h for h in have if h not in want)
    if apply:
        for g in gone:
            os.remove(os.path.join(DST, g))
    by = {}
    for f, why in refused:
        by[why] = by.get(why, 0) + 1
    print("allowed %d files (%.1f MB); add %d, update %d, delete %d; refused %s" % (
        len(files), sum(os.path.getsize(os.path.join(SRC, f)) for f in files) / 2 ** 20, add, changed, len(gone), by))
    print("APPLIED" if apply else "dry run (use --apply)")


if __name__ == "__main__":
    main()
