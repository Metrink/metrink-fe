package com.metrink.function;

import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class EventFunction extends AbstractFunction {
    private static final Logger LOG = LoggerFactory.getLogger(EventFunction.class);

    public EventFunction(final Map<String, List<Object>> fields) {
        super("EventFunction", fields);
    }
}
