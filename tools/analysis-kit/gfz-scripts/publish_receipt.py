"""publish_receipt.py - read a publish_paths.sh delivery outcome without trusting a caller's captured stdout.

publish_paths.sh appends to $PUBLISH_RECEIPT (when set) as it goes, flushing each line to disk before the next step:
    committed sha: <40 hex>      written right after the compare-and-swap update-ref succeeded
    refresh: ok | deferred       the post-commit index refresh
    exit: <code>                 the script's own final status
so a controller killed mid-run (ASTRA-REQ-FRONTIER-UQ147-INTERRUPTED-PUBLISH-1003: the runner captured stdout in RAM
and was killed at its timeout after the commit) still leaves the publisher's own record on disk.

    python publish_receipt.py classify RECEIPT [--sha SHA]
        COMPLETE            committed + refresh ok + exit 0
        COMMITTED-INCOMPLETE committed line present, no terminal exit line (interrupted after commit) - NOT a success;
                            the caller verifies the sha/blobs, re-runs only the index refresh, never the commit
        REFRESH-DEFERRED    committed + exit 4
        NOT-COMMITTED       no committed line (refused or killed before the update-ref)
    python publish_receipt.py reflog SHA
        REFLOG-ATTESTED     git's HEAD reflog records `publish_paths.sh` writing exactly SHA (update-ref -m) - proof the
                            publisher's own compare-and-swap wrote the object; says NOTHING about its exit or refresh.
                            A recovery label for runs that predate the receipt; never reported as recovered stdout.
        NOT-ATTESTED        no such reflog entry
    python publish_receipt.py --self-test
"""
import os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))


def classify(text, sha=None):
    committed = re.findall(r"^committed sha: ([0-9a-f]{40})$", text, re.M)
    exits = re.findall(r"^exit: (\d+)$", text, re.M)
    refresh = re.findall(r"^refresh: (\w+)$", text, re.M)
    if not committed:
        return "NOT-COMMITTED"
    if sha and committed[-1] != sha and not committed[-1].startswith(sha):
        return "NOT-COMMITTED"  # the receipt names a different object
    if not exits:
        return "COMMITTED-INCOMPLETE"
    if exits[-1] == "0" and refresh and refresh[-1] == "ok":
        return "COMPLETE"
    if exits[-1] == "4":
        return "REFRESH-DEFERRED"
    return "COMMITTED-INCOMPLETE"


def reflog(sha, root=ROOT):
    r = subprocess.run(["git", "-C", root, "reflog", "--format=%H %gs", "-n", "2000", "HEAD"], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        h, _, msg = line.partition(" ")
        if (h == sha or h.startswith(sha)) and msg.strip() == "publish_paths.sh":
            return "REFLOG-ATTESTED"
    return "NOT-ATTESTED"


def _self_test():
    fails = []

    def ok(c, m):
        print(("ok   " if c else "FAIL ") + m)
        if not c:
            fails.append(m)

    s = "a" * 40
    ok(classify("committed sha: %s\nrefresh: ok\nexit: 0\n" % s) == "COMPLETE", "C1 full receipt is COMPLETE")
    # the interrupted-after-commit control: the commit landed, the run never reached its terminal line
    ok(classify("committed sha: %s\n" % s) == "COMMITTED-INCOMPLETE", "C2 interrupted after commit is NOT a success")
    ok(classify("committed sha: %s\nrefresh: deferred\nexit: 4\n" % s) == "REFRESH-DEFERRED", "C3 deferred refresh")
    ok(classify("") == "NOT-COMMITTED", "C4 empty receipt (refused or killed before update-ref)")
    ok(classify("committed sha: %s\nrefresh: ok\nexit: 0\n" % s, sha="b" * 40) == "NOT-COMMITTED", "C5 a receipt for another object")
    ok(classify("exit: 0\n") == "NOT-COMMITTED", "C6 an exit line without a committed line never reads as delivered")
    # the reflog check is sensitive: a sha that HEAD never held is NOT-ATTESTED
    ok(reflog("0" * 40) == "NOT-ATTESTED", "C7 reflog: an unknown object is not attested")
    print("self-test: %d failure(s)" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--self-test":
        sys.exit(_self_test())
    if a[0] == "classify":
        sha = a[a.index("--sha") + 1] if "--sha" in a else None
        print(classify(open(a[1], encoding="utf-8").read() if os.path.exists(a[1]) else "", sha))
    elif a[0] == "reflog":
        print(reflog(a[1]))
