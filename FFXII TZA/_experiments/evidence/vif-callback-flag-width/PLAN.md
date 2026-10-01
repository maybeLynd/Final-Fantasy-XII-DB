# VIF callback flag width — exact original composition

Question: after GiVmax writes its zero flag byte, does the DIRECT callback depend
only on that byte, or also on the unwritten upper three bytes of the argument slot?
Major system: legacy VIF/GIF renderer. FABLE mechanism and OPUS exact ABI/flag
representation are the canonical consumers; independent SPEC review follows.

A preflight identified 001DB5B9 byte store; wrapper0022C944 dword load;
decoder0022C9BB dword import/0022CB27 forward; adapter001DB643 dword truth test.
Do not infer the actual value of the untouched upper bytes from these accesses.
Choose small B original-code composition to preserve actual ABI/calls and show
the collector's resulting byte under competing supplied stack states. No live
initialization, native allocation, scheduling or presentation is tested.

Reuse existing verified-image reader/Unicorn/Capstone. Original caller, wrapper,
decoder, reset, adapter, size helper and collector execute. Supply one valid
DIRECT or DIRECTHL command with an EOP GIF tag and enough backing. Pre-create
collector chunks so only its packet allocation, memcpy and ownership-registration
boundaries need disclosed stubs. Stub effects do not prove their native effects.

Feasibility/detection control first: clean zero slot produces one copied packet,
flag0, known byte-store/dword-load/forward/test/store trace, exact copy and healthy
guest return. Preserve it, do not rerun to inflate a count. Then change only slot
upper bytes; a dirty low-byte control checks that the real caller overwrites it.
DIRECTHL and high signed bit controls distinguish command and nonzero semantics.

Budget: <=5000 instructions /2s per case, fresh guest per case. Stop on unmapped
access, unexpected code/native boundary, failure to return, corrupted reference
code, changed source/nonvolatile registers or missing detection chain. Never run
the live game to investigate a supplied-ABI claim or claim game health from guest
success. Preserve any failed raw case and fix only its actual instrument problem.

Cleanup: discard guest memory; reference/save/config unchanged, PC off. No native
or live process attaches. Ordinary upper-stack values, upstream reachability,
render replay and visual consequences stay OPEN. No L3 phase or full campaign.
