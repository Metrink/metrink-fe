package com.metrink;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.AbstractMap.SimpleImmutableEntry;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.antlr.v4.runtime.tree.AbstractParseTreeVisitor;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.TerminalNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.collect.ImmutableList;
import com.metrink.function.EventFunction;
import com.metrink.function.LogFunction;
import com.metrink.function.MetricFunction;
import com.metrink.parser.MetrinkBackendParser.Absolute_date_literalContext;
import com.metrink.parser.MetrinkBackendParser.Absolute_date_time_literalContext;
import com.metrink.parser.MetrinkBackendParser.Absolute_time_literalContext;
import com.metrink.parser.MetrinkBackendParser.Boolean_literalContext;
import com.metrink.parser.MetrinkBackendParser.ComparitorContext;
import com.metrink.parser.MetrinkBackendParser.EventContext;
import com.metrink.parser.MetrinkBackendParser.Event_identContext;
import com.metrink.parser.MetrinkBackendParser.FieldContext;
import com.metrink.parser.MetrinkBackendParser.Field_listContext;
import com.metrink.parser.MetrinkBackendParser.Integer_literalContext;
import com.metrink.parser.MetrinkBackendParser.LogContext;
import com.metrink.parser.MetrinkBackendParser.Log_identContext;
import com.metrink.parser.MetrinkBackendParser.MetricContext;
import com.metrink.parser.MetrinkBackendParser.Metric_alertContext;
import com.metrink.parser.MetrinkBackendParser.Metric_identContext;
import com.metrink.parser.MetrinkBackendParser.Number_arrayContext;
import com.metrink.parser.MetrinkBackendParser.Number_literalContext;
import com.metrink.parser.MetrinkBackendParser.Regex_literalContext;
import com.metrink.parser.MetrinkBackendParser.Relative_time_arrayContext;
import com.metrink.parser.MetrinkBackendParser.Relative_time_literalContext;
import com.metrink.parser.MetrinkBackendParser.String_arrayContext;
import com.metrink.parser.MetrinkBackendParser.String_literalContext;
import com.metrink.parser.MetrinkBackendParser.Time_indicatorContext;
import com.metrink.parser.MetrinkBackendVisitor;

public class AlertVisitor extends AbstractParseTreeVisitor<Object> implements MetrinkBackendVisitor<Object> {
    private static final Logger LOG = LoggerFactory.getLogger(AlertVisitor.class);

    @Override
    public Object visitMetric_alert(final Metric_alertContext ctx) {
        if (ctx.getChildCount() == 5) { // no duration
            return new MetricAlert((MetricFunction) visit(ctx.getChild(0)), (String) visit(ctx.getChild(1)), (Number) visit(ctx.getChild(2)), (String) visit(ctx
                    .getChild(4)));
        } else {
            return new MetricAlert((MetricFunction) visit(ctx.getChild(0)), (String) visit(ctx.getChild(1)), (Number) visit(ctx.getChild(2)),
                    (LocalDateTime) visit(ctx.getChild(4)), (String) visit(ctx.getChild(6)));
        }
    }

    @Override
    public Object visitComparitor(final ComparitorContext ctx) {
        return ctx.getText(); // just return the string for now
    }

    @Override
    public Object visitMetric(final MetricContext ctx) {
        if (ctx.children.size() == 6) {
            return new MetricFunction((Map<String, List<Object>>) visit(ctx.getChild(2)), (LocalDateTime) visit(ctx.getChild(4)));
        } else {
            return new MetricFunction((Map<String, List<Object>>) visit(ctx.getChild(2)), null);
        }
    }

    @Override
    public Object visitLog(final LogContext ctx) {
        return new LogFunction((Map<String, List<Object>>) visit(ctx.getChild(2)));
    }

    @Override
    public Object visitEvent(final EventContext ctx) {
        return new EventFunction((Map<String, List<Object>>) visit(ctx.getChild(2)));
    }

    @Override
    public Object visitMetric_ident(final Metric_identContext ctx) {
        return ctx.getText();
    }

    @Override
    public Object visitLog_ident(final Log_identContext ctx) {
        return ctx.getText();
    }

    @Override
    public Object visitEvent_ident(final Event_identContext ctx) {
        return ctx.getText();
    }

    @Override
    public Object visitField_list(final Field_listContext ctx) {
        final Map<String, List<Object>> fields = new HashMap<>();

        for (final ParseTree child : ctx.children) {
            if (",".equals(child.getText())) {
                continue;
            }

            final Entry<String, List<Object>> entry = (Entry<String, List<Object>>) visit(child);

            if (fields.containsKey(entry.getKey())) {
                throw new IllegalArgumentException("Field " + entry.getKey() + " is already set");
            }

            fields.put(entry.getKey(), entry.getValue());
        }

        return fields;
    }

