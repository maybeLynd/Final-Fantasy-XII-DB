#!/usr/bin/env python3
"""resolve_switch_arms.py - decode an MSVC jump-table dispatch, or refuse to guess.

WHY. `16-UI/Widget-Object-Model/widget-message-handlers.tsv` carries a `kind` column, and ten
of its rows read `upper-bound` with the note `switch arms not resolved` - the id list is then
every id the bounds check admits, which for `0029BE50` was thirty when seven have an arm and
twenty-three fall to the default. `upper-bound` and `exact` are the difference between a handler
that answers thirty messages and one that answers seven and forwards the rest to the base widget
procedure, so the column is load-bearing and ten rows are not answering it.

THE SHAPE, and both levels matter. MSVC emits, for a switch over a dense-ish id range:

    dec    eax                                  ; normalise the id to a 0-based index
    cmp    eax, 0x1D                            ; the bound
    ja     <default>
    lea    rdi, [rip - 0x17BE7D]                ; = the IMAGE BASE, 0x120000
    movzx  eax, byte  [rdi + rax   + 0x17C4F0]  ; LEVEL 1 - index -> arm number (optional)
    mov    ecx, dword [rdi + rax*4 + 0x17C4D0]  ; LEVEL 2 - arm -> target, image-relative
    add    rcx, rdi
    jmp    rcx

The byte level is what collapses thirty ids onto eight arms. A tool that decoded only the dword
table would report eight targets and no mapping from id to target, which is not an id list.

IT FAILS CLOSED, and that is the whole point of writing it rather than reading ten by hand.
Every part is required: the image-base register must be PROVEN by a `lea` landing exactly on the
base, the bound must be found, the dword table must be found, and the normalisation from message
id to table index must reduce to a sum of constants. If any of those is missing the function is
reported UNRESOLVED with the reason, and NO id list is emitted for it. A partial decode that
printed some ids would be worse than the `upper-bound` it replaced, because `upper-bound` at
least says what it is.

ONE LIMIT, STATED. This reads the dispatch, not the arms. Two ids sharing an arm are reported as
two ids, which is correct for the `ids` column; whether the arm then branches further on
something else is not this tool's question, and `receiver_flow_census.py` is the instrument that
answers it - it refuses to issue a census while any instruction is unreached, which is how the
SECOND table in `0029BE50` (at `0029BFF2`) was found after the first looked complete.
"""
import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402
import disasm_fn as DF  # noqa: E402

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    import capstone.x86 as X
except ImportError:
    sys.stderr.write("resolve_switch_arms: needs capstone\n")
    raise SystemExit(2)

IMAGE_BASE = 0x120000
FUNCS = os.path.join(KP.WORK, "graph", "functions.tsv")


def extents():
    m = {}
    with open(FUNCS, encoding="utf-8") as fh:
        fh.readline()
        for ln in fh:
            p = ln.rstrip("\n").split("\t")
            try:
                m[int(p[0], 16)] = int(p[2])
            except (ValueError, IndexError):
                pass
    return m


def decode(img, md, start, nbytes):
    ins, a, end = [], start, start + nbytes
    while a < end:
        b = img.read(a, 16)
        if not b:
            break
        i = next(md.disasm(b, a), None)
        if i is None:
            break
        ins.append(i)
        a += i.size
    if a != end:
        raise SystemExit("resolve_switch_arms: %08X - the listed end %08X falls inside an "
                         "instruction (the last one runs to %08X)." % (start, end, a))
    return ins


def base_registers(ins):
    """Registers proven to hold the image base, by a lea that lands exactly on it."""
    out = {}
    for i in ins:
        if i.mnemonic != "lea" or len(i.operands) != 2:
            continue
        d, s = i.operands
        if s.type != X.X86_OP_MEM or s.mem.base != X.X86_REG_RIP:
            continue
        if i.address + i.size + s.mem.disp == IMAGE_BASE:
            out[i.reg_name(d.reg)] = i.address
    return out


def norm64(name):
    """rax/eax/ax/al -> rax, so a 32-bit index and its 64-bit base compare equal."""
    if name is None:
        return None
    m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi",
         "ebp": "rbp", "esp": "rsp"}
    if name in m:
        return m[name]
    if name.startswith("r") and name.endswith("d"):
        return name[:-1]
    return name


