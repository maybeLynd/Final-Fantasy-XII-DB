#!/usr/bin/env bash
# Commit ONLY the paths named on the command line, in a private index.
#
# Why this exists. Twice now the rule "check the staged column before committing"
# has failed in the same way: the check ran, it showed a peer's files staged, and
# the commit went ahead anyway because it was chained behind the check with &&.
# An && chain stops on a non-zero exit, and a non-empty staged column is not an
# error -- it is output somebody has to read. A guard that depends on the agent
# reading its own output is not a guard.
#
# So the index itself is made private. GIT_INDEX_FILE points git at a scratch
# index seeded from HEAD, the named paths are added to that, and the commit is
# built from it. The repository index is never touched, which means a peer's
# staged work CANNOT be swept in even if this script is run carelessly, and
# their staging survives the commit intact.
#
#   publish_paths.sh <message-file> <path> [<path> ...]
#   PUBLISH_AUTHOR="Name <email>" publish_paths.sh ...   # author override, no amend
#
# Hold @publication before running this. It does not check the board; it only
# makes the staging mistake impossible.
#
# ONE PUBLISHER AT A TIME, AND IT IS THE WRAPPER'S JOB. 2026-09-16: a wrapper timed out
# waiting for @publication and a SECOND copy was started for the same task and the same
# file while the first process was still alive. It resolved cleanly only because the first
# claimed the moment a blocking resource was released and finished before the second
# arrived. THAT IS A LUCKY INTERLEAVING, NOT A SYNCHRONISATION MECHANISM - the two could
# have met at the claim, at the guard, or at the commit.
#
# The private index below stops a PEER's staged work entering this commit. It does nothing
# about a second copy of your own wrapper. If a publisher times out: establish whether it
# is still alive, terminate or reap it, and only then re-drive. A pid lock in the wrapper
# is the cheap way, and a stale one must be reaped and reported rather than obeyed forever.
#
# It also REFUSES A DIRECTORY ARGUMENT. Two mistakes are possible here and the private
# index only prevents one: a peer's work can be swept in because it was already STAGED
# (prevented below), or because the caller named a PATH THAT CONTAINS IT (prevented in
# the add loop). Both happened on 2026-09-12, an hour apart, by the same agent.

set -euo pipefail

if [ "$#" -lt 2 ]; then
    echo "usage: publish_paths.sh <message-file> <path> [<path> ...]" >&2
    exit 2
fi

msg="$1"; shift
[ -f "$msg" ] || { echo "publish_paths.sh: no such message file: $msg" >&2; exit 2; }
# Make the message path absolute NOW: the correction gate and other checks
# run from inside gfz-scripts (cd below), where a repo-relative $msg silently
# misses and records named in the message are never seen.
msg="$(cd "$(dirname "$msg")" && (pwd -W 2>/dev/null || pwd))/$(basename "$msg")"

root="$(git rev-parse --show-toplevel)"
tmp="$(mktemp "${TMPDIR:-/tmp}/opus-index.XXXXXX")"
trap 'rm -f "$tmp"' EXIT

# ---------------------------------------------------------------------------
# The private index stops a peer's STAGED work being swept IN. It does nothing
# about the opposite failure, which is writing a peer's committed work OUT:
#
#   read-tree HEAD        <- private index describes THIS commit
#   ... a peer commits ...   <- HEAD moves
#   commit-tree -p HEAD      <- parent is the NEW head, tree is from the OLD one,
#                               so every file the caller did not name comes back
#                               to its old content as a DELETION or a revert.
#
# That happened on 2026-09-13: commit b05dc3b1 reverted two of FABLE's files,
# neither of them named on the command line, because FABLE committed 8965e28c
# inside that window. Nothing was lost - the worktree still held FABLE's bytes -
# but the committed tree was wrong until 5b45d568 restored it.
#
# So: pin the base, and make the ref update a COMPARE-AND-SWAP against it. If
# HEAD moved, nothing is written; re-seed from the new HEAD and build again.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# @publication, checked here rather than trusted to the caller.
#
# On 2026-09-13 OPUS committed dd620542 while SWE2-EC7 held the reservation for
# SWE2-EC7-PUB-MKVPARSER. Nothing was damaged -- the private index and the CAS below
# both did their jobs -- but the reservation exists to stop the contention happening
# at all, and it was not held. The cause was not forgetfulness: the claim was run as
#
#     team.py apply --agent OPUS --file claim.json | tail -1 && publish_paths.sh ...
#
# and a pipeline's exit status is the LAST command's, so `tail` returned 0 and the
# refusal scrolled past as text. That is the same failure the private index was built
# for, one level up: a guard that depends on the agent reading its own output is not
# a guard.
#
# So the check moved into the script. It REFUSES only when another agent holds the
# reservation -- a peer who holds it properly is never blocked -- and warns when
# nobody holds it, because a solo publish on a quiet board is not worth wedging.
# Set XII_PUBLISH_NO_BOARD_CHECK=1 to skip it (recovery, or a board that cannot be read).
# ---------------------------------------------------------------------------
#
# ONE EXEMPTION, added 2026-09-13. The board-tail commit -- the commit that records the
# reservation transitions themselves -- necessarily runs AFTER the release, so a named
# agent legitimately holds nothing at that moment. The exit-4 branch was refusing exactly
# that commit and telling the caller to `unset TEAM_AGENT`, which routes the one commit
# that should be attributable onto the anonymous warn path: the same path that let
# a17de4d1 through. So when EVERY named path is the board file itself, the commit is
# allowed and says so. It cannot be used to smuggle content past the guard, because a
# single database path in the same invocation turns the exemption off.
if [ "${XII_PUBLISH_NO_BOARD_CHECK:-0}" != "1" ]; then
    board="$root/Database/FFXII TZA/_index/_inbox/TEAM.json"
    me="${TEAM_AGENT:-}"
    board_tail_only=1
    for _p in "$@"; do
        case "${_p#./}" in
            "Database/FFXII TZA/_index/_inbox/TEAM.json") ;;
            *) board_tail_only=0 ;;
        esac
    done
    if [ -f "$board" ]; then
        holder="$(python - "$board" <<'PYEOF'
