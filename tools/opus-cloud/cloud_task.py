"""cloud_task.py - put each cloud session on the team board so no identity duplicates it (OPUS, 2026-10-01).

  open STREAM SUFFIX "WHAT" [--page PAGE ...] [--repo db|re]
      Adds and claims OPUS-CLOUD-<STREAM>-<SUFFIX>-<MMDD> (assigned to OPUS). Each --page becomes a held resource
      (file:database/ffxii tza/<page>, the key form the lanes use), so another identity's claim on that page is refused
      while the cloud session works. Run scope_guard.py first; open refuses nothing by itself beyond team.py's checks.
  close TASK "NOTE" [commit:HASH ...]
      Finishes the task (releasing the pages) once the report is ingested or abandoned.
Prints team.py's result lines; a claim counts only when it printed "Saved revision"."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloudlib as cl  # noqa: E402


def main(a):
    if a and a[0] == "open" and len(a) >= 4:
        stream, suffix, what = a[1].upper(), a[2].upper(), a[3]
        pages = [a[i + 1] for i, x in enumerate(a) if x == "--page"]
        repo = a[a.index("--repo") + 1] if "--repo" in a else "db"
        tid = "OPUS-CLOUD-%s-%s-%s" % (stream, suffix, time.strftime("%m%d"))
        res = [{"key": "file:database/ffxii tza/" + p.lower()} for p in pages] or \
              [{"key": "cloud:%s/%s" % (repo, suffix.lower())}]
        task = {"id": tid, "kind": "research", "priority": "P3", "requester": "OPUS", "assigned_to": "OPUS",
                "target": ", ".join(pages) or what, "scope": "cloud session (%s repo): %s" % (repo.upper(), what),
                "completion": "report ingested by OPUS (docs/CLOUD_AGENTS.md task log); pages released",
                "dependencies": [],
                "resources": res}
        print("add:", cl.board_apply({"action": "add", "task": task}))
        print("claim:", cl.board_apply({"action": "claim", "task": tid, "agent": "OPUS",
                                        "note": "OPUS: cloud session working this scope; other identities please leave it "
                                                "until this task is DONE (docs/CLOUD_PROGRAM.md)", "resources": res}))
        print("TASK", tid)
        return 0
    if a and a[0] == "close" and len(a) >= 3:
        print("finish:", cl.board_apply({"action": "finish", "task": a[1], "note": a[2],
                                         **({"result_refs": a[3:]} if a[3:] else {})}))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