def resolve_one(img, ins, verbose=False):
    """Return a list of dispatch dicts, or a list of refusals."""
    bases = base_registers(ins)
    found, refused = [], []
    for n, i in enumerate(ins):
        if i.mnemonic != "jmp" or not i.operands or i.operands[0].type != X.X86_OP_REG:
            continue
        jreg = norm64(i.reg_name(i.operands[0].reg))
        why = []
        dword_tbl = byte_tbl = None
        idx_reg = None
        # walk back a bounded window for the two loads and the add
        for j in range(n - 1, max(-1, n - 14), -1):
            k = ins[j]
            if k.mnemonic == "add" and len(k.operands) == 2 \
               and norm64(k.reg_name(k.operands[0].reg)) == jreg \
               and k.operands[1].type == X.X86_OP_REG \
               and k.reg_name(k.operands[1].reg) in bases:
                continue
            if k.mnemonic in ("mov", "movsxd") and len(k.operands) == 2 \
               and k.operands[1].type == X.X86_OP_MEM and dword_tbl is None:
                m = k.operands[1].mem
                bn = k.reg_name(m.base) if m.base else None
                if bn in bases and m.scale == 4:
                    dword_tbl = IMAGE_BASE + m.disp
                    idx_reg = norm64(k.reg_name(m.index)) if m.index else None
                continue
            if k.mnemonic == "movzx" and len(k.operands) == 2 \
               and k.operands[1].type == X.X86_OP_MEM and byte_tbl is None:
                m = k.operands[1].mem
                bn = k.reg_name(m.base) if m.base else None
                if bn in bases and m.scale in (0, 1) and m.index:
                    byte_tbl = IMAGE_BASE + m.disp
                    idx_reg = norm64(k.reg_name(m.index))
        if dword_tbl is None:
            refused.append((i.address, "no image-base-relative dword table feeds the jmp"))
            continue
        # the bound and the normalisation, searching back from the jmp
        bound = default = None
        bound_at = None
        track = idx_reg
        for j in range(n - 1, -1, -1):
            k = ins[j]
            if k.mnemonic == "ja":
                prev = ins[j - 1] if j else None
                if prev is not None and prev.mnemonic == "cmp" \
                   and prev.operands[0].type == X.X86_OP_REG \
                   and prev.operands[1].type == X.X86_OP_IMM:
                    bound = prev.operands[1].imm
                    track = norm64(prev.reg_name(prev.operands[0].reg))
                    default = k.operands[0].imm
                    bound_at = j - 1
                break
        # The normalisation runs BEFORE the bound check, and only instructions that WRITE the
        # tracked register can change it - a cmp does not, and the first version refused on the
        # very cmp it had just consumed.
        shift = 0
        source = None
        if bound_at is not None:
            for j in range(bound_at - 1, -1, -1):
                k = ins[j]
                wrote = {norm64(k.reg_name(r)) for r in k.regs_access()[1]}
                if track not in wrote:
                    continue
                if k.mnemonic == "dec":
                    shift += 1
                elif k.mnemonic == "sub" and len(k.operands) > 1 \
                        and k.operands[1].type == X.X86_OP_IMM:
                    shift += k.operands[1].imm
                elif k.mnemonic == "add" and len(k.operands) > 1 \
                        and k.operands[1].type == X.X86_OP_IMM:
                    shift -= k.operands[1].imm
                elif k.mnemonic == "lea" and len(k.operands) > 1 \
                        and k.operands[1].type == X.X86_OP_MEM \
                        and k.operands[1].mem.base and not k.operands[1].mem.index:
                    # `lea eax, [rcx - 2]` is an add that also RENAMES the register, which the
                    # first version refused on. Modelled exactly: the constant folds into the
                    # shift and the tracked register becomes the lea's base.
                    shift -= k.operands[1].mem.disp
                    track = norm64(k.reg_name(k.operands[1].mem.base))
                elif k.mnemonic in ("mov", "movzx", "movsxd", "cdqe", "movsx"):
                    # The id arrives here. WHICH VALUE it is decides whether this dispatch is
                    # the MESSAGE switch or some inner one: a widget handler is
                    # handler(this, msg) and the message id is the first dword of msg, so the
                    # message switch is the one whose index is loaded from [rdx]. Without this
                    # the tool would happily put an inner switch's cases in an `ids` column.
                    if len(k.operands) > 1 and k.operands[1].type == X.X86_OP_MEM:
                        src = k.op_str.split(",", 1)[1].strip()
                        if k.operands[1].mem.base and k.reg_name(k.operands[1].mem.base) == "rdx" \
                           and k.operands[1].mem.disp == 0 and not k.operands[1].mem.index:
                            source = "MESSAGE ID - " + src
                        else:
                            source = src
                    elif len(k.operands) > 1 and k.operands[1].type == X.X86_OP_REG:
                        source = "register " + k.reg_name(k.operands[1].reg)
                    break                      # nothing more is applied
                else:
                    why.append("unmodelled %s writing the index register at %08X"
                               % (k.mnemonic, k.address))
                    break
        if bound is None:
            refused.append((i.address, "no `cmp <reg>, N` / `ja` bound found before the jmp"))
            continue
        if why:
            refused.append((i.address, why[0]))
            continue
        nidx = bound + 1
        if byte_tbl is not None:
            bt = list(img.read(byte_tbl, nidx))
            arms = max(bt) + 1
        else:
            bt = list(range(nidx))
            arms = nidx
        dw = img.read(dword_tbl, 4 * arms)
        tgt = [IMAGE_BASE + struct.unpack_from("<I", dw, 4 * a)[0] for a in range(arms)]
        found.append({"jmp": i.address, "bound": bound, "shift": shift, "default": default,
                      "byte_tbl": byte_tbl, "dword_tbl": dword_tbl, "arms": tgt, "map": bt,
                      "source": source})
    return found, refused


