# routertab.py : decode the UI request router 00254B50's two-level jump table.
#
#   byteIdx = byte [00254C70 + (id - 1)]       id in 1..24  (lea eax,[rbx-1]; cmp eax,0x17; ja default)
#   arm     = 00120000 + dword[00254C58 + 4 * byteIdx]
#
# The table's targets are ARMS INSIDE 00254B50, not route functions, so each arm is followed to its
# first direct call to name the route. Control: ids 1 and 4 must reach the SAME route, 0035D660 -
# the router page states they share the battle-menu open, and a decode that loses that agreement is
# reading the wrong tables, or the right tables at the wrong level.
import struct

exec(open('disw.py').read().split("fn = int")[0])

BYTES, DWORDS, BASE = 0x254C70, 0x254C58, 0x120000

rows = []
for rid in range(1, 25):
    bi = d[off(BYTES) + rid - 1]
    arm = BASE + struct.unpack_from("<I", d, off(DWORDS) + 4 * bi)[0]
    rows.append((rid, bi, arm))

groups = {}
for rid, bi, arm in rows:
    groups.setdefault((bi, arm), []).append(rid)


def route_of(arm, span=0x18):
    """The arm's first direct call - the route function it hands the request to."""
    for x in md.disasm(d[off(arm):off(arm) + span], arm):
        if x.mnemonic == "call" and x.op_str.startswith("0x"):
            return int(x.op_str, 16)
    return None


print("id  arm-index  arm       route")
for rid, bi, arm in rows:
    r = route_of(arm)
    print("%2d      %2d     %08X  %s %s"
          % (rid, bi, arm, ("%08X" % r) if r else "(no call in the arm)", names.get(r, "") if r else ""))

print("\ndistinct arms: %d" % len(groups))
for (bi, arm), ids in sorted(groups.items()):
    r = route_of(arm)
    print("  arm %2d %08X -> %-10s %-24s ids %s"
          % (bi, arm, ("%08X" % r) if r else "(none)", names.get(r, "") if r else "", ids))

ctrl = {rid: route_of(arm) for rid, bi, arm in rows}
ok = ctrl[1] == ctrl[4] == 0x35D660
print("\nCONTROL  ids 1 and 4 share one route, and it is 0035D660 : %s  (%s, %s)"
      % (ok, "%08X" % ctrl[1] if ctrl[1] else None, "%08X" % ctrl[4] if ctrl[4] else None))
