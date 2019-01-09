package actions;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import org.jetbrains.annotations.NotNull;

public class ScanCurrentFileAction extends AnAction {

    public ScanCurrentFileAction() {
        this("ScanCurrentFileAction");
    }

    public ScanCurrentFileAction(String name) {
        super(name);
    }

    @Override
    public void actionPerformed(@NotNull AnActionEvent anActionEvent) {
        System.err.println("lol");
    }
}
