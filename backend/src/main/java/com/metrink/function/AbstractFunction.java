package com.metrink.function;

import java.util.List;
import java.util.Map;

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
}
