// @category GFZ
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class GFZFunctionAnnotationSnapshotV2 extends GhidraScript {
    static final byte[] MAGIC = new byte[]{'G','F','Z','A','N','N','2',0};
    static void putString(DataOutputStream d, String s) throws IOException {
        if (s == null) { d.writeInt(-1); return; }
        byte[] b=s.getBytes(StandardCharsets.UTF_8); d.writeInt(b.length); d.write(b);
    }
    static String nsName(Function f) {
        Namespace ns=f.getParentNamespace(); return ns==null?null:ns.getName(true);
    }
    public void run() throws Exception {
        String[] a=getScriptArgs(); if(a.length!=1) throw new IllegalArgumentException("output path required");
        List<Function> fs=new ArrayList<>();
        FunctionIterator it=currentProgram.getFunctionManager().getFunctions(true);
        while(it.hasNext()){Function f=it.next(); if(!f.isExternal()) fs.add(f);}
        fs.sort(Comparator.comparingLong(f->f.getEntryPoint().getOffset()));
        try(DataOutputStream d=new DataOutputStream(new BufferedOutputStream(new FileOutputStream(a[0])))) {
            d.write(MAGIC); d.writeInt(2); d.writeInt(fs.size());
            for(Function f:fs){
                ByteArrayOutputStream rb=new ByteArrayOutputStream(4096);
                DataOutputStream r=new DataOutputStream(rb);
                r.writeLong(f.getEntryPoint().getOffset());
                putString(r,f.getName());
                putString(r,nsName(f));
                Symbol sym=f.getSymbol(); putString(r,sym==null?null:sym.getSource().toString());
                putString(r,f.getComment());
                putString(r,f.getRepeatableComment());
                putString(r,f.getPrototypeString(false,true));
                putString(r,f.getSignatureSource()==null?null:f.getSignatureSource().toString());
                putString(r,f.getCallingConventionName());
                r.writeBoolean(f.isInline()); r.writeBoolean(f.hasNoReturn()); r.writeBoolean(f.hasVarArgs()); r.writeBoolean(f.isThunk());
                Function tf=f.getThunkedFunction(false); r.writeLong(tf==null?-1L:tf.getEntryPoint().getOffset());
                // Body extents are structural guardrails and make accidental function-shape changes visible.
                List<AddressRange> ranges=new ArrayList<>();
                AddressRangeIterator rit=f.getBody().getAddressRanges(); while(rit.hasNext()) ranges.add(rit.next());
                ranges.sort(Comparator.comparingLong(x->x.getMinAddress().getOffset()));
                r.writeInt(ranges.size()); for(AddressRange ar:ranges){r.writeLong(ar.getMinAddress().getOffset());r.writeLong(ar.getMaxAddress().getOffset());}
                List<FunctionTag> tags=new ArrayList<>(f.getTags());
                tags.sort((x,y)->{int c=x.getName().compareTo(y.getName()); if(c!=0)return c; String a1=x.getComment()==null?"":x.getComment(), b1=y.getComment()==null?"":y.getComment(); return a1.compareTo(b1);});
                r.writeInt(tags.size());
                for(FunctionTag t:tags){putString(r,t.getName());putString(r,t.getComment());}
                r.flush(); byte[] rec=rb.toByteArray(); d.writeInt(rec.length); d.write(rec);
            }
        }
        println("GFZ_ANNOTATION_SNAPSHOT_V2_WRITTEN functions="+fs.size()+" path="+a[0]);
    }
}
