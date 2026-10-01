#!/usr/bin/env python
"""diff_storage_read - the shipped storage-read completion family against storage_read.c

Three bodies run at their real virtual addresses under Unicorn. The globals they reach are
planted at their real addresses - 01F44D40/48 (storage base/end), 02EAF8E8/E0 (cursor object,
result), 02CA99B8 (recovery parent) - and the restore's destination is the image's own active
buffer at 02164280, because 002EF640 is `lea rax, [rip+disp]; ret` and RUNS rather than being
hooked: the copy lands at the shipped offset or it lands wrong.

WHAT THIS SUITE IS FOR: THE ZERO THAT IS NOT "NOTHING"
------------------------------------------------------
The contract's load-bearing claim is that a short read returns 0 AFTER writing the front of the
destination and advancing the cursor. A reconstruction that reports the partial count, or that
cleans up on failure, fails the dest digest or the cursor line. The restore is the same shape
upside down: 0xE240 bytes copied from parent+0x588, or nothing at all on a null parent - the
boundary canary at +0xE240 is the byte that proves the copy stopped before group bank A.

EDGE CASES THAT ARE REAL CODE PATHS
------------------------------------
- count == 0 returns 1, not 0: the copy is skipped by `jle`, then `0 == 0` sets the boolean.
- a negative count returns 0 by the same tail.
- null cursor object AND null destination are both refused by the inner read.
- mode != 0 in the wrapper writes -4 to the result global and returns it, touching nothing else.
- the bound check is `cursor >= end - base` UNSIGNED, computed every iteration.
"""

# PARITY - charter section 21. Declared here; parity_status.py derives CONTRACT from CONTRACT_MAP
# and reports any disagreement with what is declared.
PARITY = {
    "subsystem": "storage_read",
    "entry": "00862590",
    "contract": "19-Save-Load-Settings/CONTRACT-storage-read-completion.md",
    "dimensions": {
        "CALCULATION":      ("COVERED",
                             "the boolean tail (copied == count), the boolean-times-size product, "
                             "and the dword-width end-minus-base bound are compared as bits across "
                             "full, short, zero and negative counts"),
        "STRUCTURAL":       ("COVERED",
                             "the destination is digested whole so a short read's overwritten "
                             "front and stale tail are both visible; the restore's 0xE240 window "
                             "is digested and the 0x40 bytes behind it compared separately"),
        "STATE-TRANSITION": ("COVERED",
                             "the cursor is compared after every call - advance-on-partial and "
                             "resume-on-retry are measured, and the result global is compared on "
                             "both wrapper arms"),
        "CONTRACT":         ("NOT COVERED",
                             "derived from CONTRACT_MAP below, not declared - the queue, "
                             "dispatcher and state-machine rows are all upstream of the two "
                             "bodies this suite drives"),
        "EDGE-CASE":        ("COVERED",
                             "count 0 returns 1, negative returns 0, null cursor and null dest "
                             "are refused, cursor at and past the end, exact-boundary requests, "
                             "mode != 0, and a null recovery parent"),
        "SERIALIZATION":    ("N/A",
                             "the read is a counted byte move; no format is parsed on this path"),
        "RNG":              ("N/A", "no random draw on this path"),
        "TIMING":           ("N/A", "no ordering beyond the sequence the caller drives"),
        "INTEGRATION":      ("NOT COVERED",
                             "the storage backend that fills base/end and whoever consumes the "
                             "result global are outside these three bodies"),
        "PRESENTATION":     ("N/A", "nothing is displayed"),
        "FULL-SUBSYSTEM":   ("NOT COVERED",
                             "the seek (008625D0/00866A80), the sub-state chain and the queue "
                             "compaction named in section 4 are not driven here"),
    },
}

