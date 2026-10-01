# Current title input control: no keyboard positive established

ASTRA, 2026-09-13. **INCONCLUSIVE_POSITIVE_NOT_ESTABLISHED.**

Player version: FF12 opened normally, but the one confirmation press did not
visibly leave Load Game and no pressed-key byte was sampled. The game is closed,
all26 save/config originals are restored, and PC control is off. This does not
prove that FF12 never received the press or that keyboard controls cannot work.

## Question and method

Before the HIGH combat-handler request spends another loaded-state session, can
the existing keyboard reader observe a supported confirmation press and pair it
with title-menu acceptance? H1: a registered held state is sampled. H2: no such
state is observed, due to missed delivery/brief timing or a polling/observer-state
boundary. The second outcome cannot distinguish those causes by itself.

MethodC: actual running title state is necessary for this registration question.
Reuse the prepared reader and read controls. The initial plan named Space; the
actual single nominal positive was **Return**, selected from EXP031's historical
Enter confirmation control. That earlier control used a different delivery method
and loaded state; it is not a current positive. No parameter for held-key duration
exists in this UI API. No key sweep or loaded-save setup follows the failed control.

## Identity and initial state

PID32960, game window3675546, exact shipping EXE
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
image base00120000. Current Steam properties show CloudOFF and empty advanced
launch options;26 original files copied and matched before launch. `title-before`
shows the boot autosave notice, not a ready title menu. `title-ready` and
`before-positive` show Load Game selected. No save was loaded.

`origins.json` links the unchanged observer and keyboard reader to the prepared
sources. The setup's only new change is its backup directory. Raw observations
preserve exact source hashes, full module inventories and before/after code checks.
Both windows match all7,996,981 bytes of the disk `.text`, SHA
5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4.
LUAC19930d0a1a0a and null-read rejection controls pass; full spans and pointer-width
API declarations are retained. Each window has102 modules before and afterward.
The module policy checks watched names; other modules' code/data bytes were not
all hashed or proven unmodified. This is not a claim about every module's state.

The first sandbox module query returned unreadable before sampling. The observer
rejected it: `noinput-initial-invalid.json`,0samples,INVALID. The same observer
with granted process-read access then completed. No detector result depends on
that failed attempt. The existing identity gate already supplies the regression
control: unreadable identity cannot become a successful zero observation.

## Raw observations and interpretation

[Normalized observation](observation.json) is derived from
[no-input raw JSON, lossless gzip](noinput-memory.json.gz) and
[Return-window raw JSON, lossless gzip](positive-memory.json.gz).
Uncompressed byte counts and SHA256 are retained; decompression reproduces the
original observer output exactly. `review.py` checks the retained controls and
sample-derived figures. RECORDED_ONLY is a capture status, never a semantic pass.

| Window | Samples | Nonzero held-byte samples | Largest sample gap |
|---|---:|---:|---:|
| No input,20s | 3647 | 0 | 10.049ms |
| One Return,20s | 3647 | 0 | 11.170ms |

The Return tool call is11:34:22.022–11:34:22.072UTC and lies inside the second
capture;9 sample starts lie inside that API-call interval. **50ms is the tool
round-trip, not measured key-down duration.** Both immediate and later screenshots
retain Load Game selection. All sampled pointer brackets were stable; all256 bytes
were zero. The0208D45C stamp stayed0 at title, which proves neither that input
polling ran nor that it stopped. Pointer stability does not establish title-state
polling, atomicity or absence of reuse.

Input sent: tool accepted Return. Registered: **not established**. Menu/action
accepted: **not established**. Executed action/consequence: **not established**.
A finite polling zero without a keyboard detection positive cannot prove absence.
No pause, target, command, attack, damage/death or handler inference follows.
No original-code injection, game-memory write, debugger, hook or suspension.

## Cleanup and next discriminator

Both observer handles closed. AltF4 opened the native Exit Dialog. Its first
cached-index click was rejected as unavailable; no exit was inferred. Re-selected
the current window, refreshed the focused dialog and sent Return for cleanup.
Immediate window enumeration still listed FF12, but the subsequent process query
was empty. PC-control JS was reset after that exit proof. The earlier reset during
recovery did not itself close FF12. OS/dialog responsiveness is not the missing
keyboard-array positive.

Only LUIDLow79439→78642 changed in one GameSetting.ini. The working configuration
was preserved; `cleanup.py` verified that exact delta before restoration.
[Cleanup receipt](cleanup.json) verifies all26 original hashes and unchanged backup,
with no FF12 process. **Live authorization remains ACTIVE; no new stop/takeover
occurred during this resumed run.** PC control remains off while unused.

ASTRA-REQ-FABLE-TITLE-KEYBOARD-POLL asks for the shipping writer/consumer and title
poll qualification of the existing `*(02EA5368)->+DF8->+118->+30` array. It uses
FABLE's new AP-4 pipeline evidence rather than redoing it. A/B investigation stays
with FABLE/OPUS/SWE2 under scarce-usage policy. Choose a different sufficient next
live discriminator after that review; do not repeat the same unqualified pulse.
The HIGH handler and same-session save questions remain open. This is an evidence
checkpoint, not completion of the full L1/L2 database or required final reviews.
