# F-interior pack: `00-Engine-Core-Runtime/CONTRACT-shared-transform-workbench.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-shared-transform-workbench.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; inbox mentions: SWE2-AUDIT-SEM.md, SWE2-CONTRACT.md). OPUS read these before packing.

## 00455560 (1112 B, extent 00455560-004559B8)

Page context: " section names the edges of the two cited bodies.*  **Presentation — CLIENT (32 edges).** Twenty-nine Presentation bodies of 793 to 1,983 bytes in one address run (among them '0044CC50', '0044D080', '00455560', '004584E0' and '0045D2F0'; thirteen are called directly by the effect type dispatcher, nine by neighbouring bodies in the run, seven by no direct call) call the one consumer '003970A0' to copy the workbench matrix at '022D91B0' o"

```
00455560  mov      qword ptr [rsp + 0x18], rbx
00455565  mov      qword ptr [rsp + 0x20], rdi
0045556A  push     rbp
0045556B  lea      rbp, [rsp - 0x57]
00455570  sub      rsp, 0x100
00455577  mov      rax, qword ptr [rip + 0x1aef2b2]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0045557E  xor      rax, rsp
00455581  mov      qword ptr [rbp + 0x47], rax
00455585  movups   xmm0, xmmword ptr [rcx + 0x250]
0045558C  mov      rdi, qword ptr [rcx + 0x20]
00455590  mov      rbx, rcx
00455593  movups   xmm1, xmmword ptr [rcx + 0x260]
0045559A  movups   xmmword ptr [rbp - 0x39], xmm0
0045559E  movups   xmm0, xmmword ptr [rcx + 0x270]
004555A5  movups   xmmword ptr [rbp - 0x29], xmm1
004555A9  movups   xmm1, xmmword ptr [rcx + 0x280]
004555B0  movups   xmmword ptr [rbp - 0x19], xmm0
004555B4  movups   xmmword ptr [rbp - 9], xmm1
004555B8  movzx    ecx, byte ptr [rdi + 0x4a]
004555BC  shr      ecx, 2
004555BF  and      ecx, 7
004555C2  sub      ecx, 1
004555C5  je       0x455603  ; -> 00455603
004555C7  sub      ecx, 1
004555CA  je       0x4555fa  ; -> 004555FA
004555CC  sub      ecx, 2
004555CF  je       0x4555e8  ; -> 004555E8
004555D1  cmp      ecx, 1
004555D4  jne      0x455613  ; -> 00455613
004555D6  lea      rcx, [rbp - 0x39]
004555DA  call     0x434a70  ; -> 00434A70 fn
004555DF  lea      rcx, [rip + 0x269947a]  ; -> 02AEEA60
004555E6  jmp      0x45560a  ; -> 0045560A
004555E8  lea      rcx, [rbp - 0x39]
004555EC  call     0x434900  ; -> 00434900 fn
004555F1  lea      rcx, [rip + 0x2699468]  ; -> 02AEEA60
004555F8  jmp      0x45560a  ; -> 0045560A
004555FA  lea      rcx, [rip + 0x269966f]  ; -> 02AEEC70
00455601  jmp      0x45560a  ; -> 0045560A
00455603  lea      rcx, [rip + 0x2699626]  ; -> 02AEEC30
0045560A  lea      rdx, [rbp - 0x39]
0045560E  call     0x398030  ; -> 00398030 fn
00455613  mov      ecx, dword ptr [rbx + 0x290]
00455619  call     0x39b620  ; -> 0039B620 fn
0045561E  lea      rcx, [rip + 0x269968b]  ; -> 02AEECB0
00455625  call     0x39b550  ; -> 0039B550 fn
0045562A  lea      rcx, [rbp + 7]
0045562E  call     0x3970a0  ; -> 003970A0 fn
00455633  lea      r8, [rip + 0x268acd6]  ; -> 02AE0310
0045563A  lea      rdx, [rbp - 0x39]
0045563E  lea      rcx, [rbp + 7]
00455642  call     0x397910  ; -> 00397910 fn
00455647  movzx    eax, byte ptr [rdi + 0x240]
0045564E  sub      al, 2
00455650  test     al, 0xfd
00455652  jne      0x455997  ; -> 00455997
00455658  mov      r9d, dword ptr [rbx + 0x44]
0045565C  lea      rdx, [rbp - 0x49]
00455660  xor      r8d, r8d
00455663  mov      qword ptr [rsp + 0x118], rsi
0045566B  lea      rcx, [rdi + 0x1a0]
00455672  call     0x431830  ; -> 00431830 fn
00455677  test     rax, rax
0045567A  je       0x45598f  ; -> 0045598F
00455680  mov      edx, dword ptr [rbx + 0x44]
00455683  lea      rcx, [rdi + 0x30]
00455687  call     0x4314e0  ; -> 004314E0 fn
0045568C  movsxd   rdx, eax
0045568F  lea      rcx, [rdi + 0x1a0]
00455696  movzx    eax, word ptr [rdi + 0x24a]
0045569D  and      eax, 7
004556A0  mov      qword ptr [rip + 0x2699261], rdx  ; -> 02AEE908
004556A7  mov      dword ptr [rip + 0x2699253], eax  ; -> 02AEE900
004556AD  mov      rax, qword ptr [rbp - 0x49]
004556B1  mov      qword ptr [rip + 0x268acb8], rax  ; -> 02AE0370
004556B8  mov      rax, qword ptr [rbp - 0x41]
004556BC  mov      qword ptr [rip + 0x268ac9d], rax  ; -> 02AE0360
004556C3  mov      edx, dword ptr [rbx + 0x44]
004556C6  call     0x4309c0  ; -> 004309C0 fn
004556CB  movss    dword ptr [rip + 0x268abdd], xmm0  ; -> 02AE02B0
004556D3  lea      rcx, [rdi + 0x1b0]
004556DA  mov      edx, dword ptr [rbx + 0x44]
004556DD  call     0x4309c0  ; -> 004309C0 fn
004556E2  movss    xmm1, dword ptr [rip + 0x268abc6]  ; -> 02AE02B0
004556EA  lea      rsi, [rbx + 0x230]
004556F1  movss    dword ptr [rip + 0x268abbb], xmm0  ; -> 02AE02B4
004556F9  lea      r8, [rbp - 0x65]
004556FD  addss    xmm1, dword ptr [rbx + 0x29c]
00455705  mov      rdx, rsi
00455708  mov      rcx, rbx
0045570B  movss    dword ptr [rip + 0x268ab9d], xmm1  ; -> 02AE02B0
00455713  addss    xmm0, dword ptr [rbx + 0x2a0]
0045571B  movss    dword ptr [rip + 0x268ab91], xmm0  ; -> 02AE02B4
00455723  call     0x2f1f40  ; -> 002F1F40 fn
00455728  lea      rdx, [rbx + 0x240]
0045572F  lea      r8, [rbp - 0x65]
00455733  lea      rcx, [rbp - 0x65]
00455737  call     0x26ee00  ; -> 0026EE00 fn
0045573C  mov      edx, dword ptr [rbx + 0x44]
0045573F  lea      rcx, [rdi + 0x1e0]
00455746  call     0x42fdb0  ; -> 0042FDB0 fn
0045574B  lea      r8, [rbp - 0x65]
0045574F  mov      dword ptr [rbp - 0x69], eax
00455752  lea      rdx, [rbp - 0x69]
00455756  lea      rcx, [rbp - 0x69]
0045575A  call     0x26ee00  ; -> 0026EE00 fn
0045575F  movzx    eax, byte ptr [rbp - 0x69]
00455763  mov      dword ptr [rip + 0x268ab37], eax  ; -> 02AE02A0
00455769  movzx    eax, byte ptr [rbp - 0x68]
0045576D  mov      dword ptr [rip + 0x268ab31], eax  ; -> 02AE02A4
00455773  movzx    eax, byte ptr [rbp - 0x67]
00455777  mov      dword ptr [rip + 0x268ab2b], eax  ; -> 02AE02A8
0045577D  movzx    eax, byte ptr [rbp - 0x66]
00455781  mov      dword ptr [rip + 0x268ab25], eax  ; -> 02AE02AC
00455787  movsxd   rax, dword ptr [rbx + 0x298]
0045578E  mov      ecx, dword ptr [rdi + rax*4 + 0x2a0]
00455795  call     0x20e600  ; -> 0020E600 fn
0045579A  mov      rbx, rax
0045579D  test     rax, rax
004557A0  je       0x45598f  ; -> 0045598F
004557A6  lea      rcx, [rip + 0x2699503]  ; -> 02AEECB0
004557AD  call     0x39b550  ; -> 0039B550 fn
004557B2  movzx    edx, byte ptr [rdi + 0x294]
004557B9  shr      edx, 1
004557BB  and      edx, 3
004557BE  sub      edx, 1
004557C1  je       0x4558da  ; -> 004558DA
004557C7  sub      edx, 1
004557CA  je       0x4558ce  ; -> 004558CE
004557D0  cmp      edx, 1
004557D3  jne      0x45598f  ; -> 0045598F
004557D9  test     byte ptr [rdi + 0x24a], 7
004557E0  jne      0x455844  ; -> 00455844
004557E2  mov      dword ptr [rip + 0x268aa94], 2  ; -> 02AE0280
004557EC  mov      ecx, dword ptr [rbx + 0x10]
004557EF  call     0x20e600  ; -> 0020E600 fn
004557F4  mov      ecx, dword ptr [rbx + 0x14]
004557F7  lea      rdi, [rip + 0x268aa7a]  ; -> 02AE0278
004557FE  mov      edx, dword ptr [rip + 0x268aa68]  ; -> 02AE026C
00455804  lea      r8, [rip + 0x44215]  ; -> 00499A20
0045580B  mov      dword ptr [rsp + 0x30], ecx
0045580F  mov      r9, rdi
00455812  mov      ecx, dword ptr [rip + 0x268aa50]  ; -> 02AE0268
00455818  mov      qword ptr [rsp + 0x28], rax
0045581D  mov      dword ptr [rsp + 0x20], 0x118
00455825  call     0x3a2f70  ; -> 003A2F70 fn
0045582A  mov      dword ptr [rip + 0x268aa4c], 0  ; -> 02AE0280
00455834  mov      ecx, dword ptr [rbx + 0x10]
00455837  call     0x20e600  ; -> 0020E600 fn
0045583C  mov      r9, rdi
0045583F  jmp      0x4558fc  ; -> 004558FC
00455844  test     byte ptr [rdi + 0x4b], 1
00455848  mov      rcx, rsi
0045584B  jne      0x455863  ; -> 00455863
0045584D  lea      rdx, [rbp - 0x59]
00455851  call     0x399600  ; -> 00399600 fn
00455856  test     eax, eax
00455858  jne      0x45598f  ; -> 0045598F
0045585E  mov      esi, dword ptr [rbp - 0x55]
00455861  jmp      0x45586a  ; -> 0045586A
00455863  call     0x39a9b0  ; -> 0039A9B0 fn
00455868  mov      esi, eax
0045586A  mov      dword ptr [rip + 0x268aa0c], 2  ; -> 02AE0280
00455874  mov      ecx, dword ptr [rbx + 0x10]
00455877  call     0x20e600  ; -> 0020E600 fn
0045587C  mov      ecx, dword ptr [rbx + 0x14]
0045587F  lea      rdi, [rip + 0x268a9f2]  ; -> 02AE0278
00455886  mov      r8d, dword ptr [rip + 0x268a9df]  ; -> 02AE026C
0045588D  lea      r9, [rip + 0x4418c]  ; -> 00499A20
00455894  mov      edx, dword ptr [rip + 0x268a9ce]  ; -> 02AE0268
0045589A  mov      dword ptr [rsp + 0x38], ecx
0045589E  mov      ecx, esi
004558A0  mov      qword ptr [rsp + 0x30], rax
004558A5  mov      dword ptr [rsp + 0x28], 0x118
004558AD  mov      qword ptr [rsp + 0x20], rdi
004558B2  call     0x3a33b0  ; -> 003A33B0 fn
004558B7  mov      dword ptr [rip + 0x268a9bf], 0  ; -> 02AE0280
004558C1  mov      ecx, dword ptr [rbx + 0x10]
004558C4  call     0x20e600  ; -> 0020E600 fn
004558C9  jmp      0x45595b  ; -> 0045595B
004558CE  mov      dword ptr [rip + 0x268a9a8], 2  ; -> 02AE0280
004558D8  jmp      0x4558e4  ; -> 004558E4
004558DA  mov      dword ptr [rip + 0x268a99c], 0  ; -> 02AE0280
004558E4  test     byte ptr [rdi + 0x24a], 7
004558EB  jne      0x45592a  ; -> 0045592A
004558ED  mov      ecx, dword ptr [rbx + 0x10]
004558F0  call     0x20e600  ; -> 0020E600 fn
004558F5  lea      r9, [rip + 0x268a97c]  ; -> 02AE0278
004558FC  mov      ecx, dword ptr [rbx + 0x14]
004558FF  lea      r8, [rip + 0x4411a]  ; -> 00499A20
00455906  mov      edx, dword ptr [rip + 0x268a960]  ; -> 02AE026C
0045590C  mov      dword ptr [rsp + 0x30], ecx
00455910  mov      ecx, dword ptr [rip + 0x268a952]  ; -> 02AE0268
00455916  mov      qword ptr [rsp + 0x28], rax
0045591B  mov      dword ptr [rsp + 0x20], 0x118
00455923  call     0x3a2f70  ; -> 003A2F70 fn
00455928  jmp      0x45598f  ; -> 0045598F
0045592A  test     byte ptr [rdi + 0x4b], 1
0045592E  mov      rcx, rsi
00455931  jne      0x455945  ; -> 00455945
00455933  lea      rdx, [rbp - 0x59]
00455937  call     0x399600  ; -> 00399600 fn
0045593C  test     eax, eax
0045593E  jne      0x45598f  ; -> 0045598F
00455940  mov      esi, dword ptr [rbp - 0x55]
00455943  jmp      0x45594c  ; -> 0045594C
00455945  call     0x39a9b0  ; -> 0039A9B0 fn
0045594A  mov      esi, eax
0045594C  mov      ecx, dword ptr [rbx + 0x10]
0045594F  call     0x20e600  ; -> 0020E600 fn
00455954  lea      rdi, [rip + 0x268a91d]  ; -> 02AE0278
0045595B  mov      ecx, dword ptr [rbx + 0x14]
0045595E  lea      r9, [rip + 0x440bb]  ; -> 00499A20
00455965  mov      r8d, dword ptr [rip + 0x268a900]  ; -> 02AE026C
0045596C  mov      edx, dword ptr [rip + 0x268a8f6]  ; -> 02AE0268
00455972  mov      dword ptr [rsp + 0x38], ecx
00455976  mov      ecx, esi
00455978  mov      qword ptr [rsp + 0x30], rax
0045597D  mov      dword ptr [rsp + 0x28], 0x118
00455985  mov      qword ptr [rsp + 0x20], rdi
0045598A  call     0x3a33b0  ; -> 003A33B0 fn
0045598F  mov      rsi, qword ptr [rsp + 0x118]
00455997  mov      rcx, qword ptr [rbp + 0x47]
0045599B  xor      rcx, rsp
0045599E  call     0x808c40  ; -> 00808C40 fn
004559A3  lea      r11, [rsp + 0x100]
004559AB  mov      rbx, qword ptr [r11 + 0x20]
004559AF  mov      rdi, qword ptr [r11 + 0x28]
004559B3  mov      rsp, r11
004559B6  pop      rbp
004559B7  ret      
```

