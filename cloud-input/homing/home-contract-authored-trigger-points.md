# Homing pack: `03-World-Area-Field/CONTRACT-authored-trigger-points.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-authored-trigger-points.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0035E500 (73 B, extent 0035E500-0035E549)

Entered from (direct sites whose caller this page cites): `0050FAF0` + 0x7A (call; `0050FAF0` is cited on this page); `0050FAF0` + 0x9E (call; `0050FAF0` is cited on this page)
Other direct sites: `002A59C0` + 0xA6 (call); `002A59C0` + 0x142 (call); `002A59C0` + 0x15E (call); `002A59C0` + 0x19B (call); `002A59C0` + 0x1BD (call)

Host context: "-Quest-Hunt/persistent-flag-banks.md) §8d   (AF-6, FABLE 2026-09-12), re-verified by decoding '002FAFD0'–'002FB14A' whole: sole caller is   the durative verb 'btlAtelOpenTreasureMessage''s end thunk '0050FAF0'; record '+0x0B' is the   gil chance, '+0xC'–'+0x12' two item pairs swapped 50/50 → 95/5 when the leader carries effect   layer 25 (Diamond Armlet), '+0x14'/'+0x16' the gil amounts (bit 6 of '+8' = random '1..N'),   '+9' the persis" / "-Quest-Hunt/persistent-flag-banks.md) §8d   (AF-6, FABLE 2026-09-12), re-verified by decoding '002FAFD0'–'002FB14A' whole: sole caller is   the durative verb 'btlAtelOpenTreasureMessage''s end thunk '0050FAF0'; record '+0x0B' is the   gil chance, '+0xC'–'+0x12' two item pairs swapped 50/50 → 95/5 when the leader carries effect   layer 25 (Diamond Armlet), '+0x14'/'+0x16' the gil amounts (bit 6 of '+8' = random '1..N'),   '+9' the persis"

```
0035E500  test     rcx, rcx
0035E503  je       0x35e548  ; -> 0035E548
0035E505  movzx    r10d, word ptr [rcx + 4]
0035E50A  cmp      r10w, 3
0035E50F  jge      0x35e548  ; -> 0035E548
0035E511  test     edx, edx
0035E513  je       0x35e52c  ; -> 0035E52C
0035E515  cmp      edx, 1
0035E518  jne      0x35e544  ; -> 0035E544
0035E51A  movsx    rax, r10w
0035E51E  mov      dword ptr [rcx + rax*8 + 0xc], edx
0035E522  mov      dword ptr [rcx + rax*8 + 0x10], r8d
0035E527  inc      word ptr [rcx + 4]
0035E52B  ret      
0035E52C  movsx    rax, r10w
0035E530  mov      dword ptr [rcx + rax*8 + 0xc], 0
0035E538  mov      word ptr [rcx + rax*8 + 0x10], r8w
0035E53E  mov      word ptr [rcx + rax*8 + 0x12], r9w
0035E544  inc      word ptr [rcx + 4]
0035E548  ret      
```

## 0035E560 (28 B, extent 0035E560-0035E57C)

Entered from (direct sites whose caller this page cites): `0050FAF0` + 0x40 (call; `0050FAF0` is cited on this page)
Other direct sites: `002A59C0` + 0x2E (call)

Host context: "-Quest-Hunt/persistent-flag-banks.md) §8d   (AF-6, FABLE 2026-09-12), re-verified by decoding '002FAFD0'–'002FB14A' whole: sole caller is   the durative verb 'btlAtelOpenTreasureMessage''s end thunk '0050FAF0'; record '+0x0B' is the   gil chance, '+0xC'–'+0x12' two item pairs swapped 50/50 → 95/5 when the leader carries effect   layer 25 (Diamond Armlet), '+0x14'/'+0x16' the gil amounts (bit 6 of '+8' = random '1..N'),   '+9' the persis"

```
0035E560  test     rcx, rcx
0035E563  je       0x35e57b  ; -> 0035E57B
0035E565  xor      eax, eax
0035E567  and      dword ptr [rcx + 8], 0xfffffffc
0035E56B  mov      word ptr [rcx + 4], ax
0035E56F  mov      qword ptr [rcx + 0xc], rax
0035E573  mov      qword ptr [rcx + 0x14], rax
0035E577  mov      qword ptr [rcx + 0x1c], rax
0035E57B  ret      
```
