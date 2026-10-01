#!/usr/bin/env python3
"""select_explained_callee_adapters.py - frontier NativeAdapter bodies whose ONE external
callee is already explained (A or declared), so the adapter's explanation is
'forwards to <callee> with <argument transform>'.

Request: FABLE-REQ-SWE2-EC7-ADAPTERS-OF-EXPLAINED-CALLEES.

    "member = frontier body whose external call / tail-jump set (security cookie and
     0016D6A0 excluded) is exactly one target, that target is not in the frontier at
     selection time, the body has no loop and no rip store"

A body qualifies when ALL of these hold:

  1. census tag carries `GFZ.V121.CodeDomain.NativeAdapter.*` - the tag is the
     toolchain-generated-form evidence; a frontier body that merely ends in one call
     is not thereby a generated adapter;
  2. body is neither A-measured nor already declared (live frontier at selection time);
  3. the external direct call/jmp set - intra-body branches excluded by the spec's
     "intra-body branches excluded" control, `__security_check_cookie` (00808C40) and
     `_guard_check_icall` (0016D6A0) excluded per the spec - is EXACTLY ONE distinct
     target.  A body containing ANY indirect call/jmp (through a register or memory)
     is refused outright: an indirect edge has no statically certain target, so the
     "one callee" premise cannot be verified;
  4. that target is NOT in the live frontier - it is A-measured or declared, so the
     adapter's behaviour is inherited from an explained callee;
  5. no loop (no backward direct branch) and no rip-relative STORE (the first operand
     is a rip-relative memory operand for any mnemonic other than cmp/test/lea-like
     reads - this includes RMW forms like `or dword [rip+x], imm`).

The members TSV carries one row per member:
    entry <TAB> census-form <TAB> callee <TAB> callee-disposition <TAB> owning-page <TAB> transform

`callee-disposition` is the live letter (A, or the declaring family's B/C);
`owning-page` is the declaring family page for a declared callee, or the
evidence-bearing page(s) whose interior citation makes the callee A.

where transform is one of the spec's five classes, read off the argument-setup prefix
(the instructions before the first external call/jmp; post-call result handling is not
an argument transform):

  - `none`            - no argument register (rcx/rdx/r8/r9) is rewritten before the call;
  - `this-adjusted`   - rcx is rewritten in place: `add/sub rcx, imm`,
                        `lea rcx,[rcx+imm]`, or `mov rcx,[rcx+X]` (deref-adjust);
  - `shifted`         - an argument register is loaded from a different argument
                        register (`mov rcx,rdx`, `mov r8,rdx`, ...) or an argument
                        other than rcx is dereferenced in place;
  - `constant-inserted` - an argument register is given a value the caller never
                        supplied (`mov edx, imm`, `xor edx,edx`, or a load from a
                        rip-relative/absolute address - a static this counts);
  - `flag-normalised` - an argument register is coerced to a 0/1 flag (`setcc`,
                        `movzx` off a setcc byte, `and/or reg,1`).

When several features appear in one prefix the class is chosen by fixed priority -
this-adjusted > shifted > flag-normalised > constant-inserted > none - i.e. the class
that changes the callee-facing signature the most wins; the `form` column keeps the
fine detail for anyone needing the rest.

Controls printed at the end:
  - frontier denominator, the per-form qualifying census, and the leftover reasons;
  - every member re-checked: exactly one external target and callee not in frontier
    (positive control);
  - callee disposition distribution (A vs declared family).
"""
import bisect
import collections
import io
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
for _ in range(10):
    if os.path.isdir(os.path.join(ROOT, "Database", "FFXII TZA")):
        break
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as cd  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP  # noqa: E402

DB = os.path.join(ROOT, "Database", "FFXII TZA")
WORK = os.path.join(ROOT, "Database", "Tools", "work")
EXE = os.path.join(WORK, "exe", "FFXII_TZA.exe")
OUT = os.path.join(HERE, "explained-callee-adapters.tsv")
GRAPH = os.path.join(WORK, "graph", "functions.tsv")

