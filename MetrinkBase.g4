grammar MetrinkBase;

metric:
    METRIC LPAREN field_list (COMMA (relative_time_literal|relative_time_array))? RPAREN;

log:
    LOG LPAREN field_list RPAREN;

event:
    EVENT LPAREN field_list RPAREN;

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
    integer_literal TIME_INDICATOR;

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

METRIC:
    ('metric'|'m');

LOG:
    ('log'|'l');

EVENT:
    ('log'|'l');

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

TIME_INDICATOR:
    [smhd];

PM_INDICATOR:
    [pP][mM];

AM_INDICATOR:
    [aA][mM];

TRUE:
    'true'|'TRUE';

FALSE:
    'false'|'FALSE';

IDENTIFIER:
    [a-zA-Z][a-zA-Z0-9_.]*;

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