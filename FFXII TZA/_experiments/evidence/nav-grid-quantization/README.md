# Original navigation-grid construction: subtract, quantize, partially reset

The original builder003924B0 uses a275-cell initial budget, floors its refined
cell size and adds exactly1.0, then computes the two grid dimensions. The current
type prose omits the flooring step; the unit-definition summary omits the36-byte
prefix subtraction. The corridor contract also names the wrong globals for the
cell size and origins. Current type fields already have the correct addresses.

PLAN.md states the questions/method/controls. source.json retains exact607B builder,
252B rectangle getter and10B reference decoder through their final RETs, exact
shipping6B sqrtf/floorf thunks, qualified DLL/import name bindings, operand-derived
globals, shipping1.0 bytes and consumer preimages. No exception metadata or
address-neighbourhood semantics. Typed TSV snapshots contain the exact relevant
rows/header, with their full parent-file hashes; they are not a census or mirror.

The source computation for positive finite dimensions is:

```text
n = 36
budget = trunc((0x2800 - n) / (n + 1)) = 275
w = maxA - minA; h = maxB - minB
c0 = sqrtf(f32(w*h) / f32(budget))
nx = trunc(f32(w/c0)); ny = trunc(f32(h/c0))
refined = maxss(f32(w/f32(nx)), f32(h/f32(ny)))
c = f32(floorf(refined) + 1.0f)
cols = trunc(f32(f32(w + f32(c - 1.0f)) / c))
rows = trunc(f32(f32(h + f32(c - 1.0f)) / c))
allocation argument = signed32(cols * rows * (n + 1) + n)
```

The additions/divisions/conversions follow the source's individual f32 operations.
This is **floor+1**, including at integer values, rather than an ordinary ceiling
or a tiny epsilon. The1.0 constant at01CEBBA8 is used at both addition/subtraction
sites. Qualified import names establish the intended math API; its loaded DLL
implementation/effects are not executed in this method-A package.

Two arithmetic illustrations show why the omitted operations matter:

| rectangle | original formula | omitted operation |
|---|---|---|
| 100×100 | refined6.25 → cell7 | skip floor → cell7.25 |
| 336×320 | budget275 → cell22,16×15,allocation argument8916 | budget276 → cell21,16×16,argument9508 |

The inputs fit the header's byte size/count representation, but no occurrence in
shipped maps is claimed. These are conditional f32 round-nearest calculations
assuming intended sqrtf/floorf, **not original execution or captured allocations**.
Original instructions establish the formula; a calculation does not prove itself.
No allocator capacity, grid-budget universal bound or leak is inferred.

The four rectangle outputs are the header-derived origins and maxima. The source
getter reads two signed16 origins and four byte size/count values; its codec is
included for reference arithmetic, not proof of a live arena/base value. Actual
loaded root/header identity and lifetime remain separate. Already-qualified
vestigial stack-copy fields074/084 remain as their current records describe them;
this package does not recensus readers or reopen their meaning.

Exact globals:070 origin A,078 origin B,080 maximum A,088 maximum B,090 cell size.
The corridor header currently says070 cell size and078/080 eps cells. Its linked
type fields already agree with the original producer/query interpretation; the
header needs propagation rather than another type system.

The builder writes02AEE0B8=36 **before** calling the rectangle getter. If the
nav root is null, the getter returns0 and the builder skips the later rectangle,
quantization/allocation path. Its own initial write still occurs, so "no-op if
getter returns zero" needs that exception. It may overwrite36 with36 in an
already-initialised state; no current game-state value or runtime frequency is
claimed. Cookie epilogue/native effects remain distinct from the local source claim.

check.py checks exact primary bytes/operands/import identities/constant, existing
correct field rows, disputed current prose and arithmetic discriminators.
observation.json normalises the source findings. validation.json is STATIC ONLY;
new isolated/native/live cases0. Independent SPEC review and OPUS/FABLE corrections
remain pending. Historical experiments/mutations are untouched; no final campaign.

Cleanup: reference/artifacts read-only, PC OFF, no game/native/input/instrument or
save/config/reference edits or fresh live restoration receipt. Live authorization
and persistent setup budget unchanged. Accepted whole L1+L2 remains NOT_MET.

Player version: nearby-object queries use a grid. Its cells are rounded to the
next whole size using a specific budget, and a missing map still performs one
small reset. Reproducing the simplified description can build a different grid.
