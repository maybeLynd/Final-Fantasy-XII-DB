# The sound id's `id >> 9` is the SE-block registry index (OPUS, 2026-09-26)

**Evidence class: STATIC** (the shipping image, every instruction decoded at its address), `live_game: false`.

A rejecting regression for the correction to
[`seb-se-block-index.md`](../../../18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md) §3.4, raised by FABLE
(`FABLE-CONTRA-OPUS-SEB-ID-BLOCK-FIELD-IS-THE-REGISTRY-INDEX`). The consumer check is
[`../seb-id-registry-index-consumer-check.md`](../seb-id-registry-index-consumer-check.md).

**4 / 4 pass; `result.json` is byte-identical over two runs (md5 `e66d6663e3203fd611d493ecde763a87`).**

| case | what the image shows |
|---|---|
| `C1` | `003A1180` rebuilds `(word +0xA << 16) \| word +8` of registry entry `k` (table `02AEEDC0`), compares it with the handle, then `shl edx, 9` / `add edx, ebx` on that same `word +8` |
| `C2` | `003A1650` passes the entry's `word +8` to `002DEF00`, which does `and ecx, 0x3f` and forwards the file's `word +8` (`n`) separately, through `001DBD20` → `00210B60` → `0021B430` → `00223AD0` |
| `C3` | `00223AD0` stores the index at bank `+0x3C` (`00223C83`) and `n` at `+0x38` (`00223C9C`); its entry check compares `n` with the file's `word +8` |
| `C4` | `0021B5B0` computes `id >> 9` and compares it with `+0x3C` (`0021B5FA`); `0021B430` finds a bank by `+0x3C` too (`0021B476`) |

Run: `python check.py` (needs `pefile` and `capstone`, and the shipping EXE at the path in the script).
