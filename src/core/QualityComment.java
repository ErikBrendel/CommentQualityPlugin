package core;

import com.intellij.psi.PsiComment;
import org.jetbrains.annotations.NotNull;

/**
 * our model class that represents one comment in the code base that can get quality-analysed
 */
public class QualityComment {

    private final PsiComment psiComment;

    public QualityComment(@NotNull PsiComment psiComment) {
        this.psiComment = psiComment;
    }

    /**
     * @return the whole content of this comment, including the comment-creating characters
     */
    public String fullText() {
        return psiComment.getText();
    }

    /**
     * @return just the text that lies within the comment, inside the comment-creating characters
     */
    public String contentString() {
        // this sadly omits all the @param, @author and all these tags, so we cannot use it
        //if (psiComment instanceof PsiDocComment) {
        //    PsiElement[] descriptionElements = ((PsiDocComment) psiComment).getDescriptionElements();
        //    String result = "";
        //    for (PsiElement e : descriptionElements) {
        //        result = result.trim() + " " + e.getText();
        //    }
        //    return result.trim();
        //}


        String full = fullText().trim();
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
}
