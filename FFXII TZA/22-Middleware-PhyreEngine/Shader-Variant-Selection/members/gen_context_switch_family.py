#!/usr/bin/env python3
"""gen_context_switch_family.py - regenerate context-switch-family.tsv from the shipping EXE.

Everything in the TSV is read out of the image, nothing is typed in:

  * the eight static singletons are found by walking the CRT dynamic-initializer table
    (008C31D8..008C5678) for entries that call the by-name registrar 006B8D20;
  * each installer's body gives the object address (its `lea rcx` argument), the derived
    vtable it installs, the key-word count it adds to the global budget 02E522E0, and the
    teardown it hands to the MSVC atexit wrapper 00808B90;
  * the object's own .data image gives the switch NAME (+0x08) and the authored base value
    byte (+0x24);
  * the vtable gives the four virtual slots: deleting destructor, value domain, evaluator,
    preprocessor defines.

Run from anywhere:  python gen_context_switch_family.py [path/to/FFXII_TZA.exe]
Default EXE path is the checkout's work/exe copy; sha256 is printed and must match
73461d0896204b1c259c52f61aef4efbc95a2fffc...721f8 (the charter authority hash).
"""
import hashlib
import os
import struct
import sys

DEFAULT_EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
BASE = 0x120000
XC_LO, XC_HI = 0x8C31D8, 0x8C5678
REGISTRAR = 0x6B8D20
ATEXIT = 0x808B90
BASE_VTABLE = 0x00D80EA8
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "context-switch-family.tsv")


