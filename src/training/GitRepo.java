package training;

import com.intellij.lang.*;
import com.intellij.lang.java.JavaParserDefinition;
import com.intellij.lang.java.parser.FileParser;
import com.intellij.lang.java.parser.JavaParser;
import com.intellij.lang.java.parser.JavaParserUtil;
import com.intellij.lexer.Lexer;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.project.ProjectManager;
import com.intellij.pom.java.LanguageLevel;
import com.intellij.psi.*;
import com.intellij.psi.impl.PsiParserFacadeImpl;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.IFileElementType;
import com.intellij.psi.tree.TokenSet;
import com.intellij.psi.util.PsiUtil;
import core.QualityComment;
import org.jetbrains.annotations.NotNull;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static com.intellij.lang.java.parser.JavaParserUtil.setLanguageLevel;

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

        File root = rootDirectory();
        for (String filename : filesFound) {
            if ("".equals(filename)) continue;
            System.out.println(filename);
            try {
                //todo: extract psi of that file, find comments, classify them
                // https://intellij-support.jetbrains.com/hc/en-us/community/posts/360003230920-Retrieve-PSI-tree-of-external-file
                File file = new File(root, filename.trim().substring(2));
                String fileContent = String.join("\n", Files.readAllLines(file.toPath()));

                ParserDefinition def = new JavaParserDefinition();
                LanguageLevel level = LanguageLevel.HIGHEST;
                Lexer lexer = JavaParserDefinition.createLexer(level);
                PsiBuilderFactory factory = PsiBuilderFactory.getInstance();
                PsiBuilder builder = factory.createBuilder(def, lexer, fileContent);
                JavaParserUtil.setLanguageLevel(builder, level);
                FileParser fileParser = JavaParser.INSTANCE.getFileParser();
                fileParser.parse(builder);

                //todo: and add the comments and classifications to the result list
                parsedFiles++;
            } catch (NoSuchFileException e) {
                System.err.println("Cannot find file, skipping...");
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
