"""gen_text_gap_classification.py - classifies the text-gap citations in place, by decoding each address.

PUBLISHED INTO THE KIT 2026-09-14 from `Tools/work/OPUS/classify_text_gaps.py`, which `.gitignore` excludes.
A canonical candidates file under `_index/candidates/` named it in its header, so the instruction
for reproducing a file this corpus cites pointed at a tool no peer had. Found by extending
`check_cited_instruments.py` to side files - it had been closed over `_index/*.md` and the kit's own
`*.py` and was blind to `.tsv` entirely.

THE BODY BELOW IS THE ORIGINAL, UNCHANGED. Rewriting its paths and defaults while publishing it
would mean the tool in the kit is not the tool that produced the file beside it, and seeing how the
rows were derived is the whole reason for publishing. The only addition is the two lines under this
docstring, which resolve the repository root from `__file__` and change into it so the tool's
repo-relative paths mean what they have always meant, from any working directory.

NAMED `gen_*`, NOT `check_*`: `run_gates.py` globs `check_*.py`, and a generator under that prefix
would run as a gate every suite and rewrite its own output as a side effect of auditing.

> **DO NOT RUN THIS WITHOUT READING THE NEXT SENTENCE.** IT EDITS `text-gap-citations-250.tsv` IN PLACE. Read what it writes before running it on a file whose verdicts are already settled.
"""
import os as _os
import sys as _sys

# The repository root, four levels above this file: gfz-scripts -> analysis-kit -> Tools -> Database
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.dirname(_os.path.abspath(__file__)))))))

# The original module docstring, kept verbatim:
# classify_text_gaps.py - adjudicate the 250 cited .text addresses that are in no listed body.
#
# The registry says of itself: *"EVERY ROW IS UNCONFIRMED. This file seeds the evidence; it decides
# nothing."* Deciding them is OPUS work, and it is what FINAL-AUDIT pass 1 is waiting on -- pass 1
# fails if a cited address *"is not a function (or is cited as one and is data)"*, and today those 250
# are re-read from scratch at every audit because no confirmation is ever recorded.
#
# The four verdicts the file defines:
#
#     TABLE     a jump/PSM/dispatch table belonging to prev_fn
#     UNLISTED  a real body the function list does not contain (UC-1)
#     PAD       alignment padding
#     DEFECT    cited as a function and is not one
#
# WHAT IS DECIDED MECHANICALLY AND WHAT IS NOT. Each test below is a *sufficient* condition with its
# evidence recorded in the `why` column, and anything that meets none of them is left UNCONFIRMED for
# a human read rather than being swept into the nearest bucket. **A verdict with no evidence is worth
# less than no verdict**, which is the whole reason this file was seeded rather than filled.
#
#   PAD       the bytes at the address are int3/nop filler AND the run reaches the next body
#   TABLE     four or more consecutive dwords at the address resolve, as image-base + dword, into
#             prev_fn's own body -- a rel32 table indexed off the image base, the form this binary
#             uses everywhere -- AND prev_fn contains an indirect jmp
#   UNLISTED  the bytes decode as a standard MSVC prologue and the decode runs to a ret/jmp without
#             desynchronising

import io, os, struct, sys, collections

_src = open(os.path.join("Database", "Tools", "work", "OPUS",
                         "falsify_saveload_widgets.py")).read().split("PASS, FAIL")[0]
exec(_src)

F = "Database/FFXII TZA/_index/candidates/text-gap-citations-250.tsv"
TEXT_LO, TEXT_HI = 0x00121000, 0x00121000 + 7996981


def dwords(va, n):
    off = fo(va)
    if off is None:
        return []
    return [struct.unpack_from("<I", d, off + 4 * i)[0] for i in range(n)]


FILLER = (0xCC, 0x90, 0x00)


def is_pad(va, upto):
    """Filler is int3, nop -- and ZERO. The first version knew only 0xCC and 0x90, and a gap of
    `00 00 00 00 ...` therefore fell through to the decoder, which read it as
    `add byte ptr [rax], al` repeated and called it unclassifiable. 2026-09-14, OPUS."""
    off = fo(va)
    if off is None:
        return False, 0
    k = 0
    while off + k < len(d) and d[off + k] in FILLER and (upto is None or va + k < upto):
        k += 1
    return k >= 1, k