IMAGE = 0x120000
COOKIE = 0x00808C40      # __security_check_cookie
GUARD_ICALL = 0x0016D6A0  # _guard_check_icall - every CFG-guarded indirect call
EXCLUDED = {COOKIE, GUARD_ICALL}
NOREAD_RIP_MEM = {"cmp", "test", "bt", "bts", "btr", "lea", "nop"}
MD = Cs(CS_ARCH_X86, CS_MODE_64)
MD.detail = True


def sections(exe):
    pe = struct.unpack_from("<I", exe, 0x3C)[0]
    n = struct.unpack_from("<H", exe, pe + 6)[0]
    o = pe + 0x18 + struct.unpack_from("<H", exe, pe + 0x14)[0]
    out = {}
    for i in range(n):
        name = exe[o + i * 40:o + i * 40 + 8].rstrip(b"\0").decode()
        vs, va, rs, rp = struct.unpack_from("<IIII", exe, o + i * 40 + 8)
        out[name] = (IMAGE + va, IMAGE + va + vs, rp)
    return out


SETCC = {"sete", "setne", "setz", "setnz", "seta", "setae", "setb", "setbe",
         "setc", "setnc", "setg", "setge", "setl", "setle", "sets", "setns",
         "seto", "setno", "setp", "setnp", "setpe", "setpo"}
NONWRITE = {"test", "cmp", "bt", "bts", "btr", "btc", "nop"}
_ALIAS = {}
for _b, _ls in (("rax", ("al", "ah", "ax", "eax")), ("rbx", ("bl", "bh", "bx", "ebx")),
                ("rcx", ("cl", "ch", "cx", "ecx")), ("rdx", ("dl", "dh", "dx", "edx")),
                ("rsi", ("sil", "si", "esi")), ("rdi", ("dil", "di", "edi")),
                ("rbp", ("bpl", "bp", "ebp")), ("rsp", ("spl", "sp", "esp"))):
    for _n in _ls + (_b,):
        _ALIAS[_n] = _b
for _i in range(8, 16):
    for _s in ("", "d", "w", "b"):
        _ALIAS["r%d%s" % (_i, _s)] = "r%d" % _i


def reg(name):
    return _ALIAS.get(name, name)


def transform(insns):
    """Classify the argument transform from the prefix before the first external
    call/jmp.  Returns one of the spec's five classes; ties break by fixed
    priority (this-adjusted > shifted > flag-normalised > constant-inserted).
    `flagregs` tracks registers whose value is a normalized 0/1 flag so that
    `setne al; mov ecx,eax` is seen as flag-normalising ecx."""
    feats = set()
    flagregs = set()
    for ins in insns:
        if ins.mnemonic in ("call", "jmp"):
            break  # argument setup ends at the callee edge; post-call is result work
        ops = ins.operands
        if not ops or ops[0].type != X86_OP_REG:
            continue
        dn = reg(ins.reg_name(ops[0].reg))
        is_arg = dn in ("rcx", "rdx", "r8", "r9")
        if ins.mnemonic in SETCC:
            flagregs.add(dn)
            if is_arg:
                feats.add("flag-normalised")
            continue
        if ins.mnemonic in NONWRITE or len(ops) < 2:
            continue
        s = ops[1]
        src_flag = (s.type == X86_OP_REG and reg(ins.reg_name(s.reg)) in flagregs)
        if s.type == X86_OP_MEM and s.mem.base and reg(ins.reg_name(s.mem.base)) in flagregs:
            src_flag = True
        if src_flag:
            flagregs.add(dn)
            if is_arg:
                feats.add("flag-normalised")
            continue
        flagregs.discard(dn)
        if not is_arg:
            continue
        is_rcx = dn == "rcx"
        if s.type == X86_OP_IMM:
            if ins.mnemonic in ("and", "or") and s.imm == 1:
                feats.add("flag-normalised")  # boolean coercion, not an inserted constant
            elif is_rcx and ins.mnemonic in ("add", "sub"):
                feats.add("this-adjusted")
            else:
                feats.add("constant-inserted")
        elif s.type == X86_OP_REG:
            sn = reg(ins.reg_name(s.reg))
            if sn == dn and ins.mnemonic in ("xor", "sub", "and"):
                feats.add("constant-inserted")  # reg,reg -> zero
            elif sn in ("rcx", "rdx", "r8", "r9"):
                feats.add("shifted")
        elif s.type == X86_OP_MEM:
            if s.mem.base in (X86_REG_RIP, 0):
                feats.add("constant-inserted")  # static/global data inserted
            elif reg(ins.reg_name(s.mem.base)) == dn:
                feats.add("this-adjusted" if is_rcx else "shifted")
            else:
                feats.add("shifted")
    for cls in ("this-adjusted", "shifted", "flag-normalised", "constant-inserted"):
        if cls in feats:
            return cls
    return "none"


