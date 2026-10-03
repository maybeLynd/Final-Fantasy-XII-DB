"""apply_batch6.py [--apply] - OPUS consumes FABLE's six routed OV-42 batch-6 texts (FABLE-REQ-OPUS-OV42-BATCH6-ROUTES-1002;
FABLE's reviews of ASTRA's caller-row, caller-quotient-bound, terminal-resource-helper, interpreter-transfer,
action-table-binding and mode17-query-boundaries packets, consumed on FABLE's pages at 28534fcdb) - OPUS, 2026-10-02.

- _types/fields.tsv: AuthoredTableHeader +0x08 / +0x0C reader lists widened (forward multiply sites, inverse sites 4-5).
- authored-data-table-registry.md: the AG-12 block corrected (FABLE's OLD -> NEW, FABLE concurring) and a new OPUS
  section: the forward readers, the two further inverse readers, the terminal helper's widths, the binder's ABI.
- where-mp-comes-from.md: EXP-061's late-veto sentence qualified, and a new OPUS section on the two masks.
- the-script-to-native-calling-convention.md: a new OPUS note on out-reference store width and PUSHV width / kind.
OPUS re-read every cited instruction at the bytes first (batch6_check.py, 63 checks). Idempotent; fields.tsv has mixed
EOLs, so rows are edited by splitlines(keepends=True) and only the evidence cell's end changes.
"""
import io
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
FIELDS = "_types/fields.tsv"
REG = "02-Resource-And-Asset-Pipeline/authored-data-table-registry.md"
MP = "10-Status-Periodic-Terminal/where-mp-comes-from.md"
CC = "01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md"
REV = "_index/candidates/fable-review-astra-ov42-"
REC = "_index/candidates/opus-ov42-batch6-routes-1002/"
TAG = (" || READERS ADDED 2026-10-02 (OPUS, from FABLE's reviews of ASTRA ov42-caller-row-preconditions / "
       "ov42-terminal-resource-helper): ")

ROWS = {
    ("AuthoredTableHeader", "0x08"): TAG + "forward (multiply) sites 00304850 + 0xD9, 0030D160 + 0x7F and 00305430 + "
    "0x58 / + 0xA0 / + 0x186 - each a movzx feeding a 32-bit imul whose product is added in 32 bits into the row "
    "register (so a table used this way must lie below 4 GB); inverse (divide) sites 00305640 + 0x4B and + 0x13C, "
    "each an UNSIGNED 32-bit div with no zero test (recordStride > 0 is a precondition there too).",
    ("AuthoredTableHeader", "0x0C"): TAG + "00304850 + 0xB3 / + 0xC7, 0030D160 + 0x59 / + 0x6D, 00305430 + 0x31 / "
    "+ 0x46, + 0x79 / + 0x8E and + 0x162 / + 0x177 (the forward row builds), 00305640 + 0x2E and + 0x128 (the "
    "inverse sites) - each resolved through 0020E600.",
}

AG12_OLD = ("> | `+0x14` u32 | `+= desc`, then **resolved** through `0020E620` and stored back (`00384647`–`00384662`); "
            "the resolved pointer is a sub-directory `{u16 count; u32 entry[count + 1]}` whose entries are each rebased by "
            "`desc` — the first `count` through the child binder `003846F0(&entry, rebased, 0)`, the last in place "
            "(`00384680`–`003846C7`) | |\n")
