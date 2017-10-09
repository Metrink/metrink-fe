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
import com.metrink.parser.MetrinkBackendParser.Absolute_date_literalContext;
import com.metrink.parser.MetrinkBackendParser.Absolute_date_time_literalContext;
import com.metrink.parser.MetrinkBackendParser.Absolute_time_literalContext;
import com.metrink.parser.MetrinkBackendParser.Boolean_literalContext;
import com.metrink.parser.MetrinkBackendParser.ComparitorContext;
import com.metrink.parser.MetrinkBackendParser.EventContext;
import com.metrink.parser.MetrinkBackendParser.FieldContext;
import com.metrink.parser.MetrinkBackendParser.Field_listContext;
import com.metrink.parser.MetrinkBackendParser.Integer_literalContext;
import com.metrink.parser.MetrinkBackendParser.LogContext;
import com.metrink.parser.MetrinkBackendParser.MetricContext;
import com.metrink.parser.MetrinkBackendParser.Metric_alertContext;
import com.metrink.parser.MetrinkBackendParser.Number_arrayContext;
import com.metrink.parser.MetrinkBackendParser.Number_literalContext;
import com.metrink.parser.MetrinkBackendParser.Regex_literalContext;
import com.metrink.parser.MetrinkBackendParser.Relative_time_arrayContext;
import com.metrink.parser.MetrinkBackendParser.Relative_time_literalContext;
import com.metrink.parser.MetrinkBackendParser.String_arrayContext;
import com.metrink.parser.MetrinkBackendParser.String_literalContext;
import com.metrink.parser.MetrinkBackendParser.Trigger_expressionContext;
import com.metrink.parser.MetrinkBackendVisitor;

public class AlertVisitor extends AbstractParseTreeVisitor<Object> implements MetrinkBackendVisitor<Object> {
    private static final Logger LOG = LoggerFactory.getLogger(AlertVisitor.class);

    public Object visitMetric_alert(final Metric_alertContext ctx) {
        // TODO Auto-generated method stub
        return null;
    }

    public Object visitTrigger_expression(final Trigger_expressionContext ctx) {
        // TODO Auto-generated method stub
        return null;
    }

    public Object visitComparitor(final ComparitorContext ctx) {
        // TODO Auto-generated method stub
        return null;
    }

    public Object visitMetric(final MetricContext ctx) {
        // TODO Auto-generated method stub
        return null;
    }

    public Object visitLog(final LogContext ctx) {
        // TODO Auto-generated method stub
        return null;
    }

    public Object visitEvent(final EventContext ctx) {
        // TODO Auto-generated method stub
        return null;
    }

    private void collectFields(final Field_listContext ctx) {

    }

    public Object visitField_list(final Field_listContext ctx) {
        final Map<String, List<Object>> fields = new HashMap<String, List<Object>>();

        for (final ParseTree child : ctx.children) {
            final Entry<String, List<Object>> entry = (Entry<String, List<Object>>) this.visit(child);

            if (fields.containsKey(entry.getKey())) {
                throw new IllegalArgumentException("Field " + entry.getKey() + " is already set");
            }

            fields.put(entry.getKey(), entry.getValue());
        }

        return fields;
    }

    public Object visitField(final FieldContext ctx) {
        final String identifier = (String) this.visit(ctx.children.get(0));
        final Object value = this.visit(ctx.children.get(2)); // skip the colon

        // force to list, if not string array
        if (!(value instanceof List)) {
            return new SimpleImmutableEntry<String, List<Object>>(identifier, ImmutableList.of(value));
        } else {
            return new SimpleImmutableEntry<String, List<Object>>(identifier, ImmutableList.copyOf((List) value));
        }
    }

    public Object visitNumber_array(final Number_arrayContext ctx) {
        final List<Number> ret = new ArrayList<Number>();

        for (final ParseTree child : ctx.children) {
            ret.add((Number) this.visit(child));
        }

        return ret;
    }

    public Object visitNumber_literal(final Number_literalContext ctx) {
        this.visitChildren(ctx);

        final String literal = ctx.getText();

        if (literal.contains(".")) {
            return new Float(literal);
        } else {
            return new Integer(literal);
        }
    }

    public Object visitRelative_time_array(final Relative_time_arrayContext ctx) {
        final List<LocalDateTime> ret = new ArrayList<LocalDateTime>();

        for (final ParseTree child : ctx.children) {
            ret.add((LocalDateTime) this.visit(child));
        }

        return ret;
    }

    public Object visitRelative_time_literal(final Relative_time_literalContext ctx) {
        final Integer value = (Integer) this.visit(ctx.children.get(0));
        final String unit = (String) this.visit(ctx.children.get(1));

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

    public Object visitAbsolute_date_time_literal(final Absolute_date_time_literalContext ctx) {
        final LocalDateTime date = (LocalDateTime) this.visit(ctx.children.get(0));
        final LocalDateTime time = (LocalDateTime) this.visit(ctx.children.get(1));

        return LocalDateTime.of(date.getYear(), date.getMonth(), date.getDayOfMonth(), time.getHour(), time.getMinute());
    }

    public Object visitAbsolute_date_literal(final Absolute_date_literalContext ctx) {
        this.visitChildren(ctx);

        final String literal = ctx.getText();

        // format: POSITIVE_INTEGER_LITERAL MINUS POSITIVE_INTEGER_LITERAL MINUS
        // POSITIVE_INTEGER_LITERAL;
        final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");

        return LocalDateTime.from(formatter.parse(literal));
    }

    public Object visitAbsolute_time_literal(final Absolute_time_literalContext ctx) {
        this.visitChildren(ctx);

        final String literal = ctx.getText();

        // format: POSITIVE_INTEGER_LITERAL COLON POSITIVE_INTEGER_LITERAL
        // (PM_INDICATOR|AM_INDICATOR)?;
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm");

        if (literal.endsWith("m") || literal.endsWith("M")) {
            formatter = DateTimeFormatter.ofPattern("hh:mm aa");
        }

        return LocalDateTime.from(formatter.parse(literal));
    }

    public Object visitInteger_literal(final Integer_literalContext ctx) {
        this.visitChildren(ctx);

        return new Integer(ctx.getText());
    }

    public Object visitBoolean_literal(final Boolean_literalContext ctx) {
        this.visitChildren(ctx);

        if ("true".equalsIgnoreCase(ctx.getText())) {
            return Boolean.TRUE;
        } else {
            return Boolean.FALSE;
        }
    }

    public Object visitString_array(final String_arrayContext ctx) {
        final List<String> ret = new ArrayList<String>();

        for (final ParseTree child : ctx.children) {
            ret.add((String) this.visit(child));
        }

        return ret;
    }

    public Object visitRegex_literal(final Regex_literalContext ctx) {
        throw new UnsupportedOperationException("Regular expressions not supported yet");
    }

    public Object visitString_literal(final String_literalContext ctx) {
        this.visitChildren(ctx);

        String strLit = ctx.getText();
        strLit = strLit.substring(1, strLit.length() - 1);

        return strLit;
    }

    @Override
    public Object visitTerminal(final TerminalNode node) {
        return node.getText();
    }

}
