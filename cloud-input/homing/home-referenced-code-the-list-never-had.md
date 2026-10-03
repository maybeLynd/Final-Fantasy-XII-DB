# Homing pack: `99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-referenced-code-the-list-never-had.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0037A960 (69 B, extent 0037A960-0037A9A5)

Entered from (direct sites whose caller this page cites): `003DEA10` + 0x8 (jmp; `003DEA10` is cited on this page)
Other direct sites: none

Host context: "eturns on both paths; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | '00379F53', '00379F5B' | | '0037AA00' | 69 B | entered by a conditional jump ('jne') from '003DEA10' + 0x2; it starts right after 'int3' padding; it forms 'r8' = '02EBF420' + sign-extended 'ecx' times 0x50 and loads qword '+0x18' of it; when that qword is null or dword '+0x4' of its target is zero it returns; otherwise for each i"

```
0037A960  movsxd   rax, ecx
0037A963  lea      r8, [rax + rax*4]
0037A967  shl      r8, 4
0037A96B  lea      rax, [rip + 0x2b44aae]  ; -> 02EBF420
0037A972  add      r8, rax
0037A975  mov      rcx, qword ptr [r8 + 0x18]
0037A979  test     rcx, rcx
0037A97C  je       0x37a9a4  ; -> 0037A9A4
0037A97E  xor      eax, eax
0037A980  cmp      dword ptr [rcx + 4], eax
0037A983  jbe      0x37a9a4  ; -> 0037A9A4
0037A985  mov      edx, eax
0037A987  nop      word ptr [rax + rax]
0037A990  mov      byte ptr [rdx + rcx + 0x12], 0
0037A995  lea      rdx, [rdx + 8]
0037A999  mov      rcx, qword ptr [r8 + 0x18]
0037A99D  inc      eax
0037A99F  cmp      eax, dword ptr [rcx + 4]
0037A9A2  jb       0x37a990  ; -> 0037A990
0037A9A4  ret      
```

## 003B1560 (86 B, extent 003B1560-003B15B6)

Entered from (direct sites whose caller this page cites): `0036E9A0` + 0x0 (jmp; `0036E9A0` is cited on this page)
Other direct sites: none

Host context: "| | '002697F0' | 10 | '0050E390' | 'edx := 1', tail-jumps '00269860' | | '0026AF70' | 7 | '0034D350' | global byte '02099DA0' := 'cl' | | '0026DC50' | 5 | '00350320', '003505F0' | 'jmp 002ECD20' | | '0036E9A0' | 5 | '00340010' | 'jmp 003B1560' |  '003594C0' is the second of the two the database already had: the party page names it.  **Twelve of the fourteen are named nowhere else in this database**, and their callers are: '_index/ADDRES"

```
003B1560  mov      qword ptr [rsp + 8], rbx
003B1565  mov      qword ptr [rsp + 0x10], rsi
003B156A  push     rdi
003B156B  sub      rsp, 0x20
003B156F  mov      edi, ecx
003B1571  lea      rbx, [rip + 0x2b0d088]  ; -> 02EBE600
003B1578  lea      rsi, [rip + 0x2b0d681]  ; -> 02EBEC00
003B157F  nop      
003B1580  mov      ecx, dword ptr [rbx - 0x20]
003B1583  test     ecx, ecx
003B1585  je       0x3b15a6  ; -> 003B15A6
003B1587  movzx    eax, byte ptr [rbx]
003B158A  test     al, 1
003B158C  je       0x3b159d  ; -> 003B159D
003B158E  test     edi, edi
003B1590  je       0x3b1599  ; -> 003B1599
003B1592  call     0x3b18e0  ; -> 003B18E0 fn
003B1597  jmp      0x3b159d  ; -> 003B159D
003B1599  and      al, 0xfe
003B159B  mov      byte ptr [rbx], al
003B159D  add      rbx, 0x30
003B15A1  cmp      rbx, rsi
003B15A4  jl       0x3b1580  ; -> 003B1580
003B15A6  mov      rbx, qword ptr [rsp + 0x30]
003B15AB  mov      rsi, qword ptr [rsp + 0x38]
003B15B0  add      rsp, 0x20
003B15B4  pop      rdi
003B15B5  ret      
```
