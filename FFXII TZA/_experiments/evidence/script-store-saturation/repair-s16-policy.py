import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';p=W/'check.py';old=p.read_bytes();assert not (W/'result.json').exists();(R/'check-before-s16-policy.py').write_bytes(old)
(W/'failure.json').write_text(json.dumps(dict(status='INVALID_STANDARD_S16_CLAMP_ASSUMPTION',stage='REDUCER_BEFORE_RESULT',cause='Original width3 MOV EAX,FFFF8001 and MOV R9D,8000 define signed-input clamp[-32767,+32768], not conventional[-32768,+32767]. Original guest lower/upper writes contradict initial checker prediction. Raw22 bounded executions retained, no accepted result.',old_check_sha256=hashlib.sha256(old).hexdigest(),repair='Correct exact original word-store policy, preserve bit pattern versus signed interpretation, validate true boundaries with additive original cases. Cause/intent of unusual bound constants UNKNOWN.'),indent=2)+'\n')
s=old.decode().replace('(-32768,32767)','(-32767,32768)').replace('width1s8 and3s16 by signed MIN/MAX clamp.', 'width1s8 by signed MIN/MAX clamp; width3 clamps signed input to[-32767,+32768] then stores low16 bits (unusual asymmetric bounds, intent unknown).')
assert s!=old.decode();p.write_text(s)
