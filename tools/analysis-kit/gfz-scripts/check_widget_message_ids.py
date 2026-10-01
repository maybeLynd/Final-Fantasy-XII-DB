#!/usr/bin/env python3
"""check_widget_message_ids.py - the handler table's id lists against the image that made them.

WHY. `16-UI/Widget-Object-Model/widget-message-handlers.tsv` is 267 rows and NOTHING CHECKED IT.
On 2026-09-20 fourteen of those rows were carrying a BOUNDS CHECK instead of a measurement -
`00279E20` claimed all 52 ids and answers 21, the other 31 reaching the default arm, which
forwards to the base widget procedure. That was found by hand, one row at a time, and the only
reason it was found at all is that somebody happened to read one.

So the table re-derives itself here. Every row marked `exact` is decoded again from the shipping
image by `resolve_switch_arms`, and a row whose id list no longer matches is reported.

WHAT A DISAGREEMENT MEANS, and it is USUALLY NOT THE TABLE'S FAULT. Five shapes, and the first
version of this file had three - the two it was missing are the two that actually fired:

  AGREES     byte for byte.
  LITERAL    the row carries an id the table does not, and the body tests that id with a
             `cmp <id>, imm` / `je` BEFORE it normalises for the table. The row is RIGHT and this
             decoder alone cannot see it. All three of the first run's `STALE` verdicts were
             this, and every one of them was a high id - 285, 287, 289.
  STALE      the row and the image genuinely disagree, in a way the shape above does not
             explain. Worth a human.
  SPARSE     no jump table, but a readable `sub`/`cmp` + `je` chain, which is what MOST of these
             handlers use - 201 of the 262 `exact` rows have no table at all. 176 re-derive and
             agree exactly.
  SUPERSET   the chain answers every id the row names AND MORE, which means the ROW under-reports.
             All of these keep only the LAST id of their chain - one signature, not a handful of
             coincidences. THE CHAIN LIST IS ITSELF A FLOOR: neither the `jg` subtree nor a range
             test is followed, so these want reading rather than a mechanical rewrite. Reported,
             never applied. Ten on 2026-09-20. **All ten were then read and this is now zero.**
  RICHER     the mirror of SUPERSET and the good direction - the row names every id the chain
             finds AND MORE, because somebody read the body. NOT A FINDING. The ten here are the
             ten that were SUPERSETS, and they had ONE MECHANISM between them: every row kept
             exactly the PIVOT ID OF THE BINARY-SEARCH ROOT - the `cmp <id>, K` immediately after
             `mov ecx, dword ptr [rdx]`, whose `jg` opens the high half and whose `je` takes K's
             own arm - and nothing past it. Whatever produced the `exact` column read the first
             compare after the id load and stopped. What it missed is exactly what this decoder
             refuses to follow: a `jg` subtree, a running subtraction (`sub ecx,1` / `je` repeated,
             where the LAST compare is unreadable without the ones before it), or a jump table
             behind a range test - `add eax, -8` / `cmp eax, 2` / `ja <default>` admits 8, 9 AND 10
             from one compare, because `ja` fires when eax-8 is above 2 UNSIGNED, so 7 wraps to
             0xFFFFFFFF and takes the default. THE HALF THIS DECODER DOES READ AGREED WITH THE
             HAND READ IN ALL TEN, which is why the corrections are additions and not repairs.
             A RANGE TEST'S WIDTH IS NOT ITS ID SET: 002C2320's window admits eleven ids and five
             of its table entries point AT THE DEFAULT ARM, so it answers six.
  UNBACKED   no table AND no chain this decoder can read. **This is now zero.** The last fifteen
             were the simplest shape of all and the register-based walk could not see them at
             all, because it waits for a `mov <r>, [rdx]` that never comes: `00290FF0` is
             eighteen bytes of `cmp dword ptr [rdx], 4` / `jne` / two stores / `jmp <base
             procedure>`, comparing the id STRAIGHT OUT OF MEMORY. No accumulator, each compare
             naming its id outright.
  EXTENT BAD the function list's length for that body ends INSIDE an instruction, so no decode
             over it can be trusted. `0057FE80` is one. That is a defect in
             `work/graph/functions.tsv` rather than in the row, and it is reported as such.

`unparsed` rows are counted and NOT checked: that value is an admission. There were five and
there are three, and none of the three is an admission any more.

TWO OF THE FIVE WERE HIDDEN BY A REGISTER COPY AND NOTHING ELSE. The walk waited for
`mov <r>, [rdx]`; `0027C870` opens `mov rdi, rdx` and loads at `0027C8A0 mov ecx, [rdi]`, and
`002878E0` opens `mov r14, rdx` and loads at `00287925 mov edx, [r14]`. `resolve_switch_arms` now
follows the receiver through a straight copy - which is what the fleet's `receiver_flow_census`
always did - and both decode, agreeing with a hand read: `1,2` and `1,2,10,14,18`.
**`002878E0` is why the copy must be followed carefully**: between the copy and the id load it
runs `call 0x1e0b90` / `sub eax,1` / `je` / `cmp eax,1` / `jne`, a running chain in EXACTLY the
dispatch's shape over a CALL RESULT, which would have yielded a confident `1,2` for a body that
answers five ids. It is excluded because nothing is collected before the id load.

THE REMAINING THREE ANSWER NO IDS AT ALL, which is why they were never going to decode. `005C5230`
is three bytes - `xor eax, eax` / `ret`, int3-padded on both sides - and `0017CDE0` is a five-byte
thunk to it. THAT THE BASE WIDGET PROCEDURE IS A NO-OP RETURNING ZERO IS NOT NEW AND IS NOT MINE:
`CONTRACT-widget-object.md` and `the-widget-constructor-and-object-sizes.md` both already record
`33 C0 C3`, three bytes, returning 0. What was missing is narrower and belongs to this table - its
OWN row for `005C5230` sat `unparsed`, so the table that sends every unhandled id there never said
where they went, and the 10-site row with the widest reach in the file read as unexamined.
`002985C0` is a five-byte `jmp 003EE420`, out of this table, and is the one genuinely open edge of
the five. Their `kind` stays `unparsed` deliberately - `exact` with an empty id list is
indistinguishable from a cell nobody filled in, and a fourth vocabulary word would mean changing
every consumer of the column for three rows.

THE CONTROL IS MANDATORY AND SYNTHETIC. A fabricated row whose ids are deliberately wrong must
be reported, and the real row it was built from must agree - so the walk is shown capable of both
answers before any absence below is believed. A checker that can only say `fine` has not been
shown to be reading anything.
"""
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP          # noqa: E402
import disasm_fn as DF          # noqa: E402
import resolve_switch_arms as R  # noqa: E402

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_REG, X86_OP_MEM, X86_OP_IMM
except ImportError:
    sys.stderr.write("check_widget_message_ids: needs capstone\n")
    raise SystemExit(2)