AG12_NEW = ("> | `+0x14` u32 | `+= desc` ~~, then **resolved** through `0020E620` and stored back~~ giving M, then "
            "**encoded** by `0020E620` (M minus the low DWORD of `01F83530`) and that encoded DWORD stored back, even when "
            "M is 0 (`00384647`–`00384662`); if M != 0 the sub-directory `{u16 count; u32 entry[count + 1]}` is reached by "
            "decoding the stored value with `0020E600` (zero-extend + the full QWORD `01F83530`), and its entries are each "
            "rebased by ~~`desc`~~ **M** — the first `count` through the child binder `003846F0(&entry, entry + M, 0)`, "
            "the last in place (`00384680`–`003846C7`) *(corrected 2026-10-02, OPUS, on FABLE's review of ASTRA "
            "`ov42-action-table-binding`: `0020E620` is the encoder, not a resolver; EBP = M at `003845F0` + 0x6B feeds "
            "both the child argument + 0xB9 and the in-place add + 0xC9)* | |\n")
P48_OLD = "> `+0x04` (count) and `+0x08` (stride) are not touched — they are values, not offsets."
P48_NEW = ("> `+0x04` (count) and `+0x08` (stride) are not ~~touched~~ written by any of the binder's own stores — they "
           "are values, not offsets. *(narrowed 2026-10-02, OPUS, on FABLE's review of ASTRA `ov42-action-table-binding`: "
           "that is the direct store footprint, not whole-call preservation; a nested directory overlapping the header "
           "can write them through the in-place add, e.g. a count-0 directory at `desc + 4` adds M to `desc + 8`.)*")

REG_SECTION = """
## The action table's forward readers, two more inverse readers and the binder's ABI (OPUS, 2026-10-02)

From FABLE's reviews of ASTRA's [`ov42-caller-row-preconditions`](../""" + REV + """caller-row-preconditions-1002/REVIEW.md),
[`ov42-caller-quotient-bound`](../""" + REV + """caller-quotient-bound-1002/REVIEW.md),
[`ov42-terminal-resource-helper`](../""" + REV + """terminal-resource-helper-1002/REVIEW.md) and
[`ov42-action-table-binding`](../""" + REV + """action-table-binding-1002/REVIEW.md), all ACCEPT-WITH-NARROWING.
OPUS re-read every instruction named here at the bytes ([`batch6_check.py`](../""" + REC + """batch6_check.py), 63 checks,
FAILS 0). Statements marked *(FABLE)* rest on FABLE's review scripts, not on this record's checks.

**The forward readers.** Three routines build a row pointer from an index through the slot `02EBF138` header. Each
multiplies by the `+0x08` stride and adds the product to the decoded `+0x0C` base in 32 bits.
- `00304850`: the index is the WORD at unit `+0x714`, latched at + 0x3D (`movzx r13d, word ptr [rsi + 0x64]`,
  RSI = unit + 0x6B0). An unsigned compare against 0x21E (+ 0x8E / + 0x92) leaves before the phase switch.
  - The row build: `+0x0C` at + 0xB3 / + 0xC7, the stride at + 0xD9, `imul ecx, eax` at + 0xE1 and `add r15d, ecx`
    at + 0xE4. The row is zero-extend32(low32(lookup) + id * stride).
  - The row is then used as a pointer, so the table must lie below 4 GB.
- `0030D160`: the index is the incoming DX (+ 0x27). The build: `+0x0C` at + 0x59 / + 0x6D, the stride at + 0x7F,
  and a 32-bit add into RSI at + 0x89.
- `00305430`: an unsigned 16-bit `cmp dx, 0x115` bounds the index (+ 0x16 / + 0x23). Three row builds follow: `+0x0C`
  at + 0x31 / + 0x46, + 0x79 / + 0x8E and + 0x162 / + 0x177, with the stride at + 0x58, + 0xA0 and + 0x186.
- The stride is re-read after each lookup call, the same two-load shape as the inverse sites. A positive stride is
  assumed by every inverse reader, and no forward site checks the descriptor's fields.

**Inverse readers four and five: the terminal cost helper `00305640`.**
- The sites: `+0x0C` at + 0x2E, the stride at + 0x4B, then `div r10d` at + 0x50. A second pair has `+0x0C` at + 0x128,
  the stride at + 0x13C and `div ecx` at + 0x143. Both are unsigned 32-bit divides with no zero test.
- Widths: the two comparators get `movzx edx, di` (+ 0x81, + 0x8C), the quotient mod 65536. The full 32-bit
  recomputed quotient is passed on at + 0x14A (`mov edx, eax`).
- Mode: + 0xA3 `test r12d, r12d` and + 0xA8 `setne` normalise the incoming flag to 0 / 1. The two stats writers
  get 16 plus that bit, not the raw flag *(FABLE)*.
- Own non-stack writes: DWORD unit `+0xE58` := 0 (+ 0x73) and WORD unit `+0xDC8` := 0xFFFF (+ 0x7A). Both are gated
  by unit, record and record byte `+5` == 0 *(FABLE)*.
- NULL preconditions: unit (+ 0x99 reads unit `+0x698` unconditionally), the record (+ 0xC4 reads its WORD `+0x28`),
  the descriptor, and a stride > 0 at both divides.

**The section binder's ABI** (`003845F0`, the AG-12 block above, as corrected):
- Entry: RCX = slot, RDX = descriptor. The action-table caller `00237FC0` passes RCX = &`02EBF138` and RDX = its own
  incoming ECX sign-extended (+ 0xF `movsxd`). FABLE's review traces that DWORD to directory `+0x3C`.
- `*slot = desc` (QWORD, + 0x4) comes before the null test and every rebase. `+0x0C` is addressed through RDX
  (+ 0x10); `+0x10`, `+0x18`, `+0x1C` and `+0x14` go through reloads of `*slot` (+ 0x21, + 0x32, + 0x43, + 0x54).
- The rebase is NOT idempotent: x != 0 becomes low32(x + low32(desc)), and there is no already-rebased flag.
- Widths: the encoder `0020E620` subtracts the low DWORD of `01F83530`, and the decoder `0020E600` zero-extends and
  adds the full QWORD. Only the low-32 round trip is exact. Full 64-bit identity needs the QWORD's upper half to be 0.
- Preconditions: valid, separate slot and descriptor storage, and sub-directory storage disjoint from the header.
"""

