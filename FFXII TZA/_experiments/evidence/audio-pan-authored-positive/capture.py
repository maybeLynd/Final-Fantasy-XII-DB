"""Selected authored headers only; reuse the existing VBF index reader.

No FF12 execution, broad corpus census, archive writes or full-archive hash claim.
All output files are exclusive. A failed decode is invalid, never treated as raw.
"""
import hashlib
import io
import json
from pathlib import Path
import struct
import sys
import time
import zlib

E=Path(__file__).resolve().parent
ROOT=E.parents[4]
TOOLS=ROOT/'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0,str(TOOLS))
from census_format_magics import load_index

VBF=Path('D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FFXII_TZA.vbf')
EXE=VBF.parent/'x64/FFXII_TZA.exe'
EXPECTED_EXE='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
PATHS=[
 'ps2data/sound/se/sead_data_win/se001/se001001.win.sab',
 'ps2data/sound/se/sead_data_win/se001/se001002.win.sab',
 'ps2data/sound/se/sead_data_win/se000/se000.win.sab',
]
sha=lambda b:hashlib.sha256(b).hexdigest()


def write(path,data):
    with path.open('xb') as f:f.write(data)


def main():
    board=json.loads((ROOT/'Database/FFXII TZA/_index/_inbox/TEAM.json').read_text())
    assert any(t['id']=='ASTRA-SAB-OVERRIDE-AUTHORED-POSITIVE' and t['agent']=='ASTRA'
               and t['status']=='ACTIVE' for t in board['tasks'])
    assert sha(EXE.read_bytes())==EXPECTED_EXE
    reader=(TOOLS/'census_format_magics.py').read_bytes()
    record=dict(status='INVALID',method='A: selected authored archive blocks, no execution',
                started_unix=time.time(),paths=PATHS,source_sha256=sha(Path(__file__).read_bytes()),
                index_reader_sha256=sha(reader),python=sys.version,zlib=zlib.ZLIB_RUNTIME_VERSION,
                executable_path=str(EXE),executable_sha256=EXPECTED_EXE,
                archive_path=str(VBF),entries=[])
    write(E/'index-reader.py',reader)
    st=VBF.stat()
    record['before']=dict(size=st.st_size,mtime_ns=st.st_mtime_ns)
    try:
        with VBF.open('rb') as f:
            prefix=f.read(16)
            magic,header_len,num=struct.unpack('<4sIQ',prefix)
            assert magic==b'SRYK' and 16<header_len<record['before']['size']
            f.seek(0);header=f.read(header_len)
            assert len(header)==header_len
            names,blocks=load_index(io.BytesIO(header))
            assert len(names)==num and all(n in names for n in PATHS)
            order=list(names)
            entry_base=0x10+num*16
            string_base=entry_base+num*32
            string_size=struct.unpack_from('<I',header,string_base)[0]
            block_base=string_base+string_size
            record['archive_index']=dict(prefix_hex=prefix.hex(),header_size=header_len,
                sha256=sha(header),entry_count=num,string_size=string_size,
                string_size_hex=header[string_base:string_base+4].hex(),block_base=block_base)
            for n,path in enumerate(PATHS):
                idx=order.index(path)
                raw_record=header[entry_base+idx*32:entry_base+(idx+1)*32]
                sb,sb2,size,offset,name_offset=struct.unpack('<IIQQQ',raw_record)
                assert (sb,size,offset)==names[path]
                csize=blocks[sb] or 0x10000
                expected=min(size,0x10000)
                assert size>=0x60 and header_len<=offset and offset+csize<=st.st_size
                encoded=path.encode()+b'\0'
                name_at=string_base+4+name_offset
                assert header[name_at:name_at+len(encoded)]==encoded
                assert name_at+len(encoded)<=block_base
                raw_length=header[block_base+sb*2:block_base+sb*2+2]
                assert struct.unpack('<H',raw_length)[0]==blocks[sb]
                f.seek(offset);raw=f.read(csize)
                assert len(raw)==csize
                if csize==expected:
                    decoded=raw;compression='stored'
                else:
                    dec=zlib.decompressobj();decoded=dec.decompress(raw,expected+1)
                    assert dec.eof and not dec.unused_data and not dec.unconsumed_tail
                    assert len(decoded)==expected
                    compression='zlib'
                assert len(decoded)==expected
                stem=f'{n:02d}'
                write(E/(stem+'-archive-block.bin'),raw)
                write(E/(stem+'-decoded-block.bin'),decoded)
                # These are first-block format controls, not whole-bank validity.
                assert decoded[:4]==b'sabf' and decoded[4]==2 and decoded[8]==4
                assert struct.unpack_from('<I',decoded,12)[0]==size
                length=decoded[9];bank=decoded[16:16+length]
                assert decoded[16+length]==0 and path.rsplit('/',1)[1].startswith(bank.decode())
                directory=((16+length)&0xf0)+struct.unpack_from('<H',decoded,6)[0]
                tags=[decoded[directory+i*16:directory+i*16+4] for i in range(4)]
                assert tags==[b'snd ',b'seq ',b'trk ',b'mtrl']
                record['entries'].append(dict(path=path,index=idx,record_offset=entry_base+idx*32,
                    record_hex=raw_record.hex(),opaque_index_hash_hex=header[16+idx*16:32+idx*16].hex(),
                    name_offset_in_archive=name_at,name_hex=encoded.hex(),
                    block_size_offset=block_base+sb*2,block_size_hex=raw_length.hex(),
                    block_offset=offset,compressed_size=csize,decoded_size=expected,compression=compression,
                    raw_file=stem+'-archive-block.bin',raw_sha256=sha(raw),
                    decoded_file=stem+'-decoded-block.bin',decoded_sha256=sha(decoded),
                    header_hex=decoded[:16].hex(),bank_name=bank.decode(),entry_size=size,
                    param_word=struct.unpack_from('<H',decoded,10)[0]))
                f.seek(offset);assert f.read(csize)==raw, 'selected block changed during capture'
            f.seek(0);assert f.read(header_len)==header, 'archive index changed during capture'
        end=VBF.stat()
        record['after']=dict(size=end.st_size,mtime_ns=end.st_mtime_ns)
        assert record['after']==record['before']
        record['status']='BOUNDED_AUTHORED_OBSERVATIONS'
    except BaseException as error:
        record['error']=repr(error)
        raise
    finally:
        record['ended_unix']=time.time()
        write(E/'capture.json',(json.dumps(record,indent=2)+'\n').encode())
    for e in record['entries']:print(e['path'],e['bank_name'],'word+0A=',e['param_word'])


if __name__=='__main__':main()
