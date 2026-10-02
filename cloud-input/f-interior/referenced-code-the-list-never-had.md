# F-interior pack: `99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/referenced-code-the-list-never-had.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 00263A30 (109 B, extent 00263A30-00263A9D)

Page context: "l-jumps '0025B500'. **Already known** - the movement-mode page found it by hand | | '0025D9C0' | 18 | '0034C880' | loads the global at '02099D70', passes 'word [rcx]' and '[global+0x28]', tail-jumps '00263A30' | | '002697F0' | 10 | '0050E390' | 'edx := 1', tail-jumps '00269860' | | '0026AF70' | 7 | '0034D350' | global byte '02099DA0' := 'cl' | | '0026DC50' | 5 | '00350320', '003505F0' | 'jmp 002ECD20' | | '0036E9A0' | 5 | '00340010' | '"

```
00263A30  push     rbx
00263A32  sub      rsp, 0x20
00263A36  lea      rbx, [rip + 0x6b1ccb]  ; -> 00915708 [str "NOACTOR"]
00263A3D  cmp      ecx, 4
00263A40  ja       0x263a94  ; -> 00263A94
00263A42  movsxd   rax, ecx
00263A45  imul     rcx, rax, 0x288
00263A4C  lea      rax, [rip + 0x1e353bd]  ; -> 02098E10
00263A53  add      rcx, rax
00263A56  je       0x263a94  ; -> 00263A94
00263A58  test     byte ptr [rcx + 0x10], 1
00263A5C  je       0x263a94  ; -> 00263A94
00263A5E  mov      qword ptr [rsp + 0x30], rdi
00263A63  mov      rdi, qword ptr [rcx]
00263A66  test     rdi, rdi
00263A69  je       0x263a8f  ; -> 00263A8F
00263A6B  cmp      edx, dword ptr [rcx + 0x20]
00263A6E  jge      0x263a8f  ; -> 00263A8F
00263A70  call     0x358940  ; -> 00358940 fn
00263A75  test     rax, rax
00263A78  je       0x263a8f  ; -> 00263A8F
00263A7A  mov      rax, qword ptr [rax + 0x40]
00263A7E  test     rax, rax
00263A81  je       0x263a8f  ; -> 00263A8F
00263A83  mov      ecx, dword ptr [rdi + 0x4c]
00263A86  movsxd   rbx, dword ptr [rax]
00263A89  add      rcx, rdi
00263A8C  add      rbx, rcx
00263A8F  mov      rdi, qword ptr [rsp + 0x30]
00263A94  mov      rax, rbx
00263A97  add      rsp, 0x20
00263A9B  pop      rbx
00263A9C  ret      
```

## 0034ED80 (56 B, extent 0034ED80-0034EDB8)

Page context: "d code.** The remaining **fourteen have a caller the function list does contain**, and every one of those fourteen is reached by a **tail 'jmp'**, never a 'call'.  > That is the shape of the defect. '0034ED80' is listed at 56 bytes; its real body is **eleven**, > ending 'jmp 0x2ec3c0'. The recorded size then runs past the padding and swallows a **second, > unrelated function**. The list took the thunk, gave it the wrong length, and neve"

```
0034ED80  mov      rcx, rdx
0034ED83  mov      edx, 1
0034ED88  jmp      0x2ec3c0  ; -> 002EC3C0 fn
0034ED8D  int3     
0034ED8E  int3     
0034ED8F  int3     
0034ED90  sub      rsp, 0x28
0034ED94  mov      rcx, r9
0034ED97  call     0x267e10  ; -> 00267E10 fn
0034ED9C  mov      ecx, eax
0034ED9E  add      rsp, 0x28
0034EDA2  jmp      0x3e8fe0  ; -> 003E8FE0 fn
0034EDA7  int3     
0034EDA8  int3     
0034EDA9  int3     
0034EDAA  int3     
0034EDAB  int3     
0034EDAC  int3     
0034EDAD  int3     
0034EDAE  int3     
0034EDAF  int3     
0034EDB0  mov      qword ptr [rsp + 8], rbx
```

## 00350320 (56 B, extent 00350320-00350358)

Page context: " and '[global+0x28]', tail-jumps '00263A30' | | '002697F0' | 10 | '0050E390' | 'edx := 1', tail-jumps '00269860' | | '0026AF70' | 7 | '0034D350' | global byte '02099DA0' := 'cl' | | '0026DC50' | 5 | '00350320', '003505F0' | 'jmp 002ECD20' | | '0036E9A0' | 5 | '00340010' | 'jmp 003B1560' |  '003594C0' is the second of the two the database already had: the party page names it.  **Twelve of the fourteen are named nowhere else in this datab"

```
00350320  mov      rcx, rdx
00350323  xor      edx, edx
00350325  jmp      0x26dc50  ; -> 0026DC50 fn
0035032A  int3     
0035032B  int3     
0035032C  int3     
0035032D  int3     
0035032E  int3     
0035032F  int3     
00350330  sub      rsp, 0x28
00350334  mov      rcx, r9
00350337  call     0x267db0  ; -> 00267DB0 fn
0035033C  add      rsp, 0x28
00350340  jmp      0x17e7d0  ; -> 0017E7D0 fn
00350345  int3     
00350346  int3     
00350347  int3     
00350348  int3     
00350349  int3     
0035034A  int3     
0035034B  int3     
0035034C  int3     
0035034D  int3     
0035034E  int3     
0035034F  int3     
00350350  push     rbx
00350352  sub      rsp, 0x20
```

## 00354950 (33 B, extent 00354950-00354971)

Page context: " of a pending request; corrected 2026-09-18 (FABLE) | | '00269E00' | 24 | '00353630', '00353A50' | '[rcx+0x14]' **bit 5** := 'dl & 1'; when 'edx' is zero, tail-jumps '0025B500' | | '003DE3E0' | 23 | '00354950' | global byte '02B58C3C' bit 0 := 'ecx != 0' | | '00269F00' | 21 | '00353D00', '00354910' | '[rcx+0x08]' **bit 0** := 'dl & 1'; when 'edx' is zero, tail-jumps '0025B500'. **Already known** - the movement-mode page found it by hand"

```
00354950  mov      ecx, 1
00354955  jmp      0x3de3e0  ; -> 003DE3E0 fn
0035495A  int3     
0035495B  int3     
0035495C  int3     
0035495D  int3     
0035495E  int3     
0035495F  int3     
00354960  jmp      0x2efd50  ; -> 002EFD50 fn
00354965  int3     
00354966  int3     
00354967  int3     
00354968  int3     
00354969  int3     
0035496A  int3     
0035496B  int3     
0035496C  int3     
0035496D  int3     
0035496E  int3     
0035496F  int3     
```
