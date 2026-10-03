"""apply_ec7corr.py [--apply] - SWE2-EC7's corrections of 2026-10-03 on its own lines (Claude stand-in for Devin).

Requests: FABLE-REQ-EC7-TITLE-PACKET-CORRECTIONS-1002 (R1, R2), FABLE-REQ-EC7-K54-ROLES-1002 (X1, X2),
OPUS-REQ-EC7-PREFETCH-CLOSE-CONDITIONAL-1002. Each old text is EC7's; each edit strikes it and states the reading the
bytes support (control: ec7_corr_check.py). Same unique-match rule as OPUS's batch appliers."""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
TP = "00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md"
RN = "02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md"
RS = "21-RNG-And-Determinism/rng-streams.md"
PF = "02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md"
K54 = "(corrected 2026-10-03, SWE2-EC7: FABLE's kind-0x54 record c4d8dcd31 executed the body bit-exact, %s; ec7_corr_check.py)"

EDITS = [
    # R1 - 00189120 takes no argument.
    (TP,
     "and loader bodies share: a null `rcx` returns at once; otherwise\n"
     "`00189120(rcx)` resolves the object twice and `00185A90(result,\n"
     "&0017ECC0, rcx)` registers the `0017ECC0` leaf on it with the\n"
     "original argument as the callback's data.",
     "and loader bodies share: a null `rcx` returns at once; otherwise\n"
     "~~`00189120(rcx)` resolves the object twice and `00185A90(result,\n"
     "&0017ECC0, rcx)` registers the `0017ECC0` leaf on it with the\n"
     "original argument as the callback's data~~ it reads the shared global `01F7F598` twice through `00189120` (which\n"
     "takes no argument: `mov rax, [01F7F598]` / `ret`), tests only the first read for NULL, and passes the second to\n"
     "`00185A90` with callback `0017ECC0` and the original argument as data; on the fast arm `00185A90` appends the pair to\n"
     "the queue at `ctx+0xC38+32*ctx[+0xCB8]` without calling anything, and when full it hands off to `001858A0`\n"
     "*(corrected 2026-10-03, SWE2-EC7: ASTRA's title packets T1/T2, SPEC-supported wording, routed by FABLE as R1;\n"
     "ec7_corr_check.py)*."),
    # R2 - the anchor's call target.
    (RS,
     "Interior anchor `0062BCBE` (an `0062EC70` call).",
     "Interior anchor `0062BCBE` (~~an `0062EC70` call~~ a `0062B100` call; the `0062EC70` call is at `0062BD75`"
     " *(corrected 2026-10-03, SWE2-EC7: ASTRA's T17/K1, routed by FABLE as R2; ec7_corr_check.py)*)."),
    # PREFETCH - the close is conditional on both fields.
    (PF,
     "`0x0059BD40` (frees the stream's `+0x30`, releases the `+0x40` handle)",
     "`0x0059BD40` (~~frees the stream's `+0x30`, releases the `+0x40` handle~~ frees the stream's `+0x30` when nonzero,"
     " and releases the `+0x40` handle when it is positive; see the path page section 5c"
     " *(corrected 2026-10-03, SWE2-EC7: `je` at `0x0059BD50`, `jle` at `0x0059BD66`, and Close returns AL 1 either way;"
     " ASTRA's filecache-close-zero-sentinel packet, FABLE-accepted; ec7_corr_check.py)*)"),
    # X1 - 0043E7B0, a per-pair swap.
    (TP,
     "`0043E7B0` (140 B) is the `r9d`-count qword push the workbench callers\n"
     "run: each iteration stores `[rcx+i*8]` to `02EB8738`, rotates the\n"
     "`02EB8790`/`02EB8798`/`02EB87A0` triplet, and writes `eax`/`edx` into\n"
     "`[rdx+i*8-4]`/`[-8]` - a counted copy driving the global ring.\n"
     "Interior anchor `0043E7F4` (the `[r8-4]` store).",
     "`0043E7B0` (140 B) is ~~the `r9d`-count qword push the workbench callers\n"
     "run: each iteration stores `[rcx+i*8]` to `02EB8738`, rotates the\n"
     "`02EB8790`/`02EB8798`/`02EB87A0` triplet, and writes `eax`/`edx` into\n"
     "`[rdx+i*8-4]`/`[-8]` - a counted copy driving the global ring~~ a per-pair UV swap: each source qword is staged in\n"
     "the scratch cell `022D8F90`, its low dword stored at `dst+4` (`0043E7F4`) and its high dword at `dst+0`\n"
     "(`0043E826`), the counter kept in `022D94A0` - `dst[i] = (v, u)`; a do-while, so a count of 0 still swaps one pair\n"
     "*" + K54 % "E1, 40 trials; the scratch cells are `022D8F90`/`022D94A0`, not `02EB87xx`" + "*.\n"
     "Interior anchor `0043E7F4` (the `[r8-4]` store)."),
    # X1 - 00434760, affine map then swap.
    (TP,
     "`00434760` (404 B) is the larger bank-transform: `[r8]`'s xmm seeds\n"
     "`02EB9010`/`02EB9350`, `[rcx]` qwords feed `02EB8E80`-family rotates,\n"
     "and each of `r9d` iterations spins `xmm3` through the `02EB8F90` bank\n"
     "- `mulss` by `xmm4`/`xmm5`, scaled adds at `rip+0x1ac4bda`, stores to\n"
     "`02EB91A8`/`02EB91A4`/`02EB92D8`/`02EB92E0` - before the output xmm\n"
     "lands at `[rdx-4]`/`[-8]` and `02EB9498` counts down.\n"
     "Interior anchor `00434840` (the `mulss xmm2, xmm4` bank step).",
     "`00434760` (404 B) is ~~the larger bank-transform: `[r8]`'s xmm seeds\n"
     "`02EB9010`/`02EB9350`, `[rcx]` qwords feed `02EB8E80`-family rotates,\n"
     "and each of `r9d` iterations spins `xmm3` through the `02EB8F90` bank\n"
     "- `mulss` by `xmm4`/`xmm5`, scaled adds at `rip+0x1ac4bda`, stores to\n"
     "`02EB91A8`/`02EB91A4`/`02EB92D8`/`02EB92E0` - before the output xmm\n"
     "lands at `[rdx-4]`/`[-8]` and `02EB9498` counts down~~ the per-pair affine map followed by a swap: the same\n"
     "arithmetic as `00434630` (`0043480F`-`0043487C`), with the x result stored at `dst+4` (`0043489C`) and the y result at\n"
     "`dst+0` (`004348D0`) - `(b1 + v*b3, b0 + u*b2)` *" + K54 % "E3, 406 pairs" + "*.\n"
     "Interior anchor `00434840` (the `mulss xmm2, xmm4` ~~bank step~~ of the affine arithmetic)."),
    # X1 - 00434630, affine map.
    (TP,
     "`00434630` (289 B) is the reduced sibling: same `[r8]` seed into\n"
     "`02EB8FA0`/`02EB92D0`, same `r9d` bank loop at half the steps, single\n"
     "output `[rax-8]` and the `02EB9490` countdown - the two-step variant\n"
     "of `00434760`'s three-step pass.\n"
     "Interior anchor `004346BA` (the `mulss` bank step).",
     "`00434630` (289 B) is ~~the reduced sibling: same `[r8]` seed into\n"
     "`02EB8FA0`/`02EB92D0`, same `r9d` bank loop at half the steps, single\n"
     "output `[rax-8]` and the `02EB9490` countdown - the two-step variant\n"
     "of `00434760`'s three-step pass~~ the per-pair affine map: the `[r8]` block is staged as `022D92F0` =\n"
     "(b0, b1, b2, b3) and `022D9300` = (b2, b3), then each pair becomes `(b0 + u*b2, b1 + v*b3)`, stored at `dst`\n"
     "(`0043473D`); `00434760` is this map plus a swap *" + K54 % "E2, 388 pairs" + "*.\n"
     "Interior anchor `004346BA` (the `mulss` ~~bank step~~ by `b3`, read from `022D9300`)."),
    # X1 - 0043E840, scale about the centre.
    (TP,
     "and vector copies land at `022D92F0`/`022D9308` - a call-free publish of the workbench header.",
     "and vector copies land at `022D92F0`/`022D9308` - ~~a call-free publish of the workbench header~~ a scale about the"
     " centre: with `(a, b)` from `[r8]` and the immediate's low dword -0.5, each pair becomes `((u - 0.5)*a,"
     " (v - 0.5)*b)`, stored at `dst` (`0043E98D`) *" + K54 % "E6, 578 pairs" + "*."),
    # X1 - 00396F20, gather by normal index.
    (TP,
     "`r9d` counts down while `[rdx]` qwords write into `[rax-8]` slots - a call-free indexed copy.",
     "`r9d` counts down while `[rdx]` qwords write into `[rax-8]` slots - ~~a call-free indexed copy~~ a gather by"
     " normal index: each corner's signed 16-bit index forms `index*16 + table`, and that entry's first qword is copied to"
     " the destination pair - `UV'[k] = (L[n_k].x, L[n_k].y)`, the loop ending when the counter equals the cell"
     " `022D8F10` *" + K54 % "E4, 685 corners" + "*."),
    (TP,
     "`00396F20` (161 B) is the index scatter the composers run:",
     "`00396F20` (161 B) is ~~the index scatter~~ the normal-index gather the composers run:"),
    # X1 - 00394B70, screen-position term (it adds; it does not scatter).
    (TP,
     "and `addss` into the out vector - the weight scatter under the composers' vertex lists.",
     "and `addss` into the out vector - ~~the weight scatter under the composers' vertex lists~~ the screen-position term"
     " added into the UV pairs: `UV'[k] += ((X/16)/512 - 3.5, (Y/16)/512 - 3.5625)` from the `u16` screen X, Y at"
     " `table + 16*idx` *" + K54 % "E5, 375 corners; it adds into the gathered pair" + "*."),
    # X2 - 00521450 is not call-free; it is the six-plane triangle clipper.
    (RN,
     "`00521450` (1,886 B, call-free) is the matrix-bank multiply the\n",
     "`00521450` (1,886 B, ~~call-free~~ one call, the edge blend at `00521B26`) is ~~the matrix-bank multiply~~ the"
     " homogeneous triangle clipper the\n"),
    (RN,
     "repeats the accumulate - a pure-SSE 4x4 transform fold with no calls.",
     "repeats the accumulate - ~~a pure-SSE 4x4 transform fold with no calls~~ the 4x4 transform is only its prologue:"
     " the body clips each triangle against six planes (near z first), interpolating a cut edge through the two-record"
     " blend that [clamping-a-point-into-a-volume.md](../../06-Movement-And-Navigation/clamping-a-point-into-a-volume.md)"
     " describes, and returns the vertex count *(corrected 2026-10-03, SWE2-EC7: FABLE's kind-0x54 record c4d8dcd31 X2/E7;"
     " ec7_corr_check.py)*."),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
