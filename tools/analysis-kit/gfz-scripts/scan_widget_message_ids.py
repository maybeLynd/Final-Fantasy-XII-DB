"""Which message ids does a widget actually handle? Read from the dispatchers themselves.

WHY IT MATTERS RATHER THAN BEING TRIVIA. scan_widget_proc_abi.py can prove a function's first
argument is a widget when it sends a STATIC MESSAGE RECORD through the object's own proc - but
only for records some already-trusted function sends, which leaves the transition stepper
00246C20 vouching only for itself. The other half of the same contract closes it: a message id
that a REGISTERED HANDLER dispatches on is, by construction, a widget message id, because a
registered handler is invoked by the constructor's own callback slot. Combine the two and a
record is a widget message when its id is in the handled vocabulary AND it is sent through an
[obj] proc call - two independent conditions, neither of them resemblance.

HOW A HANDLER DECODES ITS ID, and it is why this needs a reader rather than a grep. The
dispatchers do not compare against the id; they SUBTRACT AND FALL THROUGH:

    mov  ecx, dword ptr [rdx]     ; the message id
    sub  ecx, 1                   ; now ecx = id - 1
    je   L_one                    ;   ... so this arm is id 1
    sub  ecx, 1                   ; now ecx = id - 2
    je   L_two                    ;   ... id 2
    cmp  ecx, 0x10                ; ecx is ALREADY id - 2 here
    je   L_three                  ;   ... so this arm is id 0x12, NOT 0x10
    jmp  <default handler>

That last line is the trap, and this store walked into it twice in one day and corrected it by
hand. This reader carries the accumulated subtraction, so it cannot make that mistake.

THE CONTROL is the two handlers whose arms were read by hand and then corrected: 002985D0 must
come back as {1, 2, 0x12} and 00298250 as {1, 2, 0x0F}. If the reader disagrees with the hand
reading, one of them is wrong and neither result may be used.

THE OTHER SHAPE IS A JUMP TABLE, and it is fully readable rather than a wall: `dec eax ; cmp
eax,N ; ja <default>`, then a BYTE table mapping id-1 to a case index and a DWORD table mapping
that index to an image-relative target. An id is HANDLED when its case target differs from the
out-of-range destination - and the default case is not assumed to be any particular index, it
is identified as the one whose target IS that destination. Adding this took the decoded count
from 22 of 40 to 27 and the vocabulary from 14 ids to 32.

WHAT IT STILL DOES NOT DECODE is reported rather than hidden: 13 handlers whose chain this
reader loses are counted as UNDECODED and their ids are simply absent. The vocabulary is
therefore a LOWER BOUND on what widgets handle - the safe direction, since it is used to admit
things.

    scan_widget_message_ids.py [--verbose]
"""
import argparse
import collections
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP, X86_REG_R8

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
OUT = os.path.join(ROOT, "Database", "FFXII TZA", "16-UI", "widget-message-ids.tsv")
CTORS = (0x245000, 0x2465F0)
CONTROL = {0x2985D0: {1, 2, 0x12}, 0x298250: {1, 2, 0x0F}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    raw = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off, secs = pe + 24 + opt, []
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((nm, ib + va, vs, rs, pr))
        off += 40

    def fo(x):
        for nm, va, vs, rs, pr in secs:
            if va <= x < va + vs and (x - va) < rs:
                return pr + (x - va)
        return None

    tlo = thi = 0
    for nm, va, vs, rs, pr in secs:
        if nm == ".text":
            tlo, thi = va, va + vs

    funcs = []
    with io.open(FUNCS, encoding="utf-8") as fh:
        next(fh)
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) >= 3:
                try:
                    funcs.append((int(c[0], 16), int(c[2])))
                except ValueError:
                    pass
    flen = dict(funcs)

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    cache = {}

    def body(entry):
        if entry not in cache:
            n, f = flen.get(entry, 0), fo(entry)
            cache[entry] = [] if (f is None or n <= 0) else list(md.disasm(raw[f:f + n], entry))
        return cache[entry]

    handlers = set()
    for entry, _ in funcs:
        r8 = None
        for i in body(entry):
            o = i.operands
            if (i.mnemonic == "lea" and len(o) == 2 and o[0].type == X86_OP_REG
                    and o[0].reg == X86_REG_R8):
                t = None
                if o[1].type == X86_OP_MEM and o[1].mem.base == X86_REG_RIP:
                    t = i.address + i.size + o[1].mem.disp
                r8 = t if (t and tlo <= t < thi) else None
            elif (i.mnemonic in ("call", "jmp") and len(o) == 1 and o[0].type == X86_OP_IMM
                    and o[0].imm in CTORS and r8):
                handlers.add(r8)

    def decode(entry):
        """Ids this handler dispatches on, or None if the chain could not be followed."""
        ins = body(entry)
        if not ins:
            return None
        # find the register that receives the message id, and where
        idreg, start = None, None
        for k, i in enumerate(ins[:24]):
            o = i.operands
            if (i.mnemonic in ("mov", "movzx", "movsx") and len(o) == 2
                    and o[0].type == X86_OP_REG and o[1].type == X86_OP_MEM
                    and o[1].mem.base and o[1].mem.base != X86_REG_RIP
                    and o[1].mem.disp == 0 and md.reg_name(o[1].mem.base) in ("rdx", "edx")):
                idreg = md.reg_name(o[0].reg)
                start = k + 1
                break
        if idreg is None:
            return None
        ids, acc, table = set(), 0, False
        for i in ins[start:start + 40]:
            o = i.operands
            nm = i.mnemonic
            if o and o[0].type == X86_OP_REG and md.reg_name(o[0].reg) == idreg:
                if nm == "sub" and len(o) == 2 and o[1].type == X86_OP_IMM:
                    acc += o[1].imm
                    continue
                if nm == "add" and len(o) == 2 and o[1].type == X86_OP_IMM:
                    acc -= o[1].imm
                    continue
                if nm == "dec":
                    acc += 1
                    continue
                if nm == "inc":
                    acc -= 1
                    continue
                if nm == "cmp" and len(o) == 2 and o[1].type == X86_OP_IMM:
                    pending = acc + o[1].imm
                    continue
                if nm == "test" and len(o) == 2 and o[1].type == X86_OP_REG \
                        and md.reg_name(o[1].reg) == idreg:
                    pending = acc
                    continue
                if nm in ("mov", "movzx", "movsx", "xor", "and", "or", "shr", "shl"):
                    return sorted(ids) if ids else None
            if nm in ("je", "jz"):
                ids.add(locals().get("pending", acc))
                continue
            if nm in ("jne", "jnz"):
                continue
            if nm in ("ja", "jae", "jb", "jbe", "jg", "jge", "jl", "jle"):
                table = True
                continue
            if nm == "jmp" and o and o[0].type == X86_OP_REG:
                table = True
                break
            if nm == "jmp":
                break
            if nm == "ret":
                break
        if not ids:
            return None
        return sorted(ids) + (["TABLE"] if table else [])

    def decode_table(entry):
        """The jump-table form, which is most of what the chain reader loses.

        The shape is fixed and fully readable:

            mov  eax, dword ptr [rdx]                 the message id
            dec  eax                                  -> id - 1   (the accumulated offset)
            cmp  eax, N ; ja <default>                out of range goes to the default handler
            lea  rdx, [<image base>]
            movzx eax, byte ptr [rdx + rax + BYTEOFF] a byte table: id-1 -> case index
            mov  ecx, dword ptr [rdx + rax*4 + DWOFF] a dword table: case index -> rel32 target
            add  rcx, rdx ; jmp rcx

        An id is HANDLED when its case target differs from the `ja` destination. The default
        case is not assumed to be any particular index: it is identified as the one whose
        target IS the out-of-range destination, which is what the compiler guarantees.
        """
        ins = body(entry)
        acc = None
        limit = defdest = byteoff = dwoff = None
        idreg = None
        for k, i in enumerate(ins[:40]):
            o = i.operands
            nm = i.mnemonic
            if (idreg is None and nm in ("mov", "movzx") and len(o) == 2
                    and o[0].type == X86_OP_REG and o[1].type == X86_OP_MEM
                    and o[1].mem.base and o[1].mem.base != X86_REG_RIP
                    and o[1].mem.disp == 0 and md.reg_name(o[1].mem.base) in ("rdx", "edx")):
                idreg, acc = md.reg_name(o[0].reg), 0
                continue
            if idreg is None:
                continue
            if o and o[0].type == X86_OP_REG and md.reg_name(o[0].reg) == idreg:
                if nm == "dec":
                    acc += 1
                elif nm == "sub" and len(o) == 2 and o[1].type == X86_OP_IMM:
                    acc += o[1].imm
                elif nm == "cmp" and len(o) == 2 and o[1].type == X86_OP_IMM:
                    limit = o[1].imm
            if nm == "ja" and o and o[0].type == X86_OP_IMM:
                defdest = o[0].imm
            if (nm == "movzx" and len(o) == 2 and o[1].type == X86_OP_MEM
                    and o[1].mem.index != 0 and o[1].mem.scale == 1 and o[1].size == 1):
                byteoff = o[1].mem.disp
            if (nm == "mov" and len(o) == 2 and o[1].type == X86_OP_MEM
                    and o[1].mem.index != 0 and o[1].mem.scale == 4 and o[1].size == 4):
                dwoff = o[1].mem.disp
            if nm == "jmp" and o and o[0].type == X86_OP_REG:
                break
        if None in (acc, limit, defdest, byteoff, dwoff):
            return None
        ids = []
        for v in range(limit + 1):
            fb = fo(ib + byteoff + v)
            if fb is None:
                return None
            ci = raw[fb]
            fd = fo(ib + dwoff + ci * 4)
            if fd is None:
                return None
            rel = struct.unpack_from("<i", raw, fd)[0]
            tgt = (ib + rel) & 0xFFFFFFFFFFFF
            if tgt != defdest:
                ids.append(v + acc)
        return sorted(ids) if ids else None

    decoded, undecoded, by_table = {}, [], 0
    for h in sorted(handlers):
        r = decode(h)
        if r is None or "TABLE" in r:
            r2 = decode_table(h)
            if r2 is not None:
                decoded[h] = r2
                by_table += 1
                continue
        if r is None:
            undecoded.append(h)
        else:
            decoded[h] = r

    print("HANDLERS   %d registered, %d decoded (%d by jump table), %d not"
          % (len(handlers), len(decoded), by_table, len(undecoded)))

    print()
    print("CONTROL    the two dispatchers read by hand and corrected the same day")
    ok = True
    for h, want in sorted(CONTROL.items()):
        got = set(x for x in decoded.get(h, []) if isinstance(x, int))
        mark = "AGREES" if got == want else "DISAGREES"
        if got != want:
            ok = False
        print("  %08X  hand {%s}  reader {%s}  %s"
              % (h, ", ".join("0x%X" % x for x in sorted(want)),
                 ", ".join("0x%X" % x for x in sorted(got)), mark))
    if not ok:
        print("  The reader and the hand reading disagree; neither result may be used.")
        return 1

    vocab = collections.Counter()
    for h, ids in decoded.items():
        for x in ids:
            if isinstance(x, int):
                vocab[x] += 1
    print()
    print("VOCABULARY  message ids at least one registered handler dispatches on")
    print("  %-6s %s" % ("id", "handlers"))
    for x in sorted(vocab):
        print("  0x%-4X %d" % (x, vocab[x]))
    print()
    print("  This is a LOWER BOUND: %d handlers could not be decoded (jump tables or chains this"
          % len(undecoded))
    print("  reader loses), and their ids are simply absent. Safe direction for admitting.")
    if a.verbose:
        for h in undecoded:
            print("    undecoded %08X" % h)

    if a.dry_run:
        print("\ndry run, nothing written")
        return 0
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("message_id\thandlers\tdispatchers\n")
        for x in sorted(vocab):
            hs = sorted(h for h, ids in decoded.items() if x in ids)
            fh.write("0x%X\t%d\t%s\n" % (x, vocab[x], " ".join("%08X" % h for h in hs)))
    print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
