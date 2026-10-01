"""opus_md_standing.py - insert OPUS's standing GitHub/cloud responsibility section into OPUS.md, right after the RESUME
PROTOCOL section (before the first dated work section), so resume-block rewrites never remove it. Idempotent,
EOL-preserving."""
import io
P = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\_inbox\OPUS.md"
HEAD = "## Standing responsibility: the GitHub repos and the cloud program (OPUS, 2026-10-01)"
SECTION = HEAD + """

The user assigned OPUS two standing jobs on 2026-10-01:
- **Keep the private GitHub repos current.** That is maybeLynd/Final-Fantasy-XII-DB (the database snapshot) and
  maybeLynd/Final-Fantasy-XII-RE.
- **Run the cloud-session program.** It spends the temporary $250 cloud credit (expires 2026-11-05) on database work
  without duplicating anything OPUS, FABLE, ASTRA or the SWE2 (Devin) lanes do.

**Where things are.**
- **How to launch, and billing:** `C:/Users/Kristian/Desktop/CLOUD_SESSIONS_GUIDE.md`. Launches go through
  `C:/Users/Kristian/Tools/cloud-launch/cloud_launch.py`; never through routines.
- **The program:** in the DB repo checkout `C:/Users/Kristian/source/repos/Final-Fantasy-XII-DB`:
  - `docs/CLOUD_PROGRAM.md`: the five streams F, D, A, C, R, the no-duplication protocol and the lifecycle;
  - `docs/cloud-briefs/`: one brief per stream;
  - `docs/CLOUD_AGENTS.md`: the task log;
  - `docs/REPO_MANAGEMENT.md`: sync cadence and conventions.
- **Tools:** `Tools/work/OPUS/cloud/`. These are mirrored to the DB repo's `tools/opus-cloud/` at each sync, because
  Tools/work is not in git.
  - `scope_guard.py`: BLOCK / WARN / CLEAR per page;
  - `cloud_task.py open|close`: the board task `OPUS-CLOUD-*`, holding the pages;
  - `f_pack.py`: F-interior input packs;
  - `listing.py`;
  - `interior_ingest.py check|apply`: refuses to apply until SWE2-AUDIT-SPEC accepts the interior method;
  - `interior_applier.py`;
  - `briefs/`: the launch messages.

**At every resume, after the TEAM-CURRENT block:**
1. **Follow cloud tasks.**
   - List the open `OPUS-CLOUD-*` board tasks.
   - `git -C C:/Users/Kristian/source/repos/Final-Fantasy-XII-DB fetch`, and look for finished `cloud/*` branches.
   - Ingest each finished report:
     - Stream F: `interior_ingest.py check`, then re-read every row against the review sheet in
       `Tools/work/OPUS/cloud/review/`, then `apply` once the verdict allows.
     - Streams A, C and D: verify each finding and route it to the page's owner as a notice. Do not fix other
       identities' pages.
     - Stream R: verify, then copy accepted maps to the RE repo's `docs/readiness/`.
   - Then archive the report into `main`, delete the branch, `cloud_task.py close`, and update the log row.
2. **Sync the snapshot from committed state, commit, push** (`tools/sync_from_xiionline.py --apply`). Do this at
   every checkpoint and after every publish batch, so the repo always carries the latest committed work.
3. **Plan the next wave.**
   - Pace launches by OPUS's verification capacity and the credit balance. Ask the user for the Settings -> Usage bar
     after each new wave size.
   - Before each launch: `scope_guard.py`, then `cloud_task.py open`, then sync and push, then launch, then a log row.
4. **Stop using cloud sessions** when the credit is spent or on 2026-11-05. Nothing may depend on them.

**Rules.**
- A cloud result is a pointer, never evidence, and never independent review.
- Every cloud scope is guarded and claimed first.
- Wave 1 (2026-10-01) is streams F, A and R. Streams D and C wait for scopes that are OPUS-owned or unowned and not in
  another identity's flight.

"""
raw = io.open(P, "rb").read()
crlf = b"\r\n" in raw[:4000]
t = raw.decode("utf-8")
if HEAD in t:
    print("ALREADY")
else:
    a = t.index("## RESUME PROTOCOL")
    nxt = t.index("\n## ", a + 5) + 1
    sec = SECTION.replace("\n", "\r\n") if crlf else SECTION
    io.open(P, "wb").write((t[:nxt] + sec + t[nxt:]).encode("utf-8"))
    print("PATCHED crlf=%s" % crlf)
