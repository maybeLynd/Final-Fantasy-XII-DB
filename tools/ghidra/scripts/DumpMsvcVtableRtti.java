// @category GFZ
import ghidra.app.script.GhidraScript; import ghidra.program.model.address.*; import ghidra.program.model.mem.*; import java.io.*; import java.nio.charset.StandardCharsets;
public class DumpMsvcVtableRtti extends GhidraScript {
 long uq(Address a)throws Exception{return currentProgram.getMemory().getLong(a);}
 int ui(Address a)throws Exception{return currentProgram.getMemory().getInt(a);}
 String cstr(Address a)throws Exception{StringBuilder s=new StringBuilder();Memory m=currentProgram.getMemory();for(int i=0;i<512;i++){byte b=m.getByte(a.add(i));if(b==0)break;s.append((char)(b&255));}return s.toString();}
 public void run()throws Exception{String[] z=getScriptArgs();if(z.length<2)throw new IllegalArgumentException("out vftable..."); PrintWriter w=new PrintWriter(new OutputStreamWriter(new FileOutputStream(z[0]),StandardCharsets.UTF_8)); Address image=currentProgram.getImageBase(); w.println("vftable\tcol_ptr\tsig\toffset\tcdOffset\ttype_rva\ttype_addr\ttype_name\tclass_rva\tself_rva");
  for(int i=1;i<z.length;i++){try{Address vt=toAddr(Long.parseUnsignedLong(z[i],16));long colv=uq(vt.subtract(8));Address col=toAddr(colv);int sig=ui(col),off=ui(col.add(4)),cd=ui(col.add(8)),tr=ui(col.add(12)),cr=ui(col.add(16)),sr=ui(col.add(20));Address ta=image.add(Integer.toUnsignedLong(tr));String name=cstr(ta.add(16));w.printf("%s\t%s\t%d\t%d\t%d\t%08X\t%s\t%s\t%08X\t%08X%n",vt,col,sig,off,cd,tr,ta,name,cr,sr);}catch(Exception e){w.println(z[i]+"\tERROR\t"+e.toString());}}
  w.close();println("DUMP_MSVC_VTABLE_RTTI_PASS");}
}
