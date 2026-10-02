# F-interior pack: `01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-script-to-native-calling-convention.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; inbox mentions: FABLE.md). OPUS read these before packing.

## 0034E5C0 (103 B, extent 0034E5C0-0034E627)

Page context: "tes '0'–'7' / '1'–'5'   ([the list-wait census](../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md)). - **Script verbs, which no earlier census covered.** 'sysreq' ('0x00AA', '0034E5C0') and 'sysreqf'   ('0x0228', '0034EC80') pop class, ordinal, then channel, and call '00269A90'. That bounds the class   ('< 0x12') and the ordinal ('0 ≤ ordinal < count', '00269ABB') but **not the channel**, which   '00269BA0' pass"

```
0034E5C0  mov      qword ptr [rsp + 8], rbx
0034E5C5  mov      qword ptr [rsp + 0x10], rbp
0034E5CA  mov      qword ptr [rsp + 0x18], rsi
0034E5CF  push     rdi
0034E5D0  sub      rsp, 0x30
0034E5D4  mov      rsi, r9
0034E5D7  call     0x2640c0  ; -> 002640C0 fn
0034E5DC  mov      rcx, rsi
0034E5DF  mov      ebp, dword ptr [rax + 0x28]
0034E5E2  call     0x267e10  ; -> 00267E10 fn
0034E5E7  mov      rcx, rsi
0034E5EA  mov      edi, eax
0034E5EC  call     0x267e10  ; -> 00267E10 fn
0034E5F1  mov      rcx, rsi
0034E5F4  mov      ebx, eax
0034E5F6  call     0x267e10  ; -> 00267E10 fn
0034E5FB  mov      r9d, edi
0034E5FE  mov      dword ptr [rsp + 0x20], 0
0034E606  mov      r8d, eax
0034E609  mov      edx, ebx
0034E60B  mov      ecx, ebp
0034E60D  call     0x269a90  ; -> 00269A90 fn
0034E612  mov      rbx, qword ptr [rsp + 0x40]
0034E617  mov      rbp, qword ptr [rsp + 0x48]
0034E61C  mov      rsi, qword ptr [rsp + 0x50]
0034E621  add      rsp, 0x30
0034E625  pop      rdi
0034E626  ret      
```

## 0034EC80 (103 B, extent 0034EC80-0034ECE7)

Page context: " census](../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md)). - **Script verbs, which no earlier census covered.** 'sysreq' ('0x00AA', '0034E5C0') and 'sysreqf'   ('0x0228', '0034EC80') pop class, ordinal, then channel, and call '00269A90'. That bounds the class   ('< 0x12') and the ordinal ('0 ≤ ordinal < count', '00269ABB') but **not the channel**, which   '00269BA0' passes on as 'edx'. 'sysreqall' ('0x00AB', "

```
0034EC80  mov      qword ptr [rsp + 8], rbx
0034EC85  mov      qword ptr [rsp + 0x10], rbp
0034EC8A  mov      qword ptr [rsp + 0x18], rsi
0034EC8F  push     rdi
0034EC90  sub      rsp, 0x30
0034EC94  mov      rsi, r9
0034EC97  call     0x2640c0  ; -> 002640C0 fn
0034EC9C  mov      rcx, rsi
0034EC9F  mov      ebp, dword ptr [rax + 0x28]
0034ECA2  call     0x267e10  ; -> 00267E10 fn
0034ECA7  mov      rcx, rsi
0034ECAA  mov      edi, eax
0034ECAC  call     0x267e10  ; -> 00267E10 fn
0034ECB1  mov      rcx, rsi
0034ECB4  mov      ebx, eax
0034ECB6  call     0x267e10  ; -> 00267E10 fn
0034ECBB  mov      r9d, edi
0034ECBE  mov      dword ptr [rsp + 0x20], 1
0034ECC6  mov      r8d, eax
0034ECC9  mov      edx, ebx
0034ECCB  mov      ecx, ebp
0034ECCD  call     0x269a90  ; -> 00269A90 fn
0034ECD2  mov      rbx, qword ptr [rsp + 0x40]
0034ECD7  mov      rbp, qword ptr [rsp + 0x48]
0034ECDC  mov      rsi, qword ptr [rsp + 0x50]
0034ECE1  add      rsp, 0x30
0034ECE5  pop      rdi
0034ECE6  ret      
```

## 0034F380 (61 B, extent 0034F380-0034F3BD)

Page context: "el, and call '00269A90'. That bounds the class   ('< 0x12') and the ordinal ('0 ≤ ordinal < count', '00269ABB') but **not the channel**, which   '00269BA0' passes on as 'edx'. 'sysreqall' ('0x00AB', '0034F380') pops class, then channel, into   '00269AD0'. In all three the channel is the **first-pushed argument**.   ['members/sysreq_channel_census.py'](members/sysreq_channel_census.py) →   ['members/sysreq-channel-census.tsv'](members/sy"

```
0034F380  mov      qword ptr [rsp + 8], rbx
0034F385  push     rdi
0034F386  sub      rsp, 0x20
0034F38A  mov      rcx, r9
0034F38D  mov      rbx, r9
0034F390  call     0x267e10  ; -> 00267E10 fn
0034F395  mov      rcx, rbx
0034F398  mov      edi, eax
0034F39A  call     0x267e10  ; -> 00267E10 fn
0034F39F  mov      ebx, eax
0034F3A1  call     0x2640c0  ; -> 002640C0 fn
0034F3A6  mov      r8d, edi
0034F3A9  mov      edx, ebx
0034F3AB  mov      ecx, dword ptr [rax + 0x28]
0034F3AE  mov      rbx, qword ptr [rsp + 0x30]
0034F3B3  add      rsp, 0x20
0034F3B7  pop      rdi
0034F3B8  jmp      0x269ad0  ; -> 00269AD0 fn
```

## 00394600 (30 B, extent 00394600-0039461E)

Page context: "d callees outside the census: '00244F50', '00808C40'. The '0023FBE0' descriptor and the '0x4D8' selector are the shared submit contract; '01EFAC11' is the sibling-paired flag byte ('01EFAC10' is the '00394600' twin's gate).  ## The '00511F20'/'00512130' exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)  | root | member (target) | role | interior | | --- | --- | --- | --- | | '00511F20' | '00394600' | 'byte[01EFAC"

```
00394600  cmp      byte ptr [rip + 0x1b66609], 2  ; -> 01EFAC10 [u8 0x03]
00394607  je       0x39461d  ; -> 0039461D
00394609  xor      r8d, r8d
0039460C  lea      rdx, [rip - 0x773]  ; -> 00393EA0
00394613  mov      ecx, 0x108
00394618  jmp      0x244f50  ; -> 00244F50 fn
0039461D  ret      
```

## 003DB790 (11 B, extent 003DB790-003DB79B)

Page context: "' ('003DBCF0', '003DBD5F'). That has seven call sites in six functions (raw E8/E9 index plus 'jcc' sweep).  | route | channel source | values | |---|---|---| | 'ScriptVM_SubmitActorRuntimeRequest' → '003DB790' / '003DBAE0' | the 'REQ'-family descriptor ('002689B1') | '0'–'7', authored immediates (SWE2-DATA census above) | | '003DBDC0', '003DC0D0' | the originating entry's '+3', under descriptor word '0x402' | '+0x61' arm: **not an index"

```
003DB790  mov      r8d, 1
003DB796  jmp      0x3dbcf0  ; -> 003DBCF0 fn
```
