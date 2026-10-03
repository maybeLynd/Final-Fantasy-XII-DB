# Homing pack: `04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-actor-storage-record-field-map.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00198730 (18 B, extent 00198730-00198742)

Entered from (direct sites whose caller this page cites): `00182D60` + 0x10 (jmp; `00182D60` is cited on this page)
Other direct sites: none

Host context: "d owner resolvers '0031B860'/'0031B810'. Shared "find owning battle unit" fan-in.  **Input — MECHANICAL (SWE2-CONTRACT 2026-09-15, 8 edges).** '00225CD0'/'00225EB0' call the input helpers '00182D40'/'00182D60'/'00182DA0' (6 edges); 'InputGameplay_ArbitrateDigitalInputAndModalState' shares '0025B4C0'; 'Input.ActorControlMaskPropagationRuntime' '00226BE0' shares '00358940'.  **Script_VM_Native_Bridge — CLIENT (SWE2-EC7-164, 102 edges, one"

```
00198730  movzx    eax, byte ptr [rcx + 0x3a]
00198734  test     al, 1
00198736  je       0x198741  ; -> 00198741
00198738  and      al, 0xfe
0019873A  mov      byte ptr [rcx + 0x3b], 1
0019873E  mov      byte ptr [rcx + 0x3a], al
00198741  ret      
```

## 002E4F40 (93 B, extent 002E4F40-002E4F9D)

Entered from (direct sites whose caller this page cites): `002693D0` + 0xD1 (call; `002693D0` is cited on this page); `002693D0` + 0x14A (call; `002693D0` is cited on this page)
Other direct sites: `00351340` + 0x35 (jmp); `003DD8D0` + 0x49 (call)

Host context: "' ('00268BEA' +1); +16 more | | '+0x016' | 2 | uint16 | 'handleTag11' | 0 / 6 |  | '0046B690' ('0046B806'); '0046B870' ('0046B9E6'); +4 more | | '+0x018' | 1 | uint32 | *not in the store* | 2 / 35 | '002693D0' ('00269500'); '00262F90' ('00262FDB' +1) | '0025B820' ('0025B8EC'); '00268B10' ('00268BBE' +1); +33 more | | '+0x019' | 1 |  | inside the store's '+0x18' row | 1 / 4 | '00262F90' ('00262FE6' +1) | '0025B820' ('0025B8FF'); '002693D" / "' ('00268BEA' +1); +16 more | | '+0x016' | 2 | uint16 | 'handleTag11' | 0 / 6 |  | '0046B690' ('0046B806'); '0046B870' ('0046B9E6'); +4 more | | '+0x018' | 1 | uint32 | *not in the store* | 2 / 35 | '002693D0' ('00269500'); '00262F90' ('00262FDB' +1) | '0025B820' ('0025B8EC'); '00268B10' ('00268BBE' +1); +33 more | | '+0x019' | 1 |  | inside the store's '+0x18' row | 1 / 4 | '00262F90' ('00262FE6' +1) | '0025B820' ('0025B8FF'); '002693D"

```
002E4F40  sub      rsp, 0x28
002E4F44  test     rcx, rcx
002E4F47  je       0x2e4f5c  ; -> 002E4F5C
002E4F49  mov      rax, qword ptr [rcx + 0xc0]
002E4F50  test     rax, rax
002E4F53  jne      0x2e4f63  ; -> 002E4F63
002E4F55  xor      eax, eax
002E4F57  add      rsp, 0x28
002E4F5B  ret      
002E4F5C  xor      eax, eax
002E4F5E  test     rax, rax
002E4F61  je       0x2e4f55  ; -> 002E4F55
002E4F63  cmp      dword ptr [rax], -1
002E4F66  je       0x2e4f55  ; -> 002E4F55
002E4F68  movzx    ecx, word ptr [rax]
002E4F6B  cmp      cx, -1
002E4F6F  je       0x2e4f93  ; -> 002E4F93
002E4F71  movsx    rax, cx
002E4F75  imul     rcx, rax, 0x740
002E4F7C  add      rcx, qword ptr [rip + 0x1fe1fa5]  ; -> 022C6F28
002E4F83  je       0x2e4f93  ; -> 002E4F93
002E4F85  cmp      dword ptr [rcx + 0x284], 0
002E4F8C  je       0x2e4f93  ; -> 002E4F93
002E4F8E  call     0x427300  ; -> 00427300 fn
002E4F93  mov      eax, 1
002E4F98  add      rsp, 0x28
002E4F9C  ret      
```

## 002E9560 (78 B, extent 002E9560-002E95AE)

Entered from (direct sites whose caller this page cites): `002693D0` + 0xC6 (call; `002693D0` is cited on this page); `002693D0` + 0x13F (call; `002693D0` is cited on this page)
Other direct sites: `00351340` + 0x1C (call); `003DD8D0` + 0x3E (call)

