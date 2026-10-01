# Type-specific consumers of three movement-commit fields

Method A only: certified shipping EXE bytes, catalogued function sizes and the
reviewed operand-role adapter. The four preceding constant-store entries are
positive controls. Each selected step range decodes completely, but this scan
does not prove an image-wide function extent or follow every nested call.

| Node byte / store | Matching step | Direct observation in the step |
|---|---|---|
| `0x67`, `node+0x3D8 = 1` | `0045FD10`, 56 B | No direct `+0x3D8` operand in this bounded body; two calls remain. Consumer open. |
| `0x6B`, `node+0x3D4 = 1` | `00529D50`, 917 B | `0052A063 cmp [rbx+0x3D4],r13d`; unequal arm writes `r13d` at `0052A06C`. The scan sees `r13d` zeroed at `00529FEC`, but has not proved that every entry to the comparison passes that zero. |
| `0x71`, `node+0x434 = 1` | `0052A8B0`, 1273 B | `0052AD2E cmp [rbx+0x434],0`; nonzero arm writes zero at `0052AD37` before further work. |
| `0x72`, `node+0x3F8 = 1` | `0052B5E0`, 1519 B | `0052BB35 cmp [rbx+0x3F8],0`; nonzero arm calls `0052BBD0` at `0052BB45`. The callee's effects have not been established here. |

In all three bodies with a direct hit, original prologue code moves entry RCX to
RBX, with no explicit RBX write before the first hit. Intervening calls mean
that receiver continuity is conditional on their ordinary nonvolatile-register
ABI behavior; initialized instance identity and invocation timing are still
unobserved. Same displacement alone is not a receiver proof. These are
candidate type-specific readers and bounded conditional actions, not universal
flag meaning, exact frame scheduling, class preservation, or player-visible
effects. The `0x67` no-hit is strictly limited to its 56-byte body.

Next discriminator: verify the normal step-dispatch RCX provenance and the
specific nested effect of `0052BBD0`; for `0x67`, inspect the two actual callees
or other readers only if it affects the contract. Use existing type-method and
EC-7 work before new captures. No live session is needed to establish this
source-level boundary; initialized ownership/reuse and actual scheduling may
still require live FF12 later.
