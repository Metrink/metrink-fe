package com.metrink;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;

import org.antlr.v4.runtime.BaseErrorListener;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CodePointCharStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.RecognitionException;
import org.antlr.v4.runtime.Recognizer;
import org.antlr.v4.runtime.Token;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.metrink.parser.MetrinkBackendLexer;
import com.metrink.parser.MetrinkBackendParser;
import com.metrink.parser.MetrinkBackendParser.Metric_alertContext;

public class AlertVisitorTest {
    private static final Logger LOG = LoggerFactory.getLogger(AlertVisitorTest.class);

    @Before
    public void setUp() throws Exception {
    }

    private static class MyErrorListener extends BaseErrorListener {

        @Override
        public void syntaxError(final Recognizer<?, ?> recognizer,
                final Object offendingSymbol,
                final int line,
                final int charPositionInLine,
                final String msg,
                final RecognitionException e) {
            LOG.error("{}:{} {}", line, charPositionInLine, msg);
            // LOG.error("ERROR:", e);
        }
    }

    @Test
    public void test() throws Exception {

        try (Stream<String> stream = Files.lines(Paths.get("src/test/resources/valid_queries.txt"))) {
            stream.forEach((final String line) -> {
                if (line.isEmpty() || line.startsWith("#")) {
                    return;
                }

                final CodePointCharStream charStream = CharStreams.fromString(line);
                final MetrinkBackendLexer lexer = new MetrinkBackendLexer(charStream);
                final CommonTokenStream tokenStream = new CommonTokenStream(lexer);

                tokenStream.fill();

                for (final Token token : tokenStream.getTokens()) {
                    LOG.info("TOKEN: {} {}", token, lexer.getVocabulary().getSymbolicName(token.getType()));
                }

                tokenStream.seek(0);

                final MetrinkBackendParser mbp = new MetrinkBackendParser(tokenStream);

                mbp.removeErrorListeners();
                mbp.addErrorListener(new MyErrorListener());

                final Metric_alertContext tree = mbp.metric_alert();

                final AlertVisitor av = new AlertVisitor();

                final Object ret = av.visit(tree);

                if (ret instanceof MetricAlert) {
                    LOG.info("Successfully parsed: {}", line);
                }
            });
        }
    }
}
