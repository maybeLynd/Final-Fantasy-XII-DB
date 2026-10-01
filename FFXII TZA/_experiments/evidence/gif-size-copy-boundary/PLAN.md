# GIF size/copy preconditions — method A

Question: does 0020F310 return a full buffer extent, or a modulo-32-bit sum,
and what does collector 001DB660 actually pass to allocation and memcpy?
Consumer: FABLE legacy VIF/GIF mechanism; OPUS ABI/representation/preconditions.

Competing explanations: a widened total tracks the traversed packet; individual
steps and accumulated total have different widths; or the caller performs its
own overflow/length rejection before copying. The existing formulas are already
documented. Width, termination and copy boundaries are the target.

Method A is sufficient: verified shipping instructions distinguish these local
explanations. No isolated run or live setup is needed to qualify the dataflow.
Exact PE RuntimeFunction entries, bytes and decoded instructions are retained.
Read the complete helper and collector; preserve current consumer preimage.

Controls: gate-zero bypass and small PACKED/REGLIST/IMAGE/EOP paths; mathematical
threshold witnesses distinguish signedness, step width and accumulator wrap.
These are symbolic consequences of instructions, not original-code executions,
fixtures proving initialization, or actual multi-gigabyte packets.

Acceptance: exact byte/disassembly consistency, source widths/branches and caller
arguments support the limited statement. Invalidate if an intervening conversion,
guard, different PE extent or contrary current consumer changes the interpretation.
Stop rather than allocate huge payloads or infer native allocation/copy effects.

PC remains off. Reference is read only; no saves/configuration/process are touched.
No fresh cleanup/restoration receipt is claimed. Independent acceptance and canonical
propagation remain pending. Actual producer bounds and normal invocation are not
settled by local code. Owner changes are routed, never overwritten.