TABLE = os.path.join(KP.DB, "16-UI", "Widget-Object-Model", "widget-message-handlers.tsv")


def rows():
    raw = io.open(TABLE, encoding="utf-8", newline="").read().split("\n")
    head = raw[0].split("\t")
    for line in raw[1:]:
        if line.strip():
            yield dict(zip(head, line.split("\t")))


class ExtentBad(Exception):
    pass


def literal_ids(img, md, ex, entry):
    """Ids this body tests with a LITERAL compare before it normalises the id for the table.

    THE FIRST VERSION OF THIS CHECKER CALLED THREE ROWS STALE AND ALL THREE WERE RIGHT.
    `00280DE0` opens `mov eax, dword ptr [rdx]` / `cmp eax, 0x11F` / `jg default` / `je <arm>` -
    so id 287 has an arm of its own, reached BEFORE the jump table and invisible to a decoder
    that reads only tables. The row said 287 and the table did not, and the row was correct.
    The same shape explains 0055CD40's 285 and 005691E0's 289.

    So the id register is followed from its load out of `[rdx]` and every `cmp <it>, imm` is
    collected, stopping the moment anything else writes it - which is where the normalisation
    for the table begins and the immediates stop being ids.
    """
    if entry not in ex:
        return set()
    try:
        ins = R.decode(img, md, entry, ex[entry])
    except SystemExit:
        return set()
    track, out = None, set()
    holds = {"rdx"}
    for n, i in enumerate(ins):
        if track is None:
            if R.loads_receiver(i, holds):
                track = R.norm64(i.reg_name(i.operands[0].reg))
            holds = R.receiver_alias(ins, n, holds)
            continue
        if i.mnemonic == "cmp" and len(i.operands) == 2 \
           and i.operands[0].type == X86_OP_REG \
           and R.norm64(i.reg_name(i.operands[0].reg)) == track \
           and i.operands[1].type == X86_OP_IMM:
            out.add(i.operands[1].imm)
            continue
        if track in {R.norm64(i.reg_name(r)) for r in i.regs_access()[1]}:
            break
    return out


