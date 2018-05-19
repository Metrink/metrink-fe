package com.metrink;

import java.util.Set;

import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.datto.monitoring.Metric;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class FlinkAlertStream implements Runnable {
    private static final Logger LOG = LoggerFactory.getLogger(FlinkAlertStream.class);

    private final StreamExecutionEnvironment env;
    private final DataStream<ObjectNode> objectStream;
    private final ParameterTool parameters;
    private final Set<MetricAlert> alerts;

    public FlinkAlertStream(final StreamExecutionEnvironment env, final DataStream<ObjectNode> objectStream, final ParameterTool parameters) {
        this.env = env;
        this.objectStream = objectStream;
        this.parameters = parameters;
    }

    @Override
    public void run() {
        final ObjectMapper mapper = new ObjectMapper();

        // first convert the JSON into Metric objects
        final SingleOutputStreamOperator<Metric> metricStream =
                objectStream.map(node -> mapper.convertValue(node, Metric.class)).name("metric stream");

        metricStream.filter(metric -> {

        })


        // we divide the object stream into 2: non-windowed, and windowed


    }

}
