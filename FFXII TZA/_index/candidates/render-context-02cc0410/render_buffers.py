"""render_buffers.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
RenderContext02CC0410's +0x520..+0x82F span, read from the objects' own creators and from the context's teardown, and the
four buffer sizes the creators take from the context's +0xF4..+0x103.

  D  the context's teardown 0062B5A0 (called at 0079F079 on the getter 00624670's result) runs 0062B290 on this + 0x7D8,
     0062BA30 on this + 0x9C0, 0062B430 on this + 0x708 and 0062B4E0 on this + 0x760, releases +0x7B8 through its vtable
     slot +0x10, and frees +0x700 with 00618FD0 when bit 31 of +0x6F8 is clear. Its initialiser (00625CC0 on; r14 = this)
     calls 00607D10 on +0x520 / +0x548, 00624980(this + 0x7D8, this), 00624F70(this + 0x708, device, [+0xF4], [+0xF8]) and
     00625210(this + 0x760, device, [+0xFC], [+0x100])
  V  00624F70: +0x30 / +0x34 = the vertex / index byte sizes (0 means 0x400000 / 0x100000); two ID3D11Device::CreateBuffer
     (slot +0x18) per kind, DYNAMIC (2), CPU write (0x10000), bind 1 into +0 / +8 and bind 2 (size + 0x10) into +0x10 / +0x18;
     then 0017D260(size, 16) into +0x38 / +0x40 and (size + 0x10, 16) into +0x48 / +0x50. 0062B430 releases +0..+0x18 through
     slot +0x10 and frees +0x38..+0x50 with 00584730. Extent 0x58: this + 0x708 + 0x58 = + 0x760, the next object
  U  00625210 calls 006250C0 with usage 0, extra bind 0x80, CPU 0: the same header, bind 0x81 / 0x82, misc 0x20; then
     ID3D11Device::CreateUnorderedAccessView (slot +0x40), format 0x27 (R32_TYPELESS), dimension 1 (buffer), flags 1 (raw),
     into +0x38 / +0x48 (per buffer). 0062B4E0 releases +0x38..+0x50 and +0..+0x18. Extent 0x58, ending at + 0x7B8
  P  00624980(obj, context): one CreateBuffer (0x30000, DYNAMIC, bind 1, CPU write) into +0, +8 = 0; CreateVertexShader
     (slot +0x60) into +0x20; CreatePixelShader (slot +0x78) into +0x28 / +0x30 / +0x38; CreateInputLayout (slot +0x58) into
     +0x10; CreateBuffer (0x50 bytes, bind 4 = constant) into +0x18. 0062B290 releases +0, +0x10, +0x20..+0x38 and +0x18 and
     calls 0062BA30 on its own +0x58 - the PShaderPassStateD3D11 the context's constructor builds at +0x830 - so the object
     is 0x58 + 0x190 = 0x1E8 bytes and ends at the context's +0x9C0, where the next pass state begins
  R  the rest of the span: 005DBF30 on +0x520 / +0x548 (a 0x28-byte record: qwords +0 / +8, dword +0x10, qword +0x18,
     +0x20 = 02CF7A30); 00607D10 stores dword +0x18, dword +0x1C, qword +0x20; 00604B82 reads +0x18 / +0x1C of this + 0x520
     zero-extended into cvtsi2ss. 00808FE4(this + 0x570, 0x18, 8, 005DC1B0) - eight 0x18-byte records ({qword, qword,
     dword}). 005DC190(this + 0x630, 0, 0). 0061CE30 resizes the +0x700 array: count x 0x30 bytes, each built by 005DBFC0,
     count stored at +0x6F8. 00625408 stores 0.1, 0.1, 0.8, 0.5 at +0x7C0..+0x7CC; the constructor stores 1.0f at +0x7D0
  W  REGRESSION (FAILS before): the span's rows are in the store and the three new object types tile
Not claimed: what the two 0x28 records, the 0x18 records, the +0x630 object and the 0x30 array elements are; what the
+0x7C0 floats tune; the role of each shader.
Usage: python render_buffers.py [--patch]
"""
import hashlib, os, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def has(lo, hi, pairs):
    A = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)}
    miss = [hex(a) for a, v in pairs if A.get(a) != v]
    if miss: print("   missing", miss)
    return not miss
