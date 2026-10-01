"""s02_emu.py - SWE2-AUDIT-SPEC independent re-execution of a sample of SECTION-02's native checks (2026-09-30).

Evidence class: ISOLATED ORIGINAL CODE (emulation). Unicorn 2 on Windows, not the package's C host and not Linux. The
certified image (sha asserted by ind.py) is mapped at its image base with every section's raw bytes and zero-filled
virtual tails; the original queue bodies run unmodified. No bridge or stub is installed: execution is confined to an
allow-list of original bodies (the SECTION-02 manifest's queue bodies and leaves), and ANY fetch outside it stops the
run and fails the check - so every result below comes from original instructions only. Calls use the Microsoft x64 ABI
(rcx, rdx, r8, r9, then stack args above a 0x20 shadow space) and return to a sentinel.

Checks (names follow native_controls.c where they correspond):
  constructor_all_64_links_and_indices, constructor_preserves_unwritten_bytes (A5 prefill)
  take_moves_free_head_not_array_base, tail_insert_preserves_head, head_insert_reorders_pending,
  retire_middle_updates_both_neighbors, retire_head_preserves_tail, retire_last_empties_pending,
  splice_does_not_zero_payload_or_state, sixty_fourth_take_exhausts_free_list
  request_stamps_defined_fields, request_ignores_descriptor_part_callback
  offset_truncation_<v> for the package's ten offsets (expected: C truncation toward zero to a 0x800 multiple)
  generation_and_slot_are_distinct, slot_reuse_changes_request_generation,
  maximum_constructor_domain_counter_wraps_to_one, out_of_domain_counter_uses_signed_wrap_compare,
  planted_zero_counter_still_consumes_slot
  cancel_rejects_stale_generation, cancel_rejects_sentinel_ids, cancel_without_callback_preserves_byte_count
  null_part_callback_returns_1 (0032E3B0 on a slot whose +0x50 is 0)
Control (sensitivity): the offset check is also run against a deliberately wrong expectation (round up), which must
fail for the positive unaligned offsets; and an out-of-allow-list call must be caught (0032E520(0) drains through the
footer services, which are NOT allowed, so it must stop at 003EADD0 or 0046DD50).
"""
import os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ddres-b6-0930"))
import ind as I  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UcError
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,
                               UC_X86_REG_RAX, UC_X86_REG_RIP)

SLOT, PH, PT, FH, CTR = 0x022C31C0, 0x022C51C0, 0x022C51C8, 0x022C51D0, 0x01EED498
GATE = 0x02B5E111       # the chunked-builder gate byte read by 0032E620 (package: w8(0x2b5e111, ...))
HEAP, STACK, SENT = 0x40000000, 0x50000000, 0x60000000
ALLOW = [(0x0032E040, 0x0032E066), (0x0032E070, 0x0032E2CD), (0x0032E2F0, 0x0032E322), (0x0032E330, 0x0032E36B),
         (0x0032E370, 0x0032E3AE), (0x0032E3B0, 0x0032E3EA), (0x0032E400, 0x0032E450), (0x0032E450, 0x0032E4CE),
         (0x0032E4D0, 0x0032E512), (0x0032E520, 0x0032E58B), (0x0032E590, 0x0032E611), (0x0032E620, 0x0032E774),
         (0x0032E780, 0x0032E7AC), (0x0032E870, 0x0032E98D), (0x0032E990, 0x0032EA4A), (0x0032EC40, 0x0032ECD3),
         (0x003EB0D0, 0x003EB0F9), (0x0035E810, 0x0035E818), (0x0046DFE0, 0x0046DFF2), (0x0046E0E0, 0x0046E0E7),
         (0x0016D6A0, 0x0016D6A3), (0x003697F0, 0x003697FD)]

