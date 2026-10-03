# F-interior pack: `17-Presentation-Rendering/Character-Render-Records/the-bone-trails.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-bone-trails.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

## 003712C0 (17 B, extent 003712C0-003712D1)

Page context: "ted and the microprogram is CALLED inside     the registrar, while only the GS replay is deferred, and the trail's own template carries the MSCALF that calls it     - section 5a); the sibling sampler 003712C0; the three     callers of the immediate release. Pending first review ---  # Bone trails  A model can ask, in **section 4 of its FCP block** ([the FCP block](../Model-And-Motion-Formats/fcp-character-parameter-block.md)), for up to"

```
003712C0  cmp      dword ptr [rcx + 0x9c], 2
003712C7  je       0x3712cc  ; -> 003712CC
003712C9  xor      eax, eax
003712CB  ret      
003712CC  jmp      0x3736d0  ; -> 003736D0 fn
```

## 0042BDD0 (8 B, extent 0042BDD0-0042BDD8)

Page context: "4 is up, calls '00425E70(record, byte +0x3D0)' | | fan-out | '00425E70' (202 B) | applies the state to the record, to its child '+8', and - through the hierarchy walker with the eight-byte forwarder '0042BDD0' - to the hierarchies under that child's '+8' and '+0xA'. This is how a command addressed to a character reaches the weapon in its hand | | build / switch off | '003E6770' (276 B) | **on**: if the record's first trail handle ('+0x4"

```
0042BDD0  mov      edx, dword ptr [rdx + 0x38]
0042BDD3  jmp      0x3e6770  ; -> 003E6770 fn
```

## 0042E440 (63 B, extent 0042E440-0042E47F)

Page context: "d '0x740'-stride record at '022C6F28' receives it via '00424010' when '00426220' passes, the '+8'-linked next record gets the same triple, and each '+8'/'+0xA' continuation walks '0042EF90' with the '0042E440' callback - the bone-trail default-position write.  Interior anchor '0042B387' (function '0042B270').  '0042A390' (482 B) is '0042B270''s sibling variant '00427DE0' runs on the alternate path: the same '00422D50'/'00409F50'/'@FMN'/"

```
0042E440  mov      qword ptr [rsp + 8], rbx
0042E445  push     rdi
0042E446  sub      rsp, 0x20
0042E44A  mov      rbx, rdx
0042E44D  mov      rdi, rcx
0042E450  mov      rdx, qword ptr [rdx + 8]
0042E454  call     0x426220  ; -> 00426220 fn
0042E459  test     eax, eax
0042E45B  jne      0x42e474  ; -> 0042E474
0042E45D  movss    xmm3, dword ptr [rbx + 0x34]
0042E462  mov      rcx, rdi
0042E465  movss    xmm2, dword ptr [rbx + 0x30]
0042E46A  movss    xmm1, dword ptr [rbx + 0x2c]
0042E46F  call     0x424010  ; -> 00424010 fn
0042E474  mov      rbx, qword ptr [rsp + 0x30]
0042E479  add      rsp, 0x20
0042E47D  pop      rdi
0042E47E  ret      
```
