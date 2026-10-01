import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';p=W/'check.py';old=p.read_bytes();assert not (W/'result.json').exists()
(R/'check-before-comment-fix.py').write_bytes(old)
failure=dict(status='INVALID_SOURCE_MATCHER_PRECONDITION',stage='REDUCER_BEFORE_RESULT',cause='Actual retained btlctrl physical line5 assignment has trailing Japanese // comment. Checker copied a strict whole-line pattern without the established61 optional comment suffix; raw capture valid, no result produced.',old_check_sha256=hashlib.sha256(old).hexdigest(),raw_sha256=hashlib.sha256((W/'raw.json').read_bytes()).hexdigest(),repair='Assignment matcher accepts optional trailing // text, as original61. Preserve exact source bytes, variable identity requires metadata and encoded controls; no raw recapture.',feasibility_limits='Feasibility guessed map slot20 wanted curmenu; actual61/source is mp_debugmenu_flg. UNVALIDATED preparation retained; never promoted that guessed name.')
(W/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
src=old.decode();needle=r"(\d+)\s*;?\s*',text)";assert src.count(needle)==1;src=src.replace(needle,r"(\d+)\s*;?\s*(?://.*)?',text)");p.write_text(src)
