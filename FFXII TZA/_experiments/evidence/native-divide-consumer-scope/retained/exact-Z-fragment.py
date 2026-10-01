# Z
cs.detail = True
wx, we = [], []
for lo, hi in ((0x25E4C0, 0x25E550), (0x25E550, 0x261DDB)):
    for x in cs.disasm(d[off(lo):off(hi)], lo):
        try: _, wr = x.regs_access()
        except Exception: continue
        if X86_REG_XMM7 in wr: wx.append(x.address)
        if X86_REG_EBP in wr or X86_REG_RBP in wr: we.append((x.address, x.mnemonic))
cs.detail = False
Zd = {a: (m, o) for a, m, o in dis(0x25E550, 0x25E567)}
check("Z", wx == [0x25E55F, 0x261DBC] and Zd.get(0x25E555) == ("mov", "ebp, 1") and Zd.get(0x25E55F) == ("xorps", "xmm7, xmm7")
      and [a for a, m in we if a >= 0x25E550 and m not in ("pop", "push")] == [0x25E555],
      "the interpreter writes xmm7 only at 0025E55F (zero) and 00261DBC (restore); ebp only at 0025E555 (= 1) besides push/pop; ebp writes %s" % [hex(a) for a, m in we])
