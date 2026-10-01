# VIF UNPACK cycle and cursor evidence — pending independent acceptance

Method B, isolated verified shipping x64 instructions. No running FF12, PC control, native callback, instrument, save/config/reference write or reconstruction implementation. Reference SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`; canonical image base `00120000`. Complete original `0022BFF0` (2268 bytes) and decoder `0022C970` (533 bytes), verified against the image and their three contiguous chained PE RuntimeFunction fragments. Source/raw/tool identity is in source.json; tools are Python3.14.6, Unicorn2.1.0, Capstone5.0.7. The existing verified loader/guest-memory helper is retained unchanged.

Question and competing explanations are in PLAN.md. The existing static inner-stride measurements are correct; they alone do not describe whole-loop behavior across write cycles or the actual source access extent. FABLE retains UQ-215 static production/data-borne census; no canonical files taken over.

All fixtures use NUM3, unsigned0, addTOPS0, ADDR0 and supplied WL=CL1/2/3. Source pointer is above4GiB. Win64 entry stack modulus8, shadow/stack arguments, nonvolatile register sentinels, destination canaries and exact code bytes are checked. Selected paths use no stubs; the integrated decoder calls the real UNPACK exactly once. See raw-results.json for every observed source read, destination/global write, executed instruction, return/stack and before/after bytes. These are supplied guest state, not real engine initialization or live pointers.

| Format | WL=CL | source element starts, bytes relative to payload | return bytes |
|---|---|---|---|
| V2-32 | 1 | 0,8,16; each reads two dwords | 24 |
| V2-32 | 2 | 0,4,16; overlap within first write cycle | 24 |
| V2-32 | 3 | 0,4,8; overlap within one write cycle | 24 |
| V4_5 | 1 | 0,2,4; four reads of each halfword | 8 |
| V4_5 | 2 | 0,8,4; outer advance resets inner indexing | 8 |
| V4_5 | 3 | 0,8,16 | 8 |
| V4-32 control | 1,2,3 | 0,16,32; four dwords each | 48 |

Normalized observation: the inner read-index defect is conditional on more than one element being processed in that inner cycle. The original outer advance is `8*WL` for V2-32 and `2*WL` for V4_5; it resets the inner index. Thus the tested single-element cycle reads packed elements consecutively. This qualifies an unrestricted whole-stream “overlap by a dword / one halfword in four” interpretation, not FABLE's measured inner instruction scale. The V2-32 arm writes only the first two dwords of each sixteen-byte destination slot; the remaining two retain the warm canary. V4_5 writes all four expanded channels.

The returned byte count is independent of actual maximum source read. V4_5/NUM3 returns8 but reads through byte9 at WL=CL2 and byte17 at WL=CL3. In the integrated packet: STCYCL2/2 at0, UNPACK header at4, six payload bytes plus two padding bytes at8, following STCYCL5/5 at16. UNPACK reads that following command's low halfword as its second colour element, then reads payload+4 for its third. Decoder subsequently reads the same address16 as a command, writes both lengths5, and returns20. Every transition is in the raw event/PC sequence; no callback or mocked command parser substitutes for it.

A separate guard control maps only the nominal eight payload bytes up to a guest page boundary. WL=CL1 returns8 normally. WL=CL2 writes the first destination element then attempts a halfword at payload+8 and faults at original22C840. This is a deliberately bounded guest-memory fault with no completed return, not a FF12 crash or evidence of a reachable authored packet defect. No partial guard result is promoted to a normal execution. No save/game health claim is involved.

Controls/checks: eleven normal original returns plus the distinct deliberate fault; destination/source preservation and exact writes; V4-32 positive controls across the same cycles; paired guarded single/multi-element cycle; eight corrupted-evidence controls reject missing observer, conflated read extent/return, falsely universal CL1 corruption, missing next-header observation, promoted fault, broken positive control, changed code and zero cases. check.py reduces the retained run, it does not replay it. qualify.py rechecks original provenance only. The failed initial page-crossing setup and failed single-PE-entry qualification are retained; neither yielded an accepted semantic claim. No experiment was repeated to obtain more counts.

Semantic implication for L1/L2: representation/executable specifications must keep (1) nominal parser cursor advance, (2) actual read addresses, (3) write-cycle resets and (4) partially written destination lanes separate. A bounds validator using only returned consumption can miss the demonstrated V4_5 reads. A replacement implementation copying every packed element would differ from original for the supplied multi-element cycles. This is a database obligation and bounded sufficiency probe, not an L3 implementation/parity campaign.

Limitations: no arbitrary NUM/WL/CL sweep, fill/skip-cycle claim, unsigned/TOPS coverage, hardware PS2 parity certification, loaded-data census, real initialization, presentation, scheduling, crash cause or universal deadness. Existing code-built V4-32 census is preserved. Actual data-borne use remains OPEN. The single-word form being correct does not prove every configuration is correct.

Affected consumers: FABLE's `the-vif1-vu1-layer.md` UQ-215 and register row/census; OPUS decoder extent/ABI interpretation and any specifications claiming return==access span. Independent SWE2-AUDIT-SPEC must examine primary bytes/raw controls; FABLE/OPUS must incorporate accepted narrowing through their ownership. Current state: ROUTED/PENDING PROPAGATION, not semantic closure.

Cleanup: each guest is discarded. Source bytes and destination canaries verified; reference hash verified at capture and qualification. No FF12/PC session was opened, so no new live restoration receipt is asserted. Existing live authorization and pending extra input-budget permission are unchanged. DB_GOAL=NOT_MET.