MP_OLD = "with the late global test removed is rejected."
MP_NEW = ("with the late global test removed is rejected. *(qualified 2026-10-02, OPUS, on FABLE's review of ASTRA "
          "`ov42-mode17-query-boundaries`: the global mask in that run was a substituted callee. The shipping "
          "`BattleTarget_ComputeGlobalEligibilityMask` zeroes its result and writes only the low WORD, so its high half "
          "is always 0. On the shipping code the late veto can come only from the unit mask's high half, which is the "
          "console's Invincible setting (`+0xC20`) read twice - see \"The two eligibility masks\" below.)*")

MP_SECTION = """
## The two eligibility masks (OPUS, 2026-10-02)

From FABLE's review of ASTRA's [`ov42-mode17-query-boundaries`](../""" + REV + """mode17-query-boundaries-1002/REVIEW.md)
(ACCEPT-WITH-NARROWING). OPUS re-read the global mask's zeroing, the setting getter and the settings root at the bytes
([`batch6_check.py`](../""" + REC + """batch6_check.py)). The unit mask's arms rest on FABLE's `rv_mode17q.py`.
- **Global** (`BattleTarget_ComputeGlobalEligibilityMask`, `0030B770`): the DWORD result is zeroed at + 0x15, and only
  its low WORD is written after that. The high WORD is 0 for every input. The low WORD is 0..31: bit `0x1` when `02089340` has any of 0x3080, bit `0x2` from
  bit `0x1` of `022C2158`, and bits `0x4`, `0x8` and `0x10` from its bits `0x400`, `0x200` and `0x800`.
- **Unit** (`0030B7F0(unit, edx)`): 0 unless the unit is non-NULL and bit `0x10` of its first DWORD is set. Its high
  WORD has two bits *(FABLE)*:
  - bit `0x1` when the first setting read is 1, unit `+0x698` is non-NULL and that record's byte `+5` is 0;
  - bit `0x2` when the second read is 2.
  Both reads go through `0017D470`, which returns DWORD `+0xC20` of the settings object. Two calls make two reads, so the
  high WORD is 0..3 in general and 0..2 when both reads see one value. The low bit `0x2` needs EDX != 0. The MP writer
  `00300CE0` passes EDX = 0 at both its call sites.
- **The settings root** (read by the accessor `0017D470` calls first): a non-NULL root at `01F81428` is returned as is, with no call. A NULL root
  allocates 0x10E8 bytes, runs the constructor `001CCB20` on success and stores the result as the root. A failed
  allocation leaves it NULL, and the getter then reads `[0xC20]`.
- **Premises:** an initialized root, no other write to the root or `+0xC20` during the query, and private frames
  under the Win64 ABI.
"""

