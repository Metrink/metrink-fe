package com.metrink.function;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MetricFunction extends AbstractFunction {
    private static final Logger LOG = LoggerFactory.getLogger(MetricFunction.class);

    private final LocalDateTime overlay;

    public MetricFunction(final Map<String, List<Object>> fields, final LocalDateTime overlay) {
        super("MetricFunction", fields);
        this.overlay = overlay;
    }
}
