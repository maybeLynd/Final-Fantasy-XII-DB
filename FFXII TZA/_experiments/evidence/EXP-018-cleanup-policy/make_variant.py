"""Create one private hwbp variant from the checked exit-policy source from EXP-017."""
from pathlib import Path
import hashlib
import difflib

out = Path(__file__).resolve().parent
original = (out/'hwbp-original.py').read_bytes()
assert not (out/'hwbp-variant.py').exists(), 'Preserve prior instrument output'
assert not (out/'variant.diff').exists(), 'Preserve prior source diff'
assert hashlib.sha256(original).hexdigest() == 'fb69cd13ee47c54745c9e5942aebbe6a5b2b574ebe145e3a8d8a6c800b10e091'
source = original.decode().replace('\r\n','\n')
variant = source

def replace(old, new):
    global variant
    assert variant.count(old) == 1, old
    variant = variant.replace(old,new)

replace('    a = ap.parse_args()', '''    ap.add_argument('--cleanup-before-continue', action='store_true')
    ap.add_argument('--api-out', required=True)
    a = ap.parse_args()
    from api_receipts import Audit
    global k32
    audit = Audit(k32, a.api_out)
    k32 = audit
    cleared_at_final_event = False''')
replace('''                            if a.stop_after and total_hits >= a.stop_after:
                                resume_past_breakpoint(ev.dwThreadId)''', '''                            if a.stop_after and total_hits >= a.stop_after:
                                if a.cleanup_before_continue:
                                    audit.mark('clear_before_continue_begin', tid=ev.dwThreadId)
                                    clears = [(tid, set_slots(tid, [])) for tid in threads_of(pid)]
                                    cleared_at_final_event = bool(clears) and all(ok for tid,ok in clears)
                                    audit.mark('clear_before_continue_end', results=clears,
                                               all_succeeded=cleared_at_final_event)
                                resume_past_breakpoint(ev.dwThreadId)''')
replace('''        for tid in threads_of(pid):
            set_slots(tid, [])
        k32.DebugActiveProcessStop(pid)''', '''        try:
            if not cleared_at_final_event:
                audit.mark('fallback_or_original_clear_after_continue')
                for tid in threads_of(pid):
                    set_slots(tid, [])
            k32.DebugActiveProcessStop(pid)
        finally:
            audit.save()''')
replace('''    except OSError as error:
        sys.stderr.write''', '''    except OSError as error:
        audit.save()
        sys.stderr.write''')
(out/'hwbp-variant.py').write_text(variant,encoding='utf-8',newline='\n')
(out/'variant.diff').write_text(''.join(difflib.unified_diff(source.splitlines(True),
                               variant.splitlines(True),fromfile='hwbp-original.py',
                               tofile='hwbp-variant.py')),encoding='utf-8',newline='\n')
print(hashlib.sha256(variant.encode()).hexdigest())