import json, sys
try:
    b = json.load(open(sys.argv[1], encoding='utf-8'))
except Exception:
    sys.exit(0)
for t in b.get('tasks', []):
    # claimed_resources is the hold team.py actually recorded when a claim named its
    # own (possibly narrower) set; resources is only the task's declared want. The
    # claim-time hold is what this guard must see, or a legitimate narrowed hold is
    # invisible here (OPUS-NOTICE-FRONTIER-A-CLAIM-TIME-HOLD-IS-INVISIBLE-TO-PUBLISH-PATHS).
    res = t.get('claimed_resources') or t.get('resources', [])
    if t.get('status') == 'ACTIVE' and any(
            r.get('key') == '@publication' for r in res):
        print('%s	%s' % (t.get('agent') or '?', t.get('id')))
        break
PYEOF
)"
        if [ -n "$holder" ]; then
            hagent="${holder%%	*}"; htask="${holder##*	}"
            if [ -n "$me" ] && [ "$hagent" = "$me" ]; then
                echo "publish_paths.sh: @publication held by $hagent ($htask) -- that is you, proceeding" >&2
            else
                echo "publish_paths.sh: REFUSING -- @publication is held by $hagent ($htask)." >&2
                echo "  Wait for the release and claim it yourself. Set TEAM_AGENT=<your id> if that holder IS you." >&2
                exit 3
            fi
        elif [ -n "$me" ] && [ "$board_tail_only" != "1" ]; then
            # You named yourself and you hold nothing. That is not the quiet-board case the warning
            # below is for -- it is a claim that never landed. On 2026-09-13 OPUS published a17de4d1
            # this way: the `add` op for the reservation task failed on a transient TEAM.lock, its
            # output had been discarded to /dev/null, the six claim retries all reported "unknown
            # task", and by then nobody held the key so the warning let the batch through. Refusing
            # here costs a solo publisher one export and catches the case the guard exists for.
            echo "publish_paths.sh: REFUSING -- TEAM_AGENT=$me holds no @publication reservation." >&2
            echo "  Nobody holds it, so this is a claim that did not land rather than a quiet board." >&2
            echo "  Claim it, or unset TEAM_AGENT to publish as an unidentified solo caller." >&2
            echo "  (Publishing ONLY TEAM.json is exempt -- a board tail follows the release.)" >&2
            exit 4
        elif [ "$board_tail_only" = "1" ]; then
            echo "publish_paths.sh: board tail (TEAM.json only) by ${me:-an unidentified caller}; no reservation needed, proceeding" >&2
        else
            echo "publish_paths.sh: WARNING -- no ACTIVE task holds @publication. Claim it before publishing." >&2
        fi
    fi

    # BOARD INTEGRITY AT THE PUBLICATION CHECKPOINT, added 2026-09-26
    # (SWE2-FRONTIER) for the TEAM rollback incident: a long-running process
    # dumped an 11-hour-stale in-memory board over ~1,050 live operations, and
    # commit 67015c61a then published the stale file as if it were live state.
    # A publish must never be the channel that commits a rolled-back board.
    #
    # When TEAM.json is among the named paths, the durability journal must
    # agree the file is live state (same revision+content hash at high-water,
    # current epoch). On any incident verdict this refuses: the correct move
    # is the coordinated recovery, not a commit that entrenches the fork.
    team_named=0
    for _p in "$@"; do
        case "${_p#./}" in
            "Database/FFXII TZA/_index/_inbox/TEAM.json") team_named=1 ;;
        esac
    done
    if [ "$team_named" = "1" ]; then
        if ! ( cd "$root/Database/Tools/analysis-kit/gfz-scripts" && \
               python team.py boardcheck ) >/dev/null 2>&1; then
            echo "publish_paths.sh: REFUSING -- TEAM.json fails the durability journal check." >&2
            echo "  The board on disk does not match the journaled high-water. Do not commit it;" >&2
            echo "  run 'python team.py boardcheck' for the incident detail." >&2
            exit 6
        fi
    fi

    # GENERATED CURRENT BLOCKS ARE REFRESHED AT PUBLICATION (2026-09-26 directive).
    # An operative header block is a dated view of the board; publishing a file that
    # still carries yesterday's queue_snapshot would freeze a stale selection into
    # history. For every named .md containing a TEAM-CURRENT marker, regenerate the
    # block before staging. If the board moved mid-generation the tool writes an
    # honest stale-inputs label rather than a silently-old "current".
    for _p in "$@"; do
        _f="${_p#./}"
        case "$_f" in
            *.md)
                _agent="$(grep -o 'TEAM-CURRENT:begin agent=[A-Z0-9-]*' "$root/$_f" 2>/dev/null \
                          | head -1 | sed 's/.*agent=//' || true)"
                if [ -n "$_agent" ]; then
                    ( cd "$root/Database/Tools/analysis-kit/gfz-scripts" && \
                      python team.py current --agent "$_agent" --write --file "$root/$_f" ) >&2 || true
                fi ;;
        esac
    done

    # PARKING WORK IN A SHARED FILE IS NOT A SAFE HOLD, IT IS AN EXPOSED ONE (2026-09-19, OPUS).
    #
    # The private index stops a peer's STAGED work entering your commit. Nothing stops your own
    # UNSTAGED worktree edit entering THEIRS, because `git add -- <path>` takes the file as it is.
    # The protection is one-directional and it is worth knowing which direction.
    #
    # Measured: an OPUS section written into `game-application.md` was held back deliberately -
    # its companion change shared `_types/fields.tsv` with a peer's uncommitted rows, so publishing
    # would have swept theirs in. While it waited, `c27f5c836` (SWE2-EC7) committed that page and
    # carried the OPUS section with it. Nothing was lost and the text is correct at HEAD, but it is
    # attributed to another agent's commit and it went out without its author's final gate run.
    #
    # So the courtesy of parking protects peers from you and does not protect you from peers, and
    # the longer the park, the likelier someone else publishes it. Prefer: split the change so the
    # contested file is its own commit and publish the rest NOW; or publish promptly and name the
    # peer's rows in the message. Do not leave finished work sitting in a shared file for hours.
    #
    # FILE CLAIMS, WHICH UNTIL NOW PROTECTED NOTHING AT ALL.
    #
    # `team.py apply()` enforces resource overlap on the CLAIM path only -- there is no write path,
    # because writes do not go through team.py. So a `file:` reservation has always been advisory,
    # and the board presented it to every other agent as exclusive. Measured on 2026-09-14 while
    # adjudicating OPUS-CONTRA-DATA-INDEX-LOCK-SCOPE: two commits edited `_index/OPEN-QUESTIONS.md`
    # while another agent held it -- 070920dd (OPUS, ELEVEN MINUTES after the claim was taken) and
    # 02229841 (SWE2-CONTRACT) -- and in the same window the holder wrote nothing at all.
    # **The lock penalised the agents who honoured it and stopped nobody else.**
    #
    # This is the first place a write becomes durable, so it is the first place the claim can be
    # seen. It WARNS and does not refuse, deliberately: a hard refusal here would have blocked
    # FABLE's adjudicated 296-row register batch behind a claim its owner had never exercised and
    # could not release that day (session free, daily-cap). A guard that can deadlock the fleet on
    # an unexercised claim is worse than the gap it closes. The refusal belongs behind a review,
    # which is filed; the visibility does not.
    if [ -f "$board" ]; then
        foreign="$(python - "$board" "${TEAM_AGENT:-}" "$@" <<'PYEOF'
