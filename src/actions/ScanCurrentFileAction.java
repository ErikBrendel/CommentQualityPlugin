package actions;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import core.CommentFinder;
import org.jetbrains.annotations.NotNull;

import java.util.List;

public class ScanCurrentFileAction extends AnAction {

    public ScanCurrentFileAction() {
        this("ScanCurrentFileAction");
    }

    public ScanCurrentFileAction(String name) {
        super(name);
    }

    @Override
    public void actionPerformed(@NotNull AnActionEvent anActionEvent) {
        List<String> comments = CommentFinder.CommentsInCurrentFile(anActionEvent);
        System.out.println("Comments: " + comments.size());
        for (String comment : comments) {
            System.out.println(comment);
        }
    }
}