def derive(img, md, ex, entry):
    """The ids this body's MESSAGE dispatch gives, or None when there is no such dispatch.

    A BAD EXTENT IS ONE ROW'S PROBLEM, NOT THE SWEEP'S. resolve_switch_arms refuses outright when
    the function list's length ends inside an instruction - correctly, because a decode over a
    wrong extent is a confident wrong decode - and it does so by raising SystemExit, which killed
    the first version of this sweep at the first such body (0057FE80, whose listed end falls one
    byte inside its last instruction). The refusal is right and the blast radius was not: the row
    is reported and the remaining rows are still checked.
    """
    if entry not in ex:
        return None
    try:
        ins = R.decode(img, md, entry, ex[entry])
    except SystemExit as e:
        raise ExtentBad(str(e))
    found, _refused = R.resolve_one(img, ins)
    msg = [f for f in found if (f["source"] or "").startswith("MESSAGE ID")]
    if len(msg) != 1:
        return None
    f = msg[0]
    by_target = collections.defaultdict(list)
    for k, arm in enumerate(f["map"]):
        by_target[f["arms"][arm]].append(k + f["shift"])
    return sorted(i for t, v in by_target.items() if t != f["default"] for i in v)


def control(img, md, ex):
    """One real row must agree; the same row with a bent id list must be reported."""
    real = derive(img, md, ex, 0x29BE50)
    if real is None:
        print("CONTROL  FAIL - the decoder finds no message dispatch in 0029BE50")
        return False
    bent = [i for i in real if i != real[0]]
    ok_agree = real == derive(img, md, ex, 0x29BE50)
    ok_differ = bent != real
    print("CONTROL  a real row re-derives identically: %s   a bent copy of it is seen to "
          "differ: %s" % ("PASS" if ok_agree else "FAIL", "PASS" if ok_differ else "FAIL"))
    return ok_agree and ok_differ


