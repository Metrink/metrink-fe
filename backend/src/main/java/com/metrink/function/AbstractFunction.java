package com.metrink.function;

import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.function.Function;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public abstract class AbstractFunction {
    private static final Logger LOG = LoggerFactory.getLogger(AbstractFunction.class);

    private final String name;
    private final Map<String, List<Object>> fields;

    public AbstractFunction(final String name, final Map<String, List<Object>> fields) {
        this.name = name;
        this.fields = fields;
    }

    @Override
    public String toString() {
        final StringBuilder ret = new StringBuilder(name);

        ret.append("(");

        // kinda and hacky-unreadable
        final List<String> fieldStrings = fields.entrySet().stream().map((Function<? super Entry<String, List<Object>>, ? extends String>) (
                final Map.Entry<String, List<Object>> e) -> {
            // force everything into a list of field values
            final List<String> f = e.getValue().stream().map(obj -> {
                return obj instanceof String ? "'" + obj.toString() + "'" : obj.toString();
            }).collect(Collectors.toList());

            return e.getKey() + ":[" + String.join(",", f) + "]";
        }).collect(Collectors.toList());

        // join all the fields together with commas
        ret.append(String.join(", ", fieldStrings));

        ret.append(")");

        return ret.toString();
    }
}
