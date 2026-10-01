"""tex_incorp.py - incorporate ASTRA's nine texture packages (each ACCEPTed by SWE2-AUDIT-SPEC at its scoped bounds) into the
two pages that already explain these functions, and correct the 0061C250 offsets (OPUS, 2026-10-01).

Byte-preserving and idempotent: each edit's old text must occur exactly once, or its new text already be there.
Prints PATCHED / ALREADY per edit and FAILS n (nothing is written unless every edit applies).
"""
import os, sys

DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
GA = "00-Engine-Core-Runtime/Application-Root/game-application.md"
SI = "19-Save-Load-Settings/CONTRACT-save-image-buffers.md"


def ev(up, pkg, rev):
    return ("ASTRA [`%s`](%s_experiments/evidence/%s/README.md), ACCEPTed by SWE2-AUDIT-SPEC "
            "([review](%s_index/candidates/auditspec-review-%s-0930/REVIEW.md))" % (pkg, up, pkg, up, rev))


G = "../../"
S = "../"
N_COPY = (" *(OPUS, 2026-10-01; " + ev(G, "texture-copy-construction", "texture-copy-construction") + ", static: `edx` is the new "
          "count N, `r9d` the copy count K, `r8` the source; N = 1 uses the helper record at `rcx+8`. The helper does not clamp: "
          "K <= N is its caller's precondition, and K > N would copy past an N-record buffer. The copied head keeps each record's "
          "`+0x38` counter and its `+0x48` / `+0x50` async data; the tail records get `+0..+0x30` and `+0x38` zeroed and the "
          "`00D54348` vtable at `+0x40`, while their `+0x48` / `+0x50` keep whatever the allocation held.)*")
OLD_FILL = ("tail: each 0x58 record gets\nseven zeroed qwords, `+0x28`\nzeroed, and the `00D54348`\nvtable (RTTI `01D12448`)\n"
            "installed at `+0x30`.\n")
NEW_FILL = ("tail: each 0x58 record gets\n~~seven zeroed qwords, `+0x28`\nzeroed, and the `00D54348`\nvtable (RTTI `01D12448`)\n"
            "installed at `+0x30`.~~\n*(Corrected 2026-10-01, OPUS: seven zeroed qwords at `+0..+0x30`, a zeroed dword at `+0x38`, "
            "and the `00D54348` vtable (RTTI `01D12448`) at `+0x40`. The loop stores through `rax = rcx + 0x10` (`0061C25F`), so "
            "the old offsets were read 0x10 short. Found by " + ev(G, "texture-copy-construction", "texture-copy-construction") +
            "; regression `tex_check.py` T1 in [`opus-texture-incorp-1001`](../../_index/candidates/opus-texture-incorp-1001/consumer-check.md).)*\n")
N_RESIZE = (" *(OPUS, 2026-10-01; " + ev(G, "texture-copy-capacity-caller", "texture-copy-capacity-caller") + ", static: the old "
            "count is the record's dword with bit 31 cleared, and `cmp`/`cmovb` set K = min(new count, old count) right before the "
            "`0061D100` call, so K <= N holds on this path. A new count equal to the whole old dword returns 0 with no work; a NULL "
            "buffer with a non-zero count returns 0xD before any change. On success the old buffer goes to `00584730` only when it "
            "is not the new one, not the inline `+8` slot, not NULL and bit 31 was clear; then the new pointer (unless inline) and "
            "the new count are stored.)*")
N_HIGH = (" *(OPUS, 2026-10-01; " + ev(G, "texture-resize-drain-caller", "texture-resize-drain-caller") + ", static: when `+0xBC` "
          "is set and `0062BCB0` fails, it returns before both calls; otherwise the `0062B100` wait on the same object runs before "
          "the `00627DA0` resize of `+0x30`. That wait reads each old element's counter until it is not positive, one element "
          "at a time; it does not prove that nothing is pending afterwards. After a successful resize a masked count of 0 "
          "selects NULL and reads it (`0062815B`), so the callers must pass a positive count. Callers, per "
          + ev(G, "texture-resize-input-domain", "texture-resize-input-domain") + " and " +
          ev(G, "texture-resize-upstream-safe-counts", "texture-resize-upstream-counts") + ": six direct call sites pass 1, 4 or "
          "`max(1, r9d)` (`0017E8E0`, `0017F3B0`), so a raw 0 is excluded; the selected upstream callers of those two pass 1, 4 or "
          "32. For an arbitrary dynamic `r9d` the count `0x80000000` still masks to 0. Callers outside these selected paths are "
          "not covered.)*")
