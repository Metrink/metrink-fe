grammar MetrinkFrontend;

import MetrinkBase;

metrink_query:
    (relative_time_literal | absolute_date_time_literal | absolute_time_literal) ('to' (absolute_date_time_literal | absolute_time_literal) )? (graph_expression | log_expression | event_expression);

