"""P6 (static) - which table the condition arm 00301830 actually indexes, and which of its slots are
empty.

EXP-095 names the spec table `0x1ED0460` and lists its holes as 0x4038-0x4047 and 0x4128-0x412F.
The shipped code reads:
    003018DD  lea eax, [rdx - 0x4000]
    003018E3  cmp eax, 0x166
    003018E8  ja  0x301aa4                   ; ids above 0x4166 never reach the table
    003018F0  lea rcx, [rip -> 01EEC460]
    003018F7  cmp qword ptr [rcx + rax*8], rsi
So the table is 01EEC460, with 8-byte entries and 0x167 slots. This probe counts the empty slots
there and the nonzero bytes over the same extent at 01ED0460. It executes nothing, so there is no
RIP status to report.
"""
import os, struct, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load, read

raw, secs = load()
n = 0x167
a = read(raw, secs, 0x1ED0460, n * 8)
print("01ED0460 (EXP-095's named table), %d bytes: nonzero bytes = %d" % (n * 8, sum(1 for b in a if b)))
t = read(raw, secs, 0x1EEC460, n * 8)
empty = [0x4000 + i for i in range(n) if struct.unpack_from("<Q", t, i * 8)[0] == 0]
print("01EEC460 (the lea target at 003018F0): %d slots, empty = %d -> %s"
      % (n, len(empty), [hex(x) for x in empty]))
print("first entry 01EEC460[0] = %016X" % struct.unpack_from("<Q", t, 0)[0])