check("D", has(0x62B5A0, 0x62B7A1, [(0x62B61F, ("lea", "rcx, [rbx + 0x7d8]")), (0x62B626, ("call", "0x62b290")), (0x62B66B, ("lea", "rcx, [rbx + 0x9c0]")),
                                     (0x62B672, ("call", "0x62ba30")), (0x62B69C, ("lea", "rcx, [rbx + 0x708]")), (0x62B6A3, ("call", "0x62b430")),
                                     (0x62B6A8, ("lea", "rcx, [rbx + 0x760]")), (0x62B6AF, ("call", "0x62b4e0")), (0x62B6B4, ("mov", "edx, dword ptr [rbx + 0x6f8]")),
                                     (0x62B6BE, ("mov", "rcx, qword ptr [rbx + 0x700]")), (0x62B6D9, ("call", "0x618fd0")), (0x62B6EB, ("mov", "rcx, qword ptr [rbx + 0x7b8]")),
                                     (0x62B6FA, ("call", "qword ptr [rax + 0x10]"))])
      and has(0x79F065, 0x79F07E, [(0x79F068, ("call", "0x624670")), (0x79F076, ("mov", "rcx, rax")), (0x79F079, ("call", "0x62b5a0"))])
      and has(0x625CC0, 0x625DE0, [(0x625CFB, ("lea", "rcx, [r14 + 0x520]")), (0x625D0F, ("call", "0x607d10")), (0x625D14, ("lea", "rcx, [r14 + 0x548]")),
                                   (0x625D28, ("call", "0x607d10")), (0x625D2D, ("lea", "rcx, [r14 + 0x7d8]")), (0x625D34, ("mov", "rdx, r14")), (0x625D37, ("call", "0x624980")),
                                   (0x625D86, ("mov", "r9d, dword ptr [r14 + 0xf8]")), (0x625D8D, ("lea", "rcx, [r14 + 0x708]")), (0x625D94, ("mov", "r8d, dword ptr [r14 + 0xf4]")),
                                   (0x625DB0, ("call", "0x624f70")), (0x625DBD, ("mov", "r9d, dword ptr [r14 + 0x100]")), (0x625DC4, ("lea", "rcx, [r14 + 0x760]")),
                                   (0x625DCB, ("mov", "r8d, dword ptr [r14 + 0xfc]")), (0x625DD6, ("call", "0x625210"))]),
      "teardown 0062B5A0 and initialiser 00625CC0 hand the context's +0x520 / +0x548 / +0x708 / +0x760 / +0x7D8 to the objects' routines")