import json, sys
board, me = sys.argv[1], sys.argv[2]
paths = [p[2:] if p.startswith('./') else p for p in sys.argv[3:]]
try:
    b = json.load(open(board, encoding='utf-8'))
except Exception:
    sys.exit(0)
held = {}
for t in b.get('tasks', []):
    if t.get('status') != 'ACTIVE':
        continue
    agent = t.get('agent') or '?'
    if me and agent == me:
        continue
    for r in (t.get('claimed_resources') or t.get('resources', [])):
        k = str(r.get('key', ''))
        if k.startswith('file:'):
            held[k[5:].lower()] = (agent, t.get('id'))
for p in paths:
    hit = held.get(p.lower())
    if hit:
        print('%s | %s | %s' % (p, hit[0], hit[1]))
PYEOF
)"
        if [ -n "$foreign" ]; then
            echo "publish_paths.sh: WARNING -- path(s) reserved on the board by ANOTHER agent:" >&2
            printf '  %s\n' "$foreign" >&2
            echo "  A file: reservation is ADVISORY -- team.py gates claims, not writes -- so this is" >&2
            echo "  not a refusal. It is the first point at which the claim is visible to you." >&2
            echo "  Proceed only if you have the holder's handoff or a recorded adjudication." >&2
        fi
    fi
fi

# ---------------------------------------------------------------------------
# OVERLAY CARRIERS HAVE ONE PUBLISHER, added 2026-09-26 for
# OPUS-NOTICE-FRONTIER-69E9CAD19-SWEPT-SECTION01-OVERLAY.
#
# 69e9cad19 (ORACLE, EXP-151 contract sync) committed
# CONTRACT-battle-unit-construction.md wholesale along with its own edit and
# carried the uncommitted SECTION-01 overlay with it - five evidence citations
# dropped, restored at 673c442af. The file WAS listed in the overlay drop
# census; the hazard set is therefore enumerable, and naming one of those paths
# while the overlay plan is in force means you are publishing somebody else's
# overlay - dropping or reverting whatever it changed (291ec5588 later did the
# reverse and silently reverted ORACLE's 01EC81F0 fix in the same class).
#
# The census file column is the carrier set - these are exactly the paths where
# a wholesale commit drops evidence. While the continuation-overlay plan is in
# force they publish through the plan's named publisher only:
#
#   TEAM_AGENT=SWE2-FRONTIER   -> allowed (the plan names FRONTIER publisher)
#   TEAM_AGENT=<other>         -> REFUSE
#   TEAM_AGENT unset           -> warn and proceed
#
# The gate dies with the plan: when EXTERNAL-CONTINUATION's last section lands,
# the census files are historical and this check is inert.
#
# Made mechanical 2026-09-30 (SWE2-FRONTIER, on FABLE's report that the gate still
# refused after all twelve sections landed): the check reads the plan itself and is
# inert once overlay-publication-plan.md carries a line `plan_state: CLOSED`. The plan
# owner writes that line only after verifying no census carrier holds an uncommitted
# continuation overlay; reopening the plan is deleting the line.
# ---------------------------------------------------------------------------
carrier_hit="$(python - "$root" "${TEAM_AGENT:-}" "$@" <<'PYEOF'
import glob, os, sys
root, me = sys.argv[1], sys.argv[2]
paths = {p[2:] if p.startswith('./') else p for p in sys.argv[3:]}
carriers = set()
cand = os.path.join(root, "Database", "FFXII TZA", "_index", "candidates")
import re
try:
    plan = open(os.path.join(cand, "overlay-publication-plan.md"), encoding="utf-8").read()
