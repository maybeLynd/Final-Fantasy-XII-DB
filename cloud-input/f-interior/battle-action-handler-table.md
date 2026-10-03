# F-interior pack: `07-Combat-Action/Action-Dispatch/battle-action-handler-table.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/battle-action-handler-table.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

## 00265060 (38 B, extent 00265060-00265086)

Page context: "08C5B2C'/'01CEBBA8'/'01CEBD80'/'01F44830'. Interior anchor '00335691' (a '0033CB70' call).    ## SWE2-EC7-66 update (2026-09-19) - '003448F0'  '003448F0' (130 B) is a battle-action body - '00264010'/'00265060'/'00267DB0'/'00267E10'/'0026B4C0'/'004686D0' plus '01F44830'. Interior anchor '00344912' (a '00267DB0' call).   ## SWE2-EC7-96 update (2026-09-20) - '00309A90' measured  '00309A90' (78 B) is the three-way float select '00301830', '"

```
00265060  test     rcx, rcx
00265063  je       0x26507e  ; -> 0026507E
00265065  movzx    edx, byte ptr [rcx + 3]
00265069  shr      edx, 5
0026506C  sub      edx, 1
0026506F  je       0x265076  ; -> 00265076
00265071  cmp      edx, 2
00265074  jne      0x26507e  ; -> 0026507E
00265076  mov      rax, qword ptr [rcx + 0xb8]
0026507D  ret      
0026507E  lea      rax, [rip + 0x1e34d3b]  ; -> 02099DC0
00265085  ret      
```

## 00344390 (124 B, extent 00344390-0034440C)

Page context: " to the resource layer.  **Script_VM_Native_Bridge — CLIENT (SWE2-EC7 2026-09-19, 3 edges).** '004686D0', a callee this table's '0033A120' section cites, is also called by three bridge-filed bodies ('00344390', '003448F0', '00345630'). The bridge callers are mechanical verb users of a shared helper.  **InputGameplay — MECHANICAL (SWE2-EC7-96, 1 edge).** '00253B90' — the gate this table's '00309A90' section cites — is reached through '00"

```
00344390  mov      qword ptr [rsp + 8], rbx
00344395  mov      qword ptr [rsp + 0x10], rbp
0034439A  mov      qword ptr [rsp + 0x18], rsi
0034439F  push     rdi
003443A0  sub      rsp, 0x20
003443A4  mov      rbp, rcx
003443A7  mov      rdi, r9
003443AA  mov      rcx, r9
003443AD  call     0x267e10  ; -> 00267E10 fn
003443B2  mov      rcx, rdi
003443B5  mov      ebx, eax
003443B7  call     0x267e10  ; -> 00267E10 fn
003443BC  mov      ecx, ebx
003443BE  mov      edi, eax
003443C0  call     0x264010  ; -> 00264010 fn
003443C5  mov      ecx, edi
003443C7  mov      rsi, rax
003443CA  call     0x264010  ; -> 00264010 fn
003443CF  mov      rcx, rax
003443D2  call     0x265060  ; -> 00265060 fn
003443D7  mov      rcx, rsi
003443DA  mov      rbx, rax
003443DD  call     0x265060  ; -> 00265060 fn
003443E2  mov      rcx, rax
003443E5  mov      rdx, rbx
003443E8  call     0x4686d0  ; -> 004686D0 fn
003443ED  movaps   xmm1, xmm0
003443F0  mov      rcx, rbp
003443F3  mov      rbx, qword ptr [rsp + 0x30]
003443F8  mov      rbp, qword ptr [rsp + 0x38]
003443FD  mov      rsi, qword ptr [rsp + 0x40]
00344402  add      rsp, 0x20
00344406  pop      rdi
00344407  jmp      0x26b4c0  ; -> 0026B4C0 fn
```

## 00426520 (59 B, extent 00426520-0042655B)

Page context: "6C90' and '00427320', while '00427320' calls 'CharacterRenderRecord_GetFCPPresentationConfigurationPayload' '003E55F0', '003E7D10', '00420890', '00423230' and '0042F310' and is called by '00426130', '00426520', '00426560', '00426C90' and '00521000'. Three different things cross here: a vector-subtract leaf every layer uses (mechanical), presentation-filed stance, frustum, suppression and relation bodies that share this page's action-sid"

```
00426520  cmp      cx, -1
00426524  je       0x42655a  ; -> 0042655A
00426526  movsx    rax, cx
0042652A  imul     rcx, rax, 0x740
00426531  xor      eax, eax
00426533  add      rcx, qword ptr [rip + 0x1ea09ee]  ; -> 022C6F28
0042653A  cmp      dword ptr [rcx + 0x284], eax
00426540  cmove    rcx, rax
00426544  test     rcx, rcx
00426547  je       0x42655a  ; -> 0042655A
00426549  or       byte ptr [rcx + 0x4b7], 0x40
00426550  mov      edx, 0x1001
00426555  jmp      0x427320  ; -> 00427320 fn
0042655A  ret      
```
