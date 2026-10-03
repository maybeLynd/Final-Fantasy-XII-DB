# F homing pack: `18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md`

Generated 2026-10-02 22:28 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 003C9A30 (966 B, extent 003C9A30-003C9DF6)

Documented callee on this page: `003C9950`

```
003C9A30  mov      qword ptr [rsp + 8], rbx
003C9A35  mov      qword ptr [rsp + 0x10], rsi
003C9A3A  push     rdi
003C9A3B  sub      rsp, 0x20
003C9A3F  mov      eax, dword ptr [rdx]
003C9A41  mov      rbx, rcx
003C9A44  dec      eax
003C9A46  cmp      eax, 0x12
003C9A49  ja       0x3c9de2  ; -> 003C9DE2
003C9A4F  cdqe     
003C9A51  lea      rsi, [rip - 0x2a9a58]  ; -> 00120000 (image base)
003C9A58  mov      eax, dword ptr [rsi + rax*4 + 0x2a9df8]  ; image base + 0x2a9df8 = 003C9DF8
003C9A5F  add      rax, rsi
003C9A62  jmp      rax
003C9A64  mov      rax, qword ptr [rip + 0x1cd11c5]  ; -> 0209AC30
003C9A6B  add      rcx, 0x50
003C9A6F  mov      r9, rbx
003C9A72  mov      r8d, 3
003C9A78  mov      rdx, qword ptr [rax + 0x10]
003C9A7C  call     0x2432b0  ; -> 002432B0 fn
003C9A81  xor      edi, edi
003C9A83  movzx    ecx, word ptr [rax + 0xa]
003C9A87  movzx    edx, word ptr [rax + 8]
003C9A8B  movsx    r8d, word ptr [rax + 6]
003C9A90  test     rbx, rbx
003C9A93  je       0x3c9abf  ; -> 003C9ABF
003C9A95  movzx    eax, word ptr [rax + 4]
003C9A99  mov      word ptr [rbx + 0x98], ax
003C9AA0  mov      rax, qword ptr [rbx + 0x60]
003C9AA4  mov      word ptr [rbx + 0x9a], r8w
003C9AAC  mov      word ptr [rbx + 0x9c], dx
003C9AB3  mov      word ptr [rbx + 0x9e], cx
003C9ABA  mov      rcx, qword ptr [rax]
003C9ABD  jmp      0x3c9ac2  ; -> 003C9AC2
003C9ABF  mov      rcx, rdi
003C9AC2  and      dword ptr [rcx + 8], 0xfffffffe
003C9AC6  mov      edx, 0xd1
003C9ACB  mov      rcx, rbx
003C9ACE  call     0x247930  ; -> 00247930 fn
003C9AD3  mov      edx, 2
003C9AD8  mov      rcx, rbx
003C9ADB  call     0x394700  ; -> 00394700 fn
003C9AE0  xor      r8d, r8d
003C9AE3  mov      qword ptr [rip + 0x277dc56], rbx  ; -> 02B47740
003C9AEA  lea      rdx, [rip - 0x531]  ; -> 003C95C0
003C9AF1  mov      word ptr [rbx + 0xc0], 0x707
003C9AFA  mov      ecx, 0xc8
003C9AFF  mov      dword ptr [rbx + 0xc4], edi
003C9B05  mov      qword ptr [rbx + 0xd0], rdi
003C9B0C  call     0x244f50  ; -> 00244F50 fn
003C9B11  mov      qword ptr [rbx + 0xc8], rax
003C9B18  xor      eax, eax
003C9B1A  mov      rbx, qword ptr [rsp + 0x30]
003C9B1F  mov      rsi, qword ptr [rsp + 0x38]
003C9B24  add      rsp, 0x20
003C9B28  pop      rdi
003C9B29  ret      
003C9B2A  and      dword ptr [rcx + 0xc4], 0xfffffff7
003C9B31  xor      eax, eax
003C9B33  mov      rbx, qword ptr [rsp + 0x30]
003C9B38  mov      rsi, qword ptr [rsp + 0x38]
003C9B3D  add      rsp, 0x20
003C9B41  pop      rdi
003C9B42  ret      
003C9B43  call     0x31a8e0  ; -> 0031A8E0 fn
003C9B48  xor      edi, edi
003C9B4A  mov      ecx, edi
003C9B4C  nop      dword ptr [rax]
003C9B50  movzx    ecx, word ptr [rsi + rcx*2 + 0xbf1710]  ; image base + 0xbf1710 = 00D11710
003C9B58  test     eax, ecx
003C9B5A  jne      0x3c9b6a  ; -> 003C9B6A
003C9B5C  inc      edi
003C9B5E  movsxd   rcx, edi
003C9B61  cmp      rcx, 7
003C9B65  jb       0x3c9b50  ; -> 003C9B50
003C9B67  mov      dil, 7
003C9B6A  mov      rcx, rbx
003C9B6D  call     0x3c9840  ; -> 003C9840 fn
003C9B72  test     byte ptr [rbx + 0xc4], 2
003C9B79  je       0x3c9dd0  ; -> 003C9DD0
003C9B7F  mov      rax, qword ptr [rbx + 0xc8]
003C9B86  test     rax, rax
003C9B89  je       0x3c9b94  ; -> 003C9B94
003C9B8B  movzx    ecx, byte ptr [rax + 0xc0]
003C9B92  jmp      0x3c9b96  ; -> 003C9B96
003C9B94  mov      cl, 7
003C9B96  cmp      dil, 7
003C9B9A  je       0x3c9ba5  ; -> 003C9BA5
003C9B9C  cmp      dil, cl
003C9B9F  je       0x3c9dd0  ; -> 003C9DD0
003C9BA5  mov      rcx, rbx
003C9BA8  call     0x3c98a0  ; -> 003C98A0 fn
003C9BAD  xor      eax, eax
003C9BAF  mov      rbx, qword ptr [rsp + 0x30]
003C9BB4  mov      rsi, qword ptr [rsp + 0x38]
003C9BB9  add      rsp, 0x20
003C9BBD  pop      rdi
003C9BBE  ret      
003C9BBF  or       dword ptr [rcx + 0xc4], 1
003C9BC6  xor      eax, eax
003C9BC8  mov      rbx, qword ptr [rsp + 0x30]
003C9BCD  mov      rsi, qword ptr [rsp + 0x38]
003C9BD2  add      rsp, 0x20
003C9BD6  pop      rdi
003C9BD7  ret      
003C9BD8  call     0x31a8e0  ; -> 0031A8E0 fn
003C9BDD  xor      edi, edi
003C9BDF  mov      edx, edi
003C9BE1  mov      ecx, edi
003C9BE3  movzx    ecx, word ptr [rsi + rcx*2 + 0xbf1710]  ; image base + 0xbf1710 = 00D11710
003C9BEB  test     eax, ecx
003C9BED  jne      0x3c9bfc  ; -> 003C9BFC
003C9BEF  inc      edx
003C9BF1  movsxd   rcx, edx
003C9BF4  cmp      rcx, 7
003C9BF8  jb       0x3c9be3  ; -> 003C9BE3
003C9BFA  mov      dl, 7
003C9BFC  mov      eax, dword ptr [rbx + 0xc4]
003C9C02  mov      byte ptr [rbx + 0xc0], dl
003C9C08  test     al, 4
003C9C0A  je       0x3c9cd6  ; -> 003C9CD6
003C9C10  test     al, 8
003C9C12  jne      0x3c9dd0  ; -> 003C9DD0
003C9C18  mov      rcx, qword ptr [rbx + 0xc8]
003C9C1F  test     rcx, rcx
003C9C22  je       0x3c9c33  ; -> 003C9C33
003C9C24  movzx    eax, byte ptr [rcx + 0xc1]
003C9C2B  test     al, al
003C9C2D  jne      0x3c9dd0  ; -> 003C9DD0
003C9C33  movzx    edx, byte ptr [rbx + 0xc1]
003C9C3A  test     rcx, rcx
003C9C3D  je       0x3c9c7b  ; -> 003C9C7B
003C9C3F  mov      rax, qword ptr [rcx + 0x60]
003C9C43  mov      byte ptr [rcx + 0xc0], dl
003C9C49  mov      byte ptr [rcx + 0xc3], dil
003C9C50  mov      r8, qword ptr [rax]
003C9C53  cmp      dl, 7
003C9C56  je       0x3c9c72  ; -> 003C9C72
003C9C58  mov      rax, qword ptr [r8 + 0x20]
003C9C5C  mov      edi, 1
003C9C61  movzx    edx, dl
003C9C64  movzx    ecx, byte ptr [rax + rdx*8 + 7]
003C9C69  mov      byte ptr [r8 + 0x39], cl
003C9C6D  mov      word ptr [r8 + 0xa], dx
003C9C72  and      dword ptr [r8 + 8], 0xfffffffe
003C9C77  or       dword ptr [r8 + 8], edi
003C9C7B  mov      rcx, rbx
003C9C7E  call     0x3c9e50  ; -> 003C9E50 fn
003C9C83  mov      rcx, qword ptr [rbx + 0xc8]
003C9C8A  test     rcx, rcx
003C9C8D  je       0x3c9cb5  ; -> 003C9CB5
003C9C8F  mov      eax, dword ptr [rcx + 0x7c]
003C9C92  and      eax, 0xffde0fff
003C9C97  or       eax, 0x1e0400
003C9C9C  mov      dword ptr [rcx + 0x7c], eax
003C9C9F  mov      rcx, rbx
003C9CA2  mov      rdx, qword ptr [rbx + 0xc8]
003C9CA9  call     0x246ad0  ; -> 00246AD0 fn
003C9CAE  or       dword ptr [rbx + 0xc4], 2
003C9CB5  mov      rcx, rbx
003C9CB8  call     0x3c9840  ; -> 003C9840 fn
003C9CBD  and      dword ptr [rbx + 0xc4], 0xfffffffb
003C9CC4  xor      eax, eax
003C9CC6  mov      rbx, qword ptr [rsp + 0x30]
003C9CCB  mov      rsi, qword ptr [rsp + 0x38]
003C9CD0  add      rsp, 0x20
003C9CD4  pop      rdi
003C9CD5  ret      
003C9CD6  test     al, 1
003C9CD8  je       0x3c9dd0  ; -> 003C9DD0
003C9CDE  test     al, 8
003C9CE0  jne      0x3c9dd0  ; -> 003C9DD0
003C9CE6  mov      rcx, qword ptr [rbx + 0xc8]
003C9CED  test     rcx, rcx
003C9CF0  je       0x3c9cfc  ; -> 003C9CFC
003C9CF2  movzx    r8d, byte ptr [rcx + 0xc0]
003C9CFA  jmp      0x3c9cff  ; -> 003C9CFF
003C9CFC  mov      r8b, 7
003C9CFF  cmp      dl, r8b
003C9D02  je       0x3c9dd0  ; -> 003C9DD0
003C9D08  test     rcx, rcx
003C9D0B  je       0x3c9d14  ; -> 003C9D14
003C9D0D  movzx    ecx, byte ptr [rcx + 0xc1]
003C9D14  test     cl, cl
003C9D16  je       0x3c9d3e  ; -> 003C9D3E
003C9D18  sub      cl, 3
003C9D1B  cmp      cl, 1
003C9D1E  ja       0x3c9d52  ; -> 003C9D52
003C9D20  cmp      dl, 7
003C9D23  je       0x3c9d34  ; -> 003C9D34
003C9D25  or       eax, 4
003C9D28  mov      byte ptr [rbx + 0xc1], dl
003C9D2E  mov      dword ptr [rbx + 0xc4], eax
003C9D34  mov      rcx, rbx
003C9D37  call     0x3c98a0  ; -> 003C98A0 fn
003C9D3C  jmp      0x3c9d52  ; -> 003C9D52
003C9D3E  cmp      dl, 7
003C9D41  je       0x3c9d52  ; -> 003C9D52
003C9D43  or       eax, 4
003C9D46  mov      byte ptr [rbx + 0xc1], dl
003C9D4C  mov      dword ptr [rbx + 0xc4], eax
003C9D52  test     byte ptr [rbx + 0xc4], 4
003C9D59  je       0x3c9dd0  ; -> 003C9DD0
003C9D5B  mov      rcx, rbx
003C9D5E  call     0x3c9950  ; -> 003C9950 fn
003C9D63  xor      eax, eax
003C9D65  mov      rbx, qword ptr [rsp + 0x30]
003C9D6A  mov      rsi, qword ptr [rsp + 0x38]
003C9D6F  add      rsp, 0x20
003C9D73  pop      rdi
003C9D74  ret      
003C9D75  and      dword ptr [rcx + 0xc4], 0xfffffffe
003C9D7C  xor      eax, eax
003C9D7E  mov      rbx, qword ptr [rsp + 0x30]
003C9D83  mov      rsi, qword ptr [rsp + 0x38]
003C9D88  add      rsp, 0x20
003C9D8C  pop      rdi
003C9D8D  ret      
003C9D8E  mov      rcx, qword ptr [rcx + 0xc8]
003C9D95  xor      edi, edi
003C9D97  test     rcx, rcx
003C9D9A  je       0x3c9db1  ; -> 003C9DB1
003C9D9C  test     byte ptr [rbx + 0xc4], 2
003C9DA3  jne      0x3c9db1  ; -> 003C9DB1
003C9DA5  call     0x244f00  ; -> 00244F00 fn
003C9DAA  mov      qword ptr [rbx + 0xc8], rdi
003C9DB1  mov      rcx, qword ptr [rbx + 0xd0]
003C9DB8  test     rcx, rcx
003C9DBB  je       0x3c9dc9  ; -> 003C9DC9
003C9DBD  call     0x3697f0  ; -> 003697F0 fn
003C9DC2  mov      qword ptr [rbx + 0xd0], rdi
003C9DC9  mov      qword ptr [rip + 0x277d970], rdi  ; -> 02B47740
003C9DD0  xor      eax, eax
003C9DD2  mov      rbx, qword ptr [rsp + 0x30]
003C9DD7  mov      rsi, qword ptr [rsp + 0x38]
003C9DDC  add      rsp, 0x20
003C9DE0  pop      rdi
003C9DE1  ret      
003C9DE2  mov      rbx, qword ptr [rsp + 0x30]
003C9DE7  mov      rsi, qword ptr [rsp + 0x38]
003C9DEC  add      rsp, 0x20
003C9DF0  pop      rdi
003C9DF1  jmp      0x5c5230  ; -> 005C5230 fn
```
