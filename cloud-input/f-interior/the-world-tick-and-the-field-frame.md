# F-interior pack: `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-world-tick-and-the-field-frame.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 00340970 (118 B, extent 00340970-003409E6)

Page context: "rs bit 0 of dword '022C7D04' and byte '022C7CE9' | '0033B6D4' call, '0033B6D9' and, '0033B6E0' mov | | '003574B0' | 115 B | calls '00267E10(r9)' and '00267F90(r9, 0)', forwards its four arguments to '00340970', calls '00263FF0(0)', '002348E0' and '0035A6F0', and tail-calls '00269800' with '00263FF0''s result | '003574D3' call, '003574EE' call, '003574F5' call, '00357502' call, '0035751E' jmp | | '003586A0' | 31 B | sets bit 'ecx' of byt"

```
00340970  mov      qword ptr [rsp + 8], rbx
00340975  push     rdi
00340976  sub      rsp, 0x20
0034097A  mov      rbx, r9
0034097D  call     0x2640c0  ; -> 002640C0 fn
00340982  mov      rcx, rbx
00340985  mov      rdi, rax
00340988  call     0x267e10  ; -> 00267E10 fn
0034098D  mov      r8d, eax
00340990  xor      edx, edx
00340992  mov      rcx, rdi
00340995  mov      ebx, eax
00340997  call     0x25ae00  ; -> 0025AE00 fn
0034099C  mov      r8d, ebx
0034099F  mov      edx, 1
003409A4  mov      rcx, rdi
003409A7  call     0x25ae00  ; -> 0025AE00 fn
003409AC  mov      r8d, ebx
003409AF  mov      edx, 4
003409B4  mov      rcx, rdi
003409B7  call     0x25ae00  ; -> 0025AE00 fn
003409BC  mov      r8d, ebx
003409BF  mov      edx, 2
003409C4  mov      rcx, rdi
003409C7  call     0x25ae00  ; -> 0025AE00 fn
003409CC  mov      r8d, ebx
003409CF  mov      edx, 3
003409D4  mov      rcx, rdi
003409D7  mov      rbx, qword ptr [rsp + 0x30]
003409DC  add      rsp, 0x20
003409E0  pop      rdi
003409E1  jmp      0x25ae00  ; -> 0025AE00 fn
```

## 003DF810 (208 B, extent 003DF810-003DF8E0)

Page context: "' mov, '003DC7C3' je | | '003DF670' | 108 B | clears bit 0 of dword '02B59D18' when '003588B0(003590D0())' returns an actor that '002EA6A0' accepts, else sets it; when the dword is then 0 tail-calls '003DF810', otherwise calls '0029CAB0(0, 0, 0, 0)' and zeroes dwords '02B59D14', '02B59D10' and qwords '02B59D08', '02B59D00' | '003DF67B' call, '003DF691' and, '003DF69A' or, '003DF6A7' jmp, '003DF6B6' call, '003DF6D0' mov | | '003E1310' | "

```
003DF810  push     rbp
003DF812  sub      rsp, 0x20
003DF816  mov      ecx, 7
003DF81B  lea      rax, [rip + 0x277a4ba]  ; -> 02B59CDC
003DF822  lea      rdx, [rip + 0x277a497]  ; -> 02B59CC0
003DF829  nop      dword ptr [rax]
003DF830  mov      ebp, dword ptr [rax]
003DF832  test     ebp, ebp
003DF834  jne      0x3df872  ; -> 003DF872
003DF836  dec      ecx
003DF838  sub      rax, 4
003DF83C  cmp      rax, rdx
003DF83F  jge      0x3df830  ; -> 003DF830
003DF841  xor      r9d, r9d
003DF844  xor      r8d, r8d
003DF847  xor      edx, edx
003DF849  xor      ecx, ecx
003DF84B  call     0x29cab0  ; -> 0029CAB0 fn
003DF850  xor      eax, eax
003DF852  mov      qword ptr [rip + 0x277a4a7], rax  ; -> 02B59D00
003DF859  mov      qword ptr [rip + 0x277a4a8], rax  ; -> 02B59D08
003DF860  mov      dword ptr [rip + 0x277a4aa], eax  ; -> 02B59D10
003DF866  mov      dword ptr [rip + 0x277a4a8], eax  ; -> 02B59D14
003DF86C  add      rsp, 0x20
003DF870  pop      rbp
003DF871  ret      
003DF872  movsxd   rax, ecx
003DF875  mov      edx, ebp
003DF877  lea      rcx, [rip - 0x2bf87e]  ; -> 00120000 (image base)
003DF87E  mov      qword ptr [rsp + 0x30], rbx
003DF883  mov      qword ptr [rsp + 0x38], rsi
003DF888  mov      qword ptr [rsp + 0x40], rdi
003DF88D  mov      rsi, qword ptr [rcx + rax*8 + 0x2a39c80]  ; image base + 0x2a39c80 = 02B59C80
003DF895  mov      rdi, qword ptr [rcx + rax*8 + 0x2a39c40]  ; image base + 0x2a39c40 = 02B59C40
003DF89D  mov      r9, rsi
003DF8A0  mov      ebx, dword ptr [rcx + rax*4 + 0x2a39ce0]  ; image base + 0x2a39ce0 = 02B59CE0
003DF8A7  mov      r8, rdi
003DF8AA  mov      ecx, ebx
003DF8AC  call     0x29cab0  ; -> 0029CAB0 fn
003DF8B1  mov      qword ptr [rip + 0x277a448], rdi  ; -> 02B59D00
003DF8B8  mov      rdi, qword ptr [rsp + 0x40]
003DF8BD  mov      qword ptr [rip + 0x277a444], rsi  ; -> 02B59D08
003DF8C4  mov      rsi, qword ptr [rsp + 0x38]
003DF8C9  mov      dword ptr [rip + 0x277a445], ebx  ; -> 02B59D14
003DF8CF  mov      rbx, qword ptr [rsp + 0x30]
003DF8D4  mov      dword ptr [rip + 0x277a436], ebp  ; -> 02B59D10
003DF8DA  add      rsp, 0x20
003DF8DE  pop      rbp
003DF8DF  ret      
```

