# F-interior pack: `00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/cross-subsystem-accessor-hubs.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

## 002EAA10 (30 B, extent 002EAA10-002EAA2E)

Page context: "/'01CEBB70'/'01CEBDA0'. Interior anchor '003C3FA8' (a '00203170' call).  ## SWE2-EC7-61 update (2026-09-19) - '0032A060'  '0032A060' (154 B) is a cross-subsystem accessor hub - '00236820'/'00236850'/'002EAA10'/'00313F60'. Interior anchor '0032A06E' (a '00236850' call).   ## SWE2-EC7-67 update - '002FAED0'  '002FAED0' (129 B) is an accessor-hub body - '003148F0'/'0032AA60'/'00379CD0'/'002FB430' x2 plus '02EC3E60'. Interior anchor '002FAE"

```
002EAA10  test     rcx, rcx
002EAA13  je       0x2eaa2b  ; -> 002EAA2B
002EAA15  mov      rax, qword ptr [rcx + 0xc0]
002EAA1C  test     rax, rax
002EAA1F  je       0x2eaa2b  ; -> 002EAA2B
002EAA21  mov      ecx, dword ptr [rax]
002EAA23  test     ecx, ecx
002EAA25  jns      0x3b50e0  ; -> 003B50E0 fn
002EAA2B  xor      eax, eax
002EAA2D  ret      
```

## 0034B5D0 (64 B, extent 0034B5D0-0034B610)

Page context: "00329220' calls '002F8F20'; the remaining edges run through shared helpers the page cites. - **Script_VM_Native_Bridge — CLIENT and SERVICE (243 edges).** 226 inbound (Script_VM_Native_Bridge bodies '0034B5D0', '0034BB80', '003516E0' call page-cited '00263F10', '00264010', 'Actor_GetWorldPosition' (00265020)); 17 outbound (page-cited 'WorldActorScriptVM_InterpretBytecode' (0025E4C0) call Script_VM_Native_Bridge bodies 'VMValueStack_PopI"

```
0034B5D0  push     rbx
0034B5D2  sub      rsp, 0x20
0034B5D6  mov      rbx, rcx
0034B5D9  mov      rcx, r9
0034B5DC  call     0x267e10  ; -> 00267E10 fn
0034B5E1  mov      ecx, eax
0034B5E3  call     0x264010  ; -> 00264010 fn
0034B5E8  mov      rcx, rax
0034B5EB  call     0x263f10  ; -> 00263F10 fn
0034B5F0  mov      rcx, rax
0034B5F3  call     0x3589b0  ; -> 003589B0 fn
0034B5F8  xor      edx, edx
0034B5FA  mov      ecx, eax
0034B5FC  call     0x320790  ; -> 00320790 fn
0034B601  mov      edx, eax
0034B603  mov      rcx, rbx
0034B606  add      rsp, 0x20
0034B60A  pop      rbx
0034B60B  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00466BF0 (75 B, extent 00466BF0-00466C3B)

Page context: "'00236850'/'0031C000'/'00322C50'. Interior anchor '0031C115' (a '00236820' call).  ## SWE2-EC7-53 update (2026-09-19) - '0037A5B0'  '0037A5B0' (561 B) is an accessor-hub body - '0020E600'/'003CC5F0'/'00466BF0' plus '008C5B34'/'01CEBC9C' rdata. Interior anchor '0037A5F6' (a '0020E600' call).  ## SWE2-EC7-56 update (2026-09-19) - '003C3F90'  '003C3F90' (219 B) is an accessor-hub body - '00203170'/'003977B0'/'003985B0'/'00398C50' plus '009"

```
00466BF0  mov      rax, qword ptr [rip + 0x2a54aed]  ; -> 02EBB6E4
00466BF7  xorps    xmm0, xmm0
00466BFA  test     eax, eax
00466BFC  js       0x466c3a  ; -> 00466C3A
00466BFE  cmp      eax, dword ptr [rip + 0x2a54adc]  ; -> 02EBB6E0
00466C04  jge      0x466c3a  ; -> 00466C3A
00466C06  cdqe     
00466C08  lea      rax, [rax + rax*4]
00466C0C  shl      rax, 4
00466C10  add      rax, qword ptr [rip + 0x2a54ad9]  ; -> 02EBB6F0
00466C17  cmp      qword ptr [rax + 8], 0
00466C1C  je       0x466c3a  ; -> 00466C3A
00466C1E  mov      rax, qword ptr [rax + 0x28]
00466C22  mov      rcx, qword ptr [rax + 0xa8]
00466C29  test     rcx, rcx
00466C2C  je       0x466c32  ; -> 00466C32
00466C2E  movss    xmm0, dword ptr [rcx]
00466C32  mulss    xmm0, dword ptr [rip + 0x48c4aa]  ; -> 008F30E4 [f32 0.01]
00466C3A  ret      
```