mu = Uc(UC_ARCH_X86, UC_MODE_64)
size = (I.pe.OPTIONAL_HEADER.SizeOfImage + 0xFFF) & ~0xFFF
mu.mem_map(I.IB, size)
for s in I.pe.sections:
    raw = I.raw[s.PointerToRawData:s.PointerToRawData + min(s.SizeOfRawData, s.Misc_VirtualSize)]
    mu.mem_write(I.IB + s.VirtualAddress, raw)
PRISTINE = bytes(mu.mem_read(0x01DF0000, 0x02F98000 - 0x01DF0000))   # .data incl. its zero tail
mu.mem_map(HEAP, 0x10000)
mu.mem_map(STACK, 0x10000)
mu.mem_map(SENT, 0x1000)
mu.mem_write(SENT, b"\xC3")
state = {"escape": None}


def hook(uc, addr, sz, _):
    if addr == SENT:
        return
    if not any(a <= addr < b for a, b in ALLOW):
        state["escape"] = addr
        uc.emu_stop()


mu.hook_add(UC_HOOK_CODE, hook)


def call(fn, *args):
    state["escape"] = None
    rsp = STACK + 0x8000
    stack_args = list(args[4:])
    frame = struct.pack("<Q", SENT) + b"\0" * 0x20 + b"".join(struct.pack("<Q", x & 0xFFFFFFFFFFFFFFFF) for x in stack_args)
    mu.mem_write(rsp, frame + b"\0" * 0x80)
    regs = (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9)
    for r, v in zip(regs, args[:4]):
        mu.reg_write(r, v & 0xFFFFFFFFFFFFFFFF)
    mu.reg_write(UC_X86_REG_RSP, rsp)
    try:
        mu.emu_start(fn, SENT, timeout=5_000_000, count=2_000_000)
    except UcError as e:
        return ("fault", str(e), mu.reg_read(UC_X86_REG_RIP))
    if state["escape"] is not None:
        return ("escape", state["escape"])
    return mu.reg_read(UC_X86_REG_RAX)


def r8(a): return mu.mem_read(a, 1)[0]
def r16(a): return struct.unpack("<H", mu.mem_read(a, 2))[0]
def r32(a): return struct.unpack("<I", mu.mem_read(a, 4))[0]
def r64(a): return struct.unpack("<Q", mu.mem_read(a, 8))[0]
def w8(a, v): mu.mem_write(a, bytes([v & 0xFF]))
def w32(a, v): mu.mem_write(a, struct.pack("<I", v & 0xFFFFFFFF))
def w64(a, v): mu.mem_write(a, struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF))
def sl(i): return SLOT + 0x80 * i


def reset(fill):
    mu.mem_write(0x01DF0000, PRISTINE)
    mu.mem_write(SLOT, bytes([fill]) * (64 * 0x80))
    mu.mem_write(HEAP, b"\0" * 0x10000)
    rv = call(0x0032E450)
    assert not isinstance(rv, tuple), rv


def graph():
    seen = [0] * 64
    p, prev, n = r64(PH), 0, 0
    while p:
        if not (SLOT <= p < SLOT + 64 * 128) or (p - SLOT) % 128 or n >= 64:
            return False
        n += 1
        k = (p - SLOT) // 128
        seen[k] += 1
        if seen[k] > 1 or r64(p + 0x18) != prev:
            return False
        prev, p = p, r64(p + 0x10)
    if prev != r64(PT):
        return False
    p, prev, n = r64(FH), 0, 0
    while p:
        if not (SLOT <= p < SLOT + 64 * 128) or (p - SLOT) % 128 or n >= 64:
            return False
        n += 1
        k = (p - SLOT) // 128
        seen[k] += 1
        if seen[k] > 1 or r64(p + 0x18) != prev:
            return False
        prev, p = p, r64(p + 0x10)
    return all(x == 1 for x in seen)


RES = []


def ck(name, ok, detail=""):
    RES.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name + ((" - " + detail) if detail else ""))


def allbytes(a, n, v):
    return all(x == v for x in mu.mem_read(a, n))


