# EXP-085 - VMNativeCommand_ExecuteLifecycle (002621D0) isolated original-code execution.
#
# CONTRACT-verb-dispatch-abi.md section 13 executes the DISPATCH half only; section 16 names
# STATE-TRANSITION - "the phase machine, which needs the executor 002621D0 and three scripted
# callbacks" - as the last offline-constructible parity dimension. This harness is exactly that:
# the shipped 461 bytes of 002621D0 plus its four real leaf callees (003DC240 / 003DC270 /
# 003DC2A0 / 00358940), all at canonical virtual addresses, with begin/poll/result supplied as
# fixture-planted stubs that LOG their full argument surface before returning a controlled value.
#
# A scripted callback is not a proved one (the contract's own caveat): what is measured here is
# the ordering, the argument registers, the phase machine, the post-result phase re-read and the
# one-value push rule - the executor's behaviour, not any verb's.
#
# Verified call surface of 002621D0 (disassembly, shipping bytes):
#   00262220 call 003DC240   (GetPollCallback - resolved unconditionally, saved for later)
#   0026223B call 00358940   (context rebind; only when word[ctx] != dword[cmdState+8])
#   0026225D call 003DC2A0   (GetResultCallback)
#   00262278 call rax        (result callback - planted stub)
#   002622BA call 003DC270   (GetBeginCallback)
#   002622DB call rax        (begin callback - planted stub)
#   002622F8 call rax        (poll callback - planted stub)
# No other call exists in the body; every path is covered by real leaves or fixture stubs.
#
# Executor signature (measured from the prologue):
#   rcx = arg1 = the actor manager (forwarded to begin as the FIFTH, stack, argument only)
#   rdx = arg2 = the issuing context (r14; word[r14] is the rebind key)
#   r8  = arg3 = the value stack (rbx; dword[r8] = depth, arrays at +4 / +0x44 / +0x84 / +0x184)
#   r9d = arg4 = the verb id: family = sar(r9d,12), command = r9d & 0xFFF
#   [rsp+0x28] = arg5 = cmdState: +8 dword rebind index, +0xC return slot, +0x15 phase byte,
#                +0x18 = 16 bytes of per-command scratch handed to every callback as r8

import hashlib, json, struct, sys, os

sys.path.insert(0, r"Database/Tools/work/ASTRA/python-libs")
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000  # canonical VAs already include it; never add it again

# ---- fixture map -------------------------------------------------------------
CTX    = 0x30000000   # issuing context: +0 word rebind key, +8 actor-table ptr
ATBL   = 0x30001000   # actor table: [0] dword count, [8+i*8] actor ptrs
CMDS   = 0x30002000   # cmdState
VSTACK = 0x30003000   # value stack: +0 depth, +4 type, +0x44 tag, +0x84 hi, +0x184 value
TRACE  = 0x30004000   # per-callback argument slots (3 x 0x40)
MGR    = 0x30006000   # the actor manager (arg1), forwarded to begin's stack slot
TBL_A  = 0x30010000   # command table for family 2 (count 0x2000 -> record 0x1FFF in range)
TBL_N  = 0x30060000   # command table for family -1 (the sar case; count 0x1000)
STUBS  = 0x38000000   # planted callback code
STACK  = 0x60000000
RETQ   = 0x70000000

B_STUB = STUBS + 0x100
P_STUB = STUBS + 0x200
R_STUB = STUBS + 0x300

EXEC = 0x2621D0

FAM_ARRAY = 0x02B57EF0          # the sixteen-entry family array, hard-coded lea in all accessors

# ---- PE extraction -----------------------------------------------------------
def load_exe():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs = []
    off = pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    def rd(va, n):
        r = va - BASE
        for sva, vs, ra, rs in secs:
            if sva <= r < sva + rs:
                return d[ra + (r - sva):ra + (r - sva) + n]
        raise AssertionError("VA not in image: %x" % va)
    d = raw
    return rd

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)

