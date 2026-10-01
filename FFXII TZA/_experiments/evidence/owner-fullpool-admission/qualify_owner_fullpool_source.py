"""Bounded reuse of the existing reviewed-role original-body qualifier."""
import hashlib
import importlib.util
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
helper=HERE/'qualify_owner_queue_order_source.py'
spec=importlib.util.spec_from_file_location('fullpool_retained_qualifier',helper)
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)

if __name__=='__main__':
    q.main(Path(sys.argv[1]),q.UP,entries=[0x3dda70,0x32e620,0x32e870],include_pump_table=False)
    print('OUTER_DRIVER_SHA256:'+hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
