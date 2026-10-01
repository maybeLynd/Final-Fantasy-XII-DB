"""Preserve invalid first reduction; fix declared normalized row checksum path."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;old=(W/'check.py').read_bytes();s=old.decode();needle="sha((R/'affected-field-row.txt').read_bytes())==raw['consumer']['affected_row_sha256']";assert s.count(needle)==1
R=W/'retained/invalid-row-hash-normalization';R.mkdir(exist_ok=False);(R/'check-before.py').write_bytes(old)
raw=json.loads((W/'raw.json').read_text());p=W/'retained/affected-field-row.txt';row=p.read_text();sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(row.encode())==raw['consumer']['affected_row_sha256'] and sha(p.read_bytes())!=raw['consumer']['affected_row_sha256'] and b'\r\n' in p.read_bytes()
(R/'failure.json').write_text(json.dumps(dict(status='INVALID_REDUCTION_ROW_HASH',phase='Before guest/path reduction and before result.json existed',check_sha256=sha(old),assertion=needle,cause='Producer checksum was UTF8 LF normalized row text; Windows write_text retained CRLF bytes. First checker compared physical bytes instead of declared normalized text.',recorded_normalized_sha256=raw['consumer']['affected_row_sha256'],physical_sha256=sha(p.read_bytes()),normalized_sha256=sha(row.encode()),correction='Default checker hashes read_text().encode() for this normalized row field. Raw capture/driver/guest observations untouched; file byte identities still separately protected by manifest.',limits='This was an invalid reduction, not a passed experiment. No result from first reduction; no original guest re-execution for a row encoding fix.'),indent=2)+'\n')
(W/'check.py').write_text(s.replace(needle,"sha((R/'affected-field-row.txt').read_text().encode())==raw['consumer']['affected_row_sha256']"))
print('Preserved invalid reduction; corrected actual default row-normalization path, raw unchanged')
