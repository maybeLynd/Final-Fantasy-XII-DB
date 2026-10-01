# EXP-182 — `1CCB20` render-singleton ctor + `1D50D0` full alloc chain

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). `1E9F40`/`1FE8B0`/`861EC0` ran real;
`19C5D0` (CRT string-copy wrapper), `1D0390`, `202880`, `5CC930`, `210EC0`
are scripted boundaries (disclosed — `19C5D0` string slots asserted still
0xAA). `210EC0` uses a dynamic heap-alloc stub honoring rcx size.

Harness: `Temp\exp166_check.py` — **239/239, stable ×3**.

## `1D50D0` — lazy singleton, now full-real

`q[0x1F81428] == 0` → `210ec0(0x10E8)` → `1CCB20(obj)` → stores ptr,
returns it. `t1d50d0-null` executes the whole chain real: alloc stub →
ctor → `q[0x1F81428]` set → `d[sp+0xA78]==0x500` proven on the allocated
object. `17D490` = `d[singleton+0xAAC]` (EXP-180).

## `1CCB20(obj)` — field map of the 0x10E8-byte singleton

A render/lighting settings object. All field writes verified against a
0xAA-prefilled object (unwritten fields provable):

- `+0xAA8` qword zero → **`d[+0xAAC]` (the nav-generation dword `17D490`
  reads) starts 0** → `265920` takes the fallback arm until something
  else writes it.
- `+0xA78=0x500`, `+0xA7C=0x2D0` (1280×720-ish dims); `+0xAD8/+0xADC =
  0x2710` (10000); `+0xACC/+0xAD0 = 0xD1` (209); `w+0xABC/w+0xAC4 =
  0x101`; `d+0xAC0=1`.
- **Camera block**: `f[+0xC10]=0x3F490FD8` (π/4 = 45° fov),
  `f[+0xC14]=0x3FE38E39` (1.7778 = **16/9 aspect**), `+0xC18 =
  0x3F93CD3A` (≈1.1547); `d+0xC04=3`, `d+0xC08=8`, `d+0xC40=0x63000C`
  (written 0 first, then this — sealed value), `d+0xC68=+0xC6C=0x270F`
  (9999 caps).
- `f[+0xCF4]=45.0`, `f/q[+0xDB0]=30.0`, `d[+0xE18]=0x3E8` (1000 ms),
  `q[+0xDDC]=0x11`, `d[+0x10D4]=0x280`, `w[+0x10D8]=0x100`,
  `f[+0x10B8]=0x3F051EB8` (≈0.52).
- Threshold floats `f[+0xD94]=0.01`, `f[+0xD98]=0.001`,
  `f[+0xD9C]≈1e-4`.
- `5CC930()` (timer) − const `d[0x2CB60E8]` → `q[+0xD88]` (proven
  `-const` under stub-ret-0).
- `+0x130` block memset zero, len `0x938`; trailing 6×0xC dword
  zero-loop covers `+0xE68..+0x10A7`.
- `19C5D0(dst, 0x20, src)` ×3 → `+0xD0C`="None", `+0xD2C`="Irradiance",
  `+0xD4C`="Specular" (static string addresses `0x8F6CD8`,
  `0x8FD560`, `0x8FD570`) — cubemap/lightmap resource name slots.

## Sub-ctors (real)

- `1E9F40(obj+8)` — ~40-field leaf init; several `1.0f` quads
  (`+0x58`,`+0x6C`,`+0x80`,`+0x94` relative to obj+8).
- `1FE8B0(obj+0xA98)` — `d=6`, `q+8=0` (a small kind-6 record head).
- `861EC0` — real memset path (jmp `61EC0` handler).
- `202880(obj+0xA98)` — calls `2001F0`, rewrites `d=6`/`q+8=0`
  (scripted — deeper init).

## Harness additions

`allocx` dynamic SCR retkey (`rax = self.alloc(rcx)`), `ctorobj`/
`rcx_ctor` fixture keys, REAL tags `z1ccb20`/`z1d50d0`/`z1e9f40`/
`z1fe8b0`, SCR stubs for the four deep/CRT callees.
