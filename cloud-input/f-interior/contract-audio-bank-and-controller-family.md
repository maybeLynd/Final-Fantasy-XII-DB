# F-interior pack: `18-Audio/Audio-Bank-And-Controller-Family/CONTRACT-audio-bank-and-controller-family.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-audio-bank-and-controller-family.json`.

Functions: 8. Each is cited on the page only at its entry and is still in the F frontier.

## 002182E0 (103 B, extent 002182E0-00218347)

Page context: "20' (52 B) | | 'StreamAudioBank' | '009081A0' | 11 | '00222550' | '0021CD80' (52 B) | | 'AudioController' | '00906CD0' | **7** | '002127D0' | **absent** | | 'MusicAudioController' | '00907970' | 8 | '002182E0' | '00218980' (9 B) | | 'SebAudioController' | '00907DE0' | 8 | '0021AC00' | '0021B150' (9 B) | | 'SepAudioController' | '00907BA8' | 8 | '00219610' | '00219B10' (9 B) | | 'ShoutAudioController' | '00907FF0' | 8 | '0021BF60' | '002"

```
002182E0  mov      qword ptr [rsp + 8], rbx
002182E5  mov      qword ptr [rsp + 0x10], rsi
002182EA  push     rdi
002182EB  sub      rsp, 0x20
002182EF  lea      rax, [rip + 0x6ef67a]  ; -> 00907970
002182F6  mov      rsi, rcx
002182F9  mov      qword ptr [rcx], rax
002182FC  mov      edi, edx
002182FE  add      rcx, 0x78
00218302  call     0x218070  ; -> 00218070 fn
00218307  lea      rcx, [rsi + 0x40]
0021830B  call     0x218070  ; -> 00218070 fn
00218310  lea      rcx, [rsi + 0x20]
00218314  call     0x218100  ; -> 00218100 fn
00218319  mov      rcx, rsi
0021831C  call     0x212760  ; -> 00212760 fn
00218321  test     dil, 1
00218325  je       0x218334  ; -> 00218334
00218327  mov      edx, 0xb8
0021832C  mov      rcx, rsi
0021832F  call     0x809950  ; -> 00809950 fn
00218334  mov      rbx, qword ptr [rsp + 0x30]
00218339  mov      rax, rsi
0021833C  mov      rsi, qword ptr [rsp + 0x38]
00218341  add      rsp, 0x20
00218345  pop      rdi
00218346  ret      
```

## 0021BF60 (103 B, extent 0021BF60-0021BFC7)

Page context: "9 B) | | 'SebAudioController' | '00907DE0' | 8 | '0021AC00' | '0021B150' (9 B) | | 'SepAudioController' | '00907BA8' | 8 | '00219610' | '00219B10' (9 B) | | 'ShoutAudioController' | '00907FF0' | 8 | '0021BF60' | '0021C440' (9 B) | | 'StreamAudioController' | '00908200' | **7** | '0021CDC0' | **absent** |  ## 3. Types  ''' bank    +0x08  an intrusive entry list; each node's payload is at node +0x10         +0x38  the id the slot-10 and s"

```
0021BF60  mov      qword ptr [rsp + 8], rbx
0021BF65  mov      qword ptr [rsp + 0x10], rsi
0021BF6A  push     rdi
0021BF6B  sub      rsp, 0x20
0021BF6F  lea      rax, [rip + 0x6ec07a]  ; -> 00907FF0
0021BF76  mov      rsi, rcx
0021BF79  mov      qword ptr [rcx], rax
0021BF7C  mov      edi, edx
0021BF7E  add      rcx, 0x78
0021BF82  call     0x21bdf0  ; -> 0021BDF0 fn
0021BF87  lea      rcx, [rsi + 0x40]
0021BF8B  call     0x21bdf0  ; -> 0021BDF0 fn
0021BF90  lea      rcx, [rsi + 0x20]
0021BF94  call     0x21be80  ; -> 0021BE80 fn
0021BF99  mov      rcx, rsi
0021BF9C  call     0x212760  ; -> 00212760 fn
0021BFA1  test     dil, 1
0021BFA5  je       0x21bfb4  ; -> 0021BFB4
0021BFA7  mov      edx, 0xb8
0021BFAC  mov      rcx, rsi
0021BFAF  call     0x809950  ; -> 00809950 fn
0021BFB4  mov      rbx, qword ptr [rsp + 0x30]
0021BFB9  mov      rax, rsi
0021BFBC  mov      rsi, qword ptr [rsp + 0x38]
0021BFC1  add      rsp, 0x20
0021BFC5  pop      rdi
0021BFC6  ret      
```

