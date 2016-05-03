grammar metrink;

graph_query:
    (relative_time_literal | absolute_date_literal | absolute_time_literal) ('to' (absolute_date_literal | absolute_time_literal) )? graph_expression;

graph_expression:
    (additive_expression)+ (connector function)*;

connector:
    '|' | '>|' | '&';

metric:
    ('metric'|'m') '(' (string_array|STRING_LITERAL) ',' (string_array|STRING_LITERAL) ',' (string_array|STRING_LITERAL) (','(relative_time_literal|relative_time_array))? ')';

string_array:
    '[' STRING_LITERAL (',' STRING_LITERAL)* ']';

function:
    function_name ( argument_list )?;

function_name:
    IDENTIFIER;

argument_list:
    '(' argument (',' argument)* ')';

argument:
    relative_time_literal | additive_expression | STRING_LITERAL | percent_literal | boolean_literal;

additive_expression:
    multiplicative_expression ( ('+'|'-') additive_expression )?;

multiplicative_expression:
    (number_literal|metric|function) ( ('*'|'/') multiplicative_expression )?;

number_literal:
    INTEGER_LITERAL | FLOATING_POINT_LITERAL;

relative_time_array:
    '[' relative_time_literal (',' relative_time_literal)* ']';

relative_time_literal:
    '-'? integer_literal relative_time_indicator;

absolute_date_literal:
    integer_literal '-' integer_literal '-' integer_literal absolute_time_literal;

absolute_time_literal:
    integer_literal ':' integer_literal (PM_INDICATOR|AM_INDICATOR)?;

percent_literal:
    '-'? integer_literal '%';

boolean_literal:
    TRUE | FALSE;

integer_literal:
    INTEGER_LITERAL;

relative_time_indicator:
    TIME_INDICATOR | 'm';

/*
 * TOKENS
 */
IDENTIFIER:
    [a-zA-Z][a-zA-Z0-9]*;

INTEGER_LITERAL:
    [0-9]+;

FLOATING_POINT_LITERAL:
    ([0-9]+'.'[0-9]*)|('.'[0-9]+);

TIME_INDICATOR:
    [shd];

PM_INDICATOR:
    [pP][mM];

AM_INDICATOR:
    [aA][mM];

TRUE:
    'true'|'TRUE';

FALSE:
    'false'|'FALSE';

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