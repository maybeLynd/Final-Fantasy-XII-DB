# VIF admission/progress preconditions — static original evidence

Question, competing explanations, budget and consumers are in PLAN.md. This separate package uses method A because the primary instruction flow suffices; no Unicorn, native harness, FF12, PC control or new experiment count. It does not depend on acceptance of ASTRA's earlier cycle/cursor execution.

Exact reference SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base00120000. Three complete decoded bodies/raw bytes in primary.json: wrapper0022C94043B; decoder0022C970533B; UNPACK0022BFF02268B. Existing reader retained unchanged; source/tool identity and current canonical preimage included. Instruction anchors are checked against complete byte-preserved extraction. These are static derivations, not measured live defaults or execution traces.

The canonical page documents STCYCL mapping and rejects filling when WL>CL. It does not establish byte-level admission or a zero-WL progress guarantee. These missing preconditions matter to a decoder specification used by modding/reconstruction; they are not a claim that the existing page's filling observation is false.

**Packet byte length is an entry/continuation condition.** Wrapper0022C954 forwards its EDX into decoderR8D. Decoder saves it inR12D, zeroesEDI, exits for length<=0, then follows a straight-line path to0022C9D6's four-byte header load. EDI is advanced4 at0022C9D3 before that load, and the budget comparison0022CB55 occurs after command handling. Positive supplied lengths1,2,3 therefore enter the same first four-byte access path. On later iterations a remainder1..3 also admits a full header. No truncated-header rejection is added by the wrapper. This says what the supplied length bounds, not that the physical backing buffer ends there or an actual authored packet is truncated.

**UNPACK does not receive remaining packet length.** Decoder builds its arguments from the decoded format, flag bits, NUM and ADDR, with a payload pointer;0022CAC7 calls original UNPACK and0022CACC addsEAX toEDI. The supplied byte budget is retained separately inR12D. This API's nominal cursor and source-access preconditions must stay distinct. This static flow fact does not certify arbitrary payload extents or any actual game packet.

**Zero write length can have no progress.** For the selected V4-32 arm with positiveNUM and WL=CL0, the initial signed WL>CL test does not reject. R11D=WL0; EBX starts0; R13D=NUM>0. Loop0022C630 selects min(remainingNUM,WL)=0, skips the inner read/store loop via0022C63E, then:

- R10 += CL*16 =0 (0022C678);
- RAX += WL*16 =0 (0022C67B);
- EBX += WL =0 (0022C67E);
- EDI += −WL =0 (0022C681);
- EBX<NUM remains true at0022C683/686 and returns to0022C630.

After the first trip the relevant register state is a fixed point. The selected cycle contains no calls or memory accesses and has no normal-return path for those supplied values. This is a bounded static progress proof; no deliberately hanging game/harness was launched. WL=CL1 chooses a one-element inner count and incrementsEBX1, a static positive discriminator against treating every configuration as zero progress. NUM0 bypasses this selected loop through0022C60B; the positiveNUM condition is essential. No all-format, CL>0 zero-WL, asynchronous interruption or default-initialization universal is asserted.

check.py qualifies original bytes, entry/loop register producers and branch/update anchors. Five corrupted-analysis controls reject a progressing counter, inserted pre-header admission, changed budget handling, zero-cycle exit and empty bodies. These are receipt/derivation controls, not mutant executions. Normalization and PASS receipts are separate from semantic truth; independent original-byte review remains required.

Affected consumers: FABLE's VIF mechanism/UQ-215/data-borne census boundaries and OPUS decoder ABI/access/progress specifications. Add the preconditions under those owners; do not erase the original filling observation, presume every authored packet satisfies them, or claim any shipped packet hangs. Reachability, valid authored ranges, real initialization and presentation remain OPEN where needed. No static exclusion of other formats. State: ROUTED/PENDING OWNER INCORPORATION and independent SWE2-AUDIT-SPEC review.

Cleanup: no guest/native/live process or instruments created; reference read-only with exact hash check. No save/config changes or fresh live restoration receipt. PC OFF. DB_GOAL=NOT_MET.