## 0021CDC0 (103 B, extent 0021CDC0-0021CE27)

Page context: "| 'SepAudioController' | '00907BA8' | 8 | '00219610' | '00219B10' (9 B) | | 'ShoutAudioController' | '00907FF0' | 8 | '0021BF60' | '0021C440' (9 B) | | 'StreamAudioController' | '00908200' | **7** | '0021CDC0' | **absent** |  ## 3. Types  ''' bank    +0x08  an intrusive entry list; each node's payload is at node +0x10         +0x38  the id the slot-10 and slot-9 gates test controller         +0x08  the same entry list shape         +0x2"

```
0021CDC0  mov      qword ptr [rsp + 8], rbx
0021CDC5  mov      qword ptr [rsp + 0x10], rsi
0021CDCA  push     rdi
0021CDCB  sub      rsp, 0x20
0021CDCF  lea      rax, [rip + 0x6eb42a]  ; -> 00908200
0021CDD6  mov      rsi, rcx
0021CDD9  mov      qword ptr [rcx], rax
0021CDDC  mov      edi, edx
0021CDDE  add      rcx, 0x78
0021CDE2  call     0x21cc50  ; -> 0021CC50 fn
0021CDE7  lea      rcx, [rsi + 0x40]
0021CDEB  call     0x21cc50  ; -> 0021CC50 fn
0021CDF0  lea      rcx, [rsi + 0x20]
0021CDF4  call     0x21cce0  ; -> 0021CCE0 fn
0021CDF9  mov      rcx, rsi
0021CDFC  call     0x212760  ; -> 00212760 fn
0021CE01  test     dil, 1
0021CE05  je       0x21ce14  ; -> 0021CE14
0021CE07  mov      edx, 0xb8
0021CE0C  mov      rcx, rsi
0021CE0F  call     0x809950  ; -> 00809950 fn
0021CE14  mov      rbx, qword ptr [rsp + 0x30]
0021CE19  mov      rax, rsi
0021CE1C  mov      rsi, qword ptr [rsp + 0x38]
0021CE21  add      rsp, 0x20
0021CE25  pop      rdi
0021CE26  ret      
```

## 00222C70 (62 B, extent 00222C70-00222CAE)

Page context: " the classes.* Each bank's slot 10 reads the manager's '+0x3C' and acts on its own subset of the bits:  | class (vtable) | slot 10 | bits it acts on | |---|---|---| | 'MusicAudioBank' ('00907910') | '00222C70' | '& 1' → slot 0 ('jmp [rax]') | | 'SepAudioBank' ('00907B48') | '00223540' | '& 2' → slot 9, as a tail jump; only when bit 2 is clear, '& 8' / '& 0x10' / '& 0x20' → its slots 3 / 4 / 5 | | 'SebAudioBank' ('00907D80') | '00224B30'"

```
00222C70  push     rbx
00222C72  sub      rsp, 0x20
00222C76  mov      rbx, rcx
00222C79  call     0x210b30  ; -> 00210B30 fn
00222C7E  mov      rcx, rax
00222C81  call     0x210930  ; -> 00210930 fn
00222C86  test     eax, eax
00222C88  je       0x222ca8  ; -> 00222CA8
00222C8A  call     0x210b30  ; -> 00210B30 fn
00222C8F  test     byte ptr [rax + 0x3c], 1
00222C93  je       0x222ca8  ; -> 00222CA8
00222C95  mov      rax, qword ptr [rbx]
00222C98  mov      edx, 1
00222C9D  mov      rcx, rbx
00222CA0  add      rsp, 0x20
00222CA4  pop      rbx
00222CA5  jmp      qword ptr [rax]
00222CA8  add      rsp, 0x20
00222CAC  pop      rbx
00222CAD  ret      
```

## 002230D0 (35 B, extent 002230D0-002230F3)

Page context: "exactly on 2026-09-26)* *Corrected 2026-09-26 (FABLE, Claude Opus 5.5), from the bytes and the executed case 'AC7_sep_slot3_skips_the_band_150000_to_150999_only'.* - Sep's slots 3 and 4 ('00223100', '002230D0') compute '[+0x38] − 0x249F0' and return on an unsigned '< 0x3E8'. So   they skip only the band 150000–150999: ids below 150000 wrap high and pass, as do ids from 151000 up (149999   passes, 150000 and 150999 do not, 151000 passes)"

