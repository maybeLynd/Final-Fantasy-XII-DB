"""Create one private hwbp variant from the exact EXP-015 source."""
from pathlib import Path
import hashlib
import difflib

out = Path(__file__).resolve().parent
original = (out/'hwbp-original.py').read_bytes()
assert hashlib.sha256(original).hexdigest() == 'c0c643355ffdc09b82860744e35c5301535448302bdae92847aad631a50c87e5'
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
(out/'hwbp-variant.py').write_text(variant,encoding='utf-8',newline='\n')
(out/'variant.diff').write_text(''.join(difflib.unified_diff(source.splitlines(True),
                               variant.splitlines(True),fromfile='hwbp-original.py',
                               tofile='hwbp-variant.py')),encoding='utf-8',newline='\n')
print(hashlib.sha256(variant.encode()).hexdigest())
