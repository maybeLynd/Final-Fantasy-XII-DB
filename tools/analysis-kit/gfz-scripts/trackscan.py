"""One call for an ad-hoc image-wide "who accesses this base?" scan, with the rules already on.

WHY THIS EXISTS. On 2026-09-20 I catalogued eight ways a register-tracking scan lies
(_index/ABSENCE-CLAIM-GATE.md), hardened three census tools against them - and then, in the same
session, answered a one-off question with a twenty-line ad-hoc tracker that had none of the rules.
It reported a reader that did not exist: the body was sweeping a stride-8 pointer array and its
base register had been reassigned since the seeding load. The near-miss was the tracker's, not the
store's.

The tools carried the rules; the throwaway scan did not, because writing a correct one takes
twenty lines and writing a wrong one takes five. This makes the correct one take one call.

    from trackscan import scan
    # every access through a pointer loaded from [anything + 0xB8]
    for h in scan(seed_load_disp=0xB8, offsets=(0x50, 0x54, 0x58)):
        print(h)

RULES APPLIED, all from the catalogue:
  1 whole extent decoded, so table-dispatch arms are visible
  2 `add base, index` keeps the base
  8 `add index, base` makes the DESTINATION a base
  3 a load from memory kills the register - it is a different object now
  5 a stack load is AMBIGUOUS: flagged, not guessed (`suspect` on the hit)
  6 a call clobbers rax/rcx/rdx/r8-r11
  7 register names are canonicalised, so `xor eax, eax` kills `rax`
  + the deferred kill: a `mov` that reads through the base it overwrites is recorded first

WHAT IT DOES NOT DO: follow a pointer into a callee, or see a base that never passes through a
register this scan seeds on. The shape that actually bit: a base arriving as a CALL RETURN -
`call getter; mov r15, rax` - whose only cell-load site sits inside the getter's body (the
`NavTrailerRecord28` "no code reads" false-negative, ABSENCE-CLAIM-GATE blind spot 13,
2026-09-28). Those are the declared limits of every tool here; a zero from this is
still bounded evidence, not proof of absence.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP, disasm_fn as DF, resolve_switch_arms as R
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import capstone.x86 as X

try:
    from regcanon import canon
except ImportError:
    def canon(n):
        return n

_md = Cs(CS_ARCH_X86, CS_MODE_64); _md.detail = True
_img = DF.Image(KP.EXE)
_ex = R.extents()

VOLATILE = ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11")

Hit = collections.namedtuple(
    "Hit", "host site rw disp size text suspect")


def scan(seed_load_disp=None, seed_rip_target=None, rip_mode="deref",
         offsets=None, hosts=None):
    """Track a base and report accesses through it.

    seed_load_disp   seed on `mov reg, [any + DISP]` - e.g. 0xB8 for a context pointer
    seed_rip_target  seed on a named global at ADDR
    rip_mode         what that global IS, and the two are different objects:
                       "deref" - it HOLDS a pointer; seed on `mov reg, [rip->ADDR]` and
                                 track the POINTEE. Fields found are the pointee's.
                       "addr"  - it IS the object; seed on `lea reg, [rip->ADDR]` and
                                 track the global itself. Fields found are its own.
                     There is no "either": accepting both conflates a global's address with
                     the object it points at, and every field then lands on the wrong type.
                     Blind spot 8 taught the same lesson about `add` - a base and an index
                     look alike until you say which one you meant.
    offsets          only report these displacements (None = all)
    hosts            restrict to these function entries (None = the whole image)
    """
    if seed_load_disp is None and seed_rip_target is None:
        raise ValueError("give seed_load_disp or seed_rip_target")
    if rip_mode not in ("deref", "addr"):
        raise ValueError("rip_mode must be 'deref' or 'addr'")
    want = set(offsets) if offsets else None
    out = []
    items = ([(h, _ex.get(h, 0)) for h in hosts] if hosts else sorted(_ex.items()))
    for va, n in items:
        if not n or n <= 0:
            continue
        try:
            ins = list(R.decode(_img, _md, va, n))
        except BaseException:
            continue
        held, suspect = {}, set()
        for i in ins:
            seeded = False
            # ---- seed -------------------------------------------------
            if i.mnemonic in ("mov", "lea") and len(i.operands) == 2 and \
                    i.operands[0].type == X.X86_OP_REG and i.operands[1].type == X.X86_OP_MEM:
                m = i.operands[1].mem
                dn = canon(i.reg_name(i.operands[0].reg))
                if seed_rip_target is not None and m.base and \
                        canon(i.reg_name(m.base)) == "rip" and \
                        i.address + i.size + m.disp == seed_rip_target and \
                        i.mnemonic == ("mov" if rip_mode == "deref" else "lea"):
                    held[dn] = (0, True); seeded = True
                elif seed_load_disp is not None and i.mnemonic == "mov" and m.base and \
                        canon(i.reg_name(m.base)) != "rip" and m.disp == seed_load_disp:
                    held[dn] = (0, True); seeded = True
            if seeded:
                continue

            if i.mnemonic == "lea" and len(i.operands) == 2 and \
                    i.operands[0].type == X.X86_OP_REG:
                dn = canon(i.reg_name(i.operands[0].reg))
                m = i.operands[1].mem
                if m.base and canon(i.reg_name(m.base)) in held:
                    # BLIND SPOT 10: carry the constant. `lea r, [base+0x8FA0]` then `[r+0xAC0]`
                    # is +0x9A60, and reporting +0xAC0 puts it in another object's coordinates.
                    # An index register means an ELEMENT walk, where a single bias is meaningless,
                    # so the chain stops being pure and the raw displacement is kept and flagged.
                    bb, bp = held[canon(i.reg_name(m.base))]
                    held[dn] = (bb + m.disp, bp and not m.index)
                else:
                    held.pop(dn, None)
            elif i.mnemonic == "add" and len(i.operands) == 2 and \
                    i.operands[0].type == X.X86_OP_REG:
                dn = canon(i.reg_name(i.operands[0].reg))          # rules 2, 8 and 10
                s = i.operands[1]
                if dn in held:
                    held[dn] = (0, False)      # base + scaled index: a new element, bias restarts
                elif s.type == X.X86_OP_REG and canon(i.reg_name(s.reg)) in held:
                    held[dn] = (0, False)      # `add index, base`: the destination is the element

            pending = None
            if i.mnemonic == "mov" and len(i.operands) == 2 and \
                    i.operands[0].type == X.X86_OP_REG:
                dn = canon(i.reg_name(i.operands[0].reg))
                s = i.operands[1]
                if s.type == X.X86_OP_REG and canon(i.reg_name(s.reg)) in held:
                    held[dn] = held[canon(i.reg_name(s.reg))]
                elif s.type == X.X86_OP_MEM and s.mem.base and \
                        canon(i.reg_name(s.mem.base)) in ("rsp", "rbp"):
                    if dn in held:
                        suspect.add(dn)                            # rule 5
                else:
                    pending = dn                                   # deferred kill

            for op in i.operands:
                if op.type == X.X86_OP_MEM and op.mem.base:
                    b = canon(i.reg_name(op.mem.base))
                    if b in held:
                        bb, bp = held[b]
                        d = op.mem.disp + bb if bp else op.mem.disp
                        if want is None or d in want:
                            out.append(Hit(va, i.address,
                                           "W" if (op.access & 2) else "R",
                                           d, op.size,
                                           "%s %s" % (i.mnemonic, i.op_str),
                                           (b in suspect) or not bp))
            if pending is not None:
                held.pop(pending, None)

            if i.mnemonic == "call":                               # rule 6
                for _v in VOLATILE: held.pop(_v, None)
                suspect -= set(VOLATILE)
                continue
            if i.mnemonic not in ("lea", "add", "mov", "cmp", "test"):
                for op in i.operands:
                    if op.type == X.X86_OP_REG and (op.access & 2):
                        held.pop(canon(i.reg_name(op.reg)), None)    # rule 7 via canon
    return out


def self_test():
    """The near-miss this module exists to prevent, as a fixture.

    MovementContext is reached by `mov reg, [actor+0xB8]`. Its +0x58 has exactly ONE access in the
    image - the write at 0026B592 - and a naive tracker also reports 00295161, which belongs to a
    body sweeping a stride-8 pointer array with a reassigned base.
    """
    hits = scan(seed_load_disp=0xB8, offsets=(0x58,))
    sites = {h.site for h in hits}
    ok_has = 0x26B592 in sites
    ok_not = 0x295161 not in sites
    print("%s the known write 0026B592 is reported" % ("ok  " if ok_has else "MISS"))
    print("%s the naive tracker's phantom 00295161 is NOT reported" % ("ok  " if ok_not else "MISS"))
    print("self-test: 2 case(s), %d failure(s)" % ((not ok_has) + (not ok_not)))
    return (not ok_has) + (not ok_not)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    print(__doc__)
