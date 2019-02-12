package core;

import com.intellij.psi.*;

import java.util.ArrayList;
import java.util.List;

public class Utils {

    public static boolean isAtStartOfContainingBlock(PsiComment comment) {
        PsiElement parent = comment.getParent();
        PsiElement firstChild = parent.getFirstChild();
        if (comment == firstChild) return true;

        PsiElement current = comment;

        while (current != firstChild) {
            current = current.getPrevSibling();
            if (!isIgnorable(current)) return false;
        }

        return true;
    }

    private static boolean isIgnorable(PsiElement element) {
        return element instanceof PsiWhiteSpace || element instanceof PsiJavaToken;
    }

    public static boolean isFollowedByCode(PsiComment comment) {
        PsiElement current = comment;
        while (current != null) {
            current = current.getNextSibling();
            if (current instanceof PsiStatement) return true;
        }
        return false;
    }

    public static List<PsiElement> allNextSiblingsOf(PsiElement targetElement) {
        List<PsiElement> elements = new ArrayList<>();

        PsiElement current = targetElement.getNextSibling();
        while (current != null) {
            elements.add(current);
            current = current.getNextSibling();
        }

        return elements;
    }

    public static String commentFreeTextOf(List<PsiElement> roots) {
        StringBuilder s = new StringBuilder();
        for (PsiElement root : roots) {
            if (!(root instanceof PsiComment)) {
                PsiElement copy = root.copy();
                deleteCommentsIn(copy);
                s.append(" ").append(copy.getText());
            }
        }
        return s.toString();
    }

    private static void deleteCommentsIn(PsiElement element) {
        for (PsiElement child : element.getChildren()) {
            if (child instanceof PsiComment) {
                child.delete();
            } else {
                deleteCommentsIn(child);
            }
        }
    }

    public static PsiElement statementParentOf(PsiElement element) {
        PsiElement current = element;
        while (current != null) {
            if (current instanceof PsiStatement && !(current instanceof PsiBlockStatement)) {
                return current;
            }
            current = current.getParent();
        }
        return element;
    }
}