```
002230D0  mov      eax, dword ptr [rcx + 0x38]
002230D3  sub      eax, 0x249f0
002230D8  cmp      eax, 0x3e8
002230DD  jb       0x2230f2  ; -> 002230F2
002230DF  cmp      qword ptr [rcx + 0x50], 0
002230E4  je       0x2230f2  ; -> 002230F2
002230E6  test     byte ptr [rcx + 0x49], 0x69
002230EA  jne      0x2230f2  ; -> 002230F2
002230EC  mov      rax, qword ptr [rcx]
002230EF  jmp      qword ptr [rax]
002230F2  ret      
```

## 00223100 (41 B, extent 00223100-00223129)

Page context: "s re-quoted exactly on 2026-09-26)* *Corrected 2026-09-26 (FABLE, Claude Opus 5.5), from the bytes and the executed case 'AC7_sep_slot3_skips_the_band_150000_to_150999_only'.* - Sep's slots 3 and 4 ('00223100', '002230D0') compute '[+0x38] − 0x249F0' and return on an unsigned '< 0x3E8'. So   they skip only the band 150000–150999: ids below 150000 wrap high and pass, as do ids from 151000 up (149999   passes, 150000 and 150999 do not, 15"

```
00223100  mov      eax, dword ptr [rcx + 0x38]
00223103  sub      eax, 0x249f0
00223108  cmp      eax, 0x3e8
0022310D  jb       0x223128  ; -> 00223128
0022310F  cmp      qword ptr [rcx + 0x50], 0
00223114  je       0x223128  ; -> 00223128
00223116  movzx    eax, byte ptr [rcx + 0x49]
0022311A  test     al, 0x68
0022311C  jne      0x223128  ; -> 00223128
0022311E  test     al, 1
00223120  je       0x223128  ; -> 00223128
00223122  mov      rax, qword ptr [rcx]
00223125  jmp      qword ptr [rax]
00223128  ret      
```

## 00223130 (35 B, extent 00223130-00223153)

Page context: "igned '< 0x3E8'. So   they skip only the band 150000–150999: ids below 150000 wrap high and pass, as do ids from 151000 up (149999   passes, 150000 and 150999 do not, 151000 passes). - Sep's slot 5 ('00223130') tests the same window with 'jae', so it acts **only** inside the band. - Seb's iterator copies skip an entry whose '[+0x24] / 1000 == 150' (reciprocal '0x10624DD3', 'sar 6', 'cmp 0x96'):   the same band.  *The band is a property "

```
00223130  mov      eax, dword ptr [rcx + 0x38]
00223133  sub      eax, 0x249f0
00223138  cmp      eax, 0x3e8
0022313D  jae      0x223152  ; -> 00223152
0022313F  cmp      qword ptr [rcx + 0x50], 0
00223144  je       0x223152  ; -> 00223152
00223146  test     byte ptr [rcx + 0x49], 1
0022314A  jne      0x223152  ; -> 00223152
0022314C  mov      rax, qword ptr [rcx]
0022314F  jmp      qword ptr [rax]
00223152  ret      
```

## 00225440 (73 B, extent 00225440-00225489)

Page context: " → **direct calls** to '00224290' / '002240B0' / '00224470', not its vtable slots 3 / 4 / 5 ('00224180' / '00223FA0' / '00224360') | | 'ShoutAudioBank' ('00907F90'), 'StreamAudioBank' ('009081A0') | '00225440' | '& 4' → slot 9 only | | 'AudioBank' ('009078B0') | '_purecall' | — |  *A port that implements one uniform mask gets four of the five concrete banks wrong.*  **AC-7 — One 1000-id band, 150000–150999, is treated apart, and both cl"

```
00225440  mov      qword ptr [rsp + 8], rbx
00225445  push     rdi
00225446  sub      rsp, 0x20
0022544A  mov      rdi, rdx
0022544D  mov      rbx, rcx
00225450  call     0x210b30  ; -> 00210B30 fn
00225455  mov      rcx, rax
00225458  call     0x210930  ; -> 00210930 fn
0022545D  test     eax, eax
0022545F  je       0x22547e  ; -> 0022547E
00225461  call     0x210b30  ; -> 00210B30 fn
00225466  test     byte ptr [rax + 0x3c], 4
0022546A  je       0x22547e  ; -> 0022547E
0022546C  mov      rax, qword ptr [rbx]
0022546F  mov      r8d, 1
00225475  mov      rdx, rdi
00225478  mov      rcx, rbx
0022547B  call     qword ptr [rax + 0x48]
0022547E  mov      rbx, qword ptr [rsp + 0x30]
00225483  add      rsp, 0x20
00225487  pop      rdi
00225488  ret      
```
