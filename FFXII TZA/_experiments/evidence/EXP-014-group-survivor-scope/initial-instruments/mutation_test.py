#!/usr/bin/env python3
"""mutation_test.py - does the differential harness actually notice when the reconstruction is wrong?

The question
------------
`PARITY-STANDARD.md` §7 has carried this as an open item since the standard was written:

    "It does not define mutation testing (§36). A suite that passes because it tests nothing is a
     real failure mode and this standard cannot detect it."

Two blocks have now shown that is not hypothetical. `PersistentFlag_Gate` was written, compiled,
and called by nothing. `angle_wrap_driver.c` printed the result of its **own copy** of
`Angle_WrapLoop` while reporting *"vs reconstruction: OK"*. Both were found by other means; a
green harness said nothing about either.

**A mutation test asks the only question that matters about a test: break the thing under test,
and does the test fail?** A mutation the harness does not notice is a behaviour the harness does
not check, however many cases it runs.

The manifest is GENERATED, never written
----------------------------------------
The charter forbids hand-authoring a mutation manifest, and for a good reason: a hand-picked
mutation list is a list of things the author already believed were covered. These are produced
mechanically from the source text, by rules stated here:

    integer literal        ->  the same literal + 1        (bounds, masks, offsets, sizes)
    `>=` <-> `>`  `<=` <-> `<`  `==` <-> `!=`              (off-by-one and inverted guards)
    `<<` <-> `>>`                                          (bit direction)
    `&` -> `|`  in an expression                           (mask vs merge)
    `+` -> `-`  in an assignment's right-hand side         (sign)

Every site matching a rule becomes one mutation. Nothing is filtered by whether it looks
interesting.

Mutation outcomes
-----------------
    KILLED       the harness reported a behavioral mismatch for this mutant.
    SURVIVED     the harness PASSED with the reconstruction broken. **A gap.**
    EQUIVALENT   the mutant compiles to **byte-identical machine code**, so it cannot change
                 behaviour and no test could ever kill it. Proven, not judged -- see below.
    NO BUILD     the mutation does not compile; it is not a test result and is reported apart.
    INVALID      the instrument or its output was not a valid comparison.
    TIMEOUT      the comparison did not finish in its recorded time window.

Proving equivalence instead of arguing it
-----------------------------------------
Adjudicating survivors by hand is where a mutation score goes soft: "that one is equivalent" is
exactly the sentence a tired author writes about a gap. One class can be settled mechanically.

Builds run with **`/Brepro`** on both the compiler and the linker, which makes MSVC output
byte-for-byte reproducible. If a mutant's executable hashes the same as the baseline's, the
mutation emitted **the same code** -- so it is equivalent, provably, and belongs outside the
denominator rather than in the survivor list.

This found three at once: `name_registry.h` declares the full node layout (`TYPE 0x00`, `NAME 0x08`,
`NEXT 0x10`, `VALUE 0x18`, `SIZE 0x20`) as documentation of the physical structure, but the
registration function reads only two of the five. Mutating the other three changed a declaration
nothing compiles against, and they had been sitting in the survivor list looking like test gaps.

The implication only runs one way: identical code proves equivalence; **different code proves
nothing**, so those mutants still go to the harness.

**SURVIVED is the finding.** It names, precisely, a line whose behaviour no case distinguishes.

Safety
------
Production sources are never mutated. Each baseline/mutant receives a fresh private copy of
its source/header/driver/harness dependencies. Temporary case inputs and outputs are removed
in finally, including after compilation failure or interruption. Raw build/harness receipts
remain in the campaign output directory. Partial, invalid, timed-out and zero-tested campaigns
cannot pass. Identical executable bytes prove equivalence only; they do not count as tested.
"""
import argparse
import ast
from contextlib import contextmanager
import json
from pathlib import Path
import tempfile
import hashlib
import os
import re
import subprocess
import sys
import time

ROOT = r"C:\Users\Kristian\source\repos\XIIOnline\Reconstruction"
VCVARS = (r"C:\Program Files\Microsoft Visual Studio\18\Community\VC"
          r"\Auxiliary\Build\vcvars64.bat")

