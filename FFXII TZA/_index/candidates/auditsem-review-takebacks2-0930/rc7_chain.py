"""SWE2-AUDIT-SEM RC-7 re-read (own code): 0061FDA0 from the MSAA byte read to both device vtable +0x28
(ID3D11Device::CreateTexture2D) calls. Prints (1) the descriptor stores at rsp+0x48.. (D3D11_TEXTURE2D_DESC: +0x14 =
SampleDesc.Count, +0x18 = Quality), (2) the straight span 0061FEFE..006200CD, (3) every call and every access to
the descriptor copy at rsp+0x78 / rbp-0x78 / rbp-0x80 and to the flag at rsp+0x24."""
import img
xs = [x for x in img.dis(0x0061FDA0, 1200, stop_ret=False) if x.address < 0x006203A0]
print("(1) descriptor stores and the byte read")
for x in xs:
    s = x.op_str
    if x.address <= 0x0061FF00 and ("rsp + 0x4" in s or "rsp + 0x5" in s or "rsp + 0x6" in s or "rsp + 0x7" in s
                                   or 0x0061FEB0 <= x.address):
        print("  %08X %s %s" % (x.address, x.mnemonic, s))
print("(2) span 0061FEFE..006200E5")
for x in xs:
    if 0x0061FEFE <= x.address <= 0x006200E5:
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("(3) calls, the copy and the flag")
for x in xs:
    if x.mnemonic == "call" or any(k in x.op_str for k in ("rbp - 0x78", "rbp - 0x80", "rsp + 0x78", "rsp + 0x24")):
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
