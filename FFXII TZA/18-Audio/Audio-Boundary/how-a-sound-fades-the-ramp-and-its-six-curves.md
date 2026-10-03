---
system: How a sound fades — the parameter ramp and its six curves
category: 18-Audio
status: AUDITED
owner_layer: PrimaryOwner:Audio
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 20 addresses cited - 2 data, 4 entry, 13 interior, 1 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-fade-curves-pass-1
  crossref_clean: true
  reopened_count: 0
---

# How a sound fades — the parameter ramp and its six curves

## 1. What the player sees

Music that swells as you step into a room. A spell effect that trails away instead of stopping dead.
The battle theme ducking under a cutscene line. **None of those is a straight line** — the game has
**six named fade shapes**, and every fading sound picks one.

And a sound's loudness is not one fade. It is **all of its fades multiplied together**, times a
master level — so a track fading in while the whole mix ducks does both at once, and the result is
the product.

## 2. The ramp

Five fields, 48 bytes apart in an array:

```
ramp +0x08  f32  start value
ramp +0x0C  f32  target value
ramp +0x10  f32  elapsed
ramp +0x14  f32  duration      -- exactly 0.0 means "no ramp"
ramp +0x1C  i32  curve id, 0..5
                              stride 0x30 = 48 bytes
```

**Two independent functions read those same offsets**, which is why the layout is `PROVEN` rather
than inferred from one site: `007A9E00` (75 B) evaluates one ramp, and `007A9D30` (198 B) walks an
array of them. They agree field for field.

**In the type store as `AudioParameterRamp`** (2026-09-08) — `_types/`, validated by
`types_index.py`. Labelled **`SIGNATURE RESOLVED`, not `TYPE RESOLVED`**: the `0x30` stride is
proven, and ~~24 of those 48 bytes have no reader in either function (`0x000`–`0x008` and
`0x020`–`0x030`)~~ **28 of those 48 bytes have no reader in either function — `0x000`–`0x008`,
**`0x018`–`0x01C`** and `0x020`–`0x030`** (corrected 2026-09-13, §6). **The type store already
had this right**: `fields.tsv` carries `+0x018` as its own `UNRESOLVED` row. It was this
paragraph that dropped the middle gap, not the store.

### One ramp

```c
float Ramp_Value(const Ramp *r)              /* 007A9E00 */
{
    if (r->duration == 0.0f)                 /* ucomiss / jne at 007A9E0E */
        return r->target;                    /* snap, no interpolation at all */
    float t = r->elapsed / r->duration;      /* 007A9E29 divss                */
    float k = Ramp_Curve(t, r->curve);       /* 007A9E2D call 007A9E50        */
    return r->start + k * (r->target - r->start);
}
```

> **A duration of exactly zero is the "no fade" case**, and it is tested with an equality compare,
> not a threshold. A ramp given a very small non-zero duration does *not* take this path.

### All of them

```c
float Voice_Parameter(const Voice *v)        /* 007A9D30 */
{
    float acc = 1.0f;                        /* 01CEBBA8 = 1.0f               */
    const Ramp *r = v->ramps_40;
    for (int n = v->count_7C; n > 0; n--) {
        acc *= Ramp_Value(r);                /* inlined; same five offsets    */
        r = (const Ramp *)((const char *)r + 0x30);
    }
    acc *= v->master_4C;
    ...
}
```

**The parameter is a product, not a sum.** Every ramp is a multiplier in `[0,1]`-ish terms, the
master at `+0x4C` is one more, and `count == 0` leaves the accumulator at `1.0`.

## 3. The six curves, with their real constants

`007A9E50` (204 B, **63 callers**) is a six-arm jump table on the curve id, table at `007A9F1C`.
Every constant it uses is one of two: `01CEBBA8` = **1.0f** and `01CEBC08` = **2.0f**. `00861F6E` is
`powf`.