except OSError:
    plan = ""  # a missing plan is not a closed plan: the gate stays in force
closed = re.search(r"^plan_state:\s*CLOSED\s*$", plan, re.M) is not None
for tsv in ([] if closed else glob.glob(os.path.join(cand, "overlay-drop-census-*.tsv"))):
    try:
        for line in open(tsv, encoding="utf-8"):
            f = line.split("\t", 1)[0].strip()
            if f and f != "file":
                carriers.add("Database/FFXII TZA/" + f)
    except OSError:
        pass
for p in sorted(paths & carriers):
    print(p)
PYEOF
)"
if [ -n "$carrier_hit" ]; then
    if [ "${TEAM_AGENT:-}" = "SWE2-FRONTIER" ]; then
        echo "publish_paths.sh: overlay carrier(s) named - you are the plan's publisher, proceeding:" >&2
        printf '  %s\n' "$carrier_hit" >&2
    elif [ -z "${TEAM_AGENT:-}" ]; then
        echo "publish_paths.sh: WARNING -- overlay carrier(s) named by an unidentified caller:" >&2
        printf '  %s\n' "$carrier_hit" >&2
        echo "  These paths carry the EXTERNAL-CONTINUATION overlays; the plan names SWE2-FRONTIER" >&2
        echo "  the sole publisher (69e9cad19 swept SECTION-01 this way)." >&2
    else
        echo "publish_paths.sh: REFUSING -- overlay carrier(s) are publishable only by the plan's named publisher:" >&2
        printf '  %s\n' "$carrier_hit" >&2
        echo "  _index/candidates/overlay-publication-plan.md ruling 1 names SWE2-FRONTIER; a wholesale" >&2
        echo "  publish here drops or reverts the carried overlay (69e9cad19, and 291ec5588 in reverse)." >&2
        echo "  If your change is independent of the overlay, splice your hunks, or route to FRONTIER." >&2
        exit 7
    fi
fi

# ---------------------------------------------------------------------------
# IN-FILE FOREIGN SECTIONS, added 2026-09-19 for OPUS-CONTRA-SWE2EC7-BATCH26-
# SWEPT-MY-UNCOMMITTED-PAGE-SECTION (second instance; the first was FABLE's
# 1e3176eaa, tracked in the same notice).
#
# `git add -- <path>` takes the worktree file AS IT IS. Naming a page you
# legitimately edited also stages every OTHER uncommitted edit parked in that
# file, whoever wrote it - a peer's finished section rides out under your
# commit message, without their gates and without their authorship. Both
# recorded instances were whole `##`-headed sections; `git status` reporting
# the file clean afterwards is what makes this hard to notice.
#
# Ownership cannot be proven mechanically, so the gate checks the observable
# signature of the defect: every section heading a commit ADDS to a named .md
# must name the publisher (or be one of the exempt forms below). A heading
# that names nobody is exactly what a swept section looks like, and it is
# also what your own section SHOULD look like anyway - the fleet's update
# convention already carries the identity in the header.
#
#   TEAM_AGENT=SWE2-FOO  -> added `#{1,6}` headings must contain "SWE2-FOO",
#     except `## Resume state` inside that agent's own inbox file.
#   TEAM_AGENT unset     -> warn and proceed (a solo caller cannot be
#                           attributed; the heading list is still printed).
#   PUBLISH_ALLOW_FOREIGN_HEADERS=1 -> warn instead of refuse, for a
#     legitimate handoff where you deliberately commit a peer's section.
# ---------------------------------------------------------------------------
if [ -n "${TEAM_AGENT:-}" ] || [ "${PUBLISH_ALLOW_FOREIGN_HEADERS:-0}" != "1" ]; then
    foreign_heads="$(python - "$root" "${TEAM_AGENT:-}" "$@" <<'PYEOF'
import re, subprocess, sys
root, me = sys.argv[1], sys.argv[2]
paths = [p[2:] if p.startswith('./') else p for p in sys.argv[3:]]
head_re = re.compile(r'^\+\s{0,3}#{1,6}\s')
out = []
for p in paths:
    if not p.lower().endswith('.md'):
        continue
    d = subprocess.run(['git', '-C', root, 'diff', 'HEAD', '--', p],
                       capture_output=True, text=True).stdout
    own_inbox = me and p.replace('\\', '/') == 'Database/FFXII TZA/_index/_inbox/%s.md' % me
    for line in d.splitlines():
        if not head_re.match(line):
            continue
        h = line[1:].strip()
        if me and me in h:
            continue
        if own_inbox and h.startswith('## Resume state'):
            continue
        out.append('%s :: %s' % (p, h))
print('\n'.join(out))
PYEOF
)"
    if [ -n "$foreign_heads" ]; then
        if [ -n "${TEAM_AGENT:-}" ] && [ "${PUBLISH_ALLOW_FOREIGN_HEADERS:-0}" != "1" ]; then
            echo "publish_paths.sh: REFUSING -- named path(s) would commit section heading(s) that do not name $TEAM_AGENT:" >&2
            printf '  %s\n' "$foreign_heads" >&2
            echo "  A named file is committed AS IT IS - this is how a peer's parked, uncommitted" >&2
            echo "  section gets swept into your publish. Either that heading is yours and should" >&2
            echo "  carry your id, or it is a peer's and the file must wait for them." >&2
            echo "  Legitimate handoff: PUBLISH_ALLOW_FOREIGN_HEADERS=1 downgrades this to a warning." >&2
            exit 5
        else
            echo "publish_paths.sh: WARNING -- named path(s) add section heading(s) not attributable to ${TEAM_AGENT:-anyone}:" >&2
            printf '  %s\n' "$foreign_heads" >&2
        fi
    fi
