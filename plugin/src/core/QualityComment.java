package core;

import com.intellij.psi.*;
import org.jetbrains.annotations.NotNull;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * our model class that represents one comment in the code base that can get quality-analysed
 */
public class QualityComment {

    public enum Position {
        Unknown,
        LicenseHeader,
        BeforeClass,
        BeforeMethod,
        BeforeCodeBlock,
        InCodeBlock,
    }

    private final PsiComment[] psiComments;
    public final Position position;
    private final List<PsiElement> relatedCodeRoots;

    /**
     * @param psiComments can be multiple, but they all should be siblings and passed in order
     */
    public QualityComment(@NotNull PsiComment... psiComments) {
        this.psiComments = psiComments;
        position = CommentFinder.classifyPositionOf(psiComments[0]);
        relatedCodeRoots = findRelatedCodeRoots();
    }

    /**
     * @return the whole content of this comment, including the comment-creating characters
     */
    public String fullCommentText() {
        return Arrays.stream(psiComments).map(PsiElement::getText).reduce((s1, s2) -> s1 + "\n" + s2).orElse("");
    }

    /**
     * @return just the text that lies within the comment, inside the comment-creating characters
     */
    public String commentText() {
        return Arrays.stream(psiComments).map(QualityComment::contentStringOf).reduce((s1, s2) -> s1 + "\n" + s2).orElse("");
    }

    private static String contentStringOf(PsiComment comment) {
        // this sadly omits all the @param, @author and all these tags, so we cannot use it
        //if (comment instanceof PsiDocComment) {
        //    PsiElement[] descriptionElements = ((PsiDocComment) comment).getDescriptionElements();
        //    String result = "";
        //    for (PsiElement e : descriptionElements) {
        //        result = result.trim() + " " + e.getText();
        //    }
        //    return result.trim();
        //}

        String full = comment.getText();
        if (full.startsWith("/*") && full.endsWith("*/")) {
            String withoutEnds = full.substring("/*".length(), full.length() - "*/".length()).trim();
            String[] lines = withoutEnds.split("\\n");
            for (int i = 0; i < lines.length; i++) {
                String trimmed = lines[i].trim();
                if (trimmed.startsWith("*")) {
                    trimmed = trimmed.substring("*".length()).trim();
                }
                if (trimmed.length() < 3) {
                    trimmed = "";
                }
                lines[i] = trimmed;
            }
            return String.join("\n", lines).trim();
        } else if (full.startsWith("//")) {
            return full.substring("//".length()).trim();
        } else {
            System.err.println("Cannot determine on how to strip the comment content from psi node!");
        }
        return full;
    }

    public String relatedCodeText() {
        return Utils.commentFreeTextOf(relatedCodeRoots);
    }

    public List<String> commentWordList() {
        return LanguageProcessor.normalizedWordList(commentText());
    }

    public List<String> relatedCodeWordList() {
        return LanguageProcessor.normalizedWordList(relatedCodeText());
    }

    @NotNull
    private List<PsiElement> findRelatedCodeRoots() {
        switch (position) {
            case BeforeClass:
            case BeforeMethod:
            case InCodeBlock:
                return Collections.singletonList(Utils.statementParentOf(psiComments[0].getParent()));
            case BeforeCodeBlock:
                return Utils.allNextSiblingsOf(psiComments[psiComments.length - 1]);
            default:
                return Collections.emptyList();
        }
    }

    public String relatedCodeIdentity() {
        StringBuilder data = null;

        if (position == Position.BeforeMethod) {
            PsiElement methodNode = relatedCodeRoots.get(0);
            assert methodNode instanceof PsiMethod;
            data = new StringBuilder(Utils.nonBlockChildTextOf(methodNode));

            PsiElement parent = relatedCodeRoots.get(0).getParent();
            while (parent != null) {
                if (parent instanceof PsiMethod) {
                    PsiMethod methodParent = (PsiMethod) parent;
                    //data.insert(0, methodParent.getReturnTypeElement().getText() + " " + methodParent.getName() + " " + methodParent.getParameterList().getText() + " -> ");
                    data.insert(0, Utils.nonBlockChildTextOf(parent) + " -> ");
                } else if (parent instanceof PsiClass) {
                    PsiClass classParent = (PsiClass) parent;
                    data.insert(0, classParent.getName() + " -> ");
                }
                parent = parent.getParent();
            }
        }

        if (data == null) {
            data = new StringBuilder(relatedCodeText());
            if (relatedCodeText().length() > 50) {
                data = new StringBuilder(data.substring(0, 50));
            }
        }

        return data.toString().replaceAll("\n", " ").trim();
    }
}
