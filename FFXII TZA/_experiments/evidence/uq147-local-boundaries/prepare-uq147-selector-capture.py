"""Configure the existing bounded capture wrapper for the Dismiss roster selector."""
import hashlib
from pathlib import Path
W=Path(__file__).resolve().parent
P=W/'uq147-summoner-cleanup-order'
base=P/'capture-defeat-boundary.py'
assert hashlib.sha256(base.read_bytes()).hexdigest()=='e318100b6f9582028bbdd4206d4c8643f351b270841b3a8a924d070b824be784'
s=base.read_text()
changes=[
 ('Exact UQ147 defeat/recompute boundary and designated-unit lookup, STATIC_ONLY.', 'Exact Dismiss roster-slot selector and two closed leaf spans, STATIC_ONLY.'),
 ("['preview-defeat-01','preview-combatant-lookup-01']", "['preview-class3-lookup-01','preview-class3-object-01','preview-unit-reader-01']"),
 ("[('lookup-defeat-01',['0x300fc0','0x301133']),('lookup-combatant-01',['0x31b770','0x31b7da'])]", "[('lookup-class3-lookup-01',['0x31b8c0','0x31b8df']),('lookup-index-table-01',['0x263750','0x263767']),('lookup-actor-unit-leaf-01',['0x263e30','0x263e35'])]"),
 ('for entry in [0x300fc0,0x31b770]:', 'for entry in [0x31b8c0,0x263750,0x263e30]:'),
 ("        if len(roots)!=1:raise ValueError('ambiguous physical root')", """        if not roots and entry in {0x263750,0x263e30}:
            # These direct original targets are leaf spans without .pdata roots.
            # Their complete local CFG/RET closure is checked by the consumer;
            # do not fabricate an unwind root or infer global function identity.
            end={0x263750:0x263767,0x263e30:0x263e35}[entry]
            z=read(entry,end-entry)
            bodies.append(dict(entry=hex(entry),end_exclusive=hex(end),bytes=len(z),sha256=hashlib.sha256(z).hexdigest(),physical_bytes=z.hex(),records=[],identity_kind='Direct original target, declared closed leaf span; no .pdata root'))
            continue
        if len(roots)!=1:raise ValueError('ambiguous physical root')"""),
 ('Complete local shipping bodies and actual reviewed role controls, not callee effects, command acceptance, cleanup timing, natural state/reachability or presentation. Current exact previews are feasibility only. Retained native fixtures disclose scripted recompute; this source capture is not their rerun or natural KO reachability.', 'One .pdata-bounded selector and two declared direct-target leaf spans without .pdata roots. Consumer must verify their complete local CFG/RET closure. Preview labels class3 refer to roster slot index3, NOT ActorStorage class3. Physical bytes/reviewed roles, not initialized roster, KO admission, lifetime, gameplay scheduling or presentation. No fixture/live rerun.')]
for old,new in changes:
    if s.count(old)!=1:raise ValueError('Exact capture-template preimage changed: '+old[:60])
    s=s.replace(old,new)
out=P/'capture-dismiss-selector-boundary.py'
with out.open('x') as f:f.write(s)
print(hashlib.sha256(out.read_bytes()).hexdigest())