# ---- stub assembler ----------------------------------------------------------
def stub(slot, retv, r9_clobber=None, phase_set=None, slot_c_write=None, log_slot_c=False):
    """A planted callback: log rcx/rdx/r8/r9/[rsp+0x20] to `slot`, apply the optional
    side effects the case ordered, return retv in eax. Reads/writes of cmdState go through
    r8 itself (r8 == cmdState+0x18 is what the executor passes), not a fixture constant -
    so the log also proves the r8 the callback received is the documented one."""
    b = b""
    b += b"\x49\xba" + qw(slot)                    # mov r10, slot
    b += b"\x49\x89\x4a\x00"                       # mov [r10+0x00], rcx
    b += b"\x49\x89\x52\x08"                       # mov [r10+0x08], rdx
    b += b"\x4d\x89\x42\x10"                       # mov [r10+0x10], r8
    b += b"\x4d\x89\x4a\x18"                       # mov [r10+0x18], r9
    b += b"\x48\x8b\x44\x24\x28"                   # mov rax, [rsp+0x28]  (incoming arg5 - the
                                                 # caller's [rsp+0x20] before `call` pushed ret)
    b += b"\x49\x89\x42\x20"                       # mov [r10+0x20], rax
    if log_slot_c:
        b += b"\x49\x8b\x40\xf4"                   # mov rax, [r8-0xC]    (cmdState+0xC)
        b += b"\x49\x89\x42\x28"                   # mov [r10+0x28], rax
    if phase_set is not None:
        b += b"\x41\xc6\x40\xfd" + bytes([phase_set])      # mov byte [r8-3], imm (cmdState+0x15)
    if slot_c_write is not None:
        b += b"\x41\xc7\x40\xf4" + dw(slot_c_write)        # mov dword [r8-0xC], imm
    if r9_clobber is not None:
        b += b"\x49\xb9" + qw(r9_clobber)                  # mov r9, sentinel
    b += b"\xb8" + dw(retv)                        # mov eax, retv
    b += b"\xc3"                                   # ret
    return b

# ---- record/table builders ----------------------------------------------------
def write_table(uc, tbl, count, records):
    """records: {cmd: (begin, poll, result)} - the +0x10 unused slot gets a distinct value."""
    uc.mem_write(tbl, dw(count) + b"\0\0\0\0")
    for cmd, (bg, pl, rs) in records.items():
        rec = tbl + 8 + cmd * 32
        uc.mem_write(rec,      qw(bg))
        uc.mem_write(rec + 8,  qw(pl))
        uc.mem_write(rec + 16, qw(0x5555_0000_0000_0000 | cmd))
        uc.mem_write(rec + 24, qw(rs))

