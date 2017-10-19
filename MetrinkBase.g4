grammar MetrinkBase;

metric:
    metric_ident LPAREN field_list (COMMA (relative_time_literal|relative_time_array))? RPAREN;

log:
    log_ident LPAREN field_list RPAREN;

event:
    event_ident LPAREN field_list RPAREN;

metric_ident:
    'metric' | 'm';

log_ident:
    'log' | 'l';

event_ident:
    'event' | 'e';

field_list:
    field (COMMA field)*;

field:
    IDENTIFIER COLON (string_literal|string_array|number_literal|regex_literal);

number_array:
    LBRACKET number_literal (COMMA number_literal)* RBRACKET;

number_literal:
    integer_literal | FLOATING_POINT_LITERAL;

relative_time_array:
    LBRACKET relative_time_literal (COMMA relative_time_literal)* RBRACKET;

relative_time_literal:
    integer_literal time_indicator;

absolute_date_time_literal:
    absolute_date_literal absolute_time_literal;

absolute_date_literal:
    POSITIVE_INTEGER_LITERAL MINUS POSITIVE_INTEGER_LITERAL MINUS POSITIVE_INTEGER_LITERAL;

absolute_time_literal:
    POSITIVE_INTEGER_LITERAL COLON POSITIVE_INTEGER_LITERAL (PM_INDICATOR|AM_INDICATOR)?;

integer_literal:
    MINUS? POSITIVE_INTEGER_LITERAL;

boolean_literal:
    TRUE | FALSE;

string_array:
    LBRACKET string_literal (COMMA string_literal)* RBRACKET;

regex_literal:
    REGEX_LITERAL;

string_literal:
    STRING_LITERAL;

time_indicator:
    's' | 'm' | 'h' | 'd';

/*
 * TOKENS
 */
DO:
    'DO';

FOR:
    'FOR';

PIPE:
    '|';

COPY_PIPE:
    '>|';

AMP:
    '&';

LPAREN:
    '(';

RPAREN:
    ')';

LBRACKET:
    '[';

RBRACKET:
    ']';

LBRACE:
    '{';

RBRACE:
    '}';

COMMA:
    ',';

EQUAL:
    '=';

PLUS:
    '+';

MINUS:
    '-';

MUL:
    '*';

DIV:
    '/';

REM:
    '%';

COLON:
    ':';

PM_INDICATOR:
    [pP][mM]/*(LOWER_M|'M')*/;

AM_INDICATOR:
    [aA][mM]/*(LOWER_M|'M')*/;

TRUE:
    'true'|'TRUE';

FALSE:
    'false'|'FALSE';
/*
LOWER_M:
    'm';
*/
IDENTIFIER: /* must be 2-char long to disambiguate with metric/log/event */
    [a-zA-Z][a-zA-Z0-9_.]+;

POSITIVE_INTEGER_LITERAL:
    [0-9]+;

FLOATING_POINT_LITERAL:
    '-'?(([0-9]+'.'[0-9]*)|('.'[0-9]+));

REGEX_LITERAL:
    LBRACE SCharSequence? RBRACE;

STRING_LITERAL:
   QUOTE SCharSequence? QUOTE;

QUOTE:
    ('"'|'\'') -> channel(HIDDEN);

WS:
    [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

fragment SCharSequence:
   SChar+;

fragment SChar:
   ~["\\\r\n'] | '\\' ['"?abfnrtv\\];