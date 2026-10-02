"""b21_checks.py - DD batch 21 pins (SWE2-CONTRACT, 2026-10-02).

Batch 21 is status-line currency only: the 13 pages that stay PARTIAL do so on
registered live register rows, and 8 carried a bare `status: PARTIAL` that named
none of them (efx-and-efb named its resolved residue but not SD-194).

Z1  each touched page's status line now names every live id documented_rule.py
    reports for that page.
Z2  the status lines carry the batch-21 stamp.
Z3  no register row was edited (the diff is status lines only) - checked by the
    publish diff, asserted here as page line counts equal HEAD's.
Z4  the batch commit's diff is exactly the status line per page (numstat 1/1 at
    the pinned commit - pinned because the batch is published; a working-tree
    diff is empty once committed, AUDITSPEC-REQ-CONTRACT-DDRES-B21-Z4-CONTROL-1002).
"""
import io, os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
DBP = "Database/FFXII TZA/"
BATCH_COMMIT = "85718f321bd5c81f8de7e1ef64ef2811f6500d8d"

PAGES = {
 "00-Engine-Core-Runtime/the-query-record-from-initialization-to-reuse.md": ["OV-8"],
 "01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md": ["OV-10"],
 "01-Script-VM-Native-Bridge/Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md": ["OV-16"],
 "02-Resource-And-Asset-Pipeline/the-external-source-owner-and-borrowed-view-lifetime.md": ["OV-19", "OV-21"],
 "02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md": ["OV-21", "OV-33", "OV-42"],
 "02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md": ["OV-42"],
 "02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md": ["OV-42"],
 "16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md": ["OV-29"],
 "17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md": ["SD-194"],
}

fails = []
for rel, ids in PAGES.items():
    t = io.open(os.path.join(ROOT, rel), encoding="utf-8", newline="").read()
    status = next((l for l in t.splitlines() if l.startswith("status:")), "")
    for i in ids:
        if i not in status:
            fails.append("Z1 %s: status line does not name %s" % (rel, i))
    if "DD batch 21" not in status:
        fails.append("Z2 %s: no batch stamp" % rel)
    head = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + DBP + rel.replace(os.sep, "/")],
                          capture_output=True).stdout
    if not head:
        fails.append("Z3 %s: HEAD blob unreadable" % rel); continue
    if t.replace("\r\n", "\n").count("\n") != head.decode("utf-8", "replace").replace("\r\n", "\n").count("\n"):
        fails.append("Z3 %s: line count changed vs HEAD (status lines are same-line edits)" % rel)
    ns = subprocess.run(["git", "-C", REPO, "show", "--numstat", "--format=", BATCH_COMMIT,
                         "--", DBP + rel.replace(os.sep, "/")],
                        capture_output=True, text=True).stdout.split()
    if ns[:2] != ["1", "1"]:
        fails.append("Z4 %s: batch-commit diff is %s, expected 1/1 (the status line only)" % (rel, ns[:2]))

if fails:
    print("\n".join(fails)); print("FAILS", len(fails)); sys.exit(1)
print("Z1-Z4 pass:", len(PAGES), "pages; FAILS 0")
