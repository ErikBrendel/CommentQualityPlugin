package inspections;

import com.intellij.codeInspection.InspectionsBundle;
import com.intellij.codeInspection.LocalInspectionTool;
import com.intellij.codeInspection.ProblemHighlightType;
import com.intellij.codeInspection.ProblemsHolder;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import core.CommentQualityAnalysisResult;
import core.QualityComment;
import org.jetbrains.annotations.NotNull;

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
                if (element instanceof PsiComment) {
                    CommentQualityAnalysisResult result = new QualityComment((PsiComment) element).analyzeQuality();
                    if (result.isBad()) {
                        holder.registerProblem(element, result.fullMessage(), ProblemHighlightType.WARNING);
                    }
                }
            }
        };
    }
}
