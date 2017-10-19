grammar MetrinkBackend;

import MetrinkBase;

metric_alert:
    metric comparitor number_literal (FOR relative_time_literal)? DO IDENTIFIER;

comparitor:
    GT | GT_EQ | LT | LT_EQ | EQUAL | DB_EQ;

/*
 * TOKENS
 */
DO:
    'DO'|'do';

FOR:
    'FOR'|'for';

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