check("V", has(0x624F70, 0x6250BC, [(0x624F8F, ("mov", "eax, 0x400000")), (0x624F9C, ("cmove", "r8d, eax")), (0x624FA6, ("mov", "dword ptr [rcx + 0x30], r8d")),
                                     (0x624FAA, ("mov", "eax, 0x100000")), (0x624FB2, ("cmove", "r9d, eax")), (0x624FDE, ("mov", "dword ptr [rcx + 0x34], r9d")),
                                     (0x624FD6, ("mov", "dword ptr [r11 - 0x68], r8d")), (0x624FE2, ("mov", "dword ptr [rsp + 0x24], ebp")), (0x624FE6, ("mov", "dword ptr [rsp + 0x28], 1")),
                                     (0x624FEE, ("mov", "dword ptr [rsp + 0x2c], 0x10000")), (0x624FF6, ("mov", "dword ptr [rsp + 0x3c], ebp")), (0x624FFA, ("mov", "dword ptr [rsp + 0x40], ebp")),
                                     (0x62500F, ("lea", "r9, [rsi + rbx*8]")), (0x62501E, ("call", "qword ptr [r10 + 0x18]")), (0x625044, ("lea", "r9, [rsi + rax*8]")),
                                     (0x625067, ("mov", "ecx, dword ptr [rsi + 0x30]")), (0x62506F, ("call", "0x17d260")), (0x625074, ("mov", "qword ptr [rbx - 0x10], rax")),
                                     (0x62507E, ("mov", "ecx, dword ptr [rsi + 0x34]")), (0x625086, ("add", "ecx, 0x10")), (0x62508E, ("mov", "qword ptr [rbx], rax"))])
      and has(0x62B430, 0x62B4D9, [(0x62B44F, ("lea", "rdi, [rcx + 0x48]")), (0x62B460, ("mov", "rcx, qword ptr [rdi - 0x10]")), (0x62B469, ("call", "0x584730")),
                                   (0x62B47A, ("call", "0x584730")), (0x62B490, ("mov", "rcx, qword ptr [rbx]")), (0x62B49B, ("call", "qword ptr [rax + 0x10]")),
                                   (0x62B4A1, ("mov", "rcx, qword ptr [rbx + 0x10]")), (0x62B4B4, ("add", "rbx, 8"))]),
      "+0x708: two dynamic vertex and two index ID3D11Buffer, their sizes at +0x30 / +0x34 and 16-aligned CPU copies at +0x38..+0x50")
check("U", has(0x625210, 0x625256, [(0x625236, ("mov", "dword ptr [rsp + 0x30], edi")), (0x62523D, ("mov", "dword ptr [rsp + 0x28], 0x80")),
                                     (0x625245, ("mov", "dword ptr [rsp + 0x20], edi")), (0x625249, ("call", "0x6250c0"))])
      and has(0x6250C0, 0x6251FB, [(0x625106, ("mov", "dword ptr [rcx + 0x30], eax")), (0x62510D, ("mov", "dword ptr [rcx + 0x34], r10d")), (0x625111, ("mov", "r9d, 0x20")),
                                   (0x625125, ("or", "eax, 1")), (0x625168, ("or", "eax, 2")), (0x625199, ("lea", "r9, [r14 + rbx*8]")), (0x6251A8, ("call", "qword ptr [r10 + 0x18]")),
                                   (0x6251CB, ("lea", "r9, [r14 + rax*8]"))])
      and has(0x625256, 0x6253C6, [(0x6252C0, ("mov", "dword ptr [rbp - 0x19], 0x27")), (0x6252E5, ("lea", "r9, [r13 + 0x38]")), (0x6252F9, ("call", "qword ptr [r10 + 0x40]")),
                                   (0x625341, ("lea", "r9, [r13 + 0x48]")), (0x62536D, ("mov", "dword ptr [rbp - 0x19], 0x27")), (0x62537B, ("call", "qword ptr [r10 + 0x40]"))])
      and has(0x62B4E0, 0x62B599, [(0x62B4FF, ("lea", "rdi, [rcx + 0x38]")), (0x62B51B, ("call", "qword ptr [rax + 0x10]")), (0x62B52B, ("lea", "rdi, [rbx + 0x48]")),
                                   (0x62B53D, ("call", "qword ptr [rax + 0x10]")), (0x62B550, ("mov", "rcx, qword ptr [rbx]")), (0x62B561, ("mov", "rcx, qword ptr [rbx + 0x10]"))]),
      "+0x760: the same buffer header built GPU-writable (bind | 0x80, misc 0x20) and raw R32 UAVs at +0x38..+0x50")
