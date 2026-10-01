"""EO3-only connector for the qualified stopped context/read callback shape.

The runner must establish designated process/reference identity and supply the
tested stop/abort handling. This module does not attach, launch, resume or stop.
"""
import ctypes
import time
from match import PRODUCER,BUILDER,ISSUER
from ownership import owned_step


class EO3Callback:
    def __init__(self,recorder,probe_factory,clock=time.monotonic):
        self.recorder=recorder;self.probe_factory=probe_factory;self.clock=clock

    def __call__(self,m,pid,handle,tid,ctx,audit):
        event=audit.event;row=audit.last_get
        assert event and event['pid']==pid and event['tid']==tid
        assert event['code']==1 and event['exception']==0x80000004 and event['first_chance']==1
        assert row['event']==event and row['thread_binding'] and row['thread_binding']['tid']==tid
        assert row['api']=='GetThreadContext' and row['result']==1
        assert row['address']==ctypes.addressof(ctx) and row['context_hex']==bytes(ctx).hex()
        assert owned_step(ctx,event['address'],[PRODUCER,BUILDER,ISSUER])
        reader=self.probe_factory(handle)
        previous=len(self.recorder.events)
        decision=self.recorder.event(row,tid,self.clock(),reader.read)
        return dict(decision=decision,reason=self.recorder.reason,debug_event=dict(event),
                    context_api_index=row['api_index'],
                    recorder_event_index=previous if len(self.recorder.events)>previous else None,
                    semantic_payload_bytes=self.recorder.bytes,
                    limits='Context/read connector only; process/reference identity, abort and live health are runner obligations.')