# ---- the machine --------------------------------------------------------------
def build_world(case, rd):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    # shipped bodies at canonical VAs
    for page, size in [(0x262000, 0x2000), (0x358000, 0x1000),
                       (0x3DC000, 0x1000), (0x2B57000, 0x1000)]:
        uc.mem_map(page, size)
    for va, n in [(EXEC, 0x1D0), (0x358940, 0x20),
                  (0x3DC240, 0x90)]:   # all three accessors + fail arms, one span
        uc.mem_write(va, rd(va, n))
    # fixture regions
    for a, s in [(CTX,0x1000),(ATBL,0x1000),(CMDS,0x1000),(VSTACK,0x1000),
                 (TRACE,0x1000),(MGR,0x1000),(TBL_A,0x50000),(TBL_N,0x30000),
                 (STUBS,0x1000)]:
        uc.mem_map(a, s)
    uc.mem_map(STACK, 0x20000)
    uc.mem_map(RETQ, 0x1000)
    uc.mem_write(RETQ, b"\xc3")

    # ---- family array: family 2 -> TBL_A, family -1 -> TBL_N, rest zero
    fam = {1: TBL_A, 2: TBL_A, -1: TBL_N}   # family 1 shares TBL_A - the 0x1FFF-mask case needs
                                           # a real table where record 0x1FFF differs from 0xFFF
    for f, p in fam.items():
        uc.mem_write(FAM_ARRAY + (f & 0xFFFFFFFFFFFFFFFF) * 8, qw(p))

    # ---- command tables
    # TBL_A count 0x2000; commands 0..3 carry the presence/absence matrix, 0xFFF is real
    # (for the and-mask mutant), 0x1FFF is left zeroed.
    write_table(uc, TBL_A, 0x2000, {
        0: (B_STUB, P_STUB, R_STUB),
        1: (0,      P_STUB, R_STUB),
        2: (B_STUB, 0,      R_STUB),
        3: (B_STUB, P_STUB, 0),
        0xFFF: (B_STUB, P_STUB, R_STUB),
    })
    # TBL_N count 0x1000; only command 0xFFF real - reached by id=0xFFFFFFFF via sar.
    write_table(uc, TBL_N, 0x1000, {0xFFF: (B_STUB, P_STUB, R_STUB)})

    # ---- planted callbacks (defaults; cases may swap individual stubs)
    su = case.get("stubs", {})
    uc.mem_write(B_STUB, su.get("begin",  stub(TRACE + 0x00, retv=0x77, log_slot_c=True)))
    uc.mem_write(P_STUB, su.get("poll",   stub(TRACE + 0x40, retv=case.get("poll_retv", 0))))
    uc.mem_write(R_STUB, su.get("result", stub(TRACE + 0x80, retv=0,
                                              phase_set=case.get("result_phase"),
                                              slot_c_write=case.get("result_slot_c"))))

    # ---- context / manager actor table
    # 00262238 mov rcx,rbp: 00358940 is called on the MANAGER (arg1), not the context -
    # the rebind table lives at [MGR+8]; the comparison key stays word[CTX] vs dword[CMDS+8].
    uc.mem_write(CTX, struct.pack("<H", case.get("ctx_word", 2)))
    uc.mem_write(CTX + 8, qw(0xBADBAD))            # a marker: the rebind must NOT read this
    atbl_ptr = case.get("mgr_atbl", ATBL)
    uc.mem_write(MGR + 8, qw(atbl_ptr))
    if atbl_ptr:
        uc.mem_write(ATBL, dw(case.get("atbl_count", 4)))
        for i in range(4):
            uc.mem_write(ATBL + 8 + i * 8, qw(ATBL + 0x100 + i * 0x40))

    # ---- cmdState
    uc.mem_write(CMDS + 8,  dw(case.get("rebind_idx", 2)))
    uc.mem_write(CMDS + 0xC, dw(case.get("slot_c", 0xCAFEBABE)))
    uc.mem_write(CMDS + 0x15, bytes([case.get("phase", 0)]))
    if "phase16" in case:
        uc.mem_write(CMDS + 0x16, bytes([case["phase16"]]))

    # ---- value stack
    uc.mem_write(VSTACK, dw(case.get("depth", 0)))

    # ---- mutants (byte patches on the shipped body)
    for va, data in case.get("patch", []):
        uc.mem_write(va, data)

    # ---- trace hooks
    order = []
    writes = []
    reads = []
    def on_code(uc_, addr, size, _):
        tag = {B_STUB: "B", P_STUB: "P", R_STUB: "R"}.get(addr)
        if tag:
            order.append(tag)
    def on_write(uc_, access, addr, size, value, _):
        writes.append((addr, size, value))
    def on_read(uc_, access, addr, size, value, _):
        reads.append((addr, size, value))
    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    uc.hook_add(UC_HOOK_MEM_READ, on_read)
    return uc, order, writes, reads

def run_case(case, rd):
    uc, order, writes, reads = build_world(case, rd)
    sp = STACK + 0x10000
    uc.mem_write(sp, qw(RETQ))                    # return address
    uc.mem_write(sp + 0x28, qw(CMDS))             # arg5 on the stack
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, MGR)             # arg1 manager
    uc.reg_write(UC_X86_REG_RDX, CTX)             # arg2 issuing context
    uc.reg_write(UC_X86_REG_R8,  VSTACK)          # arg3 value stack
    uc.reg_write(UC_X86_REG_R9D, case.get("id", (2 << 12) | case.get("cmd", 0)))
    fault = None
    try:
        uc.emu_start(EXEC, RETQ, count=200000)
    except Exception as e:
        fault = str(e)
    nv = {r: uc.reg_read(r) for r in
          (UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI,
           UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15)}
    snap = {
        "eax": uc.reg_read(UC_X86_REG_RAX),
        "phase": uc.mem_read(CMDS + 0x15, 1)[0],
        "slot_c": struct.unpack("<I", uc.mem_read(CMDS + 0xC, 4))[0],
        "depth": struct.unpack("<i", uc.mem_read(VSTACK, 4))[0],
        "order": list(order),
        "fault": fault,
        "nv_ok": all(v == 0 for v in nv.values()),
        "stack": [struct.unpack("<i", uc.mem_read(VSTACK, 4))[0],
                   bytes(uc.mem_read(VSTACK + 4, 64)),
                   bytes(uc.mem_read(VSTACK + 0x44, 64)),
                   bytes(uc.mem_read(VSTACK + 0x84, 256)),
                   bytes(uc.mem_read(VSTACK + 0x184, 256))],
        "slots": {name: [struct.unpack("<Q", uc.mem_read(TRACE + off + i * 8, 8))[0]
                         for i in range(6)]
                  for name, off in (("B", 0), ("P", 0x40), ("R", 0x80))},
        "writes": [(a, s, v) for a, s, v in writes],
    }
    return snap