    @Override
    public Object visitField(final FieldContext ctx) {
        final String identifier = (String) visit(ctx.getChild(0));
        final Object value = visit(ctx.getChild(2)); // skip the colon

        // force to list, if not string array
        if (!(value instanceof List)) {
            return new SimpleImmutableEntry<String, List<Object>>(identifier, ImmutableList.of(value));
        } else {
            return new SimpleImmutableEntry<String, List<Object>>(identifier, ImmutableList.copyOf((List) value));
        }
    }

    @Override
    public Object visitNumber_array(final Number_arrayContext ctx) {
        final List<Number> ret = new ArrayList<>();

        for (final ParseTree child : ctx.children) {
            ret.add((Number) visit(child));
        }

        return ret;
    }

    @Override
    public Object visitNumber_literal(final Number_literalContext ctx) {
        visitChildren(ctx);

        final String literal = ctx.getText();

        if (literal.contains(".")) {
            return new Float(literal);
        } else {
            return new Integer(literal);
        }
    }

    @Override
    public Object visitRelative_time_array(final Relative_time_arrayContext ctx) {
        final List<LocalDateTime> ret = new ArrayList<>();

        for (final ParseTree child : ctx.children) {
            ret.add((LocalDateTime) visit(child));
        }

        return ret;
    }

    @Override
    public Object visitRelative_time_literal(final Relative_time_literalContext ctx) {
        final Integer value = (Integer) visit(ctx.getChild(0));
        final String unit = (String) visit(ctx.getChild(1));

        ChronoUnit chronoUnit;

        if ("s".equalsIgnoreCase(unit)) {
            chronoUnit = ChronoUnit.SECONDS;
        } else if ("m".equalsIgnoreCase(unit)) {
            chronoUnit = ChronoUnit.MINUTES;
        } else if ("d".equalsIgnoreCase(unit)) {
            chronoUnit = ChronoUnit.HOURS;
        } else if ("d".equalsIgnoreCase(unit)) {
            chronoUnit = ChronoUnit.DAYS;
        } else {
            throw new IllegalArgumentException("Unknown relative time unit: " + unit);
        }

        return LocalDateTime.now().minus(Duration.of(value, chronoUnit));
    }

    @Override
    public Object visitAbsolute_date_time_literal(final Absolute_date_time_literalContext ctx) {
        final LocalDateTime date = (LocalDateTime) visit(ctx.getChild(0));
        final LocalDateTime time = (LocalDateTime) visit(ctx.getChild(1));

        return LocalDateTime.of(date.getYear(), date.getMonth(), date.getDayOfMonth(), time.getHour(), time.getMinute());
    }

    @Override
    public Object visitAbsolute_date_literal(final Absolute_date_literalContext ctx) {
        visitChildren(ctx);

        final String literal = ctx.getText();

        // format: POSITIVE_INTEGER_LITERAL MINUS POSITIVE_INTEGER_LITERAL MINUS
        // POSITIVE_INTEGER_LITERAL;
        final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");

        return LocalDateTime.from(formatter.parse(literal));
    }

    @Override
    public Object visitAbsolute_time_literal(final Absolute_time_literalContext ctx) {
        visitChildren(ctx);

        final String literal = ctx.getText();

        // format: POSITIVE_INTEGER_LITERAL COLON POSITIVE_INTEGER_LITERAL
        // (PM_INDICATOR|AM_INDICATOR)?;
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm");

        if (literal.endsWith("m") || literal.endsWith("M")) {
            formatter = DateTimeFormatter.ofPattern("hh:mm aa");
        }

        return LocalDateTime.from(formatter.parse(literal));
    }

    @Override
    public Object visitInteger_literal(final Integer_literalContext ctx) {
        visitChildren(ctx);

        return new Integer(ctx.getText());
    }

    @Override
    public Object visitBoolean_literal(final Boolean_literalContext ctx) {
        visitChildren(ctx);

        if ("true".equalsIgnoreCase(ctx.getText())) {
            return Boolean.TRUE;
        } else {
            return Boolean.FALSE;
        }
    }

    @Override
    public Object visitString_array(final String_arrayContext ctx) {
        final List<String> ret = new ArrayList<>();

        for (int i = 1; i < ctx.getChildCount(); i += 2) {
            ret.add((String) visit(ctx.getChild(i)));
        }

        return ret;
    }

    @Override
    public Object visitRegex_literal(final Regex_literalContext ctx) {
        throw new UnsupportedOperationException("Regular expressions not supported yet");
    }

    @Override
    public Object visitString_literal(final String_literalContext ctx) {
        visitChildren(ctx);

        String strLit = ctx.getText();
        strLit = strLit.substring(1, strLit.length() - 1);

        return strLit;
    }

    @Override
    public Object visitTime_indicator(final Time_indicatorContext ctx) {
        return ctx.getText();
    }

    @Override
    public Object visitTerminal(final TerminalNode node) {
        return node.getText();
    }

}
