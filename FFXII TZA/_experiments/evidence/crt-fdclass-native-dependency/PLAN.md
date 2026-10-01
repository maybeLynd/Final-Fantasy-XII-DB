# Native classifier dependency

Question: does the identified host CRT's `_fdclass` implement the five classes
supplied by the retained navigation fixture, and does its body depend on MXCSR?
Alternative: class returns differ, or FP arithmetic changes a signaling NaN or
subnormal before classification. Consumers: OPUS navigation preconditions and
CRT service boundary; FABLE navigation semantics.

Method A is sufficient: the installed export is a complete 65-byte leaf with
integer masks/branches and MOVD from XMM0. Preserve its exact export/body identity
and the shipping FF12 import witness. No native execution is necessary to derive
these branches. It is host CRT evidence, not shipping FF12 instructions and not
proof of live API-set resolution. Do not rerun EXP-131 or the grid edge cases.

Controls: full decode/closed branch targets/five return sites; exponent and
mantissa partition, signed zero, signed subnormal, normal, infinity, quiet and
signaling NaN examples. Examples are source calculations, not observations.
Reject a wrong mantissa mask, wrong NaN return, or branch reaching outside the
body. Stop on export forwarding, byte/identity mismatch or incomplete coverage.

Retain the failed hypothesis: the old phrase 'NaN -> FF' described GGRID's
return, not the bridge result. Primary EXP-131 gen_bodies.py and check.py specify
classifier NaN=2. There is no bridge defect to route on that basis.

Artifact-only cleanup: PC control OFF; no DLL loaded/executed, no FF12 process,
save/config/reference writes. General live permission remains active, but the
spent S19 setup allowance and unapproved additional recovery remain unchanged.
Independent review and canonical incorporation remain separate from publication.