CC_SECTION = """
## Out-reference stores and PUSHV width (OPUS, 2026-10-02)

From FABLE's review of ASTRA's [`ov42-interpreter-transfer`](../../""" + REV + """interpreter-transfer-1002/REVIEW.md)
(ACCEPT-WITH-NARROWING; 77 checks in FABLE's `rv_xfer.py`). This is a representation contract for the verbs on this
page that hand a script variable to a native writer:
- A native out-reference store is a raw DWORD, whatever width the script variable is declared with.
- PUSHV's width field (bits 28..31 of the reference word) and the variable's kind (its record WORD) are independent.
  One does not imply the other.
- Scopes 6 and 7 of the reference word resolve to base 0.
"""

EDITS_MD = [(REG, AG12_OLD, AG12_NEW), (REG, P48_OLD, P48_NEW), (REG, None, REG_SECTION),
            (MP, MP_OLD, MP_NEW), (MP, None, MP_SECTION), (CC, None, CC_SECTION)]


def tsv(apply):
    p = os.path.join(DB, FIELDS)
    lines = io.open(p, encoding="utf-8", newline="").read().splitlines(keepends=True)
    done = fails = 0
    for (typ, off), add in ROWS.items():
        idx = [i for i, l in enumerate(lines) if l.split("\t")[:2] == [typ, off]]
        if len(idx) != 1:
            print("FAIL row", typ, off, "x%d" % len(idx))
            fails += 1
            continue
        i = idx[0]
        body = lines[i].rstrip("\r\n")
        eol = lines[i][len(body):]
        if add.strip() in body:
            print("SKIP", typ, off)
            continue
        lines[i] = body + add + eol
        done += 1
        print("APPLY" if apply else "WOULD", typ, off)
    if apply and done:
        io.open(p, "w", encoding="utf-8", newline="").write("".join(lines))
    return fails


def md(apply):
    fails = 0
    for page, old, new in EDITS_MD:
        p = os.path.join(DB, page)
        t = io.open(p, encoding="utf-8", newline="").read()
        key = next(l for l in new.strip().splitlines() if l.strip() and (old is None or l not in old))
        if key in t or key.replace("\n", "\r\n") in t:
            print("SKIP", page)
            continue
        if old is None:
            nl = "\r\n" if "\r\n" in t[:2000] else "\n"
            nt = t.rstrip("\r\n") + nl + new.replace("\n", nl)
        else:
            o, n = old, new
            if o not in t and o.replace("\n", "\r\n") in t:
                o, n = o.replace("\n", "\r\n"), n.replace("\n", "\r\n")
            if t.count(o) != 1:
                print("FAIL anchor x%d" % t.count(o), page)
                fails += 1
                continue
            nt = t.replace(o, n)
        if apply:
            io.open(p, "w", encoding="utf-8", newline="").write(nt)
            t = nt
        print("APPLY" if apply else "WOULD", page)
    return fails


if __name__ == "__main__":
    a = "--apply" in sys.argv
    print("FAILS %d" % (tsv(a) + md(a)))