def stype(snap, i):  return snap["stack"][1][i]
def stag(snap, i):   return snap["stack"][2][i]
def shi(snap, i):    return struct.unpack("<i", snap["stack"][3][i*4:(i+1)*4])[0]
def sval(snap, i):   return struct.unpack("<I", snap["stack"][4][i*4:(i+1)*4])[0]

def slot_arg(snap, cb, i): return snap["slots"][cb][i]

# ---- cases --------------------------------------------------------------------
def cases():
    C = lambda **k: k
    return [
        C(name="p0-run", phase=0, cmd=0, poll_retv=1,
          why="phase 0, poll returns running: begin+poll, phase->1, return 1, no push"),
        C(name="p0-done-int0", phase=0, cmd=0, poll_retv=0,
          why="poll returns 0: result runs, int-0 push, phase->0, return 0"),
        C(name="p0-result-p2", phase=0, cmd=0, poll_retv=0,
          result_phase=2, result_slot_c=0x11223344,
          why="result writes phase=2 and the return slot: the re-read pushes int slot_c"),
        C(name="p0-result-p3", phase=0, cmd=0, poll_retv=0,
          result_phase=3, result_slot_c=0x40490FDB,
          why="result writes phase=3: the re-read pushes a FLOAT from slot_c"),
        C(name="p0-result-p1", phase=0, cmd=0, poll_retv=0,
          result_phase=1, result_slot_c=0x99887766,
          why="result leaves phase<2: the pushed int is zero - slot_c is NOT pushed"),
        C(name="p1-run", phase=1, cmd=0, poll_retv=1,
          why="phase 1 skips begin entirely: poll only, phase stays 1, return 1"),
        C(name="p1-done", phase=1, cmd=0, poll_retv=0,
          why="phase 1, poll done: poll+result, no begin, phase->0"),
        C(name="p2-entry", phase=2, cmd=0,
          why="phase>=2 entry runs result ONLY; phase still 2 pushes int from slot_c - and slot_c was NOT cleared (the clear lives in the phase-0 arm)"),
        C(name="p5-entry", phase=5, cmd=0,
          why="phase 5 entry: result only, float push"),
        C(name="p0-nopoll", phase=0, cmd=2,
          why="poll slot NULL: a missing poll is not-running - begin then result"),
        C(name="p0-nobegin", phase=0, cmd=1, poll_retv=0,
          why="begin slot NULL: poll+result, no begin"),
        C(name="p0-noresult", phase=0, cmd=3, poll_retv=0,
          why="result slot NULL: begin+poll then the null arm pushes int 0 anyway"),
        C(name="stack-63", phase=0, cmd=0, poll_retv=0, depth=63,
          why="depth 63 is AT the 0x3F bound: result still runs but the push is refused"),
        C(name="stack-62", phase=0, cmd=0, poll_retv=0, depth=62,
          why="depth 62: the last writable index"),
        C(name="stack-neg1", phase=0, cmd=0, poll_retv=0, depth=-1,
          why="depth -1 is movsxd'ed: the bound passes (signed -1 < 63) and the type byte lands INSIDE the depth dword at +3"),
        C(name="p0-poll-0x100", phase=0, cmd=0, poll_retv=0x100,
          why="poll returns 0x100: test al,1 looks at the low byte only - al=0 means done"),
        C(name="p0-poll-3", phase=0, cmd=0, poll_retv=3,
          why="poll returns 3: bit 0 set means running regardless of bit 1"),
        C(name="rebind", phase=0, cmd=0, poll_retv=0, ctx_word=9, rebind_idx=2,
          why="word[ctx] != cmdState+8: 00358940 runs, callbacks get rdx = resolved actor"),
        C(name="rebind-same", phase=0, cmd=0, poll_retv=0, ctx_word=2, rebind_idx=2,
          why="keys equal: no rebind, rdx == rcx == the issuing context"),
        C(name="rebind-nulltbl", phase=0, cmd=0, poll_retv=0, ctx_word=9, mgr_atbl=0, rebind_idx=2,
          why="rebind table NULL: 00358940 returns 0 - callbacks get rdx = 0"),
        C(name="rebind-oob", phase=0, cmd=0, poll_retv=0, ctx_word=9, rebind_idx=99,
          why="rebind index >= count: rdx = 0"),
        C(name="rebind-neg", phase=0, cmd=0, poll_retv=0, ctx_word=9, rebind_idx=-1,
          why="rebind index -1 is sign-checked: rdx = 0, not table[-1]"),
        C(name="begin-eax-ignored", phase=0, cmd=0, poll_retv=1,
          why="begin returns 0x77: the executor discards it - the poll return decides"),
        C(name="poll-r9-residual", phase=0, cmd=0, poll_retv=1,
          stubs={"begin": stub(TRACE, retv=0x77, log_slot_c=True,
                               r9_clobber=0xDEAD5EED)},
          why="begin clobbers r9 to a sentinel; poll logs what the executor left it - the three-argument claim"),
        C(name="id-high-family", phase=0, cmd=0, id=0xFFFFFFFF,
          why="id FFFFFFFF: sar makes family -1 (not 0xFFFFF as shr would) -> TBL_N record 0xFFF runs"),
        C(name="id-zero", phase=0, cmd=0, id=0,
          why="id 0: family 0, command 0 - family array[0] is zero in this fixture, so no callbacks resolve"),
        C(name="mut-sar-shr", phase=0, cmd=0, id=0xFFFFFFFF,
          patch=[(0x262205, b"\x41\xc1\xec\x0c")],       # sar r12d,0xC -> shr r12d,0xC
          why="MUTANT: logical shift makes family 0xFFFFF - the array read lands far outside the page"),
        C(name="mut-and-1fff", phase=0, cmd=0, id=0x1FFF,
          patch=[(0x26220C, b"\x41\x81\xe7\xff\x1f\x00\x00")],  # and r15d,0xFFF -> 0x1FFF
          why="MUTANT: id 0x1FFF keeps command bit 12 - reads record 0x1FFF (zeroed) instead of 0xFFF"),
        C(name="mut-phase-off", phase=1, cmd=0, poll_retv=1, phase16=0,
          patch=[(0x262213, b"\x0f\xb6\x77\x16")],       # movzx esi,[rdi+0x15] -> [rdi+0x16]
          why="MUTANT: phase read one byte late - phase 1 entry runs begin"),
        C(name="mut-p1-jne", phase=1, cmd=0, poll_retv=1,
          patch=[(0x26224F, b"\x0f\x85\x8a\x00\x00\x00")],  # je near -> jne near (phase==1 arm)
          why="MUTANT: phase 1 falls to the result path instead of poll-only"),
        C(name="mut-run-jne", phase=0, cmd=0, poll_retv=1,
          patch=[(0x262305, b"\x0f\x85\x4c\xff\xff\xff")],  # je near -> jne near after test al,1
          why="MUTANT: a running poll is treated as done - result runs, phase clears"),
        C(name="mut-push-jb", phase=0, cmd=0, poll_retv=0,
          patch=[(0x262283, b"\x0f\x82\x8d\x00\x00\x00")],  # jae near 00262316 -> jb near
          why="MUTANT: phase<2 after result takes the ==2 arm's jne -> float push of slot_c"),
        C(name="mut-p2-je", phase=2, cmd=0, slot_c=0x55667788,
          patch=[(0x262316, b"\x74")],                   # jne -> je (phase==2 arm)
          why="MUTANT: phase==2 after result takes the float arm instead of the int arm"),
        C(name="mut-bound-40", phase=0, cmd=0, poll_retv=0, depth=63,
          patch=[(0x262289, b"\x83\xf8\x40")],           # cmp eax,0x3F -> 0x40 (int-push arm bound)
          why="MUTANT: bound 0x40 admits index 63 - byte 63 of each array is written"),
        C(name="mut-clear-off", phase=0, cmd=0, poll_retv=0, slot_c=0xCAFEBABE,
          patch=[(0x2622B7, b"\x90\x90\x90")],           # mov [rdi+0xC],esi -> nop
          why="MUTANT: the phase-0 return-slot clear removed - begin logs the stale 0xCAFEBABE"),
    ]

