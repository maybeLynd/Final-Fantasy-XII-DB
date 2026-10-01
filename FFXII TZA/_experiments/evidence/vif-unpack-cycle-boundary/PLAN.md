# UQ-215 cycle and cursor boundary

QUESTION: Do the statically measured V2-32 / V4_5 inner source strides mean every cycle configuration misreads a packed payload? Does UNPACK's returned byte count also bound its actual read extent?

Known evidence: FABLE's 2026-09-26 inner-stride measurement and canonical PARTIAL UQ-215. All censused code-built packets are V4-32; data-borne formats remain uncensused. FABLE retains that production. Original 0022BFF0 has an outer cycle source advance, and 0022C970 advances the packet cursor by UNPACK's returned EAX.

Competing explanations: (H1) stride defects apply independent of cycle configuration; (H2) CL=1 avoids the overlapping/skipping inner iteration, while CL>1 changes the read/output sequence. (H3) return extent bounds source reads; (H4) nominal cursor and actual access extent differ, potentially including subsequent packet bytes.

Method B: execute verified complete shipping functions in existing Unicorn/GuestMem infrastructure. Static evidence alone identifies the instructions; focused execution distinguishes full-loop behavior, actual writes and packet-cursor composition. No live initialization, packet authorship, scheduling or visible drawing is claimed. No callbacks/stubs permitted on selected paths.

Budget: at most 12 supplied-state cases; <=2 seconds and 5000 instructions per case. First CL=1 positive/control feasibility, then compatible cycle cases. A complete Win64 entry and normal return are required. Record every source read, destination write, packet-header read, return, final stack, before/after canaries and exact source/tool identity. Unique payload words and V4-32 control distinguish an observer that simply reports its own expected values.

Acceptance: full raw traces discriminate H1/H2 and H3/H4; original bodies match reference hashes and complete instruction boundaries; no unexpected calls/writes, bounded return, preserved nonvolatile registers and protected bytes. Failure/timeout/zero-case is invalid, retained, never promoted. Deliberate exact-end unmapped-source probe, if used, is labeled a controlled guest fault rather than a game crash.

Consumer: FABLE's UQ-215/page and current static request FRONTIER-RT-STATIC-MISC-B; OPUS exact decoder/ABI/extent interpretation; independent SWE2-AUDIT-SPEC review. Closure pending consumer agreement; no data-borne census closure, dead-code exclusion or L3 implementation.

Restoration: guest-only memory discarded at each case; reference read-only, no FF12/PC/save/config/instrument access. Existing live setup stop-loss remains exhausted/pending extra permission; this independent work does not reset it.