def rel32_table_at(va, prev, maxskip=4):
    """A rel32 table whose start may be pushed a byte or two by an alignment nop.

    `00366636` is `66 90` -- a two-byte nop -- and then dwords that resolve into prev_fn's own body.
    Reading dwords from the cited address itself splits them across that nop and sees nothing, so
    try the next few alignments and report which one worked. 2026-09-14, OPUS.
    """
    if not prev or prev not in sizes:
        return None
    for skip in range(maxskip):
        dw = dwords(va + skip, 8)
        inside = [w for w in dw if prev <= IMAGE + w < prev + sizes[prev]]
        if len(inside) >= 4:
            return skip, len(inside)
    return None


def byte_index_table(va, upto, limit=64):
    """A run of small bytes: the index half of MSVC's two-level dense switch.

    The form is `movzx eax, byte [base + idx + d1]` then `mov eax,[base + eax*4 + d2]`, so the gap
    holds a byte table as well as a dword table. `00306D08` is `00 01 06 06 06 06 ...` -- every byte
    a valid index into a small target table, which is not something code looks like.
    """
    off = fo(va)
    if off is None:
        return None
    k, mx = 0, 0
    while off + k < len(d) and k < limit and (upto is None or va + k < upto):
        b = d[off + k]
        if b > 0x3F:
            break
        mx = max(mx, b)
        k += 1
    return (k, mx) if k >= 16 and mx >= 1 else None


def is_jmp_thunk(va):
    """A 5-byte `jmp rel32` followed by filler: a tail-call forwarder body the list does not hold."""
    off = fo(va)
    if off is None or d[off] != 0xE9:
        return None
    ins = next(MD.disasm(d[off:off + 5], va), None)
    if ins is None or ins.mnemonic != "jmp" or not ins.op_str.startswith("0x"):
        return None
    if off + 5 < len(d) and d[off + 5] not in FILLER:
        return None
    return int(ins.op_str, 16)


CALLEE_SAVED = ("rbx", "rbp", "rdi", "rsi", "r12", "r13", "r14", "r15")


def is_frame_setup(x):
    """A genuine MSVC entry, not merely an instruction that could appear anywhere.

    The first version accepted any `mov`, and promptly called `mov r10, qword ptr [rsp + 0x28]` a
    function start -- that is a body reading its fifth argument, which is code you find in the
    MIDDLE of a function as readily as at its head. An entry either saves a callee-saved register,
    opens a frame, or spills an argument into the shadow space. 2026-09-14, OPUS.
    """
    if x.mnemonic == "push" and x.op_str in CALLEE_SAVED:
        return True
    if x.mnemonic == "sub" and x.op_str.startswith("rsp,"):
        return True
    if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rsp + 0x"):
        try:
            disp = int(x.op_str.split("[rsp + ")[1].split("]")[0], 16)
        except (IndexError, ValueError):
            return False
        return disp in (8, 0x10, 0x18, 0x20)     # the four shadow-space slots
    return False


def looks_like_body(va, limit=0x400):
    off = fo(va)
    if off is None:
        return False, ""
    ins = list(MD.disasm(d[off:off + limit], va))
    if not ins:
        return False, ""
    if not is_frame_setup(ins[0]):
        return False, "%s %s" % (ins[0].mnemonic, ins[0].op_str)
    for x in ins[:120]:
        if x.mnemonic in ("ret", "jmp"):
            return True, "%s %s ... %s %s" % (ins[0].mnemonic, ins[0].op_str, x.mnemonic, x.op_str)
    return False, "%s %s (no ret within %d)" % (ins[0].mnemonic, ins[0].op_str, limit)


