package training;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.Range;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.stmt.*;

import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.comments.BlockComment;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.comments.LineComment;
import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import javassist.compiler.ast.Stmnt;

import java.io.File;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

public class TrainingWorker extends Thread {

    private final TrainingTaskList taskList;
    public boolean running = true;

    public TrainingWorker(TrainingTaskList taskList) {
        this.taskList = taskList;
    }

    @Override
    public void run() {
        while(!taskList.isFinished()){
            try{
                TrainingTaskList.Task nextTask = taskList.next();
                if(nextTask == null){
                    try{
                        Thread.sleep(10);
                    } catch(InterruptedException e){
                        e.printStackTrace();
                    }
                } else{
                    try{
                        extractComments(nextTask);
                    } catch(Exception e){
                        e.printStackTrace();
                    }
                    taskList.done();
                }
            } catch(Exception ex){
                ex.printStackTrace();
            }
        }
        running = false;
    }


    private static void extractLineComments(TrainingTaskList.Task task) {
        String filename = task.filename;
        File rootDirectory = task.rootDirectory;

        try{
            ParseResult<CompilationUnit> parsed = new JavaParser().parse(new File(rootDirectory, filename));
            parsed.ifSuccessful(cu -> {

                String repoName = rootDirectory.getName();
                CsvWriter export = new CsvWriter(new File(rootDirectory, "../__commentLineMetrics/" + repoName + "/" + filename + ".csv"));
                export.writeCell("commented").writeCell("loc").writeCell("comment").writeCell("code").writeCell("containedComments")
                        .writeCell("condition").writeCell("conditionChildren").writeCell("condition_length").writeCell("type")
                        .endLine();

                VoidVisitor<CsvWriter> visitor = new VoidVisitorAdapter<CsvWriter>() {

                    private void writeBasics(final Statement stmt, final CsvWriter writer){
                        boolean commented = false;
                        if(stmt.getComment().isPresent()){
                            commented = true;
                        }
                        int loc = stmt.getRange().map(Range::getLineCount).orElse(0);
                        String comment = stmt.getComment().map(Node::toString).orElse("");
                        String code = stmt.toString();
                        int containedComments = stmt.getAllContainedComments().size();
                        writer.writeCell(commented).writeCell(loc).writeCell(comment).writeCell(code).writeCell(containedComments);
                    }

                    @Override
                    public void visit(final IfStmt ifElseStmt, final CsvWriter writer) {
                        super.visit(ifElseStmt, writer);
                        this.writeBasics(ifElseStmt, writer);
                        String condition = ifElseStmt.getCondition().toString();
                        // Todo: some sort of how many blocks follow would be good
                        int conditionChildren = ifElseStmt.getCondition().getChildNodes().size();
                        writer.writeCell(condition).writeCell(conditionChildren).writeCell(condition.length()).writeCell("if").endLine();
                    }

                    @Override
                    public void visit(final TryStmt tryStmt, final CsvWriter writer) {
                        super.visit(tryStmt, writer);
                        this.writeBasics(tryStmt, writer);
                        String condition = "";
                        int conditionChildren = 0;
                        writer.writeCell(condition).writeCell(conditionChildren).writeCell(condition.length()).writeCell("try").endLine();
                    }

                    @Override
                    public void visit(final ForStmt forStmt, final CsvWriter writer) {
                        super.visit(forStmt, writer);
                        this.writeBasics(forStmt, writer);
                        String condition =  forStmt.getCompare().toString();
                        int conditionChildren = 0;
                        writer.writeCell(condition).writeCell(conditionChildren).writeCell(condition.length()).writeCell("for").endLine();
                    }

                    @Override
                    public void visit(final WhileStmt whileStmt, final CsvWriter writer) {
                        super.visit(whileStmt, writer);
                        this.writeBasics(whileStmt, writer);
                        String condition =  whileStmt.getCondition().toString();
                        int conditionChildren = whileStmt.getCondition().getChildNodes().size();
                        writer.writeCell(condition).writeCell(conditionChildren).writeCell(condition.length()).writeCell("while").endLine();
                    }

                    @Override
                    public void visit(final SwitchStmt switchStmt, final CsvWriter writer) {
                        super.visit(switchStmt, writer);
                        this.writeBasics(switchStmt, writer);
                        String condition = "";
                        int conditionChildren = 0;
                        writer.writeCell(condition).writeCell(conditionChildren).writeCell(condition.length()).writeCell("switch").endLine();
                    }

                    @Override
                    public void visit(final SynchronizedStmt synchronizedStmt, final CsvWriter writer) {
                        super.visit(synchronizedStmt, writer);
                        this.writeBasics(synchronizedStmt, writer);
                        String condition = synchronizedStmt.getExpression().toString();
                        int conditionChildren = synchronizedStmt.getExpression().getChildNodes().size();
                        writer.writeCell(condition).writeCell(conditionChildren).writeCell(condition.length()).writeCell("sync").endLine();
                    }



                };
                cu.accept(visitor, export);
                export.close();
                if(export.getRowsWritten() < 2){
                    export.abort();
                }
            });
        } catch(Exception ex){
            throw new RuntimeException(ex);
        }
    }


