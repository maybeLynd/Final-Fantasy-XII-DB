"""textgap_append.py - append two adjudicated rows to text-gap-citations-250.tsv (OPUS, 2026-10-01;
AUDITSPEC-REQ-OPUS-TEXTGAP-NEW-CITES-1001). Append-only (no existing row touched), idempotent. Each row's evidence is
re-checked in the image first: the indexing instruction, the bound, and the table extent. Prints CHECK / PATCHED /
ALREADY and FAILS n."""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
import check_dispositions as cd  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(HERE, "..", "text-gap-citations-250.tsv")
IB = 0x120000
d, off = fp.load_image()
sizes = cd.load_functions()
md = Cs(CS_ARCH_X86, CS_MODE_64)


def ins(a):
    return next(md.disasm(d[off(a):off(a) + 16], a))


def b8(a):
    return " ".join("%02x" % x for x in d[off(a):off(a) + 8])


fails = 0
# row 1: the interpreter's jump table
j = sum(1 for k in range(200) if 0x0025E4C0 <= struct.unpack_from("<I", d, off(0x00261DF8 + 4 * k))[0] + IB < 0x0025E4C0 + sizes[0x0025E4C0])
c1 = ins(0x0025E5DD)
ok1 = (0x0025E4C0 + sizes[0x0025E4C0] == 0x00261DF6 and d[off(0x00261DF6):off(0x00261DF6) + 2] == b"\x66\x90"
       and c1.mnemonic == "mov" and "+ 0x141df8]" in c1.op_str and j >= 100)
print("CHECK row1: body ends 00261DF6, 66 90 pad, 0025E5DD %s %s, leading dwords resolving into the body %d -> %s"
      % (c1.mnemonic, c1.op_str, j, "ok" if ok1 else "FAIL")); fails += not ok1
# row 2: the container-kind switch's byte index table
c2, c3, c4 = ins(0x0027C40F), ins(0x0027C421), ins(0x0027C42A)
ok2 = (c2.op_str == "eax, 0x16" and "+ 0x15c6b8]" in c3.op_str and "+ 0x15c6a0]" in c4.op_str
       and all(x <= 5 for x in d[off(0x0027C6B8):off(0x0027C6B8) + 23]))
print("CHECK row2: 0027C40F cmp %s, 0027C421 %s, 0027C42A %s, 23 bytes all <= 5 -> %s"
      % (c2.op_str, c3.op_str, c4.op_str, "ok" if ok2 else "FAIL")); fails += not ok2

# rows 3-4: 002805D0's two switch tables, cited by OPUS's own world-tick interior row (de98b80ce)
c5, c6, c7 = ins(0x0028060C), ins(0x0028061A), ins(0x00280623)
offs = [struct.unpack_from("<I", d, off(0x00280650 + 4 * k))[0] + IB for k in range(3)]
ok3 = (0x002805D0 + sizes[0x002805D0] == 0x0028064F and c5.op_str == "eax, 0x11" and "+ 0x16065c]" in c6.op_str
       and "+ 0x160650]" in c7.op_str and offs == [0x00280630, 0x0028063E, 0x00280648]
       and all(x <= 2 for x in d[off(0x0028065C):off(0x0028065C) + 18]))
print("CHECK rows3-4: 0028060C cmp %s, 0028061A %s, 00280623 %s, offsets %s, 18 bytes all <= 2 -> %s"
      % (c5.op_str, c6.op_str, c7.op_str, ["%08X" % x for x in offs], "ok" if ok3 else "FAIL")); fails += not ok3
nxt = min(e for e in sizes if e > 0x0028065C)
ROWS = [
    "\t".join(["00261DF6", "0025E4C0", "WorldActorScriptVM_InterpretBytecode", "00261DF6", "0", "00261F90", "yes", b8(0x00261DF6), "TABLE",
               "the body ends at 00261DF6; a 66 90 pad, then 100 dwords from 00261DF8 to 00261F88 resolve as image-base+rel32 into "
               "0025E4C0's own body - the jump table 0025E5DD indexes (mov ecx, [r8+rax*4+0x141df8], r8 = image base); the page's "
               "'the table starts two bytes past the body end' (OPUS 2026-10-01 on SWE2-AUDIT-SPEC's request)",
               "01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md"]),
    "\t".join(["0027C6B8", "0027C3D0", "BattleMenu_ClassifySelectedEntryAndHandleImmediateCommands", "0027C6B8", "0", "0027C730", "yes",
               b8(0x0027C6B8), "TABLE",
               "0027C3D0's container-kind switch: 0027C40F bounds kind-6 at 0x16, 0027C421 reads the byte index at "
               "[image base + rax + 0x15c6b8] (23 bytes, values 0..5), 0027C42A selects the dword case from the table at 0027C6A0 "
               "(OPUS 2026-10-01 on SWE2-AUDIT-SPEC's request)",
               "12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md"]),
    "\t".join(["00280650", "002805D0", "FUN_002805d0", "00280650", "0", "%08X" % nxt, "yes", b8(0x00280650), "TABLE",
               "the body ends at 0028064F (one nop); 3 dwords resolve as image-base+rel32 into 002805D0's own body (00280630, "
               "0028063E, 00280648) - the case table 00280623 reads (mov ecx, [r8+rax*4+0x160650], r8 = image base) "
               "(OPUS 2026-10-01, cited by its world-tick interior row)",
               "00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md"]),
    "\t".join(["0028065C", "002805D0", "FUN_002805d0", "0028065C", "0", "%08X" % nxt, "yes", b8(0x0028065C), "TABLE",
               "002805D0's byte index table: 0028060C bounds the index at 0x11, 0028061A reads [image base + rax + 0x16065c] "
               "(18 bytes, values 0..2) to pick one of the 3 offsets at 00280650 (OPUS 2026-10-01, cited by its world-tick "
               "interior row)",
               "00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md"]),
]
if not fails:
    b = open(P, "rb").read()
    have = {l.split(b"\t", 1)[0] for l in b.split(b"\n") if l and not l.startswith(b"#")}
    add = [r for r in ROWS if r.split("\t", 1)[0].encode() not in have]
    if not add:
        print("ALREADY")
    else:
        if not b.endswith(b"\n"):
            b += b"\n"
        open(P, "wb").write(b + "".join(r + "\n" for r in add).encode("utf-8"))
        print("PATCHED %d row(s)" % len(add))
print("FAILS", fails)
sys.exit(1 if fails else 0)