def switch_region(prev):
    """-> (lo, hi, bound, detail) for a TWO-LEVEL dense switch's tables, or None.

    The form, read whole rather than half:

        cmp   eax, 0x35                              ; bound
        ja    default
        lea   rdx, [rip - 0x1de704]                  ; rdx = image base
        movzx eax, byte  ptr [rdx + rax   + 0x1de790]  ; BYTE index table
        mov   ecx, dword ptr [rdx + rax*4 + 0x1de77c]  ; DWORD target table
        add   rcx, rdx
        jmp   rcx

    Two tables, not one, and the dword table is NOT bound+1 entries long -- it holds one entry per
    DISTINCT target, and the byte table maps each of the bound+1 indices onto one of them. Sizing the
    dword table as 4*(bound+1) overlaps it straight through the byte table and misses both. The dword
    table runs from its own displacement up to the byte table's; the byte table runs bound+1 bytes.
    2026-09-14, OPUS.
    """
    if not prev or prev not in sizes:
        return None
    s = stream(prev)
    for i, x in enumerate(s):
        if x.mnemonic != "cmp":
            continue
        b = next((o.imm for o in x.operands if o.type == X86_OP_IMM), None)
        if b is None or not (0 < b < 0x400):
            continue
        if not any(y.mnemonic in ("ja", "jae", "jnbe") for y in s[i + 1:i + 3]):
            continue
        base = bytedisp = dworddisp = None
        for y in s[i + 1:i + 12]:
            if y.mnemonic == "lea" and base is None:
                for o in y.operands:
                    if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP:
                        base = y.address + y.size + o.mem.disp
            elif base is not None and y.mnemonic in ("movzx", "movsx") and bytedisp is None:
                for o in y.operands:
                    if o.type == X86_OP_MEM and o.mem.index != 0 and o.mem.scale == 1 and o.mem.disp:
                        bytedisp = o.mem.disp
            elif base is not None and y.mnemonic == "mov" and dworddisp is None:
                for o in y.operands:
                    if o.type == X86_OP_MEM and o.mem.index != 0 and o.mem.scale == 4 and o.mem.disp:
                        dworddisp = o.mem.disp
        if base is None or dworddisp is None:
            continue
        if bytedisp is None:
            return (base + dworddisp, base + dworddisp + 4 * (b + 1), b,
                    "single-level rel32 table, bound 0x%X" % b)
        lo = base + min(bytedisp, dworddisp)
        hi = max(base + bytedisp + b + 1, base + dworddisp + 4 * (b + 1)
                 if dworddisp > bytedisp else base + bytedisp + b + 1)
        return (lo, hi, b,
                "two-level dense switch: dword table %08X, byte index table %08X, bound 0x%X"
                % (base + dworddisp, base + bytedisp, b))
    return None


_span_cache = {}


def table_span(prev):
    """-> (table_start, table_end_exclusive, bound) for prev's rel32 dispatch table, or None.

    Read from the dispatching code, not guessed from bytes: `dispatch()` already recovers the bound
    and the table address for this binary's `lea base ; mov eax,[base + idx*4 + disp] ; add rax,base`
    form, which is the same shape the UI screens use.
    """
    if prev in _span_cache:
        return _span_cache[prev]
    span = None
    if prev in sizes:
        b, _dflt, tbl, _c = dispatch(prev)
        if tbl is not None and b:
            span = (tbl, tbl + 4 * (b + 1), b)
    _span_cache[prev] = span
    return span


