"""sd63_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for SD-63 (2026-09-30). Read-only on the image.
Decodes the 16-byte source table at 00D3EB38 straight from the file bytes (name qword at -8, then two dwords) with
its own section-aware reader, prints what 006372B0 returns (the fifth argument of 005FD700), reads the head of
005FD700 for what it writes into the 24-byte records, and lists the rest of 005FD2A0 after the buffer allocation."""
import sys, struct, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk

def cstr(a):
    o = tk.off(a); e = tk.d.index(b"\0", o); return tk.d[o:e].decode("latin-1")

print("== source table (entry i: name @ 00D3EB30+16i, dwords @ 00D3EB38+16i)")
codes = {}
for i in range(24):
    base = 0x00D3EB30 + 16 * i
    p = tk.u64(base); a, b = struct.unpack("<II", tk.d[tk.off(base + 8):tk.off(base + 8) + 8])
    nm = cstr(p) if p and tk.off(p) is not None and tk.sec_of(p) == ".rdata" else "(not a string: %X)" % (p or 0)
    print("  %2d %-34s %3d %3d" % (i, nm, a, b))
    if i < 23: codes.setdefault(b, []).append(nm)
print("== type code -> names:")
for k in sorted(codes): print("  %3d: %s" % (k, ", ".join(codes[k])))
print("== 006372B0 (fifth argument source)")
for x in tk.dis(0x006372B0, 0x006372B0 + 0x40)[:12]: print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("== 005FD700 size %s; stores through the record pointer (first 400 bytes, memory destinations)" % tk.fsize(0x005FD700))
for x in tk.fdis(0x005FD700):
    if any(tk.is_store(x, k) for k in range(len(x.operands))) and "rsp" not in x.op_str and "rbp" not in x.op_str:
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
