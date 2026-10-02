"""apply_input_fixes.py [--apply] - six 15-Input corrections from the reconstruction-readiness map (cloud stream R,
verified by OPUS 2026-10-01; contradictions G-C1x, G-C2x, G-C4x, G-C8x of the 15-Input map).

Checks the image first (input_fixes_check.py); then each edit is an exact, single-occurrence replacement.
Default is a dry run (WOULD PATCH); --apply writes. Byte-preserving (each file keeps its own EOLs), idempotent
(ALREADY when the new text is present and the old is not); prints FAILS n.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
IS = os.path.join(DB, "15-Input", "Input-Stack", "input-stack-device-channel-and-bindings.md")
KM = os.path.join(DB, "15-Input", "Binding-Profiles", "keymap-ini-file-format-and-default-controls.md")
R2 = os.path.join(DB, "15-Input", "Modal-Toggles", "r2-force-fight-toggle.md")
BC = os.path.join(DB, "15-Input", "Binding-Profiles", "CONTRACT-binding-profiles.md")
NC = os.path.join(DB, "15-Input", "Input-Name-Registry", "CONTRACT-input-name-registry.md")
NP = os.path.join(DB, "15-Input", "Input-Name-Registry", "the-input-name-registry-and-channel-aliases.md")
TAG = "corrected 2026-10-01, OPUS, from the 15-Input reconstruction-readiness map, re-read at the bytes"
PROP = "propagated 2026-10-01, OPUS, from the system page; register rows answered"

EDITS = [
    (IS,
     "| `001965E0` | 159 B | `InputManager_ValidateBindingIdRanges` — returns 1 when no profile is fully in range |",
     "| `001965E0` | 159 B | `InputManager_ValidateBindingIdRanges` — ~~returns 1 when no profile is fully in range~~ "
     "returns 1 unless profile 1 is fully in range: the outer pass repeats the same scan of profile 1 three times "
     "(`r11` is loaded once with `01F80F94` at `001965EB` and never advanced), so profiles 2 and 3 are range-checked "
     "by nothing *(" + TAG + "; the keymap page's validator section had it right)* |"),
    (IS,
     "(returns 1 when no profile is fully in range)",
     "(returns 1 unless profile 1 is fully in range - profiles 2 and 3 are not checked; see the table above)"),
    (KM,
     "| 488 B | copies 2 records `01F80130` → `01DF1738` |",
     "| 488 B | copies ~~2 records `01F80130` → `01DF1738`~~ **3 records of `0x15C`**: `01F80130` / `01F8028C` / "
     "`01F803E8` → `01DF1738` / `01DF1894` / `01DF19F0` (the `2` at `00196290` is the inner `0x80`-byte round count) "
     "*(" + TAG + ")* |"),
    (IS,
     "**`0x01DF15DC` is a staging buffer, not the authored defaults.** The prototype-copy census",
     "~~**`0x01DF15DC` is a staging buffer, not the authored defaults.**~~ *(Corrected 2026-10-01, OPUS: "
     "`0x01DF15DC` and `0x01DF1738` are records 1 and 2 of the five-record bank the poll walks every frame - "
     "`00197089` loads `01DF1480`, five rounds, `add rsi, 0x15c` at `001970BB` - so the publisher writes records "
     "2-4 of that live bank, not a scratch area. The keymap and binding-profile pages say the same. The rest of "
     "this paragraph is kept as written history.)* The prototype-copy census"),
    (IS,
     "**PARTIAL.** The three families,",
     "~~**PARTIAL.**~~ *(Superseded 2026-10-01, OPUS: the status line reads DOCUMENTED and every residue named "
     "below is answered.)* The three families,"),
    (R2,
     "**What the mode looks like on screen is not established**, and this document says so",
     "~~**What the mode looks like on screen is not established**~~ *(Superseded 2026-10-01, OPUS: it is the HUD's "
     "`FLEEING` label - see the correction under the overview and SD-2 in §7.)* This document said so"),
    (NC,
     "2. **Whether a channel value is what `keymap.ini` stores.** The keymap document proves",
     "2. ~~**Whether a channel value is what `keymap.ini` stores.**~~ *(Superseded: **ANSWERED 2026-09-22 (FABLE)** on "
     "the system page - the node `+0x18` value IS the keymap control code for buttons too, 13 of 13 worked examples, "
     "46 of 46 button values inside the band 11-27; " + PROP + ".)* The keymap document proves"),
    (NC,
     "3. **Whether the alias groups stay indistinguishable downstream.** They are one channel here;",
     "3. ~~**Whether the alias groups stay indistinguishable downstream.**~~ *(Superseded: **ANSWERED 2026-09-22 "
     "(FABLE)** on the system page - downstream separates mouse buttons, codes 1-3 on their own backend, from pad "
     "buttons, 11-27; but no name reaches codes 1-3, so `Button_LeftMB` binds the pad; " + PROP + ".)* They are one "
     "channel here;"),
    (NP,
     "- **That the alias groups are indistinguishable downstream.** They are one channel at the registry;",
     "- ~~**That the alias groups are indistinguishable downstream.**~~ *(Superseded: **`DM-1` ANSWERED 2026-09-22 "
     "(FABLE)** - downstream separates them completely, and no name reaches the mouse codes; see the `DM-1` section "
     "above. Struck 2026-10-01, OPUS.)* They are one channel at the registry;"),
    # G-C5x: the binding contract's open lists, superseded by dated register answers (pointers only)
    (BC, "| `DC-2` | the device gate",
     "| ~~`DC-2`~~ | *(Superseded: **ANSWERED 2026-09-14 (FABLE)**, register `DC-2` - statically the gate never "
     "closes: `001C1990` returns `[01F81268]`, whose one field is written once, `= 0`, by `001C1940`; " + PROP + ".)* "
     "the device gate"),
    (BC, "| `DC-3` | `008F3A28` = `120.0`,",
     "| ~~`DC-3`~~ | *(Superseded: **ANSWERED 2026-09-14 (FABLE)**, register `DC-3` - `120.0` is `WHEEL_DELTA` for the "
     "mouse-wheel binding mode 4; the load at `00197253` is hoisted and used at `00197383`; " + PROP + ".)* "
     "`008F3A28` = `120.0`,"),
    (BC, "| `BP-3` | the `(kind, code)` walk",
     "| ~~`BP-3`~~ | *(Superseded: **ANSWERED 2026-09-12 (FABLE)**, register `BP-3` - the walk is over the `0x140` "
     "runtime record's axis entries; " + PROP + ".)* the `(kind, code)` walk"),
    (BC, "| `BP-4` | what the 0–16384 triangular accumulator",
     "| ~~`BP-4`~~ | *(Superseded: **ANSWERED 2026-09-12 (FABLE)**, register `BP-4` - it is the controller "
     "vibration gain, which `0035F590` applies to the motors; " + PROP + ".)* what the 0–16384 triangular accumulator"),
    (BC, "| `BP-5` | why codes `0`, `4`–`10` exist",
     "| ~~`BP-5`~~ | *(Superseded: **CLOSED 2026-09-18 as `NO ADMISSIBLE SOURCE`** (proposed FABLE, signed OPUS), "
     "register `BP-5` - the shipped default profile binds none of them; " + PROP + ".)* why codes `0`, `4`–`10` exist"),
    (BC, "| new | the three bank writers `0015BD30`",
     "| ~~new~~ | *(Superseded: **ANSWERED 2026-09-26 (OPUS)**, register `AU-4` - the region is three blocks at "
     "stride `0x420`, each built by its own CRT initialiser before `main`; " + PROP + ".)* the three bank writers "
     "`0015BD30`"),
    (BC, "- **That the three banks are keyboard / pad / something else.**",
     "- ~~**That the three banks are keyboard / pad / something else.**~~ *(Superseded: register `UQ-143`, "
     "narrowed 2026-09-18 and 2026-09-25 (FABLE) - bank A's records 0 and 1 are the gamepad and mouse profiles, "
     "2-4 the three keyboard layouts, and the two conditional banks follow system-stop slots: the battle-menu bank "
     "and the menu / cutscene-lock bank; " + PROP + ".)*"),
    (BC, "- **Where group 2's four slots are consumed.**",
     "- ~~**Where group 2's four slots are consumed.**~~ *(Superseded: `00197710` is their read surface - "
     "the keymap page's \"Where the file's bindings are actually read\" section; " + PROP + ".)*"),
    (BC, "- **What records 0 and 1 of the bank at `01DF1480` hold.**",
     "- ~~**What records 0 and 1 of the bank at `01DF1480` hold.**~~ *(Superseded: register `UQ-143` - the "
     "gamepad and the mouse profiles; " + PROP + ".)*"),
    (BC, "- **What the axis entry's `+0x04` field means.**",
     "- ~~**What the axis entry's `+0x04` field means.**~~ *(Superseded: **ANSWERED 2026-09-18 (FABLE)**, register "
     "`UQ-144` - the fields are `{kind, subKind, codeA, codeB}`, and the 4 is a sub-kind only the mouse kind reads; "
     + PROP + ".)*"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    chk = subprocess.run([sys.executable, "-B", os.path.join(HERE, "input_fixes_check.py")],
                         capture_output=True, text=True)
    last = (chk.stdout.strip().splitlines() or [""])[-1]
    print("CHECK", last)
    if last != "FAILS 0":
        print("REFUSING: the image check did not pass")
        print("FAILS 1")
        return 1
    for path, old, new in EDITS:
        raw = open(path, "rb").read()
        o, n = old.encode("utf-8"), new.encode("utf-8")
        name = os.path.basename(path)
        if n in raw and o not in raw:
            print("ALREADY %s: %s" % (name, old[:50]))
            continue
        if raw.count(o) != 1:
            print("REFUSING %s: old text occurs %d times: %s" % (name, raw.count(o), old[:50]))
            fails += 1
            continue
        if apply:
            open(path, "wb").write(raw.replace(o, n))
            print("PATCHED %s: %s" % (name, old[:50]))
        else:
            print("WOULD PATCH %s: %s" % (name, old[:50]))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