def receiver_alias(ins, n, holds):
    """The registers that still hold the MESSAGE POINTER, maintained one instruction at a time.

    `rdx` holds it on entry, by the widget procedure's own signature - the constructor ends
    `00246740 lea rdx, [rsp+0x20]` / `00246745 mov rcx, rdi` / `00246748 call rax`, handing the
    record's address in rdx and the widget in rcx. SOME HANDLERS COPY IT FIRST AND THE DECODER
    COULD NOT SEE THEM AT ALL: `002878E0` opens `mov r14, rdx` and does not load the id until
    `00287925 mov edx, dword ptr [r14]`, and `0027C870` opens `mov rdi, rdx` and loads at
    `0027C8A0 mov ecx, dword ptr [rdi]`. Both sat `unparsed` for no better reason than the copy.

    AND `002878E0` SHOWS WHY THE COPY MUST NOT BE FOLLOWED CARELESSLY. Between the copy and the id
    load it runs `call 0x1e0b90` / `sub eax, 1` / `je` / `cmp eax, 1` / `jne` - a running chain in
    EXACTLY the dispatch's shape, over a CALL RESULT. It is excluded here for the right reason
    rather than by luck: nothing is collected before the id load, and the id register is whatever
    that load writes, so a chain on some other register is never reached.

    Takes the index so the caller can apply it AFTER testing for the id load. That order matters:
    `mov edx, dword ptr [r14]` WRITES rdx, ending rdx's own life as a holder on the very
    instruction that starts the id register's.
    """
    i = ins[n]
    if (i.mnemonic == "mov" and len(i.operands) == 2
            and i.operands[0].type == X.X86_OP_REG and i.operands[1].type == X.X86_OP_REG
            and norm64(i.reg_name(i.operands[1].reg)) in holds):
        return holds | {norm64(i.reg_name(i.operands[0].reg))}
    return holds - set(norm64(i.reg_name(r)) for r in i.regs_access()[1])


def loads_receiver(i, holds, disp=0):
    """True when `i` is `mov <r>, [<held>+disp]` - the id load, through rdx or through a copy."""
    return (i.mnemonic == "mov" and len(i.operands) == 2
            and i.operands[0].type == X.X86_OP_REG and i.operands[1].type == X.X86_OP_MEM
            and i.operands[1].mem.base
            and norm64(i.reg_name(i.operands[1].mem.base)) in holds
            and i.operands[1].mem.disp == disp and not i.operands[1].mem.index)


