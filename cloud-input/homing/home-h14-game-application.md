# Homing pack: `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-game-application.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001FB830 (15 B, extent 001FB830-001FB83F)

Entered from (direct sites whose caller this page cites): `001F16C0` + 0x6E (jmp; `001F16C0` is cited on this page)
Other direct sites: none

Host context: "'/'+0x48'/'+0x54'/'+0x5C'/'+0x68'/ '+0x70' - the default transform/colour record. Interior anchor '0062DD2E' (the first '1.0f' store).  ## SWE2-EC7-77 update (2026-09-20) - '00220760' + '001A5810' + '001F16C0' lifecycle helpers measured  '00220760' (119 B) is the '[rcx+0x18]'-head chain drain: each link runs '001AF2B0(rcx, [link])' then the '+0x18' vtable slot of the '[rcx+0x30]' object with 'r8d = 0x30'; the head is then reset - '[rcx+"

```
001FB830  mov      rdx, qword ptr [rcx]
001FB833  mov      rcx, qword ptr [rip + 0x1d83c96]  ; -> 01F7F4D0
001FB83A  jmp      0x1a1850  ; -> 001A1850 fn
```

## 005E3040 (150 B, extent 005E3040-005E30D6)

Entered from (direct sites whose caller this page cites): `0060C3F0` + 0x2D (call; `0060C3F0` is cited on this page)
Other direct sites: `005C9270` + 0x2F (call); `005C9F30` + 0x3F (call)

Host context: "word 'rcx+8' and 'edx' at dword '[rcx]' and returns 0 | Interior anchor '0060C35A'; Interior anchor '0060C371'; Interior anchor '0060C393'; Interior anchor '0060C3B4'; Interior anchor '0060C3DB' | | '0060C3F0' | 135 B | returns 0 when 'edx' equals dword '[rcx]'; otherwise calls the function at '0060C3F0'+0x2D ('edx', qword 'rcx+8', the smaller (unsigned) of 'edx' and dword '[rcx]' AND '0x7fffffff') and returns '0xd' when it returns null"

```
005E3040  mov      qword ptr [rsp + 0x10], rbx
005E3045  mov      qword ptr [rsp + 0x18], rbp
005E304A  push     rsi
005E304B  sub      rsp, 0x20
005E304F  mov      ebp, r8d
005E3052  mov      rbx, rdx
005E3055  mov      esi, ecx
005E3057  test     ecx, ecx
005E3059  je       0x5e30c4  ; -> 005E30C4
005E305B  mov      ecx, esi
005E305D  mov      edx, 8
005E3062  shl      rcx, 3
005E3066  call     0x17d260  ; -> 0017D260 fn
005E306B  mov      r9, rax
005E306E  test     rax, rax
005E3071  je       0x5e30b4  ; -> 005E30B4
005E3073  mov      qword ptr [rsp + 0x30], rdi
005E3078  mov      rcx, rax
005E307B  test     ebp, ebp
005E307D  je       0x5e309d  ; -> 005E309D
005E307F  mov      edi, ebp
005E3081  mov      rdx, rcx
005E3084  add      rcx, 8
005E3088  test     rdx, rdx
005E308B  je       0x5e3097  ; -> 005E3097
005E308D  mov      rax, qword ptr [rbx]
005E3090  add      rbx, 8
005E3094  mov      qword ptr [rdx], rax
005E3097  sub      rdi, 1
005E309B  jne      0x5e3081  ; -> 005E3081
005E309D  sub      esi, ebp
005E309F  je       0x5e30ac  ; -> 005E30AC
005E30A1  lea      rdi, [r9 + rbp*8]
005E30A5  mov      ecx, esi
005E30A7  xor      eax, eax
005E30A9  rep stosq qword ptr [rdi], rax
005E30AC  mov      rdi, qword ptr [rsp + 0x30]
005E30B1  mov      rax, r9
005E30B4  mov      rbx, qword ptr [rsp + 0x38]
005E30B9  mov      rbp, qword ptr [rsp + 0x40]
005E30BE  add      rsp, 0x20
005E30C2  pop      rsi
005E30C3  ret      
005E30C4  mov      rbx, qword ptr [rsp + 0x38]
005E30C9  xor      eax, eax
005E30CB  mov      rbp, qword ptr [rsp + 0x40]
005E30D0  add      rsp, 0x20
005E30D4  pop      rsi
005E30D5  ret      
```

