# Consumer check: falsification pass 1 on CONTRACT-weather (OPUS, 2026-09-29)

corrects: 03-World-Area-Field/CONTRACT-weather.md (I-6's slot-2 fallback citation and register; §15's I-6 row; §10.4 sharpened)

## What was corrected

- **I-6's citation.** `0025AC24` is not an instruction boundary; it lies inside `0025AC20 mov rbx, [rsp+0x30]`. The
  slot-2 "stay" fallback of the prefer-3 arm is `setle cl` (`0025AC1A`) followed by `lea eax, [rcx+1]` (`0025AC1D`).
  The register is `ecx`, not `edx`. The mechanism and the invariant (every arm falls back to the current slot) hold.
- **§10.4, sharpened.** The environment-index guard is a signed `jge` against each table's own count dword, not a
  literal 16, and the default is `ebx`, zeroed once at `0026D931`.

## Current consumers

- consumer: [weather-probability-and-transition-roll.md](../../../03-World-Area-Field/Weather/weather-probability-and-transition-roll.md): revised-here. Its "`0025ABF0` and `0025AC24` yield 2" now cites `0025AC1D`.
- consumer: the other weather pages (the slot-state model, the apply and environment materialisation page, and the
  MWeather format) agree. None cites `0025AC24` or the environment-index guard's bound (searched: `0025AC24` occurs only
  on the two pages above).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_weather_contract.py`, checks W0-W17:
- W6 fails if `0025AC24` becomes an instruction start or `0025AC1D` stops being the fallback;
- W15 fails if the guard's form or the default register changes.

run: verified at 281e38648 (BROKEN 0), against the certified image `73461d08…` and `map_ref.bin` `7c63552f…`.