fi

# ---------------------------------------------------------------------------
# INLINE FOREIGN-CONTENT NOTICE, added 2026-09-21 (SWE2-FRONTIER) for
# OPUS-REQ-FRONTIER-PUBLISH-GUARD-MISSES-INLINE-EDITS.
#
# The heading guard above only sees ADDED SECTION HEADINGS. An edit appended
# inside an existing table row or paragraph is invisible to it, and that is
# the common shape for amending an OPEN-QUESTIONS row or a types.tsv cell --
# the recorded instance (2026-09-21) swept a peer's parked amendment into
# somebody else's OPEN-QUESTIONS commit with no guard firing on either side.
#
# Two additions, both deliberately non-blocking:
#   1. a per-path changed-line census is ALWAYS printed, so a publisher sees
#      at a glance that a named file carries more change than they put there;
#   2. added lines introducing an agent id that is neither the publisher's
#      own nor already present on the hunk's removed lines are printed as a
#      warning. Comparing added-versus-removed within the hunk is what keeps
#      the common legitimate case quiet: amending a cell that already names
#      a peer carries the tag on both sides of the diff.
#
# This stays a WARNING, not a refusal. Recording a peer's result in prose
# ("re-measured 2026-09-21 by OPUS") is normal and introduces a foreign id
# legitimately; only the publisher can tell a citation from a swept edit.
# If a publish prints ids you did not write, diff the path by hand first.
# ---------------------------------------------------------------------------
if [ -n "${TEAM_AGENT:-}" ]; then
    inline_report="$(python - "$root" "${TEAM_AGENT:-}" "$@" <<'PYEOF'
import re, subprocess, sys
root, me = sys.argv[1], sys.argv[2]
paths = [p[2:] if p.startswith('./') else p for p in sys.argv[3:]]
tag_re = re.compile(r'\b(?:SWE2-[A-Z][A-Z0-9-]*|ASTRA|OPUS|FABLE)\b')
census, foreign = [], []
for p in paths:
    d = subprocess.run(['git', '-C', root, 'diff', 'HEAD', '--', p],
                       capture_output=True, text=True).stdout
    adds = dels = 0
    hunk_removed = set()
    for line in d.splitlines():
        if line.startswith('@@'):
            hunk_removed = set()
        elif line.startswith('-') and not line.startswith('---'):
            dels += 1
            hunk_removed.update(tag_re.findall(line))
        elif line.startswith('+') and not line.startswith('+++'):
            adds += 1
            for tag in tag_re.findall(line):
                if tag != me and tag not in hunk_removed:
                    foreign.append('%s :: %s :: %s' % (p, tag, line[1:].strip()[:110]))
    if adds or dels:
        census.append('  %s: +%d -%d' % (p, adds, dels))
print('CENSUS')
print('\n'.join(census))
print('FOREIGN')
print('\n'.join(foreign))
PYEOF
)"
    # The while body must not end on a false test: an empty census still yields
    # one empty line, `[ -n "" ]` is the body's last command, and under
    # `set -euo pipefail` that 1 becomes the pipeline's status -- a silent exit.
    echo "$inline_report" | sed -n '/^CENSUS$/,/^FOREIGN$/p' | sed '1d;$d' | while IFS= read -r l; do
        if [ -n "$l" ]; then echo "publish_paths.sh: changed lines$l" >&2; fi
    done
    foreign_inline="$(echo "$inline_report" | sed -n '/^FOREIGN$/,$p' | sed '1d')"
    if [ -n "$foreign_inline" ]; then
        echo "publish_paths.sh: WARNING -- added line(s) carry agent id(s) that are not $TEAM_AGENT and were not on the replaced line(s):" >&2
        printf '  %s\n' "$foreign_inline" >&2
        echo "  That can be a legitimate citation, or a peer's parked inline edit riding your" >&2
        echo "  publish. The heading guard cannot see these; diff the path before re-running." >&2
    fi
fi

# ---------------------------------------------------------------------------
# CORRECTION-PUBLISH CONSUMER-CHECK GATE, added 2026-09-26 (SWE2-FRONTIER) for
# FABLE-REQ-FRONTIER-CONTRACT-CORRECTION-PUBLISH-NEEDS-CONSUMER-CHECK.
#
# EVIDENCE-POLICY rule 4a -- a correction updates every affected current
# consumer -- was enforced by memory, and the drift cases are recorded:
# EXP-189's receipt kept '8 dwords' after the contract was right; the
# encoded-id contract said (0, cx) while the bytes say handler(id, 0);
# 69e9cad19's 01EC81F0 was later reverted with no record of which reading
# was right. Detection: a named .md under Database/FFXII TZA/ whose diff
# adds a hunk containing both a struck claim '~~' and Corrected/Superseded/
# REFUTED is a CORRECTION publish (the marker must be a real ~~text~~ pair --
# a `~~` mention in prose describing the gate is not a strike; files under
# _index/_inbox/ are operational narrative and out of scope). It must then carry a consumer-check
# record under _index/candidates/ -- staged in this publish or named in the
# message -- listing each consumer's agreement state and the regression.
# Executable claim shapes (reset widths/masks, argument order, register or
# byte binds) require that record to name an existing .py control, because
# matching words is not executing the control. PENDING PROPAGATION records
# pass but are printed.
#
# OVERRIDE CONTRACT (2026-09-27): PUBLISH_NO_CORRECTION_CHECK=1 is not an
# escape hatch. It downgrades the refusal to a warning ONLY when the commit
# message itself carries an auditable authorization:
#
#   correction-override: <authorizer agent-id or board task>
#   override-reason: <why the record cannot be carried in this publish>
#
# Both lines land in the commit message, so the override is attributable and
# greppable in history. A bare env var is refused like any other violation.
# ---------------------------------------------------------------------------
gate_status=0
gate_out="$( cd "$root/Database/Tools/analysis-kit/gfz-scripts" && \
            python publish_correction_gate.py "$root" "$msg" "$@" 2>&1 )" \
    || gate_status=$?
