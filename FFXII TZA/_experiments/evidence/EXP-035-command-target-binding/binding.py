"""Compose qualified Reader.field(), EXP032 command reads and EXP034 resolution.
No OS calls or input. Returned consistency flags are not atomic/lifetime proof.
"""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent/'EXP-032-command-snapshot'),str(HERE.parent/'EXP-034-focus-resolver')]
from command_snapshot import snapshot
from reader_resolver import resolve


def sample(reader,slot=0,command_read=snapshot,resolve_read=resolve):
    before=reader.field()
    players=[r for r in before['rows'] if r['slot']==slot]
    if len(players)!=1:raise ValueError('selected player absent or ambiguous')
    player=players[0]
    first=command_read(reader,player['unit'],slot,player['actor'])
    resolved=resolve_read(reader,first['live']['target_focus_handle'])
    second=command_read(reader,player['unit'],slot,player['actor'])
    resolved_after=resolve_read(reader,second['live']['target_focus_handle'])
    after=reader.field()
    players_after=[r for r in after['rows'] if r['slot']==slot]
    same_player=len(players_after)==1 and all(players_after[0][k]==player[k] for k in ('unit','actor'))
    same_command=first['live']['raw']==second['live']['raw']
    same_resolution=resolved==resolved_after
    stable=same_player and same_command and same_resolution
    def join(field):
        if not resolved['unit']:return None,'unresolved'
        rows=[r for r in field['rows'] if r['unit']==resolved['unit']]
        if not rows:return None,'outside_filtered_census'
        if len(rows)!=1 or rows[0]['actor']!=resolved['actor']:return None,'identity_mismatch'
        return rows[0],'bound'
    target_before,before_kind=join(before)
    target_after,after_kind=join(after)
    if 'identity_mismatch' in (before_kind,after_kind):stable=False
    if before_kind!=after_kind:stable=False
    return dict(status='CONSISTENT_SAMPLE' if stable else 'AMBIGUOUS_SELECTION',
                frame_before=before['frame_before'],frame_after=after['frame_after'],
                player_before=player,player_after=players_after,
                command_before=first,command_after=second,
                resolution_before=resolved,resolution_after=resolved_after,
                same_player=same_player,same_command=same_command,same_resolution=same_resolution,
                target_before=target_before,target_after=target_after,
                binding_before=before_kind,binding_after=after_kind)
