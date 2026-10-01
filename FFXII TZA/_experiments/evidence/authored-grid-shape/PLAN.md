# One shipped navigation header versus constructor quantization

H0: the present simplified cell-size description produces the same grid shape
on a shipped area header. H1: the original floorf+1 source formula differs on
at least one shipped header. Alternative H2: the extracted slot-4 grid is not
the grid header supplied to 00383740; settle the loader/codec path first.

Method A suffices: read exact original 00384160 loader/fixup and 00383740 getter,
verify the image and a single copied map pack by SHA, parse the slot-4 header
with existing documented layout and positive content controls, then apply the
already source-bound 003924B0 arithmetic to its dimensions. Retain the 3,200 B
slot4 blob and original function bytes. Compare the omitted-floor formula under
the same +1 addition, which is a generous control against the source. Check
nearest f32 initial sqrt ±2 ulps to reject a fragile boundary case.

Acceptance: a specific packed header whose loader/getter identity is established,
nonzero sizes/counts and valid region-list/table offsets, and distinct conditional
grid dimensions under stated f32 math. No capture claims initialized pointer,
ordinary area load/caller reachability, actual imported DLL effects, heap allocation
or global prevalence. Stop if identity/content controls fail; no broad map census.

Consumers: OPUS NavGridParams field/formula owner and FABLE navigation semantics;
independent SPEC review. The prior grid-constructor source package remains
separate and already routed. PC OFF, extracted/reference files read-only.
