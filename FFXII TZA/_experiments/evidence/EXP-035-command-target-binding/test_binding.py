"""Join-policy controls; component byte/original-code tests remain EXP032/034."""
import copy
import json
from pathlib import Path
import struct
import unittest
from binding import sample
from test_reader import Reader as ResolverFixtureReader


class Fixture:
    def __init__(self):
        self.before=dict(frame_before=10,frame_after=10,rows=[
            dict(slot=0,unit=0x1000,actor=0x2000,hp=103),
            dict(slot=7,unit=0x3000,actor=0x4000,hp=84)])
        self.after=copy.deepcopy(self.before)
        self.commands=[dict(live=dict(raw='first',target_focus_handle=0x123)) for _ in range(2)]
        self.resolutions=[dict(unit=0x3000,actor=0x4000,reason='resolved') for _ in range(2)]
        self.fields=iter([self.before,self.after])
    def field(self):return next(self.fields)
    def command(self,*args):return self.commands.pop(0)
    def resolve(self,*args):return self.resolutions.pop(0)
    def run(self):return sample(self,command_read=self.command,resolve_read=self.resolve)


class Tests(unittest.TestCase):
    def test_actual_components_against_original_chain_fixtures(self):
        path=Path(__file__).resolve().parent.parent/'EXP-034-focus-resolver/result.json'
        for case in json.loads(path.read_text())['results']:
            r=ResolverFixtureReader(case['fixture'])
            header=bytearray(24);header[0]=1;struct.pack_into('<Q',header,16,0x2000)
            block=bytearray(48);struct.pack_into('<Q',block,8,0x44440000)
            struct.pack_into('<I',block,16,case['handle'])
            r.memory.update({0x208D45C:struct.pack('<I',10),0x1000:bytes(header),
                             0x1EA9:b'\0',0x16B4:b'\0\0\0',0x1700:bytes(block)})
            field=dict(frame_before=10,frame_after=10,rows=[
                dict(slot=0,unit=0x1000,actor=0x2000,hp=103),
                dict(slot=7,unit=0x50003000,actor=0x50001000,hp=84)])
            r.field=lambda:copy.deepcopy(field)
            with self.subTest(case=case['name']):
                result=sample(r)
                self.assertEqual(result['status'],'CONSISTENT_SAMPLE')
                self.assertEqual(result['resolution_before']['unit'],case['actual'])
                self.assertEqual(result['binding_before'],'bound' if case['actual'] else 'unresolved')
    def test_exact_identity_binds_hp(self):
        r=Fixture().run()
        self.assertEqual(r['status'],'CONSISTENT_SAMPLE')
        self.assertEqual(r['target_before']['hp'],84)
        self.assertEqual(r['binding_after'],'bound')
    def test_changed_command_or_resolution_or_player_is_ambiguous(self):
        for change in ['command','resolution','player','actor']:
            f=Fixture()
            if change=='command':f.commands[1]['live']['raw']='second'
            if change=='resolution':f.resolutions[1]['actor']=0x999
            if change=='player':f.after['rows'][0]['unit']=0x999
            if change=='actor':f.after['rows'][1]['actor']=0x999
            with self.subTest(change=change):self.assertEqual(f.run()['status'],'AMBIGUOUS_SELECTION')
    def test_missing_census_entry_is_not_death_or_null_resolution(self):
        f=Fixture();f.before['rows'].pop();f.after['rows'].pop()
        r=f.run()
        self.assertEqual(r['binding_before'],'outside_filtered_census')
        self.assertEqual(r['resolution_before']['unit'],0x3000)
        self.assertIsNone(r['target_before'])
    def test_null_resolution_has_no_guessed_target(self):
        f=Fixture();f.resolutions=[dict(unit=0,actor=0,reason='zero_handle') for _ in range(2)]
        r=f.run();self.assertEqual(r['binding_before'],'unresolved');self.assertIsNone(r['target_before'])
    def test_disappearing_target_invalidates_pairing(self):
        f=Fixture();f.after['rows'].pop()
        self.assertEqual(f.run()['status'],'AMBIGUOUS_SELECTION')
    def test_read_error_is_not_swallowed(self):
        f=Fixture()
        def error(*args):raise ValueError('short read')
        with self.assertRaises(ValueError):sample(f,command_read=f.command,resolve_read=error)


if __name__=='__main__':unittest.main()
