grammar metrink;

graph_query:
    (relative_time_literal | absolute_date_literal | absolute_time_literal) ('to' (absolute_date_literal | absolute_time_literal) )? graph_expression;

graph_expression:
    (additive_expression)+ (connector function)*;

connector:
    PIPE | COPY_PIPE | AMP;

metric:
    METRIC LPAREN (string_array|STRING_LITERAL) COMMA (string_array|STRING_LITERAL) COMMA (string_array|STRING_LITERAL) (COMMA (relative_time_literal|relative_time_array))? RPAREN;

string_array:
    LBRACKET STRING_LITERAL (COMMA STRING_LITERAL)* RBRACKET;

function:
    function_name ( argument_list )?;

function_name:
    IDENTIFIER;

argument_list:
    LPAREN argument (COMMA argument)* RPAREN;

argument:
    relative_time_literal | additive_expression | STRING_LITERAL | percent_literal | boolean_literal;

additive_expression:
    multiplicative_expression ( (PLUS|MINUS) additive_expression )?;

multiplicative_expression:
    (number_literal|metric|function) ( (MUL|DIV) multiplicative_expression )?;

number_literal:
    INTEGER_LITERAL | FLOATING_POINT_LITERAL;

relative_time_array:
    LBRACKET relative_time_literal (COMMA relative_time_literal)* RBRACKET;

relative_time_literal:
    MINUS? INTEGER_LITERAL TIME_INDICATOR;

absolute_date_literal:
    INTEGER_LITERAL MINUS INTEGER_LITERAL MINUS INTEGER_LITERAL absolute_time_literal;

absolute_time_literal:
    INTEGER_LITERAL COLON INTEGER_LITERAL (PM_INDICATOR|AM_INDICATOR)?;

percent_literal:
    MINUS? INTEGER_LITERAL REM;

boolean_literal:
    TRUE | FALSE;

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
    [shmd];

PM_INDICATOR:
    [pP][mM];

AM_INDICATOR:
    [aA][mM];

TRUE:
    'true'|'TRUE';

FALSE:
    'false'|'FALSE';

IDENTIFIER:
    [a-zA-Z][a-zA-Z0-9]*;

INTEGER_LITERAL:
    [0-9]+;

FLOATING_POINT_LITERAL:
    ([0-9]+'.'[0-9]*)|('.'[0-9]+);

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