| id | assembly | formula | f(0) | f(1) |
|---:|---|---|---:|---:|
| **0** | *(arm entered at `007A9F17`, past the `xorps`)* | **`t`** — the identity; see §6 | 0 | 1 |
| **1** | `t² ; u = 1 − t² ; 1 − u³` | **`1 − (1 − t²)³`** | 0 | 1 |
| **2** | `u = 1 − t ; 1 − u²` | **`1 − (1 − t)²`** | 0 | 1 |
| **3** | `t * t` | **`t²`** | 0 | 1 |
| **4** | `powf(2, t) − 1` | **`2ᵗ − 1`** | 0 | 1 |
| **5** | `2 − powf(2, 1 − t)` | **`2 − 2¹⁻ᵗ`** | 0 | 1 |
| **> 5** | `ja` → **`007A9F14`**, a *different* entry that runs `xorps xmm0, xmm0` first | `0` | 0 | 0 |

**All ~~five~~ six real curves map 0 → 0 and 1 → 1** (corrected 2026-09-13, §6 — curve 0 is the
linear one). Reproduced by hand at the midpoint:

| id | `f(0.5)` | shape |
|---:|---:|---|
| 1 | `1 − (1 − 0.25)³` = **0.578** | fast start, long tail |
| 2 | `1 − 0.5²` = **0.75** | ease-out, strongest early |
| 3 | `0.25` | ease-in, slowest early |
| 4 | `2^0.5 − 1` = **0.414** | ease-in, gentler than `t²` |
| 5 | `2 − 2^0.5` = **0.586** | ease-out, gentler than curve 2 |

> **Curves 3 and 4 are ease-in; 1, 2 and 5 are ease-out**, and each pair differs only in how sharply.
> ~~Curve 0 is not a shape — it returns silence for the whole ramp, and it is also what an
> out-of-range id gets, because the bound check `cmp edx, 5 / ja` sends everything above 5 to the
> same arm.~~
>
> **⚠ Corrected 2026-09-13 (§6): curve 0 is the LINEAR fade, and it is not the same arm as the
> out-of-range case.** The jump table's entry 0 is **`007A9F17`** — *one byte past* the
> `xorps xmm0, xmm0` at `007A9F14` that the `ja` targets. Nothing between the function's entry
> and the `jmp rcx` touches `xmm0`, so **arm 0 returns `t` unchanged**. Out-of-range still
> returns `0`; **id 0 returns a straight line.**

## 4. Nothing clamps `t`

`007A9E00` and `007A9D30` both compute `elapsed / duration` and pass it straight in. **Neither clamps
it to `[0,1]`, and `007A9E50` does not either** — its only guard is on the curve *id*.

So if `elapsed` ever exceeds `duration`, the curves extrapolate: `t = 1.5` gives `t² = 2.25` on
curve 3, and `2^1.5 − 1 = 1.83` on curve 4. **Whether that can happen depends on whoever advances
`elapsed`, which this document did not read.** `DQ-1`.

> **`dt` is traced (2026-09-14, FABLE): it is real seconds.** `007A5400` computes
> (`QueryPerformanceCounter` − previous sample) / `QueryPerformanceFrequency` (`007AD630`, `007AD670` → `02EAD0C0`) and
> hands that float to `007AB5C0` and `007AAEA0` (`007A5452`–`007A54B2`). It cannot be negative: the tick difference is
> converted as unsigned (`jns` / `addsd 2^64`, `007A546C`). Ramp durations are therefore seconds, and the game-side callers convert from sixtieths with `/ 60.0`
> (`00222B70`; [the music-change page](../how-the-music-changes-when-you-change-area.md) §7).

