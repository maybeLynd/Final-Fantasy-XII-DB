"""An access census for Widget, the type the store reuses most and had no census for.

WHY THIS EXISTS. check_census_widths.py reports zero rows disagreeing with their census, and
for Widget that zero meant nothing: WIDGET HAD NO *-accesses.tsv AT ALL, so not one of its
eighteen declared rows had ever been compared to anything. That is the exact failure the
checker's own header calls out - "a green light that means nothing was compared is worse than
a red one". This generator supplies the missing input.

THE SEED, AND WHY EACH MEMBER IS ADMISSIBLE. A census is only as good as its claim that the
base register holds the type, so nothing is admitted on resemblance:

  THE REGISTERED HANDLERS. Every call to 00245000 (construct in place) or 002465F0 (construct
  sized) passes the handler address in R8, and the constructor stores it at [obj]. The engine
  then invokes it as handler(widget, message). A function reached that way RECEIVES A WIDGET IN
  RCX BY CONSTRUCTION - that is what registration means - so its entry state is known without
  any inference. The scan recovers the handler from the `lea r8, [rip+X]` that set up each call
  and admits every distinct target.

  THE CORE FUNCTIONS, admitted one at a time and only with a caller that proves the argument.
  Each entry in CORE carries the site that calls it with a widget in RCX. They are not admitted
  because they look like widget code.

NOTHING ELSE IS ADMITTED. In particular this generator does NOT follow the widget into callees.
A generic helper called with a widget in RCX is also called with other types, and censusing its
body would file those accesses under Widget - the contamination the store's other generated
censuses guard against by allowing backtracking only into the seed set. The cost is coverage,
not correctness: a displacement this census does not carry is reported by the checker as
UNCHECKED, which is an honest gap, while a wrong row would be a false agreement.

THE TRACKING is an offset-0 MAY-taint over the instruction graph of each seed body: RCX holds
the widget at entry, a register-to-register `mov` copies it, any other definition kills it, a
call kills the caller-saved set, and a load THROUGH a tracked pointer kills it - what comes back
from an arbitrary [widget+d] is some other object, and filing its fields under the widget's
displacements is precisely how a census goes wrong. MAY rather than MUST, so a register counts
if any path reaches it holding the widget; that over-counts rather than under-counts.

WITH ONE EXCEPTION, AND THE STORE ITSELF AUTHORISES IT. Widget is SELF-REFERENTIAL: +0x10
`parent`, +0x18 `firstChild` and +0x20 `nextSibling` are all declared `Widget*`. A load through
a tracked pointer at one of those three offsets therefore yields ANOTHER WIDGET, and an access
on it is a Widget access at the same displacement. So those three loads RE-SEED the taint
instead of killing it, and the offsets are read from the declared rows rather than written into
this file - if the declaration changes, so does the census. That exception is not a convenience:
without it the tree walker 002473B0, whose whole body traverses `[rcx+0x18]` and then
`[rbx+0x20]`, contributes nothing, and the `nextSibling` row's own cited instruction is
unreachable - which is exactly how the omission was found, by the control failing on that one
row out of eighteen.

THE CENSUS STOPS AT +0xC0, AND THAT BOUND IS MEASURED RATHER THAN CHOSEN. The 50 construction
sites build widgets of 27 distinct sizes and THE SMALLEST IS EXACTLY 0xC0 - a widget with room
for nothing but the shared part. So every offset below 0xC0 exists in every widget, and no
offset at or above it can be assumed shared: at +0xC0 a 0x650 widget holds an embedded 0x4C0
widget while a 0x110 record holds something else entirely. Without the bound this file would
report 39 accesses at +0xC0 as Widget fields when they belong to 27 different derived types -
a census that is confidently wrong above the line it never drew. The excluded accesses are
counted and reported, not silently dropped, because "there is traffic up there and it is not
this type's" is itself worth recording.

THE CONTROL IS MANDATORY AND THE GENERATOR REFUSES WITHOUT IT. Every declared Widget row must
have at least one cited address that this census reaches WITH A SPAN CONTAINING THAT ROW'S OWN
OFFSET. Those eighteen citations were read by hand, one at a time, over months and by more than
one pass; if an automatic census cannot reproduce them, the seed or the tracking is wrong and
the file must not be written.

Containment rather than equality, deliberately: +0x9A cites 00246711, which is the DWORD at
+0x98 covering both halves, and demanding disp == offset would fail a citation that is correct.
And any of a row's cited addresses may satisfy it, because a row's evidence often names several
instructions and only says that they bear on the field - not that each one sits at it. The
control is printed either way, pass or fail, and an unreachable row is named with whatever the
census does hold for its addresses, rather than tolerated.

A ROW MAY BE EXEMPTED FROM THE CONTROL, BUT NEVER SILENTLY. CONTROL_EXEMPT names each one with
its reason and prints it on every run, and an exemption is not a pass - it is a declared row
this census does not cover, said out loud so the coverage figure stays honest. Adding one is a
decision about the SEED: if a declared row cannot be reached, either its evidence is wrong or
some function belongs in CORE and did not meet the named-caller standard. Both entries today
are the second case, and the standard was kept rather than bent to gain two rows.

    gen_widget_census.py [--out PATH] [--max-disp 0xC0] [--dry-run]
"""
import argparse
import collections
import io
import os
import re
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP, X86_REG_R8, X86_REG_RCX
import reg_tracking as RT  # noqa: E402  (access direction: op_kind)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
FIELDS = os.path.join(ROOT, "Database", "FFXII TZA", "_types", "fields.tsv")
OUT = os.path.join(ROOT, "Database", "FFXII TZA", "16-UI", "widget-accesses.tsv")
PROC_ABI = os.path.join(ROOT, "Database", "FFXII TZA", "16-UI",
                        "widget-proc-abi-functions.tsv")