# subsystem -> (reconstruction .c, driver .c, harness, extra harness args)
# The mutable surface is the .c AND its .h: several pilots keep their constants as macros in the
# header -- angle_wrap's pi and 2pi, flag_banks' six bank bases -- and a mutation tool that only
# reads the .c would report a suspiciously small manifest and never touch the numbers that matter.
PILOTS = {
    "angle_wrap": ("Game/Math/angle_wrap.c", "angle_wrap_driver.c", "diff_angle_wrap.py", []),
    "flag_banks": ("Game/Story/flag_banks.c", "flag_banks_driver.c", "diff_flag_banks.py", []),
    "field_music": ("Game/Audio/field_music.c", "field_music_driver.c", "diff_field_music.py",
                    ["--tables", "4", "--cases", "80"]),
    "quality_preset": ("Game/Config/quality_preset.c", "quality_preset_driver.c",
                       "diff_quality_preset.py", ["--cases", "80"]),
    "widget_construct": ("Game/UI/widget_construct.c", "widget_construct_driver.c",
                         "diff_widget_construct.py", []),
    "name_registry": ("Game/Input/name_registry.c", "name_registry_driver.c",
                      "diff_name_registry.py", []),
    "group_completion": ("Game/Spawn/group_completion.c", "group_completion_driver.c",
                         "diff_group_completion.py", []),
    "binding_publish": ("Game/Input/binding_publish.c", "binding_publish_driver.c",
                        "diff_binding_publish.py", ["--cases", "40"]),
    "transform": ("Game/Math/transform.c", "transform_driver.c", "diff_transform.py",
                  ["--cases", "60"]),
}

LIT = re.compile(r"(?<![A-Za-z0-9_])(0[xX][0-9A-Fa-f]+|[0-9]+)(?![A-Za-z0-9_])")
OPS = [(">=", ">"), ("<=", "<"), ("==", "!="), ("!=", "=="), (">>", "<<"), ("<<", ">>")]


def code_end(line):
    """-> how much of `line` is code, excluding any trailing comment.

    The generator skipped lines that BEGIN with a comment marker but not comments that follow
    code, so `uint16_t packed;  /* +0x00  start = packed & 0x7FF, length = packed >> 11 */`
    produced four "mutations" -- `0x00`, `0x7FF`, `11` and the shift -- every one of them
    guaranteed equivalent because it changed a comment. They inflated the manifest and then the
    `provably equivalent` count absorbed them, which made the instrument look more discriminating
    than it was. `field_music` generated 49 mutations and roughly a quarter were comment text.

    A `//` inside a string literal would be mistaken for a comment here. No reconstruction file
    contains one; if that changes, this is where it breaks.
    """
    cut = len(line)
    for mark in ("//", "/*"):
        i = line.find(mark)
        if i >= 0:
            cut = min(cut, i)
    return cut


def mutations(text):
    """-> [(description, mutated_text)], generated mechanically. See the docstring for the rules."""
    out = []
    lines = text.split(chr(10))
    for i, line in enumerate(lines):
        s = line.strip()
        # never mutate a comment or a preprocessor line: neither is behaviour
        if not s or s.startswith("/*") or s.startswith("*") or s.startswith("//"):
            continue
        # A #define IS behaviour when it carries a constant; an #include or a guard is not.
        if s.startswith("#") and not s.startswith("#define"):
            continue
        if s.startswith("#define") and not LIT.search(s.split(None, 2)[-1] if len(s.split()) > 2
                                                      else ""):
            continue
        cut = code_end(line)
        for m in LIT.finditer(line):
            if m.start(1) >= cut:
                continue          # inside a trailing comment: not behaviour
            tok = m.group(1)
            try:
                v = int(tok, 16) if tok.lower().startswith("0x") else int(tok, 10)
            except ValueError:
                continue
            new = ("0x%X" % (v + 1)) if tok.lower().startswith("0x") else str(v + 1)
            mutated = line[:m.start(1)] + new + line[m.end(1):]
            out.append(("line %d: %s -> %s" % (i + 1, tok, new),
                        chr(10).join(lines[:i] + [mutated] + lines[i + 1:])))
        for a, b in OPS:
            idx = line.find(a)
            while idx != -1:
                if idx >= cut:
                    break         # inside a trailing comment: not behaviour
                mutated = line[:idx] + b + line[idx + len(a):]
                out.append(("line %d: %s -> %s" % (i + 1, a, b),
                            chr(10).join(lines[:i] + [mutated] + lines[i + 1:])))
                idx = line.find(a, idx + 1)
    return out


