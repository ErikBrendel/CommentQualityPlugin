package core;

import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.LangDataKeys;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;

import java.util.ArrayList;
import java.util.List;

public class CommentFinder {

    public static List<String> CommentsInCurrentFile(AnActionEvent anActionEvent) {
        PsiFile file = anActionEvent.getDataContext().getData(LangDataKeys.PSI_FILE);
        List<PsiComment> psiComments = new ArrayList<>();
        FindComments(file, psiComments);

        List<String> comments = new ArrayList<>();
        for (PsiComment comment: psiComments) {
            comments.add(comment.getText());
        }

        return comments;
    }

    private static void FindComments(PsiElement element, List<PsiComment> comments) {
        if (element instanceof PsiComment) {
            comments.add((PsiComment) element);
        }
        for (PsiElement child: element.getChildren()) {
            FindComments(child, comments);
        }
    }
}