CTORS = (0x245000, 0x2465F0)
CALLER_SAVED = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}

# Rows the control cannot reach, each with the reason, printed on every run. An exemption is
# NOT a pass: it is a declared row this census does not cover, named so that the coverage
# figure stays honest. Adding one is a decision about the SEED - if a row cannot be reached,
# either its evidence is wrong or a function belongs in CORE and did not meet the standard.
CONTROL_EXEMPT = {
    # EMPTY, and it did not start that way. +0x88 and +0x8A were exempt for one afternoon
    # because 00246C20 failed both admission routes; the proc-ABI route with the handled-id
    # vocabulary admitted it on evidence rather than by loosening the standard, and the
    # exemptions came out the same day they went in. The mechanism stays: an exemption is
    # always visible, always reasoned, and should always be temporary.
}
# Core widget functions. Each is admitted only because a proven site calls it with a widget in
# RCX, and that site is named. Nothing here is admitted on resemblance to widget code.
CORE = {
    0x2465F0: "the sized initialiser: every one of the 50 construction sites reaches it with the "
              "object address in RCX, directly or through the 00245000 wrapper",
    0x245000: "the in-place construction wrapper: RCX is the address to construct at, e.g. "
              "0029849E `lea rcx,[rsi+0xc0] ; mov edx,0x4c0 ; call 00245000`",
    0x245020: "the release entry, called as `lea rcx,[rbx+0xc0] ; call 00245020` at 00298613",
    0x273A20: "the null/validity test, called as `lea rcx,[rbx+0xc0] ; call 00273A20` at 002985FE "
              "and on the storage itself at 002906EE",
    0x244F00: "the destructor reached from the release path",
    0x2473B0: "the recursive child walker: its own first act is `mov rbx, qword [rcx+0x18]`, the "
              "firstChild row's cited instruction, and it recurses on each child",
    0x247930: "the flag setter called as `mov rcx, rsi ; mov edx, 0x64 ; call 00247930` at "
              "00298480 and `mov rcx, rdi ; mov edx, 0x5a ; call 00247930` at 0029846B",
    0x248030: "the half-rate tree walker cited by the halfRatePhase row",
    0x244960: "called as `mov rcx, rsi ; mov rdx, r14 ; call 00244960` at 0029859C, parent in RCX",
    # Added after the census first ran. 00248030 - already a core function - calls it at
    # 00248097 with a register the taint proves holds a widget, and the body confirms it
    # from the inside: it zeroes the widget's own proc pointer with `mov qword [rdi], 0`
    # at 002483CE and walks [rdi+0x18] / [rcx+0x20], the declared child and sibling links.
    0x2482E0: "the destructor/unlink, called at 00248097 by the core function 00248030 "
              "with a proven widget in RCX; it zeroes the widget's own proc at 002483CE",
    # Added with the transition record. THREE registered handlers call it with a register the
    # taint proves holds a widget - 002BF690 at 002BF7BA, 002C0870 at 002C09E9, 002D5C80 at
    # 002D5D2F - and the body confirms it from the inside: it builds a message record on its
    # stack and invokes the widget's own proc at [obj] with it.
    0x2468A0: "starts a widget transition; called with a proven widget in RCX by the handlers "
              "002BF690 (002BF7BA), 002C0870 (002C09E9) and 002D5C80 (002D5D2F), and it "
              "dispatches through the widget's own proc at [obj]",
    # NOT ADMITTED, deliberately: 00246C20, the transition STEPPER. It is the function that
    # defines +0x88 and +0x8A, and its body argues strongly for itself - it holds RCX in RBX,
    # calls `[rcx]` with a static message record, and reads and writes exactly the fields
    # 002468A0 writes. But it has ONE call site, 002449A9 in 00244980, and no seed reaches
    # 00244980 with a widget this analysis can prove. The standard for CORE is a NAMED CALLER
    # that proves the argument, not a body that looks right, and loosening it here to gain two
    # rows of coverage would cost the meaning of every other row. The consequence is stated
    # rather than hidden: +0x88 and +0x8A are declared from 00246C20 and are NOT under the
    # census gate.
}


