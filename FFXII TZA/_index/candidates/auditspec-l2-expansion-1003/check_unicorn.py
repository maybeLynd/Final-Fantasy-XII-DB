"""check_unicorn.py - the replay pin, enforced (SWE2-AUDIT-SPEC, 2026-10-03, expansion item 5).

Exit 0 only when the running interpreter's unicorn equals the version pinned in replay-requirements.txt AND the
translation-block flush the shared replay worlds call actually works on a mapped page (the 2.1.0 failure mode).
A replay package can call `require_pinned_unicorn()` before mapping the image; a harness run on another version
then stops with a named reason instead of crashing mid-case or, worse, reporting a different result.

Control: the flush probe executes one instruction, flushes, rewrites it and executes again; it fails if the flush
did not discard the translated block (stale result) or raised (the 2.1.0 crash)."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def pinned():
    for line in open(os.path.join(HERE, "replay-requirements.txt"), encoding="utf-8"):
        m = re.match(r"\s*unicorn==([0-9.]+)", line)
        if m:
            return m.group(1)
    raise SystemExit("no unicorn pin found")


def flush_probe():
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import UC_X86_REG_RAX
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    uc.mem_map(0x10000, 0x1000)
    uc.mem_write(0x10000, b"\xB8\x01\x00\x00\x00")          # mov eax, 1
    uc.emu_start(0x10000, 0x10005)
    first = uc.reg_read(UC_X86_REG_RAX)
    uc.mem_write(0x10000, b"\xB8\x02\x00\x00\x00")          # mov eax, 2
    uc.ctl_flush_tb()
    uc.emu_start(0x10000, 0x10005)
    return first == 1 and uc.reg_read(UC_X86_REG_RAX) == 2


def require_pinned_unicorn():
    import unicorn
    want = pinned()
    if unicorn.__version__ != want:
        raise SystemExit("unicorn %s at %s; replay packages are pinned to %s (replay-requirements.txt)"
                         % (unicorn.__version__, sys.executable, want))
    try:
        ok = flush_probe()
    except Exception as e:  # the 2.1.0 failure is an exception from ctl_flush_tb
        raise SystemExit("ctl_flush_tb probe raised: %r" % (e,))
    if not ok:
        raise SystemExit("ctl_flush_tb probe ran but did not discard the translated block")
    return want


if __name__ == "__main__":
    import unicorn
    print("interpreter:", sys.executable)
    print("unicorn:", unicorn.__version__, "pinned:", pinned())
    try:
        print("flush probe:", "PASS" if flush_probe() else "FAIL (stale block)")
    except Exception as e:
        print("flush probe: RAISED", repr(e))
    require_pinned_unicorn()
    print("OK")
