"""Freeze a bounded argument proof only after actual upstream exit qualification."""
import hashlib, importlib.util, json, pathlib, shutil, sys

W = pathlib.Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prerequisites(source):
    result_path = source / 'texture-update-arguments-result-01.json'
    r = json.loads(result_path.read_text())
    status = json.loads((source / 'texture-update-arguments-positive-02.status.json').read_text())
    checker = source / 'prove-texture-update-arguments.py'
    if status.get('exit') != 0 or status.get('checker_sha256') != sha(checker):
        raise ValueError('required positive invocation failed or incomplete')
    stdout = (source / 'texture-update-arguments-positive-02.stdout').read_bytes()
    stderr = (source / 'texture-update-arguments-positive-02.stderr').read_bytes()
    if not stdout.strip() or stderr.strip() or b'Original updater argument dependencies' not in stdout:
        raise ValueError('required positive invocation output failed or missing')
    if r.get('producer_complete') is not True or r.get('status') != 'PRODUCER_CHECKED_TEXTURE_UPDATE_ARGUMENTS_INDEPENDENT_PENDING':
        raise ValueError('required positive result failed or incomplete')
    if r.get('checker_sha256') != sha(checker) or r.get('helper_sha256') != sha(source/'prove-title-queue-consumption.py'):
        raise ValueError('required positive producer preimage changed')
    spec = importlib.util.spec_from_file_location('update_freeze_roles', source/'validate-title-source-annotations.py')
    S = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(S)
    if r.get('annotation_prerequisite', {}).get('validator_sha256') != sha(source/'validate-title-source-annotations.py'):
        raise ValueError('required actual annotation validator changed')
    if not r.get('source_pins'):
        raise ValueError('required original sources empty')
    for pin in r['source_pins']:
        if sha(source/pin['path']) != pin['sha256']:
            raise ValueError('required original source preimage changed')
        S.validate(json.loads((source/pin['path']).read_text()))
    return r