if [ "$gate_status" -eq 8 ]; then
    if [ "${PUBLISH_NO_CORRECTION_CHECK:-0}" = "1" ]; then
        ov_auth="$(grep -iE '^correction-override:' "$msg" | head -1 || true)"
        ov_why="$(grep -iE '^override-reason:' "$msg" | head -1 || true)"
        if [ -n "$ov_auth" ] && [ -n "$ov_why" ]; then
            echo "publish_paths.sh: OVERRIDE -- correction gate refusal downgraded, audited:" >&2
            echo "  $ov_auth" >&2
            echo "  $ov_why" >&2
            { echo "$gate_out" | grep '^refuse:' || true; } | sed 's/^/  suppressed: /' >&2
        else
            echo "publish_paths.sh: REFUSING -- PUBLISH_NO_CORRECTION_CHECK set without an auditable override." >&2
            echo "  The message file must carry 'correction-override: <authorizer>' and" >&2
            echo "  'override-reason: <why>'. An override is an auditable act, not an env escape." >&2
            { echo "$gate_out" | grep '^refuse:' || true; } | sed 's/^/  /' >&2
            exit 8
        fi
    else
        echo "publish_paths.sh: REFUSING -- correction publish without a consumer-check record:" >&2
        { echo "$gate_out" | grep '^refuse:' || true; } | sed 's/^/  /' >&2
        echo "  EVIDENCE-POLICY 4a: stage or name a record under _index/candidates/ listing" >&2
        echo "  each current consumer's agreement and the regression that measures it." >&2
        echo "  Authorized override: PUBLISH_NO_CORRECTION_CHECK=1 plus correction-override:" >&2
        echo "  and override-reason: lines in the message file." >&2
        exit 8
    fi
elif [ "$gate_status" -ne 0 ]; then
    echo "$gate_out" >&2
    exit "$gate_status"
fi
{ echo "$gate_out" | grep '^note:' || true; } | while IFS= read -r l; do
    echo "publish_paths.sh: correction-gate ${l#note: }" >&2
done

# ---------------------------------------------------------------------------
# OPEN-CLAIM DRIFT, added 2026-09-26 (SWE2-FRONTIER) for
# FABLE-REQ-FRONTIER-STALE-OPEN-CLAIM-REPORT. A consumer page that still calls
# a question id open/unresolved while its register row is ANSWERED is a drift
# candidate -- the answer never reached it (UQ-136, DD-1, SM-1..5, G-14, EE-12
# were all found this way). REPORT-ONLY, deliberately: a dated falsification
# sentence kept as history, or an id cited for an unanswered sub-scope, is a
# legitimate hit; only hand review tells them apart. Prints hits that land in
# the files this publish touches so the publisher sees them while the text is
# in hand; the whole-DB view lives in check_questions.py.
# ---------------------------------------------------------------------------
_md_paths=()
for _a in "$@"; do
    case "$_a" in
        *.md) _md_paths+=("$_a");;
    esac
done
if [ "${#_md_paths[@]}" -gt 0 ]; then
    ( cd "$root/Database/Tools/analysis-kit/gfz-scripts" && \
      python open_claim_drift.py --paths "${_md_paths[@]}" \
      2>&1 | sed 's/^/publish_paths.sh: drift: /' >&2 ) || true
fi

# ---------------------------------------------------------------------------
# EXPECTED-CONTENT PINS, added 2026-09-20 (SWE2-FRONTIER) for
# OPUS-REQ-ASTRA-PREPUBLISH-CLEAN-GATE -- ADAPTED, not adopted verbatim.
#
# The proposal was a worktree snapshot taken when the publishing chain starts,
# diffed again at commit time. That catches only a MID-window edit; a peer's
# edit already sitting in the named path is baked into the snapshot and still
# swept. The adopted mechanism is content-pinning instead: the caller records
# `git hash-object` of each named path AT REVIEW TIME into a manifest, and this
# script re-hashes every named path before staging it. Any foreign change --
# before OR during the window -- changes the hash and refuses the publish, for
# .md, .tsv, scripts and binaries alike (the foreign-headers guard above only
# ever saw markdown headings).
#
#   git hash-object -- a.md b.tsv > "$work/expect.tsv"   # after final review
#   PUBLISH_EXPECT="$work/expect.tsv" publish_paths.sh msg a.md b.tsv
#
# Manifest lines are `<sha>\t<path>` or `<sha>  <path>`; `deleted\t<path>`
# pins an intended deletion. Every named path must carry a pin -- a partial
# manifest is how "I forgot one" happens. Extra pins for unnamed paths are
# ignored. ASTRA's own publish.py has pinned its reviewed blob this way since
# 2026-09-20; this makes the same discipline available to every publisher.
# Opt-in, not mandatory: a hard default would wedge every casual publish --
# the same judgement the file-claim warning above already records.
# ---------------------------------------------------------------------------
expect_manifest="${PUBLISH_EXPECT:-}"
if [ -n "$expect_manifest" ] && [ ! -f "$expect_manifest" ]; then
    echo "publish_paths.sh: PUBLISH_EXPECT manifest not found: $expect_manifest" >&2
    exit 2
