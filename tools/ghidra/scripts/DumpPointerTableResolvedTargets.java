// @category GFZ
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*; import ghidra.program.model.address.*; import ghidra.program.model.data.*; import ghidra.program.model.symbol.*;
import java.io.*; import java.nio.charset.StandardCharsets; import java.util.*;
public class DumpPointerTableResolvedTargets extends GhidraScript {
 static String own(Function f){for(FunctionTag t:f.getTags())if(t.getName().startsWith("GFZ.V120.PrimaryOwner."))return t.getName().substring("GFZ.V120.PrimaryOwner.".length());return "";}
 static String cd(Function f){ArrayList<String>a=new ArrayList<>();for(FunctionTag t:f.getTags())if(t.getName().startsWith("GFZ.V121.CodeDomain."))a.add(t.getName().substring("GFZ.V121.CodeDomain.".length()));Collections.sort(a);return String.join(";",a);}
 public void run() throws Exception{String[] a=getScriptArgs(); if(a.length<2)throw new IllegalArgumentException("out addr..."); PrintWriter w=new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]),StandardCharsets.UTF_8)); Listing li=currentProgram.getListing();FunctionManager fm=currentProgram.getFunctionManager();
  w.println("table\tindex\tcomponent_addr\ttarget\tname\towner\tcode_domain");
  for(int ai=1;ai<a.length;ai++){Address ad=toAddr(Long.parseUnsignedLong(a[ai],16));Data d=li.getDataAt(ad); if(d==null)d=li.getDataContaining(ad); if(d==null){w.println(a[ai]+"\tNO_DATA");continue;} int n=d.getNumComponents(); for(int i=0;i<n;i++){Data c=d.getComponent(i); if(c==null)continue; Object v=c.getValue(); Address ta=(v instanceof Address)?(Address)v:null; Function f=ta==null?null:fm.getFunctionAt(ta); w.printf("%s\t%d\t%s\t%s\t%s\t%s\t%s%n",d.getAddress(),i,c.getAddress(),ta==null?"":ta, f==null?"":f.getName(),f==null?"":own(f),f==null?"":cd(f));}}
  w.close();println("DUMP_POINTER_TABLE_TARGETS_PASS"); }
}
