# F-interior pack: `99-Unresolved-Residual/the-nine-patch-window-frame.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-nine-patch-window-frame.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 0028BB50 (2387 B, extent 0028BB50-0028C4A3)

Page context: "t_tag: GN162     basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0028BB50, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity"

```
0028BB50  mov      rax, rsp
0028BB53  mov      qword ptr [rax + 0x10], rbx
0028BB57  mov      qword ptr [rax + 0x18], rsi
0028BB5B  mov      qword ptr [rax + 0x20], rdi
0028BB5F  push     rbp
0028BB60  push     r12
0028BB62  push     r13
0028BB64  push     r14
0028BB66  push     r15
0028BB68  lea      rbp, [rsp - 0x70]
0028BB6D  sub      rsp, 0x170
0028BB74  movaps   xmmword ptr [rax - 0x38], xmm6
0028BB78  movaps   xmmword ptr [rax - 0x48], xmm7
0028BB7C  movaps   xmmword ptr [rax - 0x58], xmm8
0028BB81  movaps   xmmword ptr [rax - 0x68], xmm9
0028BB86  movaps   xmmword ptr [rax - 0x78], xmm10
0028BB8B  movaps   xmmword ptr [rax - 0x88], xmm11
0028BB93  movaps   xmmword ptr [rax - 0x98], xmm15
0028BB9B  mov      rax, qword ptr [rip + 0x1cb8c8e]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0028BBA2  xor      rax, rsp
0028BBA5  mov      qword ptr [rbp - 0x10], rax
0028BBA9  mov      rdi, rcx
0028BBAC  lea      rcx, [rbp - 0x50]
0028BBB0  call     0x203170  ; -> 00203170 fn
0028BBB5  mov      ecx, dword ptr [rdi + 0xd50]
0028BBBB  mov      esi, 0x3c0
0028BBC0  cmp      ecx, 1
0028BBC3  jne      0x28be9a  ; -> 0028BE9A
0028BBC9  mov      esi, 0x4e0
0028BBCE  mov      r14d, 0xab0
0028BBD4  movss    xmm11, dword ptr [rip + 0x689a43]  ; -> 00915620 [f32 -3.141593]
0028BBDD  xor      r12d, r12d
0028BBE0  movss    xmm9, dword ptr [rip + 0x1a6008f]  ; -> 01CEBC78 [f32 6.283185]
0028BBE9  movss    xmm10, dword ptr [rip + 0x1a6005e]  ; -> 01CEBC50 [f32 3.141593]
0028BBF2  mov      dword ptr [rsi + rdi + 0xdc], r12d
0028BBFA  mov      eax, dword ptr [rdi + 0xd4c]
0028BC00  test     al, 0x40
0028BC02  je       0x28bcb7  ; -> 0028BCB7
0028BC08  movss    xmm0, dword ptr [rdi + 0xd40]
0028BC10  addss    xmm0, dword ptr [rdi + 0xd44]
0028BC18  comiss   xmm11, xmm0
0028BC1C  movss    dword ptr [rdi + 0xd40], xmm0
0028BC24  jb       0x28bc33  ; -> 0028BC33
0028BC26  addss    xmm0, xmm9
0028BC2B  movss    dword ptr [rdi + 0xd40], xmm0
0028BC33  movss    xmm0, dword ptr [rdi + 0xd40]
0028BC3B  comiss   xmm0, xmm10
0028BC3F  jbe      0x28bc4e  ; -> 0028BC4E
0028BC41  subss    xmm0, xmm9
0028BC46  movss    dword ptr [rdi + 0xd40], xmm0
0028BC4E  movss    xmm0, dword ptr [rip + 0x1b72466]  ; -> 01DFE0BC [f32 1]
0028BC56  movss    xmm4, dword ptr [rip + 0x63a30a]  ; -> 008C5F68 [f32 0.01745329]
0028BC5E  movss    xmm3, dword ptr [rdi + 0xd44]
0028BC66  mulss    xmm0, xmm4
0028BC6A  comiss   xmm3, xmm0
0028BC6D  jbe      0x28bcb7  ; -> 0028BCB7
0028BC6F  movss    xmm0, dword ptr [rip + 0x1b72441]  ; -> 01DFE0B8 [f32 1]
0028BC77  movaps   xmm1, xmm3
0028BC7A  mulss    xmm0, dword ptr [rip + 0x689f1a]  ; -> 00915B9C [f32 11]
0028BC82  movss    xmm2, dword ptr [rip + 0x68a34a]  ; -> 00915FD4 [f32 0.0001745329]
0028BC8A  divss    xmm1, xmm0
0028BC8E  maxss    xmm2, xmm1
0028BC92  subss    xmm3, xmm2
0028BC96  movss    dword ptr [rdi + 0xd44], xmm3
0028BC9E  movss    xmm0, dword ptr [rip + 0x1b72416]  ; -> 01DFE0BC [f32 1]
0028BCA6  mulss    xmm0, xmm4
0028BCAA  comiss   xmm0, xmm3
0028BCAD  jbe      0x28bcb7  ; -> 0028BCB7
0028BCAF  movss    dword ptr [rdi + 0xd44], xmm0
0028BCB7  mov      edx, dword ptr [rdi + 0xd2c]
0028BCBD  lea      rcx, [rsp + 0x50]
0028BCC2  and      eax, 0xffffffdf
0028BCC5  mov      dword ptr [rdi + 0xd4c], eax
0028BCCB  call     0x2713e0  ; -> 002713E0 fn
0028BCD0  movss    xmm8, dword ptr [rip + 0x1a5fecf]  ; -> 01CEBBA8 [f32 1]
0028BCD9  mov      r13d, 5
0028BCDF  xorps    xmm15, xmm15
0028BCE3  test     eax, eax
0028BCE5  jne      0x28bec4  ; -> 0028BEC4
0028BCEB  movzx    eax, word ptr [rdi + 0xd54]
0028BCF2  cmp      ax, 4
0028BCF6  je       0x28bd18  ; -> 0028BD18
0028BCF8  mov      ecx, 0xfffa
0028BCFD  test     cx, ax
0028BD00  jne      0x28bea5  ; -> 0028BEA5
0028BD06  cmp      ax, 4
0028BD0A  je       0x28bea5  ; -> 0028BEA5
0028BD10  mov      word ptr [rdi + 0xd54], r13w
0028BD18  movss    xmm10, dword ptr [rip + 0x63a24b]  ; -> 008C5F6C [f32 0.1]
0028BD21  movss    xmm6, dword ptr [rip + 0x6673bf]  ; -> 008F30E8 [f32 0.05]
0028BD29  mov      ebx, 4
0028BD2E  movss    xmm7, dword ptr [rip + 0x1a5ff3a]  ; -> 01CEBC70 [f32 4]
0028BD36  movss    xmm9, dword ptr [rip + 0x6897c9]  ; -> 00915508 [f32 0.125]
0028BD3F  lea      r15d, [rbx - 2]
0028BD43  nop      dword ptr [rax]
0028BD47  nop      word ptr [rax + rax]
0028BD50  movzx    eax, word ptr [rdi + 0xd54]
0028BD57  cmp      eax, 1
0028BD5A  je       0x28c189  ; -> 0028C189
0028BD60  jbe      0x28be65  ; -> 0028BE65
0028BD66  cmp      eax, 3
0028BD69  jbe      0x28c1b9  ; -> 0028C1B9
0028BD6F  cmp      eax, ebx
0028BD71  jne      0x28be65  ; -> 0028BE65
0028BD77  movss    xmm1, dword ptr [rdi + 0xd14]
0028BD7F  movaps   xmm0, xmm1
0028BD82  movss    dword ptr [rsp + 0x28], xmm1
0028BD88  mulss    xmm0, dword ptr [rip + 0x68a24c]  ; -> 00915FDC [f32 1.25]
0028BD90  mov      qword ptr [rsp + 0x40], r12
0028BD95  movss    xmm1, dword ptr [rdi + 0xd34]
0028BD9D  mov      dword ptr [rsp + 0x20], 0x437f0000
0028BDA5  movss    dword ptr [rsp + 0x48], xmm0
0028BDAB  movss    xmm0, dword ptr [rip + 0x1b72309]  ; -> 01DFE0BC [f32 1]
0028BDB3  mulss    xmm0, xmm10
0028BDB8  mov      dword ptr [rsp + 0x24], 0x42c80000
0028BDC0  subss    xmm1, xmm0
0028BDC4  comiss   xmm15, xmm1
0028BDC8  movss    dword ptr [rdi + 0xd34], xmm1
0028BDD0  jbe      0x28bdd9  ; -> 0028BDD9
0028BDD2  mov      dword ptr [rdi + 0xd34], r12d
0028BDD9  mov      eax, dword ptr [rdi + 0xd34]
0028BDDF  lea      rcx, [rdi + 0xb0]
0028BDE6  movss    xmm3, dword ptr [rdi + 0xd34]
0028BDEE  lea      r8, [rdi + 0xc50]
0028BDF5  add      rcx, rsi
0028BDF8  mov      dword ptr [rdi + 0xd3c], eax
0028BDFE  lea      rdx, [rdi + 0xc40]
0028BE05  call     0x2754e0  ; -> 002754E0 fn
0028BE0A  movss    xmm3, dword ptr [rdi + 0xd34]
0028BE12  lea      r8, [rsp + 0x20]
0028BE17  lea      rdx, [rsp + 0x40]
0028BE1C  lea      rcx, [rsp + 0x30]
0028BE21  call     0x2754e0  ; -> 002754E0 fn
0028BE26  movss    xmm1, dword ptr [rsp + 0x34]
0028BE2C  mov      rcx, rdi
0028BE2F  movss    xmm0, dword ptr [rsp + 0x30]
0028BE35  movss    dword ptr [rsi + rdi + 0xcc], xmm0
0028BE3E  movss    dword ptr [r14 + rdi + 0xcc], xmm1
0028BE48  movss    xmm1, dword ptr [rsp + 0x38]
0028BE4E  call     0x28cf80  ; -> 0028CF80 fn
0028BE53  comiss   xmm15, dword ptr [rdi + 0xd34]
0028BE5B  jb       0x28be65  ; -> 0028BE65
0028BE5D  mov      word ptr [rdi + 0xd54], r13w
0028BE65  lea      rbx, [rdi + 0x10]
0028BE69  add      rbx, rsi
0028BE6C  mov      rcx, rbx
0028BE6F  call     0x203170  ; -> 00203170 fn
0028BE74  mov      eax, dword ptr [rdi + 0xd4c]
0028BE7A  test     al, 0x40
0028BE7C  je       0x28c3ac  ; -> 0028C3AC
0028BE82  movss    xmm2, dword ptr [rdi + 0xd40]
0028BE8A  mov      rdx, rbx
0028BE8D  mov      rcx, rbx
0028BE90  call     0x202f00  ; -> 00202F00 fn
0028BE95  jmp      0x28c429  ; -> 0028C429
0028BE9A  mov      r14d, 0x990
0028BEA0  jmp      0x28bbd4  ; -> 0028BBD4
0028BEA5  and      dword ptr [rdi + 0xd4c], 0xfffffff7
0028BEAC  mov      eax, 3
0028BEB1  mov      word ptr [rdi + 0xd54], ax
0028BEB8  mov      dword ptr [rdi + 0xd30], r12d
0028BEBF  jmp      0x28bd18  ; -> 0028BD18
0028BEC4  test     byte ptr [rdi + 0xd4c], 2
0028BECB  jne      0x28bee3  ; -> 0028BEE3
0028BECD  lea      rcx, [rdi + 0xc70]
0028BED4  lea      rdx, [rsp + 0x50]
0028BED9  call     0x202c90  ; -> 00202C90 fn
0028BEDE  jmp      0x28bd18  ; -> 0028BD18
0028BEE3  movss    xmm2, dword ptr [rip + 0x1b721d1]  ; -> 01DFE0BC [f32 1]
0028BEEB  movss    xmm3, dword ptr [rdi + 0xd24]
0028BEF3  movaps   xmm0, xmm2
0028BEF6  mulss    xmm0, dword ptr [rip + 0x667202]  ; -> 008F3100 [f32 0.6]
0028BEFE  comiss   xmm0, xmm3
0028BF01  jbe      0x28bf10  ; -> 0028BF10
0028BF03  movaps   xmm1, xmm2
0028BF06  mulss    xmm1, dword ptr [rip + 0x68a0ca]  ; -> 00915FD8 [f32 0.2222222]
0028BF0E  jmp      0x28bf27  ; -> 0028BF27
0028BF10  movaps   xmm1, xmm8
0028BF14  movaps   xmm0, xmm2
0028BF17  mulss    xmm0, dword ptr [rip + 0x68a0b9]  ; -> 00915FD8 [f32 0.2222222]
0028BF1F  subss    xmm1, xmm3
0028BF23  mulss    xmm1, xmm0
0028BF27  mulss    xmm2, dword ptr [rip + 0x639bfd]  ; -> 008C5B2C [f32 0.001]
0028BF2F  lea      r8, [rdi + 0xc80]
0028BF36  lea      rdx, [rsp + 0x50]
0028BF3B  lea      rcx, [rsp + 0x30]
0028BF40  maxss    xmm2, xmm1
0028BF44  addss    xmm2, xmm3
0028BF48  movss    dword ptr [rdi + 0xd24], xmm2
0028BF50  call     0x203080  ; -> 00203080 fn
0028BF55  movss    xmm7, dword ptr [rsp + 0x30]
0028BF5B  cvtps2pd xmm0, xmm7
0028BF5E  andps    xmm0, xmmword ptr [rip + 0x1a5fe1b]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
0028BF65  cvtpd2ps xmm2, xmm0
0028BF69  movss    xmm0, dword ptr [rsp + 0x38]
0028BF6F  cvtps2pd xmm0, xmm0
0028BF72  andps    xmm0, xmmword ptr [rip + 0x1a5fe07]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
0028BF79  cvtpd2ps xmm3, xmm0
0028BF7D  comiss   xmm2, xmm3
0028BF80  jae      0x28bf85  ; -> 0028BF85
0028BF82  movaps   xmm2, xmm3
0028BF85  movss    xmm0, dword ptr [rsp + 0x34]
0028BF8B  movaps   xmm1, xmm2
0028BF8E  call     0x861f02  ; -> 00861F02 fn
0028BF93  movaps   xmm6, xmm0
0028BF96  xorps    xmm6, xmmword ptr [rip + 0x1a5fe03]  ; -> 01CEBDA0 [f32x4 -0, -0, -0, -0]
0028BF9D  comiss   xmm6, dword ptr [rip + 0x639fcc]  ; -> 008C5F70 [f32 1.570796]
0028BFA4  jbe      0x28bfad  ; -> 0028BFAD
0028BFA6  addss    xmm6, xmm11
0028BFAB  jmp      0x28bfbf  ; -> 0028BFBF
0028BFAD  movss    xmm0, dword ptr [rip + 0x68a02f]  ; -> 00915FE4 [f32 -1.570796]
0028BFB5  comiss   xmm0, xmm6
0028BFB8  jb       0x28bfbf  ; -> 0028BFBF
0028BFBA  addss    xmm6, xmm10
0028BFBF  comiss   xmm11, xmm6
0028BFC3  jb       0x28bfca  ; -> 0028BFCA
0028BFC5  addss    xmm6, xmm9
0028BFCA  comiss   xmm6, xmm10
0028BFCE  jbe      0x28bfd8  ; -> 0028BFD8
0028BFD0  addss    xmm6, dword ptr [rip + 0x68964c]  ; -> 00915624 [f32 -6.283185]
0028BFD8  movss    xmm1, dword ptr [rsp + 0x38]
0028BFDE  movaps   xmm0, xmm7
0028BFE1  call     0x861f02  ; -> 00861F02 fn
0028BFE6  movaps   xmm7, xmm0
0028BFE9  comiss   xmm11, xmm7
0028BFED  jb       0x28bff4  ; -> 0028BFF4
0028BFEF  addss    xmm7, xmm9
0028BFF4  comiss   xmm7, xmm10
0028BFF8  jbe      0x28c002  ; -> 0028C002
0028BFFA  addss    xmm7, dword ptr [rip + 0x689622]  ; -> 00915624 [f32 -6.283185]
0028C002  movss    xmm1, dword ptr [rdi + 0xd24]
0028C00A  comiss   xmm1, xmm8
0028C00E  jb       0x28c031  ; -> 0028C031
0028C010  movss    xmm0, dword ptr [rdi + 0xd28]
0028C018  ucomiss  xmm0, xmm15
0028C01C  mov      dword ptr [rdi + 0xd24], 0x3f800000
0028C026  jp       0x28c031  ; -> 0028C031
0028C028  jne      0x28c031  ; -> 0028C031
0028C02A  and      dword ptr [rdi + 0xd4c], 0xfffffff9
0028C031  movss    xmm3, dword ptr [rdi + 0xd24]
0028C039  lea      r8, [rsp + 0x50]
0028C03E  lea      rdx, [rdi + 0xc80]
0028C045  lea      rcx, [rsp + 0x40]
0028C04A  call     0x275490  ; -> 00275490 fn
0028C04F  lea      r8, [rdi + 0xc70]
0028C056  lea      rdx, [rsp + 0x40]
0028C05B  lea      rcx, [rsp + 0x20]
0028C060  call     0x203080  ; -> 00203080 fn
0028C065  lea      rdx, [rsp + 0x40]
0028C06A  mov      dword ptr [rsp + 0x2c], r12d
0028C06F  lea      rcx, [rdi + 0xc70]
0028C076  call     0x202c90  ; -> 00202C90 fn
0028C07B  lea      rcx, [rdi + 0xcb0]
0028C082  lea      rdx, [rsp + 0x20]
0028C087  call     0x202de0  ; -> 00202DE0 fn
0028C08C  lea      rcx, [rsp + 0x20]
0028C091  call     0x270550  ; -> 00270550 fn
0028C096  comiss   xmm0, dword ptr [rdi + 0xd14]
0028C09D  movss    xmm10, dword ptr [rip + 0x639ec6]  ; -> 008C5F6C [f32 0.1]
0028C0A6  movss    dword ptr [rdi + 0xd20], xmm0
0028C0AE  movss    xmm0, dword ptr [rip + 0x1b72006]  ; -> 01DFE0BC [f32 1]
0028C0B6  jbe      0x28c0e2  ; -> 0028C0E2
0028C0B8  mulss    xmm0, dword ptr [rip + 0x1a5faa8]  ; -> 01CEBB68 [f32 0.25]
0028C0C0  addss    xmm0, dword ptr [rdi + 0xd28]
0028C0C8  comiss   xmm0, xmm8
0028C0CC  movss    dword ptr [rdi + 0xd28], xmm0
0028C0D4  jbe      0x28c108  ; -> 0028C108
0028C0D6  mov      dword ptr [rdi + 0xd28], 0x3f800000
0028C0E0  jmp      0x28c108  ; -> 0028C108
0028C0E2  movss    xmm1, dword ptr [rdi + 0xd28]
0028C0EA  mulss    xmm0, xmm10
0028C0EF  subss    xmm1, xmm0
0028C0F3  comiss   xmm15, xmm1
0028C0F7  movss    dword ptr [rdi + 0xd28], xmm1
0028C0FF  jbe      0x28c108  ; -> 0028C108
0028C101  mov      dword ptr [rdi + 0xd28], r12d
0028C108  movss    xmm3, dword ptr [rdi + 0xd28]
0028C110  lea      r8, [rsp + 0x20]
0028C115  lea      rdx, [rsp + 0x40]
0028C11A  movss    dword ptr [rsp + 0x20], xmm6
0028C120  lea      rcx, [rsp + 0x60]
0028C125  mov      dword ptr [rsp + 0x40], r12d
0028C12A  call     0x275490  ; -> 00275490 fn
0028C12F  movss    xmm6, dword ptr [rsp + 0x60]
0028C135  lea      rcx, [rdi + 0xcc0]
0028C13C  call     0x203170  ; -> 00203170 fn
0028C141  movaps   xmm2, xmm6
0028C144  lea      rdx, [rdi + 0xcc0]
0028C14B  lea      rcx, [rdi + 0xcc0]
0028C152  call     0x202e90  ; -> 00202E90 fn
0028C157  movaps   xmm2, xmm7
0028C15A  lea      rdx, [rdi + 0xcc0]
0028C161  lea      rcx, [rdi + 0xcc0]
0028C168  call     0x202f00  ; -> 00202F00 fn
0028C16D  xorps    xmm7, xmmword ptr [rip + 0x1a5fc2c]  ; -> 01CEBDA0 [f32x4 -0, -0, -0, -0]
0028C174  lea      rdx, [rbp - 0x50]
0028C178  movaps   xmm2, xmm7
0028C17B  lea      rcx, [rbp - 0x50]
0028C17F  call     0x202f00  ; -> 00202F00 fn
0028C184  jmp      0x28bd21  ; -> 0028BD21
0028C189  lea      rcx, [rdi + 0xb0]
0028C190  movaps   xmm3, xmm8
0028C194  add      rcx, r14
0028C197  lea      r8, [rdi + 0xc60]
0028C19E  lea      rdx, [rdi + 0xc40]
0028C1A5  call     0x2754e0  ; -> 002754E0 fn
0028C1AA  or       dword ptr [rdi + 0xd4c], 1
0028C1B1  mov      word ptr [rdi + 0xd54], r15w
0028C1B9  comiss   xmm8, dword ptr [rdi + 0xd34]
0028C1C1  ja       0x28c1db  ; -> 0028C1DB
0028C1C3  comiss   xmm8, dword ptr [rdi + 0xd3c]
0028C1CB  ja       0x28c1db  ; -> 0028C1DB
0028C1CD  comiss   xmm8, dword ptr [rdi + 0xd38]
0028C1D5  jbe      0x28c371  ; -> 0028C371
0028C1DB  movss    xmm0, dword ptr [rdi + 0xd18]
0028C1E3  movaps   xmm1, xmm8
0028C1E7  subss    xmm1, dword ptr [rdi + 0xd34]
0028C1EF  movss    xmm2, dword ptr [rip + 0x1b71ec5]  ; -> 01DFE0BC [f32 1]
0028C1F7  movss    dword ptr [rsp + 0x48], xmm0
0028C1FD  movss    xmm0, dword ptr [rdi + 0xd14]
0028C205  movss    dword ptr [rsp + 0x38], xmm0
0028C20B  movss    xmm0, dword ptr [rip + 0x1b71ea5]  ; -> 01DFE0B8 [f32 1]
0028C213  mulss    xmm0, xmm7
0028C217  mov      qword ptr [rsp + 0x40], r12
0028C21C  mulss    xmm2, xmm6
0028C220  mov      dword ptr [rsp + 0x30], 0x437f0000
0028C228  divss    xmm1, xmm0
0028C22C  mov      dword ptr [rsp + 0x34], 0x42c80000
0028C234  maxss    xmm2, xmm1
0028C238  addss    xmm2, dword ptr [rdi + 0xd34]
0028C240  comiss   xmm2, xmm8
0028C244  movss    dword ptr [rdi + 0xd34], xmm2
0028C24C  jbe      0x28c25f  ; -> 0028C25F
0028C24E  or       dword ptr [rdi + 0xd4c], 0x10
0028C255  mov      dword ptr [rdi + 0xd34], 0x3f800000
0028C25F  movss    xmm0, dword ptr [rip + 0x1b71e51]  ; -> 01DFE0B8 [f32 1]
0028C267  movaps   xmm1, xmm8
0028C26B  subss    xmm1, dword ptr [rdi + 0xd38]
0028C273  movss    xmm2, dword ptr [rip + 0x1b71e41]  ; -> 01DFE0BC [f32 1]
0028C27B  mulss    xmm0, xmm7
0028C27F  mulss    xmm2, xmm6
0028C283  divss    xmm1, xmm0
0028C287  maxss    xmm2, xmm1
0028C28B  addss    xmm2, dword ptr [rdi + 0xd38]
0028C293  comiss   xmm2, xmm8
0028C297  movss    dword ptr [rdi + 0xd38], xmm2
0028C29F  jbe      0x28c2b2  ; -> 0028C2B2
0028C2A1  or       dword ptr [rdi + 0xd4c], 0x10
0028C2A8  mov      dword ptr [rdi + 0xd38], 0x3f800000
0028C2B2  movss    xmm3, dword ptr [rdi + 0xd34]
0028C2BA  lea      rcx, [rdi + 0xb0]
0028C2C1  add      rcx, rsi
0028C2C4  lea      r8, [rdi + 0xc50]
0028C2CB  lea      rdx, [rdi + 0xc40]
0028C2D2  call     0x2754e0  ; -> 002754E0 fn
0028C2D7  movss    xmm0, dword ptr [rip + 0x1b71ddd]  ; -> 01DFE0BC [f32 1]
0028C2DF  mulss    xmm0, xmm9
0028C2E4  addss    xmm0, dword ptr [rdi + 0xd3c]
0028C2EC  comiss   xmm0, xmm8
0028C2F0  movss    dword ptr [rdi + 0xd3c], xmm0
0028C2F8  jbe      0x28c304  ; -> 0028C304
0028C2FA  mov      dword ptr [rdi + 0xd3c], 0x3f800000
0028C304  movss    xmm3, dword ptr [rdi + 0xd3c]
0028C30C  lea      r8, [rsp + 0x30]
0028C311  lea      rdx, [rsp + 0x40]
0028C316  lea      rcx, [rsp + 0x20]
0028C31B  call     0x2754e0  ; -> 002754E0 fn
0028C320  movss    xmm0, dword ptr [rsp + 0x20]
0028C326  lea      r8, [rsp + 0x30]
0028C32B  movss    xmm1, dword ptr [rsp + 0x24]
0028C331  lea      rdx, [rsp + 0x40]
0028C336  movss    dword ptr [rsi + rdi + 0xcc], xmm0
0028C33F  lea      rcx, [rsp + 0x20]
0028C344  movss    dword ptr [r14 + rdi + 0xcc], xmm1
0028C34E  movss    xmm3, dword ptr [rdi + 0xd38]
0028C356  call     0x2754e0  ; -> 002754E0 fn
0028C35B  movss    xmm1, dword ptr [rsp + 0x28]
0028C361  mov      rcx, rdi
0028C364  movss    dword ptr [rdi + 0xd1c], xmm1
0028C36C  call     0x28cf80  ; -> 0028CF80 fn
0028C371  cmp      word ptr [rdi + 0xd54], 3
0028C379  jne      0x28be65  ; -> 0028BE65
0028C37F  inc      dword ptr [rdi + 0xd30]
0028C385  movss    xmm0, dword ptr [rdi + 0xd34]
0028C38D  comiss   xmm0, xmm8
0028C391  jae      0x28c3a0  ; -> 0028C3A0
0028C393  test     byte ptr [rdi + 0xd4c], 0x10
0028C39A  je       0x28be65  ; -> 0028BE65
0028C3A0  mov      word ptr [rdi + 0xd54], bx
0028C3A7  jmp      0x28bd50  ; -> 0028BD50
0028C3AC  test     r15b, al
0028C3AF  je       0x28c429  ; -> 0028C429
0028C3B1  movss    xmm1, dword ptr [rdi + 0xd20]
0028C3B9  lea      rcx, [rsp + 0x70]
0028C3BE  movss    xmm7, dword ptr [rip + 0x1a5f7aa]  ; -> 01CEBB70 [f32 0.5]
0028C3C6  movss    xmm6, dword ptr [rip + 0x67576e]  ; -> 00901B3C [f32 1.5]
0028C3CE  mulss    xmm1, xmm7
0028C3D2  movaps   xmm0, xmm1
0028C3D5  addss    xmm0, xmm8
0028C3DA  subss    xmm8, xmm1
0028C3DF  minss    xmm6, xmm0
0028C3E3  maxss    xmm7, xmm8
0028C3E8  movss    dword ptr [rsi + rdi + 0x38], xmm6
0028C3EE  movss    dword ptr [rbx], xmm7
0028C3F2  call     0x203170  ; -> 00203170 fn
0028C3F7  lea      r8, [rbp - 0x50]
0028C3FB  movss    dword ptr [rsp + 0x70], xmm7
0028C401  lea      rdx, [rsp + 0x70]
0028C406  movss    dword ptr [rbp - 0x68], xmm6
0028C40B  lea      rcx, [rsp + 0x70]
0028C410  call     0x202d70  ; -> 00202D70 fn
0028C415  lea      rdx, [rdi + 0xcc0]
0028C41C  mov      rcx, rbx
0028C41F  lea      r8, [rsp + 0x70]
0028C424  call     0x202d70  ; -> 00202D70 fn
0028C429  lea      rcx, [rdi + 0x40]
0028C42D  add      rcx, rsi
0028C430  lea      rdx, [rdi + 0xc70]
0028C437  call     0x202c90  ; -> 00202C90 fn
0028C43C  lea      rcx, [rdi + 0x10]
0028C440  mov      dword ptr [rsi + rdi + 0x4c], 0x3f800000
0028C448  add      rcx, r14
0028C44B  mov      rdx, rbx
0028C44E  call     0x202c70  ; -> 00202C70 fn
0028C453  mov      rcx, qword ptr [rbp - 0x10]
0028C457  xor      rcx, rsp
0028C45A  call     0x808c40  ; -> 00808C40 fn
0028C45F  lea      r11, [rsp + 0x170]
0028C467  mov      rbx, qword ptr [r11 + 0x38]
0028C46B  mov      rsi, qword ptr [r11 + 0x40]
0028C46F  mov      rdi, qword ptr [r11 + 0x48]
0028C473  movaps   xmm6, xmmword ptr [r11 - 0x10]
0028C478  movaps   xmm7, xmmword ptr [r11 - 0x20]
0028C47D  movaps   xmm8, xmmword ptr [r11 - 0x30]
0028C482  movaps   xmm9, xmmword ptr [r11 - 0x40]
0028C487  movaps   xmm10, xmmword ptr [r11 - 0x50]
0028C48C  movaps   xmm11, xmmword ptr [r11 - 0x60]
0028C491  movaps   xmm15, xmmword ptr [r11 - 0x70]
0028C496  mov      rsp, r11
0028C499  pop      r15
0028C49B  pop      r14
0028C49D  pop      r13
0028C49F  pop      r12
0028C4A1  pop      rbp
0028C4A2  ret      
```