# One row per claim in the contract's section 15 evidence table, in the same order.
# Marking a row EXERCISED asserts that breaking the claim breaks this test.
CONTRACT_MAP = [
    ("the inner read returns a boolean, not a count",
     "EXERCISED",
     "the return is compared bitwise across full, short, at-end, zero and negative counts; a "
     "partial count is never returned - 0 or 1 only"),
    ("the wrapper multiplies that boolean by the element size",
     "EXERCISED",
     "WRAP returns size on a full read and 0 on anything short, the -4 arm writes the result "
     "global and returns it, and a mode-0 size-0 call still lands 0 through 1 * 0"),
    ("a short read has already written the destination and advanced the cursor",
     "EXERCISED",
     "the dest digest shows the front overwritten and the tail stale, and the cursor line "
     "advances by the partial count - then a retry resumes mid-buffer rather than restarting"),
    ("the recovery restore copies 0xE240 whole-image bytes and stops before group persistent "
     "bank A",
     "EXERCISED",
     "the real 002EF640 returns 0x2164280 and the copy lands there; the window digest and the "
     "0x40-byte canary behind it are compared, so a copy one byte longer or shorter shows"),
    ("the same restore copies nothing when the parent pointer is null, and returns normally",
     "EXERCISED",
     "RESTORE with the parent cleared changes neither the window nor the canary and produces "
     "the same output lines as the armed call"),
    ("the enqueue refuses a queue count of exactly 8, not `>= 8`",
     "NOT EXERCISED",
     "00582540 is upstream of this suite - the fixture drives the read and restore bodies, not the queue"),
    ("an empty completion underflows the queue count, and the same call's compaction then runs 255 `0x58`-stride shifts",
     "NOT EXERCISED",
     "00582240's count decrement and shift loop are queue machinery this suite never runs"),
    ("the underflow and the `== 8` refusal compose — `0xFF` passes the `je` and the next enqueue writes slot `0xFF`",
     "NOT EXERCISED",
     "the composition needs both queue bodies driven in sequence; neither runs here"),
    ("packet kind 8's auxiliary input is not clamped",
     "NOT EXERCISED",
     "the 13-kind dispatcher 00582040 is not among this suite's entries"),
    ("the queue compaction shifts `0x58`-stride entries down over the completed front",
     "NOT EXERCISED",
     "inside 00582240, not driven"),
    ("the load pipeline is a 16-state dispatch on `[02B40E14]`",
     "NOT EXERCISED",
     "003BA7B0's jump table is read statically; the suite drives the read body it dispatches to, not the dispatcher"),
    ("packet-9 acceptance refuses an in-flight chain and a zero length",
     "NOT EXERCISED",
     "003BB440's two guards are dispatcher-arm behaviour, not exercised"),
    ("packet-9 arms the chain at sub-state 1 with the packet's name, dest and length",
     "NOT EXERCISED",
     "same arm, same reason"),
    ("the PC record is `0x210` of cursor + mode + `wchar_t[260]` path, over a shared byte vector",
     "NOT EXERCISED",
     "008666B0's allocation shape is read statically; the suite scripts the file layer around the read it drives"),
    ("`00580840` runs `00247510` only on the state-9 success arm, parent = `[rbx+0xC0]`",
     "NOT EXERCISED",
     "the completion dispatcher is upstream of the read body; not driven"),
    ("`00580EB0` is a 15-arm state dispatcher writing `[rbx+0xE9]`; state 9 selects message `0x17`",
     "NOT EXERCISED",
     "00580EB0 is read statically; the suite's entries never reach it"),
    ("`00583990` resolves result messages through `00D23DA0`, a `{id,kind}` table clamped to 32 entries",
     "NOT EXERCISED",
     "message resolution sits behind the dispatcher, not driven"),
    ("`00580840` is re-entered as the completion callback of packets the machine itself enqueues",
     "NOT EXERCISED",
     "a re-entrancy fact about arms 8/0xB; the dispatcher does not run"),
    ("subtype `0x8001` stamps the selected slot byte at `[02CA99B8]+0x598` and the packet's `+0xEB`",
     "NOT EXERCISED",
     "0057FE80 is a different dispatch arm; not driven"),
    ("`0057FE80` is a two-level dispatcher — outer `dword[msg]−1` bounded at `0x11`, subtype select nested in outer arm 12",
     "NOT EXERCISED",
     "the message pump is upstream of the read/restore bodies; not driven"),
    ("subtype `0x12` clears `+0xD0` only when `qword[msg+0x10] == 0xA`",
     "NOT EXERCISED",
     "a subtype arm of 0057FE80; the pump is not driven"),
    ("subtype `0x1D` requires `+0xE0 & 0x10` clear and re-dispatches on `dword[[msg+0x10]]` to `00580A80`/`00580B40`/`00580CD0`",
     "NOT EXERCISED",
     "a subtype arm of 0057FE80; the pump is not driven"),
    ("subtype `0x8000` binds `edi*0xA0 + [+0x1C0]` into `+0xC8` when `*003BB3E0(slot) == 2`, else clears `[+0xC8]+0x100`",
     "NOT EXERCISED",
     "a subtype arm of 0057FE80; the pump is not driven"),
    ("`0x8001`'s tail derives `r8b` ∈ {7,8,9,0xA,0xFF} from `*info`/`[info+4]`/`+0xED`, then transitions to 1 or 0xE",
     "NOT EXERCISED",
     "the commit arm's result-code derivation; the pump is not driven"),
    ("subtype `0x8002` arms `+0xE0` bit 4 and calls `00244F00(rbx)`",
     "NOT EXERCISED",
     "a subtype arm of 0057FE80; the pump is not driven"),
    ("subtypes `0x8100`–`0x8102` re-dispatch on queue state `+0xE9 − 2` through table `0x460800`",
     "NOT EXERCISED",
     "the second nested dispatch of 0057FE80; not driven"),
    ("the `0x8100`–`0x8102` prelude sets `[02CA99E0]+0xCC = 4`, clears `+0xD8`, and runs `0057ED40`",
     "NOT EXERCISED",
     "the same nested dispatch's shared prelude; not driven"),
    ("`0057ED40` collapses `02CA99C0` to head-only when `+0xDC` bit 0 is set, else empties it",
     "NOT EXERCISED",
     "the queue-collapse helper; the queue is not driven"),
    ("outer ids 15 and 18 notify `+0xC0` through `00247510` with messages `0xF`/`0x12`",
     "NOT EXERCISED",
     "outer dispatch arms of 0057FE80; the pump is not driven"),
    ("outer id 14 selects dialog `0xC82`/`0xC84`/`0xC86` by `+0xEA` and `00394450()==3`",
     "NOT EXERCISED",
     "the dialog arm of 0057FE80; the pump is not driven"),
    ("`00582860` is the controller's own dispatcher — outer `dword[msg]−1` bounded at `0x12`, table `0x462F54`",
     "NOT EXERCISED",
     "the controller dispatcher is upstream of the read/restore bodies; not driven"),
    ("`+0x588` is allocated at controller init via `002497E0(2, 0xE240)`, exactly the backup size",
     "NOT EXERCISED",
     "the init arm of 00582860; the allocation never runs in this suite"),
    ("`+0x588` is freed at controller teardown via `003697F0` and nulled, with `+0x590` and the singleton",
     "NOT EXERCISED",
     "the teardown arm of 00582860; not driven"),
    ("`00582860` outer arm 18 is the teardown: persistence restore, normalize/reseed, sub-teardown, frees, singleton clear",
     "NOT EXERCISED",
     "the teardown arm of 00582860; not driven"),
    ("subtype `0x1D` payload-3 arm releases `+0xD8` and transitions to `0xD` in 8 of 13 queue states",
     "NOT EXERCISED",
     "00580A80 sits behind the 0x1D dispatch; not driven"),
    ("subtype `0x1D` payload-`0xD` arm's `+0xEA==0` path maps `[payload+8]` to a transition or `+0xE0`-flag dispatch",
     "NOT EXERCISED",
     "00580B40 sits behind the 0x1D dispatch; not driven"),
    ("`00580B40`'s `+0xEA!=0` path computes `(word[+0xF2]+word[+0xF4])*byte[+0xEC]+sbyte[+0xEE]+sbyte[+0xED]` and indexes `+0xEF`",
     "NOT EXERCISED",
     "the scroll-index arm of 00580B40; not driven"),
    ("subtype `0x1D` payload-`0xF` arm releases `+0xD8` then `00581350` releases `02CA99C8`'s `+0xE8` resource and plays a `+0xD0`-selected chime",
     "NOT EXERCISED",
     "00580CD0/00581350 sit behind the 0x1D dispatch; not driven"),
    ("`00582B2C` is the controller's nested subtype dispatcher — `qword[msg+8]` selects `0xF`/`0x10`/`0x12`/`0x1D`/`>0x1D`, and `0x12` re-dispatches `qword[msg+0x10]` through table `0x462FA0`",
     "NOT EXERCISED",
     "the controller's nested dispatch; not driven"),
    ("the `0x12` payload arms release or clear one controller field apiece",
     "NOT EXERCISED",
     "controller field lifecycle arms; not driven"),
    ("the `0x8001` arm posts two packets — `+0xD0` (cb `00581490`) and `+0xF8` (cb `0057F360`) — then resolves message `0xE` into `+0xF0` and enters state 2",
     "NOT EXERCISED",
     "controller packet-posting arm; not driven"),
    ("`00583040` self-posts into the queue dispatcher — when `+0xC1==0` it builds `+0xD8` = `00244F50(0x1C8, cb=0057FE80)`",
     "NOT EXERCISED",
     "the controller-to-queue cross-post; neither dispatcher is driven"),
    ("`00583040`'s nested dispatch maps `dword[msg+8]` to `{0,1,2,3,0xFF}` — `1` selects `2` or `0xFF` by `+0xC1`",
     "NOT EXERCISED",
     "00583040 sits behind the controller's 0x1D arm; not driven"),
    ("`005829C0` is the suspend path: it builds a `0x720` record when `02CA99C0==0` and arms `+0xC4` bit 1",
     "NOT EXERCISED",
     "controller arm 16; not driven"),
    ("`00582AE9` opens dialog `0x870`/`0x871` by `+0xC1` and self-posts `0x8001`",
     "NOT EXERCISED",
     "controller arm 19; not driven"),
    ("`00581310` releases its argument and, when controller `+0xC4` bit 3 is set, runs `002CC9B0`→`002CC9C0`",
     "NOT EXERCISED",
     "release helper behind the controller arms; not driven"),
    ("`005832B0` builds the `\"PS2D\"` submission descriptor — memset, magic stamp, bounds, path formatting, three `005837F0` calls",
     "NOT EXERCISED",
     "the save-write descriptor builder; a different entry family"),
    ("`00583700`/`005837F0` write the slot directory and asset names into `controller+0x128`, gated on `02CA99B8`",
     "NOT EXERCISED",
     "path builders; a different entry family"),
    ("`00583930` posts `00244F50(0x5A0, cb=00582860)` carrying `{arg3, arg1!=0, arg2!=0}`; `00583920` returns `[02CA99E8]`; `00583260` posts `00244F50(0x178, cb=0057E4D0)`",
     "NOT EXERCISED",
     "client-facing entry shims; not driven"),
    ("the `005843E0`/`00584210` admission split is `(00394450()==3)` vs `byte[+0x57]&1`, not a `+0x18`/`+0xC4` bit-4",
     "NOT EXERCISED",
     "the corrected admission pair is save-side stash/restore machinery; not among this suite's entries"),
    ("`00583CB0` backs up `0xE240` bytes from the active header to `[[02CA99B8]+0x588]+0x80`",
     "NOT EXERCISED",
     "the suite drives the restore direction (00583C00) only; the backup half never runs"),
    ("`00582040` admits the front packet through a 13-arm dispatch on `dword[+0xD8]` (table `0x46220C`); arm 1 alone copies packet `+0xE0`/`+0xE8` into queue `+0xC0`/`+0xC8`, so only a kind-1 packet carries its own completion callback and token",
     "NOT EXERCISED",
     "the start dispatcher is upstream of the two driven bodies; no packet is started"),
    ("`00582240` remaps the result two-stage — `dil` defaults to 0 for kinds 1–2 else `003BB420()`, `0017E470()` returns the stored status `[001D50D0()+0x10DC]`, and `(status, kind)` fix-ups override `dil` (status 1 or 3 with kind 7/9 → 8; status 2 with kind ≠4 → 3); `dil==4` zeroes 25 bytes at controller `+0x568`..`+0x580`",
     "NOT EXERCISED",
     "the completion remapper never runs; the suite completes nothing"),
    ("the completion callback runs `+0xC0(kind, dil, +0xC8)` only when `+0xDC` bit 1 is clear",
     "NOT EXERCISED",
     "the suppression flag and callback call live in 00582240, which is never driven"),
    ("whether any shipped caller mishandles either",
     "OPEN QUESTION",
     "no caller is driven; the claim is that the shape invites misreading, which a fixture "
     "cannot observe"),
]