Host context: "' ('00268BEA' +1); +16 more | | '+0x016' | 2 | uint16 | 'handleTag11' | 0 / 6 |  | '0046B690' ('0046B806'); '0046B870' ('0046B9E6'); +4 more | | '+0x018' | 1 | uint32 | *not in the store* | 2 / 35 | '002693D0' ('00269500'); '00262F90' ('00262FDB' +1) | '0025B820' ('0025B8EC'); '00268B10' ('00268BBE' +1); +33 more | | '+0x019' | 1 |  | inside the store's '+0x18' row | 1 / 4 | '00262F90' ('00262FE6' +1) | '0025B820' ('0025B8FF'); '002693D" / "' ('00268BEA' +1); +16 more | | '+0x016' | 2 | uint16 | 'handleTag11' | 0 / 6 |  | '0046B690' ('0046B806'); '0046B870' ('0046B9E6'); +4 more | | '+0x018' | 1 | uint32 | *not in the store* | 2 / 35 | '002693D0' ('00269500'); '00262F90' ('00262FDB' +1) | '0025B820' ('0025B8EC'); '00268B10' ('00268BBE' +1); +33 more | | '+0x019' | 1 |  | inside the store's '+0x18' row | 1 / 4 | '00262F90' ('00262FE6' +1) | '0025B820' ('0025B8FF'); '002693D"

```
002E9560  test     rcx, rcx
002E9563  je       0x2e95aa  ; -> 002E95AA
002E9565  mov      rax, qword ptr [rcx + 0xc0]
002E956C  test     rax, rax
002E956F  je       0x2e95aa  ; -> 002E95AA
002E9571  cmp      dword ptr [rax], -1
002E9574  je       0x2e95aa  ; -> 002E95AA
002E9576  movzx    ecx, word ptr [rax]
002E9579  cmp      cx, -1
002E957D  jne      0x2e9588  ; -> 002E9588
002E957F  movss    xmm0, dword ptr [rip + 0x60f7f9]  ; -> 008F8D80 [f32 30]
002E9587  ret      
002E9588  movsx    rax, cx
002E958C  imul     rcx, rax, 0x740
002E9593  add      rcx, qword ptr [rip + 0x1fdd98e]  ; -> 022C6F28
002E959A  je       0x2e957f  ; -> 002E957F
002E959C  cmp      dword ptr [rcx + 0x284], 0
002E95A3  je       0x2e957f  ; -> 002E957F
002E95A5  jmp      0x423280  ; -> 00423280 fn
002E95AA  xorps    xmm0, xmm0
002E95AD  ret      
```

## 002E9C60 (63 B, extent 002E9C60-002E9C9F)

Entered from (direct sites whose caller this page cites): `002E6BD0` + 0xB6 (call; `002E6BD0` is cited on this page)
Other direct sites: none

Host context: " ('0025BCEA') | | '+0x0EA' | 2 |  | *not in the store* | 0 / 2 |  | '00268EA0' ('00268EF8'); '00263050' ('002631BB') | | '+0x0EC' | 4 | uint64 | *not in the store* | 2 / 0 | '002EB430' ('002EB443'); '002E6BD0' ('002E6C33') |  | | '+0x0F0' | 8 |  | inside the store's '+0xEC' row | 1 / 1 | '002EB430' ('002EB44D') | '002EC3F0' ('002EC486' +2) | | '+0x0F4' | 1 |  | *not in the store* | 0 / 3 |  | '00268D10' ('00268E5A'); '0025C830' ('0025D0"

```
002E9C60  test     rcx, rcx
002E9C63  je       0x2e9c9c  ; -> 002E9C9C
002E9C65  movsx    rax, word ptr [rcx + 0x1e]
002E9C6A  test     eax, eax
002E9C6C  js       0x2e9c9c  ; -> 002E9C9C
002E9C6E  lea      r8, [rax + rax*8]
002E9C72  shl      r8, 5
002E9C76  lea      rax, [rip + 0x1e78123]  ; -> 02161DA0
002E9C7D  add      r8, rax
002E9C80  mov      eax, dword ptr [rcx + 0x24]
002E9C83  cmp      dword ptr [r8 + 0x5c], eax
002E9C87  jne      0x2e9c9c  ; -> 002E9C9C
002E9C89  test     edx, edx
002E9C8B  js       0x2e9c9c  ; -> 002E9C9C
002E9C8D  mov      eax, dword ptr [r8 + 0x40]
002E9C91  bt       eax, edx
002E9C94  jae      0x2e9c9c  ; -> 002E9C9C
002E9C96  mov      eax, 1
002E9C9B  ret      
002E9C9C  xor      eax, eax
002E9C9E  ret      
```
