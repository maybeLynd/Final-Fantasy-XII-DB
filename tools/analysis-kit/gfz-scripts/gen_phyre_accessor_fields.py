#!/usr/bin/env python3
"""Recover Phyre field offsets from SCRIPT-ACCESSOR registrations, not from member metadata.

WHY THIS EXISTS. The field schema in `phyre-field-schema.tsv` comes from data-member registration
and covers 246 classes. A class that registers no data member reports nothing there, and the store
has been reading that as no evidence - `PApplication` carried 4,400 bytes in a single unobserved
row on exactly that reasoning. It registers ELEVEN SCRIPT-CALLABLE ACCESSORS instead, and nine of
their adapters are a single instruction reading `this` at a fixed offset.

AN ADAPTER IS BETTER EVIDENCE THAN A MEMBER RECORD, not worse. The instruction carries the offset,
the width and the machine type together, and it distinguishes things a member list cannot:
  * `movsd` / `movss` say the field is a double / a float rather than an 8- or 4-byte blob;
  * `lea` rather than `mov` says the member is EMBEDDED and not reached through a pointer;
  * a mask or a `btr` after the load says the stored word is PACKED and the field is not the
    whole dword;
  * an index scale says the element size of an array the accessor walks.

WHAT THIS DOES. For every body that calls the binder 00632FB0 it recovers, per call, the owner
descriptor (rdx), the accessor name (r8, a C string) and the adapter address (the `lea rax` that
follows), then decodes the adapter's first memory access off rcx.

WHAT IT DELIBERATELY DOES NOT DO. It does not write to the type store, and it does not resolve an
adapter it cannot read in one step - a multi-instruction adapter is reported with its
disassembly and left for a human, because a getter that calls a helper or walks a chain is not a
field. Rows marked `AMBIGUOUS` are candidates, never findings.

Usage:  python gen_phyre_accessor_fields.py [--all]
        --all also prints the adapters that did not reduce to a single access.
"""
import collections
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kit_paths as KP, disasm_fn as DF
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import capstone.x86 as X