fi

# ---------------------------------------------------------------------------
# DERIVED-MIRROR FRESHNESS AT THE PUBLICATION CHECKPOINT, added 2026-09-26
# (SWE2-FRONTIER) under the derived-data freshness policy in
# Database/FFXII TZA/_index/DERIVED-DATA.md.
#
# knowledge.sqlite is a dated snapshot of its inputs. Publishing while it is
# stale is legal - raw-source edits must never be blocked on the mirror - but
# publishing without KNOWING it is the failure mode: the next reader quotes a
# stale answer as current. So every publish prints the mirror's own recorded
# freshness (dependency fingerprints, not timestamps); a stale report names
# which inputs moved. Warning only, deliberately.
# ---------------------------------------------------------------------------
if [ -f "$root/Database/Tools/work/knowledge/knowledge.sqlite" ]; then
    ( cd "$root/Database/Tools/analysis-kit/gfz-scripts" && \
      python knowledge_db.py check --out "$root/Database/Tools/work/knowledge/knowledge.sqlite" \
      2>&1 | sed 's/^/publish_paths.sh: mirror: /' >&2 ) || true
fi

attempt=0
while : ; do
attempt=$((attempt + 1))
base="$(git -C "$root" rev-parse HEAD)"

# Seed the private index from the pinned base so the commit is a delta against it
# and not against an empty tree. Everything not added below is carried over unchanged.
GIT_INDEX_FILE="$tmp" git -C "$root" read-tree "$base"

if [ -n "$expect_manifest" ]; then
    pin_bad="$(python - "$root" "$expect_manifest" "$@" <<'PYEOF'
import os, subprocess, sys
root, expect = sys.argv[1], sys.argv[2]
paths = [p[2:] if p.startswith('./') else p for p in sys.argv[3:]]
want = {}
for line in open(expect, encoding='utf-8'):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    sha, sep, p = line.partition('\t')
    if not p:
        sha, sep, p = line.partition('  ')
    want[p.strip()] = sha.strip()
bad = []
for p in paths:
    if p not in want:
        bad.append('%s :: no pin for this named path' % p)
        continue
    if not os.path.exists(os.path.join(root, p)):
        if want[p].lower() in ('deleted', 'delete'):
            continue
        bad.append('%s :: pinned as content but absent from the worktree' % p)
        continue
    actual = subprocess.run(['git', '-C', root, 'hash-object', '--', p],
                            capture_output=True, text=True).stdout.strip()
    if actual != want[p]:
        bad.append('%s :: worktree %s != pinned %s' % (p, actual[:12], want[p][:12]))
print('\n'.join(bad))
sys.exit(1 if bad else 0)
PYEOF
)" || {
        echo "publish_paths.sh: REFUSING -- named path(s) differ from their pinned bytes:" >&2
        printf '  %s\n' "$pin_bad" >&2
        echo "  A named path is committed AS IT IS in the worktree; a peer's uncommitted edit to" >&2
        echo "  it lands under your message. Re-review the file, or re-pin only what you wrote." >&2
        exit 6
    }
fi

for p in "$@"; do
    # A path that is GONE from the worktree but present in HEAD is a deletion -- half of every
    # rename. Refusing it outright meant a rename could not be published at all: the new name was
    # committed and the old one silently stayed, leaving two copies of the same file. Named
    # explicitly like any other path, so a deletion is still something the caller has to ask for.
    if [ ! -e "$root/$p" ]; then
        if GIT_INDEX_FILE="$tmp" git -C "$root" ls-files --error-unmatch -- "$p" >/dev/null 2>&1; then
            echo "publish_paths.sh: '$p' is gone from the worktree -- committing it as a DELETION" >&2
            GIT_INDEX_FILE="$tmp" git -C "$root" rm --cached --quiet -- "$p"
            continue
        fi
        echo "publish_paths.sh: not in the worktree and not in HEAD: $p" >&2
        exit 2
    fi
    # A DIRECTORY IS NEVER WHAT A SCOPED COMMIT MEANS. The private index below stops a peer's
    # STAGED work being swept in; it cannot stop the caller naming a directory, because
    # `git add -- <dir>` adds every changed file under it and that is exactly what was asked
    # for. Commit 3912914 took three files inside two peers' ACTIVE claims that way, an hour
    # after the private index was introduced to stop the other half of the same mistake.
    # Name the files. If there are thirty, list thirty - or generate the list, which is what
    # the caller of a thirty-file commit should be doing anyway.
    if [ -d "$root/$p" ]; then
        echo "publish_paths.sh: '$p' is a DIRECTORY. Name the files explicitly." >&2
        echo "  git add on a directory stages every changed file under it, including a peer's." >&2
        exit 2
    fi
    GIT_INDEX_FILE="$tmp" git -C "$root" add -- "$p"
done

echo "--- staged in the private index (this is the whole commit) ---"
GIT_INDEX_FILE="$tmp" git -C "$root" diff --cached --numstat "$base"

tree="$(GIT_INDEX_FILE="$tmp" git -C "$root" write-tree)"
if [ "$tree" = "$(git -C "$root" rev-parse "$base^{tree}")" ]; then
    echo "publish_paths.sh: those paths are identical to HEAD; nothing to commit" >&2
    exit 1
fi