# ---- expectations --------------------------------------------------------------
def expect(c, s):
    """Return a list of (what, got, want) failures."""
    F = []
    def chk(what, got, want):
        if got != want:
            F.append("%s: got %r want %r" % (what, got, want))
    n = c["name"]

    if n == "mut-sar-shr":
        chk("fault", s["fault"] is not None, True)
        return F
    if n == "mut-and-1fff":
        chk("order", s["order"], [])            # record 0x1FFF is all-zero: nothing runs
        chk("depth", s["depth"], 1)             # but the null-result push still lands
        return F
    if n == "mut-phase-off":
        chk("order", s["order"], ["B", "P"])    # phase byte read late -> phase 0 path
        return F
    if n == "mut-p1-jne":
        chk("order", s["order"], ["R"])         # phase1 -> result path
        return F
    if n == "mut-run-jne":
        chk("order", s["order"], ["B", "P", "R"])
        chk("phase", s["phase"], 0)
        return F
    if n == "mut-push-jb":
        chk("type0", stype(s, 0), 2)            # float where int was pushed
        return F
    if n == "mut-p2-je":
        chk("type0", stype(s, 0), 2)
        return F
    if n == "mut-bound-40":
        chk("depth", s["depth"], 64)            # push at index 63 landed
        return F
    if n == "mut-clear-off":
        chk("B logged slot_c", slot_arg(s, "B", 5), 0xCAFEBABE)   # stale, not cleared
        return F

    # ---- non-mutant cases
    chk("fault", s["fault"], None)
    chk("nonvolatile preserved", s["nv_ok"], True)

    if n == "p0-run":
        chk("order", s["order"], ["B", "P"])
        chk("eax", s["eax"], 1)
        chk("phase", s["phase"], 1)
        chk("depth", s["depth"], 0)
        chk("begin saw cleared slot_c", slot_arg(s, "B", 5), 0)
    elif n == "p0-done-int0":
        chk("order", s["order"], ["B", "P", "R"])
        chk("eax", s["eax"], 0)
        chk("phase", s["phase"], 0)
        chk("depth", s["depth"], 1)
        chk("type0", stype(s, 0), 1)
        chk("tag0", stag(s, 0), 6)
        chk("val0", sval(s, 0), 0)
    elif n == "p0-result-p2":
        chk("order", s["order"], ["B", "P", "R"])
        chk("depth", s["depth"], 1)
        chk("type0", stype(s, 0), 1)
        chk("val0", sval(s, 0), 0x11223344)
        chk("phase", s["phase"], 0)
    elif n == "p0-result-p3":
        chk("type0", stype(s, 0), 2)
        chk("val0", sval(s, 0), 0x40490FDB)
    elif n == "p0-result-p1":
        chk("type0", stype(s, 0), 1)
        chk("val0", sval(s, 0), 0)              # slot_c ignored when phase < 2
    elif n == "p1-run":
        chk("order", s["order"], ["P"])         # begin NOT run on phase 1
        chk("eax", s["eax"], 1)
        chk("phase", s["phase"], 1)
    elif n == "p1-done":
        chk("order", s["order"], ["P", "R"])
        chk("phase", s["phase"], 0)
    elif n == "p2-entry":
        chk("order", s["order"], ["R"])         # neither begin nor poll
        chk("type0", stype(s, 0), 1)
        chk("val0", sval(s, 0), 0xCAFEBABE)     # slot_c persisted - NOT cleared
    elif n == "p5-entry":
        chk("order", s["order"], ["R"])
        chk("type0", stype(s, 0), 2)
        chk("val0", sval(s, 0), 0xCAFEBABE)
    elif n == "p0-nopoll":
        chk("order", s["order"], ["B", "R"])    # missing poll = not running
    elif n == "p0-nobegin":
        chk("order", s["order"], ["P", "R"])
    elif n == "p0-noresult":
        chk("order", s["order"], ["B", "P"])
        chk("depth", s["depth"], 1)
        chk("type0", stype(s, 0), 1)
        chk("val0", sval(s, 0), 0)
    elif n == "stack-63":
        chk("order", s["order"], ["B", "P", "R"])
        chk("depth", s["depth"], 63)            # push refused AT the bound
        chk("phase", s["phase"], 0)
    elif n == "stack-62":
        chk("depth", s["depth"], 63)
        chk("type at 62", stype(s, 62), 1)
    elif n == "stack-neg1":
        chk("depth", s["depth"], 0x02000000)    # type byte lands at VSTACK+3 (inside depth), then inc
    elif n == "p0-poll-0x100":
        chk("order", s["order"], ["B", "P", "R"])   # low byte 0 -> done despite 0x100
    elif n == "p0-poll-3":
        chk("order", s["order"], ["B", "P"])
        chk("eax", s["eax"], 1)
        chk("phase", s["phase"], 1)
    elif n == "rebind":
        chk("order", s["order"], ["B", "P", "R"])
        chk("B.rdx resolved", slot_arg(s, "B", 1), ATBL + 0x100 + 2 * 0x40)
        chk("B.rcx issuing ctx", slot_arg(s, "B", 0), CTX)
    elif n == "rebind-same":
        chk("B.rdx == rcx", slot_arg(s, "B", 1), CTX)
    elif n in ("rebind-nulltbl", "rebind-oob", "rebind-neg"):
        chk("order", s["order"], ["B", "P", "R"])
        chk("B.rdx null", slot_arg(s, "B", 1), 0)
    elif n == "begin-eax-ignored":
        chk("order", s["order"], ["B", "P"])
        chk("eax", s["eax"], 1)                  # poll's 1, not begin's 0x77
    elif n == "poll-r9-residual":
        chk("order", s["order"], ["B", "P"])
        chk("P.r9 residual", slot_arg(s, "P", 3), 0xDEAD5EED)
    elif n == "id-high-family":
        chk("order", s["order"], ["B", "P", "R"])
    elif n == "id-zero":
        chk("order", s["order"], [])             # family 0 unplanted -> all null
        chk("depth", s["depth"], 1)              # null-result push still lands
    else:
        F.append("no expectation for case")

    # ---- argument-register claims, checked on every case whose callbacks ran
    if "B" in s["order"]:
        chk("B.rcx", slot_arg(s, "B", 0), CTX)
        chk("B.r8 scratch", slot_arg(s, "B", 2), CMDS + 0x18)
        chk("B.r9 stack", slot_arg(s, "B", 3), VSTACK)
        chk("B stack arg = manager", slot_arg(s, "B", 4), MGR)
    if "P" in s["order"]:
        chk("P.rcx", slot_arg(s, "P", 0), CTX)
        chk("P.r8 scratch", slot_arg(s, "P", 2), CMDS + 0x18)
        if n != "poll-r9-residual":
            # r9 is never set for poll: it holds whatever the previous frame left -
            # the value-stack pointer if begin ran (it was set for begin), else the id.
            want_r9 = VSTACK if "B" in s["order"] else c.get("id", (2 << 12) | c.get("cmd", 0))
            chk("P.r9 residual", slot_arg(s, "P", 3), want_r9)
    if "R" in s["order"]:
        chk("R.rcx", slot_arg(s, "R", 0), CTX)
        chk("R.r8 scratch", slot_arg(s, "R", 2), CMDS + 0x18)
        chk("R.r9 stack", slot_arg(s, "R", 3), VSTACK)
    return F

