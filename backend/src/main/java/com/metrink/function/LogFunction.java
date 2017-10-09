package com.metrink.function;

import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LogFunction extends AbstractFunction {
    private static final Logger LOG = LoggerFactory.getLogger(LogFunction.class);

    public LogFunction(final Map<String, List<Object>> fields) {
        super("LogFunction", fields);
    }
}
