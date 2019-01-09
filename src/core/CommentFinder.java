package core;

import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.LangDataKeys;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class CommentFinder {

    public static List<QualityComment> CommentsInCurrentFile(@NotNull AnActionEvent anActionEvent) {
        PsiFile file = anActionEvent.getDataContext().getData(LangDataKeys.PSI_FILE);
        if (file == null) {
            return Collections.emptyList();
        }

        List<PsiComment> psiComments = new ArrayList<>();
        FindComments(file, psiComments);

        List<QualityComment> comments = new ArrayList<>();
        for (PsiComment psiComment : psiComments) {
            comments.add(new QualityComment(psiComment));
        }

        return comments;
    }

    private static void FindComments(@NotNull PsiElement element, @NotNull List<PsiComment> comments) {
        if (element instanceof PsiComment) {
            comments.add((PsiComment) element);
        }
        for (PsiElement child : element.getChildren()) {
            FindComments(child, comments);
        }
    }
}
