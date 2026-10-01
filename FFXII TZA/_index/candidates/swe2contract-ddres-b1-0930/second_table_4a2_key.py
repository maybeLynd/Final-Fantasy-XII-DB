"""second_table_4a2_key.py - regression for the second-console-table page's +0x4A2 correction (SWE2-CONTRACT,
2026-09-30). Static. Reads only. Rejects the old reading ("a console arm writes +0x4A2 and `lea rdx,[0x8FA928]`
selects it: ShadowValueB"; "a glyph-record builder copies it").

Checks (exit 1 on any failure):
  K1 the store `mov byte ptr [rax+0x4a2], bl` at 001C977B lies inside 001C7940 (the scene-config loader), not inside
     the console dispatcher 001D1660 (13,753 B) — so the writer is not a console arm;
  K2 the loader idiom: the key string whose `lea rdx` precedes the lookup call 001FF740 that precedes the byte's
     source (`cmp eax,1 / sete bl` after the int reader 00200B80) is `mUseLinearTonemap`; and the `lea` AFTER the store
     (001C978E, 008FA928) is `ShadowValueB`, i.e. the next setting's key, not this one's. Positive control: the same
     rule applied to the preceding float store 001C972F names `mMapObjectShadowFadeRange`;
  K3 the reader 0018F316 lies inside 0018EEE0, and the byte goes to [rdi+0x9a] (0018F31D).
"""
import sys
import capstone
import block_writer_disjoint as b


def inside(ext, addr, fn):
    return fn <= addr < fn + ext[fn]


def cstr(at, a):
    d = at(a, 64)
    return d.split(b"\0")[0].decode("ascii", "replace") if d else None


def key_for_store(ins, k, at):
    """walk back from the store at index k: the lookup call 001FF740 nearest before the reader call, then the
    `lea rdx` nearest before that lookup."""
    j = k
    while j > 0 and not (ins[j].mnemonic == "call" and ins[j].op_str in ("0x200b50", "0x200b80")):
        j -= 1
    while j > 0 and not (ins[j].mnemonic == "call" and ins[j].op_str == "0x1ff740"):
        j -= 1
    while j > 0:
        j -= 1
        i = ins[j]
        if i.mnemonic == "lea" and i.op_str.startswith("rdx, [rip"):
            return cstr(at, i.address + i.size + i.operands[1].mem.disp)
    return None


def main():
    at, ext = b.load(), b.extents()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    fails = 0
    k1 = inside(ext, 0x001C977B, 0x001C7940) and not inside(ext, 0x001C977B, 0x001D1660)
    ins = list(md.disasm(at(0x001C7940, ext[0x001C7940]), 0x001C7940))
    idx = {i.address: n for n, i in enumerate(ins)}
    key_4a2 = key_for_store(ins, idx[0x001C977B], at)
    key_ctl = key_for_store(ins, idx[0x001C972F], at)
    nxt = ins[idx[0x001C978E]]
    next_key = cstr(at, nxt.address + nxt.size + nxt.operands[1].mem.disp)
    k2 = key_4a2 == "mUseLinearTonemap" and key_ctl == "mMapObjectShadowFadeRange" and next_key == "ShadowValueB"
    rd = list(md.disasm(at(0x0018F316, 16), 0x0018F316))
    k3 = inside(ext, 0x0018F316, 0x0018EEE0) and "0x4a2" in rd[0].op_str and rd[1].op_str.startswith("byte ptr [rdi + 0x9a]")
    for ok, name in ((k1, "K1 001C977B is in 001C7940, not in the console 001D1660"),
                     (k2, "K2 +0x4A2 key = %r (control %r); the lea after the store = %r" % (key_4a2, key_ctl, next_key)),
                     (k3, "K3 0018F316 is in 0018EEE0 and stores to [rdi+0x9a]")):
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
        fails += not ok
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
