package training;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.project.ProjectManager;
import com.intellij.openapi.vfs.LocalFileSystem;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.PsiFile;
import com.intellij.psi.PsiManager;
import core.CommentFinder;
import core.QualityComment;

import java.io.File;
import java.text.DecimalFormat;
import java.util.*;

public class GitRepo {

    private static final DecimalFormat PERCENT_FORMAT = new DecimalFormat("00.0");

    private final String name;

    public GitRepo(String name) {
        this.name = name;
    }

    public void Update() {
        if (!isCloned()) {
            System.out.println("cloning " + name + ", this may take a while...");
            cloneRepo();
        } else {
            System.out.println("updating " + name + "...");
            ExternalProgram.WorkingDirectory = rootDirectory();
            System.out.println(ExternalProgram.run("git pull"));
        }
    }

    public void findAllComments(int repoIndex, int totalRepos) {
        ExternalProgram.WorkingDirectory = rootDirectory();
        List<String> foundFiles = ExternalProgram.runArgs("find", ".", "-name", "*.java");


        String print_start = "[" + (repoIndex + 1) + "/" + totalRepos + "] ";
        int fileIndex = 0;
        float totalFiles = foundFiles.size();
        for (String filename : foundFiles) {
            fileIndex++;
            if ("".equals(filename)) continue;

            if (filename.startsWith("./")) {
                filename = filename.substring(2);
            }

            System.out.println(print_start + PERCENT_FORMAT.format(fileIndex * 100f / totalFiles) + "%  " + filename);
            try {
                allCommentsIn(filename);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    private void allCommentsIn(String filename) {
        List<String> versionsAndDates = ExternalProgram.runArgs("git", "log", "--format=%H %at", "--reverse", filename);

        if (versionsAndDates.size() <= 2) return;

        Map<String, List<CommentOccurrence>> foundComments = new HashMap<>();

        for (String versionAndDate : versionsAndDates) {
            String[] versionAndDateData = versionAndDate.split(" ");
            String version = versionAndDateData[0];
            int timestamp = Integer.parseInt(versionAndDateData[1]);
            String fileContent = ExternalProgram.runArgsJoined("git", "show", version + ":" + filename);
            VirtualFile vFile = new OtherContentFileDecorator(new File(rootDirectory(), filename), fileContent);
            PsiFile file = parsePsi(vFile);

            for (QualityComment comment : CommentFinder.findComments(file)) {
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

        CsvWriter export = new CsvWriter(new File(rootDirectory(), "commentMetrics/" + filename + ".csv"));

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

    private static class CommentOccurrence {
        public final QualityComment comment;
        public final int timestamp;

        private CommentOccurrence(QualityComment comment, int timestamp) {
            this.comment = comment;
            this.timestamp = timestamp;
        }
    }

    private PsiFile parsePsi(String localFilePath) {
        // https://intellij-support.jetbrains.com/hc/en-us/community/posts/360003230920-Retrieve-PSI-tree-of-external-file
        File file = new File(rootDirectory(), localFilePath);
        VirtualFile vFile = LocalFileSystem.getInstance().findFileByIoFile(file);
        if (vFile == null) throw new RuntimeException("Cannot find virtual file, skipping...");

        return parsePsi(vFile);
    }

    private PsiFile parsePsi(VirtualFile file) {
        Project proj = ProjectManager.getInstance().getOpenProjects()[0];
        PsiFile psiFile = PsiManager.getInstance(proj).findFile(file);
        if (psiFile == null) throw new RuntimeException("Cannot find psi file file, skipping...");

        return psiFile;
    }

    private void cloneRepo() {
        File root = rootDirectory();
        FileUtil.mkdirs(root);
        String gitUrl = TrainingMain.REPO_URL_START + name + TrainingMain.REPO_URL_END;
        System.out.println(ExternalProgram.runArgs("git", "clone", gitUrl, root.getAbsolutePath()));
    }

    private File _rootDirectory = null;
    private File rootDirectory() {
        if (_rootDirectory == null) {
            _rootDirectory = new File(TrainingMain.REPO_CLONE_PATH + name.replaceAll("/", "-") + "/");
        }
        return _rootDirectory;
    }

    private boolean isCloned() {
        File root = rootDirectory();
        return root.exists() && root.isDirectory();
    }
}
