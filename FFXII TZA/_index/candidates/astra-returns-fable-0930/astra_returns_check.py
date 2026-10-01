"""astra_returns_check.py - FABLE, 2026-09-30: one image check per consumed ASTRA return (read-only, shipping EXE).
Checks (FAILS n):
 F1 FST domain: 0032E620 rejects a negative EDX (0032E64A test / jns, 0032E64E or eax,-1); 002DF960 is
    kind*5000 + movsxd(index) with an unchecked dword load (no cmp in the body); 0032FCA0 sizes the full index
    (0032FD94 movsxd rdx / 0032FD99 call 0032E400) and a negative size (0032FED2 jl 0032FF25) clears the directory
    header byte (0032FF2D mov byte [rax],0).
 F2 override domain: 001CCC06 stores QWORD 0x2710 at +0xADC (high dword = +0xAE0 = 0); 002F79E0 copies 00D0F9E0 ->
    022BE930 and the eight u16 words are 241,231,234,237,229,228,227,226 (none in 511..534); 002F7A00 is the only
    rip writer of 01EEBAF0 and 002F8D66 its reader, followed by js.
 F3 override labels: 001CE9AA movsxd [r15+0xae0], shl 5, lea [r15+0xae4] (32-byte label slots, no clamp between).
 F4 title member notification: 00249274 forms 002495C0 (the only rip reference to it); 002495C0 increments +0x1A at
    002495ED and calls the owner at 00249632, then clears ticket bit 0 (00249634) and member bit 0 (00249637).
 F5 title retirement guards: 0024A680 is 141 B; membership base 0208F580, stride 0x48, bound 0x40; the tail clears
    [rbx+0x38] bit 0x20 (0024A6F8) and decrements 02090780 (0024A6FC); no store to [rbx+0x10] / [rbx+0x18].
Control: 02090780 has exactly two rip references - the allocator's inc (0024A58A) and the decrement (0024A6FC)."""
import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "takebacks"))
import tk
fails = 0
def check(n, ok, why=""):
    global fails
    print(n, "PASS" if ok else "FAIL " + why); fails += 0 if ok else 1
def body(e): return {x.address: x for x in tk.fdis(e)}
def rip(x):
    for o in x.operands:
        if o.type == 3 and o.mem.base == 41: return x.address + x.size + o.mem.disp   # X86_REG_RIP = 41
    return None
def ins(b, a): x = b.get(a); return (x.mnemonic + " " + x.op_str) if x else None

R = body(0x0032E620); L = body(0x002DF960); P = body(0x0032FCA0)
check("F1 negative reject", ins(R, 0x0032E64A) == "test edx, edx" and ins(R, 0x0032E64C).startswith("jns")
      and ins(R, 0x0032E64E) == "or eax, 0xffffffff", str((ins(R, 0x0032E64A), ins(R, 0x0032E64E))))
check("F1 flat lookup unchecked", ins(L, 0x002DF963) == "imul r8, rax, 0x1388" and ins(L, 0x002DF96A) == "movsxd rcx, edx"
      and ins(L, 0x002DF977) == "mov eax, dword ptr [rax + r8*4]" and not any(x.mnemonic == "cmp" for x in L.values()))
check("F1 full-index size + header clear", ins(P, 0x0032FD94).startswith("movsxd rdx") and ins(P, 0x0032FD99) == "call 0x32e400"
      and ins(P, 0x0032FED2) == "jl 0x32ff25" and ins(P, 0x0032FF2D) == "mov byte ptr [rax], 0",
      str((ins(P, 0x0032FD94), ins(P, 0x0032FD99), ins(P, 0x0032FF2D))))

C = body(0x001CCB20); I = body(0x002F79E0); S = body(0x002F7A00); M = body(0x002F8D60)
words = [struct.unpack_from("<H", tk.d, tk.off(0x00D0F9E0) + 2 * i)[0] for i in range(8)]
check("F2 ctor qword 0x2710 at +0xADC", ins(C, 0x001CCC06) == "mov qword ptr [rdi + 0xadc], 0x2710")
check("F2 initializer copy + words", rip(I[0x002F79E0]) == 0x00D0F9E0 and rip(I[0x002F79E8]) == 0x022BE930
      and words == [241, 231, 234, 237, 229, 228, 227, 226] and not any(511 <= w <= 534 for w in words), str(words))
w_refs = tk.rip_refs(0x01EEBAF0, 0x01EEBAF4)[0]
writers = sorted(x.address for x, k, t in w_refs if tk.is_store(x, k))
check("F2 index writer/reader", writers == [0x002F7A00] and rip(M[0x002F8D66]) == 0x01EEBAF0
      and ins(M, 0x002F8D72).startswith("js"), str([hex(a) for a in writers]))

F = body(0x001CD0E0)
check("F3 label slot arithmetic", ins(F, 0x001CE9AA) == "movsxd rax, dword ptr [r15 + 0xae0]" and ins(F, 0x001CE9B1) == "shl rax, 5"
      and ins(F, 0x001CE9B5) == "lea rcx, [r15 + 0xae4]")

N = body(0x00249210); Q = body(0x002495C0)
d_refs = tk.rip_refs(0x002495C0, 0x002495C1)[0]
check("F4 descriptor formed once", rip(N[0x00249274]) == 0x002495C0 and [x.address for x, k, t in d_refs] == [0x00249274],
      str([hex(x.address) for x, k, t in d_refs]))
check("F4 done count then owner call", ins(Q, 0x002495ED) == "inc word ptr [rdi + 0x1a]" and ins(Q, 0x00249632) == "call rax"
      and ins(Q, 0x00249634) == "and dword ptr [rdi], 0xfffffffe" and ins(Q, 0x00249637) == "and dword ptr [rbx + 0x20], 0xfffffffe")

G = body(0x0024A680)
stores = [x for x in G.values() for k in range(len(x.operands)) if tk.is_store(x, k)]
ptr_clear = [hex(x.address) for x in stores if "[rbx + 0x10]" in x.op_str or "[rbx + 0x18]" in x.op_str]
check("F5 body size / membership", tk.fsize(0x0024A680) == 141 and rip(G[0x0024A695]) == 0x0208F580
      and ins(G, 0x0024A6A7) == "add rax, 0x48" and 0x0208F580 + 64 * 0x48 == 0x02090780)
check("F5 local effects", ins(G, 0x0024A6F8) == "and dword ptr [rbx + 0x38], 0xffffffdf" and rip(G[0x0024A6FC]) == 0x02090780
      and G[0x0024A6FC].mnemonic == "dec" and not ptr_clear
      and 0x0024A6F8 in [x.address for x in stores], str(ptr_clear))   # the store census must see the 0x38 AND

c_refs = sorted((x.address, x.mnemonic) for x, k, t in tk.rip_refs(0x02090780, 0x02090784)[0])
check("control counter refs", c_refs == [(0x0024A58A, "inc"), (0x0024A6FC, "dec")], str(c_refs))
print("FAILS", fails)
