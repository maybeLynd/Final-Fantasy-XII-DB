"""sd122_record.py - SD-122 (FABLE, 2026-09-30): the subresource-variant binding record (128 x 80 B pool at [02B47798]).
Checks (FAILS n):
 R1 the allocator 003CCC20 copies a 48-byte payload (three movups pairs, +0x00..+0x2F), not 32.
 R2 it zeroes +0x34 (dword, 003CCC5C) and +0x38 / +0x40 (003CCC65 / 003CCC69), then writes +0x30 = (gen << 8) | index.
 R3 it links the record into its handle-table entry's list (entry = [02B47790-ish] + (handle & 0xFF) * 64, validated
    by +4 == handle at 003CCE59): head +0x28 / tail +0x30, the record's +0x38 = next and +0x40 = prev, ordered by the
    payload's byte +2 (003CCEA0 cmp byte [rax+2], cl) - writes of +0x38 at 003CCEB2 / 003CCEE1 / 003CCEFC and of
    +0x40 at 003CCEBA / 003CCED9 / 003CCF00.
 R4 the updater 003CCF20 counts the start delay +0x0A down by the per-call step r14w (003CCFD9); on running out the
    overshoot seeds +0x34 (003CCFEA); otherwise +0x34 += r14w (003CCFF5); +0x34 is bounded by the payload's +0x08
    (003CCFFA-003CD007: if +0x08 != 0 and +0x08 < +0x34, take the expiry path at 003CD009).
 R5 the allocator adds a spread to +0x0A when the payload word +0x0C is non-zero (003CCC97 test, 003CCE2E add).
Control: the pool's only rip users are 003CCC20, 003CCF20, 003CD650 and 003CD6E0 (the census the page names)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "takebacks"))
import tk
A = {x.address: x for x in tk.fdis(0x003CCC20)}
U = {x.address: x for x in tk.fdis(0x003CCF20)}
fails = 0
def check(n, ok):
    global fails
    print(n, "PASS" if ok else "FAIL"); fails += 0 if ok else 1
dec, raw = tk.rip_refs(0x02B47798, 0x02B477A0)
users = sorted({tk.owner(x.address)[0] for x, k, t in dec})
check("CONTROL pool users = 003CCC20, 003CCF20, 003CD650, 003CD6E0", users == [0x003CCC20, 0x003CCF20, 0x003CD650, 0x003CD6E0])
mv = [a for a, x in A.items() if x.mnemonic == "movups" and x.op_str.startswith("xmmword ptr [rbx")]
check("R1 payload copied as 3 x 16 bytes (+0x00, +0x10, +0x20)", sorted(A[a].op_str for a in mv) ==
      ["xmmword ptr [rbx + 0x10], xmm1", "xmmword ptr [rbx + 0x20], xmm0", "xmmword ptr [rbx], xmm0"])
check("R2 zeroes +0x34/+0x38/+0x40 then writes the handle at +0x30",
      A[0x003CCC5C].op_str == "dword ptr [rbx + 0x34], r8d" and A[0x003CCC65].op_str == "qword ptr [rbx + 0x40], r8"
      and A[0x003CCC69].op_str == "qword ptr [rbx + 0x38], r8" and A[0x003CCC7B].op_str == "dword ptr [rbx + 0x30], eax")
w38 = [a for a, x in A.items() if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [") and "+ 0x38], r" in x.op_str]
w40 = [a for a, x in A.items() if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [") and "+ 0x40], r" in x.op_str]
check("R3 list links: entry validated (003CCE59), ordered by byte +2 (003CCEA0), +0x38/+0x40 written in the insert arms",
      A[0x003CCE59].op_str == "dword ptr [rdi + 4], ecx" and A[0x003CCEA0].op_str == "byte ptr [rax + 2], cl"
      and {0x003CCEB2, 0x003CCEE1, 0x003CCEFC} <= set(w38) and {0x003CCEBA, 0x003CCED9, 0x003CCF00} <= set(w40))
check("R4 delay +0x0A counted by r14w; +0x34 seeded / advanced; bounded by +0x08",
      U[0x003CCFD9].op_str == "ax, r14w" and U[0x003CCFEA].op_str == "word ptr [rbx + 0x34], ax"
      and U[0x003CCFF5].op_str == "word ptr [rbx + 0x34], r14w" and U[0x003CCFFA].op_str == "eax, word ptr [rbx + 8]"
      and U[0x003CD003].op_str == "ax, word ptr [rbx + 0x34]" and U[0x003CD007].mnemonic == "jae")
check("R5 +0x0C non-zero adds a spread to +0x0A", A[0x003CCC97].op_str == "word ptr [r9 + 0xc], r8w" and A[0x003CCE2E].op_str == "word ptr [rbx + 0xa], ax")
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
