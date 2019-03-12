package training;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.Range;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.stmt.IfStmt;

import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.comments.BlockComment;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.comments.LineComment;
import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

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
                        extractLineComments(nextTask);
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
                CsvWriter export = new CsvWriter(new File(rootDirectory, "../__commentMetrics/" + repoName + "/" + filename + ".csv"));
                export.writeCell("commented").writeCell("loc").writeCell("condition").writeCell("conditionChildren")
                        .writeCell("comment").writeCell("code")
                        .endLine();

                VoidVisitor<CsvWriter> visitor = new VoidVisitorAdapter<CsvWriter>() {
                    @Override
                    public void visit(final IfStmt ifElseStmt, final CsvWriter writer) {
                        super.visit(ifElseStmt, writer);
                        boolean commented = false;
                        if(ifElseStmt.getComment().isPresent()){
                            commented = true;
                        }
                        int loc = ifElseStmt.getRange().map(Range::getLineCount).orElse(0);
                        String comment = ifElseStmt.getComment().map(Node::toString).orElse("");
                        String code = ifElseStmt.toString();
                        String condition = ifElseStmt.getCondition().toString();
                        int conditionChildren = ifElseStmt.getCondition().getChildNodes().size();
                        writer.writeCell(commented).writeCell(loc).writeCell(condition).writeCell(conditionChildren);
                        writer.writeCell(comment).writeCell(code).endLine();
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
                        .writeCell("comment").writeCell("code").writeCell("commentType")
                        .endLine();

                VoidVisitor<CsvWriter> visitor = new VoidVisitorAdapter<CsvWriter>() {
                    @Override
                    public void visit(final MethodDeclaration method, final CsvWriter writer) {
                        super.visit(method, writer);
                        boolean commented = method.getComment().isPresent();
                        List<String> modifiers = method.getModifiers().stream().map(Node::toString).map(String::trim).collect(Collectors.toList());
                        int parameterAmount = method.getParameters().size();
                        int loc = method.getRange().map(Range::getLineCount).orElse(0);
                        String comment = method.getComment().map(Node::toString).orElse("");
                        String code = method.toString();

                        writer.writeCell(commented).writeCell(modifiers).writeCell(parameterAmount).writeCell(loc);
                        writer.writeCell(comment).writeCell(code).writeCell("method").endLine();
                    }

                    /* Blockcomments are mostly licenses
                    @Override
                    public void visit(final BlockComment comment, final CsvWriter writer) {
                        super.visit(comment, writer);
                        visitComment(comment, writer, "block");
                    }*/


                    @Override
                    public void visit(final LineComment comment, final CsvWriter writer) {
                        super.visit(comment, writer);
                        visitComment(comment, writer, "line");
                    }

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