check("P", has(0x624980, 0x624C29, [(0x6249A6, ("mov", "rsi, qword ptr [rdx + 0x108]")), (0x6249C7, ("mov", "dword ptr [rbp - 0x51], 0x30000")),
                                     (0x6249CE, ("mov", "dword ptr [rbp - 0x4d], 2")), (0x6249D5, ("mov", "dword ptr [rbp - 0x49], 1")), (0x6249FF, ("lea", "r9, [rdi + rax*8]")),
                                     (0x624A03, ("call", "qword ptr [r10 + 0x18]")), (0x624A11, ("cmp", "ebx, 1")), (0x624A16, ("mov", "dword ptr [rdi + 8], r15d")),
                                     (0x624A1A, ("lea", "rbx, [rdi + 0x20]")), (0x624A42, ("call", "qword ptr [r10 + 0x60]")), (0x624A5E, ("lea", "rbx, [rdi + 0x28]")),
                                     (0x624A7F, ("call", "qword ptr [r10 + 0x78]")), (0x624A9B, ("lea", "rbx, [rdi + 0x30]")), (0x624AD8, ("lea", "rbx, [rdi + 0x38]")),
                                     (0x624AF9, ("call", "qword ptr [r10 + 0x78]")), (0x624B22, ("lea", "rbx, [rdi + 0x10]")), (0x624B9F, ("call", "qword ptr [r10 + 0x58]")),
                                     (0x624BB3, ("lea", "r9, [rdi + 0x18]")), (0x624BB7, ("mov", "qword ptr [rbp - 0x69], 0x50")), (0x624BC3, ("mov", "qword ptr [rbp - 0x61], 4")),
                                     (0x624BD5, ("call", "qword ptr [rax + 0x18]"))])
      and has(0x62B290, 0x62B338, [(0x62B29D, ("add", "rcx, 0x58")), (0x62B2A1, ("call", "0x62ba30")), (0x62B2A6, ("mov", "rcx, qword ptr [rbx]")),
                                   (0x62B2B9, ("mov", "rcx, qword ptr [rbx + 0x10]")), (0x62B2CC, ("mov", "rcx, qword ptr [rbx + 0x20]")), (0x62B2DF, ("mov", "rcx, qword ptr [rbx + 0x28]")),
                                   (0x62B2F2, ("mov", "rcx, qword ptr [rbx + 0x30]")), (0x62B305, ("mov", "rcx, qword ptr [rbx + 0x38]")), (0x62B318, ("mov", "rcx, qword ptr [rbx + 0x18]"))])
      and has(0x6CAFC0, 0x6CB000, [(0x6CAFD4, ("call", "0x62ba30"))]),
      "+0x7D8: vertex buffer, input layout, constant buffer, a vertex and three pixel shaders; its release also releases its +0x58 pass state (0062BA30, the pass-state release the renderer uses)")
