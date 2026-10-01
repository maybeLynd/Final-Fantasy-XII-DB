The original external_jumps field enumerated unconditional JMP only, not all
external jumps. Actual affected captures: raw.json, raw-nested.json (2E6303 JS),
raw-closure-r3.json (2EC47B/2EC4AD JE). Full instruction bytes were retained and
no class-preservation conclusion was accepted. No published canonical index changed.
Historical producers/checker/receipts are archived with exact hashes; raw/identity/
terminal records unchanged. Historical checks bind to archived producer bytes,
not silently to corrected code. Corrected default capture.py and actual downstream
capture scripts use Capstone's JUMP group, retaining conditionality and immediate/
indirect status. Next real source capture must exercise that corrected path.
Re-reduce historical edges additively using the same code; retain old records and
identify changed edge lists/consumers. Do not infer no native effects from zero calls
or an empty JMP-only list. JS to265510 is conditional tail delegation, not a CALL.
