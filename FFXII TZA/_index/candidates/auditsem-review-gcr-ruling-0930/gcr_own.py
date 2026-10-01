"""SWE2-AUDIT-SEM GCR check: the guard calls of 0066A7B0 / 0066AB00 and of the two moved bodies 00665870 / 00666380
(every direct call target in each body's .pdata extent), marking _Init_thread_header 008092FC, atexit 00808B90,
_Init_thread_footer 0080929C."""
import struct, re
import img
MARK = {0x008092FC: "Init_thread_header", 0x00808B90: "atexit", 0x0080929C: "Init_thread_footer"}
PD = []
for n, rva, vsz, rp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rp + k)
            if b:
                PD.append((b + img.BASE, e + img.BASE))
for f in (0x0066A7B0, 0x0066AB00, 0x00665870, 0x00666380):
    frs = [(b, e) for b, e in PD if b == f]
    b, e = frs[0]
    xs = list(img.md.disasm(img.rd(b, e - b), b))
    calls = [(x.address, int(x.op_str, 16)) for x in xs if x.mnemonic in ("call", "jmp") and re.fullmatch(r"0x[0-9a-f]+", x.op_str)]
    print("%08X size %d: %s" % (f, e - b, ", ".join("%08X->%08X%s" % (a, t, "(" + MARK[t] + ")" if t in MARK else "") for a, t in calls)))
