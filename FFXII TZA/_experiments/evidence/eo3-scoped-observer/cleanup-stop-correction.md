# ASTRA — a stop request must not prevent cleanup

An added timing control put the stop request at the beginning of existing
timeout cleanup. The first connected runner raised from its WaitForDebugEvent
wrapper during cleanup too: cleanup stayed None, no debug-register clear ran,
and detach was attempted. The raw synthetic reproducer and exact source are
retained. No native/FF12 use of that runner occurred.

The guard now recognizes the retained timeout_cleanup_begin marker and permits
only that existing cleanup path to service its events. A stop encountered during
capture still latches and ends capture. A stop arriving after capture expired
no longer blocks clearing/detaching. Neither case restarts capture or sends input.
The connection control now tests both timings and requires clear/readback/detach.

The runner also emits readiness only after successful stopped thread arming and
initial-event continuation. Readiness I/O failure is recorded, then unwinds on
the next capture poll after pending has been cleared; it cannot interrupt the
cleanup event loop. Failed arming does not produce readiness. These are synthetic
connection results, not native delivery or healthy-game evidence.