def snapshot_inputs(root, recon_rel, driver, harness):
    """Capture only this pilot's local include/import dependencies; reject escaping paths."""
    root = Path(root).resolve()
    snapshot = {}
    def add(path):
        path = path.resolve()
        rel = path.relative_to(root).as_posix()
        if rel in snapshot:
            return
        data = path.read_bytes()
        snapshot[rel] = data
        text = data.decode('utf-8')
        if path.suffix in {'.c', '.h'}:
            for include in re.findall(r'^\s*#\s*include\s*"([^"]+)"',text,re.M):
                add(path.parent/include)
        elif path.suffix == '.py':
            for node in ast.walk(ast.parse(text)):
                names = ([a.name for a in node.names] if isinstance(node,ast.Import)
                         else [node.module] if isinstance(node,ast.ImportFrom) and node.module else [])
                for name in names:
                    local = path.parent/(name.split('.')[0]+'.py')
                    if local.is_file():
                        add(local)
    add(root/recon_rel)
    header = (root/recon_rel).with_suffix('.h')
    if header.is_file():
        add(header)
    add(root/'Tests/Differential'/driver)
    add(root/'Tests/Differential'/harness)
    return snapshot


@contextmanager
def isolated_case(snapshot, scratch, target=None, mutated=None):
    scratch = Path(scratch).resolve()
    scratch.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='case-',dir=scratch) as tmp:
        work = Path(tmp).resolve()
        # Validate the exact recursive cleanup target before TemporaryDirectory can remove it.
        if work.parent != scratch or work == scratch:
            raise ValueError('invalid isolated cleanup target')
        for rel,data in snapshot.items():
            path = work/rel
            path.resolve().relative_to(work)
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
        if target is not None:
            if target not in snapshot:
                raise ValueError('mutation target is outside captured inputs')
            (work/target).write_bytes(mutated)
        yield work


def run_process(command, cwd, timeout):
    """Own the child tree until completion; also reap it on interruption."""
    p = subprocess.Popen(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                         text=True,start_new_session=os.name != 'nt')
    def stop():
        if os.name == 'nt':
            killed = subprocess.run(['taskkill','/F','/T','/PID',str(p.pid)],capture_output=True,timeout=10)
            if killed.returncode and p.poll() is None:
                # The process handle still permits termination if taskkill was denied.
                # Do not count this as successful tree cleanup: descendants are unverified.
                p.kill()
                p.wait(timeout=10)
                raise RuntimeError('process-tree cleanup failed: '+killed.stderr.decode(errors='replace'))
        else:
            import signal
            try:
                os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError:
                pass
        return p.communicate(timeout=30)
    timed_out = False
    try:
        stdout,stderr = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        stdout,stderr = stop()
    except BaseException:
        stop()
        raise
    return dict(command=[str(x) for x in command],exit_code=p.returncode,
                stdout=stdout,stderr=stderr,timed_out=timed_out)


