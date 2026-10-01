// Dump every reference to each address in an input file, with the referencing function
// and the referencing instruction. Built because the database repeatedly needs to answer
// "who writes this global?" -- a question the call-graph edge dump cannot answer, since it
// records function->function edges only.
//
// Read/write is distinguished by reference type, so a caller can tell the single writer of
// a global from its many readers. That distinction has already mattered once: a claim that
// "enmity decay scales with the global time base" was retracted after the sole writer turned
// out to run only at shutdown. One writer plus thirty-nine readers is not a dynamic value.
//
// args: <out.tsv> <addresses.txt>
//@category GFZ
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.symbol.RefType;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class DumpDataXrefs extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        if (a.length < 2) { println("DUMP_DATA_XREFS_FAIL need <out.tsv> <addresses.txt>"); return; }

        List<String> targets = new ArrayList<>();
        for (String line : Files.readAllLines(Paths.get(a[1]), StandardCharsets.UTF_8)) {
            // PowerShell's Set-Content -Encoding utf8 emits a BOM, which silently turned
            // the first target into a bad address once. Strip it rather than trusting callers.
            String s = line.replace("﻿", "").trim();
            if (!s.isEmpty() && !s.startsWith("#")) targets.add(s);
        }

        int rows = 0, missed = 0;
        try (PrintWriter w = new PrintWriter(new OutputStreamWriter(
                new FileOutputStream(a[0]), StandardCharsets.UTF_8))) {
            w.println("target\tkind\tfrom\tfrom_func\tfunc_entry\tinstruction");
            for (String t : targets) {
                Address target;
                try { target = toAddr(t); } catch (Exception e) { target = null; }
                if (target == null) { missed++; println("DUMP_DATA_XREFS_BADADDR " + t); continue; }

                ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(target);
                int n = 0;
                while (it.hasNext()) {
                    Reference r = it.next();
                    Address from = r.getFromAddress();
                    RefType rt = r.getReferenceType();
                    // Collapse to the question actually being asked: does this site write it?
                    String kind = rt.isWrite() ? "WRITE" : rt.isRead() ? "READ"
                                : rt.isCall() ? "CALL" : rt.isFlow() ? "FLOW" : rt.getName();
                    Function f = getFunctionContaining(from);
                    Instruction ins = getInstructionAt(from);
                    w.println(String.join("\t",
                        t, kind, from.toString(),
                        f == null ? "-" : f.getName(),
                        f == null ? "-" : f.getEntryPoint().toString(),
                        ins == null ? "-" : ins.toString()));
                    rows++; n++;
                }
                if (n == 0) println("DUMP_DATA_XREFS_NONE " + t);
            }
        }
        println("DUMP_DATA_XREFS_PASS targets=" + targets.size() + " rows=" + rows + " bad=" + missed);
    }
}
