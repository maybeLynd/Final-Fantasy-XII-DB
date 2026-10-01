# Keyboard-registration boundary: prepared, not live-validated

Player version: this reader watches the game's keyboard-state bytes while a
separate supported control sends input. It cannot press keys and it does not
claim that a sampled button state became an accepted game command.

EXP082's one Escape input did not visibly pause the game. No registration bytes
were sampled, so that result cannot distinguish missed registration from later
input handling. Repeating its load/navigation sequence without this evidence
would not answer the missing question.

Method A here: reuse the existing EXP006/024 pointer chain and EXP081's complete
reference/read qualification. Method C is required for actual current-process
registration. No game, UI, native FF12 code or debugger was used in preparation.

`input_sample.py` reads `*(02EA5368) -> +DF8 -> +118 -> +30`, preserving each
qword and all256 keyboard bytes between frame reads at0208D45C. It resolves the
chain again afterward. A changed chain is retained as CHANGED_CHAIN, never
presented as stable registration. Null and incomplete reads raise errors; they
cannot masquerade as an all-zero array. This is the existing keyboard chain,
not a new pointer discovery or a proof about the mouse device.

`observe.py` reuses EXP081's process/path/executable/module/full-text/known-byte
and null-read controls, pointer-width API declarations and finally-close path.
It requires ASTRA's @runtime and a fresh process.json naming the sole intended
reference. CLI labels are noinput, positive or pause, with exclusive output
creation; labels describe intended conditions, not successful controls.

The reader samples for at most20 seconds or4000 samples, sleeping5ms between
reads. It retains actual intervals. This bounds demand, not blocking OS read
latency. Authored profiles01F80F90/150B and live profiles01F80130/414B are retained
before/after with stability checks; these are raw bindings, not decoded action
acceptance. Exact text, modules and known read control are checked again afterward.
No custom input sender, write, hook, breakpoint or undocumented UI hold API is
introduced. Exit status RECORDED_ONLY never means a semantic pass.

Four fixture tests pass: distinctive high-address/raw-byte control; zero preserved
without a negative verdict; changed-pointer evidence; null/short/unreadable
rejection. Their API is a fake Reader. Neither those controls nor successful
compilation tests real process access or live keyboard detection. Existing
instrument history and its failed controls are preserved, not replayed.

Next feasibility requires freshly backed-up state, a no-input window, a separately
established positive keyboard control and the single requested input paired with
UI evidence. A sampled nonzero byte can support registered state only with that
identity/timing context. If the positive cannot be established, revise delivery
before another full save/combat setup. A finite polling zero cannot prove that
an arbitrarily brief transition never occurred, even with positive controls.
Unchanged chain/frame values do not prove atomicity, lifetime or exclude ABA.

No old-save, target, command-execution, death or handler conclusion follows from
this preparation. Live authorization remains active; new stop/takeover halts
control and does not permit automatic restart. PC control is currently ended.