DST, AUX = HEAP + 0x2000, HEAP + 0x1000
DONE, CANC, PART = 0x70000010, 0x70000020, 0x70000030   # never called in these checks (addresses outside ALLOW)


def aux(off, part=PART):
    w32(AUX, off); w32(AUX + 4, 0x98765432); w32(AUX + 8, 0x89ABCDEF)
    w64(AUX + 0x10, DONE); w64(AUX + 0x18, CANC); w64(AUX + 0x20, part)


def req(k, i, d, n, a, tail):
    return call(0x0032E870, k, i, d, n, a, tail)


reset(0xA5)
ok = graph() and all(r32(sl(i) + 0x58) == i and r32(sl(i) + 0x64) == 0xFFFFFFFF and r16(sl(i) + 0x20) == 0 and r32(sl(i) + 0x28) == 0
                     for i in range(64))
ck("constructor_all_64_links_and_indices", ok, "freeHead %08X pending %X counter %d" % (r64(FH), r64(PH), r32(CTR)))
ok = all(allbytes(sl(i), 16, 0xA5) and allbytes(sl(i) + 0x22, 6, 0xA5) and allbytes(sl(i) + 0x2C, 0x2C, 0xA5)
         and allbytes(sl(i) + 0x5C, 8, 0xA5) and allbytes(sl(i) + 0x68, 0x18, 0xA5) for i in range(64))
ck("constructor_preserves_unwritten_bytes", ok)

reset(0)
rv = call(0x0032E990, 1); ck("take_moves_free_head_not_array_base", rv == SLOT and r64(FH) == sl(1) and r64(PH) == SLOT and r64(PT) == SLOT and graph(), "ret %s" % (hex(rv) if isinstance(rv, int) else rv))
rv = call(0x0032E990, 1); ck("tail_insert_preserves_head", rv == sl(1) and r64(PH) == SLOT and r64(PT) == sl(1) and r64(SLOT + 0x10) == sl(1) and graph())
rv = call(0x0032E990, 0); ck("head_insert_reorders_pending", rv == sl(2) and r64(PH) == sl(2) and r64(PT) == sl(1) and r64(sl(2) + 0x10) == SLOT and graph())
call(0x0032EC40, SLOT); ck("retire_middle_updates_both_neighbors", r64(sl(2) + 0x10) == sl(1) and r64(sl(1) + 0x18) == sl(2) and r64(FH) == SLOT and graph())
call(0x0032EC40, sl(2)); ck("retire_head_preserves_tail", r64(PH) == sl(1) and r64(PT) == sl(1) and graph())
call(0x0032EC40, sl(1)); ck("retire_last_empties_pending", r64(PH) == 0 and r64(PT) == 0 and graph())
reset(0xA5)
call(0x0032E990, 1)
before = bytes(mu.mem_read(SLOT, 128))
call(0x0032EC40, SLOT)
after = bytes(mu.mem_read(SLOT, 128))
ok = all(after[i] == before[i] for i in range(128) if not (0x10 <= i < 0x20) and not (0x64 <= i < 0x68))
ck("splice_does_not_zero_payload_or_state", ok and r32(SLOT + 0x64) == 0xFFFFFFFF and graph())
reset(0)
for _ in range(64):
    rv = call(0x0032E990, 1)
ck("sixty_fourth_take_exhausts_free_list", rv == sl(63) and r64(FH) == 0 and graph())

reset(0xA5)
aux(0x8FF)
rv = req(9, 0x1234, DST, 0x500, AUX, 1)
ck("request_stamps_defined_fields", rv == 0x40 and r8(SLOT + 0x20) == 1 and r8(SLOT + 0x21) == 9 and r32(SLOT + 0x24) == 0x1234 and
   r64(SLOT + 0x38) == DST and r64(SLOT + 0x70) == DST and r32(SLOT + 0x5C) == 0 and r16(SLOT + 0x22) == 0, "ret %s" % (hex(rv) if isinstance(rv, int) else rv))
