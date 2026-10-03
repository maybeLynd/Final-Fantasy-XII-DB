# Homing pack: `14-Story-Event-Quest-Hunt/persistent-flag-banks.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-persistent-flag-banks.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E11B0 (129 B, extent 002E11B0-002E1231)

Entered from (direct sites whose caller this page cites): `002E16B0` + 0x90 (call; `002E16B0` is cited on this page)
Other direct sites: none

Host context: "Actor-Names/the-npc-name-dictionary.md) section 2.3); and the two name-source readers on the shop page, '002B9C70' and '002BA530'. *Writer* of 'PersistentFlag_SetBank2048': the message-window opener '002E16B0(actor, ...)', whose first act for a non-null actor is 'SetBank2048(actor word +0x102, 1)' ('002E16DF'..'002E16EB'); the setter rejects any id above '0x7FF' unsigned ('0032ABF7'), which also discards the negative ids that mean a lit"

```
002E11B0  add      ecx, 5
002E11B3  cmp      ecx, 0x14
002E11B6  ja       0x2e122e  ; -> 002E122E
002E11B8  movsxd   rax, ecx
002E11BB  lea      rdx, [rip - 0x1c11c2]  ; -> 00120000 (image base)
002E11C2  mov      ecx, dword ptr [rdx + rax*4 + 0x1c1234]  ; image base + 0x1c1234 = 002E1234
002E11C9  add      rcx, rdx
002E11CC  jmp      rcx
002E11CE  mov      eax, 1
002E11D3  ret      
002E11D4  mov      eax, 2
002E11D9  ret      
002E11DA  mov      eax, 3
002E11DF  ret      
002E11E0  mov      eax, 4
002E11E5  ret      
002E11E6  mov      eax, 5
002E11EB  ret      
002E11EC  mov      eax, 6
002E11F1  ret      
002E11F2  mov      eax, 7
002E11F7  ret      
002E11F8  mov      eax, 8
002E11FD  ret      
002E11FE  mov      eax, 9
002E1203  ret      
002E1204  mov      eax, 0xa
002E1209  ret      
002E120A  mov      eax, 0xb
002E120F  ret      
002E1210  mov      eax, 0xc
002E1215  ret      
002E1216  mov      eax, 0xd
002E121B  ret      
002E121C  mov      eax, 0xe
002E1221  ret      
002E1222  mov      eax, 0xf
002E1227  ret      
002E1228  mov      eax, 0x10
002E122D  ret      
002E122E  xor      eax, eax
002E1230  ret      
```

## 002ED3A0 (76 B, extent 002ED3A0-002ED3EC)

Entered from (direct sites whose caller this page cites): `003EC6C0` + 0x24 (call; `003EC6C0` is cited on this page)
Other direct sites: `0034CCF0` + 0x3E (jmp); `0034D2B0` + 0x4B (jmp); `0034D640` + 0x48 (jmp)

Host context: "02EC3EA0'** (count '02EC3EC8', write index '02EC3EC4', rotated '% 3', '002FA878'–'002FA8F7'), > which is what the trigger walk looks up by field id. **'settrapshowstatus'** ('0x0547', > '00355E00' → '003EC6C0') shows or hides the sixteen marker slots '003EB720' indexes. > > **Who can spring one, and who is hit.** The trigger walk refuses a unit whose stats flags carry > bit 26 or whose **effect id 37 — *"Move safely past traps"*** ('lis"

```
002ED3A0  test     rcx, rcx
002ED3A3  je       0x2ed3eb  ; -> 002ED3EB
002ED3A5  cmp      dword ptr [rcx], -1
002ED3A8  je       0x2ed3eb  ; -> 002ED3EB
002ED3AA  movzx    eax, word ptr [rcx]
002ED3AD  cmp      ax, -1
002ED3B1  je       0x2ed3eb  ; -> 002ED3EB
002ED3B3  movsx    rax, ax
002ED3B7  imul     rcx, rax, 0x740
002ED3BE  add      rcx, qword ptr [rip + 0x1fd9b63]  ; -> 022C6F28
002ED3C5  je       0x2ed3eb  ; -> 002ED3EB
002ED3C7  cmp      dword ptr [rcx + 0x284], 0
002ED3CE  je       0x2ed3eb  ; -> 002ED3EB
002ED3D0  and      dword ptr [rcx + 0x304], 0xfffffffd
002ED3D7  neg      edx
002ED3D9  sbb      eax, eax
002ED3DB  and      eax, 2
002ED3DE  or       dword ptr [rcx + 0x304], eax
002ED3E4  or       dword ptr [rcx + 0x290], 0x10
002ED3EB  ret      
```

## 00363730 (26 B, extent 00363730-0036374A)

Entered from (direct sites whose caller this page cites): `00378230` + 0x9E (call; `00378230` is cited on this page)
Other direct sites: none

Host context: "CE (65 edges).** '00265270' is also called by bodies filed to WorldAreaField (world area): '001EDCD0' (AuthoredPresentationCondition); '002628B0' reaches bodies filed to WorldAreaField (world area): '00378230', '003DFA50', '003EAA00' - shared machinery across the layer boundary, no shared ownership.  ## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)  *Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* thes"

```
00363730  mov      byte ptr [rip + 0x1f68359], 0  ; -> 022CBA90
00363737  mov      qword ptr [rip + 0x1f683ae], 0  ; -> 022CBAF0
00363742  mov      byte ptr [rip + 0x1f68351], 0  ; -> 022CBA9A
00363749  ret      
```