## 00616210 (58 B, extent 00616210-0061624A)

Entered from (direct sites whose caller this page cites): `00163760` + 0x43 (call; `00163760` is cited on this page); `00163D60` + 0x2F (call; `00163D60` is cited on this page)
Other direct sites: `00163110` + 0x46 (call); `00163170` + 0x46 (call); `001631D0` + 0x46 (call); `00163230` + 0x46 (call); `00163290` + 0x38 (call); `001632E0` + 0x38 (call); `00163330` + 0x38 (call); `00163380` + 0x38 (call); `001633D0` + 0x44 (call); `00163430` + 0x44 (call); `00163490` + 0x44 (call); `001634F0` + 0x44 (call); `00163550` + 0x38 (call); `001635A0` + 0x38 (call); `001635F0` + 0x38 (call); `00163640` + 0x46 (call); `001636A0` + 0x46 (call); `00163700` + 0x46 (call); `001637C0` + 0x46 (call); `00163820` + 0x46 (call); `00163880` + 0x46 (call); `001638E0` + 0x46 (call); `00163940` + 0x46 (call); `001639A0` + 0x46 (call); `00163A00` + 0x46 (call); `00163A60` + 0x46 (call); `00163AC0` + 0x46 (call); `00163B20` + 0x46 (call); `00163B80` + 0x46 (call); `00163BE0` + 0x46 (call); `00163C40` + 0x46 (call); `00163CA0` + 0x46 (call); `00163D00` + 0x46 (call)

Host context: "d '02CB757C', then tail-jumps to '00808B90(008AB0B0)' | Interior anchor '001615CB'; Interior anchor '001615D7'; Interior anchor '001615EC'; Interior anchor '001615FF'; Interior anchor '00161609' | | '00163760' | 88 B | calls the function at site '00163760' + 0x43 with ('02CF72C0', '00D560D8', 0, 0x1F8) and stack arguments 0, 0x3D, 0x3D, 0x3D, 0x3D, then tail-jumps to '00808B90(008AEF70)' | Interior anchor '0016378A'; Interior anchor '00" / "tack arguments 0, 0x3D, 0x3D, 0x3D, 0x3D, then tail-jumps to '00808B90(008AEF70)' | Interior anchor '0016378A'; Interior anchor '0016379B'; Interior anchor '001637A3'; Interior anchor '001637B3' | | '00163D60' | 68 B | calls the function at site '00163D60' + 0x2F with ('02CF7A30', "UNKNOWN" ('00D26D00'), 0x33, 0) and five zero stack arguments, then tail-jumps to '00808B90(008AF070)' | Interior anchor '00163D66'; Interior anchor '00163D8"

```
00616210  push     rbx
00616212  sub      rsp, 0x20
00616216  mov      rbx, rcx
00616219  call     0x62cd40  ; -> 0062CD40 fn
0061621E  mov      eax, dword ptr [rsp + 0x50]
00616222  mov      dword ptr [rbx + 0x20], eax
00616225  mov      eax, dword ptr [rsp + 0x58]
00616229  mov      dword ptr [rbx + 0x24], eax
0061622C  mov      eax, dword ptr [rsp + 0x60]
00616230  mov      dword ptr [rbx + 0x28], eax
00616233  mov      eax, dword ptr [rsp + 0x68]
00616237  mov      dword ptr [rbx + 0x2c], eax
0061623A  mov      eax, dword ptr [rsp + 0x70]
0061623E  mov      dword ptr [rbx + 0x30], eax
00616241  mov      rax, rbx
00616244  add      rsp, 0x20
00616248  pop      rbx
00616249  ret      
```
