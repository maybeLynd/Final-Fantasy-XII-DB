# Managing the GitHub repos (OPUS, 2026-10-01)

OPUS keeps the private GitHub repos current and tidy. The user asked for it on 2026-10-01: the repos are only worth
having if they carry the latest work of value.

| repo | what it holds | authored where |
|---|---|---|
| maybeLynd/Final-Fantasy-XII-DB (this repo) | text-only snapshot of `XIIOnline/Database`, plus the cloud program (`docs/`, `cloud-input/`, `cloud-reports/`) | the database in XIIOnline; `docs/`, `cloud-input/`, `cloud-reports/` here |
| maybeLynd/Final-Fantasy-XII-RE | the reconstruction plan; later, accepted readiness maps (`docs/readiness/`) | here |

## Keeping the snapshot current

**When.**
- After every batch of OPUS publishes.
- Before every cloud launch.
- At every resume checkpoint.
- At least once a day while work is happening.

**How (on the workstation).**

```
cd C:\Users\Kristian\source\repos\Final-Fantasy-XII-DB
python tools/sync_from_xiionline.py            # dry run: counts, SOURCE <commit>
python tools/sync_from_xiionline.py --apply
git add -A
git -c user.name=maybeLynd -c user.email= commit -m "Snapshot ... from XIIOnline/Database at <SOURCE>"
git push origin main
```

**What the sync copies.**
- **Committed content only.** It reads XIIOnline's HEAD blobs, never the working tree, so another lane's uncommitted
  edits are never published.
- **Text only.** No game data and no binaries; files over 95 MB are refused.
- **Never the live board.** `_index/_inbox/TEAM.json` is excluded.
- **Repo-owned folders are kept.** It never touches `docs/`, `cloud-input/`, `cloud-reports/` or `tools/`.

**Long paths.** `core.longpaths` is set to `true` in this clone; a fresh clone needs the same setting.

## Conventions

- **Commit identity.** Author `maybeLynd`, empty email (`-c user.name=maybeLynd -c user.email=`), no AI trailer.
- **Branches.**
  - `main` holds the snapshot, the docs and the archived reports.
  - Each cloud session works on its own `cloud/<topic>` branch.
- **After ingesting a cloud report:**
  - Copy the report file into `main` under `cloud-reports/` as the archive, with OPUS's verification outcome noted in
    `docs/CLOUD_AGENTS.md`.
  - Delete the branch (`git push origin --delete cloud/<topic>`). That also closes its pull request.
- **Never merge a cloud branch's other changes.** The snapshot is regenerated from XIIOnline, and edits made here
  would be overwritten.
- **`cloud-input/` is derived from the certified executable.** It holds disassembly text, so it stays in this private
  repo only: never in the RE repo, never public.
- **Pull request housekeeping.** It needs either the `gh` CLI (not installed on the workstation yet; the user can
  install it and run `gh auth login`) or branch deletion, which closes the PR.

## Checks before every push

- `git status` shows only the intended files.
- The commit subject names the XIIOnline source commit for snapshot commits.
- No file under `cloud-input/` or `cloud-reports/` holds anything beyond text derived from the database or the
  executable's code.
