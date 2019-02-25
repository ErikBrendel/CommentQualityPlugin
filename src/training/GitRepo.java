package training;

import com.intellij.openapi.project.Project;
import com.intellij.openapi.project.ProjectManager;
import com.intellij.openapi.vfs.LocalFileSystem;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiFile;
import com.intellij.psi.PsiManager;
import core.CommentFinder;
import core.QualityComment;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class GitRepo {

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
            ExternalProgram.run("git pull");
        }
    }

    public List<QualityComment> allComments() {
        String foundFiles = ExternalProgram.runArgs("find", ".", "-name", "*.java");
        String[] filesFound = foundFiles.split("\n");

        List<QualityComment> result = new ArrayList<>();

        int parsedFiles = 0;

        Project proj = ProjectManager.getInstance().getOpenProjects()[0];
        File root = rootDirectory();
        for (String filename : filesFound) {
            if ("".equals(filename)) continue;
            System.out.println(filename);
            try {
                // https://intellij-support.jetbrains.com/hc/en-us/community/posts/360003230920-Retrieve-PSI-tree-of-external-file
                File file = new File(root, filename.trim().substring(2));
                VirtualFile vFile = LocalFileSystem.getInstance().findFileByIoFile(file);

                if (vFile == null) {
                    System.err.println("Cannot find virtual file, skipping...");
                    continue;
                }
                PsiFile psiFile = PsiManager.getInstance(proj).findFile(vFile);

                if (psiFile == null) {
                    System.err.println("Cannot find psi file file, skipping...");
                    continue;
                }
                List<PsiComment> psiComments = CommentFinder.findComments(psiFile);
                System.out.println(psiComments.size());

                //todo: and add the comments and classifications to the result list
                parsedFiles++;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        System.out.println("Parsing results: parsed " + parsedFiles + " of " + filesFound.length + " files.");

        return result;
    }

    private void cloneRepo() {
        File root = rootDirectory();
        FileUitls.mkdirs(root);
        String gitUrl = TrainingMain.REPO_URL_START + name + TrainingMain.REPO_URL_END;
        ExternalProgram.runArgs("git", "clone", gitUrl, root.getAbsolutePath());
    }

    private File rootDirectory() {
        return new File(TrainingMain.REPO_CLONE_PATH + name.replaceAll("/", "-") + "/");
    }

    private boolean isCloned() {
        File root = rootDirectory();
        return root.exists() && root.isDirectory();
    }
}
