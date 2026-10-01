// @category GFZ
// GFZNonFunctionAnnotationSnapshotV1 -- deterministic export of NON-function annotation
// state: symbols, address comments, equates, the DTM inventory, applied data types and
// reference overrides. Complement to GFZFunctionAnnotationSnapshotV2 (function records).
// Text format, one record per line, each section sorted -- built for content diffing
// across parent GZFs.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.data.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class GFZNonFunctionAnnotationSnapshotV1 extends GhidraScript {

    static String esc(String s) {
        if (s == null) return "";
        StringBuilder b = new StringBuilder(s.length() + 8);
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '\\': b.append("\\\\"); break;
                case '\n': b.append("\\n"); break;
                case '\r': b.append("\\r"); break;
                case '\t': b.append("\\t"); break;
                default:   b.append(c);
            }
        }
        return b.toString();
    }

    public void run() throws Exception {
        String[] a = getScriptArgs();
        if (a.length != 1) throw new IllegalArgumentException("output path required");
        Program prog = currentProgram;
        Listing listing = prog.getListing();
        SymbolTable st = prog.getSymbolTable();

        // Function entry points, for flagging which symbols sit on defined functions.
        Set<Long> funcEntries = new HashSet<>();
        FunctionIterator fit = prog.getFunctionManager().getFunctions(true);
        while (fit.hasNext()) funcEntries.add(fit.next().getEntryPoint().getOffset());

        // ---- SYMBOL: every symbol, flagged by whether its address is a function entry.
        List<String> symbols = new ArrayList<>();
        SymbolIterator sit = st.getSymbolIterator();
        while (sit.hasNext()) {
            Symbol s = sit.next();
            Namespace ns = s.getParentNamespace();
            symbols.add(
                s.getAddress().toString() + '\t' +
                s.getSymbolType().toString() + '\t' +
                esc(s.getName()) + '\t' +
                esc(ns == null ? "" : ns.getName(true)) + '\t' +
                s.getSource().toString() + '\t' +
                (s.isPrimary() ? '1' : '0') + '\t' +
                (s.isPinned() ? '1' : '0') + '\t' +
                (funcEntries.contains(s.getAddress().getOffset()) ? '1' : '0'));
        }
        symbols.sort(null);

        // ---- COMMENT: every comment-bearing address, all five comment types.
        CommentType[] ctypes = {
            CommentType.PLATE, CommentType.PRE, CommentType.EOL,
            CommentType.REPEATABLE, CommentType.POST
        };
        List<String> comments = new ArrayList<>();
        for (CommentType ct : ctypes) {
            AddressIterator ait = listing.getCommentAddressIterator(ct, prog.getMemory(), true);
            while (ait.hasNext()) {
                Address ad = ait.next();
                String c = listing.getComment(ct, ad);
                if (c != null)
                    comments.add(ad.toString() + '\t' + ct.toString() + '\t' +
                        (funcEntries.contains(ad.getOffset()) ? '1' : '0') + '\t' + esc(c));
            }
        }
        comments.sort(null);

        // ---- EQUATE: name, value, category path.
        List<String> equates = new ArrayList<>();
        EquateTable et = prog.getEquateTable();
        Iterator<Equate> eit = et.getEquates();
        while (eit.hasNext()) {
            Equate e = eit.next();
            equates.add(esc(e.getName()) + '\t' + e.getValue() + '\t' +
                e.getReferenceCount());
        }
        equates.sort(null);

        // ---- DATATYPE: full DTM inventory (category path, name, size, description).
        List<String> dtypes = new ArrayList<>();
        Iterator<DataType> dit = prog.getDataTypeManager().getAllDataTypes();
        while (dit.hasNext()) {
            DataType dt = dit.next();
            CategoryPath cp = dt.getCategoryPath();
            dtypes.add(
                esc(cp == null ? "" : cp.getPath()) + '\t' +
                esc(dt.getName()) + '\t' +
                dt.getLength() + '\t' +
                esc(dt.getDescription()));
        }
        dtypes.sort(null);

        // ---- DATA: applied data type at every defined data unit.
        List<String> applied = new ArrayList<>();
        DataIterator diter = listing.getDefinedData(true);
        while (diter.hasNext()) {
            Data d = diter.next();
            DataType dt = d.getDataType();
            applied.add(
                d.getMinAddress().toString() + '\t' +
                esc(dt == null ? "" : dt.getName()) + '\t' +
                d.getLength());
        }
        applied.sort(null);

        // ---- REF-OVERRIDE: every reference carrying an overridden ref type.
        List<String> orefs = new ArrayList<>();
        ReferenceManager rm = prog.getReferenceManager();
        ReferenceIterator rit = rm.getReferenceIterator(prog.getMinAddress());
        while (rit.hasNext()) {
            Reference r = rit.next();
            RefType rt = r.getReferenceType();
            if (rt != null && rt.isOverride()) {
                orefs.add(
                    r.getFromAddress().toString() + '\t' +
                    r.getOperandIndex() + '\t' +
                    r.getToAddress().toString() + '\t' +
                    rt.toString());
            }
        }
        orefs.sort(null);

        try (BufferedWriter w = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(a[0]), StandardCharsets.UTF_8))) {
            w.write("GFZ-NONFUNC-ANN1\n");
            w.write("program\t" + esc(prog.getName()) + '\n');
            w.write("imagebase\t" + prog.getImageBase().toString() + '\n');
            w.write("function_count\t" + funcEntries.size() + '\n');
            w.write("[SYMBOL]\tcount=" + symbols.size() + '\n');
            for (String s : symbols) w.write(s + '\n');
            w.write("[COMMENT]\tcount=" + comments.size() + '\n');
            for (String s : comments) w.write(s + '\n');
            w.write("[EQUATE]\tcount=" + equates.size() + '\n');
            for (String s : equates) w.write(s + '\n');
            w.write("[DATATYPE]\tcount=" + dtypes.size() + '\n');
            for (String s : dtypes) w.write(s + '\n');
            w.write("[DATA]\tcount=" + applied.size() + '\n');
            for (String s : applied) w.write(s + '\n');
            w.write("[REF-OVERRIDE]\tcount=" + orefs.size() + '\n');
            for (String s : orefs) w.write(s + '\n');
        }
        println("GFZ_NONFUNC_ANNOTATION_SNAPSHOT_V1_WRITTEN" +
            " symbols=" + symbols.size() +
            " comments=" + comments.size() +
            " equates=" + equates.size() +
            " datatypes=" + dtypes.size() +
            " data=" + applied.size() +
            " overrides=" + orefs.size() +
            " path=" + a[0]);
    }
}