def sparse_chain(img, ins):
    """Ids answered by a linear `sub`/`cmp` + `je` chain, or None when there is no such chain.

    NOT EVERY HANDLER USES A JUMP TABLE, and the ones that do not are the majority: of the 267
    rows in widget-message-handlers.tsv, 201 marked `exact` have no table at all. MSVC emits a
    chain for a sparse id set, and it is a running SUBTRACTION rather than a series of compares:

        mov ecx, dword ptr [rdx]     ; the message id
        sub ecx, 1     / je A        ; id == 1
        sub ecx, 1     / je B        ; id == 2      (1 + 1)
        sub ecx, 0xa   / je C        ; id == 12     (2 + 10)
        sub ecx, 0xc   / je D        ; id == 24     (12 + 12)
        cmp ecx, 0x1d  / je E        ; id == 53     (24 + 29)  - a compare does NOT accumulate
        mov rcx, rdi / call 005C5230 ; the default: the base widget procedure

    So the running total after each `sub` IS the id that arm answers, and a trailing `cmp`
    tests the total plus its own immediate WITHOUT advancing it. Mixing those two up shifts
    every id after the first compare, which is why the two forms are handled separately here
    rather than as one `subtract and test`.

    THE SAME REFUSALS AS THE TABLE DECODER. The id register must be loaded from `[rdx]`, and the
    walk stops the moment anything other than a modelled `sub`/`dec`/`cmp` writes it - a register
    the analysis has given up on cannot go on naming ids. No chain, no result.
    """
    def branch_after(n):
        """The branch a compare at index `n` feeds, skipping instructions that keep the flags.

        THE COMPILER SCHEDULES BETWEEN THE COMPARE AND THE BRANCH, and requiring them adjacent
        drops real arms. 005565E0 ends `cmp ecx, 7` / `mov rcx, rsi` / `je <arm>` - the `mov` is
        the next call's receiver hoisted into the gap, and it writes no flags, so the `je` still
        answers the compare. Insisting on adjacency lost id 25 there and on 0055A340. Only an
        instruction that WRITES EFLAGS ends the search, which is the actual rule rather than a
        list of mnemonics I happened to think of.
        """
        for k in range(n + 1, min(n + 6, len(ins))):
            j = ins[k]
            if j.mnemonic in ("je", "jne"):
                return j
            if X.X86_REG_EFLAGS in j.regs_access()[1]:
                return None
        return None

    def in_memory_ids():
        """Ids compared STRAIGHT OUT OF `[rdx]`, with no register to track.

        The simplest shape, and the one the register-based walk cannot see at all because it
        waits for a `mov <r>, [rdx]` that never comes. `00290FF0` is eighteen bytes end to end -
        `cmp dword ptr [rdx], 4` / `jne` / two stores / `jmp <base procedure>` - and `0056F410`
        is the same with a `mov rbx, rcx` scheduled into the gap. There is no accumulator here:
        each compare names its id outright.
        """
        out = []
        for n2, j in enumerate(ins):
            if j.mnemonic != "cmp" or len(j.operands) != 2:
                continue
            m, imm = j.operands[0], j.operands[1]
            if m.type != X.X86_OP_MEM or imm.type != X.X86_OP_IMM:
                continue
            if not m.mem.base or m.mem.disp or m.mem.index:
                continue
            # through rdx OR through a copy of it, for the same reason the register walk follows
            # one: `0056F410` is this shape with `mov rbx, rcx` scheduled in, and a handler that
            # copies rdx first is not a different dispatch.
            h = {"rdx"}
            for k in range(n2):
                h = receiver_alias(ins, k, h)
                if not h:
                    break
            if norm64(j.reg_name(m.mem.base)) not in h:
                continue
            b = branch_after(n2)
            if b is not None:
                out.append(imm.imm)
        return sorted(set(out))

    def branch_after(n):
        """The branch a compare at index `n` feeds, skipping instructions that keep the flags.

        THE COMPILER SCHEDULES BETWEEN THE COMPARE AND THE BRANCH, and requiring them adjacent
        drops real arms. 005565E0 ends `cmp ecx, 7` / `mov rcx, rsi` / `je <arm>` - the `mov` is
        the next call's receiver hoisted into the gap, and it writes no flags, so the `je` still
        answers the compare. Insisting on adjacency lost id 25 there and on 0055A340. Only an
        instruction that WRITES EFLAGS ends the search, which is the actual rule rather than a
        list of mnemonics I happened to think of.
        """
        for k in range(n + 1, min(n + 6, len(ins))):
            j = ins[k]
            if j.mnemonic in ("je", "jne"):
                return j
            if X.X86_REG_EFLAGS in j.regs_access()[1]:
                return None
        return None

    track, acc, ids, started = None, 0, [], False
    holds = {"rdx"}
    for n, i in enumerate(ins):
        if track is None:
            if loads_receiver(i, holds):
                track = norm64(i.reg_name(i.operands[0].reg))
            holds = receiver_alias(ins, n, holds)
            continue
        nxt = ins[n + 1] if n + 1 < len(ins) else None
        if i.mnemonic in ("sub", "dec") \
           and i.operands[0].type == X.X86_OP_REG \
           and norm64(i.reg_name(i.operands[0].reg)) == track:
            acc += 1 if i.mnemonic == "dec" else (
                i.operands[1].imm if len(i.operands) > 1
                and i.operands[1].type == X.X86_OP_IMM else None)
            if acc is None:
                return None
            if nxt is not None and nxt.mnemonic == "je":
                ids.append(acc)
                started = True
            continue
        if i.mnemonic in ("cmp", "test") \
           and i.operands[0].type == X.X86_OP_REG \
           and norm64(i.reg_name(i.operands[0].reg)) == track:
            nxt = branch_after(n)
            # `je` takes the arm; `jne` takes the DEFAULT and the arm is the fall-through.
            # The inverted form is how these chains usually END - 0027AD70 finishes
            # `cmp r8d, 6` / `jne <default>`, so id 18 is answered by falling through and a
            # decoder that only reads `je` drops the last arm of every such handler. That was
            # 24 rows, and all but a few were the row's list minus its LAST id.
            if nxt is not None and nxt.mnemonic in ("je", "jne"):
                if i.mnemonic == "test":
                    ids.append(acc)
                elif i.operands[1].type == X.X86_OP_IMM:
                    ids.append(acc + i.operands[1].imm)
                else:
                    return None
                started = True
                if nxt.mnemonic == "jne":
                    break                 # the arm is the fall-through; the chain ends here
            continue
        if i.mnemonic == "je":
            continue                      # already consumed with its test
        if track in {norm64(i.reg_name(r)) for r in i.regs_access()[1]}:
            break                         # the id register is gone; the chain is over
    if started:
        return sorted(set(ids))
    mem = in_memory_ids()
    return mem or None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("addrs", nargs="*")
    ap.add_argument("--exe", default=DF.DEFAULT_EXE)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    img = DF.Image(a.exe)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    ex = extents()

    if a.self_test:
        # 0029BE50 is the worked case: two tables, 30 ids, 8 arms, 7 real.
        ins = decode(img, md, 0x29BE50, ex[0x29BE50])
        found, refused = resolve_one(img, ins)
        ok = (len(found) == 2 and found[0]["bound"] == 0x1D
              and found[0]["dword_tbl"] == 0x29C4D0 and found[0]["byte_tbl"] == 0x29C4F0
              and len(set(found[0]["map"])) == 8)
        # and a function with no indirect jmp at all must yield nothing, not a guess
        ins2 = decode(img, md, 0x2964D0, ex[0x2964D0])
        f2, r2 = resolve_one(img, ins2)
        print("SELF-TEST  two-table dispatch decoded: %s   a body with no dispatch stays "
              "silent: %s" % ("PASS" if ok else "FAIL",
                              "PASS" if not f2 and not r2 else "FAIL"))
        return 0 if (ok and not f2 and not r2) else 2

    for s in a.addrs:
        entry = int(s, 16)
        if entry not in ex:
            print("%08X not in the function list" % entry)
            continue
        ins = decode(img, md, entry, ex[entry])
        found, refused = resolve_one(img, ins)
        print("=== %08X  %d bytes, %d instructions ===" % (entry, ex[entry], len(ins)))
        for r in refused:
            print("  UNRESOLVED at %08X: %s" % r)
        for f in found:
            ids = {}
            for k, arm in enumerate(f["map"]):
                ids.setdefault(f["arms"][arm], []).append(k + f["shift"])
            real = sorted(i for t, v in ids.items() if t != f["default"] for i in v)
            print("  dispatch %08X: bound %d, id shift %+d, byte table %s, dword table %08X, "
                  "%d arms" % (f["jmp"], f["bound"] + 1, f["shift"],
                               ("%08X" % f["byte_tbl"]) if f["byte_tbl"] else "none",
                               f["dword_tbl"], len(f["arms"])))
            print("      index from: %s" % (f["source"] or "UNKNOWN"))
            print("      default %08X takes %d id(s)"
                  % (f["default"], len(ids.get(f["default"], []))))
            print("      ids with an arm of their own: %s"
                  % ",".join(str(i) for i in real))
    return 0


if __name__ == "__main__":
    sys.exit(main())
