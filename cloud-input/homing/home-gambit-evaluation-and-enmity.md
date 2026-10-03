# Homing pack: `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-gambit-evaluation-and-enmity.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003A7950 (109 B, extent 003A7950-003A79BD)

Entered from (direct sites whose caller this page cites): `003ED8A0` + 0x135 (call; `003ED8A0` is cited on this page)
Other direct sites: none

Host context: " quest-list selection machine '00579420'; '003829D0' (cited only as the one caller on the Z-10 alias route) calls '003CC000' and is called by 'CameraSystem_SelectAndPublishActiveView' '00259820' and '003ED8A0'. The first three are real consumers (an on-screen test for a selector, the party stance, and the target-relation broadcast after a commit); the others are fan-in on shared helpers and carry no gambit or threat meaning.  **RNG_Rand"

```
003A7950  mov      qword ptr [rsp + 8], rbx
003A7955  mov      qword ptr [rsp + 0x10], rsi
003A795A  push     rdi
003A795B  sub      rsp, 0x20
003A795F  movzx    eax, byte ptr [rcx + 1]
003A7963  lea      rbx, [rcx + 1]
003A7967  mov      rcx, qword ptr [rip + 0x2b1763a]  ; -> 02EBEFA8
003A796E  lea      rsi, [rax*8]
003A7976  mov      rdi, qword ptr [rsi + rcx + 8]
003A797B  test     rdi, rdi
003A797E  je       0x3a79a9  ; -> 003A79A9
003A7980  mov      rcx, rdi
003A7983  call     0x333c00  ; -> 00333C00 fn
003A7988  mov      rcx, rdi
003A798B  call     0x3697f0  ; -> 003697F0 fn
003A7990  mov      rcx, qword ptr [rip + 0x2b17611]  ; -> 02EBEFA8
003A7997  mov      qword ptr [rsi + rcx + 8], 0
003A79A0  mov      rcx, qword ptr [rip + 0x2b17601]  ; -> 02EBEFA8
003A79A7  dec      dword ptr [rcx]
003A79A9  mov      rsi, qword ptr [rsp + 0x38]
003A79AE  lea      rax, [rbx + 1]
003A79B2  mov      rbx, qword ptr [rsp + 0x30]
003A79B7  add      rsp, 0x20
003A79BB  pop      rdi
003A79BC  ret      
```

## 003A7A50 (73 B, extent 003A7A50-003A7A99)

Entered from (direct sites whose caller this page cites): `003ED8A0` + 0x142 (call; `003ED8A0` is cited on this page)
Other direct sites: none

Host context: " quest-list selection machine '00579420'; '003829D0' (cited only as the one caller on the Z-10 alias route) calls '003CC000' and is called by 'CameraSystem_SelectAndPublishActiveView' '00259820' and '003ED8A0'. The first three are real consumers (an on-screen test for a selector, the party stance, and the target-relation broadcast after a commit); the others are fan-in on shared helpers and carry no gambit or threat meaning.  **RNG_Rand"

```
003A7A50  push     rbx
003A7A52  sub      rsp, 0x20
003A7A56  lea      rbx, [rcx + 1]
003A7A5A  movzx    ecx, byte ptr [rcx + 1]
003A7A5E  call     0x3a78a0  ; -> 003A78A0 fn
003A7A63  movups   xmm0, xmmword ptr [rbx + 3]
003A7A67  xor      edx, edx
003A7A69  movups   xmmword ptr [rax], xmm0
003A7A6C  movups   xmm1, xmmword ptr [rbx + 0x13]
003A7A70  movups   xmmword ptr [rax + 0x10], xmm1
003A7A74  movsd    xmm0, qword ptr [rbx + 0x23]
003A7A79  movsd    qword ptr [rax + 0x20], xmm0
003A7A7E  mov      ecx, dword ptr [rbx + 0x2b]
003A7A81  mov      dword ptr [rax + 0x28], ecx
003A7A84  mov      rcx, rax
003A7A87  call     0x333c80  ; -> 00333C80 fn
003A7A8C  lea      rax, [rbx + 0xa3]
003A7A93  add      rsp, 0x20
003A7A97  pop      rbx
003A7A98  ret      
```

## 003A7AA0 (53 B, extent 003A7AA0-003A7AD5)

Entered from (direct sites whose caller this page cites): `003ED8A0` + 0x1C7 (call; `003ED8A0` is cited on this page)
Other direct sites: none

Host context: " quest-list selection machine '00579420'; '003829D0' (cited only as the one caller on the Z-10 alias route) calls '003CC000' and is called by 'CameraSystem_SelectAndPublishActiveView' '00259820' and '003ED8A0'. The first three are real consumers (an on-screen test for a selector, the party stance, and the target-relation broadcast after a commit); the others are fan-in on shared helpers and carry no gambit or threat meaning.  **RNG_Rand"

```
003A7AA0  push     rbx
003A7AA2  sub      rsp, 0x20
003A7AA6  movzx    edx, byte ptr [rcx + 1]
003A7AAA  lea      rbx, [rcx + 1]
003A7AAE  mov      rcx, qword ptr [rip + 0x2b174f3]  ; -> 02EBEFA8
003A7AB5  movzx    eax, byte ptr [rbx + 1]
003A7AB9  mov      rcx, qword ptr [rcx + rdx*8 + 8]
003A7ABE  test     rcx, rcx
003A7AC1  je       0x3a7acb  ; -> 003A7ACB
003A7AC3  movzx    edx, al
003A7AC6  call     0x3340c0  ; -> 003340C0 fn
003A7ACB  lea      rax, [rbx + 2]
003A7ACF  add      rsp, 0x20
003A7AD3  pop      rbx
003A7AD4  ret      
```

## 003A92B0 (24 B, extent 003A92B0-003A92C8)

Entered from (direct sites whose caller this page cites): `003ED8A0` + 0x1D1 (call; `003ED8A0` is cited on this page)
Other direct sites: none

Host context: " quest-list selection machine '00579420'; '003829D0' (cited only as the one caller on the Z-10 alias route) calls '003CC000' and is called by 'CameraSystem_SelectAndPublishActiveView' '00259820' and '003ED8A0'. The first three are real consumers (an on-screen test for a selector, the party stance, and the target-relation broadcast after a commit); the others are fan-in on shared helpers and carry no gambit or threat meaning.  **RNG_Rand"

```
003A92B0  push     rbx
003A92B2  sub      rsp, 0x20
003A92B6  mov      rbx, rcx
003A92B9  call     0x3a9160  ; -> 003A9160 fn
003A92BE  lea      rax, [rbx + 2]
003A92C2  add      rsp, 0x20
003A92C6  pop      rbx
003A92C7  ret      
```
