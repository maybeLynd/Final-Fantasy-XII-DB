"""apply_astra3.py [--apply] - three ASTRA returns consumed on the pages that state their functions (OPUS, 2026-10-02).

Board returns, each SPEC-accepted (SWE2-AUDIT-SPEC, 2026-10-01, ACCEPT, no narrowing beyond the presentation packet's
retained-invalid control-01 note):
  R1 ASTRA-RETURN-OPUS-SD194-STALE-NAME-SLICE-1001   _experiments/evidence/sd194-stale-name-slice/
     review _index/candidates/auditspec-review-astra-sd194-stale-name-slice-1001/REVIEW.md
  R2 ASTRA-RETURN-OPUS-PRESENTATION-INDEX-DOMAIN-1001 _experiments/evidence/presentation-index-domain/
     review _index/candidates/auditspec-review-astra-presentation-index-domain-1001/REVIEW.md
  R3 ASTRA-RETURN-OPUS-MODE-SUMMON-TAIL-1001          _experiments/evidence/mode-summon-tail/
     review _index/candidates/auditspec-review-astra-mode-summon-tail-1001/REVIEW.md

Every consumed fact was re-read at the shipping image with retool.py dis/callers (2026-10-02, OPUS):
  00377DC0 - r11 = entry RSP; three pushes and sub rsp, 0x290 put the post-prologue RSP at entry-0x2A8, so the
    output rsp+0x50 is entry-0x258 and the input rbp+0x60 (rbp = r11-0x1A8) is entry-0x148, 0x110 = 272 bytes apart;
    R9 = 0x103 at +0x43 before the copier call at +0x49; k = n-j-5 (+0xBE..+0xC3), +0xC copy count at +0xDC,
    RCX = rsp+0x5C, R8 = rbx at +0x106, memcpy thunk call at +0x109, four suffix stores +0x110..+0x12E,
    movsxd rax, edi at +0x133 before mov rdi, [rsp+0x280] at +0x13B, final byte store at +0x152, ret at +0x269.
  00309230 - null tests +0x5B / +0x68 select xor ecx, ecx (+0x8E); otherwise a second 0020E600 call (+0x74) and
    movzx edx, word [ctx+8] / imul ecx, edx, 0x113 / add ecx, eax (+0x80..+0x8A); cmp rbx, rcx at +0x90 (rbx = the
    entry RDX, +0x21); unequal: movzx eax, word [rbx+0x24] (+0x95); equal: [rdi+0x698] -> byte +4 (+0x9B, +0xA2),
    sub eax, 0x1B (+0xA6), cdqe, mov eax, [rsp+rax*4+0x20] (+0xAB), no compare between. 00306BD0+0x7D calls it,
    +0x82 mov edx, eax, +0x86 calls 0032FC30.
  00313550 - and eax, 1 / cmp eax, ecx (+0x10, +0x13); OR or AND, store, jmp 0035C620 (+0x25, +0x34); ret +0x39.
    0035C620 = lea rcx, [022CA408] / jmp 00273E30. 00273E30: eax = 0x1210, call 00808F10 (+0x25), xor eax, eax
    (+0x62), QWORD stores [rcx], [rcx+8], [rcx+0x10], [rcx+0x18] at +0x6E, +0x77, +0x7E, +0x85.
    Callers of 00313550: 00328BD0, 0034E1F0 (ecx = 1), 0034FE80, 0050FFB0 (raw popped int).

Each edit is a qualifying addition *(qualified 2026-10-02, OPUS: ...)*; nothing is struck (no accepted result refutes
a page statement; the packets narrow and qualify). Interior addresses are entry+offset. No code-block, front-matter or
heading edits; no table column changes. Natural reachability, inherited bytes, loaded-CRT behaviour, natural
type/context admission and the full 00273E30 body stay open as the packets keep them.
Exact substrings, each once, matched in LF or CRLF form; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
Q = "*(qualified 2026-10-02, OPUS"
EFX = "17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md"
MAP = "03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md"
BAND = "04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md"
AVAIL = "07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md"
CRM = "00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md"
LAD = "00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md"
PRI = "01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md"
BSB = "11-Party/Battle-State-Block/the-battle-state-block-field-map.md"
CBSB = "11-Party/Battle-State-Block/CONTRACT-battle-state-block.md"
BSR = "08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md"

SD = "[`sd194-stale-name-slice`](../../_experiments/evidence/sd194-stale-name-slice/README.md)"
PX = "[`presentation-index-domain`](../../_experiments/evidence/presentation-index-domain/README.md)"
MS = "[`mode-summon-tail`](../../_experiments/evidence/mode-summon-tail/README.md)"
FIVE = "[five-small-bin-tables.md](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md)"
PREFIX = ("given a normal stack-probe return, a valid private frame, a writable receiver and no interference")

EDITS = [
    # ---- R1: 00377DC0's name builder (sd194-stale-name-slice) ----
    # R1a: the .efb name is one branch's output, not the request's universal path.
    (EFX, "  extension: `PS2Data\\efb\\<stem>.efb`.",
     "  extension: `PS2Data\\efb\\<stem>.efb` " + Q + ": that name is built on one branch only - when the copied "
     "name has a `\\` or `/` with more than four bytes after the last one; with no separator, or exactly four bytes "
     "after it, the request names an empty string, and with 0-3 bytes after it the copied name is kept whole - the "
     "'Not settled here' paragraph below, from ASTRA's SPEC-accepted " + SD + ", method A)*."),
    # R1b: positions, the captured signed index, the copy count, normal-return-only suffix, no memcpy safety,
    #      premises; and R9 = 0x103 is a character limit, not a capacity.
    (EFX, "contract is exceeded for those inputs — a contract limit, not an observed fault).",
     "contract is exceeded for those inputs — a contract limit, not an observed fault) " + Q + ", consuming the same "
     "packet after its SPEC ACCEPT: the input sits at entry-RSP−0x148 (`rbp+0x60`) and the copied output at "
     "entry-RSP−0x258 (post-prologue `rsp+0x50`), 272 bytes apart, so the first n+1-byte copy is disjoint over the "
     "admitted domain; the −4..−1 index is the signed EDI captured at `00377DC0`+0x133 before RDI is restored at "
     "+0x13B, and the byte store at +0x152 lands outside the copied output but inside the allocated frame - no crash "
     "or frame damage is inferred; the `memcpy` count `k+12` (call at +0x109) includes the 12-byte prefix allowance, "
     "and the suffix stores at output+k+12..15 and the NUL at +k+16 follow only under a normal return and ABI - they "
     "are not observed native effects; the nine overlap classes are hypothetical arithmetic over admitted lengths, so "
     "there is no universal memcpy safety and no claim about the loaded VCRUNTIME140 `memcpy`; the whole reading "
     "assumes valid stack memory, a first NUL at n ≤ 259 and normal ABI and noninterference, none of which a failed "
     "lookup supplies; and the `R9 = 0x103` passed at +0x43 is the namespace copier's signed character limit, not a "
     "proven destination capacity - the copier's own limit semantics are a separate retained-source question)*."),
    # R1c: the claim table's runtime row - what is static now and what stays runtime.
    (EFX, "| runtime (**SD-194**, registered 2026-10-01) |",
     "| runtime (**SD-194**, registered 2026-10-01) " + Q + ": the static branch footprint on that path is settled "
     "under stated premises by ASTRA's SPEC-accepted sd194-stale-name-slice; the inherited bytes and which fields "
     "load stay runtime)* |"),
    # R1d: the map-pack page's 'built from the same path' holds on the positive branch only.
    (MAP, "(`00377E8A`–`00377EEE`), with completion",
     "(`00377E8A`–`00377EEE`) " + Q + ": that name is built only when the copied path has a `\\` or `/` with more "
     "than four bytes after the last one; otherwise the request carries an empty string or the copied path "
     "unchanged - ASTRA's SPEC-accepted " + SD + ", method A, under valid stack memory, a first NUL within 259 bytes "
     "and normal ABI; [the EFX/EFB page](../../17-Presentation-Rendering/Effect-File-Formats/"
     "efx-and-efb-effect-containers.md) §2b)*, with completion"),
    # R1e: the frame line - the two buffers' entry-relative positions and the R9 limit.
    (MAP, "`0x290` frame\n(`00377DC0`/`00377DCF`).",
     "`0x290` frame\n(`00377DC0`/`00377DCF`) " + Q + ": a 618-byte body, ret at `00377DC0`+0x269; the name input "
     "sits at entry-RSP−0x148 (`rbp+0x60`) and the copied output at entry-RSP−0x258 (`rsp+0x50` after the "
     "prologue), 272 bytes apart; the `R9 = 0x103` at +0x43 is the copier's signed character limit, not a proven "
     "destination capacity - ASTRA's SPEC-accepted sd194-stale-name-slice, method A)*."),

    # ---- R2: 00309230's presentation selector (presentation-index-domain) ----
    (BAND, "only one that uses the band as an **index**:",
     "only one that uses the band as an **index** " + Q + ", from ASTRA's SPEC-accepted " + PX + ", method A: the "
     "test below compares the full 64-bit entry RDX, the row pointer, with a zero-extended 32-bit value at "
     "`00309230`+0x90 - `low32(the second ImageAddress_ResolveRuntimePointer return) + u16(context+8) × 0x113`, or 0 "
     "when the global context or the first return is null; the two returns and the two context reads are not assumed "
     "identical, and equality also needs RDX's upper 32 bits zero. The ordinary arm returns the u16 at row `+0x24` "
     "zero-extended (0..65535) without looking at the type. The indexed arm has no local bound: its read stays inside "
     "the thirteen initialised DWORDs only for type 27..39, and other types predict reads of the frame's gap, its "
     "stack cookie, saved registers, the return address or caller bytes - predicted addresses under a normal call and "
     "a valid frame, not observed values or faults. Which types and contexts naturally reach the equal arm stays "
     "open)*:"),
    (BAND, "`0x1B` differently, and the difference is not the bound — **it uses `type − 0x1B` as an index**:",
     "`0x1B` differently, and the difference is not the bound — **it uses `type − 0x1B` as an index** " + Q + ": and "
     "it applies no bound of its own - nothing tests the type between its load at `00309230`+0xA2 and the table read "
     "at +0xAB; see the §5 qualification above)*:"),
    (AVAIL, "    raw record's type byte minus `0x1B` with no bound check (`003092D6`..`003092DB`).",
     "    raw record's type byte minus `0x1B` with no bound check (`003092D6`..`003092DB`) " + Q + ", from ASTRA's "
     "SPEC-accepted " + PX + ", method A: 'row `0x113`' is a full 64-bit compare of the entry RDX with the "
     "zero-extended 32-bit `low32(second resolver return) + u16(context+8) × 0x113`, or 0 when the context or the "
     "first return is null, the two resolver returns and context reads not assumed identical; the `+0x24` arm "
     "returns the word zero-extended (0..65535) without the type; the table read is in bounds only for type 27..39, "
     "and out-of-band addresses are source predictions, not observed faults or values; the returned EAX reaches "
     "`0032FC30` as EDX with no index check between, a source transfer not shown to occur in play; natural type and "
     "context admission stays OPEN)*."),

    # ---- R3: 00313550's raw compare and the native tail (mode-summon-tail) ----
    (CRM, "nothing and does not jump.*\n",
     "nothing and does not jump.* " + Q + ", from ASTRA's SPEC-accepted " + MS + ", method A: 'equals' is "
     "`(flags & 1)` against the raw 32-bit ECX (`00313550`+0x13), so the no-write path is guaranteed only for the 0/1 "
     "values the API is meant to pass; with bit 0 set, any other nonzero argument stores the same flags and still "
     "jumps - a source countermodel, no shipped caller shown passing one. And the jump is not an inert notification: "
     "`0035C620` replaces RCX with the fixed object `022CA408` - the battle-menu text widths of " + FIVE + " (FABLE) - "
     "and enters the 2,382-byte UI initializer whose prefix, " + PREFIX + ", zeroes `[022CA408, 022CA428)`; the "
     "rest of that body, its later effects and any notifications are not read, and a stub at either address shows "
     "only the interception)*\n"),
    (CRM, "the tail call to `0035C620`, a recorded boundary);",
     "the tail call to `0035C620`, a recorded boundary " + Q + ": the replay recorded the jump, not what the native "
     "tail does - its prefix zeroes 32 bytes at `022CA408`, §7's 2026-10-02 qualification)*);"),
    (LAD, "paths tail `0035C620` to propagate.",
     "paths tail `0035C620` to propagate " + Q + ", from ASTRA's SPEC-accepted " + MS + ": 'equal' is the raw "
     "32-bit ECX against bit 0, so 'changed' holds for 0/1 arguments only - with the bit set, any other nonzero value "
     "rewrites the same flags and still tails (a source countermodel, no natural caller shown); and the tail is more "
     "than propagation: it hands the fixed object `022CA408` to a 2,382-byte UI initializer whose prefix zeroes the "
     "object's first 32 bytes, under a normal stack probe, a valid frame and receiver and no interference; the rest "
     "of that body is not read)*."),
    (PRI, "and then tail-jumps into the notify;",
     "and then tail-jumps into the notify " + Q + ", from ASTRA's SPEC-accepted " + MS + ": 'differs' is a raw 32-bit "
     "compare of the argument with bit 0, so only 0/1 arguments guarantee no write on an unchanged bit - this verb "
     "passes 1; and the notify is not inert: it hands the fixed object `022CA408` to a UI initializer whose prefix "
     "zeroes the object's first 32 bytes, under a normal stack probe, a valid frame and receiver and no "
     "interference; later effects are not read)*;"),
    (BSB, "state-block singleton handed to the shared setter.",
     "state-block singleton handed to the shared setter " + Q + ": `022CA408` is a fixed static object, the "
     "battle-menu text-width words of " + FIVE + " (FABLE), not the block behind `02EBF190`; and the jump is not a "
     "bare forward - " + PREFIX + ", `00273E30`'s prefix zeroes `[022CA408, 022CA428)` with four QWORD stores "
     "(`00273E30`+0x6E..+0x85) before the uncaptured rest of its 2,382 B; a stub at either address shows only the "
     "interception; ASTRA's SPEC-accepted " + MS + ", method A)*."),
    (CBSB, "(calling a notifier when it was set)",
     "(calling a notifier when it was set " + Q + ": not an inert notifier - it hands the fixed object `022CA408`, "
     "the battle-menu text widths, to a UI initializer whose prefix zeroes the object's first 32 bytes under a normal "
     "stack probe, a valid frame and receiver and no interference; ASTRA's SPEC-accepted mode-summon-tail)*)"),
    (BSR, "calls the propagation step `0035C620`;",
     "calls the propagation step `0035C620` " + Q + ": not a pure propagation - it hands the fixed object `022CA408` "
     "to a UI initializer whose prefix zeroes 32 bytes of it, under a normal stack probe and no interference; ASTRA's "
     "SPEC-accepted mode-summon-tail)*;"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        if old in new:
            print("NEW CONTAINS OLD", rel.split("/")[-1], old[:40]); fails += 1; continue
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