N_SAVE = ("\n\n**The texture path behind `0062C360` (OPUS, 2026-10-01; ASTRA's packages, each ACCEPTed by SWE2-AUDIT-SPEC at its "
          "own scoped bounds; static, nothing executed).** The rows are `Texture2DD3D11Element` records (0x58 bytes) of a "
          "`PTexture2DD3D11`.\n"
          "- *Admission*, " + ev(S, "texture-async-boundary", "texture-async-boundary") + ": the 0xC8-byte copy is twelve "
          "16-byte load/store pairs and one 8-byte pair, each written as it is read, so no overlap guarantee follows. The "
          "element's `+0x40` async data takes the texture pointer at its `+8` and the index at its `+0x10` (element `+0x48` / "
          "`+0x50`); its slot 0 (`00D54348`, `00621FF0`) tails `00622010`. `0062EB90` hands `context + 0x38*bank` to "
          "`00199DB0`, which inserts the pointer as a **key in an ordered tree**, refusing a key already present, rather than "
          "appending a callback pair; an insertion increments the container's `+0x28`. That container count is not the "
          "element's `+0x38` wait counter.\n"
          "- *The update callback*, " + ev(S, "texture-update-arguments", "texture-update-arguments") + ": `00622010` calls "
          "graphics-context slot `0x180` once per mip, from mip 0 to `min(11, +0x18 bit 1 ? 0 : +0x10)` (1 to 12 calls), with "
          "`rcx` the context, `rdx` the element's resource, `r8d` the mip, `r9d` 0, and on the stack the running source pointer, "
          "a dword row pitch and 0. The first source pointer is element `+0x28`; the resource, count and format are read again "
          "inside the loop, so the admitted 0xC8-byte copy is not a frozen upload snapshot. With B the format dword `+0x14` and F "
          "bit 0 of format byte `+0x18`, a dimension rounds to `(d + 3) & ~3` when F is set; the pitch is "
          "`(B * w * (F ? 4 : 1)) >> 3` and the source advance `(B * w * h) >> 3`, each product cut to 32 bits before the "
          "shift. After the loop a masked count of 1 frees and clears the selected element's `+0x28` through `00584730`.\n"
          "- *Removal*, " + ev(S, "texture-async-removal", "texture-async-removal") + ": `0062EC70` searches one bank, "
          "`context + 0x38*bank`, for the key (node key `+0x20`); on a hit it decrements the bank's `+0x28`, unlinks the node "
          "and frees its 0x28 bytes through the bank allocator's slot `0x18`, and a miss returns before any of that. The caller "
          "at `0062BD75` passes the bank current at release time (`01F7F590`) and the context `01F7F5B8`, not the bank the key "
          "was queued in, so a key left in another bank is not found by this call. That is a conditional source result, not an "
          "observed state.\n"
          "- *Bank dispatch*, " + ev(S, "texture-async-bank-dispatch", "texture-async-bank-dispatch") + ": `00185A50` submits "
          "with the bank current before the call, then sets `01F7F590` to the bank plus one, modulo 4, and returns it whatever "
          "the submission returned. `005FEA50` writes a 0x80-byte command (opcode `0x2F` at 0, the callback at `+8`, the data at "
          "`+0x10`), or returns 0xD when it cannot reserve one. The callback `00186610` reads the bank at `+0x10` and the "
          "current context and tails `0062EBC0`, which calls each key's virtual slot 0 before taking the tree successor, then "
          "frees the tree and resets the bank's count `+0x28`. Which interpreter executes opcode `0x2F` is open.\n"
          "- Open across all four: real callers, threads and timing, every writer of element `+0x38`, natural pending work in "
          "another bank, and lifetime (FABLE's scheduling questions).")
EDITS = [
    (GA, "Interior anchor `0061D14C`\n(the `00613770` copy).", "Interior anchor `0061D14C`\n(the `00613770` copy)." + N_COPY),
    (GA, OLD_FILL, NEW_FILL),
    (GA, "`00627DA0` (175 B) is a game-application body - `00584730`/`0061D100`. Interior anchor `00627DE8` (a `0061D100` call).",
     "`00627DA0` (175 B) is a game-application body - `00584730`/`0061D100`. Interior anchor `00627DE8` (a `0061D100` call)." + N_RESIZE),
    (GA, "`00628100` (153 B) is one of the `001B72B0` Y/U/V-channel triad callees - `0061FDA0`/`00627DA0`/`0062B100`/`0062BCB0`. "
         "Interior anchor `00628118` (a `0062BCB0` call).",
     "`00628100` (153 B) is one of the `001B72B0` Y/U/V-channel triad callees - `0061FDA0`/`00627DA0`/`0062B100`/`0062BCB0`. "
     "Interior anchor `00628118` (a `0062BCB0` call)." + N_HIGH),
    (SI, "`00607FA0` — the save-image write family.", "`00607FA0` — the save-image write family." + N_SAVE),
]

fails, out = 0, {}
for rel, old, new in EDITS:
    p = os.path.join(DB, rel)
    b = out.get(p) or open(p, "rb").read()
    o, n = old.encode("utf-8"), new.encode("utf-8")
    if n in b:
        print("ALREADY", rel.split("/")[-1], old[:40].replace("\n", " ")); out[p] = b; continue
    k = b.count(o)
    if k != 1:
        print("REFUSING (%d) %s %s" % (k, rel.split("/")[-1], old[:50].replace("\n", " "))); fails += 1; continue
    out[p] = b.replace(o, n)
    print("PATCHED", rel.split("/")[-1], old[:40].replace("\n", " "))
if not fails:
    for p, b in out.items():
        open(p, "wb").write(b)
print("FAILS", fails)
sys.exit(1 if fails else 0)
