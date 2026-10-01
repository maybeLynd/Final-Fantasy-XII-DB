import ghidra.app.script.GhidraScript;
import ghidra.program.database.mem.FileBytes;
import java.io.*;
import java.util.*;

public class ExtractEmbeddedOriginal extends GhidraScript {
  @Override
  protected void run() throws Exception {
    String[] args = getScriptArgs();
    if (args.length != 1) throw new IllegalArgumentException("usage: <output>");
    List<FileBytes> list = currentProgram.getMemory().getAllFileBytes();
    println("FILEBYTES_COUNT="+list.size());
    for (int i=0;i<list.size();i++) {
      FileBytes fb=list.get(i);
      println("FILEBYTES["+i+"] filename="+fb.getFilename()+" offset="+fb.getFileOffset()+" size="+fb.getSize());
    }
    if (list.size()!=1) throw new IllegalStateException("expected exactly one FileBytes record");
    FileBytes fb=list.get(0);
    File out=new File(args[0]);
    try (OutputStream os=new BufferedOutputStream(new FileOutputStream(out))) {
      byte[] buf=new byte[1<<20];
      long off=0, n=fb.getSize();
      while (off<n) {
        int want=(int)Math.min(buf.length,n-off);
        int got=fb.getOriginalBytes(off,buf,0,want);
        if (got<=0) throw new IOException("short FileBytes read at "+off);
        os.write(buf,0,got);
        off += got;
      }
    }
    println("EMBEDDED_ORIGINAL_EXTRACT_PASS path="+out.getAbsolutePath()+" size="+out.length());
  }
}
