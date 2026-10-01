// @category GFZ
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;import ghidra.program.model.listing.*;import ghidra.program.model.symbol.*;import java.io.*;import java.nio.charset.StandardCharsets;import java.util.*;
public class DumpUnresolvedIncomingOwnerRefs extends GhidraScript {
 static String owner(Function f){if(f==null)return "";for(FunctionTag t:f.getTags())if(t.getName().startsWith("GFZ.V120.PrimaryOwner."))return t.getName().substring("GFZ.V120.PrimaryOwner.".length());return "";}
 static boolean finalNo(Function f){for(FunctionTag t:f.getTags())if(t.getName().equals("GFZ.V120.FinalNoPrimaryOwner"))return true;return false;}
 static boolean codeDom(Function f){for(FunctionTag t:f.getTags())if(t.getName().startsWith("GFZ.V121.CodeDomain."))return true;return false;}
 static boolean unresolved(Function f){return !f.isExternal() && owner(f).isEmpty() && !finalNo(f) && !codeDom(f);}
 public void run() throws Exception {String[] a=getScriptArgs();if(a.length!=1)throw new IllegalArgumentException("out"); FunctionManager fm=currentProgram.getFunctionManager();ReferenceManager rm=currentProgram.getReferenceManager();ArrayList<String> out=new ArrayList<>();int funcs=0,refs=0;FunctionIterator it=fm.getFunctions(true);while(it.hasNext()){Function f=it.next();if(!unresolved(f))continue;TreeMap<String,Integer> data=new TreeMap<>(),other=new TreeMap<>();ReferenceIterator ri=rm.getReferencesTo(f.getEntryPoint());while(ri.hasNext()){Reference r=ri.next();Function src=fm.getFunctionContaining(r.getFromAddress());String o=owner(src);if(o.isEmpty())continue;TreeMap<String,Integer> m=r.getReferenceType().isData()?data:other;m.put(o,m.getOrDefault(o,0)+1);refs++;}if(!data.isEmpty()||!other.isEmpty()){funcs++;out.add(String.format("%08X\t%d\t%s\t%s",f.getEntryPoint().getOffset(),f.getBody().getNumAddresses(),fmt(data),fmt(other)));}}
 try(PrintWriter w=new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]),StandardCharsets.UTF_8))){w.println("entry\tbody_bytes\tincoming_data_owner_refs\tincoming_other_owner_refs");for(String s:out)w.println(s);}println("UNRESOLVED_INCOMING_OWNER_REFS functions="+funcs+" refs="+refs);}
 static String fmt(TreeMap<String,Integer> m){ArrayList<String>a=new ArrayList<>();for(Map.Entry<String,Integer>e:m.entrySet())a.add(e.getKey()+":"+e.getValue());return String.join(";",a);}
}
