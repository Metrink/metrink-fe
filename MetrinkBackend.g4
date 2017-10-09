grammar MetrinkBackend;

import MetrinkBase;

metric_alert:
    metric trigger_expression DO IDENTIFIER;

trigger_expression:
    comparitor number_literal FOR relative_time_literal;

comparitor:
    GT | GT_EQ | LT | LT_EQ | EQUAL | DB_EQ;

/*
 * TOKENS
 */
DO:
    'DO';

FOR:
    'FOR';

GT:
    '>';

LT:
    '<';

GT_EQ:
    '>=';

LT_EQ:
    '<=';

DB_EQ:
    '==';

