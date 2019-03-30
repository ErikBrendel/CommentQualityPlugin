package training;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.Range;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.stmt.*;
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
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                } else {
                    try {
                        extractComments(nextTask);
                        extractLineComments(nextTask);
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


    private static <T extends Node> T ParentOfType(Node node, Class<T> type) {
        Node current = node;
        while (current != null) {
            if (type.isInstance(current)) {
                return type.cast(current);
            }
            current = current.getParentNode().orElse(null);
        }
        return null;
    }

    private static void extractLineComments(TrainingTaskList.Task task) {
        String filename = task.filename;
        File rootDirectory = task.rootDirectory;

        try {
            ParseResult<CompilationUnit> parsed = new JavaParser().parse(new File(rootDirectory, filename));
            parsed.ifSuccessful(cu -> {

                String repoName = rootDirectory.getName();
                CsvWriter export = new CsvWriter(new File(rootDirectory, "../__commentLineMetrics/" + repoName + "/" + filename + ".csv"));
                export.writeCell("commented").writeCell("loc").writeCell("comment").writeCell("code").writeCell("containedComments")
                        .writeCell("containingMethodHasComment")
                        .writeCell("condition").writeCell("conditionChildren").writeCell("condition_length").writeCell("type")
                        .endLine();

                VoidVisitor<CsvWriter> visitor = new VoidVisitorAdapter<CsvWriter>() {

                    private void writeBasics(final Statement stmt, final CsvWriter writer) {
                        boolean commented = false;
                        if (stmt.getComment().isPresent()) {
                            commented = true;
                        }
                        int loc = stmt.getRange().map(Range::getLineCount).orElse(0);
                        String comment = stmt.getComment().map(Node::toString).orElse("");
                        String code = stmt.toString();
                        int containedComments = stmt.getAllContainedComments().size();
                        boolean containingMethodHasComment = false;
                        MethodDeclaration containingMethod = ParentOfType(stmt, MethodDeclaration.class);
                        if (containingMethod != null) {
                            containingMethodHasComment = containingMethod.getComment().isPresent();
                        }
                        writer.writeCell(commented).writeCell(loc).writeCell(comment).writeCell(code).writeCell(containedComments)
                                .writeCell(containingMethodHasComment);
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
                        String condition = forStmt.getCompare().toString();
                        int conditionChildren = 0;
                        writer.writeCell(condition).writeCell(conditionChildren).writeCell(condition.length()).writeCell("for").endLine();
                    }

                    @Override
                    public void visit(final WhileStmt whileStmt, final CsvWriter writer) {
                        super.visit(whileStmt, writer);
                        this.writeBasics(whileStmt, writer);
                        String condition = whileStmt.getCondition().toString();
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
                if (export.getRowsWritten() < 2) {
                    export.abort();
                }
            });
        } catch (Exception ex) {
            throw new RuntimeException(ex);
        }
    }


    private static void extractComments(TrainingTaskList.Task task) {
        String filename = task.filename;
        File rootDirectory = task.rootDirectory;

        try {
            ParseResult<CompilationUnit> parsed = new JavaParser().parse(new File(rootDirectory, filename));
            parsed.ifSuccessful(cu -> {

                String repoName = rootDirectory.getName();
                CsvWriter export = new CsvWriter(new File(rootDirectory, "../__commentMetrics/" + repoName + "/" + filename + ".csv"));
                export.writeCell("commented").writeCell("modifiers").writeCell("modifierCount")
                        .writeCell("parameterAmount").writeCell("loc")
                        .writeCell("declaration").writeCell("comment").writeCell("code").writeCell("commentType")
                        .writeCell("annotations").writeCell("annotationNames").writeCell("annotationCount")
                        .writeCell("methodName").writeCell("methodNameLength")
                        .writeCell("methodNameWordCount").writeCell("nrInlineComments")
                        .writeCell("modifierVisibility").writeCell("modifierStatic")
                        .writeCell("modifierFinal").writeCell("modifierAbstract")
                        .writeCell("modifierSynchronized")
                        .writeCell("hasBody")
                        .endLine();

                VoidVisitor<CsvWriter> visitor = new VoidVisitorAdapter<CsvWriter>() {
                    @Override
                    public void visit(final MethodDeclaration method, final CsvWriter writer) {
                        super.visit(method, writer);
                        boolean commented = method.getComment().isPresent();
                        List<String> modifiers = method.getModifiers().stream().map(Node::toString).map(String::trim).collect(Collectors.toList());
                        boolean hasBody = method.getBody().isPresent();
                        boolean isInterfaceMethod = !hasBody && !modifiers.contains("abstract");
                        int parameterAmount = method.getParameters().size();
                        int loc = method.getRange().map(Range::getLineCount).orElse(0);
                        String comment = method.getComment().map(Node::toString).orElse("");
                        String code = method.toString().replace(comment, "");
                        String declaration = method.getDeclarationAsString();
                        String annotations = method.getAnnotations().toString();
                        List<String> annotationNames = method.getAnnotations().stream().map(n -> n.getName().toString()).sorted(String::compareTo).collect(Collectors.toList());
                        String methodName = method.getNameAsString();
                        int nrInlineComments = method.getAllContainedComments().size();
                        writer.writeCell(commented).writeCell(modifiers).writeCell(modifiers.size())
                                .writeCell(parameterAmount).writeCell(loc)
                                .writeCell(declaration).writeCell(comment).writeCell(code).writeCell("method")
                                .writeCell(annotations).writeCell(annotationNames).writeCell(annotationNames.size())
                                .writeCell(methodName).writeCell(methodName.length())
                                .writeCell(methodName.split("(?<=[a-z])(?=[A-Z])").length)
                                .writeCell(nrInlineComments)
                                .writeCell(visibilityValue(modifiers, isInterfaceMethod)).writeCell(modifiers.contains("static"))
                                .writeCell(modifiers.contains("final")).writeCell(modifiers.contains("abstract"))
                                .writeCell(modifiers.contains("synchronized"))
                                .writeCell(hasBody)
                                .endLine();
                    }

                    private int visibilityValue(List<String> modifiers, boolean isInterfaceMethod) {
                        if (modifiers.contains("public") || isInterfaceMethod) {
                            return 3;
                        } else if (modifiers.contains("private")) {
                            return 0;
                        } else if (modifiers.contains("protected")) {
                            return 1;
                        }
                        return 2;//package local
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
