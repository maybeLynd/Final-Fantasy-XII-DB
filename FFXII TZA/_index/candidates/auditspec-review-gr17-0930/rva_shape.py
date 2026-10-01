import os,sys,struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T
for a in [0x01D6BA10,0x01D6BA20,0x01D6AFDC,0x01D6B03C,0x01D6BFCC,0x01D6BFDC,0x01D75184,0x01D751C0,0x01D751D0,0x01D823CC,0x01D823DC,0x01D78040,0x01D78084,0x01D77F20,0x01D77F34,0x01D77F44]:
    b,e,u=struct.unpack("<III",T.rd(a,12))
    print("%08X begin %08X end %08X unwind %08X  shape=%s" % (a,b+T.IB,e+T.IB,u+T.IB, e>b and 0x01C00000<=u+T.IB<0x02000000))
for t in (0x003304A0,0x0032F850):
    print("%08X rip refs"%t, T.rip_refs(t,t+1), T.data_refs(t)["abs64"])