> **Answered 2026-09-14 (FABLE, `DQ-1`): it cannot, because the advancer clamps.** The per-update ramp step is `007AA770`,
> called from `007AAEA0`. It walks both of a voice's ramp arrays: `[+0x38]` with count `+0x78`, and `[+0x40]` with count
> `+0x7C`, the array `007A9D30` multiplies. The stride is `0x30`. For each **active** ramp (byte `+0x20` set) it does:
>
> ```
> elapsed = elapsed + dt                      ; addss [rec+0x10]    007AA7D4 / 007AA834
> if (elapsed >= duration) {                  ; comiss vs [rec+0x14] 007AA7DD / 007AA83D
>     elapsed = duration; active = 0          ;                      007AA7E8-007AA7EE / 007AA848-007AA84E
> } else active = 1
> ```
>
> So `elapsed / duration` tops out at exactly 1.0, and a finished ramp stops advancing. A zero duration never divides:
> `007A9E00` returns the end value first. The music layer's ramps use the same clamp with the same record fields
> (`007C36C0` at `007C398F`, `007C4790` at `007C515A`). **An `elapsed` past `duration` would need a writer other than
> these advancers.** An image-wide search in the Sead span for the `addss [rec+0x10]` advance form found no unclamped
> instance, but writes of other forms were not censused. ~~`dt` itself (the `xmm1` argument) was not traced, so a negative
> step is not ruled out.~~ *(Superseded by §4's trace, struck 2026-10-01, OPUS: `dt` is the frame time `007A5400` computes from an unsigned QPC difference (`007A5452`-`007A5488`), passed through `007AAEA0` (`007AAECD` -> `007AB030`), so a negative step cannot occur.)*

## 5. What this does not claim

- **Which parameter these ramps drive.** The arithmetic is a normalised interpolation multiplied into
  a product with a master level, which is the shape of a volume chain — **but no caller was traced to
  a mixer field**, and the same machinery would serve pitch or a filter cutoff equally well. The
  ramp is proven; the destination is not.

  > **Answered 2026-09-14 (FABLE, `DQ-2`): `007A9D30` is a sound Category's *pitch* multiplier, not a volume.**
  > The object is not a voice.
  > - **The object is a `Category`.** `007AA770`, the per-update step of `DQ-1`, advances two ramp arrays on it: `+0x38`
  >   (count `+0x78`) and `+0x40` (count `+0x7C`). It follows `+0x58`, the referenced category that `007AA320`
  >   (*"Category::InitializeRefCategory"*, `01CB44B0`) installs.
  > - **Two products.** It takes `007A9F40` (array `+0x38`, master `+0x48`) and `007A9D30` (array `+0x40`, master
  >   `+0x4C`; `007AA89F`). Each is pushed to every live Sound, Music or kind-9 handle whose slot 24 (`+0xC0`, the
  >   sound header's byte `+6`) equals the category number at `+0x60`: the first through slot 5 (`+0x28`), the second
  >   through slot 6 (`+0x30`) (`007AA907`–`007AA936`). `007A9A10` does the same for a newly attached sound
  >   (`007A9C85`–`007A9CA5`).
  > - **Slot 6 is pitch.** For `Sound` it is `007BE3A0`: `+0x68`, dirty `+0x5D`. Among the Sound methods (`007BC000`–`007C1000`), the only reader of `+0x68` is slot 27,
  >   `007BD900`, which multiplies it into the `+0x188` ramp. `SetPitch` (slot 8, `007BE8A0`, *"Sound::SetPitch failed
  >   range over"*, range `0.001953125`–`2.0`) sets that ramp.
  > - **Slot 5 is volume.** `007BE3B0` writes `+0x64` (dirty `+0x5C`). Its only reader in that range is slot 26, `007BDBB0`: the
  >   header level `[+0x30]+0x0C` × four `0x40`-stride ramp entries (fields from `+0x90`) × `+0x64`.
  >   `SetVolume` (slot 7, `007BEAF0`, *"Sound::SetVolume failed range over"*, range `0.0`–`1.0`) ramps the first of
  >   those entries at `+0x88`.
  > - **`Music@Magi`** takes the same two slots: `007C9170` → `+0x5B0` and `007C9150` → `+0x5DC`.
  >
  > So §2's `Voice_Parameter` and `voice->+0x4C` name a Category and its pitch master. The same 48-byte ramp also
  > carries the Sound's own pitch (`+0x188`) and pan (`+0x1B8` / `+0x1E8` / `+0x218`,
  > [how a sound request becomes a voice](how-a-sound-request-becomes-a-voice.md) §7). Not read: who writes the two
  > masters `+0x48` / `+0x4C`, and how the config menu's volume options reach the Category. That is `G-3`.
- **That the curve ids have names in the data.** They are `0…5` as the jump table decides them. No
  authored table was found that names them, and the shapes above are the evidence, not a label.
- **What `007A9D30` does after the product.** It multiplies in `v->+0x4C` and continues; the rest of
  the function was not read.
- **Anything about voices, banks or routing.** Those are
  [the sound driver architecture](../sqex-sd-sound-driver-architecture.md) and
  [how a sound request becomes a voice](how-a-sound-request-becomes-a-voice.md); this document is one
  arithmetic layer and stops there.

## 6. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one query at a time and read in full.)*

### ⚠ Curve 0 is the linear fade, not silence — and it is a different arm from out-of-range

The jump table at **`007A9F1C`** decodes to six targets:

| id | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| arm | **`007A9F17`** | `007A9E76` | `007A9E9D` | `007A9EB9` | `007A9EC5` | `007A9EE2` |

and the bound check sends anything above 5 somewhere else:

```asm
007A9E57  cmp   edx, 5
007A9E5A  ja    0x7A9F14        ; <- out of range lands HERE
...
007A9F14  xorps xmm0, xmm0      ; 3 bytes
007A9F17  add   rsp, 0x38       ; <- arm 0 lands HERE, past the xorps
007A9F1B  ret
```

**Arm 0 is one byte past the zeroing instruction.** Between the function's first instruction and the
`jmp rcx` — `sub rsp, 0x38`, `movaps xmm3, xmm0`, `cmp`, `ja`, `movsxd`, `lea`, `mov ecx`,
`add rcx, rdx` — **nothing writes `xmm0`**, so `xmm0` still holds the caller's `t`. **Curve 0 returns
`t`: it is the plain linear fade**, the most ordinary shape of all, and the one §3 recorded as
returning silence.

Out-of-range genuinely does return 0 — that half stands — but the two are **separate exits**, not the
same arm. The player-facing consequence inverts: a sound on curve 0 does not go silent for the whole
ramp; **it fades in a straight line.**

### The other five curves reproduce instruction for instruction

| id | assembly, decoded | §3's formula |
|---:|---|---|
| 1 | `xmm3 = t²` ; `xmm2 = 1 − t²` ; `xmm1 = xmm2³` ; `1 − xmm1` | **`1 − (1 − t²)³`** ✓ |
| 2 | `xmm1 = 1 − t` ; `xmm1 ×= xmm1` ; `1 − xmm1` | **`1 − (1 − t)²`** ✓ |
| 3 | `xmm3 = t × t` | **`t²`** ✓ |
| 4 | `powf(2, t)` then `− 1.0` | **`2ᵗ − 1`** ✓ |
| 5 | `xmm1 = 1 − t` ; `powf(2, 1−t)` ; `2 − result` | **`2 − 2¹⁻ᵗ`** ✓ |

Only two constants appear — `01CEBBA8` and `01CEBC08` — and `00861F6E` is named **`powf`** in the
function list. `007A9E50` has **63** callers, exactly as §3 says.

`007A9E00` reproduces line for line: `ucomiss` at `007A9E0E`, `jne` to the interpolating path, the
snap returning `+0x0C`, `divss` at `007A9E29`, `call 007A9E50` at `007A9E2D`, then
`start + k·(target − start)` from `+0x08` and `+0x0C`. So does `007A9D30`: count from `+0x7C`, the
ramp array reached **through a pointer at `+0x40`**, `rbx` biased by `+0x14` so the loop reads
`[rbx]`, `[rbx−8]`, `[rbx−4]`, `[rbx+8]`, `[rbx−0xC]` — **the same five fields** — `add rbx, 0x30`
per step, `mulss` into the accumulator, and `× [rsi+0x4C]` at the end. The `count ≤ 0` path jumps
straight to `1.0 × master`.

### ⚠ The unread span is 28 bytes, not 24 — and the type store already knew

§2 lists the gaps as `0x000`–`0x008` and `0x020`–`0x030`. The readers touch `+0x08`, `+0x0C`,
`+0x10`, `+0x14` and `+0x1C` — **`+0x18` is touched by neither function**, so the unread span is
`0x00`–`0x07`, **`0x18`–`0x1B`** and `0x20`–`0x2F`: **28 bytes of 48**. `_types/fields.tsv` carries
`+0x018` as its own `UNRESOLVED` row, so **the store was right and the prose summarising it dropped a
gap.**

### §4's negative holds, and gets sharper

No `minss` or `maxss` appears anywhere in `007A9E00`, `007A9D30` or `007A9E50`. **The control is that
the instrument does see a guard when there is one** — it finds `cmp edx, 5 / ja` on the curve *id* in
the same listing. So `t` really is unclamped, and with curve 0 now known to be the identity the
consequence is blunter than §4's: on curve 0 an `elapsed` past `duration` passes **straight through**
as a multiplier greater than 1, with no exponent to soften it. `DQ-1` stands — whoever advances
`elapsed` was not read.

**Not claimed.** Which parameter the ramps drive — §5's first bullet stands; no caller was traced to a
mixer field here either. What the 28 unread bytes hold. What `007A9D30` does after the product.
Whether any shipped data selects curve 0 — **the arm is decoded, no authored table was searched**.
Nothing was executed and no sound was heard.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-how-a-sound-fades-the-ramp-and-its-six-c-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00222B70` | 95 B | calls `007A7010(rcx+0x38)` and, only when that returns non-zero, calls `007A81F0(rcx+0x38, ...)` with `xmm1` = `r9d` converted to float and divided by 127.0 (`00906A44`), `xmm2` = `r8d` converted to float and divided by 60.0 (`008F6D54`) and `r9d` = -1; when `007A7010` returns zero it returns without the second call | `00222B8C`, `00222B93`, `00222BAA`, `00222BB2`, `00222BBA` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-how-a-sound-fades-the-ramp-and-its-six-c-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `007A9D30` | 198 B | starts from the float 1.0 at `01CEBBA8` and, for each of the sign-extended dword `[rcx+0x7c]` records of 0x30 bytes starting at qword `[rcx+0x40]`, multiplies in a factor that is the record's float `+0xc` when its float `+0x14` equals 0.0, and otherwise `007A9E50(+0x10 / +0x14, edx = dword +0x1c)` times (`+0xc` - `+0x8`) plus `+0x8`; it then multiplies by float `[rcx+0x4c]` and returns the product in `xmm0` (a count of zero or below returns 1.0 times `[rcx+0x4c]`) | `007A9D77`, `007A9D90`, `007A9DAC`, `007A9DB6`, `007A9DDE` |
| `007A9F40` | 198 B | starts from the float 1.0 at `01CEBBA8` and, for each of the sign-extended dword `[rcx+0x78]` records of 0x30 bytes starting at qword `[rcx+0x38]`, multiplies in a factor that is the record's float `+0xc` when its float `+0x14` equals 0.0, and otherwise `007A9E50(+0x10 / +0x14, edx = dword +0x1c)` times (`+0xc` - `+0x8`) plus `+0x8`; it then multiplies by float `[rcx+0x48]` and returns the product in `xmm0` (a count of zero or below returns 1.0 times `[rcx+0x48]`) | `007A9F87`, `007A9FA0`, `007A9FBC`, `007A9FC6`, `007A9FEE` |
| `007AA320` | 186 B | negates the word at `+4` of the record qword `[rdx+8]` and returns 0 when the result is not positive (signed 16-bit); otherwise it calls `007AAA20` with that value sign-extended, stores the returned pointer to qword `[rcx+0x58]` and returns 0 when dword `+0x10` of it is non-zero; when that dword is zero it calls `0019C5D0(rsp+0x20, 0x100, 01CB44B0)` with `r9` not set in this body, writes a 0xa byte at the returned length (moved back by 2 when the length is 0xff or more) and a zero byte after it (calling `00809728` when that index reaches 0x100), calls through the qword at `008C2120` with `rsp+0x20` and then calls `007A5570(2, rsp+0x20)`, and returns -1; the stack cookie is checked through `00808C40` | `007AA346`, `007AA351`, `007AA371`, `007AA3A0`, `007AA3B0` |
| `007BE8A0` | 216 B | when `xmm1` is at least 0.001953125 (`008C5B30`) and not above 2.0 (`01CEBC08`) it calls `007CA560(rcx+0x188)` with `xmm1` and the other incoming registers, `r9d` = 0 and a zero byte stack argument, and returns that call's result; otherwise it calls `0019C5D0(rsp+0x30, 0x100, '[sead][!warn!]Sound::SetPitch failed range over %f', (double)xmm1)`, writes a 0xa byte at the returned length (moved back by 2 when it is 0xff or more) and a zero byte after it (calling `00809728` when that index reaches 0x100), calls through the qword at `008C2120` with `rsp+0x30` and then calls `007A5570(1, rsp+0x30)`, and returns -1; the stack cookie is checked through `00808C40` | `007BE8B9`, `007BE8C2`, `007BE8DA`, `007BE914`, `007BE953` |
