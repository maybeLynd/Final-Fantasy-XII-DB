"""apply.py [--apply] - consume FABLE's independent reviews of four ASTRA OV packets into the three FABLE-led pages
(FABLE, 2026-10-02). Dry run by default; --apply writes. Prints FAILS N last. Each edit replaces exactly one OLD."""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
AR = "01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md"
IC = "01-Script-VM-Native-Bridge/CONTRACT-interpreter-core.md"
AV = "07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md"
RV = "../../_index/candidates/"      # from a page two levels deep
NL = "\n"

OV16_AR = NL.join([
    "OriginalREQEW remains blocked until the target entry is removed and the removal posts the notification. RET is the",
    "usual removal, but not the only one.",
    "",
    "**A cancellation can attempt the end notification without RET** *(2026-10-02, FABLE, from ASTRA's",
    "[`request-cancel-notification`](../../_experiments/evidence/request-cancel-notification/README.md) (`011e013c7`),",
    "FABLE independent review ACCEPT-WITH-NARROWING,",
    "[`fable-review-astra-request-cancel-notification-1002`](" + RV + "fable-review-astra-request-cancel-notification-1002/REVIEW.md)).*",
    "",
    "- **What the cancel verbs pass.** `freqcancel` (`00352980`) passes its popped channel and mode 4 to",
    "  `ActorResource_RecycleEntryRange` (`003DB420`). The two-argument form (`00353660`) passes its first pop + 1 and",
    "  resolves the second pop to another actor.",
    "- **What the recycler selects.** Mode 4 clears the state filter. The recycler walks channels from",
    "  `byte actor+0x88` - 1 down to max(0, signed bound), keeping only those set in its entry snapshot of",
    "  `word actor+6`. For each such channel it hands the first entry with a nonzero `+0x11` to `003DB2A0`: at most one",
    "  entry per channel per call.",
    "- **When the notification is attempted.** The entry must be its channel's head, with mode `+0x10` = 3 and a",
    "  requester ordinal other than `0x8000`. `003DB2A0` then unhooks it (clearing `+0x11`) and calls `003DC0D0`",
    "  whatever the run state was. The interpreter is not called in front of that attempt.",
    "- **A non-head entry is not removed.** The removal's search passes the removed index itself to its index leaf on",
    "  every pass instead of walking the list, so a cancel does not remove an entry that sits behind a zero-state head.",
    "- **What an end notification means.** It is evidence that the target entry was removed, not that the target's",
    "  bytecode executed RET. Admission, delivery and consumption of the notification are separate stages (below).",
    "- **The recycler's return value** is 1 on every normal path, including a NULL actor, an empty range and no",
    "  selection, so it says nothing about removal or notification.",
    "- **The NULL-actor hazard.** After a NULL actor both verbs still tail-jump to the request scheduler `003DB6E0`, which",
    "  reads `[rcx + 0x63]` without testing rcx.",
    "- **Premises:** valid, stable and disjoint actor and entry storage; normal ABI and returns. The removal past the",
    "  attempt is opaque for entry flags 2 and above (a flags helper whose effects are not read; its address is on the binding-and-channels page).",
    "- **Still open:** whether an authored scene cancels a mode-3 entry; natural interleaving; same-key re-entry; the",
    "  scheduler's own effects.",
])

