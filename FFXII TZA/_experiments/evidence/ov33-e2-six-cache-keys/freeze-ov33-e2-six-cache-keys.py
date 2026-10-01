"""Freeze six-key domain result and exact inputs, no peer campaign rerun."""
import hashlib,importlib.util,json,pathlib,shutil
W=pathlib.Path(__file__).resolve().parent;out=W/'ov33-e2-six-cache-keys-frozen-ready'
if out.exists():raise ValueError('immutable key-domain packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'ov33-e2-six-cache-keys-result-01.json').read_text());c=json.loads((W/'ov33-e2-six-key-controls-01/result.json').read_text())
if r.get('producer_complete') is not True or r['checker_sha256']!=sha(W/'prove-ov33-e2-six-cache-keys.py') or c['status']!='PASS_ACTUAL_SIX_KEY_REFUSALS_INDEPENDENT_PENDING' or c['checker_sha256']!=r['checker_sha256'] or len(c['refusals'])!=3 or any(q['exit']==0 or not q['result_absent'] or not q['expected_error_seen'] for q in c['refusals']):raise ValueError('required key-domain proof/control failed')
s=importlib.util.spec_from_file_location('key_freeze_annotation',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
paths=[]
for p in r['source_pins']:
 if sha(W/p['path'])!=p['sha256']:raise ValueError('required hash source moved')
 S.validate(json.loads((W/p['path']).read_text()));paths.append(p['path'])
for p in r['required_input_pins']:
 if sha(W/p['path'])!=p['sha256']:raise ValueError('required data/source input moved')
 paths.append(p['path'])
paths += ['capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','capture-filecache-hash-loop.py','retain-ov33-e2-key-inputs.py','prove-ov33-e2-six-cache-keys.py','control-ov33-e2-six-cache-keys.py','freeze-ov33-e2-six-cache-keys.py','ov33-e2-six-cache-keys-result-01.json','ov33-e2-six-cache-keys-method-01.json']
paths += [p.relative_to(W).as_posix() for p in sorted((W/'ov33-e2-six-key-controls-01').rglob('*')) if p.is_file()]
paths += [p.relative_to(W).as_posix() for pattern in ('filecache-hash-loop-capture-01.*','ov33-e2-key-inputs-invocation-01.*','ov33-e2-six-key-positive-01.*','ov33-e2-six-key-controls-invocation-01.*') for p in sorted(W.glob(pattern))]
for name in paths:
 if not (W/name).is_file():raise ValueError('missing required packet member '+name)
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for name in dict.fromkeys(paths):
 p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,p)
(out/'README.md').write_text("""# OV33 E2: no cache-key collision for the six archive-missing sized paths

Method A STATIC_ONLY. Producer checked; independent review and canonical
incorporation pending. No native/harness/emulated/game execution. This is the
six-path cache-key intersection, not a new FST/path census or wholeOV33 closure.

The retained FABLE census selectsUS kind1 ids129/130/131, UK131/132 andCN127,
with the same path under both edx modes. Their original source/output hashes are
preserved, not treated as ASTRA executions or automatic independent acceptance.
The complete retained shipping archive-name domain is89,414 uniqueASCII names.
None of these six missing-file keys collides with any archive-name key. The
actual reducer finds its positive known-system.cnf collision/control through the
same key/domain lookup; absence was not inferred from an empty input or live
silence. Selected rows, normalized names, exact keys and collision sets are in
ov33-e2-six-cache-keys-result-01.json.

Under unchanged ASCII/C-locale normalization and archive-name-only population,
these paths cannot acquire a key from that domain and cannot take the cache
membership gate. A live sample cannot change that finite-domain exclusion.
Cache producer/writer/indirect binding completeness remains a prerequisite;
the peer b14's three direct-call lists are not silently promoted to all-code
closure. RawkindFF rewritten/uninitialized paths, locale/interference/eviction,
actual flag/cache state and request/owner lifetime remain separately open.
No claim that allE2 or allOV33 is resolved, or that a missing path cannot arise.

The complete40B original674A00 loop is byte/role-qualified through the reviewed
shared adapter. It computes low32(33*h+sign8(byte)), starting1505, untilNUL,
then clears bit31. Normal CFG has no calls, one return. This binds the reused
Python recurrence to shipping instructions; it is not original-code execution.
The two exact pure norm/djb2 definitions are reused from SWE2-CONTRACT b14;
its campaign is not run. Its three-string Unicorn checks and317 assertions are
external corroboration, not our tests, game observations or independent
acceptance of the new six-path result. b14's subject was89 other mode0EFB paths.

Exact data provenance is the read-only installed VBF index/name prefix, not a
full archive/payload hash. Original10,080,610-byte prefix is retained losslessly
as a3,007,099-byte zlib blob with raw/compressed SHA256, original header/filecount,
file stat and strict range/offset/NUL/ASCII/unique-name checks. No payloads were
extracted. This proves index/name-domain membership, not file-read success.
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000, Capstone5.0.7/tool/control receipts are preserved.

Default reproduction with existing analysis Python, fresh output:

    python <packet>/prove-ov33-e2-six-cache-keys.py <fresh.json>

Three actual CLI refusals reuse one positive: a redecodable/annotation-consistent
multiply32 instead of33, zero input population and missing index-prefix data.
Each exits nonzero with the expected reason and no final result. The changed
instruction passes the actual shared decoder before original body gate refuses.
Producer controls, independent review and canonical consumption are separate.

FABLE owns E2 semantic incorporation and remaining cache provenance/raw-path
questions; OPUS owns the resource no-status contract. This removes one scoped
formerly-runtime collision discriminator under explicit premises, not six whole
runtime rows. New wholeOV closure count0; prior retired obsolete runtime request1
cumulative. FullL1+L2/M0-M5 goal ACTIVE/NOT_MET. K14 closed/accepted, menu budget
spent/unapproved, EXP127 invalid. Helpers are finite foreground processes; no
PC/game/input/instrument/save/config/reference/peer-process writes or kills.
""",encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VERIFIED_INDEPENDENT_PENDING',members=members),indent=2)+'\n');print('Frozen six-key proof',len(members),sha(out/'manifest.json'))
