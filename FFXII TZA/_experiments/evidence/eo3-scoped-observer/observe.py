"""Scoped EO3 stopped-event recorder. No native API, attach or resume operation.

The caller supplies a proven successful context read and exact read callback.
This object may request HOLD_FOR_OWNED_ABORT; it must never be connected to a
resume-unconditionally capture loop. Native delivery/abort remain unqualified.
"""
import copy
import struct
from match import Match, PRODUCER, BUILDER, ISSUER, PRIMARY_RETURN, sext
from project import project


class Recorder:
    def __init__(self, started):
        self.started = started
        self.match = Match()
        self.events = []
        self.reads = []
        self.bytes = 0
        self.producers_seen = 0
        self.decision = 'CONTINUE'
        self.reason = None

    def stop(self, reason, hold=False):
        self.decision = 'HOLD_FOR_OWNED_ABORT' if hold else 'STOP_NO_VERDICT'
        self.reason = reason
        return self.decision

    def read(self, address, size, purpose, reader):
        if self.bytes + size > 32768:
            raise ValueError('semantic payload budget')
        self.bytes += size  # attempted bytes also count
        receipt = dict(address=address, size=size, purpose=purpose, hex=None)
        self.reads.append(receipt)
        try:
            raw = reader(address, size)
            if not isinstance(raw, bytes) or len(raw) != size:
                raise ValueError('incomplete read')
            receipt['hex'] = raw.hex()
            return raw
        except Exception as error:
            receipt['error'] = str(error)
            raise

    def event(self, row, tid, now, reader):
        if self.decision != 'CONTINUE':
            raise ValueError('recorder stopped; explicit new session required')
        if now < self.started or now - self.started >= 10:
            return self.stop('clock/deadline', hold=True)
        if self.bytes + 1232 > 32768:
            return self.stop('semantic payload budget', hold=True)
        self.bytes += 1232
        event = dict(tid=tid, monotonic=now, context_read=copy.deepcopy(row), reads_begin=len(self.reads))
        self.events.append(event)
        try:
            ctx = project(row)
            ctx['tid'] = tid
            event['context'] = ctx
            if ctx['rip'] == PRODUCER:
                self.producers_seen += 1
                if self.producers_seen > 8:
                    return self.stop('producer budget', hold=True)
                parent = struct.unpack('<Q', self.read(ctx['rsp']+0x38,8,'producer return',reader))[0]
                event['parent_return'] = parent
                if parent != PRIMARY_RETURN:
                    event['selection'] = 'different caller; no semantic sample'
                else:
                    path = bytearray()
                    for offset in range(128):
                        path += self.read(ctx['rdi']+offset,1,'selected path byte',reader)
                        if path[-1] == 0:
                            break
                    self.match.producer(ctx,parent,bytes(path))
                    event['selection'] = 'selected primary caller'
                    if ctx['rdi'] != sext(ctx['rdi'] & 0xffffffff):
                        return self.stop('selected producer pointer loses identity; issuance unobserved',hold=True)
            elif ctx['rip'] == BUILDER:
                if (tid,ctx['rsp']+0x40) not in self.match.producers:
                    event['selection'] = 'unselected builder frame'
                else:
                    ret = struct.unpack('<Q',self.read(ctx['rsp']+0x38,8,'builder return',reader))[0]
                    raw = self.read(ctx['r10'],0x80,'completed selected slot',reader)
                    self.match.builder(ctx,ret,raw)
                    event['selection'] = 'selected builder'
            elif ctx['rip'] == ISSUER:
                if not any(a == ctx['rbx'] for a,i in self.match.requests):
                    event['selection'] = 'unselected issuer slot'
                else:
                    raw = self.read(ctx['rbx'],0x80,'selected issuer slot',reader)
                    self.match.issuer(ctx,raw)
                    event['selection'] = 'selected issuer'
                    if not self.match.producers and not self.match.requests:
                        self.match.finish()
                        self.decision = 'STOP_MATCHED_PENDING_HEALTH'
                        self.reason = 'first complete isolated request; not a live semantic verdict'
            else:
                raise ValueError('not a scoped observation site')
            if self.producers_seen >= 8 and self.decision == 'CONTINUE':
                return self.stop('producer budget',hold=True)
            return self.decision
        except Exception as error:
            return self.stop(type(error).__name__+': '+str(error),hold=True)
        finally:
            event['reads_end'] = len(self.reads)
            event['decision'] = self.decision
            event['reason'] = self.reason

    def finish(self):
        if self.decision != 'STOP_MATCHED_PENDING_HEALTH':
            raise ValueError('empty, incomplete, failed or stopped capture is not a match')
        return dict(status=self.decision, results=self.match.finish(),events=self.events,
                    reads=self.reads,semantic_payload_bytes=self.bytes,
                    limits=['No native adapter/delivery/abort qualification.',
                            'A matched record does not establish game health or normal reachability.',
                            'No scheduling transparency or historical crash cause.'])