# AUTHOR OVERRIDE, added 2026-09-16 (OPUS) for FABLE-REQ-OPUS-PUBLISH-PATHS-HAS-NO-AUTHOR-OVERRIDE.
#
# An identity whose commits must carry a different name had no way to say so, so the routine was
# to publish and then `git commit --amend --author=...`. That puts a SECOND git operation
# immediately after the one this script exists to make safe, and an amend that ran while a peer had
# staged work is exactly the failure the private index prevents. It was safe on 2026-09-16 only
# because the repository index happened to be empty AND somebody remembered to check - which is the
# shape of guard this file's own header argues against.
#
# So the identity goes in before the commit object is built, not after it exists. commit-tree takes
# it from the environment, so there is nothing to rewrite.
#
#   PUBLISH_AUTHOR="maybeLynd <>" publish_paths.sh <msg> <path>...
#
# AUTHOR ONLY. The COMMITTER stays the ambient identity, which is the git-correct split and keeps
# the record of who actually ran the tool - an author override should not erase that. An empty
# address is allowed, because "maybeLynd <>" is the form the fleet already uses.
if [ -n "${PUBLISH_AUTHOR:-}" ]; then
    case "$PUBLISH_AUTHOR" in
        *"<"*">"*) ;;
        *) echo "publish_paths.sh: PUBLISH_AUTHOR must be 'Name <email>', got '$PUBLISH_AUTHOR'" >&2
           exit 2 ;;
    esac
    GIT_AUTHOR_NAME="${PUBLISH_AUTHOR%%<*}"
    GIT_AUTHOR_NAME="$(printf '%s' "$GIT_AUTHOR_NAME" | sed -e 's/[[:space:]]*$//')"
    GIT_AUTHOR_EMAIL="${PUBLISH_AUTHOR#*<}"
    GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL%>*}"
    if [ -z "$GIT_AUTHOR_NAME" ]; then
        echo "publish_paths.sh: PUBLISH_AUTHOR has no name part" >&2
        exit 2
    fi
    export GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL
fi

commit="$(git -C "$root" commit-tree "$tree" -p "$base" -F "$msg")"
# Three-argument update-ref is the compare-and-swap: it writes only if HEAD is still
# exactly $base. A peer that committed while this was building loses nothing, because
# nothing is written -- the loop re-seeds from their commit and builds again on top.
if git -C "$root" update-ref -m "publish_paths.sh" HEAD "$commit" "$base" 2>/dev/null; then
    break
fi

echo "publish_paths.sh: HEAD moved while this commit was being built (a peer committed)." >&2
echo "  Nothing was written. Re-seeding from the new HEAD and rebuilding." >&2
if [ "$attempt" -ge 3 ]; then
    echo "publish_paths.sh: HEAD moved on $attempt consecutive attempts; giving up rather than" >&2
    echo "  spinning. Re-run when the peer's commits have settled." >&2
    exit 1
fi
done

echo "--- committed ---"
# Print the object this run wrote, not HEAD: a peer can commit between the
# update-ref above and this line, and `git log -1` would then name THEIR commit.
# Callers verifying the publish must check $commit, never moving HEAD -- see
# ASTRA-RETURN-FRONTIER-POSTCOMMIT-IDENTITY-GUARD (c3e5349 vs peer 43d06fe).
git -C "$root" show -s --format="%h %s" "$commit"
echo "publish_paths.sh: committed sha: $commit"

# HEAD has moved but the repository index still describes the old HEAD for the
# paths just committed, which would make git status report them as changed in
# reverse. Refresh the index for THOSE PATHS ONLY -- they now equal HEAD, so the
# entries become clean -- and touch nothing else, so peer staging is preserved.
# The refresh runs on the REAL index, so a concurrent writer holding
# .git/index.lock makes `git add` exit 128 (ASTRA-NOTICE-FRONTIER-POSTCOMMIT-
# INDEX-LOCK-0930: commit bc6e03755 landed, refresh exit 128). The commit itself
# is already durable by then -- retry briefly, then report REFRESH-DEFERRED
# with the commit sha rather than fail ambiguously. Re-running the refresh is
# safe: the committed blobs equal the worktree, so the retry is idempotent.
refresh_tries=0
while :; do
    refresh_rc=0
    for p in "$@"; do
        if [ -e "$root/$p" ]; then
            git -C "$root" add -- "$p" || refresh_rc=1
        else
            git -C "$root" rm --cached --quiet --ignore-unmatch -- "$p" || refresh_rc=1
        fi
    done
    [ "$refresh_rc" -eq 0 ] && break
    refresh_tries=$((refresh_tries + 1))
    if [ "$refresh_tries" -ge 20 ]; then
        cat >&2 <<EOF
publish_paths.sh: REFRESH-DEFERRED -- the commit DID land as $commit.
  The post-commit repository-index refresh could not take .git/index.lock
  after $refresh_tries tries (a concurrent writer held it). Nothing is lost.
  Until the refresh completes, \`git status\` reports the just-committed paths
  as changed-in-reverse; peer staging is untouched either way.
  To finish later, run for each named path:
      git add -- <path>                 (paths that exist)
      git rm --cached -- <path>         (paths the commit deleted)
  Delivery bookkeeping: this run is NOT a complete delivery. Verify the exact
  commit sha and blobs, then re-run only the refresh -- never the commit.
EOF
        exit 4
    fi
    sleep 1
done

# The repository index still holds whatever it held before, including a peer's
# staging. Show that it survived, because the point of the script is that it does.
echo "--- repository index, untouched by the commit above ---"
git -C "$root" diff --cached --numstat | head -40

# A committed document change can move the route report's inputs even when the
# content fingerprint is unchanged at this instant (a commit lands between the
# next auto run's fingerprint and this one is impossible - the mark is belt and
# braces for ordering): mark the progress package dirty so the controller's
# next cadence tick regenerates regardless of fingerprint.
progdir="$root/Database/FFXII TZA/_index/progress"
if [ -d "$progdir" ]; then
    touch "$progdir/.dirty" 2>/dev/null || true
fi
