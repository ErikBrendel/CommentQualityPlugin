package core;

import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LanguageProcessor {

    // https://stackoverflow.com/questions/7593969/regex-to-split-camelcase-or-titlecase-advanced
    private static String CamelCaseRegex = "(?<!(^|[A-Z]))(?=[A-Z])|(?<!^)(?=[A-Z][a-z])";
    // https://www.ranks.nl/stopwords
    private static HashSet<String> StopWords = new HashSet<>(Arrays.asList("a about above after again against all am an and any are aren as at be because been before being below between both but by can cannot could couldn did didn do does doesn doing don down during each few for from further had hadn has hasn have haven having he her here hers herself him himself his how i if in into is isn it its itself let me more most mustn my myself no nor not of off on once only or other ought our ours ourselves out over own same shan she should shouldn so some such than that the their theirs them themselves then there these they this those through to too under until up very was wasn we were weren what when where which while who whom why with won would wouldn you your yours yourself yourselves".split(" ")));

    /**
     * transforms raw text to a list of words in it, splitting at spaces,
     * camelCases, newlines, sentence-ends and other common word-separators.
     * Makes everything lowercase.
     *
     * @param content e.g. "We'll not take that road.   The other-road is better."
     * @return e.g. [we not take that road the other road is better]
     */
    public static List<String> normalizedWordList(String content) {
        final Pattern pattern = Pattern.compile("\\b[a-zA-Z0-9]+\\b");
        final Matcher matcher = pattern.matcher(content);

        List<String> words = new ArrayList<>();
        while (matcher.find()) {
            String identified = matcher.group(0);
            for (String word : identified.split(CamelCaseRegex)) {
                String normalized = NormalizeWord(word);
                if (normalized != null) words.add(normalized);
            }
        }
        return words;
    }

    @Nullable
    private static String NormalizeWord(String word) {
        word = word.split("'")[0];

        word = word.toLowerCase();

        if (StopWords.contains(word)) return null;

        return word;
    }

}
