package inspections;

import com.intellij.codeInspection.InspectionToolProvider;
import org.jetbrains.annotations.NotNull;

/**
 * tells the IDE what inspections this plugin wants to add to it
 */
class BadCommentsInspectionsProvider implements InspectionToolProvider {
    @NotNull
    @Override
    public Class[] getInspectionClasses() {
        Class[] data = new Class[1];
        data[0] = BadCommentsInspection.class;
        return data;
    }
}