rows, head = [], None
raw = io.open(F, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
lines = raw.replace("\r\n", "\n").split("\n")
for line in lines:
    if line.startswith("#") or not line.strip():
        continue
    p = line.split("\t")
    if head is None and p[0] == "addr":
        head = p
        continue
    rows.append(p)
if head is None:
    head = ["addr", "prev_fn", "prev_name", "prev_end", "delta_from_end", "next_fn",
            "prev_fn_indirect_jmp", "first_bytes", "verdict", "why", "cited_by"]

ia, ip, ipe, inx, ind = (head.index("addr"), head.index("prev_fn"), head.index("prev_end"),
                         head.index("next_fn"), head.index("prev_fn_indirect_jmp"))
iv, iw = head.index("verdict"), head.index("why")

out = collections.Counter()
decided = []
for p in rows:
    va = int(p[ia], 16)
    prev = int(p[ip], 16) if p[ip] else None
    nxt = int(p[inx], 16) if p[inx] else None
    verdict, why = "UNCONFIRMED", ""

    pad, runlen = is_pad(va, nxt)
    if pad and nxt is not None and va + runlen >= nxt:
        verdict = "PAD"
        why = "int3/nop filler for %d bytes, reaching the next listed body %08X" % (runlen, nxt)
    else:
        dw = dwords(va, 8)
        inside = [w for w in dw if prev and prev <= IMAGE + w < (prev + sizes.get(prev, 0))]
        if len(inside) >= 4 and p[ind].strip().lower() == "yes":
            verdict = "TABLE"
            why = ("%d of the first 8 dwords resolve as image-base+rel32 into %08X's own body, and "
                   "%08X contains an indirect jmp" % (len(inside), prev, prev))
        else:
            ok, shape = looks_like_body(va)
            if ok:
                verdict = "UNLISTED"
                why = "decodes from this address as a body: %s" % shape
            else:
                # SECOND TABLE FORM, and the one that covers most of the residue. Rather than
                # guessing at a table's shape from its bytes, read the table's ADDRESS out of the
                # dispatching function itself: `lea rX,[rip+..]` giving a base, then
                # `mov eXX,[rX + rY*4 + disp]` whose displacement added to that base IS the table.
                # An address falling inside [table, table + 4*(bound+1)) is that table, decided from
                # the code that indexes it instead of from what its bytes happen to decode to.
                # 2026-09-14, OPUS.
                span = table_span(prev)
                if span and span[0] <= va < span[1]:
                    verdict = "TABLE"
                    why = ("inside the rel32 dispatch table %08X..%08X that %08X indexes "
                           "(bound 0x%X, read from its own dispatch code)"
                           % (span[0], span[1] - 1, prev, span[2]))
                else:
                    rt = rel32_table_at(va, prev)
                    bi = byte_index_table(va, nxt)
                    th = is_jmp_thunk(va)
                    if rt is not None:
                        skip, n = rt
                        verdict = "TABLE"
                        why = ("%d of 8 dwords at %08X resolve as image-base+rel32 into %08X's own "
                               "body%s" % (n, va + skip, prev,
                                           "" if not skip else
                                           " (the table starts %d byte(s) in, after an alignment nop)"
                                           % skip))
                    elif bi is not None and p[ind].strip().lower() == "yes":
                        k, mx = bi
                        verdict = "TABLE"
                        why = ("a %d-byte run of small indices (max 0x%X) and %08X carries an "
                               "indirect jmp - the index half of a two-level dense switch"
                               % (k, mx, prev))
                    elif th is not None:
                        verdict = "UNLISTED"
                        why = ("a 5-byte `jmp %08X` followed by filler - a tail-call forwarder body "
                               "the function list does not contain" % th)
                    else:
                        sw = switch_region(prev)
                        if sw and sw[0] <= va < sw[1]:
                            verdict = "TABLE"
                            why = ("inside %08X's %s (region %08X..%08X)"
                                   % (prev, sw[3], sw[0], sw[1] - 1))
                        elif p[ind].strip().lower() == "yes":
                            why = ("prev_fn has an indirect jmp but this reader could not locate "
                                   "its table")
    p[iv] = verdict
    if why:
        p[iw] = why
    out[verdict] += 1
    decided.append((va, verdict, why))

print("THE 250 TEXT-GAP CITATIONS, adjudicated where the evidence is sufficient\n")
for k, v in out.most_common():
    print("  %-12s %3d" % (k, v))
print("\n  sample of each verdict:")
seen = set()
for va, verdict, why in decided:
    if verdict in seen:
        continue
    seen.add(verdict)
    print("    %08X  %-10s %s" % (va, verdict, why[:110]))

if "--write" in sys.argv:
    # THE COLUMN HEADER IN THIS FILE IS ITSELF A `#` LINE. Emitting `head` as a bare TSV row as well
    # appends a 251st data row whose verdict column literally reads "verdict" -- which is what the
    # first write did, and what restoring from a backup undid. Keep every comment exactly as found
    # and write data rows only. 2026-09-14, OPUS.
    body = [l for l in lines if l.startswith("#")]
    for p in rows:
        body.append("\t".join(p))
    io.open(F, "w", encoding="utf-8", newline="").write(nl.join(body) + nl)
    print("\n  registry written")
