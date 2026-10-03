# Homing pack: `17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-fte-fct-texture-colour-tables.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0017F0B0 (15 B, extent 0017F0B0-0017F0BF)

Entered from (direct sites whose caller this page cites): `0053AB50` + 0x2CA (call; `0053AB50` is cited on this page); `0053AB50` + 0x2DC (call; `0053AB50` is cited on this page)
Other direct sites: none

Host context: "e whole record array in record order        (dataOff chain contiguous 2,127/2,127, ending exactly at entryLen) '''  Record layout (0x20 bytes, record-relative — 'rec = FTE + 0x40 + idx*0x20', reader '0053AB50' computes '((idx+2)<<5) + FTE'):  ''' +0x00  u32  VRAM bytes reserved        (multiple of 0x2000 in 2,127/2,127;                                           bottom-up allocator 00537AA0) +0x04  u16  w    pixel width +0x06  u16  h    " / "e whole record array in record order        (dataOff chain contiguous 2,127/2,127, ending exactly at entryLen) '''  Record layout (0x20 bytes, record-relative — 'rec = FTE + 0x40 + idx*0x20', reader '0053AB50' computes '((idx+2)<<5) + FTE'):  ''' +0x00  u32  VRAM bytes reserved        (multiple of 0x2000 in 2,127/2,127;                                           bottom-up allocator 00537AA0) +0x04  u16  w    pixel width +0x06  u16  h    "

```
0017F0B0  test     rcx, rcx
0017F0B3  je       0x17f0be  ; -> 0017F0BE
0017F0B5  mov      rax, qword ptr [rcx]
0017F0B8  xor      edx, edx
0017F0BA  jmp      qword ptr [rax + 8]
0017F0BE  ret      
```

## 0017F200 (16 B, extent 0017F200-0017F210)

Entered from (direct sites whose caller this page cites): `0053AB50` + 0x4A1 (call; `0053AB50` is cited on this page)
Other direct sites: none

Host context: "e whole record array in record order        (dataOff chain contiguous 2,127/2,127, ending exactly at entryLen) '''  Record layout (0x20 bytes, record-relative — 'rec = FTE + 0x40 + idx*0x20', reader '0053AB50' computes '((idx+2)<<5) + FTE'):  ''' +0x00  u32  VRAM bytes reserved        (multiple of 0x2000 in 2,127/2,127;                                           bottom-up allocator 00537AA0) +0x04  u16  w    pixel width +0x06  u16  h    "

```
0017F200  test     rcx, rcx
0017F203  je       0x17f20f  ; -> 0017F20F
0017F205  mov      r8, qword ptr [rcx]
0017F208  jmp      qword ptr [r8 + 0xc0]
0017F20F  ret      
```

## 0017F210 (16 B, extent 0017F210-0017F220)

Entered from (direct sites whose caller this page cites): `0053AB50` + 0x242D (call; `0053AB50` is cited on this page)
Other direct sites: none

Host context: "e whole record array in record order        (dataOff chain contiguous 2,127/2,127, ending exactly at entryLen) '''  Record layout (0x20 bytes, record-relative — 'rec = FTE + 0x40 + idx*0x20', reader '0053AB50' computes '((idx+2)<<5) + FTE'):  ''' +0x00  u32  VRAM bytes reserved        (multiple of 0x2000 in 2,127/2,127;                                           bottom-up allocator 00537AA0) +0x04  u16  w    pixel width +0x06  u16  h    "

```
0017F210  test     rcx, rcx
0017F213  je       0x17f21f  ; -> 0017F21F
0017F215  mov      r10, qword ptr [rcx]
0017F218  jmp      qword ptr [r10 + 0x80]
0017F21F  ret      
```

## 0017F220 (21 B, extent 0017F220-0017F235)

Entered from (direct sites whose caller this page cites): `0053AB50` + 0x41D (call; `0053AB50` is cited on this page)
Other direct sites: none

Host context: "e whole record array in record order        (dataOff chain contiguous 2,127/2,127, ending exactly at entryLen) '''  Record layout (0x20 bytes, record-relative — 'rec = FTE + 0x40 + idx*0x20', reader '0053AB50' computes '((idx+2)<<5) + FTE'):  ''' +0x00  u32  VRAM bytes reserved        (multiple of 0x2000 in 2,127/2,127;                                           bottom-up allocator 00537AA0) +0x04  u16  w    pixel width +0x06  u16  h    "

```
0017F220  test     rcx, rcx
0017F223  je       0x17f234  ; -> 0017F234
0017F225  mov      rax, qword ptr [rcx]
0017F228  test     edx, edx
0017F22A  setne    dl
0017F22D  jmp      qword ptr [rax + 0xa8]
0017F234  ret      
```

## 003E41F0 (71 B, extent 003E41F0-003E4237)

Entered from (direct sites whose caller this page cites): `0053AB50` + 0x427 (call; `0053AB50` is cited on this page)
Other direct sites: none

Host context: "e whole record array in record order        (dataOff chain contiguous 2,127/2,127, ending exactly at entryLen) '''  Record layout (0x20 bytes, record-relative — 'rec = FTE + 0x40 + idx*0x20', reader '0053AB50' computes '((idx+2)<<5) + FTE'):  ''' +0x00  u32  VRAM bytes reserved        (multiple of 0x2000 in 2,127/2,127;                                           bottom-up allocator 00537AA0) +0x04  u16  w    pixel width +0x06  u16  h    "

```
003E41F0  mov      r8, qword ptr [rip + 0x1ee2d31]  ; -> 022C6F28
003E41F7  xor      r9d, r9d
003E41FA  nop      word ptr [rax + rax]
003E4200  cmp      cx, -1
003E4204  je       0x3e4233  ; -> 003E4233
003E4206  movsx    rax, cx
003E420A  imul     rax, rax, 0x740
003E4211  add      rax, r8
003E4214  cmp      dword ptr [rax + 0x284], r9d
003E421B  cmove    rax, r9
003E421F  test     rax, rax
003E4222  je       0x3e4233  ; -> 003E4233
003E4224  movzx    edx, word ptr [rax + 6]
003E4228  cmp      dx, -1
003E422C  je       0x3e4233  ; -> 003E4233
003E422E  movzx    ecx, dx
003E4231  jmp      0x3e4200  ; -> 003E4200
003E4233  movzx    eax, cx
003E4236  ret      
```
