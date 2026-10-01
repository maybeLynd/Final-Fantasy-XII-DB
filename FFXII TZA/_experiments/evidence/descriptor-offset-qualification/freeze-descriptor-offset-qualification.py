"""Freeze additive descriptor correction; legacy source/result remains immutable."""
import hashlib, json, pathlib, shutil, subprocess
W = pathlib.Path(__file__).resolve().parent; sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
out = W / 'descriptor-offset-qualification-frozen-ready'
if out.exists(): raise ValueError('immutable packet exists')
r = json.loads((W/'descriptor-offset-qualification-result-01.json').read_text())
c = json.loads((W/'descriptor-offset-qualification-controls-01/result.json').read_text())
for tag, driver in [('descriptor-offset-qualification-positive-01','normalize-namebinding-descriptor.py'),
                    ('descriptor-offset-qualification-controls-run-01','control-descriptor-offset-qualification.py')]:
    s = json.loads((W/(tag+'.status.json')).read_text())
    if s['exit'] != 0 or s.get('driver_sha256',s.get('checker_sha256')) != sha(W/driver): raise ValueError('required invocation failed/stale')
    if not (W/(tag+'.stdout')).read_bytes().strip() or (W/(tag+'.stderr')).read_bytes().strip(): raise ValueError('required invocation incomplete')
if r['producer_complete'] is not True or r['checker_sha256'] != sha(W/'normalize-namebinding-descriptor.py'): raise ValueError('positive missing/stale')
if c['status'] != 'PASS_ACTUAL_DESCRIPTOR_REFUSALS_INDEPENDENT_PENDING' or len(c['refusals']) != 2 or c['positive_reused']['sha256'] != sha(W/'descriptor-offset-qualification-result-01.json'): raise ValueError('controls incomplete')
if any(not (x['exit'] and x['expected_error_seen'] and x['result_absent'] and x['normalized_absent']) for x in c['refusals']): raise ValueError('control invalid')
pins = r['source_pins'] + r['required_invocation_receipts']
if any(sha(W/x['path']) != x['sha256'] for x in pins): raise ValueError('prerequisite changed')
if sha(W/r['normalized_result']['path']) != r['normalized_result']['sha256']: raise ValueError('normalized output changed')
paths = {x['path'] for x in pins} | {'descriptor-offset-retained-pin-result-01.json', 'descriptor-offset-qualification-method-01.json',
    'descriptor-offset-term-candidates-01.json', 'namebinding-error-policy-method-01.json', 'descriptor-offset-qualification-result-01.json',
    'namebinding-pin-exception-qualified-02.json', 'normalize-namebinding-descriptor.py', 'control-descriptor-offset-qualification.py',
    'freeze-descriptor-offset-qualification.py', 'prove-title-queue-consumption.py', 'validate-title-source-annotations.py', 'capture-index-path.py'}
paths |= {tag+ext for tag in ['descriptor-offset-qualification-positive-01','descriptor-offset-qualification-controls-run-01'] for ext in ['.status.json','.stdout','.stderr']}
paths |= {p.relative_to(W).as_posix() for p in (W/'descriptor-offset-qualification-controls-01').rglob('*') if p.is_file()}
projected = ['Database/FFXII TZA/_experiments/evidence/descriptor-offset-qualification/'+n for n in sorted(paths|{'manifest.json','README.md','.gitattributes'})] + ['Database/FFXII TZA/_index/_inbox/ASTRA.md']
units = len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units > 24000: raise ValueError('qualified native path budget exceeded')
out.mkdir(); (out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for n in sorted(paths):
    p = out/n; p.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(W/n,p)
(out/'README.md').write_text('''# Correct the name-binding descriptor offset label

Method A retained original shipping bytes. Producer valid; independent review
and FABLE/OPUS consumption pending. Full L1+L2 goal ACTIVE/NOT_MET.

Player version: the zero means start reading at the beginning of the file. It
does not enable or disable failed-load notification. That notification uses a
separate byte-count condition; an offset cannot settle whether a load succeeded.

Original2EAD50 zeroes DWORD descriptor+0. Retained full32E870 reads that DWORD,
uses CDQ/AND7FF/ADD/ANDFFFFF800, then stores slot+2C as initial file offset.
Requested byte count goes separately to slot+28. The original queue contract
already establishes32E370 callback-nonnull/count==-1 gating and callback ABI;
we consume that evidence, without rerunning its tests or receiving their credit.
The preparatory question's erroneous flag hypotheses remain in history.

One own frozen pin-exception packet has affected descriptor.flags=0, matching
flags0 sentence, README/proof/freezer prose and publication summary. Four other
direct packet roots have no matching terms in this targeted search, which is
not a repository-wide or universal field census. Actual record18/19 bit flags,
queue mode/chunk fields, raw instructions and branch findings are unchanged.
Canonical queue/index was already correct; no regression there is alleged.

normalize-namebinding-descriptor.py is the current additive producer path.
Its actual CLI invocation produces qualified02, renaming the exact field to
initial_file_offset and replacing only the one exact established sentence.
Legacy driver/input/result/manifest remain immutable. The publication path
requires this checked qualification, its original pins and actual invocation.

Reference EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
imagebase120000. Existing capture identity and reviewed access annotations are
retained; the normalizer rechecks exact original bytes and annotation roles.
Two actual CLI refusal controls reject missing semantic preimage and a coherent
same-size offset-store mutation. Both report and normalized output stay absent.
Reproduce in a writable repo copy with original image, normalizer and fresh
output. This is a checked correction, not independent semantic acceptance.

Natural error-count writers, IO outcome, caller initialization, recovery,
scheduling/reentrancy and lifetime remain open. Initial size is not necessarily
the later error-helper count. No live/native/emulated run or whole runtime-row
closure; no game/PC/instrument/save/config/reference/peer-process mutation.
''',encoding='utf8')
members = [dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='FROZEN_PRODUCER_VALID_INDEPENDENT_PENDING', members=members,member_count=len(members),native_path_units=units,method=r['method'],exe_sha256=r['exe_sha256'],native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0),indent=2)+'\n')
print(json.dumps(dict(folder=out.name,members=len(members),manifest_sha256=sha(out/'manifest.json'),native_path_units=units)))
