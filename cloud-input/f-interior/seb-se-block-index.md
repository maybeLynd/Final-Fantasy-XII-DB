# F-interior pack: `18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/seb-se-block-index.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 001DBD20 (58 B, extent 001DBD20-001DBD5A)

Page context: " **The loader side.** '003A1650' passes the same 'word +8' to '002DEF00', which masks it '& 0x3F' >   ('002DEF00 and ecx,0x3f') and hands it, with the file's own 'word +8' ('n', '002DEF0B'), through '001DBD20' → >   '00210B60' → '0021B430' to '00223AD0(bank, idx, n, …)'. That call stores the index at **bank '+0x3C'** >   ('00223C83') and 'n' at **bank '+0x38'** ('00223C9C'). Its entry check compares 'n' with the file's 'word +8' >   ('0"

```
001DBD20  mov      qword ptr [rsp + 8], rbx
001DBD25  mov      qword ptr [rsp + 0x10], rsi
001DBD2A  push     rdi
001DBD2B  sub      rsp, 0x20
001DBD2F  mov      rbx, r8
001DBD32  mov      edi, edx
001DBD34  mov      esi, ecx
001DBD36  call     0x210b30  ; -> 00210B30 fn
001DBD3B  mov      rcx, rax
001DBD3E  mov      r9, rbx
001DBD41  mov      r8d, edi
001DBD44  mov      edx, esi
001DBD46  mov      rbx, qword ptr [rsp + 0x30]
001DBD4B  mov      rsi, qword ptr [rsp + 0x38]
001DBD50  add      rsp, 0x20
001DBD54  pop      rdi
001DBD55  jmp      0x210b60  ; -> 00210B60 fn
```

## 002DEC10 (5 B, extent 002DEC10-002DEC15)

Page context: "e 'UQ-149' names as *“the runtime bank slot as well as the 'sead' bank data”*, and it is named there correctly.  ### 3.2 Registration — '003A1650'  '003A0C90(blockId)' looks the id ('+0x08', read by '002DEC10') up in a 64-entry registry of 24-byte records at '02AEEDC0': a hit increments the record's use count ('+0x0E') and the new file is released; a miss claims a record, stores the loaded handle ('+0x14') and marks it in the bitmap at "

```
002DEC10  movsx    eax, word ptr [rcx + 8]
002DEC14  ret      
```