import argparse
import os
import struct
import subprocess
import sys
import tempfile

try:
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UcError
    from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX,
                                   UC_X86_REG_R8, UC_X86_REG_RSP, UC_X86_REG_RIP)
except ImportError:
    sys.stderr.write("diff_storage_read: needs unicorn (pip install unicorn)\n")
    raise SystemExit(2)

INNER_FN   = 0x00866A00
WRAPPER_FN = 0x00862590
RESTORE_FN = 0x00583C00
GETBUF_FN  = 0x002EF640          # runs for real: lea rax, [ACTIVE_BUF]; ret

BASE_AT   = 0x01F44D40          # qword  - storage base pointer
END_AT    = 0x01F44D48          # dword  - storage end, as a raw 32-bit value
CUROBJ_AT = 0x02EAF8E8          # qword  - the wrapper's cursor-object pointer
RESULT_AT = 0x02EAF8E0          # dword  - the wrapper's last result
PARENT_AT = 0x02CA99B8          # qword  - the recovery source object
ACTIVE_BUF = 0x02164280         # the image's own active buffer, returned by the real getter

# fixture regions
STORAGE_AT = 0x52000000         # the storage image the base points at
DEST_AT    = 0x52100000
CURSOR_AT  = 0x52200000         # the cursor object; its first dword is the cursor
PARENTOBJ_AT = 0x52300000       # the recovery parent; +0x588 holds the source pointer
SRC_AT     = 0x52400000         # the restore's source bytes
STACK      = 0x40000000
RET_MAGIC  = 0x50000000