FORMS = (("xmmword", 16), ("qword ptr", 8), ("dword ptr", 4), ("word ptr", 2), ("byte ptr", 1))


def _width(instruction):
    """The operand width an instruction states, or 8 when it states none (lea/implicit)."""
    for token, w in FORMS:
        if token in instruction:
            return w
    return 8


def load_image():
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
    return raw, secs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-disp", type=lambda x: int(x, 0), default=0xC0,
                    help="exclusive upper bound; the default is the smallest "
                         "widget the image constructs, so it is the largest "
                         "offset every widget provably has")
    a = ap.parse_args()

    raw, secs = load_image()

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
                    funcs.append((int(c[0], 16), int(c[2]), c[1]))
                except ValueError:
                    pass
    flen = {e: n for e, n, _ in funcs}
    fname = {e: nm for e, _, nm in funcs}

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    cache = {}

    def body(entry):
        if entry not in cache:
            n, f = flen.get(entry, 0), fo(entry)
            cache[entry] = [] if (f is None or n <= 0) else list(md.disasm(raw[f:f + n], entry))
        return cache[entry]

    def norm(r):
        nm = md.reg_name(r)
        m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi",
             "ebp": "rbp", "esp": "rsp", "ax": "rax", "bx": "rbx", "cx": "rcx", "dx": "rdx",
             "si": "rsi", "di": "rdi", "al": "rax", "bl": "rbx", "cl": "rcx", "dl": "rdx"}
        if nm in m:
            return m[nm]
        if nm and nm.startswith("r") and nm[-1] in "dwb" and nm[1:-1].isdigit():
            return "r" + nm[1:-1]
        return nm

    # The self-referential offsets, read from the declared rows rather than hard-coded.
    self_ptr = set()
    with io.open(FIELDS, encoding="utf-8") as fh:
        next(fh)
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) >= 5 and c[0] == "Widget" and c[4].strip() == "Widget*":
                self_ptr.add(int(c[1], 16))
    print("SELF-REFERENTIAL OFFSETS declared Widget*: %s"
          % ", ".join("+0x%X" % d for d in sorted(self_ptr)))

    handlers = set()
    for entry, _, _ in funcs:
        r8 = None
        for i in body(entry):
            ops = i.operands
            if (i.mnemonic == "lea" and len(ops) == 2 and ops[0].type == X86_OP_REG
                    and ops[0].reg == X86_REG_R8):
                t = None
                if ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP:
                    t = i.address + i.size + ops[1].mem.disp
                r8 = t if (t and tlo <= t < thi) else None
            elif (i.mnemonic in ("call", "jmp") and len(ops) == 1
                    and ops[0].type == X86_OP_IMM and ops[0].imm in CTORS and r8):
                handlers.add(r8)

    # A THIRD ADMISSION ROUTE, and it is data rather than a list kept here. Widget's +0x000 is
    # its proc, and the engine sends a message with `mov rax,[obj] ; lea rdx,[record] ; mov
    # rcx,obj ; call rax`, where the record is static data. scan_widget_proc_abi.py closes over
    # that: a record counts only once a function this census ALREADY trusts sends it that way,
    # and only then may other senders of the same record be admitted. It writes its result to
    # widget-proc-abi-functions.tsv, which is READ here rather than transcribed - if the closure
    # changes so does the seed, and the file carries which record vouched for each function.
    proc_abi = []
    if os.path.exists(PROC_ABI):
        with io.open(PROC_ABI, encoding="utf-8") as fh:
            next(fh)
            for ln in fh:
                c = ln.rstrip("\n").split("\t")
                if c and c[0]:
                    proc_abi.append(int(c[0], 16))
    extra = sorted({p for p in proc_abi if p not in handlers and p not in CORE})
    seeds = ([(h, "handler") for h in sorted(handlers)]
             + [(c, "core") for c in sorted(CORE) if c not in handlers]
             + [(p, "proc-abi") for p in extra])
    rows = []
    for entry, role in seeds:
        ins = body(entry)
        if not ins:
            continue
        idx = {i.address: k for k, i in enumerate(ins)}
        succ = collections.defaultdict(set)
        for k, i in enumerate(ins):
            m = i.mnemonic
            tgt = i.operands[0].imm if (i.operands and i.operands[0].type == X86_OP_IMM) else None
            if m == "jmp":
                if tgt in idx:
                    succ[k].add(idx[tgt])
            elif m.startswith("j"):
                if tgt in idx:
                    succ[k].add(idx[tgt])
                if k + 1 < len(ins):
                    succ[k].add(k + 1)
            elif m != "ret" and k + 1 < len(ins):
                succ[k].add(k + 1)

        state = [None] * len(ins)
        state[0] = frozenset(["rcx"])
        work, seen = [0], set()
        while work:
            k = work.pop()
            cur = state[k]
            if cur is None:
                continue
            i = ins[k]
            if not i.mnemonic.startswith("nop"):
                for n_, op in enumerate(i.operands):
                    if (op.type == X86_OP_MEM and op.mem.index == 0
                            and op.mem.base and op.mem.base != X86_REG_RIP
                            and norm(op.mem.base) in cur):
                        sig = (i.address, op.mem.disp, op.size)
                        if sig in seen:
                            continue
                        seen.add(sig)
                        kind = RT.op_kind(i, op, n_)
                        if kind == "addr":
                            kind = "a"
                        rows.append((entry, fname.get(entry, "FUN_%08x" % entry), i.address,
                                     op.mem.disp, kind,
                                     "%s %s" % (i.mnemonic, i.op_str),
                                     "widget rcx " + role, ""))
            nxt = set(cur)
            m, ops = i.mnemonic, i.operands
            if m == "call":
                nxt -= CALLER_SAVED
            elif m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG:
                d = norm(ops[0].reg)
                s = ops[1]
                if s.type == X86_OP_REG and norm(s.reg) in nxt:
                    nxt.add(d)
                elif (s.type == X86_OP_MEM and s.size == 8 and s.mem.index == 0
                        and s.mem.base and s.mem.base != X86_REG_RIP
                        and norm(s.mem.base) in nxt and s.mem.disp in self_ptr):
                    nxt.add(d)          # a declared Widget* yields another Widget
                else:
                    nxt.discard(d)
            elif ops and ops[0].type == X86_OP_REG and m not in ("cmp", "test", "push"):
                nxt.discard(norm(ops[0].reg))
            nxt = frozenset(nxt)
            for s in succ[k]:
                if state[s] is None:
                    state[s] = nxt
                    work.append(s)
                elif not nxt <= state[s]:
                    state[s] = state[s] | nxt
                    work.append(s)

    kept = [r for r in rows if r[3] < a.max_disp]
    dropped = len(rows) - len(kept)
    over = sorted({r[3] for r in rows if r[3] >= a.max_disp})
    print("SEEDS  %d registered handlers + %d core + %d proc-ABI"
          % (len(handlers), len([c for c in CORE if c not in handlers]), len(extra)))
    print("ROWS   %d accesses through a register proven to hold the widget" % len(rows))
    print("BOUND  keeping %d below +0x%X; EXCLUDING %d at %d offsets at or above it "
          "- those belong to whichever sized widget the handler serves, not to the "
          "shared part" % (len(kept), a.max_disp, dropped, len(over)))
    rows = kept
    spans = collections.defaultdict(list)
    for r in rows:
        spans[r[2]].append((r[3], _width(r[5])))

    # ---- the control -----------------------------------------------------------------------
    # For each declared Widget row: at least one address the row cites must appear in the
    # census with a span that CONTAINS the row's own offset. Containment rather than equality,
    # because a legitimate citation can be a wider store - Widget +0x9A cites 00246711, which
    # is the dword at +0x98 covering both halves, and demanding disp == offset would fail a
    # citation that is correct. An address a row merely mentions in passing is not required to
    # match; what is required is that the row's evidence be REACHABLE by this census.
    todo = []
    with io.open(FIELDS, encoding="utf-8") as fh:
        next(fh)
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) >= 9 and c[0] == "Widget":
                off = int(c[1], 16)
                addrs = [int(m.group(1), 16)
                         for m in re.finditer(r"\b(00[0-9A-F]{6})\b", c[8])]
                todo.append((off, c[3], addrs))
    ok, miss, exempt = [], [], []
    for off, name, addrs in todo:
        if off in CONTROL_EXEMPT:
            exempt.append((off, name))
            continue
        hit = None
        for s in addrs:
            for d, w in spans.get(s, ()):
                if d <= off < d + w:
                    hit = (s, d, w)
                    break
            if hit:
                break
        (ok if hit else miss).append((off, name, addrs, hit))
    print()
    print("CONTROL  every declared Widget row must have a cited address this census reaches,")
    print("         with a span containing the row's own offset")
    print("  declared rows : %d" % len(todo))
    print("  reproduced    : %d" % len(ok))
    print("  EXEMPT, with a stated reason: %d" % len(exempt))
    for off, name in exempt:
        print("    +0x%03X %-14s %s" % (off, name, CONTROL_EXEMPT[off]))
    print("  NOT reproduced: %d" % len(miss))
    for off, name, addrs, _ in miss:
        seen_here = [(s, spans[s]) for s in addrs if s in spans]
        print("    +0x%03X %-14s cites %s" % (off, name, ", ".join("%08X" % s for s in addrs[:6])))
        if seen_here:
            for s, sp in seen_here[:4]:
                print("            %08X in census at %s"
                      % (s, ", ".join("0x%X[%d]" % (d, w) for d, w in sp)))
        else:
            print("            none of those addresses is in the census")
    if miss:
        print()
        print("REFUSING to write the census: the control is not satisfied.")
        return 1
    if a.dry_run:
        print("\ndry run, nothing written")
        return 0

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
        for e, nm, site, disp, kind, instr, route, note in sorted(rows, key=lambda r: (r[0], r[2])):
            fh.write("%08X\t%s\t%08X\t0x%X\t%s\t%s\t%s\t%s\n"
                     % (e, nm, site, disp, kind, instr, route, note))
    print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