## 004584E0 (1983 B, extent 004584E0-00458C9F)

Page context: "es the edges of the two cited bodies.*  **Presentation — CLIENT (32 edges).** Twenty-nine Presentation bodies of 793 to 1,983 bytes in one address run (among them '0044CC50', '0044D080', '00455560', '004584E0' and '0045D2F0'; thirteen are called directly by the effect type dispatcher, nine by neighbouring bodies in the run, seven by no direct call) call the one consumer '003970A0' to copy the workbench matrix at '022D91B0' out as one 64"

```
004584E0  push     rbp
004584E2  push     rdi
004584E3  lea      rbp, [rsp - 0x38]
004584E8  sub      rsp, 0x138
004584EF  mov      rax, qword ptr [rip + 0x1aec33a]  ; -> 01F44830 [u64 0x00002B992DDFA232]
004584F6  xor      rax, rsp
004584F9  mov      qword ptr [rbp + 0x10], rax
004584FD  cmp      byte ptr [rcx], 0
00458500  mov      rdi, rcx
00458503  je       0x458c89  ; -> 00458C89
00458509  movups   xmm0, xmmword ptr [rcx + 0x250]
00458510  mov      qword ptr [rsp + 0x158], rbx
00458518  movups   xmm1, xmmword ptr [rcx + 0x260]
0045851F  mov      rbx, qword ptr [rcx + 0x20]
00458523  movups   xmmword ptr [rsp + 0x70], xmm0
00458528  movups   xmm0, xmmword ptr [rcx + 0x270]
0045852F  movups   xmmword ptr [rbp - 0x80], xmm1
00458533  movups   xmm1, xmmword ptr [rcx + 0x280]
0045853A  movups   xmmword ptr [rbp - 0x70], xmm0
0045853E  movups   xmmword ptr [rbp - 0x60], xmm1
00458542  movzx    ecx, byte ptr [rbx + 0x4a]
00458546  shr      ecx, 2
00458549  and      ecx, 7
0045854C  sub      ecx, 1
0045854F  je       0x45858f  ; -> 0045858F
00458551  sub      ecx, 1
00458554  je       0x458586  ; -> 00458586
00458556  sub      ecx, 2
00458559  je       0x458573  ; -> 00458573
0045855B  cmp      ecx, 1
0045855E  jne      0x4585a0  ; -> 004585A0
00458560  lea      rcx, [rsp + 0x70]
00458565  call     0x434a70  ; -> 00434A70 fn
0045856A  lea      rcx, [rip + 0x26964ef]  ; -> 02AEEA60
00458571  jmp      0x458596  ; -> 00458596
00458573  lea      rcx, [rsp + 0x70]
00458578  call     0x434900  ; -> 00434900 fn
0045857D  lea      rcx, [rip + 0x26964dc]  ; -> 02AEEA60
00458584  jmp      0x458596  ; -> 00458596
00458586  lea      rcx, [rip + 0x26966e3]  ; -> 02AEEC70
0045858D  jmp      0x458596  ; -> 00458596
0045858F  lea      rcx, [rip + 0x269669a]  ; -> 02AEEC30
00458596  lea      rdx, [rsp + 0x70]
0045859B  call     0x398030  ; -> 00398030 fn
004585A0  movaps   xmm0, xmmword ptr [rsp + 0x70]
004585A5  lea      r8, [rbp - 0x50]
004585A9  movaps   xmm1, xmmword ptr [rbp - 0x80]
004585AD  lea      rdx, [rsp + 0x70]
004585B2  movups   xmmword ptr [rip + 0x26896a7], xmm0  ; -> 02AE1C60
004585B9  lea      rcx, [rip + 0x2696630]  ; -> 02AEEBF0
004585C0  movaps   xmm0, xmmword ptr [rbp - 0x70]
004585C4  movups   xmmword ptr [rip + 0x26896b5], xmm0  ; -> 02AE1C80
004585CB  movups   xmmword ptr [rip + 0x268969e], xmm1  ; -> 02AE1C70
004585D2  call     0x397910  ; -> 00397910 fn
004585D7  lea      rdx, [rbp - 0x50]
004585DB  lea      rcx, [rbp - 0x50]
004585DF  call     0x39b960  ; -> 0039B960 fn
004585E4  lea      rdx, [rbp - 0x40]
004585E8  lea      rcx, [rbp - 0x40]
004585EC  call     0x39b960  ; -> 0039B960 fn
004585F1  lea      rdx, [rbp - 0x30]
004585F5  lea      rcx, [rbp - 0x30]
004585F9  call     0x39b960  ; -> 0039B960 fn
004585FE  movaps   xmm0, xmmword ptr [rbp - 0x50]
00458602  movaps   xmm1, xmmword ptr [rbp - 0x40]
00458606  movups   xmmword ptr [rip + 0x2689683], xmm0  ; -> 02AE1C90
0045860D  movaps   xmm0, xmmword ptr [rbp - 0x30]
00458611  movups   xmmword ptr [rip + 0x2689698], xmm0  ; -> 02AE1CB0
00458618  movups   xmmword ptr [rip + 0x2689681], xmm1  ; -> 02AE1CA0
0045861F  mov      ecx, dword ptr [rdi + 0x290]
00458625  call     0x39b620  ; -> 0039B620 fn
0045862A  lea      rcx, [rip + 0x269667f]  ; -> 02AEECB0
00458631  call     0x39b550  ; -> 0039B550 fn
00458636  lea      rcx, [rbp - 0x50]
0045863A  call     0x3970a0  ; -> 003970A0 fn
0045863F  lea      r8, [rip + 0x268967a]  ; -> 02AE1CC0
00458646  lea      rdx, [rsp + 0x70]
0045864B  lea      rcx, [rbp - 0x50]
0045864F  call     0x397910  ; -> 00397910 fn
00458654  movzx    eax, byte ptr [rbx + 0x240]
0045865B  sub      al, 2
0045865D  test     al, 0xfd
0045865F  jne      0x458c81  ; -> 00458C81
00458665  mov      r9d, dword ptr [rdi + 0x44]
00458669  lea      rdx, [rsp + 0x50]
0045866E  xor      r8d, r8d
00458671  mov      qword ptr [rsp + 0x160], rsi
00458679  lea      rcx, [rbx + 0x1a0]
00458680  call     0x431830  ; -> 00431830 fn
00458685  test     rax, rax
00458688  je       0x458c79  ; -> 00458C79
0045868E  mov      edx, dword ptr [rdi + 0x44]
00458691  lea      rcx, [rbx + 0x30]
00458695  mov      qword ptr [rsp + 0x168], r12
0045869D  mov      qword ptr [rsp + 0x130], r13
004586A5  mov      qword ptr [rsp + 0x128], r14
004586AD  mov      qword ptr [rsp + 0x120], r15
004586B5  call     0x4314e0  ; -> 004314E0 fn
004586BA  movsxd   rcx, eax
004586BD  mov      r12d, 0x51001
004586C3  movzx    eax, word ptr [rbx + 0x24a]
004586CA  and      eax, 7
004586CD  mov      qword ptr [rip + 0x2696234], rcx  ; -> 02AEE908
004586D4  mov      dword ptr [rip + 0x2696226], eax  ; -> 02AEE900
004586DA  lea      rcx, [rip + 0x1aa253f]  ; -> 01EFAC20
004586E1  mov      rax, qword ptr [rsp + 0x58]
004586E6  mov      qword ptr [rip + 0x2689623], rax  ; -> 02AE1D10
004586ED  movzx    eax, word ptr [rbx + 0x24a]
004586F4  and      eax, 7
004586F7  mov      rax, qword ptr [rcx + rax*8]
004586FB  mov      ecx, 0x70000
00458700  mov      qword ptr [rip + 0x2689629], rax  ; -> 02AE1D30
00458707  mov      eax, r12d
0045870A  test     byte ptr [rbx + 0x24a], 7
00458711  cmove    eax, ecx
00458714  lea      rcx, [rbx + 0x1a0]
0045871B  mov      qword ptr [rip + 0x268962e], rax  ; -> 02AE1D50
00458722  mov      rax, qword ptr [rsp + 0x50]
00458727  mov      qword ptr [rip + 0x2689642], rax  ; -> 02AE1D70
0045872E  mov      edx, dword ptr [rdi + 0x44]
00458731  call     0x4309c0  ; -> 004309C0 fn
00458736  movss    dword ptr [rip + 0x26894e2], xmm0  ; -> 02AE1C20
0045873E  lea      rcx, [rbx + 0x1b0]
00458745  mov      edx, dword ptr [rdi + 0x44]
00458748  call     0x4309c0  ; -> 004309C0 fn
0045874D  movss    xmm1, dword ptr [rip + 0x26894cb]  ; -> 02AE1C20
00458755  lea      r15, [rdi + 0x230]
0045875C  movss    dword ptr [rip + 0x26894c0], xmm0  ; -> 02AE1C24
00458764  lea      r8, [rsp + 0x44]
00458769  addss    xmm1, dword ptr [rdi + 0x29c]
00458771  mov      rdx, r15
00458774  mov      rcx, rdi
00458777  movss    dword ptr [rip + 0x26894a1], xmm1  ; -> 02AE1C20
0045877F  addss    xmm0, dword ptr [rdi + 0x2a0]
00458787  movss    dword ptr [rip + 0x2689495], xmm0  ; -> 02AE1C24
0045878F  call     0x2f1f40  ; -> 002F1F40 fn
00458794  lea      rdx, [rdi + 0x240]
0045879B  lea      r8, [rsp + 0x44]
004587A0  lea      rcx, [rsp + 0x44]
004587A5  call     0x26ee00  ; -> 0026EE00 fn
004587AA  mov      edx, dword ptr [rdi + 0x44]
004587AD  lea      rcx, [rbx + 0x1e0]
004587B4  call     0x42fdb0  ; -> 0042FDB0 fn
004587B9  lea      r8, [rsp + 0x44]
004587BE  mov      dword ptr [rsp + 0x40], eax
004587C2  lea      rdx, [rsp + 0x40]
004587C7  lea      rcx, [rsp + 0x40]
004587CC  call     0x26ee00  ; -> 0026EE00 fn
004587D1  movzx    eax, byte ptr [rsp + 0x40]
004587D6  xor      edx, edx
004587D8  mov      dword ptr [rip + 0x2689422], eax  ; -> 02AE1C00
004587DE  movzx    eax, byte ptr [rsp + 0x41]
004587E3  mov      dword ptr [rip + 0x268941b], eax  ; -> 02AE1C04
004587E9  movzx    eax, byte ptr [rsp + 0x42]
004587EE  lea      esi, [rdx + 1]
004587F1  mov      dword ptr [rip + 0x2689411], eax  ; -> 02AE1C08
004587F7  lea      r8d, [rdx + 8]
004587FB  movzx    eax, byte ptr [rsp + 0x43]
00458800  lea      r14d, [rdx + 4]
00458804  mov      dword ptr [rip + 0x2689402], eax  ; -> 02AE1C0C
0045880A  movzx    ecx, word ptr [rbx + 0x24a]
00458811  shr      ecx, 4
00458814  and      ecx, 3
00458817  je       0x4588bd  ; -> 004588BD
0045881D  sub      ecx, esi
0045881F  je       0x45887c  ; -> 0045887C
00458821  cmp      ecx, esi
00458823  jne      0x4588c3  ; -> 004588C3
00458829  movzx    eax, byte ptr [rbx + 0x249]
00458830  test     al, al
00458832  je       0x4588bd  ; -> 004588BD
00458838  js       0x458862  ; -> 00458862
0045883A  mov      dword ptr [rip + 0x268939f], r14d  ; -> 02AE1BE0
00458841  movsx    eax, byte ptr [rbx + 0x249]
00458848  dec      eax
0045884A  mov      dword ptr [rip + 0x2689398], eax  ; -> 02AE1BE8
00458850  movss    xmm0, dword ptr [rbx + 0x24c]
00458858  movss    dword ptr [rip + 0x26893cc], xmm0  ; -> 02AE1C2C
00458860  jmp      0x4588c3  ; -> 004588C3
00458862  mov      dword ptr [rip + 0x2689377], r8d  ; -> 02AE1BE0
00458869  mov      ecx, esi
0045886B  movsx    eax, byte ptr [rbx + 0x249]
00458872  sub      ecx, eax
00458874  mov      dword ptr [rip + 0x268936e], ecx  ; -> 02AE1BE8
0045887A  jmp      0x458850  ; -> 00458850
0045887C  movzx    eax, byte ptr [rbx + 0x249]
00458883  test     al, al
00458885  je       0x4588bd  ; -> 004588BD
00458887  js       0x4588a0  ; -> 004588A0
00458889  mov      dword ptr [rip + 0x2689351], esi  ; -> 02AE1BE0
0045888F  movsx    eax, byte ptr [rbx + 0x249]
00458896  dec      eax
00458898  mov      dword ptr [rip + 0x268934a], eax  ; -> 02AE1BE8
0045889E  jmp      0x4588c3  ; -> 004588C3
004588A0  mov      dword ptr [rip + 0x2689336], 2  ; -> 02AE1BE0
004588AA  mov      ecx, esi
004588AC  movsx    eax, byte ptr [rbx + 0x249]
004588B3  sub      ecx, eax
004588B5  mov      dword ptr [rip + 0x268932d], ecx  ; -> 02AE1BE8
004588BB  jmp      0x4588c3  ; -> 004588C3
004588BD  mov      dword ptr [rip + 0x268931d], edx  ; -> 02AE1BE0
004588C3  movzx    eax, byte ptr [rbx + 0x330]
004588CA  sub      al, 2
004588CC  test     al, 0xfd
004588CE  jne      0x458c59  ; -> 00458C59
004588D4  mov      r9d, dword ptr [rdi + 0x44]
004588D8  lea      rcx, [rbx + 0x290]
004588DF  xor      r8d, r8d
004588E2  lea      rdx, [rsp + 0x50]
004588E7  call     0x431830  ; -> 00431830 fn
004588EC  test     rax, rax
004588EF  je       0x458c59  ; -> 00458C59
004588F5  mov      edx, dword ptr [rdi + 0x44]
004588F8  lea      rcx, [rbx + 0x30]
004588FC  call     0x4314e0  ; -> 004314E0 fn
00458901  movsxd   rcx, eax
00458904  movzx    eax, word ptr [rbx + 0x33a]
0045890B  and      eax, 7
0045890E  mov      qword ptr [rip + 0x2695ff3], rcx  ; -> 02AEE908
00458915  mov      dword ptr [rip + 0x2695fe5], eax  ; -> 02AEE900
0045891B  lea      rcx, [rip + 0x1aa22fe]  ; -> 01EFAC20
00458922  mov      rax, qword ptr [rsp + 0x58]
00458927  mov      qword ptr [rip + 0x26893f2], rax  ; -> 02AE1D20
0045892E  movzx    eax, word ptr [rbx + 0x33a]
00458935  and      eax, 7
00458938  mov      rax, qword ptr [rcx + rax*8]
0045893C  lea      rcx, [rbx + 0x2d0]
00458943  mov      qword ptr [rip + 0x26893f6], rax  ; -> 02AE1D40
0045894A  mov      eax, 0x70000
0045894F  test     byte ptr [rbx + 0x33a], 7
00458956  cmove    r12, rax
0045895A  mov      rax, qword ptr [rsp + 0x50]
0045895F  mov      qword ptr [rip + 0x268941a], rax  ; -> 02AE1D80
00458966  mov      qword ptr [rip + 0x26893f3], r12  ; -> 02AE1D60
0045896D  mov      edx, dword ptr [rdi + 0x44]
00458970  call     0x42fdb0  ; -> 0042FDB0 fn
00458975  lea      r8, [rsp + 0x44]
0045897A  mov      dword ptr [rsp + 0x40], eax
0045897E  lea      rdx, [rsp + 0x40]
00458983  lea      rcx, [rsp + 0x40]
00458988  call     0x26ee00  ; -> 0026EE00 fn
0045898D  movzx    eax, byte ptr [rsp + 0x40]
00458992  mov      dword ptr [rip + 0x2689278], eax  ; -> 02AE1C10
00458998  movzx    eax, byte ptr [rsp + 0x41]
0045899D  mov      dword ptr [rip + 0x2689271], eax  ; -> 02AE1C14
004589A3  movzx    eax, byte ptr [rsp + 0x42]
004589A8  mov      dword ptr [rip + 0x268926a], eax  ; -> 02AE1C18
004589AE  movzx    eax, byte ptr [rsp + 0x43]
004589B3  mov      dword ptr [rip + 0x2689263], eax  ; -> 02AE1C1C
004589B9  movzx    ecx, word ptr [rbx + 0x33a]
004589C0  shr      ecx, 4
004589C3  and      ecx, 3
004589C6  je       0x458a74  ; -> 00458A74
004589CC  sub      ecx, esi
004589CE  je       0x458a2f  ; -> 00458A2F
004589D0  cmp      ecx, esi
004589D2  jne      0x458a7e  ; -> 00458A7E
004589D8  movzx    eax, byte ptr [rbx + 0x339]
004589DF  test     al, al
004589E1  je       0x458a74  ; -> 00458A74
004589E7  mov      r12d, 8
004589ED  js       0x458a17  ; -> 00458A17
004589EF  mov      dword ptr [rip + 0x26891ee], r14d  ; -> 02AE1BE4
004589F6  movsx    eax, byte ptr [rbx + 0x339]
004589FD  dec      eax
004589FF  mov      dword ptr [rip + 0x26891e7], eax  ; -> 02AE1BEC
00458A05  movss    xmm0, dword ptr [rbx + 0x33c]
00458A0D  movss    dword ptr [rip + 0x2689227], xmm0  ; -> 02AE1C3C
00458A15  jmp      0x458a84  ; -> 00458A84
00458A17  mov      dword ptr [rip + 0x26891c6], r12d  ; -> 02AE1BE4
00458A1E  movsx    eax, byte ptr [rbx + 0x339]
00458A25  sub      esi, eax
00458A27  mov      dword ptr [rip + 0x26891bf], esi  ; -> 02AE1BEC
00458A2D  jmp      0x458a05  ; -> 00458A05
00458A2F  movzx    eax, byte ptr [rbx + 0x339]
00458A36  test     al, al
00458A38  je       0x458a74  ; -> 00458A74
00458A3A  mov      r12d, 8
00458A40  js       0x458a59  ; -> 00458A59
00458A42  mov      dword ptr [rip + 0x268919c], esi  ; -> 02AE1BE4
00458A48  movsx    eax, byte ptr [rbx + 0x339]
00458A4F  dec      eax
00458A51  mov      dword ptr [rip + 0x2689195], eax  ; -> 02AE1BEC
00458A57  jmp      0x458a84  ; -> 00458A84
00458A59  mov      dword ptr [rip + 0x2689181], 2  ; -> 02AE1BE4
00458A63  movsx    eax, byte ptr [rbx + 0x339]
00458A6A  sub      esi, eax
00458A6C  mov      dword ptr [rip + 0x268917a], esi  ; -> 02AE1BEC
00458A72  jmp      0x458a84  ; -> 00458A84
00458A74  mov      dword ptr [rip + 0x2689166], 0  ; -> 02AE1BE4
00458A7E  mov      r12d, 8
00458A84  movzx    ecx, byte ptr [rbx + 0x337]
00458A8B  test     ecx, ecx
00458A8D  je       0x458b36  ; -> 00458B36
00458A93  sub      ecx, 1
00458A96  je       0x458ac4  ; -> 00458AC4
00458A98  cmp      ecx, 1
00458A9B  jne      0x458b40  ; -> 00458B40
00458AA1  mov      dword ptr [rip + 0x268914d], 0x10  ; -> 02AE1BF8
00458AAB  lea      rcx, [rbx + 0x320]
00458AB2  mov      edx, dword ptr [rdi + 0x44]
00458AB5  call     0x4309c0  ; -> 004309C0 fn
00458ABA  movss    dword ptr [rip + 0x268919a], xmm0  ; -> 02AE1C5C
00458AC2  jmp      0x458b40  ; -> 00458B40
00458AC4  movaps   xmm0, xmmword ptr [rip + 0x46d4e5]  ; -> 008C5FB0 [f32x4 0, 0, 1, 0]
00458ACB  lea      r8, [rsp + 0x60]
00458AD0  lea      rdx, [rbp - 0x10]
00458AD4  movaps   xmmword ptr [rbp - 0x10], xmm0
00458AD8  lea      rcx, [rip + 0x2695fc1]  ; -> 02AEEAA0
00458ADF  call     0x394da0  ; -> 00394DA0 fn
00458AE4  lea      rdx, [rsp + 0x60]
00458AE9  lea      rcx, [rsp + 0x60]
00458AEE  call     0x39b960  ; -> 0039B960 fn
00458AF3  movss    xmm0, dword ptr [rsp + 0x60]
00458AF9  mov      eax, 0x100
00458AFE  movss    xmm1, dword ptr [rsp + 0x64]
00458B04  movss    dword ptr [rip + 0x2689144], xmm0  ; -> 02AE1C50
00458B0C  movss    xmm0, dword ptr [rsp + 0x68]
00458B12  movss    dword ptr [rip + 0x268913e], xmm0  ; -> 02AE1C58
00458B1A  movss    dword ptr [rip + 0x2689132], xmm1  ; -> 02AE1C54
00458B22  test     word ptr [rbx + 0x33a], ax
00458B29  cmove    r14d, r12d
00458B2D  mov      dword ptr [rip + 0x26890c4], r14d  ; -> 02AE1BF8
00458B34  jmp      0x458b40  ; -> 00458B40
00458B36  mov      dword ptr [rip + 0x26890b8], 0  ; -> 02AE1BF8
00458B40  movsxd   rax, dword ptr [rdi + 0x298]
00458B47  mov      ecx, dword ptr [rbx + rax*4 + 0x390]
00458B4E  call     0x20e600  ; -> 0020E600 fn
00458B53  mov      rdi, rax
00458B56  test     rax, rax
00458B59  je       0x458c59  ; -> 00458C59
00458B5F  lea      rcx, [rip + 0x269614a]  ; -> 02AEECB0
00458B66  call     0x39b550  ; -> 0039B550 fn
00458B6B  test     byte ptr [rbx + 0x4b], 1
00458B6F  mov      rcx, r15
00458B72  jne      0x458b8a  ; -> 00458B8A
00458B74  lea      rdx, [rbp]
00458B78  call     0x399600  ; -> 00399600 fn
00458B7D  test     eax, eax
00458B7F  jne      0x458c59  ; -> 00458C59
00458B85  mov      esi, dword ptr [rbp + 4]
00458B88  jmp      0x458b91  ; -> 00458B91
00458B8A  call     0x39a9b0  ; -> 0039A9B0 fn
00458B8F  mov      esi, eax
00458B91  movzx    ecx, byte ptr [rbx + 0x384]
00458B98  shr      cl, 1
00458B9A  and      cl, 3
00458B9D  movzx    eax, cl
00458BA0  cmp      cl, 1
00458BA3  jbe      0x458c16  ; -> 00458C16
00458BA5  cmp      al, 2
00458BA7  je       0x458c0f  ; -> 00458C0F
00458BA9  cmp      al, 3
00458BAB  jne      0x458c59  ; -> 00458C59
00458BB1  or       dword ptr [rip + 0x2689040], 2  ; -> 02AE1BF8
00458BB8  mov      ecx, dword ptr [rdi + 0x10]
00458BBB  call     0x20e600  ; -> 0020E600 fn
00458BC0  mov      ecx, dword ptr [rdi + 0x14]
00458BC3  lea      rbx, [rip + 0x268900e]  ; -> 02AE1BD8
00458BCA  mov      r8d, dword ptr [rip + 0x2688ffb]  ; -> 02AE1BCC
00458BD1  lea      r9, [rip + 0x4b838]  ; -> 004A4410
00458BD8  mov      edx, dword ptr [rip + 0x2688fea]  ; -> 02AE1BC8
00458BDE  mov      dword ptr [rsp + 0x38], ecx
00458BE2  mov      ecx, esi
00458BE4  mov      qword ptr [rsp + 0x30], rax
00458BE9  mov      dword ptr [rsp + 0x28], 0x1c8
00458BF1  mov      qword ptr [rsp + 0x20], rbx
00458BF6  call     0x3a33b0  ; -> 003A33B0 fn
00458BFB  and      dword ptr [rip + 0x2688ff3], 0xfffd  ; -> 02AE1BF8
00458C05  mov      ecx, dword ptr [rdi + 0x10]
00458C08  call     0x20e600  ; -> 0020E600 fn
00458C0D  jmp      0x458c25  ; -> 00458C25
00458C0F  or       dword ptr [rip + 0x2688fe2], 2  ; -> 02AE1BF8
00458C16  mov      ecx, dword ptr [rdi + 0x10]
00458C19  call     0x20e600  ; -> 0020E600 fn
00458C1E  lea      rbx, [rip + 0x2688fb3]  ; -> 02AE1BD8
00458C25  mov      ecx, dword ptr [rdi + 0x14]
00458C28  lea      r9, [rip + 0x4b7e1]  ; -> 004A4410
00458C2F  mov      r8d, dword ptr [rip + 0x2688f96]  ; -> 02AE1BCC
00458C36  mov      edx, dword ptr [rip + 0x2688f8c]  ; -> 02AE1BC8
00458C3C  mov      dword ptr [rsp + 0x38], ecx
00458C40  mov      ecx, esi
00458C42  mov      qword ptr [rsp + 0x30], rax
00458C47  mov      dword ptr [rsp + 0x28], 0x1c8
00458C4F  mov      qword ptr [rsp + 0x20], rbx
00458C54  call     0x3a33b0  ; -> 003A33B0 fn
00458C59  mov      r14, qword ptr [rsp + 0x128]
00458C61  mov      r13, qword ptr [rsp + 0x130]
00458C69  mov      r12, qword ptr [rsp + 0x168]
00458C71  mov      r15, qword ptr [rsp + 0x120]
00458C79  mov      rsi, qword ptr [rsp + 0x160]
00458C81  mov      rbx, qword ptr [rsp + 0x158]
00458C89  mov      rcx, qword ptr [rbp + 0x10]
00458C8D  xor      rcx, rsp
00458C90  call     0x808c40  ; -> 00808C40 fn
00458C95  add      rsp, 0x138
00458C9C  pop      rdi
00458C9D  pop      rbp
00458C9E  ret      
```