ck("request_ignores_descriptor_part_callback", r64(AUX + 0x20) == PART and r64(SLOT + 0x50) == 0 and r64(SLOT + 0x40) == DONE and
   r64(SLOT + 0x48) == CANC and r32(SLOT + 0x60) == 0x89ABCDEF, "slot+0x50 = %X" % r64(SLOT + 0x50))


def trunc(v):
    q = abs(v) // 2048
    return (q if v >= 0 else -q) * 2048


def roundup(v):
    return -((-v) // 2048) * 2048


wrong_escaped = 0
for v in (0, 0x7FF, 0x800, 0x801, -1, -0x7FF, -0x800, -0x801, -2**31, 2**31 - 1):
    reset(0)
    aux(v)
    req(1, 0, DST, 1, AUX, 1)
    got = r32(SLOT + 0x2C)
    ck("offset_truncation_%d" % v, got == (trunc(v) & 0xFFFFFFFF), "stored 0x%08X" % got)
    wrong_escaped += (got == (roundup(v) & 0xFFFFFFFF)) and roundup(v) != trunc(v)
ck("control: the round-up expectation is rejected on every offset where it differs", wrong_escaped == 0)

reset(0)
id1 = req(1, 0, 0, 0, 0, 1); id2 = req(1, 0, 0, 0, 0, 1)
ck("generation_and_slot_are_distinct", id1 == 0x40 and id2 == 0x81 and r32(CTR) == 3 and graph(), "ids %s %s ctr %d" % (id1, id2, r32(CTR)))
call(0x0032EC40, SLOT)
rv = req(1, 0, 0, 0, 0, 1)
ck("slot_reuse_changes_request_generation", rv == 0xC0 and graph())
reset(0); w32(CTR, 0xFFFFFF); rv = req(1, 0, 0, 0, 0, 1)
ck("maximum_constructor_domain_counter_wraps_to_one", rv == 0x3FFFFFC0 and r32(CTR) == 1)
reset(0); w32(CTR, 0); rv = req(1, 0, 0, 1, 0, 1)
ck("planted_zero_counter_still_consumes_slot", rv == 0 and r64(PH) == SLOT and r64(FH) == sl(1) and r32(SLOT + 0x64) == 0)
reset(0); w32(CTR, 0x7FFFFFFF); rv = req(1, 0, 0, 0, 0, 1)
ck("out_of_domain_counter_uses_signed_wrap_compare", rv == 0xFFFFFFC0 and r32(CTR) == 0x80000000)

reset(0); aux(0)
rid = req(1, 12, DST, 123, AUX, 1)
rv = call(0x0032E590, rid + 64)
ck("cancel_rejects_stale_generation", r64(PH) == SLOT and r64(SLOT + 0x40) == DONE and not isinstance(rv, tuple))
call(0x0032E590, 0); call(0x0032E590, 0xFFFFFFFF)
ck("cancel_rejects_sentinel_ids", r64(PH) == SLOT)
reset(0)
rid = req(1, 12, DST, 123, 0, 1)
rv = call(0x0032E590, rid)
ck("cancel_without_callback_preserves_byte_count", r64(PH) == 0 and r32(SLOT + 0x28) == 123 and r8(SLOT + 0x20) == 0 and not isinstance(rv, tuple))

reset(0)
req(1, 0, DST, 1, 0, 1)
rv = call(0x0032E3B0, SLOT)
ck("null_part_callback_returns_1", rv == 1, "ret %s" % rv)

reset(0); req(1, 2, DST, 0, 0, 1)
rv = call(0x0032E520, 0)
ck("control: an out-of-allow-list call is caught (0032E520(0) drains into the footer services)",
   isinstance(rv, tuple) and rv[0] == "escape" and rv[1] in (0x003EADD0, 0x0046DD50, 0x0046E030, 0x0035EA30), str(rv if isinstance(rv, tuple) else hex(rv)))

n = len(RES); f = sum(1 for _, ok in RES if not ok)
print("CHECKS %d FAILS %d" % (n, f))
