package training;

import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.project.ProjectManager;
import com.intellij.openapi.util.Computable;
import com.intellij.openapi.vfs.LocalFileSystem;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.PsiFile;
import com.intellij.psi.PsiManager;
import core.CommentFinder;
import core.QualityComment;

import java.io.File;
import java.util.*;

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

    private static class CommentOccurrence {
        public final QualityComment comment;
        public final int timestamp;

        private CommentOccurrence(QualityComment comment, int timestamp) {
            this.comment = comment;
            this.timestamp = timestamp;
        }
    }

    private static void extractComments(TrainingTaskList.Task task) {
        String filename = task.filename;
        File rootDirectory = task.rootDirectory;
        ExternalProgram program = new ExternalProgram(rootDirectory);
        List<String> versionsAndDates = program.runArgs("git", "log", "--format=%H %ct", "--reverse", "--first-parent", filename);

        if (versionsAndDates.size() <= 2) return;

        Map<String, List<CommentOccurrence>> foundComments = new HashMap<>();

        for (String versionAndDate : versionsAndDates) {
            String[] versionAndDateData = versionAndDate.split(" ");
            String version = versionAndDateData[0];
            int timestamp = Integer.parseInt(versionAndDateData[1]);
            String fileContent = program.runArgsJoined("git", "show", version + ":" + filename);
            VirtualFile vFile = new OtherContentFileDecorator(new File(rootDirectory, filename), fileContent);

            List<QualityComment> comments = ApplicationManager.getApplication().runReadAction(
                    (Computable<List<QualityComment>>) () -> CommentFinder.findComments(parsePsi(vFile)));

            for (QualityComment comment : comments) {
                if (comment.position == QualityComment.Position.BeforeMethod) {
                    String id = comment.relatedCodeIdentity();
                    if (!foundComments.containsKey(id)) {
                        foundComments.put(id, new ArrayList<>());
                    }
                    List<CommentOccurrence> occurrences = foundComments.get(id);

                    occurrences.add(new CommentOccurrence(comment, timestamp));
                }
            }
        }

        if (foundComments.isEmpty()) return;

        List<String> foundIDs = new ArrayList<>(foundComments.keySet());
        for (String id : foundIDs) {
            if (foundComments.get(id).size() < 2) {
                foundComments.remove(id);
            }
        }

        if (foundComments.isEmpty()) return;

        String repoName = rootDirectory.getName();
        CsvWriter export = new CsvWriter(new File(rootDirectory, "../__commentMetrics/" + repoName + "/" + filename + ".csv"));

        export.writeCell("# id").writeCell("timestamp")
                .writeCell("commentText").writeCell("codeText")
                .writeCell("commentWords").writeCell("codeWords")
                .endLine();

        for (Map.Entry<String, List<CommentOccurrence>> commentEntry : foundComments.entrySet()) {
            String id = commentEntry.getKey();
            List<CommentOccurrence> occurrences = commentEntry.getValue();
            occurrences.sort(Comparator.comparing(o -> o.timestamp));
            for (CommentOccurrence occurrence : occurrences) {
                QualityComment comment = occurrence.comment;

                export.writeCell(id).writeCell(occurrence.timestamp)
                        .writeCell(comment.commentText()).writeCell(comment.relatedCodeText())
                        .writeCell(comment.commentWordList()).writeCell(comment.relatedCodeWordList())
                        .endLine();
            }
        }

        export.close();
    }

    private PsiFile parsePsi(File rootDirectory, String localFilePath) {
        // https://intellij-support.jetbrains.com/hc/en-us/community/posts/360003230920-Retrieve-PSI-tree-of-external-file
        File file = new File(rootDirectory, localFilePath);
        VirtualFile vFile = LocalFileSystem.getInstance().findFileByIoFile(file);
        if (vFile == null) throw new RuntimeException("Cannot find virtual rootDirectory, skipping...");

        return parsePsi(vFile);
    }

    private static PsiFile parsePsi(VirtualFile file) {
        Project proj = ProjectManager.getInstance().getOpenProjects()[0];
        PsiFile psiFile = PsiManager.getInstance(proj).findFile(file);
        if (psiFile == null) throw new RuntimeException("Cannot find psi rootDirectory rootDirectory, skipping...");

        return psiFile;
    }
}
