package core;

import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.LangDataKeys;
import com.intellij.psi.*;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class CommentFinder {

    public static List<QualityComment> commentsInCurrentFile(@NotNull AnActionEvent anActionEvent) {
        PsiFile file = anActionEvent.getDataContext().getData(LangDataKeys.PSI_FILE);
        if (file == null) {
            return Collections.emptyList();
        }

        return findComments(file);
    }

    public static List<QualityComment> findComments(@NotNull PsiElement file) {
        List<PsiComment> psiComments = new ArrayList<>();
        findComments(file, psiComments);

        List<QualityComment> comments = new ArrayList<>();
        for (PsiComment psiComment : psiComments) {
            comments.add(new QualityComment(psiComment));
        }
        return comments;
    }

    private static void findComments(@NotNull PsiElement element, @NotNull List<PsiComment> comments) {
        if (element instanceof PsiComment) {
            comments.add((PsiComment) element);
        } else {
            for (PsiElement child : element.getChildren()) {
                findComments(child, comments);
            }
        }
    }

    public static QualityComment.Position classifyPositionOf(PsiComment comment) {
        PsiElement parent = comment.getParent();
        if (parent instanceof PsiClass) {
            return QualityComment.Position.BeforeClass;
        } else if (parent instanceof PsiMethod) {
            return QualityComment.Position.BeforeMethod;
        } else if (parent instanceof PsiFile && comment == parent.getFirstChild()) {
            return QualityComment.Position.LicenseHeader;
        } else if (Utils.isAtStartOfContainingBlock(comment) || Utils.isInSingleLineCodeBlock(comment)) {
            return QualityComment.Position.InCodeBlock;
        } else if (Utils.isFollowedByCode(comment)) {
            return QualityComment.Position.BeforeCodeBlock;
        }
        return QualityComment.Position.Unknown;
    }
}