check("R", has(0x5DBF30, 0x5DBF4F, [(0x5DBF32, ("mov", "qword ptr [rcx], rax")), (0x5DBF35, ("mov", "qword ptr [rcx + 8], rax")), (0x5DBF39, ("mov", "dword ptr [rcx + 0x10], eax")),
                                     (0x5DBF3C, ("mov", "qword ptr [rcx + 0x18], rax")), (0x5DBF40, ("lea", "rax, [rip + 0x271bae9]")), (0x5DBF47, ("mov", "qword ptr [rcx + 0x20], rax"))])
      and has(0x607D10, 0x607D1C, [(0x607D10, ("mov", "dword ptr [rcx + 0x18], edx")), (0x607D13, ("mov", "dword ptr [rcx + 0x1c], r8d")), (0x607D17, ("mov", "qword ptr [rcx + 0x20], r9"))])
      and has(0x604B82, 0x604BB5, [(0x604B87, ("lea", "rcx, [rax + 0x520]")), (0x604B93, ("mov", "eax, dword ptr [rcx + 0x18]")), (0x604B99, ("cvtsi2ss", "xmm0, rax")),
                                   (0x604BA4, ("mov", "eax, dword ptr [rcx + 0x1c]"))])
      and has(0x615939, 0x6159A2, [(0x615939, ("lea", "rcx, [rbp + 0x520]")), (0x615940, ("call", "0x5dbf30")), (0x615946, ("lea", "rcx, [rbp + 0x548]")),
                                   (0x615953, ("lea", "rbx, [rbp + 0x570]")), (0x61595F, ("lea", "rax, [rip - 0x4a82c6]")), (0x615972, ("lea", "edx, [r14 + 0x18]")),
                                   (0x615976, ("lea", "r8d, [r14 + 8]")), (0x61597D, ("call", "0x808fe4")), (0x615983, ("lea", "rcx, [rbx + 0xc0]")), (0x61598F, ("call", "0x5dc190"))])
      and has(0x5DC1B0, 0x5DC1C0, [(0x5DC1B2, ("mov", "qword ptr [rcx], rax")), (0x5DC1B5, ("mov", "qword ptr [rcx + 8], rax")), (0x5DC1B9, ("mov", "dword ptr [rcx + 0x10], eax"))])
      and has(0x61CE30, 0x61CEEE, [(0x61CE4B, ("cmp", "edx, dword ptr [rcx + 0x6f8]")), (0x61CE5F, ("lea", "rcx, [rdi + rdi*2]")), (0x61CE63, ("shl", "rcx, 4")),
                                   (0x61CEA4, ("call", "0x5dbfc0")), (0x61CEE0, ("mov", "qword ptr [rsi + 0x700], rbp")), (0x61CEE7, ("mov", "dword ptr [rsi + 0x6f8], edi"))])
      and has(0x625408, 0x625473, [(0x62543A, ("mov", "dword ptr [rbx + 0x7c0], 0x3dcccccd")), (0x625446, ("mov", "dword ptr [rbx + 0x7c4], 0x3dcccccd")),
                                   (0x625450, ("mov", "dword ptr [rbx + 0x7c8], 0x3f4ccccd")), (0x625469, ("mov", "dword ptr [rbx + 0x7cc], 0x3f000000"))])
      and has(0x615A58, 0x615A63, [(0x615A58, ("mov", "qword ptr [rbp + 0x7d0], 0x3f800000"))])
      and 0x5DBF47 + 0x271BAE9 == 0x2CF7A30 and has(0x61596B, 0x615972, [(0x61596B, ("lea", "r9, [rip - 0x397c2]"))]) and 0x615972 - 0x397C2 == 0x5DC1B0,
      "0x28 records at +0x520 / +0x548, 8 x 0x18 at +0x570, 005DC190 at +0x630, the 0x30-record array at +0x6F8 / +0x700, floats at +0x7C0..+0x7D0")