## 003EB470 (129 B, extent 003EB470-003EB4F1)

Page context: " | calls '00408200' when byte '02B5D090' is set, then clears the byte | '003E910D' call, '003E9112' mov | | '003EB6C0' | 59 B | for an index up to '0x1F', releases the pointer '02B5EA20[index]' with '003EB470' when it is non-null and nulls it | '003EB6C4' cmp, '003EB6E5' call, '003EB6EA' mov | | '003EC5F0' | 42 B | for i = 0 to 15 calls '003EB6C0(i)' whenever '00377C20()' returns 0 | '003EC5F8' call, '003EC608' call, '003EC60F' cmp | | "

```
003EB470  test     rcx, rcx
003EB473  je       0x3eb4f0  ; -> 003EB4F0
003EB475  push     rdi
003EB476  sub      rsp, 0x20
003EB47A  mov      rdi, rcx
003EB47D  mov      qword ptr [rsp + 0x30], rbx
003EB482  mov      ecx, dword ptr [rcx + 0x10]
003EB485  call     0x2ed470  ; -> 002ED470 fn
003EB48A  mov      rcx, qword ptr [rdi + 0x18]
003EB48E  call     0x2eb870  ; -> 002EB870 fn
003EB493  lea      rcx, [rdi + 0x10]
003EB497  call     0x265f90  ; -> 00265F90 fn
003EB49C  mov      rcx, qword ptr [rdi]
003EB49F  mov      rax, qword ptr [rdi + 8]
003EB4A3  mov      rbx, qword ptr [rsp + 0x30]
003EB4A8  test     rcx, rcx
003EB4AB  je       0x3eb4b1  ; -> 003EB4B1
003EB4AD  mov      qword ptr [rcx + 8], rax
003EB4B1  test     rax, rax
003EB4B4  je       0x3eb4b9  ; -> 003EB4B9
003EB4B6  mov      qword ptr [rax], rcx
003EB4B9  xor      eax, eax
003EB4BB  mov      qword ptr [rdi], rax
003EB4BE  mov      qword ptr [rdi + 8], rax
003EB4C2  mov      rax, qword ptr [rip + 0x27736a7]  ; -> 02B5EB70
003EB4C9  mov      qword ptr [rip + 0x27736a0], rdi  ; -> 02B5EB70
003EB4D0  test     rax, rax
003EB4D3  je       0x3eb4d9  ; -> 003EB4D9
003EB4D5  mov      qword ptr [rax + 8], rdi
003EB4D9  lea      rcx, [rip + 0x2773690]  ; -> 02B5EB70
003EB4E0  mov      qword ptr [rdi], rax
003EB4E3  mov      qword ptr [rdi + 8], rcx
003EB4E7  mov      byte ptr [rdi + 0x40], 0
003EB4EB  add      rsp, 0x20
003EB4EF  pop      rdi
003EB4F0  ret      
```

## 003EF750 (20 B, extent 003EF750-003EF764)

Page context: ", 0)' and '00252B40(0xB, 1)', sets dword '+0xC8' of the '+0xC0' object of '*0209AC30' to 2, calls '00245020' on its '+0xB8', clears byte '+0xDEE', calls '00251E80', sets byte '+0xDEF' and tail-calls '003EF750' | '0027EFBE' call, '0027EFC8' call, '0027EFE8' mov, '0027F00C' mov, '0027F01F' mov | | '002805D0' | 127 B | returns 0 unless '0035C740()' is non-zero, the '*0209AC30' block has non-null '+0xC0' and '+0xB8', that '+0xB8' object's d"

```
003EF750  xor      r8d, r8d
003EF753  lea      rdx, [rip + 0xd6]  ; -> 003EF830
003EF75A  mov      ecx, 0x108
003EF75F  jmp      0x244f50  ; -> 00244F50 fn
```
