grammar MetrinkFrontend;

import MetrinkBase;

metrink_query:
    (relative_time_literal | absolute_date_time_literal | absolute_time_literal) ('to' (absolute_date_time_literal | absolute_time_literal) )? (graph_expression | log_expression | event_expression);

log_expression:
    (log)+ (connector function)*;

event_expression:
    (event)+ (connector function)*;

graph_expression:
    (additive_expression)+ (connector function)*;

connector:
    PIPE | COPY_PIPE | AMP;

function:
    IDENTIFIER ( argument_list )?;

argument_list:
    LPAREN argument (COMMA argument)* RPAREN;

argument:
    relative_time_literal | additive_expression | string_literal | boolean_literal;

additive_expression:
    multiplicative_expression ( (PLUS|MINUS) additive_expression )?;

multiplicative_expression:
    (number_literal|metric|function) ( (MUL|DIV) multiplicative_expression )?;