    private static void extractComments(TrainingTaskList.Task task) {
        String filename = task.filename;
        File rootDirectory = task.rootDirectory;

        try{
            ParseResult<CompilationUnit> parsed = new JavaParser().parse(new File(rootDirectory, filename));
            parsed.ifSuccessful(cu -> {

                String repoName = rootDirectory.getName();
                CsvWriter export = new CsvWriter(new File(rootDirectory, "../__commentMetrics/" + repoName + "/" + filename + ".csv"));
                export.writeCell("commented").writeCell("modifiers").writeCell("parameterAmount").writeCell("loc")
                        .writeCell("declaration").writeCell("comment").writeCell("code").writeCell("commentType")
                        .writeCell("annotations").writeCell("annotationNames").writeCell("methodName").writeCell("methodNameLength")
                        .writeCell("methodNameWordCount").writeCell("nrInlineComments").endLine();

                VoidVisitor<CsvWriter> visitor = new VoidVisitorAdapter<CsvWriter>() {
                    @Override
                    public void visit(final MethodDeclaration method, final CsvWriter writer) {
                        super.visit(method, writer);
                        boolean commented = method.getComment().isPresent();
                        List<String> modifiers = method.getModifiers().stream().map(Node::toString).map(String::trim).collect(Collectors.toList());
                        int parameterAmount = method.getParameters().size();
                        int loc = method.getRange().map(Range::getLineCount).orElse(0);
                        String comment = method.getComment().map(Node::toString).orElse("");
                        String code = method.toString().replace(comment, "");
                        String declaration = method.getDeclarationAsString();
                        String annotations = method.getAnnotations().toString();
                        List<String> annotationNames = method.getAnnotations().stream().map(n -> n.getName().toString()).sorted(String::compareTo).collect(Collectors.toList());
                        String methodName = method.getNameAsString();
                        int nrInlineComments = method.getAllContainedComments().size();
                        writer.writeCell(commented).writeCell(modifiers).writeCell(parameterAmount)
                                .writeCell(loc - nrInlineComments)
                                .writeCell(declaration).writeCell(comment).writeCell(code).writeCell("method")
                                .writeCell(annotations).writeCell(annotationNames).writeCell(methodName).writeCell(methodName.length())
                                .writeCell(methodName.split("(?<=[a-z])(?=[A-Z])").length)
                                .writeCell(nrInlineComments).endLine();
                    }

                    /* Blockcomments are mostly licenses
                    @Override
                    public void visit(final BlockComment comment, final CsvWriter writer) {
                        super.visit(comment, writer);
                        visitComment(comment, writer, "block");
                    }*/


                   /* @Override
                    public void visit(final LineComment comment, final CsvWriter writer) {
                        super.visit(comment, writer);
                        visitComment(comment, writer, "line");
                    }*/

                    private void visitComment(Comment comment, CsvWriter writer, String type) {
                        boolean commented = true;
                        List<String> modifiers = Collections.emptyList();
                        int parameterAmount = 0;
                        String commentStr = comment.getContent();

                        int loc = 0;
                        String code = "";
                        Optional<Node> relatedCode = comment.getCommentedNode();
                        if(relatedCode.isPresent()){
                            loc = relatedCode.get().getRange().map(Range::getLineCount).orElse(0);
                            code = relatedCode.get().toString();
                        }

                        writer.writeCell(commented).writeCell(modifiers).writeCell(parameterAmount).writeCell(loc);
                        writer.writeCell(commentStr).writeCell(code).writeCell(type).endLine();
                    }
                };
                cu.accept(visitor, export);
                export.close();
                if(export.getRowsWritten() < 2){
                    export.abort();
                }
            });
        } catch(Exception ex){
            throw new RuntimeException(ex);
        }
    }

}
