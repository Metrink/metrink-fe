grammar Metrink;

metrink_query:
    (relative_time_literal | absolute_date_time_literal | absolute_time_literal) ('to' (absolute_date_time_literal | absolute_time_literal) )? (graph_expression | log_expression);

log_expression:
    (log)+ (connector function)*;

graph_expression:
    (additive_expression)+ (connector function)*;

metric:
    METRIC LPAREN field_list (COMMA field_list)* (COMMA (relative_time_literal|relative_time_array))? RPAREN;

log:
    LOG LPAREN index_specifier (COMMA field_list)+ RPAREN;

index_specifier:
    INDEX EQUAL (string_literal|string_array);

field_list:
    IDENTIFIER EQUAL (string_literal|string_literal);

connector:
    PIPE | COPY_PIPE | AMP;

string_array:
    LBRACKET string_literal (COMMA string_literal)* RBRACKET;

function:
    IDENTIFIER ( argument_list )?;

argument_list:
    LPAREN argument (COMMA argument)* RPAREN;

argument:
    relative_time_literal | additive_expression | string_literal | percent_literal | boolean_literal;

additive_expression:
    multiplicative_expression ( (PLUS|MINUS) additive_expression )?;

multiplicative_expression:
    (number_literal|metric|function) ( (MUL|DIV) multiplicative_expression )?;

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

percent_literal:
    integer_literal REM;

boolean_literal:
    TRUE | FALSE;

string_literal:
    STRING_LITERAL;

/*
 * TOKENS
 */
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

INDEX:
    ('index'|'i');

LPAREN:
    '(';

RPAREN:
    ')';

LBRACKET:
    '[';

RBRACKET:
    ']';

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
    [a-zA-Z][a-zA-Z0-9_]*;

POSITIVE_INTEGER_LITERAL:
    [0-9]+;

FLOATING_POINT_LITERAL:
    '-'?(([0-9]+'.'[0-9]*)|('.'[0-9]+));

STRING_LITERAL:
   QUOTE SCharSequence? QUOTE;

QUOTE:
    ('\"'|'\'') -> channel(HIDDEN);

WS:
    [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

fragment SCharSequence:
   SChar+;

fragment SChar:
   ~["\\\r\n'] | '\\' ['"?abfnrtv\\];