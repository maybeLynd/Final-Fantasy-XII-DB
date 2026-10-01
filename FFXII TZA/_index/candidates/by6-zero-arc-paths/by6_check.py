"""BY-6 control (OPUS, 2026-09-27): what 003CC890 returns for the 47 shipped CAM7 array-C paths with no arc table.

Run with FF12_EBP_DIR pointing at the 1,115 `us` .ebp containers (as the cam7-path-commands census requires).
Z1  the census extension (census_zero.py = the published census plus a dump at its m == 0 branch) reproduces its own
    control (423 files, 3,942 records, 15,350 curves, 1,682 paths) and finds 47 zero-arc paths, all followed in the
    resident section by more bytes (the next record).
Z2  static: 003CC890 reads arc[0] at record + 0x20 + 0x38n (003CC8A0), clamps to 0.0 / 1.0, and for m = 0 skips the
    bisect (r10d = m - 1 = -1 <= 1) and interpolates between arc[0] and arc[1] (003CC905-003CC962); the loader's
    array-C build keeps records in place (0025637C movzx eax, word [rbx] / add rbx, rax).
Z3  for every zero-arc path arc[-1].key (the last segment's +0x30 word) is 1.0 and arc[0].key (the next record's
    header read as a float) is a positive value below 1e-30, so q <= ~0 gives 0.0 and q > 1.0 gives 1.0.
Z4  for 0 < q <= 1 the output is the float32 line through arc[0] and arc[1] - bytes of the NEXT record - and its value
    at q = 1 over the 47 is recorded (it is not 1.0 for any of them).
"""
import json, os, runpy, struct, statistics, hashlib, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
out = runpy.run_path(str(HERE / "census_zero.py"), run_name="__main__")
Z = json.load(open("zero_arc.json"))
assert len(Z) == 47 and all(x["past_in_section"] for x in Z)
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = HERE.parents[3] / "Tools" / "work" / "exe" / "FFXII_TZA.exe"
raw = EXE.read_bytes(); assert hashlib.sha256(raw).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
pe = pefile.PE(data=raw, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
def ins(a, n): o = pe.get_offset_from_rva(a - IB); return {i.address: (i.mnemonic, i.op_str) for i in Cs(CS_ARCH_X86, CS_MODE_64).disasm(raw[o:o + n], a)}
S = ins(0x3CC890, 218)
assert S[0x3CC8A0] == ("movss", "xmm0, dword ptr [r9 + 0x20]") and S[0x3CC8AF] == ("lea", "r10d, [r11 - 1]")
assert S[0x3CC8CC] == ("cmp", "r10d, 1") and S[0x3CC8D0][0] == "jle"
assert S[0x3CC921] == ("movss", "xmm3, dword ptr [r9 + rcx*8 + 0x24]") and S[0x3CC962] == ("addss", "xmm1, xmm0")
L = ins(0x256370, 0x20)
assert L[0x256375] == ("mov", "qword ptr [rax + rdi*8], rbx") and L[0x25637C] == ("movzx", "eax, word ptr [rbx]") and L[0x25637F] == ("add", "rbx, rax")
r = lambda x: struct.unpack("<f", struct.pack("<f", x))[0]
def remap(b, q, lastk):
    q = r(q); A0k, A0v, A1k, A1v = [struct.unpack_from("<f", b, o)[0] for o in (0, 4, 8, 12)]
    if A0k > q: return 0.0
    if q > lastk: return 1.0
    if A0k == A1k or A0v == A1v: return A0v
    return r(r(r(r(q - A0k) / r(A1k - A0k)) * r(A1v - A0v)) + A0v)
at1 = []
for x in Z:
    b = bytes.fromhex(x["past"])
    assert x["last_key"] == 1.0, x
    assert 0 < x["arc0_key"] < 1e-30, x
    assert remap(b, 0.0, 1.0) == 0.0 and remap(b, 1.5, 1.0) == 1.0
    at1.append(remap(b, 1.0, 1.0))
assert all(v != 1.0 for v in at1)
res = {"n": 47, "at_q1_min": min(at1), "at_q1_max": max(at1), "at_q1_median": statistics.median(at1),
       "in_0_1": sum(0 <= v <= 1 for v in at1), "gt_1": sum(v > 1 for v in at1), "lt_0": sum(v < 0 for v in at1)}
print(json.dumps(res)); print("PASS")