BINDER = 0x00632FB0
CHAIN = os.path.join(KP.STORE if hasattr(KP, "STORE") else
                     r"C:/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA",
                     "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                     "members", "phyre-class-parent-chain.tsv")

img = DF.Image(KP.EXE)
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True


def cstr(a, n=96):
    b = img.read(a, n)
    if not b:
        return None
    z = b.find(b"\x00")
    s = b[:z if z >= 0 else n]
    try:
        t = s.decode("ascii")
    except Exception:
        return None
    return t if t and all(32 <= ord(c) < 127 for c in t) else None


def load_classes():
    """descriptor address -> (class name, declared size)."""
    out = {}
    if not os.path.exists(CHAIN):
        return out
    for line in io.open(CHAIN, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 3:
            continue
        try:
            out[int(f[1], 16)] = (f[0], f[2])
        except ValueError:
            continue
    return out


def decode_adapter(addr):
    """Reduce an adapter to one field access, or say why it will not reduce."""
    b = img.read(addr, 0x28)
    if not b:
        return None, "unreadable"
    ins = list(md.disasm(b, addr))
    if not ins:
        return None, "undecodable"
    first = ins[0]
    # the adapter must open with an access off rcx (the `this` pointer) at a fixed displacement
    acc = None
    for op in first.operands:
        if op.type == X.X86_OP_MEM and op.mem.base and first.reg_name(op.mem.base) == "rcx" \
                and not op.mem.index:
            acc = op
            break
    if acc is None:
        return None, "first instruction does not read rcx at a fixed displacement"
    kind = first.mnemonic
    size = acc.size
    ctype = {("movsd", 8): "double", ("movss", 4): "float"}.get((kind, size))
    if ctype is None:
        ctype = {1: "uint8", 2: "uint16", 4: "uint32", 8: "void*"}.get(size, "uint8[%d]" % size)
    tail = [i.mnemonic for i in ins[1:4]]
    note = []
    embedded = (kind == "lea")
    if embedded:
        note.append("EMBEDDED - lea, not a load, so the member is inline")
        ctype = "uint8[?]"
    if "btr" in tail or "and" in tail or "shr" in tail or "sar" in tail:
        note.append("PACKED - the value is masked or shifted before return (%s)" % ",".join(tail))
    if ins[1].mnemonic not in ("ret", "btr", "and", "shr", "sar", "movsxd", "mov", "add", "pop") \
            and len(ins) > 1:
        note.append("adapter continues past the load")
    ok = any(i.mnemonic == "ret" for i in ins[:5])
    if not ok:
        return None, "no ret within five instructions - not a simple accessor"
    return dict(offset=acc.mem.disp, size=size, ctype=ctype, kind=kind,
                embedded=embedded, note="; ".join(note),
                asm=" / ".join("%s %s" % (i.mnemonic, i.op_str) for i in ins[:3])), None


def main():
    show_all = "--all" in sys.argv
    classes = load_classes()
    fns = []
    for r in csv.DictReader(io.open(os.path.join(KP.WORK, "graph", "functions.tsv"),
                                    encoding="utf-8", newline=""), delimiter="\t"):
        fns.append((int(r["entry"], 16), int(r["body_bytes"])))

    found = collections.defaultdict(list)
    unresolved = []
    calls = 0
    for fn, n in fns:
        if n <= 0 or n > 1 << 18:
            continue
        b = img.read(fn, n)
        if not b:
            continue
        ins = list(md.disasm(b, fn))
        pend_name = pend_desc = None
        awaiting = None
        for i in ins:
            if i.mnemonic == "lea" and i.operands and i.operands[0].type == X.X86_OP_REG:
                rn = i.reg_name(i.operands[0].reg)
                m = i.operands[1].mem
                if m.base == X.X86_REG_RIP and not m.index:
                    t = i.address + i.size + m.disp
                    if rn == "r8":
                        pend_name = t
                    elif rn == "rdx" and t in classes:
                        # ONLY a known class descriptor counts. Accepting any rip-relative lea
                        # into rdx attributed a vector class's setX/setY/setZ to whatever
                        # descriptor a nearby unrelated lea had loaded - a stale-register
                        # misattribution of exactly the kind ASTRA found in the AQ18 scanner.
                        # A bind whose owner arrives in a register (006B0B20 does this) is left
                        # unattributed rather than guessed.
                        pend_desc = t
                    elif rn == "rax" and awaiting is not None and 0x00121000 <= t < 0x008C2000:
                        awaiting["adapter"] = t
                        awaiting = None
            if i.mnemonic == "call" and i.operands and i.operands[0].type == X.X86_OP_IMM \
                    and i.operands[0].imm == BINDER:
                calls += 1
                awaiting = dict(reg=fn, site=i.address, name=cstr(pend_name) if pend_name else None,
                                desc=pend_desc, adapter=None)
                found[pend_desc].append(awaiting)
                pend_name = pend_desc = None

    print("binder %08X: %d call(s) across %d owner descriptor(s)\n"
          % (BINDER, calls, len(found)))
    rows = amb = 0
    for desc in sorted(found, key=lambda d: (d is None, d)):
        cls, size = classes.get(desc, ("(descriptor %s not in the parent-chain table)"
                                       % ("%08X" % desc if desc else "?"), "?"))
        entries = found[desc]
        good = []
        for e in entries:
            if not e["adapter"]:
                unresolved.append((cls, e, "no adapter address followed the call"))
                continue
            d, why = decode_adapter(e["adapter"])
            if d is None:
                unresolved.append((cls, e, why))
            else:
                good.append((e, d))
        if not good and not show_all:
            continue
        print("=== %s   descriptor %s   size %s   %d accessor(s), %d reduced ==="
              % (cls, ("%08X" % desc) if desc else "?", size, len(entries), len(good)))
        for e, d in sorted(good, key=lambda g: g[1]["offset"]):
            flag = "  <-- %s" % d["note"] if d["note"] else ""
            print("   +0x%04X  %-4d %-8s %-26s %-18s %s%s"
                  % (d["offset"], d["size"], d["ctype"], e["name"] or "(unnamed)",
                     "adapter %08X" % e["adapter"], d["asm"], flag))
            rows += 1
        print()
    print("REDUCED TO A SINGLE FIELD ACCESS: %d" % rows)
    print("NOT REDUCED (candidates, not findings): %d" % len(unresolved))
    if show_all:
        for cls, e, why in unresolved:
            print("   %-34s %-26s %s" % (cls, e["name"] or "(unnamed)", why))


main()