REC = "_index/candidates/render-context-02cc0410/render_buffers.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RC, PS = "RenderContext02CC0410", "PShaderPassStateD3D11"
T28, T18, TDB, TUB, TPP = "RenderContextRecord28", "RenderContextRecord18", "RenderDynamicBuffers58", "RenderUavBuffers58", "RenderPrimitivePass1E8"
P, U, M = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN"), ("TYPE RESOLVED", "PROBABLE")
def ev(tag, was): return "CARVED 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def r(t, o, sz, nm, ct, mean, rd, tag, was="-", w=4): return [t, ("0x%0" + str(w) + "X") % o, str(sz), nm, ct, mean, rd[0], rd[1], ev(tag, was)]
def ctx(w):
    return [r(RC, 0x520, 0x28, "record520", T28, "a 0x28-byte record built by 005DBF30; the initialiser sets its +0x18 / +0x1C / +0x20 with 00607D10, and 00604B82 reads +0x18 / +0x1C as a pair of unsigned ints it converts to float", M, "D R", w),
            r(RC, 0x548, 0x28, "record548", T28, "a second 0x28-byte record, built and set the same way", M, "D R", w),
            r(RC, 0x570, 0xC0, "records570", T18 + "[8]", "eight 0x18-byte records built by the vector constructor iterator 00808FE4 with 005DC1B0", M, "R", w),
            r(RC, 0x630, 20, "header630", "u8[20]", "the fields 005DC190 writes when the constructor calls it with (0, 0): qword +0 = the pointer argument, dword +8 = 0, dword +0xC = the count argument, dword +0x10 = 0; its object's extent is not fixed", U, "R", w),
            r(RC, 0x644, 68, "unobservedSpan0644", "u8[68]", "not written by the constructor; no reader found by the getter censuses", U, "R", w),
            r(RC, 0x688, 8, "qword688", "uint64", "zeroed by the constructor (rbx + 0x118 with rbx = this + 0x570); no reader found", U, "R", w),
            r(RC, 0x690, 64, "unobservedSpan0690", "u8[64]", "not written by the constructor; no reader found by the getter censuses", U, "R", w),
            r(RC, 0x6D0, 8, "qword6D0", "uint64", "zeroed by the constructor (rbx + 0x160); no reader found", U, "R", w),
            r(RC, 0x6D8, 24, "unobservedSpan06D8", "u8[24]", "not written by the constructor; no reader found by the getter censuses", U, "R", w),
            r(RC, 0x6F0, 4, "dword6F0", "uint32", "zeroed by the constructor; no reader found", U, "R", w),
            r(RC, 0x6F4, 4, "unobservedSpan06F4", "u8[4]", "not written by the constructor; no reader found", U, "R", w),
            r(RC, 0x6F8, 4, "record30Count", "uint32", "the element count of the +0x700 array (0061CE30 stores it after a resize); bit 31 set means the array is not owned - the teardown and 0061CE30 free it with 00618FD0 only when bit 31 is clear", P, "D R", w),
            r(RC, 0x6FC, 4, "unobservedSpan06FC", "u8[4]", "alignment before the pointer; not written", U, "R", w),
            r(RC, 0x700, 8, "records30", "void*", "an array of record30Count 0x30-byte records, allocated 8-aligned by 0061CE30 and built one by one with 005DBFC0", P, "D R", w),
            r(RC, 0x708, 0x58, "dynamicBuffers708", TDB, "the dynamic vertex / index buffers 00624F70 creates with the sizes at +0xF4 / +0xF8; 0062B430 releases them", P, "D V", w),
            r(RC, 0x760, 0x58, "uavBuffers760", TUB, "the GPU-writable vertex / index buffers and their raw UAVs 00625210 creates with the sizes at +0xFC / +0x100; 0062B4E0 releases them", P, "D U", w),
            r(RC, 0x7B8, 8, "com7B8", "void*", "a COM object the teardown releases through its vtable slot +0x10 (0062B6EB); its creator is not read here", M, "D", w),
            r(RC, 0x7C0, 16, "tuning7C0", "float[4]", "0.1, 0.1, 0.8, 0.5, stored by 00625408; what they tune is not claimed", P, "R", w),
            r(RC, 0x7D0, 4, "scale7D0", "float", "1.0, stored by the constructor (a qword store whose high half zeroes +0x7D4)", P, "R", w),
            r(RC, 0x7D4, 4, "unobservedSpan07D4", "u8[4]", "zeroed with +0x7D0; no reader found", U, "R", w),
            r(RC, 0x7D8, 0x1E8, "primitivePass7D8", TPP, "the draw resources 00624980 creates - vertex buffer, input layout, constant buffer, a vertex and three pixel shaders - and the PShaderPassStateD3D11 at its +0x58, which its release 0062B290 releases with them", P, "D P", w)]
SIZES = [r(RC, 0xF4, 4, "dynamicVertexBytes", "uint32", "the byte size 00625CC0 passes to 00624F70 for the +0x708 vertex buffers (0 means 0x400000)", P, "D V"),
         r(RC, 0xF8, 4, "dynamicIndexBytes", "uint32", "the byte size passed for the +0x708 index buffers (0 means 0x100000; the buffer is 0x10 larger)", P, "D V"),
         r(RC, 0xFC, 4, "uavVertexBytes", "uint32", "the byte size 00625CC0 passes to 00625210 for the +0x760 vertex buffers (0 means 0x400000)", P, "D U"),
         r(RC, 0x100, 4, "uavIndexBytes", "uint32", "the byte size passed for the +0x760 index buffers (0 means 0x100000)", P, "D U")]