def main():
    rd = load_exe()
    out = {"exe_sha256": SHA, "harness": os.path.basename(__file__), "cases": []}
    npass = nfail = ndetected = nmut = 0
    for c in cases():
        s = run_case(c, rd)
        fails = expect(c, s)
        is_mut = n = c["name"].startswith("mut-")
        passed = not fails
        npass += passed
        nfail += not passed
        nmut += is_mut
        ndetected += is_mut and passed
        row = {"name": c["name"], "why": c["why"], "pass": passed,
               "order": s["order"], "eax": s["eax"], "phase": s["phase"],
               "depth": s["depth"], "fault": s["fault"], "failures": fails,
               "slots": {k: ["%x" % v for v in vv] for k, vv in s["slots"].items()}}
        out["cases"].append(row)
        print("%-22s %-4s order=%-9s eax=%-3s phase=%s depth=%-3s %s" %
              (c["name"], "PASS" if passed else "FAIL", "".join(s["order"]),
               s["eax"], s["phase"], s["depth"], "; ".join(fails) or c["why"][:60]))
    out["summary"] = {"cases": len(out["cases"]), "passed": npass, "failed": nfail,
                      "mutants": nmut, "mutants_detected": ndetected}
    print("\n%d/%d cases pass; %d/%d mutants detected" % (npass, len(out["cases"]), ndetected, nmut))
    return out

if __name__ == "__main__":
    r = main()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "result.json"), "w") as f:
        json.dump(r, f, indent=1)
