# F-interior pack: `11-Party/Battle-State-Block/the-battle-state-block-field-map.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-battle-state-block-field-map.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 0035C920 (29 B, extent 0035C920-0035C93D)

Page context: "r 'byte[owner+0xFC] & 0x10', else '00327850(byte[+0x60])' writes the preferred selector and '0035C760' tests it: '00237140'/'0035C940' run on the pass arm, '0035C750'/'003271D0' on the fail arm, and '0035C920' closes before '00244F00' runs on '[+0xD8]' and '0209C318' - the roster sweep that re-publishes the party's preferred definition per member.  Interior anchor '00280BF7' (function '00280B70'). "

```
0035C920  mov      eax, dword ptr [rip + 0x1f6bac2]  ; -> 022C83E8
0035C926  mov      edx, ecx
0035C928  shl      edx, 4
0035C92B  xor      edx, eax
0035C92D  and      edx, 0x10
0035C930  xor      eax, edx
0035C932  mov      dword ptr [rip + 0x1f6bab0], eax  ; -> 022C83E8
0035C938  jmp      0x2548f0  ; -> 002548F0 fn
```

## 0035C940 (26 B, extent 0035C940-0035C95A)

Page context: "rd list iterates - each record skips on 'word[+0x60] < 0', 'byte[0] & 2', or 'byte[owner+0xFC] & 0x10', else '00327850(byte[+0x60])' writes the preferred selector and '0035C760' tests it: '00237140'/'0035C940' run on the pass arm, '0035C750'/'003271D0' on the fail arm, and '0035C920' closes before '00244F00' runs on '[+0xD8]' and '0209C318' - the roster sweep that re-publishes the party's preferred definition per member.  Interior ancho"

```
0035C940  mov      edx, dword ptr [rip + 0x1f6baa2]  ; -> 022C83E8
0035C946  mov      eax, edx
0035C948  xor      eax, ecx
0035C94A  and      eax, 1
0035C94D  xor      edx, eax
0035C94F  mov      dword ptr [rip + 0x1f6ba93], edx  ; -> 022C83E8
0035C955  jmp      0x254940  ; -> 00254940 fn
```