OV10_AR = NL.join([
    "No shipped deadlock, automatic retry or higher recovery is inferred.",
    "",
    "**The end notification is attempted before the finishing entry's own slot is free** *(2026-10-02, FABLE, from",
    "ASTRA's [`notification-retirement-order`](../../_experiments/evidence/notification-retirement-order/README.md)",
    "(`e46090c35`), FABLE independent review ACCEPT-WITH-NARROWING,",
    "[`fable-review-astra-notification-retirement-order-1002`](" + RV + "fable-review-astra-notification-retirement-order-1002/REVIEW.md)).*",
    "In a head-entry removal, `003DB2A0` first calls the unhook `003DC1B0`, which relinks the neighbours, clears entry",
    "`+0x11` and writes nothing on the actor. Next comes the mode-3 attempt through `003DC0D0`. Only after that does",
    "the removal relink the index onto the free list and publish it as the free head `+0x60`; every path from the",
    "attempt's return passes both steps.",
    "",
    "The attempt is made only when the entry is the list head, its mode `+0x10` is 3, its signed channel byte `+0x02` is",
    "not negative, its requester word `+0x06` is not `0x8000`, and the requester resolves to a non-null actor.",
    "",
    "- **Two refusals come first.** The posted descriptor selects function 0. `003DBCF0` checks that id against the",
    "  requester's function count before anything else, as an unsigned compare: a zero count returns 3. Only then does",
    "  it test the requester's free head: `0xFF` returns 2. Neither refusal calls anything or writes outside its own",
    "  stack.",
    "- **So a self-requested notification on a full pool is lost.** When the requester is the removing actor itself and",
    "  its free list is already empty, the notification is refused with 2 before the retiring slot becomes",
    "  allocatable. Conditions: a valid head mode-3 entry; a positive function count; entry flags `+0x12` 0 or 1 (2",
    "  and above also cross a flags helper whose effects are not established); stable, disjoint actor, pool and frame",
    "  storage; normal returns under the ABI; no concurrent writer. This is a conditional reading of the original code,",
    "  not an observed full pool. \"Same actor\" is a premise on the resolved requester pointer; the code compares nothing.",
    "- **The removal's return is not a delivery result.** It is bit 0 of the entry's `+0x12`, read before the attempt;",
    "  the attempt's own result is overwritten unread. With flags 1 the removal returns 1 even when the notification was",
    "  refused. Index `0xFF` returns a constant 1 without reading an entry.",
    "- **An observer has to read the attempt itself:** the requester, its free head and the call origin at",
    "  `003DBCF0` + 0x36 with return origin `003DC0D0` + 0x57. Spare capacity seen after the removal does not show that",
    "  capacity existed when the notification was allocated.",
    "- **Still open:** whether shipped play reaches a full self-pool; actor lifetime and reuse; concurrent mutation;",
    "  cancel and re-entry scheduling; the insertion helpers' success and effects on a non-`0xFF` free head.",
])

OV10_BOX = NL.join([
    "- [ ] **OV-10.** Real authored input bounds and higher recovery/delivery policy for exhausted notification capacity.",
    "  - *Qualified 2026-10-02 (FABLE, review of ASTRA `notification-retirement-order`):* the end notification is",
    "    attempted before the removed slot is relinked and published, so the capacity that matters is the requester's",
    "    free head at the attempt (section 3). A runtime observation for the residue counts only when it is taken at the",
    "    attempt, with the requester and the call origin; capacity seen after the removal does not count.",
])

IC_OV10 = NL.join([
    "without undoing target progress. A mode-3 end notification is attempted before the removed entry is relinked onto",
    "the free list, so a self-requested notification on an already-full pool is refused even though the removal then",
    "frees a slot. The removal's return is the entry's `+0x12` bit 0, not a delivery result",
    "([the actor request](Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md) section 3; a",
    "conditional static reading, premises there; FABLE 2026-10-02).",
])

IC_OV16_OLD = NL.join([
    "Original `REQSW` (24) and `REQEW` (27) each arm kind4 at their continuation PC. Mode2 generates",
    "its requester notification when the target entry starts; mode3 does so at target removal/RET.",
    "The former permits caller continuation before target bytecode runs; the latter waits for return.",
])
IC_OV16_NEW = NL.join([
    "Original `REQSW` (24) and `REQEW` (27) each arm kind4 at their continuation PC. Mode2 generates",
    "its requester notification when the target entry starts. Mode3 does so when the target entry is removed: on RET,",
    "or when a mode-4 `freqcancel` recycle (`003DB420`) removes the target as its channel head without running it",
    "(FABLE 2026-10-02, [review](../_index/candidates/fable-review-astra-request-cancel-notification-1002/REVIEW.md)).",
    "The former permits caller continuation before target bytecode runs; the latter waits for removal, which is",
    "normally, but not necessarily, the target's return.",
])