def main():
    exe = open(EXE, "rb").read()
    secs = sections(exe)
    def foff(va):
        for name, (lo, hi, rp) in secs.items():
            if lo <= va < hi:
                return rp + (va - lo)
    sizes = cd.load_functions(None)
    a_set, _eo, _ai, _da = cd.measure_a(DB, sizes)
    owner = {}
    for doc, p in cd.parse_families(DB):
        if len(p) >= 5 and p[1] in cd.LETTERS:
            try:
                for m in cd.read_members(doc, p[2]):
                    owner[m] = (p[1], doc)
            except Exception:
                pass
    frontier = set(sizes) - a_set - set(owner)

    # The family is re-derivable: once its row is live, its own members are declared
    # and would drop out of `frontier`, shrinking the family to nothing on the next
    # run.  Current members therefore re-enter the selection pool and re-qualify
    # against the live state (their callees only become MORE explained).  This also
    # makes the family a fixpoint: a frontier adapter whose callee is itself a member
    # of this family sees that callee as declared-B and joins - chains propagate.
    self_prev = set()
    if os.path.exists(OUT):
        for line in io.open(OUT, encoding="utf-8", errors="replace"):
            tok = line.split("#", 1)[0].strip().split("\t")[0].replace("0x", "")
            if re.fullmatch(r"[0-9A-Fa-f]{6,8}", tok):
                self_prev.add(int(tok, 16))
    # a member since measured A leaves the family - A beats a declaration
    pool = frontier | (self_prev - a_set)

    # interior-citation provenance for A-measured callees: the owning page of an
    # A callee is the evidence-bearing page whose citation lands inside its body
    entries = sorted(sizes)
    a_pages = collections.defaultdict(set)
    for p in cd.docs(DB):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        bearing = cd._bearing(t)
        for h in cd.CITE.findall(t):
            v = int(h, 16)
            i = bisect.bisect_right(entries, v) - 1
            if i < 0:
                continue
            e = entries[i]
            if bearing and e < v < e + sizes[e]:
                a_pages[e].add(os.path.relpath(p, DB).replace(os.sep, "/"))

    tags = {}
    for l in io.open(GRAPH, encoding="utf-8", errors="replace"):
        p = l.rstrip("\n").split("\t")
        if len(p) < 9 or p[0] == "entry":
            continue
        try:
            tags[int(p[0], 16)] = p[8]
        except ValueError:
            pass

    members = []
    reasons = collections.Counter()
    per_form = collections.Counter()
    for va in sorted(pool):
        tg = tags.get(va, "")
        if "CodeDomain.NativeAdapter." not in tg:
            continue
        n, off = sizes[va], foff(va)
        if off is None:
            reasons["not-in-.text"] += 1
            continue
        insns = list(MD.disasm(exe[off:off + n], va))
        ext, loop, ripstore, indirect = set(), False, False, False
        for ins in insns:
            tgt_is_imm = ins.op_str.startswith("0x")
            if ins.mnemonic in ("call", "jmp"):
                if tgt_is_imm:
                    t = int(ins.op_str, 16)
                    if va <= t < va + n:
                        if t < ins.address:
                            loop = True
                    elif t not in EXCLUDED:
                        ext.add(t)
                else:
                    indirect = True
            elif ins.mnemonic.startswith("j") and tgt_is_imm:
                if int(ins.op_str, 16) < ins.address:
                    loop = True
            for i, op in enumerate(ins.operands):
                if (i == 0 and op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP
                        and ins.mnemonic not in NOREAD_RIP_MEM):
                    ripstore = True
        if indirect:
            reasons["indirect-branch"] += 1
            continue
        if len(ext) != 1:
            reasons["external-targets-%d" % min(len(ext), 3)] += 1
            continue
        if loop:
            reasons["loop"] += 1
            continue
        if ripstore:
            reasons["rip-store"] += 1
            continue
        callee = next(iter(ext))
        if callee not in sizes:
            reasons["callee-outside-census"] += 1
            continue
        if callee in frontier:
            reasons["callee-frontier"] += 1
            continue
        form = next((x.split("CodeDomain.")[-1] for x in tg.split(";")
                     if "CodeDomain.NativeAdapter." in x), "NativeAdapter.?")
        if callee in a_set:
            disp, page = "A", "|".join(sorted(a_pages.get(callee, {"?"})))
        else:
            letter, ddoc = owner[callee]
            disp = letter
            page = os.path.relpath(ddoc, DB).replace(os.sep, "/")
        members.append((va, form, callee, disp, page, transform(insns)))
        per_form[form] += 1

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# frontier NativeAdapter bodies whose single external callee is already "
                "explained (A-measured or declared), so the adapter inherits the\n")
        f.write("# callee's explanation: 'forwards to <callee> with <transform>'.\n")
        f.write("# FABLE-REQ-SWE2-EC7-ADAPTERS-OF-EXPLAINED-CALLEES\n")
        f.write("address\tform\tcallee\tcallee-disposition\towning-page\ttransform\n")
        for va, form, callee, disp, page, tr in members:
            f.write("%08X\t%s\t%08X\t%s\t%s\t%s\n" % (va, form, callee, disp, page, tr))

    print("frontier %d   +self %d   members %d"
          % (len(frontier), len(self_prev), len(members)))
    print("by form:")
    for k, v in per_form.most_common():
        print("  %4d  %s" % (v, k))
    print("leftovers by reason:")
    for k, v in reasons.most_common():
        print("  %4d  %s" % (v, k))
    disp_dist = collections.Counter(d for _v, _f, _c, d, _p, _t in members)
    print("callee dispositions:", dict(disp_dist))
    tr_dist = collections.Counter(t for _v, _f, _c, _d, _p, t in members)
    print("transforms:", dict(tr_dist.most_common()))
    nopage = [m for m in members if m[3] == "A" and m[4] == "?"]
    print("A callees with no locating page: %d" % len(nopage))

    # positive control: re-verify the two load-bearing clauses on every member
    bad = 0
    for va, _f, callee, _d, _p, _t in members:
        n, off = sizes[va], foff(va)
        ext = set()
        for ins in MD.disasm(exe[off:off + n], va):
            if ins.mnemonic in ("call", "jmp") and ins.op_str.startswith("0x"):
                t = int(ins.op_str, 16)
                if not (va <= t < va + n) and t not in EXCLUDED:
                    ext.add(t)
        if len(ext) != 1 or next(iter(ext)) != callee or callee in frontier:
            bad += 1
            print("  !! %08X re-check failed" % va)
    print("positive control: %d member(s) failed re-check" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
