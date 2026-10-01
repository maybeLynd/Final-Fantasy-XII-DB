# ASTRA — EO3 stopped-event and abort qualification

This is the next component of FABLE-REQ-ASTRA-EO3-PATH-POINTER, after commits
50cfe6e8 and25b2ca41. Consumers are FABLE resource-queue semantics and OPUS queue
layout/ABI. No FF12 run or new reconstruction phase is included.

Question: can the scoped callback bind its full context and exact memory reads
to one owned stopped event, then (a) resume and cleanly detach, or (b) terminate
the explicitly owned disposable subject without letting the successor execute?
Competing explanations include wrong-thread/context binding, a read after
continuation, missing/partial reads promoted to data, and abort-after-resume.

Method: a native synthetic instrument control. Static replay already establishes
the recorder's decisions; existing native receipts establish individual GPR
projection and memory-reader behavior. They do not establish this combined
stopped-event behavior. Reuse the frozen owned-event/cleanup/API observer and the
native FP fixture. Add only a scoped callback and bounded pending-event abort.

The fixture's existing native body will operate on an owned shared mapping.
Counters immediately before and after the gate remain observable after process
exit; known RDI path/R10 counter pointers and RAX sentinel qualify required GPRs.
Preserve/restore nonvolatile RDI and retain all original fixture bytes around the
labelled additions. Known source/path bytes and counters are supplied state,
not FF12 allocations, requests, initialization or scheduling.

Controls: no-debugger baseline with both counters equal; owned breakpoint with
before=after+1; exact stopped path/counter reads; ordinary continuation increases
after and remains responsive; stopped abort leaves after unchanged after subject
exit. A deliberately unavailable read must trigger abort rather than resume or a
semantic PASS. Wrong thread/context/exception ownership must be rejected before
the callback. Preserve raw API order and all return/read counts.

Bounds: one gate, first owned observation only, at most3s attachment setup plus
2s armed capture and3s cleanup/drain. Direct Popen child identity, parent, nonce,
native image and process creation stamp must agree before attach/termination.
The whole child has a bounded deadline and explicit cleanup/reaping. No process
discovery, unrelated PID operation, FF12 control, saves/config or PC automation.

Acceptance is per control. Normal requires matching observer data, successor
effect, successful detach, no debugger, continued native sentinel returns and
normal resource cleanup. Abort requires exact owned termination, no successor
effect and verified terminal state; it is CONTROL_ABORTED, never semantic PASS.
No target-finally/free claim is made after intentional process termination.
Preserve invalid controls and change the hypothesis/instrument before rerunning.
The known FIP transparency counterexample and EXP127 invalidity remain unchanged.