AV_D = NL.join([
    "**What a zero availability reason proves about the id** *(FABLE 2026-10-02, from ASTRA's",
    "[`ov42-actor-predicate-domain`](../../_experiments/evidence/ov42-actor-predicate-domain/README.md) (`2b341ca3a`),",
    "FABLE independent review ACCEPT-WITH-NARROWING,",
    "[`fable-review-astra-ov42-actor-predicate-domain-1002`](" + RV + "fable-review-astra-ov42-actor-predicate-domain-1002/REVIEW.md)).*",
    "",
    "- `002FFCF0` has two returns: the early constant 2, and the shared reason return.",
    "- The only EAX definition that can make the shared return 0 is the final cost call `00303BD0`, reachable only",
    "  through the class-success edge after the class query at `002FFCF0` + 0x9B.",
    "- The class query receives EDX = the zero-extended low 16 bits of the incoming id (`002FFCF0` + 0x1C), ECX = `0x14`",
    "  (decimal 20) and R8D = 1. The class-`0x14` arm and the shared tail never read R8.",
    "- So a normal zero reason requires class `0x14` to accept the id. Under the count-543 premise the id is then",
    "  0..542, which still includes 511..534.",
    "- This is a necessary condition only. A zero reason also requires `0030E9C0`, `0031A7B0`, `00306480` and",
    "  `00303BD0` each to return 0; nothing here shows that any of 511..534 passes those gates.",
    "- The record's byte `+5` staying unchanged from its load to the `00306480` leg is a premise. Two callees on that",
    "  path, `0030E9C0` and `0031A7B0`, receive the record pointer itself.",
    "",
    "**Limits kept.** These limits are ASTRA's and SPEC's.",
])

AV_NEW_SECTION = NL.join([
    "proved. Natural rejection and whole OV-42 stay OPEN.",
    "",
    "### FABLE 2026-10-02: what the queue reader writes, in what order, and what its script bridge then reads (OV-42)",
    "",
    "*From ASTRA's packet [`ov42-queue-output-alias`](../../_experiments/evidence/ov42-queue-output-alias/README.md)",
    "(`4fe271b46`), reviewed by FABLE ACCEPT-WITH-NARROWING",
    "([record](" + RV + "fable-review-astra-ov42-queue-output-alias-1002/REVIEW.md), 49 checks, 0 FAIL, 11 controls).*",
    "",
    "- **The reader `00309C00` (50 B, no `.pdata`, a leaf).** It reads the queue DWORD `022C2178`.",
    "  - If the DWORD is FFFFFFFF, the reader returns DWORD 0. It writes nothing and does not reset the queue.",
    "  - Otherwise it stores the DWORD through RDX when RDX is non-null. Then, when RCX is non-null, it loads the unit",
    "    DWORD `022C218C` and stores it through RCX. Finally it resets the queue to FFFFFFFF and returns DWORD 1. Each",
    "    store is 4 bytes.",
    "  - With both pointers NULL, a pending value is still consumed: the queue is reset and the reader returns 1.",
    "- **The two stores are ordered.** The unit load and store come after the action store. If the two destinations",
    "  overlap, the unit store overwrites the overlapping bytes: action byte j becomes unit byte j - d when",
    "  0 <= j - d < 4, where d = RCX - RDX. A shared destination ends holding the unit DWORD in both views. Only",
    "  byte-disjoint destinations keep both values whatever they are, and a sample in which the two values happen to",
    "  agree cannot show that the destinations do not overlap.",
    "- **The formula assumes neither destination aliases `022C2178` or `022C218C`.** An action store into `022C218C`",
    "  would change the unit value loaded after it, and any output in `022C2178` is overwritten by the reset.",
    "- **The script bridge (165 B; FABLE confirmed the extent against `.pdata`).** It pops two out-references through",
    "  the interpreter's pop, decodes each to a destination, and passes them as RDX (action) and RCX (unit). After any",
    "  normal return it reads both destinations on a straight line with no test of the result, so it also reads them",
    "  when the reader returned 0, and copies the two values to a pair of globals after shifting their old values. The",
    "  reader's null guards therefore do not make a bridge call with invalid destinations safe; on a 0 return the",
    "  copies are whatever the destinations already held. (The bridge's address is on the script-native pages; it is",
    "  named by role here.)",
    "- **The reader has one other direct caller,** which passes two stack locals `0x20` apart. That raw `E8`/`E9`",
    "  census does not cover indirect callers.",
    "",
    "**Limits kept.** These limits are ASTRA's and FABLE's.",
    "",
    "- No authored out-reference binding, backing capacity, alias, lifetime, null or invalid destination, fault or",
    "  natural command-to-action path is observed or proved.",
    "- Whether the bridge's decode can yield an invalid destination is not read.",
    "- The role of the bridge's copy globals is not established; no reader census was taken.",
    "- The 8 branch partitions are logical, not native calls. The overlap rows are arithmetic.",
    "- Whole OV-42 stays OPEN.",
])