def load(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    secs = []
    for i in range(nsec):
        o = pe + 24 + opt + i * 40
        vs = struct.unpack_from("<I", d, o + 8)[0]
        va = struct.unpack_from("<I", d, o + 12)[0]
        rs = struct.unpack_from("<I", d, o + 16)[0]
        ro = struct.unpack_from("<I", d, o + 20)[0]
        secs.append((BASE + va, vs, ro, rs))
    return d, secs


def off_of(secs, va):
    for sva, vs, ro, rs in secs:
        if sva <= va < sva + vs:
            rel = va - sva
            return ro + rel if rel < rs else None
    return None


def main():
    exe = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EXE
    d, secs = load(exe)
    print("sha256", hashlib.sha256(d).hexdigest())

    def u8(va):
        return d[off_of(secs, va)]

    def u32(va):
        return struct.unpack_from("<I", d, off_of(secs, va))[0]

    def u64(va):
        return struct.unpack_from("<Q", d, off_of(secs, va))[0]

    def cstr(va):
        o = off_of(secs, va)
        e = d.find(b"\x00", o, o + 128)
        return d[o:e].decode("ascii")

    # --- installers: CRT dynamic-initializer entries whose body calls the registrar ---
    installers = []
    for slot in range(XC_LO, XC_HI, 8):
        fn = u64(slot)
        if not (0x121000 <= fn < 0x8C2000):
            continue
        o = off_of(secs, fn)
        body = d[o:o + 0x60]
        calls = set()
        for i in range(len(body) - 5):
            if body[i] in (0xE8, 0xE9):
                rel = struct.unpack_from("<i", body, i + 1)[0]
                tgt = fn + i + 5 + rel
                calls.add(tgt)
                # every initializer in this band ends `jmp atexit`; stop there or a fixed window
                # runs into the NEXT initializer and credits this one with its calls (00167010,
                # the object freelist, was a false positive of exactly that shape)
                if body[i] == 0xE9 and tgt == ATEXIT:
                    break
        if REGISTRAR in calls:
            installers.append((slot, fn))

    rows = []
    for slot, fn in installers:
        o = off_of(secs, fn)
        body = d[o:o + 0x60]
        obj = vtable = teardown = None
        words = 1
        leas = []
        byte_writes = []
        for i in range(len(body) - 7):
            # jmp rel32 to the atexit wrapper: the installer's last instruction, and the bound
            # of this scan - a fixed window would run into the next installer's body
            if body[i] == 0xE9:
                rel = struct.unpack_from("<i", body, i + 1)[0]
                if fn + i + 5 + rel == ATEXIT:
                    teardown = leas[-1][1] if leas else None
                    break
            # 48 8D 0D / 48 8D 05 = lea rcx/rax, [rip+disp32]
            if body[i] == 0x48 and body[i + 1] == 0x8D and body[i + 2] in (0x0D, 0x05):
                disp = struct.unpack_from("<i", body, i + 3)[0]
                leas.append((body[i + 2], fn + i + 7 + disp))
            # the word count is the immediate of `add dword [02E522E0], imm8` (`inc` means 1)
            if body[i] == 0x83 and body[i + 1] == 0x05:
                disp = struct.unpack_from("<i", body, i + 2)[0]
                if fn + i + 7 + disp == 0x2E522E0:
                    words = body[i + 6]
            # `mov byte [rip+d32], imm8` - an installer that overrides the authored +0x24 value
            if body[i] == 0xC6 and body[i + 1] == 0x05:
                disp = struct.unpack_from("<i", body, i + 2)[0]
                byte_writes.append((fn + i + 7 + disp, body[i + 6]))
        for kind, tgt in leas:
            if kind == 0x0D and obj is None and tgt >= 0x1F00000:
                obj = tgt                      # first lea rcx = the object (registrar argument)
            elif kind == 0x05:
                vtable = tgt                   # lea rax = the derived vtable installed at +0x00
        rows.append((obj, fn, slot, vtable, teardown, words, byte_writes))

    rows.sort()
    hdr = ("object\tname\tkey_words\tauthored_0x24\tafter_init_0x24\tvtable\tinstaller\txc_slot"
           "\tatexit_teardown\tdeleting_dtor\tvalue_domain\tevaluator\tdefines")
    lines = [
        "# The PContextSwitch family - the shader-variant axes of FFXII TZA (FABLE, 2026-09-21).",
        "# Generated by gen_context_switch_family.py from the shipping EXE; do not hand-edit.",
        "# object      the static singleton (0x28 bytes: +0x00 vtable, +0x08 name, +0x10 next,",
        "#             +0x18 heap-owned byte, +0x20 key words, +0x24 base value byte)",
        "# authored_0x24 / after_init_0x24   the byte in the .data image, and the value the",
        "#             installer leaves. They differ for LOW_RES_PARTICLES, the only switch whose",
        "#             installer writes +0x24 (to 0). Only the BASE evaluator reads this byte.",
        "# key_words   u32 words this switch contributes to the context-variant key, and the amount",
        "#             its installer adds to the image-wide budget 02E522E0",
        "# evaluator   vtable slot 2 - writes the value words at the key cursor",
        "# defines     vtable slot 3 - reads them back as -D<NAME>=<value> shader-compiler defines",
        "# value_domain vtable slot 1 - enumerates this switch's legal key values",
        "# The base class row has no object: it is constructed on demand by FindOrCreateDynamic.",
        hdr,
        "\t".join(["(dynamic)", "(from the asset)", "1", "-", "1", "%08X" % BASE_VTABLE, "-", "-", "-",
                   "%08X" % u64(BASE_VTABLE), "%08X" % u64(BASE_VTABLE + 8),
                   "%08X" % u64(BASE_VTABLE + 0x10), "%08X" % u64(BASE_VTABLE + 0x18)]),
    ]
    for obj, fn, slot, vt, td, words, bw in rows:
        after = dict(bw).get(obj + 0x24, u8(obj + 0x24))
        lines.append("\t".join([
            "%08X" % obj, cstr(u64(obj + 8)), str(words), str(u8(obj + 0x24)), str(after),
            "%08X" % vt, "%08X" % fn, "%08X" % slot, "%08X" % td,
            "%08X" % u64(vt), "%08X" % u64(vt + 8), "%08X" % u64(vt + 0x10), "%08X" % u64(vt + 0x18),
        ]))
    total = sum(r[5] for r in rows)
    lines.append("# budget: %d switches, %d key words registered into 02E522E0" % (len(rows), total))
    open(OUT, "w", newline="\n").write("\n".join(lines) + "\n")
    print("wrote", OUT, len(rows), "static switches,", total, "key words")


if __name__ == "__main__":
    main()
