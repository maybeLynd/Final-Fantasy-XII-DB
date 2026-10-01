// @category GFZ
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.*;
import java.io.*; import java.nio.charset.StandardCharsets; import java.nio.file.*; import java.util.*;
public class DecompileAddressFileBounded extends GhidraScript {
 public void run() throws Exception {
  String[] a=getScriptArgs(); if(a.length<2) throw new IllegalArgumentException("output address_file [seconds]");
  int sec=a.length>=3?Integer.parseInt(a[2]):3;
  List<String> addrs=Files.readAllLines(Paths.get(a[1]),StandardCharsets.UTF_8);
  PrintWriter w=new PrintWriter(new OutputStreamWriter(new FileOutputStream(a[0]),StandardCharsets.UTF_8));
  DecompInterface di=new DecompInterface(); di.toggleCCode(true); di.toggleSyntaxTree(true); if(!di.openProgram(currentProgram)) throw new RuntimeException("decomp open failed");
  FunctionManager fm=currentProgram.getFunctionManager(); int ok=0,fail=0,miss=0;
  for(String raw:addrs){String s=raw.trim(); if(s.isEmpty()||s.startsWith("#"))continue; String e=s.split("\\s+")[0];
   long x=Long.parseUnsignedLong(e.replace("0x",""),16); Address ad=currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(x); Function f=fm.getFunctionAt(ad);
   w.println("===== "+e+" "+(f==null?"<no function>":f.getName())+" =====");
   if(f==null){miss++;continue;}
   DecompileResults r=di.decompileFunction(f,sec,monitor); if(r.decompileCompleted()){w.println(r.getDecompiledFunction().getC());ok++;} else {w.println("DECOMP_FAIL "+r.getErrorMessage());fail++;}
   w.flush();
  }
  di.dispose();w.close();println("DECOMPILE_ADDRESS_FILE_BOUNDED_PASS ok="+ok+" fail="+fail+" miss="+miss+" timeout="+sec);
 }
}
