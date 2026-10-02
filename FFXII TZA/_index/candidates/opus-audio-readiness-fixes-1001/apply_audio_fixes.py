"""apply_audio_fixes.py [--apply] - 18-Audio contradictions from the reconstruction-readiness map (cloud stream R),
each verified by OPUS at the bytes or against the page's own dated correction (OPUS, 2026-10-01).

The image check (audio_fixes_check.py) runs first. Each edit replaces exactly one occurrence of OLD (a newline in OLD
matches CRLF or LF; NEW takes the matched line ending). An edit is ALREADY when its TAG is present, so a struck
"~~OLD~~" in NEW cannot re-fire. Dry run by default; --apply writes. Prints FAILS n.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
A = os.path.join(DB, "18-Audio")
P = {
    "CSR": os.path.join(A, "Audio-Boundary", "CONTRACT-sound-request.md"),
    "REQ": os.path.join(A, "Audio-Boundary", "how-a-sound-request-becomes-a-voice.md"),
    "ENG": os.path.join(A, "Audio-Boundary", "what-the-engine-calls-to-make-a-sound.md"),
    "LAY": os.path.join(A, "the-spatial-audio-object-model.md"),
    "DRV": os.path.join(A, "sqex-sd-sound-driver-architecture.md"),
    "CBK": os.path.join(A, "Audio-Bank-And-Controller-Family", "CONTRACT-audio-bank-and-controller-family.md"),
    "BK": os.path.join(A, "Audio-Bank-And-Controller-Family", "audio-bank-and-controller-family.md"),
    "CSP": os.path.join(A, "CONTRACT-spatial-source-objects.md"),
    "SAB": os.path.join(A, "Sound-Bank-And-Voice-Formats", "sab-sound-bank-container.md"),
    "MCF": os.path.join(A, "the-music-control-file-and-the-bgm-stream.md"),
    "AREA": os.path.join(A, "how-the-music-changes-when-you-change-area.md"),
    "CFM": os.path.join(A, "CONTRACT-field-music-selection.md"),
    "CMC": os.path.join(A, "CONTRACT-music-control-file-and-bgm-stream.md"),
    "FADE": os.path.join(A, "Audio-Boundary", "how-a-sound-fades-the-ramp-and-its-six-curves.md"),
    "CFG": os.path.join(A, "Sound-Bank-And-Voice-Formats", "sead-win-config.md"),
    "TRG": os.path.join(A, "Sound-Selection", "sound-trigger.md"),
    "WVAR": os.path.join(A, "which-variation-of-a-sound-you-hear.md"),
    "VAR": os.path.join(A, "Sound-Selection", "sound-variant-selection.md"),
    "ANIM": os.path.join(A, "how-an-animation-makes-a-sound.md"),
    "VPK": os.path.join(A, "the-voice-pack-slots-and-the-voice-verbs.md"),
    "R0": os.path.join(A, "README.md"),
    "R1": os.path.join(A, "Sound-Bank-And-Voice-Formats", "README.md"),
}
C = "corrected 2026-10-01, OPUS"
EDITS = [
    # item 2 - 003A13F0 is the boot bank setup; it writes -1 to A twice and C once, never B
    ("CSR", "and all three reset to `-1` by the 582-byte\nteardown `003A13F0`.",
     "and ~~all three reset to `-1` by the 582-byte\nteardown `003A13F0`~~ *(" + C + ": `003A13F0` is the 582-byte boot bank "
     "setup, called only from `00266D10`; after its requests it writes -1 to A at `003A14BE` and `003A153D` and to C at "
     "`003A15BC`, and never writes B - §14 `SR-2`, §15)*.", "582-byte boot bank setup, called only from"),
    ("REQ", "(`003A14E9`, `003A1568`, `003A15E7`); it first resets all three to `−1`.",
     "(`003A14E9`, `003A1568`, `003A15E7`); ~~it first resets all three to `−1`~~ *(" + C + ": after its requests it "
     "writes −1 to A at `003A14BE` and `003A153D` and to C at `003A15BC`; B is never written)*.",
     "after its requests it writes −1 to A at"),
    ("REQ", "| `003A13F0` | `Audio_ReleaseBankSlots` | 582 B | invalidates `02AEF3FC` to `0xFFFFFFFF` |",
     "| `003A13F0` | ~~`Audio_ReleaseBankSlots`~~ the boot bank setup *(" + C + "; only caller `00266D10`)* | 582 B | "
     "~~invalidates `02AEF3FC` to `0xFFFFFFFF`~~ clears the 9 bytes at `02AEF3F0`, builds the slot list, requests the "
     "three banks, and writes −1 to A (`003A14BE`, `003A153D`) and C (`003A15BC`); never B |",
     "the boot bank setup *(" + C + "; only caller"),
    # item 1 - a NON-ZERO from 003603C0 refuses
    ("CSR", "`002DF236 cmp ecx, -1` / `je` and `002DF23B call 003603C0` / `test eax, eax` / `je` both land on\n"
            "`002DF244 xor eax, eax`.",
     "~~`002DF236 cmp ecx, -1` / `je` and `002DF23B call 003603C0` / `test eax, eax` / `je` both land on\n"
     "`002DF244 xor eax, eax`.~~ *(Corrected 2026-10-01, OPUS, at the bytes: `002DF236 cmp ecx, -1` / `je` lands on "
     "`002DF244 xor eax, eax`, but after `002DF23B call 003603C0` / `test eax, eax` the `je` at `002DF242` jumps to the "
     "work at `002DF256`, so it is a NON-ZERO gate value that falls through to `002DF244` - as §10 row 5 and §12 say.)*",
     "so it is a NON-ZERO gate value that falls through"),
    ("CSR", "`ecx == -1` or a\nzero from `003603C0` returns 0 immediately;",
     "`ecx == -1` or a\n~~zero~~ **non-zero** *(" + C + ": `test eax, eax` / `je 002DF256` at `002DF240`)* from `003603C0` "
     "returns 0 immediately;", "**non-zero** *(" + C + ": `test eax, eax`"),
    # item 34 - 00210C50 is read (SR-7)
    ("CSR", "**`00210C50` remains\n   unread**, and is now the whole of what `SR-1` asked.",
     "~~**`00210C50` remains\n   unread**, and is now the whole of what `SR-1` asked.~~ *(Superseded: `00210C50` is read - "
     "`SR-7`, ANSWERED 2026-09-12, below: a sibling of the fork through the same `[rcx+8]` / `[rcx+0x10]` pair. Struck "
     "2026-10-01, OPUS.)*", "a sibling of the fork through the same `[rcx+8]`"),
    # item 35 - isolated execution exists
    ("CSR", "| any execution of this path, isolated or live | **none**; §13 | none | UNKNOWN |",
     "| any execution of this path, isolated or live | ~~**none**; §13~~ *(Corrected 2026-10-01, OPUS: isolated "
     "original-code execution exists - §13, 326 comparisons over six bodies with 0 mismatches, and §13a's EXP-096 / "
     "EXP-105; nothing live)* | none live | UNKNOWN for live |", "isolated original-code execution exists - §13, 326"),
    # item 3 - 002DF010 passes both 0x40 and 0x7F
    ("REQ", "| 61 B | same shape, passes only `0x40` |",
     "| 61 B | same shape, ~~passes only `0x40`~~ passes `r8d = 0x40` and `r9d = 0x7F` into `001DBDB0` "
     "(`002DF03F`, `002DF02B`) *(" + C + ")* |", "passes `r8d = 0x40` and `r9d = 0x7F` into"),
    # item 4 - +0x03 is the slot index, returned by 00361630
    ("REQ", "  +0x03  u8   handle      the value returned to callers",
     "  +0x03  u8   index       the slot's own index 0-3, written by 00360C70 and returned by 00361630;\n"
     "                          00360C20 returns +0x00 instead (" + C + ")", "written by 00360C70 and returned by 00361630"),
    ("REQ", "`+2` flags, `+3` handle |",
     "`+2` flags, `+3` slot index (returned by `00361630`; " + C + ") |", "`+3` slot index (returned by `00361630`"),
    # item 6 - the divisor is 1,000
    ("REQ", "`+0x3C` = `id / 100` (the `0x10624DD3` magic divide — the bank/section group)",
     "`+0x3C` = ~~`id / 100`~~ `id / 1000` (the `0x10624DD3` magic divide — the bank's block number; *" + C +
     ": `0x10624DD3` with `sar 6` divides by 1,000*)", "the bank's block number; *" + C),
    ("REQ", "The `id / 100` group at `+0x3C` is measured (`imul 0x10624DD3`, `sar 6`, sign\nfixup — round-toward-zero divide by 100).",
     "The ~~`id / 100`~~ `id / 1000` group at `+0x3C` is measured (`imul 0x10624DD3`, `sar 6`, sign\nfixup — "
     "round-toward-zero divide by ~~100~~ 1,000 *(" + C + "; the SAB page's §3 had it right)*).",
     "divide by ~~100~~ 1,000 *(" + C),
    # item 7 - the gate is raised in state 10; +0xD4 == 0x42 gates the teardown
    ("ENG", "in the sub-state entered when its\n    parameter `+0xD4` is `0x42`;",
     "~~in the sub-state entered when its\n    parameter `+0xD4` is `0x42`~~ in state 10 of its own state word `+0xC0` "
     "(message 2) *(" + C + ": `0027F646`-`0027F67B`; `+0xD4 == 0x42` at `0027F629` only gates the teardown call at "
     "`0027F632` under message 15)*;", "in state 10 of its own state word `+0xC0`"),
    # item 5 - 003A0E20's argument order
    ("LAY", "tails `002DF4D0(cl, cl>>8, edx, r8d)`",
     "tails ~~`002DF4D0(cl, cl>>8, edx, r8d)`~~ `002DF4D0((ecx >> 8) & 0xFF, ecx & 0xFF, edx, r8d)` *(" + C +
     ": `003A0E3C movzx ecx, cl` after `shr ecx, 8` is the first argument, `003A0E30 movzx edx, cl` the second)*",
     "`002DF4D0((ecx >> 8) & 0xFF, ecx & 0xFF, edx, r8d)`"),
    # item 15 - LAY's superseded rows, Ambient's own slots, the five modes; DRV's +0xE0
    ("LAY", "| `DirectionSound` | **no** — its heavy method is slot 7, `007F1EC0` | `rsqrtps` ×1 |",
     "| `DirectionSound` | ~~**no** — its heavy method is slot 7, `007F1EC0`~~ **yes** - superseded by the 2026-09-14 "
     "correction below | `rsqrtps` ×1 |", "**yes** - superseded by the 2026-09-14 correction below | `rsqrtps`"),
    ("LAY", "| `AmbientSound` | **no override at all** | none |",
     "| `AmbientSound` | ~~**no override at all**~~ **yes** - a constant position (`007F1D10`); superseded by the "
     "correction below | none |", "**yes** - a constant position (`007F1D10`); superseded"),
    ("LAY", "> | 7 | `007F0210` (262 B) |",
     "> | 7 | `007F0210` (262 B), inherited from `SoundSourceObject` (" + C + ") |",
     "inherited from `SoundSourceObject` (" + C),
    ("LAY", "> - **Slot 7 is per-class in all five.**",
     "> - ~~**Slot 7 is per-class in all five.**~~ *(Corrected 2026-10-01, OPUS: in four of five - `AmbientSound`'s slot "
     "7 is `SoundSourceObject`'s own `007F0210`.)*", "in four of five - `AmbientSound`'s slot"),
    ("LAY", "- **`AmbientSound` has no spatial method**, so nothing about listener position can affect it.",
     "- ~~**`AmbientSound` has no spatial method**, so nothing about listener position can affect it.~~ *(Superseded "
     "2026-09-14, CO-4: its slot 34 writes a constant position, so listener position still does not move it. Struck "
     "2026-10-01, OPUS.)*", "its slot 34 writes a constant position, so listener position"),
    ("LAY", "It contributes five slots of its own (0, 1, 7, 34, 35), not three.",
     "~~It contributes five slots of its own (0, 1, 7, 34, 35), not three.~~ *(Corrected 2026-10-01, OPUS, from the "
     "vtable bytes: it differs from `SoundSourceObject` (`01CB98A8`) at slots 0, 1, 34, 35 and 39, but slot 1 "
     "(`007E3260`) and slot 39 (`007E57B0`) are shared stubs and slot 7 (`007F0210`) is the parent's own entry, so its own "
     "bodies are 0, 34 and 35 - three, as `UQ-267` says.)*", "so its own bodies are 0, 34 and 35 - three"),
    ("LAY", "| Slot 34 overridden by Point / Polygon / Dynamic and not by Ambient |",
     "| ~~Slot 34 overridden by Point / Polygon / Dynamic and not by Ambient~~ *(Superseded 2026-09-14, CO-4: all five "
     "override slot 34; Ambient's writes a constant position. Struck 2026-10-01, OPUS.)* |",
     "all five override slot 34; Ambient's writes a constant position. Struck"),
    ("LAY", "| `+0x104` | **mode byte** — `0` selects nearest-vertex, non-zero selects plane-and-edges |",
     "| `+0x104` | **mode byte** — ~~`0` selects nearest-vertex, non-zero selects plane-and-edges~~ 0-4: point set, "
     "polyline, triangle strip, triangle fan, triangle list *(superseded by the CO-8 box above; struck 2026-10-01, "
     "OPUS)* |", "0-4: point set, polyline, triangle strip"),
    ("DRV", "setting the ready byte `+0xE0`",
     "setting ~~the ready byte~~ the audibility byte *(C-SP `SA-3`; " + C + ")* `+0xE0`",
     "the audibility byte *(C-SP `SA-3`; " + C),
    # item 8 - +0x20 is a member object (the controller's bank pool), not a second base
    ("CBK", "        +0x20  a SECOND BASE SUBOBJECT -- present in four of six (AC-3)",
     "        +0x20  the controller's embedded bank pool, a member object -- in four of six (AC-3, corrected 2026-10-01)",
     "the controller's embedded bank pool, a member object -- in four"),
    ("CBK", "**AC-3 — That extra slot is a SECOND BASE, and it is present in exactly four of six.** Each of the",
     "**AC-3 — That extra slot is ~~a SECOND BASE~~ a member-object thunk *(" + C + ", on BK `BD-4` and the bytes: "
     "`00217FD0` constructs the member at `lea rcx, [rbx+0x20]` through `00217E10`, the pool template; RTTI lists one "
     "base)*, and it is present in exactly four of six.** Each of the", "a member-object thunk *(" + C),
    ("CBK", "before dispatch is the `this`-adjustment for a secondary base subobject at `+0x20`. *The four\n"
            "targets being separate 161-byte bodies rather than one folded body is what makes this four\n"
            "inheritance paths and not one.*",
     "before dispatch is ~~the `this`-adjustment for a secondary base subobject at `+0x20`. *The four\n"
     "targets being separate 161-byte bodies rather than one folded body is what makes this four\n"
     "inheritance paths and not one.*~~ the call into the bank pool embedded at `+0x20`; the four 161-byte targets are one "
     "body that differs only in the per-type bank constructor it calls *(" + C + ")*.",
     "the call into the bank pool embedded at `+0x20`; the four 161-byte"),
    ("CBK", "drain the request queue (slot 7, where present)",
     "~~drain the request queue~~ take a free bank from the pool (slot 7, where present)",
     "take a free bank from the pool (slot 7, where present)"),
    ("CBK", "its queue drain is reached directly instead",
     "its ~~queue drain~~ pool step is reached directly instead", "its ~~queue drain~~ pool step"),
    ("CBK", "- What the secondary base at `+0x20` **is** — AC-3 establishes that four controllers have one and\n"
            "  that its methods are four separate bodies, not what interface it implements.",
     "- ~~What the secondary base at `+0x20` **is** — AC-3 establishes that four controllers have one and\n"
     "  that its methods are four separate bodies, not what interface it implements.~~ *(Superseded: it is no base; "
     "BK `BD-4` reads it as the controller's bank pool. Struck 2026-10-01, OPUS.)*",
     "it is no base; BK `BD-4` reads it as the controller's bank pool"),
    # item 10 - six bits
    ("CBK", "Slot 10 is a FIVE-BIT COMMAND MASK on one shared manager byte",
     "Slot 10 is a ~~FIVE-BIT~~ SIX-BIT *(" + C + ": bits 0x01-0x20, the six tests listed below)* COMMAND MASK on one "
     "shared manager byte", "SIX-BIT *(" + C + ": bits 0x01-0x20"),
    ("CBK", "- What the five commands of AC-6's mask mean to a player.",
     "- What the ~~five~~ six commands of AC-6's mask mean to a player.", "~~five~~ six commands of AC-6"),
    ("BK", "a five-bit command mask.**", "a ~~five-bit~~ six-bit command mask** *(" + C + ": `0x01`-`0x20`)*.",
     "six-bit command mask** *(" + C),
    # item 9 - the vtable load is inside the loop
    ("BK", "`rax = [this]` loaded once before the loop,",
     "~~`rax = [this]` loaded once before the loop~~ `rax = [this]` reloaded every iteration - `00222580` is the "
     "loop-back target of `00222596` *(" + C + ", as C-BK AC-4 says)*,", "reloaded every iteration - `00222580` is the"),
    # item 11 - the base constructor is 00212710
    ("BK", "and the base constructor `002130E0` zero-fills `+0x08`–`+0x38` as plain\n      data.",
     "and ~~the base constructor `002130E0` zero-fills `+0x08`–`+0x38` as plain\n      data~~ the base constructor "
     "`00212710` builds only the entry list at `+0x08` / `+0x10`, and each derived "
     "constructor then builds the member at `+0x20` (e.g. `00217FD0` -> `00217E10`) *(" + C + ": `002130E0` installs "
     "`00906DC8`, the `DynGeoFontTextInstance` vtable, and its only caller is `001E8580`)*.",
     "the base constructor `00212710` builds only the entry list"),
    ("BK", "  - The base constructor `002130E0` is used by a 3,572-byte Presentation body.",
     "  - ~~The base constructor `002130E0` is used by a 3,572-byte Presentation body.~~ *(Struck 2026-10-01, OPUS: "
     "`002130E0` is not this family's base constructor - it builds a `DynGeoFontTextInstance`; the family's base "
     "constructor is `00212710`.)*", "is not this family's base constructor - it builds"),
    # item 12 - the lazy object lives at +0x20; +0x50 is a separate bank field; 00221780 is the AudioBank base ctor
    ("BK", "The +0x50 field the Sep slot-8 bodies require non-null is the driver's voice/handle object\n"
           "(lazy-created through `00221D10` → `00221710` → `00220CE0`); `00221780` constructs the callback\n"
           "wrapper it carries (vtable `009078B0`).",
     "~~The +0x50 field the Sep slot-8 bodies require non-null is the driver's voice/handle object\n"
     "(lazy-created through `00221D10` → `00221710` → `00220CE0`); `00221780` constructs the callback\n"
     "wrapper it carries (vtable `009078B0`).~~ *(Corrected 2026-10-01, OPUS, at the bytes: the Sep slot-8 body "
     "`00222F20` requires `+0x50` non-null (`00222F26`) and passes it to `007A48C0` (`00222F61`); the voice/handle object "
     "it also needs is cached at `+0x20`, lazily created through `00221D10` -> `00221710` -> `00220CE0` (`00221D16`, "
     "`00221D47`), as SWE2-EC7-68 below says. `00221780` is the `AudioBank` base constructor (vtable `009078B0`).)*",
     "the Sep slot-8 body `00222F20` requires `+0x50` non-null"),
    # item 13 - BR-8's withdrawn sentences
    ("BK", "so 2 concurrent music voices, 96 environmental, 256\n> effect, 4 stream and 6 shout records exist to be handed out, "
           "and a request for a seventh shout\n> or third music voice finds the free set empty. That the free set's "
           "consumer is the voice-acquire\n> path is the reading the controller names and the set structure give; the "
           "acquire function was\n> not read here.",
     "~~so 2 concurrent music voices, 96 environmental, 256\n> effect, 4 stream and 6 shout records exist to be handed out, "
     "and a request for a seventh shout\n> or third music voice finds the free set empty. That the free set's consumer is "
     "the voice-acquire\n> path is the reading the controller names and the set structure give; the acquire function was\n"
     "> not read here.~~ *(Struck 2026-10-01, OPUS, as the 2026-09-18 correction above withdrew it: so at most 2 Music, "
     "96 Seb, 256 Sep, 4 Stream and 6 Shout bank objects can be live at once; voices come from the shared 1024-record "
     "pool, `UQ-244`.)*", "so at most 2 Music, 96 Seb, 256 Sep, 4 Stream and 6 Shout bank objects"),
    # item 14 - C-BK exists
    ("CSP", "the bank and controller\n> family remains uncontracted and this document does not claim it.",
     "the bank and controller\n> family ~~remains uncontracted and this document does not claim it~~ is contracted "
     "separately in `Audio-Bank-And-Controller-Family/CONTRACT-audio-bank-and-controller-family.md` (2026-09-22; "
     "*" + C + "*).", "is contracted separately in `Audio-Bank-And-Controller-Family/CONTRACT"),
    ("CSP", "| **Uncontracted** | [the bank and controller family](Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md) — S-41's remaining page, not claimed here |",
     "| **Sibling** | [the bank and controller family](Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md) — "
     "~~S-41's remaining page, not claimed here~~ contracted in its own CONTRACT page since 2026-09-22 (" + C + ") |",
     "contracted in its own CONTRACT page since 2026-09-22 (" + C),
    ("CSP", "- The bank and controller family, S-41's other uncontracted page.",
     "- ~~The bank and controller family, S-41's other uncontracted page.~~ *(Superseded: it has its own contract "
     "since 2026-09-22. Struck 2026-10-01, OPUS.)*", "it has its own contract since 2026-09-22. Struck"),
    ("CSP", " — S-41's remaining page\n", " — ~~S-41's remaining page~~ contracted separately (" + C + ")\n",
     "~~S-41's remaining page~~ contracted separately"),
    # item 33 - SAB's stale section-7 bullets (the 350-value count stays: unsettled)
    ("SAB", "- **`+0x05` and `+0x0A` are undecided.** `+0x05` is a 0/1 split of 512 against 4,097; `+0x0A` is\n"
            "  constant `10000` in `.mab` and takes 350 values in `.sab`. Neither is read by the two functions\n"
            "  read here, so both are `Inert` **with respect to those functions only**, not proven unread by the\n"
            "  program. → `PROPOSED-repos-4b-11`",
     "- ~~**`+0x05` and `+0x0A` are undecided.** `+0x05` is a 0/1 split of 512 against 4,097; `+0x0A` is\n"
     "  constant `10000` in `.mab` and takes 350 values in `.sab`. Neither is read by the two functions\n"
     "  read here, so both are `Inert` **with respect to those functions only**, not proven unread by the\n"
     "  program. → `PROPOSED-repos-4b-11`~~ *(Superseded, struck 2026-10-01, OPUS: §3 (2026-09-21) finds the reader "
     "`007EE01D movzx ebx, word [rcx+0xA]` / `007EE02B cmp bx, 1`, which zeroes `frpan` when `+0x0A` is 1, and the map "
     "sound list page (2026-09-27) gives `+0x0A` as a per-folder ordinal 0-267 and `+0x05` as the block / per-sound "
     "split. Whether the 350 distinct values in all `.sab` files agree with 268 `se` folders plus the `shout` banks is "
     "not re-counted here.)*", "finds the reader `007EE01D movzx ebx, word [rcx+0xA]`"),
    ("SAB", "- **How the 4,345 `se` banks are addressed is not established.** Their paths are not in the binary,\n"
            "  and path-table kind 33 begins with `shout` entries. → `PROPOSED-repos-4b-12`",
     "- ~~**How the 4,345 `se` banks are addressed is not established.** Their paths are not in the binary,\n"
     "  and path-table kind 33 begins with `shout` entries. → `PROPOSED-repos-4b-12`~~ *(Superseded: answered in §3 "
     "(2026-09-18) - the 248 block banks open through `%s/se%03d/se%03d%s`, the other 4,097 through the factory "
     "`00222DC0` with `%s/se%03d/se%06d%s`. Struck 2026-10-01, OPUS.)*", "the 248 block banks open through"),
    # ---- prose and data items (second verification pass) ----
    # item 19 - SEAD handle calls, WASAPI backend
    ("MCF", "(the XAudio-side calls)",
     "(~~the XAudio-side calls~~ SEAD handle-level driver calls that queue commands to the sound thread; the backend is "
     "WASAPI - *" + C + "*)", "SEAD handle-level driver calls that queue commands"),
    # item 20 - 0x40 is the pan, 0x7F the volume
    ("MCF", "`002256F0(arg4 = 0x7F, the volume)`,\n`002257E0(arg3 = 0x40)`",
     "~~`002256F0(arg4 = 0x7F, the volume)`,\n`002257E0(arg3 = 0x40)`~~ `002256F0(arg3 = 0x40, the pan: (v - 0x40) / 128, "
     "centre)`, `002257E0(arg4 = 0x7F, the volume: v / 127 = 1.0)` *(" + C + ": `002252DA mov ebp, r8d` / `00225367 mov "
     "edx, ebp` feeds the pan setter, `002252E5 mov esi, r9d` / `00225374 mov edx, esi` the volume setter)*",
     "the pan: (v - 0x40) / 128, centre)`"),
    ("MCF", "What `0x40` and `0x7F` set on the bank (`002256F0` / `002257E0`) is not named. `FZ-15`.",
     "~~What `0x40` and `0x7F` set on the bank (`002256F0` / `002257E0`) is not named. `FZ-15`.~~ *(Answered from the "
     "setters, 2026-10-01, OPUS: `002256F0` takes `0x40` as the pan, `(v - 0x40) / 128` = 0, centre (`00225750`); "
     "`002257E0` takes `0x7F` as the volume, `127 / 127` = 1.0 (`0022581F`); both fade over `r8 / 60` s, 0 here. "
     "`FZ-15`.)*", "takes `0x40` as the pan"),
    ("MCF", "the `bgmstreamstop` close this page's state 6 names",
     "the `bgmstreamstop` close ~~this page's state 6 names~~ (§3.2; state 6 calls `002DF680` - *" + C + "*)",
     "state 6 calls `002DF680` - *" + C),
    # item 21 - the largest span is 22
    ("MCF", "`span` **0 in 169** (max 5)",
     "`span` **0 in 169** (~~max 5~~ max 22, *" + C + ", re-walking the shipped file; §2.3 had it right*)",
     "max 22, *" + C + ", re-walking"),
    # item 23 - the musicinfo pointer typo
    ("AREA", "`[022DBA50]` live", "~~`[022DBA50]`~~ `[022CBA50]` *(typo " + C + "; `00361014`)* live",
     "`[022CBA50]` *(typo " + C),
    # item 24 - 10 mutants
    ("CFM", "the 22 cases and 20 mutants stay as recorded.",
     "the 22 cases and ~~20~~ 10 mutants *(" + C + ": `result.json` and EXP-099 record 10)* stay as recorded.",
     "~~20~~ 10 mutants *(" + C),
    # item 25 - the producer is answered, the lifetime is not
    ("CFM", "the table producer and lifetime (`DG-1`),",
     "~~the table producer and lifetime (`DG-1`)~~ an observed run of the table producer (its chain is read statically, "
     "§14.1) and the table's lifetime after binding (`DG-1`'s open half) *(" + C + ")*,", "`DG-1`'s open half"),
    ("CMC", "contract: Load the music-control table once per process and rebase it in place",
     "contract: Load the music-control table (one writer; how often it is bound is not established, MC-1) and rebase it "
     "in place", "(one writer; how often it is bound is not established, MC-1)"),
    # item 26 - dt is traced and cannot be negative
    ("FADE", "`dt` itself (the `xmm1` argument) was not traced, so a negative\n> step is not ruled out.",
     "~~`dt` itself (the `xmm1` argument) was not traced, so a negative\n> step is not ruled out.~~ *(Superseded by §4's "
     "trace, struck 2026-10-01, OPUS: `dt` is the frame time `007A5400` computes from an unsigned QPC difference "
     "(`007A5452`-`007A5488`), passed through `007AAEA0` (`007AAECD` -> `007AB030`), so a negative step cannot occur.)*",
     "the frame time `007A5400` computes from an unsigned QPC difference"),
    # item 27 - curve 0 is linear
    ("CFG", "arms compute\n`1−(1−t²)³`, `1−(1−t)²`, `t²`, `powf(C,t)−1` and `C−powf(C,1−t)` (`C = [01CEBC08]`, via\n"
            "`00861F6E`), default `0`.",
     "arms compute\n`t` (id 0, linear), `1−(1−t²)³`, `1−(1−t)²`, `t²`, `powf(C,t)−1` and `C−powf(C,1−t)` (ids 1-5; "
     "`C = [01CEBC08]`, via\n`00861F6E`); ~~default `0`~~ an id above 5 returns 0 *(" + C + ": arm 0 at `007A9F17` "
     "returns `t`; the out-of-range exit is `007A9F14`)*.", "an id above 5 returns 0 *(" + C),
    # item 28 - the ramp records start at +0x248; the parameters are named; 007E7300 is read
    ("TRG", "| `007BFEB0(i)` | `+0x254 + i*0x30`, i = 0, 1 |",
     "| `007BFEB0(i)` | ~~`+0x254 + i*0x30`~~ the ramp record at `+0x248 + i*0x30` (G-14), i = 0, 1 *(" + C + ")* |",
     "the ramp record at `+0x248 + i*0x30` (G-14), i = 0, 1"),
    ("TRG", "starting at `+0x254`,\nso index 0 reads `+0x254`/`+0x25C` and index 1 reads `+0x284`/`+0x28C`.",
     "~~starting at `+0x254`,\nso index 0 reads `+0x254`/`+0x25C` and index 1 reads `+0x284`/`+0x28C`.~~ *(Corrected "
     "2026-10-01, OPUS, per G-14: each is a ramp record at `+0x248 + i*0x30` - `+0x250` start, `+0x254` target, `+0x258` "
     "elapsed, `+0x25C` duration, `+0x264` curve mode; `007BFEB0` reads the duration and, when it is 0, returns the "
     "target.)*", "`+0x264` curve mode; `007BFEB0` reads"),
    ("TRG", "  +0x254  f32[]  parameter block, index 0   } stride 0x30, fields at +0x00 and +0x08\n"
            "  +0x284  f32[]  parameter block, index 1   } (i.e. +0x254 and +0x25C for index 0)",
     "  +0x248  ramp record, index 0: +0x250 start, +0x254 target, +0x258 elapsed, +0x25C duration,\n"
     "          +0x264 curve mode; index 1 at +0x278 (stride 0x30; G-14, corrected 2026-10-01, OPUS)",
     "+0x248  ramp record, index 0: +0x250 start"),
    ("TRG", "block(i) at this + 0x254 + i*0x30      (i = 0, 1)",
     "ramp(i) at this + 0x248 + i*0x30      (i = 0, 1; G-14, corrected 2026-10-01)", "ramp(i) at this + 0x248"),
    ("TRG", "-> FUN_007e7300   dispatch to playback   (unread)",
     "-> FUN_007e7300   dispatch to playback   (read, §2: arms state 1 -> 2)", "(read, §2: arms state 1 -> 2)"),
    ("TRG", "**Downstream:** `FUN_007e7300`, unread.",
     "**Downstream:** `FUN_007e7300`, ~~unread~~ read in §2 *(" + C + ")*.", "~~unread~~ read in §2 *(" + C),
    ("TRG", "Nothing here claims what they adjust — calling them \"volume\" or \"pitch\" would be a guess, and\n"
            "the naming discipline forbids it without an internal bridge.",
     "~~Nothing here claims what they adjust — calling them \"volume\" or \"pitch\" would be a guess, and\n"
     "the naming discipline forbids it without an internal bridge.~~ *(Superseded: G-14 (2026-09-17) names them through "
     "the `Set*` siblings - pitch, panning and lowpass; `007BFE30`'s is volume-shaped, its setter unnamed. Struck "
     "2026-10-01, OPUS.)*", "names them through the `Set*` siblings - pitch, panning and lowpass"),
    # item 29 - 007CF830 tests the weight byte
    ("WVAR", "**Read 2026-09-18 (FABLE): the predicate at `007CF830` asks whether a range is authored.**",
     "~~**Read 2026-09-18 (FABLE): the predicate at `007CF830` asks whether a range is authored.**~~ *(Corrected "
     "2026-10-01, OPUS, at the bytes `007CF834`-`007CF850`: it returns whether the candidate's WEIGHT byte - `+4` for "
     "versions 0-2, `+0x10` later, the byte `007CF9C0` returns and the random selects sum - is non-zero. The storage is "
     "shared with the range-minimum float, but the test means weighted, not range-authored: 1.0f reads 0 in that byte. "
     "See the sound-variant page's §11-§12.)*", "it returns whether the candidate's WEIGHT byte"),
    ("WVAR", "so it is a byte test on that float's low byte, true only when a range was authored.",
     "so it is a byte test on that float's low byte~~, true only when a range was authored~~.",
     "low byte~~, true only when a range was authored~~"),
    ("WVAR", "| `007CF830` | is a range authored (a byte test on the range field) |",
     "| `007CF830` | ~~is a range authored (a byte test on the range field)~~ is the candidate weighted (its weight byte "
     "non-zero; " + C + ") |", "is the candidate weighted (its weight byte non-zero"),
    ("WVAR", "the 007CF830 predicate read 2026-09-18 (is a range authored)",
     "the 007CF830 predicate read 2026-09-18 (is the candidate weighted - corrected 2026-10-01)",
     "(is the candidate weighted - corrected 2026-10-01)"),
    # item 30 - no uniform second pass
    ("VAR", "and\nselection always falls through to the uniform second pass §3 describes.",
     "~~and\nselection always falls through to the uniform second pass §3 describes~~ *(" + C + ", per §12: so pass 1 plays "
     "every set and the weighted roll finds nothing; there is no uniform second pass)*.",
     "per §12: so pass 1 plays every set"),
    # item 31 - the presentation PRNG
    ("ANIM", "**Gameplay - SHARED GENERATOR.** The picker draws from the gameplay random number generator; that is the "
             "crossing this\npage exists to record.",
     "~~**Gameplay - SHARED GENERATOR.** The picker draws from the gameplay random number generator; that is the crossing "
     "this\npage exists to record.~~ *(Superseded by CON-190 (2026-09-29), struck 2026-10-01, OPUS: **Presentation RNG - "
     "SERVICE.** The picker draws from the presentation bit-feedback PRNG, `003A6E60` on `01EF93E8`; no gameplay "
     "generator is touched.)*", "The picker draws from the presentation bit-feedback PRNG, `003A6E60`"),
    # item 32 - the voice-slot states
    ("VPK", "0 free · 1 already resident · 2 requested · 3 loaded · 4 · 5 loaded, sized",
     "0 free · 1 parked · 2 loading · 3 delivered · 4 dispose pending · 5 delivered, more owed (GA-4; corrected "
     "2026-10-01)", "1 parked · 2 loading · 3 delivered"),
    # item 36 - status banners and stale open items
    ("DRV", "**Status is PARTIAL and the scope limit is important.**",
     "~~**Status is PARTIAL and the scope limit is important.**~~ *(Superseded: the status is DOCUMENTED, owner "
     "re-status 2026-09-30; the scope note below is history. Struck 2026-10-01, OPUS.)*",
     "the status is DOCUMENTED, owner re-status 2026-09-30; the scope note below"),
    ("DRV", "**Why this document exists at PARTIAL:**",
     "~~**Why this document exists at PARTIAL:**~~ *(History - the status is DOCUMENTED since 2026-09-30; struck "
     "2026-10-01, OPUS.)* **Why this document was first written at PARTIAL:**",
     "**Why this document was first written at PARTIAL:**"),
    ("DRV", "**Still open:**\n        which rows of the options screen send commands `0x13`–`0x15` (the row procedures behind "
            "`00240750`) — `SD-22`.",
     "~~**Still open:**\n        which rows of the options screen send commands `0x13`–`0x15` (the row procedures behind "
     "`00240750`) — `SD-22`.~~ *(Superseded: `SD-22` ANSWERED 2026-09-30 - options rows 0x13-0x15 send the Music / Sound "
     "Effect / Voice volume commands. Struck 2026-10-01, OPUS.)*",
     "options rows 0x13-0x15 send the Music / Sound Effect / Voice volume commands"),
    ("DRV", "| `SQEX::Sd::Driver::Core::CoreSourceVoice` | 16 |",
     "| `SQEX::Sd::Driver::Core::CoreSourceVoice` | ~~16~~ 17 *(the vtable `01CB8360` has slots 0-16; " + C + ")* |",
     "~~16~~ 17 *(the vtable `01CB8360`"),
    ("VAR", "**PARTIAL.** `SwitchSound` is read",
     "~~**PARTIAL.**~~ *(Superseded: DOCUMENTED, owner re-status 2026-09-30; struck 2026-10-01, OPUS.)* `SwitchSound` is "
     "read", "DOCUMENTED, owner re-status 2026-09-30; struck 2026-10-01, OPUS.)* `SwitchSound`"),
    ("R0", "  **PARTIAL, tier 1.** The 64 voice slots",
     "  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** *(per the page's status line; " + C + ")*. The 64 voice slots",
     "**AUDITED, tier 1** *(per the page's status line"),
    ("R0", "_None yet._ **This is the second-largest owner category in the engine and is entirely undocumented.**",
     "~~_None yet._ **This is the second-largest owner category in the engine and is entirely undocumented.**~~ "
     "*(Superseded: the systems listed above are documented; struck 2026-10-01, OPUS.)*",
     "the systems listed above are documented; struck 2026-10-01"),
    ("R1", "**The largest undocumented hole in the database by file count.**",
     "~~**The largest undocumented hole in the database by file count.**~~ *(Superseded: the sab, seb, spp and config "
     "formats have AUDITED sheets; struck 2026-10-01, OPUS.)*", "the sab, seb, spp and config formats have AUDITED sheets"),
    ("CFG", "Which game\nsetting drives which category is not traced here.",
     "~~Which game\nsetting drives which category is not traced here.~~ *(Superseded by §7 and `SD-22`: the Music / Sound "
     "Effect / Voice settings drive categories 1 / 2 / 3 through commands 0x13 / 0x14 / 0x15. Struck 2026-10-01, OPUS.)*",
     "the Music / Sound Effect / Voice settings drive categories 1 / 2 / 3"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    chk = subprocess.run([sys.executable, "-B", os.path.join(HERE, "audio_fixes_check.py")], capture_output=True, text=True)
    last = (chk.stdout.strip().splitlines() or [""])[-1]
    print("CHECK", last)
    if last != "FAILS 0":
        print("REFUSING: the image check did not pass")
        print("FAILS 1")
        return 1
    for alias, old, new, tag in EDITS:
        path = P[alias]
        raw = open(path, "rb").read().decode("utf-8")
        if tag in raw:
            print("ALREADY %s: %s" % (alias, old[:50].replace("\n", " ")))
            continue
        assert tag in new, (alias, tag)
        pat = re.compile("\r?\n".join(re.escape(part) for part in old.split("\n")))
        hits = pat.findall(raw)
        if len(hits) != 1:
            print("REFUSING %s: old text occurs %d times: %s" % (alias, len(hits), old[:60].replace("\n", " ")))
            fails += 1
            continue
        m = pat.search(raw)
        eol = "\r\n" if ("\r\n" in m.group(0) or raw[m.end():m.end() + 2] == "\r\n") else "\n"
        repl = new.replace("\n", eol)
        raw2 = pat.sub(lambda m: repl, raw, count=1)
        if apply:
            open(path, "wb").write(raw2.encode("utf-8"))
            print("PATCHED %s: %s" % (alias, old[:50].replace("\n", " ")))
        else:
            print("WOULD PATCH %s: %s" % (alias, old[:50].replace("\n", " ")))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
