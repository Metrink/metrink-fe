package com.metrink;

import java.time.LocalDateTime;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.metrink.function.MetricFunction;

public class MetricAlert {
    private static final Logger LOG = LoggerFactory.getLogger(MetricAlert.class);

    final private MetricFunction metricFunction;
    final private String comparitor;
    final private Number limit;
    final private LocalDateTime duration;
    final private String action;

    public MetricAlert(final MetricFunction metricFunction, final String comparitor, final Number limit, final String action) {
        this(metricFunction, comparitor, limit, null, action);
    }

    public MetricAlert(final MetricFunction metricFunction, final String comparitor, final Number limit, final LocalDateTime duration, final String action) {
        this.metricFunction = metricFunction;
        this.comparitor = comparitor;
        this.limit = limit;
        this.duration = duration;
        this.action = action;
    }

    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder(metricFunction.toString());

        sb.append(comparitor);
        sb.append(limit);

        if (duration != null) {
            sb.append(" ");
            sb.append(duration);
        }

        sb.append(" ");
        sb.append(action);

        return sb.toString();
    }
}