STORE_BYTES  = 0x1000
DEST_BYTES   = 0x400
SRC_BYTES    = 0xF000
RESTORE_LEN  = 0xE240
TAIL         = 0x40


def read_exe(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs = []
    off = pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40

    def rd(va, n):
        r = va - base
        for sva, vs, ra, rs in secs:
            if sva <= r < sva + rs:
                return d[ra + (r - sva):ra + (r - sva) + n]
        return None
    return rd


def fnv64(b):
    h = 1469598103934665603
    for x in bytearray(b):
        h ^= x
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h


def page_down(a):
    return a & ~0xFFF


def page_up(a):
    return (a + 0xFFF) & ~0xFFF


def plant(n, seed):
    s = seed if seed else 1
    out = bytearray(n)
    for i in range(n):
        s ^= (s << 13) & 0xFFFFFFFF
        s ^= s >> 17
        s ^= (s << 5) & 0xFFFFFFFF
        out[i] = s & 0xFF
    return bytes(out)


class Original(object):
    # The pages the three bodies and the real getter live on.
    REGIONS = ((0x00862000, 0x00863000), (0x00866000, 0x00867000),
               (0x00583000, 0x00584000), (0x002EF000, 0x002F0000))

    def __init__(self, rd):
        uc = Uc(UC_ARCH_X86, UC_MODE_64)
        for lo, hi in self.REGIONS:
            uc.mem_map(lo, hi - lo)
            for p in range(lo, hi, 0x1000):
                b = rd(p, 0x1000)
                if b:
                    uc.mem_write(p, b)
        mapped = set()
        for a in (BASE_AT, END_AT, CUROBJ_AT):
            pg = page_down(a)
            if pg not in mapped:
                uc.mem_map(pg, 0x1000)
                mapped.add(pg)
        uc.mem_map(page_down(PARENT_AT), 0x1000)
        uc.mem_map(page_down(ACTIVE_BUF), page_up(ACTIVE_BUF + 0x566C0) - page_down(ACTIVE_BUF))
        uc.mem_map(STORAGE_AT, 0x2000)
        uc.mem_map(DEST_AT, 0x1000)
        uc.mem_map(CURSOR_AT, 0x1000)
        uc.mem_map(PARENTOBJ_AT, 0x1000)
        uc.mem_map(SRC_AT, 0x10000)
        uc.mem_map(STACK, 0x20000)
        self.uc = uc

    def w32(self, a, v):
        self.uc.mem_write(a, struct.pack("<I", v & 0xFFFFFFFF))

    def w64(self, a, v):
        self.uc.mem_write(a, struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF))

    def r32(self, a):
        return struct.unpack("<I", self.uc.mem_read(a, 4))[0]

    def call(self, entry, rcx=0, rdx=0, r8=0):
        uc = self.uc
        sp = STACK + 0x10000
        uc.mem_write(sp, struct.pack("<Q", RET_MAGIC))
        uc.reg_write(UC_X86_REG_RSP, sp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        uc.reg_write(UC_X86_REG_R8, r8)
        uc.emu_start(entry, RET_MAGIC)
        return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF

    def reset(self):
        self.w64(BASE_AT, STORAGE_AT)
        self.w32(END_AT, (STORAGE_AT + STORE_BYTES) & 0xFFFFFFFF)
        self.w64(CUROBJ_AT, CURSOR_AT)
        self.w32(RESULT_AT, 0x77777777)
        self.w64(PARENT_AT, 0)
        self.w32(CURSOR_AT, 0)
        self.uc.mem_write(STORAGE_AT, plant(STORE_BYTES, 0x11))
        self.uc.mem_write(DEST_AT, plant(DEST_BYTES, 0xDE57))
        self.uc.mem_write(SRC_AT, plant(SRC_BYTES, 0x50))
        self.uc.mem_write(ACTIVE_BUF, plant(0x566C0, 0xAC))
        self.w64(PARENTOBJ_AT + 0x588, SRC_AT)

    def dest_line(self):
        b = self.uc.mem_read(DEST_AT, DEST_BYTES)
        return ("D %016X %s %s" % (fnv64(b), bytes(b[:16]).hex().upper(),
                                   bytes(b[DEST_BYTES - 16:]).hex().upper()))

    def run(self, script):
        out = []
        for line in script:
            p = line.split()
            if p[0] == "NEW":
                self.reset()
            elif p[0] == "STORAGE":
                n = int(p[1], 16)
                self.w64(BASE_AT, STORAGE_AT)
                self.w32(END_AT, (STORAGE_AT + n) & 0xFFFFFFFF)
            elif p[0] == "END":
                self.w32(END_AT, int(p[1], 16))
            elif p[0] == "CURSOR":
                self.w32(CURSOR_AT, int(p[1], 16))
            elif p[0] == "CUROBJ":
                self.w64(CUROBJ_AT, CURSOR_AT if int(p[1]) else 0)
            elif p[0] == "PARENT":
                self.w64(PARENT_AT, PARENTOBJ_AT if int(p[1]) else 0)
            elif p[0] in ("READ", "READN", "READD"):
                count = int(p[1], 16)
                cur = 0 if p[0] == "READN" else CURSOR_AT
                dst = 0 if p[0] == "READD" else DEST_AT
                r = self.call(INNER_FN, rcx=cur, rdx=dst, r8=count)
                out.append("R %08X" % r)
                out.append("C %08X" % self.r32(CURSOR_AT))
                out.append(self.dest_line())
            elif p[0] == "WRAP":
                r = self.call(WRAPPER_FN, rcx=int(p[1], 16), rdx=DEST_AT,
                              r8=int(p[2], 16))
                out.append("W %08X" % r)
                out.append("G %08X" % self.r32(RESULT_AT))
                out.append("C %08X" % self.r32(CURSOR_AT))
                out.append(self.dest_line())
            elif p[0] == "RESTORE":
                self.call(RESTORE_FN)
                b = self.uc.mem_read(ACTIVE_BUF, RESTORE_LEN)
                out.append("A %016X %s %s" % (fnv64(b), bytes(b[:16]).hex().upper(),
                                              bytes(b[RESTORE_LEN - 16:]).hex().upper()))
                tail = self.uc.mem_read(ACTIVE_BUF + RESTORE_LEN, TAIL)
                out.append("B " + bytes(tail).hex().upper())
            elif p[0] == "STATE":
                out.append("S cur=%08X res=%08X" % (self.r32(CURSOR_AT),
                                                  self.r32(RESULT_AT)))
            else:
                raise SystemExit("unknown op: " + p[0])
        return out


def build_script():
    s = []

    # Baseline: a full read returns the count, advances the cursor, lands the bytes.
    s += ["NEW", "STATE"]
    s += ["READ 40", "STATE"]

    # THE SHORT READ - the claim this suite exists for. avail shrinks to 0x40, a request for
    # 0x80 must return 0 AFTER overwriting the front of dest and advancing the cursor by 0x40.
    s += ["NEW", "STORAGE 40", "CURSOR 0", "READ 80", "STATE"]

    # A retry resumes mid-structure: the cursor is at the end now, so nothing more copies.
    s += ["READ 40", "STATE"]

    # A partial that is not at the end: cursor 0x20 of 0x40, request 0x30 - copies 0x20.
    s += ["NEW", "STORAGE 40", "CURSOR 20", "READ 30", "STATE"]

    # count == 0 returns 1 (vacuous full copy); a negative count returns 0. Neither moves
    # the cursor or the destination.
    s += ["NEW", "CURSOR 10", "READ 0", "STATE"]
    s += ["READ FFFFFFFC", "STATE"]

    # Both null guards.
    s += ["CURSOR 0", "READN 10", "STATE"]
    s += ["READD 10", "STATE"]

    # Cursor at and past the end, and the exact-boundary cases.
    s += ["NEW", "STORAGE 40", "CURSOR 40", "READ 10", "STATE"]   # at end
    s += ["CURSOR 1000", "READ 10", "STATE"]                       # past it
    s += ["CURSOR 3F", "READ 2", "STATE"]                          # one byte short of a pair
    s += ["CURSOR 3F", "READ 1", "STATE"]                          # exactly the last byte

    # A stale result global must be overwritten on every arm.
    s += ["NEW", "STORAGE 40"]

    # The wrapper: full read returns size and writes the result global.
    s += ["NEW", "WRAP 0 40", "STATE"]

    # mode != 0: -4 to the result global and the return, storage untouched.
    s += ["WRAP 1 40", "STATE"]

    # The wrapper resume: cursor carried by the global object.
    s += ["WRAP 0 40", "STATE"]

    # Short read through the wrapper: returns 0, cursor and dest already moved.
    s += ["NEW", "STORAGE 40", "CURSOR 0", "WRAP 0 80", "STATE"]
    s += ["WRAP 0 40", "STATE"]

    # size == 0 through the wrapper: inner returns 1, the product is still 0.
    s += ["CURSOR 0", "WRAP 0 0", "STATE"]

    # A null cursor object through the wrapper: the inner guard answers 0.
    s += ["NEW", "CUROBJ 0", "WRAP 0 10", "STATE"]
    s += ["CUROBJ 1"]

    # A negative size through the wrapper: inner returns 0, the product is 0 - and it must
    # not be -4, because that would mean the mode arm ran.
    s += ["WRAP 0 FFFFFFFC", "STATE"]

    # The recovery restore: unarmed first (null parent - nothing copies, normal return),
    # then armed. The window is digested and the 0x40 bytes behind it compared: the copy
    # must stop at 0xE240 exactly.
    s += ["NEW", "RESTORE", "STATE"]
    s += ["PARENT 1", "RESTORE", "STATE"]
    s += ["RESTORE"]          # a second armed restore over the same source is a no-op
    s += ["PARENT 0", "RESTORE", "STATE"]
    return s


def run_driver(driver, script):
    fd, name = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w") as f:
            f.write("\n".join(script) + "\n")
        p = subprocess.run([driver, name], capture_output=True, text=True)
        lines = [ln for ln in p.stdout.splitlines() if ln.strip()]
        if p.returncode != 0:
            sys.stderr.write(p.stderr)
            print("DRIVER FAILED: exit %d after %d line(s) - the lines it never produced"
                  " are compared as mismatches" % (p.returncode, len(lines)))
        return lines
    finally:
        os.unlink(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True)
    ap.add_argument("--driver", default=os.path.join(".", "storage_read_driver.exe"))
    ap.add_argument("--show", type=int, default=10)
    a = ap.parse_args()

    print("diff_storage_read - the shipped storage-read family against storage_read.c")
    print("  exe    : %s" % a.exe)
    print("  driver : %s" % a.driver)
    print()

    script = build_script()
    rd = read_exe(a.exe)
    try:
        ref = Original(rd).run(script)
    except UcError as e:
        raise SystemExit("emulation failed: %s" % e)
    got = run_driver(a.driver, script)

    # A LENGTH DIFFERENCE IS A MISMATCH, NOT A REASON TO STOP. A mutant that changed the number
    # of output lines would otherwise score INVALID instead of KILLED (hp_write, 2026-09-12).
    if len(ref) != len(got):
        print("LINE COUNT DIFFERS: reference %d, driver %d - padding the shorter side"
              % (len(ref), len(got)))
        pad = ["<missing line>"]
        ref = ref + pad * (len(got) - len(ref)) if len(ref) < len(got) else ref
        got = got + pad * (len(ref) - len(got)) if len(got) < len(ref) else got

    # Controls: a suite that only ever saw zeroes could pass vacuously. Print the counts that
    # prove the states actually differed.
    rets = set(x for x in ref if x.startswith("R ") or x.startswith("W "))
    digests = set(x for x in ref if x.startswith("D ") or x.startswith("A "))
    cursors = set(x for x in ref if x.startswith("C "))
    print("%d commands, %d compared lines" % (len(script), len(ref)))
    print("  distinct return values     : %d" % len(rets))
    print("  distinct buffer digests    : %d" % len(digests))
    print("  distinct cursor values     : %d" % len(cursors))
    print()

    mism = [(i, r, g) for i, (r, g) in enumerate(zip(ref, got)) if r != g]
    print("cases: %d" % len(script))
    print("%d comparisons, %d mismatches" % (len(ref), len(mism)))
    for i, r, g in mism[:a.show]:
        print("  line %d" % i)
        print("    original      %s" % r)
        print("    reconstruction %s" % g)
    print("RESULT: %s" % ("OK" if not mism else "FAIL"))
    return 1 if mism else 0


if __name__ == "__main__":
    raise SystemExit(main())
