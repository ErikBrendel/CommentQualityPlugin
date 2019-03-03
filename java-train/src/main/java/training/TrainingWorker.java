package training;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.Range;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;
import java.util.List;
import java.util.stream.Collectors;

public class TrainingWorker extends Thread {

    private final TrainingTaskList taskList;
    public boolean running = true;

    public TrainingWorker(TrainingTaskList taskList) {
        this.taskList = taskList;
    }

    @Override
    public void run() {
        while (!taskList.isFinished()) {
            try {
                TrainingTaskList.Task nextTask = taskList.next();
                if (nextTask == null) {
                    try {
                        Thread.sleep(10);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                } else {
                    try {
                        extractComments(nextTask);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    taskList.done();
                }
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
        running = false;
    }


    private static void extractComments(TrainingTaskList.Task task) {
        String filename = task.filename;
        File rootDirectory = task.rootDirectory;

        try {
            ParseResult<CompilationUnit> parsed = new JavaParser().parse(new File(rootDirectory, filename));
            parsed.ifSuccessful(cu -> {

                String repoName = rootDirectory.getName();
                CsvWriter export = new CsvWriter(new File(rootDirectory, "../__commentMetrics/" + repoName + "/" + filename + ".csv"));
                export.writeCell("commented").writeCell("modifiers").writeCell("parameterAmount").writeCell("loc")
                        .writeCell("comment").writeCell("code")
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
                        writer.writeCell(comment).writeCell(code).endLine();
                    }
                };
                cu.accept(visitor, export);
                export.close();
                if (export.getRowsWritten() < 2) {
                    export.abort();
                }
            });
        } catch (Exception ex) {
            throw new RuntimeException(ex);
        }
    }

}
