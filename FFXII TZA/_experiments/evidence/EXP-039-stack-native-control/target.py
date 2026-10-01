"""Owned native call/RET fixture. Never discovers FFXII or any other process."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import sys
import time


def main(folder):
    k=ctypes.WinDLL('kernel32',use_last_error=True)
    k.VirtualAlloc.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32,ctypes.c_uint32]
    k.VirtualAlloc.restype=ctypes.c_void_p
    address=k.VirtualAlloc(None,4096,0x3000,0x40)
    if not address:raise ctypes.WinError(ctypes.get_last_error())
    # 0: sub rsp,28; 4: call +32; 9: add rsp,28; 13: ret.
    # 32: ret (executed); 33: ret (never executed, cold breakpoint).
    code=bytes.fromhex('4883ec28e8170000004883c428c3')+b'\xcc'*18+b'\xc3\xc3'
    ctypes.memmove(address,code,len(code))
    call=ctypes.CFUNCTYPE(None)(address)
    with (folder/'target-ready.json').open('x') as output:
        json.dump(dict(pid=os.getpid(),address=address,entry=address+32,cold=address+33,
                       return_address=address+9,code=code.hex(),code_sha256=hashlib.sha256(code).hexdigest()),output)
    with (folder/'heartbeat.bin').open('xb',buffering=0) as output:
        while True:
            call()
            output.write(b'.')
            time.sleep(.05)


if __name__=='__main__':main(Path(sys.argv[1]))
