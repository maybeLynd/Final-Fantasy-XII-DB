"""apply_ov_routed.py [--apply] - OPUS consumes FABLE's routed text from its reviews of ASTRA's OV-10 / OV-16 / OV-42
notification, queue, actor-kind and slot packets on the five OPUS-led pages (OPUS, 2026-10-02).

Sources (each FABLE review folder's consumption-draft.md, 'Route to OPUS'):
  fable-review-astra-notification-retirement-order-1002, fable-review-astra-request-cancel-notification-1002,
  fable-review-astra-ov42-actor-predicate-domain-1002, fable-review-astra-ov42-queue-output-alias-1002,
  fable-review-astra-actor-directory-kind-proof-1002, fable-review-astra-ov42-slot-id-producer-1002.
OPUS re-read at the bytes before applying (retool.py dis, 2026-10-02): 003DB2A0 (the head check, the non-walk loop at
+0x86..+0x9F, the gate order, the discarded result, the return of +0x12 bit 0, index 0xFF -> 1), 003DB550 (pure index
leaf), 003DBCF0 (count first -> 3, free head 0xFF -> 2, no calls or writes before either), 0030CFB0 (185 B),
0030D070 (229 B, no calls, WORD +0x1C stored last, AL = FF on a full array), 00348330 (165 B; reads both out-references
after the writer whatever it returns), and .data's raw end 01F7E400 < 02EBF138 < virtual end 02F97530.
Not re-read by OPUS (FABLE's review evidence stands): 003DB420 mode 4's range/selection, 002679F0 / 00266530 /
00266BD0's row and preset bindings, the 002FFD8B / 002FFE9D argument registers.

Each edit: (page, OLD anchor, NEW). An edit applies once: skipped when NEW is already present, FAIL when OLD is
missing. Line endings are preserved (pages carry mixed EOLs; the anchors are single-line).
"""
import io
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
REC = "04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md"
POOL = "04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md"
GAMBIT = "09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md"
CALL = "01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md"
SEAM = "07-Combat-Action/CONTRACT-native-command-seam.md"
RV = "fable-review-astra-"
C = "*(corrected 2026-10-02, OPUS, from FABLE's review `" + RV

POOL_SECTION = """## 7c. Removal order, the release gate's two callers, and the ordinal / row / preset bindings (OPUS, 2026-10-02)

Incorporated from FABLE's independent reviews of three ASTRA packets, all ACCEPT-WITH-NARROWING:
[`notification-retirement-order`](../_index/candidates/fable-review-astra-notification-retirement-order-1002/),
[`request-cancel-notification`](../_index/candidates/fable-review-astra-request-cancel-notification-1002/) and
[`actor-directory-kind-proof`](../_index/candidates/fable-review-astra-actor-directory-kind-proof-1002/). OPUS re-read
the removal, the index leaf and the notification's refusals at the bytes on 2026-10-02. The release gate's mode-4
caller and the directory bindings stand on FABLE's review evidence (`rv_actordir.py`, 69 / 69 PASS).

**Removal (`003DB2A0`).**
- Index `0xFF` returns a constant 1 and does nothing else.
- A removed index that is not the list head does not walk the list. Every pass hands the removed index itself to
  `003DB550` (the record page's removal table states the three outcomes).
- The mode-3 end notification through `003DC0D0` is attempted **before** the removed index is relinked onto the free
  list (`003DB650`) and published at `+0x60`. Its result is discarded.
- The removal returns entry `+0x12` bit 0.

**The notification's refusals (`003DBCF0`).** The record `003DC0D0` builds carries function id 0 at `+4`.
- `003DBCF0` checks that id against the count at `[actor+0x48]` first: a zero count returns 3.
- It then checks the free head `actor+0x60`: `0xFF` returns 2.
- Neither refusal makes a call or writes the object.

**The release gate's second caller.** The gate is reached from RET's removal and from `003DB420` mode 4 (the
`freqcancel` verbs).
- **Range.** Channels run from `byte actor+0x88 - 1` down to `max(0, signed edx)`. Both compares are signed 64-bit.
  Each channel is gated by the entry snapshot of `word actor+6`, at bit (channel mod 32).
- **Selection.** The state filter `r14d` = (`r8d` != 4 ? `r8d` : 0). The recycler takes the first nonzero
  `byte entry+0x11`, following each entry's `+0` link, with the walk bounded by `byte actor+0x89`. It takes at most
  one entry per channel per call.
- **Removal.** It completes only when the selected index is the head of the list named by `entry+2`, or by
  `actor+0x61` when `+0x10` is 4.
- **Return.** EAX 1 on every normal path.

**Ordinal, row and preset.**
- The allocator `002679F0` publishes `pool[1 + ordinal]` row by row. Ordinal i is in row k exactly when
  sum(counts[:k]) <= i < sum(counts[:k+1]). The counts are the u16 entries after the group count at descriptor +
  s32 `[desc+0x14]`.
- Nothing bounds the published ordinals by N = manager `+0x20`. N covering sum(counts) is a precondition.
- The initializer `00266530` binds record `+0x40` = desc + s32 `[desc+0x18]` + 4 + 48*i (32*i when WORD `[desc+0]` < 8).
- The preset leaf `00266BD0` switches on the GROUP (record `+3` & 0x1F), not on the kind:
  - groups 5 and 6 store `0x00030004` (group 5 also sets `+0x14` bit 7);
  - group 7 stores `0x00034C85` and sets `+0x14` bit 7;
  - group 0 stores 0, groups 1-2 store `0x38`, groups 3-4 store `0x40`.
- The initializer clears `+0x0B` bit 3 before its two `00268EA0` call sites. It therefore never files talkhold /
  talkterm itself unless a callee sets that bit.
- The directory WORD `+4` (scriptType) is read nowhere on this path.

**Limits kept.** All of this is static and conditional. Natural reachability of the cancel path and the end
notification's timing stay open where the register rows OV-10 and OV-16 leave them.

"""

