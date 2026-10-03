"""check_s39.py - FABLE, 2026-10-03, on SWE2-AUDIT-SPEC's L2 expansion (S-39, CONTRACT-render-command-list-and-graphics-handshake.md §10.1).

Claim under test (the contract's §10.1 and §2 "return semantics"): a failed malloc in an enqueue appends a null to both
lists and "the failure is absorbed silently" / "Failure is silent everywhere".
Correction: the owner list's flush 0018C8F0 loads each entry (0018C930) and reads [entry+0x10] at 0018C933 with no null
test, so a null still on the owner list when the scene teardown 001E0590 flushes it (001E05B6) faults.

Parts:
 S1-S6  static, from the shipping image (sha256 asserted by rvlib): the enqueue's null path, the getter, the teardown
        call, the flush's two loops, and a null-test detector.
 R1-R2  raw reference index (E8/E9 rel32, 0F 8x rel32, EB/7x rel8, rip-relative, image-base-relative, absolute qwords)
        for the flush and the enqueue.
 U1-U3  unicorn: the shipped flush executed on planted owner lists.
 C1-C2  SENSITIVITY CONTROLS: the old reading ("the flush null-tests") is asserted against the shipping image and must
        come out false; a patched image copy WITH a null test inserted at 0018C930 must make the detector say "tested"
        and the null-entry run return cleanly. If this check could not see the defect, C2 would fail.
Prints PASS/FAIL lines and FAILS N last.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
sys.path.insert(0, HERE)
from rvlib import Img  # noqa: E402
from rawidx import raw_refs  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_REG  # noqa: E402

FAILS = 0


def report(name, ok, detail=""):
    global FAILS
    if not ok:
        FAILS += 1
    print("%s %s  %s" % ("PASS" if ok else "FAIL", name, detail))


def dis(img, va, n):
    return list(img.cs.disasm(img.read(va, n), va))


def at(ins_list, va):
    for i in ins_list:
        if i.address == va:
            return "%s %s" % (i.mnemonic, i.op_str)
    return None


def rip_target(i):
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.base and i.reg_name(op.mem.base) == "rip":
            return i.address + i.size + op.mem.disp
    return None


def null_tested_before_deref(img, load_va, limit=12):
    """Decode from a `mov reg, [..]` entry load; return (tested, deref_va). tested is True when a `test reg,reg` or
    `cmp reg,0` followed by a conditional jump comes before the first memory operand based on reg."""
    ins = dis(img, load_va, 0x40)
    first = ins[0]
    assert first.mnemonic == "mov" and first.operands[0].type == X86_OP_REG
    reg = first.reg_name(first.operands[0].reg)
    tested = False
    for k, i in enumerate(ins[1:limit], 1):
        if i.mnemonic in ("test", "cmp") and len(i.operands) == 2:
            o0, o1 = i.operands
            if o0.type == X86_OP_REG and i.reg_name(o0.reg) == reg:
                if (i.mnemonic == "test" and o1.type == X86_OP_REG and i.reg_name(o1.reg) == reg) or \
                   (i.mnemonic == "cmp" and o1.type == 2 and o1.imm == 0):
                    if ins[k + 1].mnemonic.startswith("j") and ins[k + 1].mnemonic != "jmp":
                        tested = True
        for op in i.operands:
            if op.type == X86_OP_MEM and op.mem.base and i.reg_name(op.mem.base) == reg:
                return tested, i.address
    return tested, None


img = Img.load()

# ---- S1: 00182970 hands the owner list [01F7F5E8] to the enqueue 0018C610
f = dis(img, 0x182970, 0x2C)
getter = dis(img, 0x18CA40, 8)
s1 = (at(f, 0x182982) == "call 0x18ca40" and at(f, 0x182987) == "mov rcx, rax" and at(f, 0x182991) == "jmp 0x18c610"
      and getter[0].mnemonic == "mov" and rip_target(getter[0]) == 0x01F7F5E8 and getter[1].mnemonic == "ret")
report("S1_00182970_passes_the_owner_list_to_0018C610", s1,
       "00182982 call 0018CA40 (mov rax,[01F7F5E8]; ret), 00182987 mov rcx,rax, 00182991 jmp 0018C610")

# ---- S2: the enqueue appends rbx = 0 when malloc fails, to the owner list and then to the ordered list
e = dis(img, 0x18C610, 0x94)
s2 = (at(e, 0x18C632) == "call 0x85e730" and at(e, 0x18C641) == "test rax, rax" and at(e, 0x18C644) == "je 0x18c655"
      and at(e, 0x18C655) == "xor ebx, ebx" and at(e, 0x18C657) == "mov qword ptr [rsp + 0x40], rbx"
      and at(e, 0x18C673) == "mov qword ptr [rdx], rbx" and at(e, 0x18C678) == "lea r8, [rsp + 0x40]"
      and at(e, 0x18C680) == "call 0x1ab570" and at(e, 0x18C692) == "mov rdx, rbx" and at(e, 0x18C69F) == "jmp 0x18aff0")
report("S2_failed_malloc_appends_null_to_owner_then_ordered", s2,
       "0018C644 je -> 0018C655 xor ebx,ebx; owner push 0018C673 mov [rdx],rbx (grow arm 0018C680 from [rsp+0x40]=rbx, 0018C657); "
       "ordered via 0018C692 rdx=rbx, 0018C69F jmp 0018AFF0")

# ---- S3: the scene teardown flushes the same owner list
t = dis(img, 0x1E0590, 0x4F)
s3 = (at(t, 0x1E05A9) == "call 0x18b040" and at(t, 0x1E05AE) == "call 0x18ca40" and at(t, 0x1E05B3) == "mov rcx, rax"
      and at(t, 0x1E05B6) == "call 0x18c8f0")
report("S3_teardown_001E0590_flushes_0018CA40s_list", s3, "001E05A9 clear, 001E05AE call 0018CA40, 001E05B6 call 0018C8F0")

# ---- S4: the flush's first loop dereferences the entry with no null test
fl = dis(img, 0x18C8F0, 0xE9)
tested1, deref1 = null_tested_before_deref(img, 0x18C930)
s4 = (at(fl, 0x18C930) == "mov rdi, qword ptr [rbx]" and at(fl, 0x18C933) == "cmp byte ptr [rdi + 0x10], bpl"
      and not tested1 and deref1 == 0x18C933)
report("S4_flush_loop1_reads_entry_plus10_untested", s4,
       "0018C930 mov rdi,[rbx]; 0018C933 cmp byte [rdi+0x10],bpl; null-tested=%s, first deref %s" % (tested1, deref1 and "%X" % deref1))

# ---- S5: the only branches into the loop-1 body are the loop's own back edge (no path tests null and jumps past)
into = []
for i in fl:
    if i.mnemonic.startswith("j") and i.operands and i.operands[0].type == 2:
        tgt = i.operands[0].imm
        if 0x18C930 <= tgt <= 0x18C933:
            into.append((i.address, tgt))
s5 = into == [(0x18C956, 0x18C930)]
report("S5_loop1_entered_only_by_fallthrough_and_its_back_edge", s5, "branches into 0018C930..0018C933: %s" %
       ["%X->%X" % x for x in into])

# ---- S6: the null tests that DO exist: the flush's destroy loop and the owner destroy 0018B810
tested2, d2 = null_tested_before_deref(img, 0x18C977)
tested3, d3 = null_tested_before_deref(img, 0x18B850)
s6 = tested2 and at(fl, 0x18C97A) == "test rcx, rcx" and tested3
report("S6_destroy_loops_do_test_null", s6, "0018C97A test rcx,rcx (flush loop 2); 0018B853 (0018B810): tested=%s/%s" % (tested2, tested3))

# ---- R1/R2: raw reference index
r_flush = raw_refs(img, 0x18C8F0)
report("R1_flush_0018C8F0_has_one_reference_call_001E05B6", [(k, v) for k, v, _ in r_flush] == [("call", 0x1E05B6)],
       "raw refs: %s" % ["%s %X" % (k, v) for k, v, _ in r_flush])
r_enq = raw_refs(img, 0x18C610)
report("R2_enqueue_0018C610_has_one_reference_jmp_00182991", [(k, v) for k, v, _ in r_enq] == [("jmp", 0x182991)],
       "raw refs: %s" % ["%s %X" % (k, v) for k, v, _ in r_enq])

# ---- U: unicorn execution of the shipped flush on a planted owner list
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_MEM_UNMAPPED  # noqa: E402
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RIP  # noqa: E402
import unicorn  # noqa: E402

STUB, STACK, HEAP, SENTINEL = 0x10000000, 0x20000000, 0x30000000, 0x40000000
IAT_MEMMOVE = 0x18C9AE + 0x736092   # the flush's `call [rip+0x736092]` at 0018C9A8


def build(im):
    pe = struct.unpack_from("<I", im.d, 0x3C)[0]
    size_img = struct.unpack_from("<I", im.d, pe + 24 + 56)[0]
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    uc.mem_map(im.base, (size_img + 0xFFF) & ~0xFFF)
    uc.mem_write(im.base, im.d[:0x1000])
    for name, sva, vs, ra, rs in im.secs:
        uc.mem_write(im.base + sva, im.d[ra:ra + min(rs, vs if vs else rs)])
    for b in (STUB, STACK, HEAP, SENTINEL):
        uc.mem_map(b, 0x10000)
    uc.mem_write(STUB, b"\xC3")
    uc.mem_write(SENTINEL, b"\xC3")
    uc.mem_write(IAT_MEMMOVE, struct.pack("<Q", STUB))
    return uc


def run_flush(im, entries):
    """entries: list of qwords placed in the owner vector at HEAP+0x100; returns (status, rip, fault_addr)."""
    uc = build(im)
    vec, arr = HEAP, HEAP + 0x100
    uc.mem_write(arr, b"".join(struct.pack("<Q", x) for x in entries))
    uc.mem_write(vec, struct.pack("<QQQ", arr, arr + 8 * len(entries), arr + 8 * len(entries)))
    sp = STACK + 0x8000
    uc.mem_write(sp, struct.pack("<Q", SENTINEL))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, vec)
    fault = []
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, lambda u, acc, addr, size, val, ud: fault.append(addr) or False)
    try:
        uc.emu_start(0x18C8F0, SENTINEL, count=100000)
        return "returned", uc.reg_read(UC_X86_REG_RIP), None
    except UcError:
        return "fault", uc.reg_read(UC_X86_REG_RIP), fault[0] if fault else None


print("unicorn %s" % unicorn.__version__)
OBJ, VT = HEAP + 0x800, HEAP + 0x900
st, rip, fa = run_flush(img, [0])
report("U1_null_owner_entry_faults_at_0018C933", st == "fault" and rip == 0x18C933 and fa == 0x10,
       "status %s, rip %X, unmapped read at %s" % (st, rip, fa is not None and "%X" % fa))


def run_flush_obj(im):
    uc_entries = [OBJ]
    uc = build(im)
    vec, arr = HEAP, HEAP + 0x100
    uc.mem_write(OBJ, struct.pack("<Q", VT) + b"\0" * 8 + b"\x01" + b"\0" * 7)   # +0x10 = 1: not executed, only destroyed
    uc.mem_write(VT, struct.pack("<Q", STUB))                                  # slot 0 -> ret
    uc.mem_write(arr, struct.pack("<Q", OBJ))
    uc.mem_write(vec, struct.pack("<QQQ", arr, arr + 8, arr + 8))
    sp = STACK + 0x8000
    uc.mem_write(sp, struct.pack("<Q", SENTINEL))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, vec)
    try:
        uc.emu_start(0x18C8F0, SENTINEL, count=100000)
        end = struct.unpack("<Q", uc.mem_read(vec + 8, 8))[0]
        return "returned", end == arr
    except UcError:
        return "fault", False


st2, emptied = run_flush_obj(img)
report("U2_harness_control_nonnull_entry_returns_and_empties", st2 == "returned" and emptied,
       "status %s, vector emptied %s (the harness itself does not fault)" % (st2, emptied))

# ---- C: sensitivity controls
old_reading = tested1   # "absorbed silently" requires the flush to null-test before its first dereference
report("C1_old_reading_flush_null_tests_is_false_on_shipping_image", old_reading is False,
       "old reading evaluates to %s (must be False)" % old_reading)

# patched copy: 0018C930  48 8B 3B  mov rdi,[rbx] ; 48 85 FF test rdi,rdi ; 74 14 je 0018C94C ; 90
patched = img.patched(0x18C930, bytes.fromhex("488B3B4885FF741490"))
pt, _ = null_tested_before_deref(patched, 0x18C930)
pst, prip, pfa = run_flush(patched, [0])
report("C2_patched_null_test_is_detected_and_null_run_returns", pt is True and pst == "returned",
       "patched image: detector tested=%s, null-entry run %s (shipping image: tested=%s, %s at %X)" % (pt, pst, tested1, st, rip))

print("FAILS %d" % FAILS)
sys.exit(1 if FAILS else 0)
