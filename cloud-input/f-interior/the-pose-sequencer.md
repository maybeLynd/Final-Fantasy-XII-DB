# F-interior pack: `17-Presentation-Rendering/Model-And-Motion-Formats/the-pose-sequencer.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-pose-sequencer.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 00477670 (92 B, extent 00477670-004776CC)

Page context: "93d5d1d89721f8   method: the three render-record accessors of FCP section 7 (003E6F50, 003E7450, 003E6A20) and the four sequencer     bodies they reach (00477370 start, 00477480 step, 004776D0 value, 00477670 reset) disassembled from the authority     image and read whole, 2026-09-19; the one consumer of the value, inside the add-motion pose applier, read over the     window 00371F2E..00371FD4 only; the section format the code implies t"

```
00477670  lea      rax, [rip + 0x282f629]  ; -> 02CA6CA0
00477677  movzx    r9d, cl
0047767B  shl      r9, 6
0047767F  add      r9, rax
00477682  xor      eax, eax
00477684  cmp      dword ptr [r9 + 4], ecx
00477688  cmovne   r9, rax
0047768C  test     r9, r9
0047768F  je       0x4776cb  ; -> 004776CB
00477691  mov      eax, edx
00477693  movzx    edx, word ptr [r8 + rax*2]
00477698  mov      eax, dword ptr [r9 + 0xc]
0047769C  add      edx, r8d
0047769F  lea      rcx, [rax + rax*2]
004776A3  movzx    eax, byte ptr [rdx + rcx*2]
004776A7  mov      byte ptr [rax + r9 + 0x10], 0
004776AD  movzx    eax, byte ptr [rdx + rcx*2]
004776B1  mov      byte ptr [rax + r9 + 0x18], 0
004776B7  movzx    eax, byte ptr [rdx + rcx*2]
004776BB  mov      byte ptr [rax + r9 + 0x20], 0xff
004776C1  movzx    eax, byte ptr [rdx + rcx*2]
004776C5  mov      byte ptr [rax + r9 + 0x28], 0xff
004776CB  ret      
```

## 00504800 (59 B, extent 00504800-0050483B)

Page context: "ion 4: the applier window | **survives**: kind 1; '+0x1E4' / '+0x1E8'; the id search over '0x28'-stride groups | | Q7 | section 4: the draw side | **survives**: count × 128. '00477E90' tail-jumps to '00504800', which returns 'width << 16 \| height' from the '+0x100' table. The source x / y are indexed by value | | Q8 | section 4b: commands '0x1D' / '0x1E' | **survives**: all four arms and the '+0x413 + 1' filter | | Q9 | section 4b: the"

```
00504800  sub      rsp, 0x28
00504804  movsxd   rax, edx
00504807  movzx    ecx, word ptr [rcx + rax*2 + 0x100]
0050480F  call     0x5212e0  ; -> 005212E0 fn
00504814  mov      rcx, rax
00504817  test     rax, rax
0050481A  je       0x504834  ; -> 00504834
0050481C  test     byte ptr [rax + 0x1c], 1
00504820  je       0x504834  ; -> 00504834
00504822  movzx    eax, word ptr [rax + 0x1e]
00504826  movzx    ecx, word ptr [rcx + 0x20]
0050482A  shl      eax, 0x10
0050482D  or       eax, ecx
0050482F  add      rsp, 0x28
00504833  ret      
00504834  xor      eax, eax
00504836  add      rsp, 0x28
0050483A  ret      
```