CALL_SECTION = """
## Two out-references: the destination precondition (OPUS, 2026-10-02)

From FABLE's review [`ov42-queue-output-alias`](../../_index/candidates/fable-review-astra-ov42-queue-output-alias-1002/)
(ACCEPT-WITH-NARROWING). OPUS owns pointer, width and non-aliasing preconditions, and re-read the bridge at the bytes.

- **The precondition.** A verb that pops two out-references and passes them to a native writer needs two valid,
  byte-disjoint destinations that alias neither source global.
- **Why.** The 165-byte bridge `00348330` resolves both references, calls the writer `00309C00` with them, and then
  reads a dword through each (`00348330` + 0x79 and + 0x81) on every normal return, including 0.
  - Those two reads go into the globals `01EF920C` / `01EF9214`.
  - Before that, the bridge shifts the globals' previous values into `01EF9208` / `01EF9210`.
"""

SEAM_BULLETS = """- **Presentation-slot acquire / allocate ABI** *(OPUS, 2026-10-02, from FABLE's review
  [`ov42-slot-id-producer`](../_index/candidates/fable-review-astra-ov42-slot-id-producer-1002/); sizes and the
  allocator's shape re-read at the bytes by OPUS).*
  - The acquire wrapper `0030CFB0` (185 B) takes RCX = the unit, EDX = the identity and R8W = the action word. It
    returns nothing; its result is unit+4.
  - The allocator `0030D070` (229 B, no calls) takes ECX = the identity and DX = the action word (zero-extended; the
    upper RDX bits are ignored).
    - It returns EAX = the slot index 0..31 on success. On a full array it returns AL = FF only, with the upper RAX
      bits undefined.
    - Occupancy is WORD `+0x1C` == FFFF. The word is stored last, so a FFFF action word leaves the slot reading free.
  - The flag gate in the wrapper sets bit 1 of `022C2158` before allocating and never clears it.
  - The row read has no null guard: a null `[02EBF138]` reads address 0xC.
"""

EDITS = [
    (REC,
     "| walk to find it | `003DB326`–`003DB33F` | linear from the head through `003DB550`, so removal is O(list) |",
     "| ~~walk to find it~~ look for it | `003DB326`–`003DB33F` | ~~linear from the head through `003DB550`, so removal "
     "is O(list)~~ not a walk: every iteration passes the removed index itself to `003DB550` (`mov edx, esi`), so a "
     "non-head entry is unlinked only when its own `next` byte equals its index, returns with no unlink when that byte "
     "is `0xFF`, and otherwise repeats the same iteration " + C + "notification-retirement-order-1002`; `003DB550` is a "
     "pure index leaf, `[actor+0xA0] + idx*20`)* |"),
    (REC,
     "| release a payload | `003DB36B`, `003DB371` | only when `entry+0x06 != 0x8000` **and** `state == 3` |",
     "| ~~release a payload~~ end notification | `003DB36B`, `003DB371` | ~~only when `entry+0x06 != 0x8000` **and** "
     "`state == 3`~~ the mode-3 end notification through `003DC0D0`, attempted before the free-list relink and its "
     "result discarded; only when the signed channel byte `entry+0x02` is non-negative, `entry+0x06 != 0x8000` "
     "**and** `entry+0x10 == 3` (`+0x10` is the request mode) " + C + "notification-retirement-order-1002`)* |"),
    (POOL, "## 8. Script · resource · event interactions", POOL_SECTION + "## 8. Script · resource · event interactions"),
    (GAMBIT,
     "`0`–`0x21E`, because the action table `[02EBF138]` has 543 rows, and that is the commit's first band.",
     "`0`–`0x21E`, because the action table `[02EBF138]` has 543 rows *(qualified 2026-10-02, OPUS, from FABLE's "
     "review `" + RV + "ov42-actor-predicate-domain-1002`: the count is bound at run time, since `02EBF138` lies in "
     "`.data`'s zero-filled virtual tail past the section's raw bytes; a null descriptor refuses every id with reason "
     "4)*, and that is the commit's first band."),
    (CALL, None, CALL_SECTION),
    (SEAM, "- The two rings are indistinguishable by shape (`CS-3`).\n",
     "- The two rings are indistinguishable by shape (`CS-3`).\n" + SEAM_BULLETS),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    for page, old, new in EDITS:
        p = os.path.join(DB, page)
        t = io.open(p, encoding="utf-8", newline="").read()
        key = next(l for l in new.strip().splitlines() if l.strip() and (old is None or l not in old))
        if key in t:
            print("SKIP (present)", page)
            continue
        if old is None:
            nt = t.rstrip("\r\n") + "\n" + new
        else:
            o = old
            if o not in t and o.endswith("\n") and o[:-1] + "\r\n" in t:
                o, new = o[:-1] + "\r\n", new.replace("\n", "\r\n")
            if t.count(o) != 1:
                print("FAIL (anchor x%d)" % t.count(o), page, old[:60])
                fails += 1
                continue
            nt = t.replace(o, new)
        if apply:
            io.open(p, "w", encoding="utf-8", newline="").write(nt)
        print("APPLY" if apply else "WOULD", page)
    print("FAILS %d" % fails)


if __name__ == "__main__":
    main()