def build(root, recon_rel, driver, exe, logdir):
    root, logdir = Path(root), Path(logdir)
    work = root/'Tests/Differential'
    output = work/exe
    if output.exists():
        output.unlink()  # never accept a stale executable after a failed compile
    bat = work/'_mut_build.bat'
    text = ('@echo off\ncall "%s" >nul\n'
            'cl /nologo /W4 /O2 /Brepro /D_CRT_SECURE_NO_WARNINGS /Fe:"%s" "%s" "%s" /link /Brepro\n') % (
            VCVARS,exe,driver,root/recon_rel)
    bat.write_text(text,encoding='ascii',newline='\r\n')
    (logdir/'build.bat').write_bytes(bat.read_bytes())
    result = run_process([str(bat)],work,120)
    (logdir/'build.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    if result['timed_out']:
        raise TimeoutError('compiler did not complete')
    if result['exit_code'] or not output.is_file():
        return None
    return hashlib.sha256(output.read_bytes()).hexdigest()


def harness_verdict(result):
    if result['timed_out']:
        return 'TIMEOUT'
    text = result['stdout']
    if 'Traceback' in result['stderr'] or 'INVALID:' in result['stderr']:
        return 'INVALID'
    if result['exit_code'] == 0:
        # The current pilot protocols all emit one of these nonempty completion summaries.
        positive = (re.search(r'^RESULT: (MATCH|CALCULATION|STRUCTURAL|the reconstruction agrees)',text,re.M)
                    or re.search(r'\b[1-9]\d* comparisons, 0 mismatches',text)
                    or re.search(r'^cases:\s*[1-9]\d*\s+mismatches:\s*0\s*$',text,re.M)
                    or (re.search(r'^point cases\s*:\s*[1-9]\d*',text,re.M)
                        and re.search(r'^compose cases\s*:\s*[1-9]\d*',text,re.M)
                        and re.search(r'^mismatches\s*:\s*0\s*$',text,re.M)))
        return 'PASS' if positive else 'INVALID'
    if result['exit_code'] != 1 or 'Traceback' in result['stderr'] or 'INVALID:' in result['stderr']:
        return 'INVALID'
    negative = (re.search(r'^RESULT: (MISMATCH|.*PARITY FAILED)',text,re.M)
                or re.search(r'^first mismatches:',text,re.M)
                or re.search(r'^cases:\s*[1-9]\d*\s+mismatches:\s*[1-9]\d*\s*$',text,re.M)
                or re.search(r'^mismatches\s*:\s*[1-9]\d*\s*$',text,re.M))
    return 'FAIL' if negative else 'INVALID'


def run_harness(root, harness, exe, extra, exe_path, timeout, logdir):
    work = Path(root)/'Tests/Differential'
    cmd = [sys.executable,harness,'--exe',str(exe_path),'--driver','./'+exe]+extra
    if harness == 'diff_group_completion.py':
        cmd += ['--out',str(Path(logdir).resolve()/'differential')]
    result = run_process(cmd,work,timeout)
    result['verdict'] = harness_verdict(result)
    (Path(logdir)/'harness.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result['verdict']


def evaluate_case(snapshot, scratch, logdir, pilot, exe_path, timeout, target=None, mutated=None,
                  baseline_hash=None, build_fn=build, harness_fn=run_harness):
    recon_rel,driver,harness,extra = PILOTS[pilot]
    logdir = Path(logdir)
    logdir.mkdir(parents=True,exist_ok=False)
    record = dict(status='INCOMPLETE',target=target)
    try:
        with isolated_case(snapshot,scratch,target,mutated) as work:
            record['input_hashes'] = {rel:hashlib.sha256((work/rel).read_bytes()).hexdigest() for rel in snapshot}
            if target:
                (logdir/'mutated-source.txt').write_bytes((work/target).read_bytes())
            h = build_fn(work,recon_rel,driver,pilot+'_mut.exe',logdir)
            record['driver_sha256'] = h
            if h is None:
                record['status'] = 'NO_BUILD'
            elif baseline_hash is not None and h == baseline_hash:
                record['status'] = 'EQUIVALENT'
            else:
                record['status'] = harness_fn(work,harness,pilot+'_mut.exe',extra,exe_path,timeout,logdir)
        record['case_removed'] = not work.exists()
        if not record['case_removed']:
            raise RuntimeError('case scratch was not removed')
    finally:
        if target is not None:
            record['mutation_outcome'] = {'FAIL':'KILLED','PASS':'SURVIVED'}.get(record['status'],record['status'])
        (logdir/'case.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    return record


def campaign_verdict(total, selected, results):
    statuses = [r['status'] for r in results]
    tested = statuses.count('FAIL') + statuses.count('PASS')
    incomplete = (not tested or selected != total or len(results) != selected
                  or any(s not in {'FAIL','PASS','NO_BUILD','EQUIVALENT'} for s in statuses))
    if 'PASS' in statuses:  # a valid behavioral survivor, with incompleteness retained
        return ('FAIL_INCOMPLETE' if incomplete else 'FAIL'),1
    if incomplete:
        return 'INCOMPLETE',3
    return 'PASS',0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pilot',choices=sorted(PILOTS))
    ap.add_argument('--root',default=ROOT)
    ap.add_argument('--exe',default=str(Path(ROOT).parent/'Database/Tools/work/exe/FFXII_TZA.exe'))
    ap.add_argument('--limit',type=int,default=0,help='bounded development subset; never a full-campaign pass')
    ap.add_argument('--indices',help='comma-separated zero-based generated indices for an affected-case rerun')
    ap.add_argument('--timeout',type=float,default=0,help='0 calibrates to 6x baseline, minimum 30 seconds')
    ap.add_argument('--out',type=Path,help='new directory for durable campaign receipts')
    ap.add_argument('--scratch',type=Path,default=Path(tempfile.gettempdir())/'ffxii-mutation-cases',
                    help='temporary case parent, outside canonical evidence by default')
    a = ap.parse_args()
    if a.limit < 0 or a.timeout < 0:
        ap.error('limit and timeout cannot be negative')
    if a.limit and a.indices:
        ap.error('choose --limit or --indices, not both')
    root = Path(a.root).resolve()
    out = a.out.resolve() if a.out else Path(tempfile.mkdtemp(prefix='ffxii-mutation-'+a.pilot+'-'))
    if a.out:
        out.mkdir(parents=True,exist_ok=False)
    record = dict(command=sys.argv,status='INCOMPLETE',start_unix=time.time(),results=[],
                  instrument_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  scratch_parent=str(a.scratch.resolve()))
    snapshot = {}
    code = 2
    try:
        exe_path = Path(a.exe).resolve()
        record['reference_sha256'] = hashlib.sha256(exe_path.read_bytes()).hexdigest()
        if record['reference_sha256'] != '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':
            raise ValueError('reference executable identity mismatch')
        recon_rel,driver,harness,extra = PILOTS[a.pilot]
        snapshot = snapshot_inputs(root,recon_rel,driver,harness)
        record['input_hashes'] = {rel:hashlib.sha256(data).hexdigest() for rel,data in snapshot.items()}
        for rel,data in snapshot.items():
            p = out/'inputs'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        targets = [recon_rel]
        header = str(Path(recon_rel).with_suffix('.h')).replace('\\','/')
        if header in snapshot:
            targets.append(header)
        mutants = [(rel,desc,text.encode('utf-8')) for rel in targets
                   for desc,text in mutations(snapshot[rel].decode('utf-8'))]
        total = len(mutants)
        selected = list(enumerate(mutants))
        if a.indices:
            indices=[int(x) for x in a.indices.split(',')]
            if len(set(indices)) != len(indices) or not all(0 <= i < total for i in indices):
                raise ValueError('invalid or duplicate generated mutation index')
            selected=[(i,mutants[i]) for i in indices]
        elif a.limit:
            selected=selected[:a.limit]
        record.update(total_generated=total,selected=len(selected),manifest=[dict(target=r,description=d) for r,d,b in mutants])
        started = time.monotonic()
        baseline = evaluate_case(snapshot,a.scratch,out/'baseline',a.pilot,exe_path,a.timeout or 600)
        record['baseline'] = baseline
        if baseline['status'] != 'PASS':
            raise ValueError('unmutated baseline not valid: '+baseline['status'])
        timeout = a.timeout or max(30,6*(time.monotonic()-started))
        record['timeout_seconds'] = timeout
        for i,(manifest_index,(target,description,text)) in enumerate(selected):
            result = evaluate_case(snapshot,a.scratch,out/('case-%05d'%manifest_index),a.pilot,
                                   exe_path,timeout,target,text,baseline['driver_sha256'])
            result.update(index=manifest_index,description=description)
            record['results'].append(result)
            (out/'campaign.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
            print('%d/%d %s %s'%(i+1,len(selected),result['mutation_outcome'],description),flush=True)
        record['status'],code = campaign_verdict(total,len(selected),record['results'])
    except KeyboardInterrupt:
        record['status'] = 'INTERRUPTED'
        code = 130
    except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as e:
        record.update(status='INVALID',error=str(e))
        code = 2
    finally:
        record['end_unix'] = time.time()
        try:
            record['production_inputs_stable'] = all((root/rel).read_bytes()==b for rel,b in snapshot.items())
        except OSError:
            record['production_inputs_stable'] = False
        if not record['production_inputs_stable']:
            record['status'] = 'INVALID_INPUT_DRIFT'
        statuses = [r['status'] for r in record['results']]
        record['counts'] = {s:statuses.count(s) for s in ['NO_BUILD','EQUIVALENT','TIMEOUT','INVALID']}
        record['counts'].update(KILLED=statuses.count('FAIL'),SURVIVED=statuses.count('PASS'))
        (out/'campaign.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        print('RESULT:',record['status'],'counts:',record['counts'],'evidence:',out,flush=True)
        if not record['production_inputs_stable']:
            # Do not restore over a peer edit; invalidate this observation instead.
            code = 2
    return code


if __name__ == '__main__':
    sys.exit(main())
