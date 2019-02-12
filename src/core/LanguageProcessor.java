package core;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LanguageProcessor {

    /**
     * transforms raw text to a list of words in it, splitting at spaces,
     * camelCases, newlines, sentence-ends and other common word-separators.
     * Makes everything lowercase.
     *
     * @param content e.g. "We'll not take that road.   The other-road is better."
     * @return e.g. [we will not take that road the other road is better]
     */
    public static List<String> normalizedWordList(String content) {
        final Pattern pattern = Pattern.compile("\\b[a-zA-Z0-9]+\\b");
        final Matcher matcher = pattern.matcher(content);

        List<String> words = new ArrayList<>();
        while (matcher.find()) {
            String word = matcher.group(0);
            words.add(word.toLowerCase());
        }
        return words;
    }
}