def buf_header(t, cpu, tail):
    return [r(t, 0x00, 16, "vertexBuffers", "void*[2]", "two ID3D11Buffer (bind 1 = vertex), created by ID3D11Device::CreateBuffer", P, cpu),
            r(t, 0x10, 16, "indexBuffers", "void*[2]", "two ID3D11Buffer (bind 2 = index), size + 0x10", P, cpu),
            r(t, 0x20, 16, "unobservedSpan20", "u8[16]", "not written by the creator or the release", U, cpu),
            r(t, 0x30, 4, "vertexBytes", "uint32", "the vertex buffers' byte size (0 in the argument means 0x400000)", P, cpu),
            r(t, 0x34, 4, "indexBytes", "uint32", "the index buffers' byte size (0 means 0x100000)", P, cpu)] + tail
DBROWS = buf_header(TDB, "V", [r(TDB, 0x38, 16, "vertexShadow", "void*[2]", "16-aligned CPU copies of the vertex buffers (0017D260(vertexBytes, 16)); freed with 00584730", P, "V"),
                               r(TDB, 0x48, 16, "indexShadow", "void*[2]", "16-aligned CPU copies of the index buffers (indexBytes + 0x10); freed with 00584730", P, "V")])
UBROWS = buf_header(TUB, "U", [r(TUB, 0x38, 16, "vertexUavs", "void*[2]", "ID3D11UnorderedAccessView, raw R32_TYPELESS buffer views of the vertex buffers", P, "U"),
                               r(TUB, 0x48, 16, "indexUavs", "void*[2]", "raw R32_TYPELESS buffer views of the index buffers", P, "U")])
PPROWS = [r(TPP, 0x00, 8, "vertexBuffer", "void*", "an ID3D11Buffer, 0x30000 bytes, dynamic vertex, CPU write", P, "P"),
          r(TPP, 0x08, 4, "vertexCursor", "uint32", "zeroed after the buffer is created", M, "P"),
          r(TPP, 0x0C, 4, "unobservedSpan0C", "u8[4]", "not written by the creator", U, "P"),
          r(TPP, 0x10, 8, "inputLayout", "void*", "an ID3D11InputLayout (CreateInputLayout, device slot +0x58)", P, "P"),
          r(TPP, 0x18, 8, "constantBuffer", "void*", "an ID3D11Buffer, 0x50 bytes, bind 4 (constant); named through 0061C550", P, "P"),
          r(TPP, 0x20, 8, "vertexShader", "void*", "an ID3D11VertexShader (device slot +0x60)", P, "P"),
          r(TPP, 0x28, 24, "pixelShaders", "void*[3]", "three ID3D11PixelShader (device slot +0x78)", P, "P"),
          r(TPP, 0x40, 24, "unobservedSpan40", "u8[24]", "zeroed by the context's constructor (+0x818..+0x82F); not written by the creator", U, "P"),
          r(TPP, 0x58, 0x190, "passState", PS, "the PShaderPassStateD3D11 the context's constructor builds at +0x830; released by this object's release 0062B290", P, "P")]
R18 = [r(T18, 0x00, 16, "unobservedSpan00", "u8[16]", "two qwords 005DC1B0 zeroes; no reader found", U, "R"),
       r(T18, 0x10, 4, "dword10", "uint32", "zeroed by 005DC1B0; no reader found", U, "R"),
       r(T18, 0x14, 4, "unobservedSpan14", "u8[4]", "padding to the 0x18 stride", U, "R")]
R28 = [r(T28, 0x00, 16, "unobservedSpan00", "u8[16]", "two qwords 005DBF30 zeroes; no reader found", U, "R"),
       r(T28, 0x10, 4, "dword10", "uint32", "zeroed by 005DBF30; no reader found", U, "R"),
       r(T28, 0x14, 4, "unobservedSpan14", "u8[4]", "not written", U, "R"),
       r(T28, 0x18, 4, "valueA", "uint32", "set by 00607D10 (edx); 00604B82 reads it zero-extended and converts it to float, paired with valueB", P, "R"),
       r(T28, 0x1C, 4, "valueB", "uint32", "set by 00607D10 (r8d); read with valueA", P, "R"),
       r(T28, 0x20, 8, "ptr20", "void*", "005DBF30 defaults it to 02CF7A30; 00607D10 sets it from r9 (the initialiser passes a static address per record)", P, "R")]
