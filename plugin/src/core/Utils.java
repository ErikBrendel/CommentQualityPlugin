package core;

import com.intellij.openapi.editor.Document;
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

    public static boolean isInSingleLineCodeBlock(PsiComment comment) {
        PsiElement parent = comment.getParent();
        return lineNumberOf(parent) == lineNumberOfEnd(parent);
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

    public static PsiElement previousNonWhitespaceElement(PsiElement element) {
        PsiElement current = element;
        while (current != null) {
            current = current.getPrevSibling();
            if (!(current instanceof PsiWhiteSpace)) return current;
        }
        return null;
    }

    public static PsiElement nextNonWhitespaceElement(PsiElement element) {
        PsiElement current = element;
        while (current != null) {
            current = current.getNextSibling();
            if (!(current instanceof PsiWhiteSpace)) return current;
        }
        return null;
    }

    public static String commentFreeTextOf(List<PsiElement> roots) {
        StringBuilder s = new StringBuilder();
        for (PsiElement root : roots) {
            s.append("\n");
            readCommentFreeTextOf(root, s);
        }
        return s.toString().trim();
    }

    private static void readCommentFreeTextOf(PsiElement element, StringBuilder s) {
        if (element instanceof PsiComment) return;

        if (element.getChildren().length == 0) {
            s.append(element.getText());
            return;
        }

        for (PsiElement child : element.getChildren()) {
            readCommentFreeTextOf(child, s);
        }
    }

    public static String nonBlockChildTextOf(PsiElement element) {
        StringBuilder s = new StringBuilder();
        readNonBlockChildTextOf(s, element);
        return s.toString().trim();
    }

    private static void readNonBlockChildTextOf(StringBuilder s, PsiElement element) {
        PsiElement[] children = element.getChildren();
        if (children.length == 0) {
            s.append(element.getText());
        } else {
            for (PsiElement child : children) {
                if (!(child instanceof PsiCodeBlock) && !(child instanceof PsiComment)) {
                    readNonBlockChildTextOf(s, child);
                }
            }
        }
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

    public static int lineNumberOf(PsiElement element) {
        return lineNumberIn(element, element.getTextRange().getStartOffset());
    }

    public static int lineNumberOfEnd(PsiElement element) {
        return lineNumberIn(element, element.getTextRange().getEndOffset());
    }

    private static int lineNumberIn(PsiElement container, int offset) {
        try {
            PsiFile containingFile = container.getContainingFile();
            Document document = PsiDocumentManager.getInstance(containingFile.getProject()).getDocument(containingFile);
            if (document == null) return 0;
            return document.getLineNumber(offset);
        } catch (IndexOutOfBoundsException e) {
            throw new RuntimeException(e);
        }
    }
}
