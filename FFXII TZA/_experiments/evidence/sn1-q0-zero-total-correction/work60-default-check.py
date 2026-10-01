"""Additive62 producer correction; immutable60 original checker retained."""
import runpy
from pathlib import Path
p=Path('Database/FFXII TZA/_experiments/evidence/sn1-q0-zero-total-correction/corrected60-check.py')
assert p.exists(), 'Correction publication missing; do not fall back to stale unchecked total'
runpy.run_path(str(p),run_name='__main__')