def trow(name, size, inst, ctor, doc, route):
    return [name, size, "17-Presentation-Rendering", inst, "EMBEDDED in RenderContext02CC0410", ctor, "not read here", P[0], P[1], "L1",
            "CARVED 2026-09-28 (OPUS, %s). %s" % (REC, EXE), doc, route]
DOC = "17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md"
NEWT = [trow(T28, "0x28", "two at RenderContext02CC0410 +0x520 / +0x548", "005DBF30", DOC, "EMBED RenderContext02CC0410 +0x0520"),
        trow(T18, "0x18", "eight at RenderContext02CC0410 +0x570", "005DC1B0", DOC, "EMBED RenderContext02CC0410 +0x0570"),
        trow(TDB, "0x58", "one at RenderContext02CC0410 +0x708", "00624F70 (creates; no constructor - the context's constructor zeroes it)", DOC, "EMBED RenderContext02CC0410 +0x0708"),
        trow(TUB, "0x58", "one at RenderContext02CC0410 +0x760", "006250C0 via 00625210 (creates)", DOC, "EMBED RenderContext02CC0410 +0x0760"),
        trow(TPP, "0x1E8", "one at RenderContext02CC0410 +0x7D8", "00624980 (creates); the pass state by 00615ED0", DOC, "EMBED RenderContext02CC0410 +0x07D8")]
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); eol = fl[1][len(fl[1].rstrip("\r\n")):]; out = []; done = False
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == RC and c[1] == "0x0520" and c[2] == "784":
            out += ["\t".join(x) + e for x in ctx("%s %s (%s)" % (c[3], c[4], c[5][:200]))]; done = True; continue
        if c[0] == RC and c[1] == "0x0830" and c[3] == "passState830":
            continue                                                     # now RenderPrimitivePass1E8 +0x58
        if c[0] == RC and c[1] == "0x0000" and c[2] == "264":
            was = "%s %s (%s)" % (c[3], c[4], c[5][:160])
            out.append("\t".join([c[0], c[1], "244", c[3], "u8[244]", c[5], c[6], c[7], c[8] + " || SPLIT 2026-09-28 (OPUS, %s D V U): +0xF4..+0x103 are the four buffer sizes" % REC]) + e)
            out += ["\t".join(x[:8] + [ev(x[8].split("(OPUS, %s " % REC)[1].split(")")[0], was)]) + e for x in SIZES]
            out.append("\t".join(r(RC, 0x104, 4, "unobservedSpan0104", "u8[4]", c[5], U, "D", was)) + e); continue
        out.append(l)
    assert done
    for t, rows in ((T28, R28), (T18, R18), (TDB, DBROWS), (TUB, UBROWS), (TPP, PPROWS)):
        if not any(cells(l)[0] == t for l in out):
            idx = max(i for i, l in enumerate(out) if cells(l)[0] == RC); out[idx + 1:idx + 1] = ["\t".join(x) + eol for x in rows]
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    for row in reversed(NEWT):
        if not any(cells(l)[0] == row[0] for l in tl):
            ti = max(i for i, l in enumerate(tl) if cells(l)[0] == RC); tl[ti + 1:ti + 1] = ["\t".join(row) + te]
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
R = {int(c[1], 16): c for c in F if c[0] == RC}
tiles = all(t in T and sum(int(c[2]) for c in F if c[0] == t) == int(T[t][1], 16) for t in (T28, T18, TDB, TUB, TPP))
check("W", tiles and R.get(0x7D8, [""] * 5)[3:5] == ["primitivePass7D8", TPP] and 0x830 not in R and R.get(0x708, [""] * 5)[4] == TDB
      and R.get(0x760, [""] * 5)[4] == TUB and R.get(0xF4, [""] * 5)[3] == "dynamicVertexBytes" and 0x520 in R and R[0x520][4] == T28,
      "the span's rows are in the store; the five new types tile; the pass state at +0x830 is the +0x7D8 object's +0x58")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
