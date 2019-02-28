package plugin;

import com.intellij.codeInspection.LocalInspectionTool;
import com.intellij.codeInspection.ProblemHighlightType;
import com.intellij.codeInspection.ProblemsHolder;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import core.CommentQualityAnalysisResult;
import core.QualityComment;
import core.Utils;
import org.jetbrains.annotations.NotNull;
import training.CsvWriter;
import training.ExternalProgram;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

/**
 * Code Inspection that adds a warning to comments that get classified as bad
 *
 * see
 * https://www.jetbrains.com/help/idea/code-inspection.html
 * http://www.jetbrains.org/intellij/sdk/docs/tutorials/code_inspections.html
 * http://www.jetbrains.org/intellij/sdk/docs/reference_guide/custom_language_support/code_inspections_and_intentions.html
 * https://upsource.jetbrains.com/idea-ce/file/idea-ce-a7b3d4e9e48efbd4ac75105e9737cea25324f11e/platform/analysis-api/src/com/intellij/codeInspection/LocalInspectionTool.java
 * https://upsource.jetbrains.com/idea-ce/file/idea-ce-a7b3d4e9e48efbd4ac75105e9737cea25324f11e/platform/analysis-api/src/com/intellij/codeInspection/ProblemsHolder.java?nav=stub:21:focused
 */
public class BadCommentsInspection extends LocalInspectionTool {

    @Override
    @NotNull
    public String getDisplayName() {
        return "Comment seems not be be fitting to describe its code.";
    }

    @NotNull
    public String getGroupDisplayName() {
        return "Comment Quality";
    }

    @NotNull
    public String getShortName() {
        return "BadComments";
    }

    @NotNull
    @Override
    public PsiElementVisitor buildVisitor(@NotNull final ProblemsHolder holder, boolean isOnTheFly) {
        return new PsiElementVisitor() {
            @Override
            public void visitElement(PsiElement element) {
                super.visitElement(element);
                if (!(element instanceof PsiComment)) return;

                PsiComment comment = (PsiComment) element;
                if (isPartOfComment(comment)) return;

                QualityComment qualityComment = new QualityComment(includingOtherParts(comment));
                if (qualityComment.position != QualityComment.Position.BeforeMethod) return;

                CommentQualityAnalysisResult result = analyzeQualityOf(qualityComment);
                holder.registerProblem(element, result.fullMessage(), ProblemHighlightType.WEAK_WARNING);
            }

            private boolean isPartOfComment(PsiComment comment) {
                // if a single-line comment is directly under another one, they are one
                PsiElement prev = Utils.previousNonWhitespaceElement(comment);
                if (!(prev instanceof PsiComment)) return false;

                return Utils.lineNumberOf(prev) == Utils.lineNumberOf(comment) - 1;
            }

            private PsiComment[] includingOtherParts(PsiComment mainComment) {
                // if a single-line comment is directly under another one, they are one
                List<PsiComment> comments = new ArrayList<>();
                PsiElement current = mainComment;
                int currentLine = Utils.lineNumberOf(mainComment);
                while (current instanceof PsiComment && Utils.lineNumberOf(current) == currentLine) {
                    comments.add((PsiComment) current);
                    current = Utils.nextNonWhitespaceElement(current);
                    currentLine++;
                }
                return comments.toArray(new PsiComment[0]);
            }
        };
    }

    private static final ExternalProgram PythonProgram = new ExternalProgram(new File("/home/erik/projects/CommentQualityPlugin/python"));

    @NotNull
    private CommentQualityAnalysisResult analyzeQualityOf(QualityComment comment) {
        List<String> classification = PythonProgram.runArgs(
                "venv/bin/python3",
                "classify.py",
                comment.fullCommentText(),
                comment.relatedCodeText(),
                CsvWriter.stringifyList(comment.commentWordList()),
                CsvWriter.stringifyList(comment.relatedCodeWordList())
        );

        CommentQualityAnalysisResult.Result result = CommentQualityAnalysisResult.Result.valueOf(classification.remove(0));

        String msg = String.join("\n", classification).trim();
        if (msg.isEmpty()) msg = null;

        return new CommentQualityAnalysisResult(result, msg);
    }
}
