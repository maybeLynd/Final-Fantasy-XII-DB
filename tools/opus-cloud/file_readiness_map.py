"""file_readiness_map.py - file a verified readiness map in the RE repo docs/readiness/ (OPUS, 2026-10-02).

  python -B file_readiness_map.py --name 05-spawn --report <map.md> [--verdicts <verdicts.md> ...]
         --header <header.txt> --row "<README table row>" [--commit-msg "..."] [--push]

Writes docs/readiness/<name>.md = the report's title line, the OPUS verification header (a blockquote, from
--header), the report body, then each verdicts file as an appendix (its first '# ' title becomes
'## Appendix (OPUS, 2026-10-02): ...'). Appends --row to docs/readiness/README.md unless a row for the system is
already there. With --push, commits as maybeLynd <> (no trailer) and pushes. Prints the RE commit.
"""
import argparse
import os
import subprocess

RE = r"C:\Users\Kristian\source\repos\Final-Fantasy-XII-RE"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--verdicts", nargs="*", default=[])
    ap.add_argument("--header", required=True)
    ap.add_argument("--row", required=True)
    ap.add_argument("--commit-msg")
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()
    t = open(a.report, encoding="utf-8").read()
    first, rest = t.split("\n", 1)
    hdr = open(a.header, encoding="utf-8").read().strip("\n")
    hdr = "\n".join(l if l.startswith(">") else "> " + l for l in hdr.split("\n"))
    out = first + "\n\n" + hdr + "\n" + rest.rstrip("\n") + "\n"
    for v in a.verdicts:
        vt = open(v, encoding="utf-8").read()
        lines = vt.split("\n")
        if lines and lines[0].startswith("# "):
            lines[0] = "## Appendix (OPUS, 2026-10-02): " + lines[0][2:]
        else:
            lines.insert(0, "## Appendix (OPUS, 2026-10-02): byte verdicts")
        out += "\n" + "\n".join(lines).rstrip("\n") + "\n"
    dst = os.path.join(RE, "docs", "readiness", a.name + ".md")
    open(dst, "w", encoding="utf-8", newline="\n").write(out)
    readme = os.path.join(RE, "docs", "readiness", "README.md")
    r = open(readme, encoding="utf-8").read().rstrip("\n")
    system = a.row.split("|")[1].strip()
    if ("| " + system + " |") not in r:
        r += "\n" + a.row.strip() + "\n"
        open(readme, "w", encoding="utf-8", newline="\n").write(r)
    print("WROTE", dst)
    if a.push:
        g = ["git", "-C", RE]
        subprocess.run(g + ["add", "docs/readiness/" + a.name + ".md", "docs/readiness/README.md"], check=True)
        subprocess.run(g + ["-c", "user.name=maybeLynd", "-c", "user.email=", "commit", "-q", "-m",
                            a.commit_msg or ("docs/readiness: " + a.name + " map with OPUS's byte verdicts")], check=True)
        subprocess.run(g + ["push", "-q", "origin", "HEAD"], check=True)
        print("RE", subprocess.run(g + ["log", "-1", "--format=%h"], capture_output=True, text=True).stdout.strip())


if __name__ == "__main__":
    main()