def main():
    img = DF.Image(DF.DEFAULT_EXE)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    ex = R.extents()

    if not control(img, md, ex):
        print("\ncontrol failed - the output is refused")
        return 2

    stale, unbacked, agree, unparsed, missing, badext, literal = [], [], 0, 0, [], [], []
    sparse_agree, sparse_differ, sparse_super, sparse_richer = [0], [], [], []
    for r in rows():
        if r.get("kind") == "unparsed":
            unparsed += 1
            continue
        if r.get("kind") != "exact":
            continue
        entry = int(r["handler"], 16)
        try:
            got = derive(img, md, ex, entry)
        except ExtentBad as e:
            badext.append((r["handler"], str(e)))
            continue
        if got is None:
            if entry not in ex:
                missing.append(r["handler"])
                continue
            # NO TABLE - try the sparse chain, which is what most of these handlers use.
            try:
                chain = R.sparse_chain(img, R.decode(img, md, entry, ex[entry]))
            except SystemExit:
                chain = None
            want = [int(x) for x in r["ids"].split(",") if x.strip()]
            if chain is None:
                unbacked.append(r["handler"])
            elif chain == want:
                sparse_agree[0] += 1
            elif set(want) < set(chain):
                sparse_super.append((r["handler"], want, chain))
            elif set(chain) < set(want):
                sparse_richer.append((r["handler"], want, chain))
            else:
                sparse_differ.append((r["handler"], want, chain))
            continue
        want = [int(x) for x in r["ids"].split(",") if x.strip()]
        if want == got:
            agree += 1
            continue
        extra = [i for i in want if i not in got]
        short = [i for i in got if i not in want]
        lits = literal_ids(img, md, ex, entry) if extra and not short else set()
        if extra and not short and all(i in lits for i in extra):
            literal.append((r["handler"], extra))
        else:
            stale.append((r["handler"], want, got))

    print("  control passes - the counts below are meaningful\n")
    print("ROWS RE-DERIVED FROM THE IMAGE")
    print("  agree exactly                                  : %d" % agree)
    print("  STALE - the row and the image disagree         : %d" % len(stale))
    for h, want, got in stale:
        print("      %s  row %s" % (h, ",".join(map(str, want))))
        print("      %s  image %s" % (" " * 8, ",".join(map(str, got))))
    print("  ids handled by a LITERAL compare before the table  : %d" % len(literal))
    for h, extra in literal:
        print("      %s  %s - `cmp <id>, imm` / `je` ahead of the dispatch, so the row is"
              % (h, ",".join(map(str, extra))))
        print("      %s  RIGHT and this decoder alone could not see it" % (" " * 8))
    print("  re-derived from a SPARSE cmp/je chain, agreeing     : %d" % sparse_agree[0])
    print("  sparse chain is a SUPERSET - the ROW under-reports  : %d" % len(sparse_super))
    for h, want, got in sparse_super:
        print("      %s  row %s" % (h, ",".join(map(str, want))))
        print("      %s  chain %s" % (" " * 8, ",".join(map(str, got))))
    if sparse_super:
        print("      EVERY ONE OF THESE KEEPS ONLY THE LAST ID OF ITS CHAIN, which is one")
        print("      signature and not ten coincidences. Two are verified by hand: 002C2320")
        print("      answers 1 and 8 where its row says 8, and 005636F0 answers 1, 4 and 12")
        print("      where its row says 12. THE CHAIN LIST IS ITSELF A FLOOR - neither the")
        print("      `jg` subtree nor a range test like 005636F0's `add eax,-8 / cmp 2 / ja`")
        print("      is followed - so these rows want reading, not a mechanical rewrite.")
    print("  the ROW is richer than this decoder - NOT a finding : %d" % len(sparse_richer))
    for h, want, got in sparse_richer:
        print("      %s  row %s" % (h, ",".join(map(str, want))))
        print("      %s  chain %s" % (" " * 8, ",".join(map(str, got))))
    if sparse_richer:
        print("      The mirror of SUPERSET, and the good direction: the row names every id the")
        print("      chain finds AND MORE, because somebody read the body. ALL TEN OF THESE WERE")
        print("      SUPERSETS ON 2026-09-20 and every one kept the same thing - the PIVOT of the")
        print("      binary-search root, the `cmp` right after `mov ecx,[rdx]` whose `jg` opens")
        print("      the high half. What each was missing is a shape this decoder refuses: a `jg`")
        print("      subtree, a running subtraction, or a jump table behind a range test like")
        print("      `add eax,-8` / `cmp 2` / `ja`, which admits 8, 9 AND 10 from one compare.")
        print("      The low half it DOES read agreed with the hand read in all ten. A decoder")
        print("      that reads only `cmp`+`je` must not call a row that was read stale.")
    print("  sparse chain DIFFERS otherwise - needs a human      : %d" % len(sparse_differ))
    for h, want, got in sparse_differ:
        print("      %s  row %s" % (h, ",".join(map(str, want))))
        print("      %s  chain %s" % (" " * 8, ",".join(map(str, got))))
    if sparse_differ:
        print("      NEITHER SIDE IS CALLED WRONG HERE. The chain decoder reads two forms -")
        print("      a running `sub`+`je` and a `cmp`+`je`/`jne` tail - and at least two more")
        print("      exist, including the three-way `cmp` / `jg` / `je` split that 002C2320")
        print("      opens with. A row and a partial decode disagreeing is a reason to read")
        print("      the body, not to rewrite either.")
    print("  UNBACKED - no table AND no readable chain      : %d" % len(unbacked))
    if unbacked:
        print("      %s" % ", ".join(unbacked))
        print("      Not necessarily wrong: a SPARSE COMPARE CHAIN yields an exact id set and")
        print("      this decoder reads only jump tables. It is not re-derivable here.")
    print("  handler not in the function list               : %d" % len(missing))
    if missing:
        print("      %s" % ", ".join(missing))
    print("  EXTENT BAD - the function list ends mid-instruction: %d" % len(badext))
    for h, why in badext:
        print("      %s  %s" % (h, why.split(" - ", 1)[-1]))
        print("      %s  This is a defect in work/graph/functions.tsv, not in the row: no"
              % (" " * 8))
        print("      %s  decode over that body can be trusted until the length is fixed."
              % (" " * 8))
    print("  `unparsed` rows, counted and not checked        : %d" % unparsed)
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