EDITS = [
    (AR, "| 3 | At003DB2A0 removal/RET through003DC0D0 |",
     "| 3 | At `003DB2A0` removal through `003DC0D0`: on RET, and also when a mode-4 `freqcancel` recycle (`003DB420`) removes the entry as its channel head |"),
    (AR, "OriginalREQEW remains blocked until the target executes RET and removal posts the notification.", OV16_AR),
    (AR, "No shipped deadlock, automatic retry or higher recovery is inferred.", OV10_AR),
    (AR, "- [ ] **OV-10.** Real authored input bounds and higher recovery/delivery policy for exhausted notification capacity.", OV10_BOX),
    (IC, "without undoing target progress.", IC_OV10),
    (IC, IC_OV16_OLD, IC_OV16_NEW),
    (AV, "if (unit == NULL)                                        return 0x2C;",
     "if (raw == NULL)  /* RDX = 002FFCF0's RDI, q[unit+0x698] */  return 0x2C;"),
    (AV, "if (BattleStats_HasRequiredLicenseForAction(unit, actionId))     return 0;",
     "if (BattleStats_HasRequiredLicenseForAction(raw, actionId))      return 0;"),
    (AV, "  - Class `0x14` accepts 0..542. The count is `[02EBF138]+4` = 543 (`00322F84`, `0032302C`..`0032303B`).",
     NL.join(["  - Class `0x14` accepts 0..542. The count is the runtime value `[02EBF138]+4` (`00322F84`, `0032302C`..`0032303B`).",
              "    543 is the shipped table's row count, and that is a premise: `02EBF138` lies in `.data`'s virtual tail, so it is",
              "    0 at load, and a NULL descriptor refuses every id (FABLE 2026-10-02, review below)."])),
    (AV, "  - (a) `0030DB70`'s record arm. If the unit's raw record (`002FFD05`) has byte `+5` = 0, `003060E0` returns 5 for",
     NL.join(["  - (a) `0030DB70`'s record arm. The raw record is the pointer `002FFCF0` loads from the incoming RDX `+0x698` at",
              "    `002FFD05` and keeps in RDI; it passes that pointer as RDX to `00306480` (`002FFCF0` + 0x1A7), which forwards it",
              "    unchanged to `003060E0`, where `003060E0` + 0x49 reads `+5`. The later reloads of `+0x698` do not replace it, so",
              "    the `+5` test concerns that parsed record, not a byte of the outer unit (FABLE 2026-10-02). If the unit's raw",
              "    record has byte `+5` = 0, `003060E0` returns 5 for"])),
    (AV, NL.join(["- The row-`0x113` type bound, the row/codec identity and the descriptor count staying unmodified are premises. So are",
                  "  the interpreter's value transfer (`00309C13` -> `00267E10`) and stable raw-record state."]),
     NL.join(["- The row-`0x113` type bound, the row/codec identity and the descriptor count staying unmodified are premises. So is",
              "  stable raw-record state. So is the interpreter's value transfer: the reader stores the action DWORD through its",
              "  RDX destination (`00309C13`), and a later script read takes it from there; that read is not part of the bridge,",
              "  and its reader is unread. The bridge pops both out-references through `00267E10` *before* the reader runs, so",
              "  the transfer is unchanged only if the two destinations are valid, byte-disjoint and not overwritten before the",
              "  read (next subsection; FABLE 2026-10-02)."])),
    (AV, "**Limits kept.** These limits are ASTRA's and SPEC's.", AV_D),
    (AV, "proved. Natural rejection and whole OV-42 stay OPEN.", AV_NEW_SECTION),
]

def main():
    write = "--apply" in sys.argv
    texts, fails = {}, 0
    for rel, old, new in EDITS:
        p = os.path.join(DB, *rel.split("/"))
        if rel not in texts:
            texts[rel] = io.open(p, encoding="utf-8", newline="").read()
        t = texts[rel]
        crlf = "\r\n" in t
        o, n = (old.replace(NL, "\r\n"), new.replace(NL, "\r\n")) if crlf else (old, new)
        if n in t:   # several NEWs contain their OLD, so test NEW first
            print("ALREADY", os.path.basename(rel)); continue
        if t.count(o) != 1:
            print("MISS %s (%d): %s" % (os.path.basename(rel), t.count(o), old[:70])); fails += 1; continue
        texts[rel] = t.replace(o, n)
        print("WOULD PATCH" if not write else "PATCHED", os.path.basename(rel))
    if write and not fails:
        for rel, t in texts.items():
            io.open(os.path.join(DB, *rel.split("/")), "w", encoding="utf-8", newline="").write(t)
    print("FAILS %d" % fails)
    sys.exit(1 if fails else 0)

main()