def main():
    if len(sys.argv) not in (2, 3):
        raise ValueError('fresh packet directory [input directory]')
    out = pathlib.Path(sys.argv[1])
    source = pathlib.Path(sys.argv[2]) if len(sys.argv) == 3 else W
    if out.exists():
        raise ValueError('immutable packet exists')
    r = prerequisites(source)  # A required upstream FAIL cannot be masked below.
    c = json.loads((source/'texture-update-arguments-controls-01/result.json').read_text())
    if c.get('status') != 'PASS_ACTUAL_TEXTURE_UPDATE_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals', [])) != 5:
        raise ValueError('required concrete control result incomplete')
    if any(q.get('exit') == 0 or q.get('result_absent') is not True or q.get('expected_error_seen') is not True for q in c['refusals']):
        raise ValueError('required concrete refusal failed')
    if c.get('checker_sha256') != sha(source/'prove-texture-update-arguments.py') or c.get('freezer_sha256') != sha(source/'freeze-texture-update-arguments.py'):
        raise ValueError('required control producer changed')
    if c.get('positive_reused', {}).get('sha256') != sha(source/'texture-update-arguments-result-01.json'):
        raise ValueError('required control positive moved')
    paths = ['texture-update-arguments-method-01.json', 'texture-async-count-path-source-01.json',
             'texture-update-arguments-result-01.json', 'prove-title-queue-consumption.py',
             'validate-title-source-annotations.py', 'prove-texture-update-arguments.py',
             'prove-texture-update-arguments-before-syntax-fix-01.py',
             'control-texture-update-arguments.py', 'freeze-texture-update-arguments.py']
    paths += ['texture-update-arguments-positive-'+version+suffix
              for version in ('01', '02') for suffix in ('.stdout', '.stderr', '.status.json')]
    paths += [p.relative_to(source).as_posix() for p in sorted((source/'texture-update-arguments-controls-01').rglob('*')) if p.is_file()]
    if any(not (source/p).is_file() for p in paths):
        raise ValueError('required packet member missing')
    out.mkdir()
    (out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
    for name in paths:
        target = out/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source/name, target)
    (out/'README.md').write_text('''# Deferred texture update: exact arguments and width-sensitive pitches

Method A STATIC_ONLY. Producer checked; independent review and canonical
consumption pending. Shipping EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. Reuses the committed texture-async-boundary retained source rather
than recapturing it or repeating its earlier admission/tree tests. The full
622010..6221DC normal body and621FF0 leaf are pinned and redecoded by the actual
reviewed access-role adapter. No original-code/native/emulated/game execution.

Question: which values reach context slot180, and does admission's200B copy
establish an immutable upload snapshot? The local source selects element+28 as
the initial data pointer, captures entry width/height and mip limit, then re-reads
resource/count/format fields inside the loop. Format is read again after the
native call to calculate the next data-pointer position. There is no explicit
direct read of owner+C0..187 as a descriptor in this body. That is NOT a universal
tail-unused claim: source/format/context may alias it or opaque callees may read
it. The copied tail's full meaning and real scheduler behavior remain open.

At the slot180 call, RCX is the context from[5FD050 return+110], RDX the selected
element's resource qword+0, R8D the mip index, R9D0; stack20 is the running source
pointer, stack28 a DWORD pitch and stack30 DWORD0. Slot identity/native effects
are separate; a local call is not proof of a GPU upload or visible presentation.
The callback itself does not validate index<count. The earlier admission's
validation occurs at a different boundary and cannot establish later lifetime.

Let B name the observed format DWORD+14; its name does not independently prove
format semantics. F is format byte+18 bit0. For a dimension d, rounding is
F ? (low32(d+3)&FFFFFFFC) : u32(d). Row pitch is
zeroextend32(low32(low32(B*roundedWidth)*(F?4:1)))>>3. Data advance is
zeroextend32(low32(low32(B*roundedWidth)*roundedHeight))>>3, added modulo64 to
the running pointer. Both products truncate in32 bits before the final shift,
including the apparent64-bit SHR RAX. Widening multiplication changes behavior.
Examples distinguish ordinary rounding, product overflow and ADD32 rounding
overflow. They are conditional arithmetic derivations, not shipping-asset or
original-instruction samples.

Last mip is min_unsigned(11, owner18 bit1 ?0:u32(owner10)); the stable normal
loop calls for0..last inclusive, hence1..12 calls. Width/height initially0 fall
back to owner fields; each later dimension becomes max_unsigned(1,old>>1).
After the loop, current maskedcount1 causes a re-read of selected+28 for584730,
then another selection and zero store. Under stable storage this releases/nulls
that field. With mutated state those are different read times; no original-pointer
release, cancellation, counter ownership or concurrency guarantee follows.

Reproduce the reduction using the existing analysis Python and a fresh output:

    python <packet>/prove-texture-update-arguments.py <fresh.json>

Five actual CLI refusal controls reuse the successful positive: consistent
payload-offset and arithmetic-shift mutations, missing source, false store-role
annotation, and a failed positive exit supplied to the actual freezer. The last
refuses before any output directory exists; downstream controls cannot turn an
upstream failure green. Original positive01 failed at Python parsing before any
result, was never PASS, and remains retained with its original driver. A one-line
syntax correction produced positive02. Positive output, exit, result, tool and
source prerequisites are all checked in the actual freeze path. Empty successful
stderr is legitimate; absent/empty positive stdout is refused.

OPUS owns element+28/ABI/arithmetic incorporation; FABLE owns deferred-read and
lifetime interpretation. Valid stable owner/count/storage/format/source/context
and normally returning ABI-preserving callees are the ordinary formula premises.
No complete caller/writer/alias closure, actual initialization, resource binding,
native effects, presentation, timing, natural overflow, reuse or fullOV closure.
The next useful question is an unowned original element+28 producer or scheduler
removal/counter dependency; do not repeat these settled parameter samples.

Player version: the texture updater reads several values when it runs; copying
parameters earlier does not by itself freeze all later behavior. A faithful
reconstruction must also retain the game's32-bit size arithmetic.

Cleanup: retained file reads and disposable synthetic control copies; finite
foreground tools terminate. No PC/game/input/instrument/save/config/reference
or unrelated-process mutation. Parked menu spent/unapproved; EXP127 invalid.
The full L1+L2 goal remains ACTIVE/NOT_MET. Manifest integrity, producer tests,
independent acceptance and canonical consumption are distinct.
''', encoding='utf-8')
    members = [dict(path=p.relative_to(out).as_posix(), bytes=p.stat().st_size, sha256=sha(p))
               for p in sorted(out.rglob('*')) if p.is_file()]
    (out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',
                                                    method='A STATIC_ONLY', members=members), indent=2)+'\n')
    print('Frozen', len(members), 'members; manifest', sha(out/'manifest.json'))


if __name__ == '__main__':
    main()
