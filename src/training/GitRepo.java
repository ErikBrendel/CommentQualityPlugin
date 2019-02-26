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
        String foundFiles = ExternalProgram.runArgs("find", ".", "-name", "*.java");
        String[] filesFound = foundFiles.split("\n");


        String print_start = "[" + (repoIndex + 1) + "/" + totalRepos + "] ";
        int fileIndex = 0;
        float totalFiles = filesFound.length;
        for (String filename : filesFound) {
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
        PsiFile file = parsePsi(filename);

        CsvWriter export = new CsvWriter(new File(rootDirectory(), "commentMetrics/" + filename + ".csv"));
        export.writeCell("# identity").writeCell("comment").writeCell("code").endLine();

        for (QualityComment comment : CommentFinder.findComments(file)) {
            if (comment.position == QualityComment.Position.BeforeMethod) {
                export
                        .writeCell(comment.relatedCodeIdentity())
                        .writeCell(comment.commentWordList())
                        .writeCell(comment.relatedCodeWordList())
                        .endLine();
            }
        }

        export.close();

        //todo: and add the comments and classifications to the result list
    }

    private PsiFile parsePsi(String localFilePath) {
        // https://intellij-support.jetbrains.com/hc/en-us/community/posts/360003230920-Retrieve-PSI-tree-of-external-file
        File file = new File(rootDirectory(), localFilePath);
        VirtualFile vFile = LocalFileSystem.getInstance().findFileByIoFile(file);
        if (vFile == null) throw new RuntimeException("Cannot find virtual file, skipping...");

        Project proj = ProjectManager.getInstance().getOpenProjects()[0];
        PsiFile psiFile = PsiManager.getInstance(proj).findFile(vFile);
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
