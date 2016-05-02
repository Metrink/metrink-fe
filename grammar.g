parser MetrinkParser:
    ignore: '[ \r\t\n]+'  # don't care about spaces

    token END: "$"

    # these are our reserved words
    token METRIC: "metric"
    token M: "m"
    token TRUE: "(true)|(TRUE)"
    token FALSE: "(false)|(FALSE)"

    # reserved symbols
    token LPAREN: "\\("
    token RPAREN: "\\)"
    token LBRACE: "{"
    token RBRACE: "}"
    token LBRACKET: "\\["
    token RBRACKET: "]"
    token COLON: ":"
    token SEMICOLON: ";"
    token COMMA: ","
    token DOT: "."
    token AT: "@"

    # operators
    token ASSIGN: "="
    token LT: "<"
    token GT: ">"
    token BANG: "!"
    token EQ: "=="
    token LE: "<="
    token GE: ">="
    token NE: "!="
    token OR: "or"
    token DOUBLE_PIPE: "||"
    token AND: "and"
    token DOUBLE_AMP: "&&"
    token INCR: "\\+\\+"
    token DECR: "--"
    token PLUS: "\\+"
    token MINUS: "-"
    token STAR: "\\*"
    token SLASH: "/"
    token REM: "%"
    token PLUSASSIGN: "\\+="
    token MINUSASSIGN: "-="
    token STARASSIGN: "\\*="
    token SLASHASSIGN: "/="
    token REMASSIGN: "%="
    token PIPE: "|"
    token COPY_PIPE: ">|"
    token AMP: "&"

    # quotes
    token SINGLE_QUOTE: "'"
    token DOUBLE_QUOTE: "\""

    # literals
    token INTEGER_LITERAL: "[0-9]+"
    token FLOATING_POINT_LITERAL: "([0-9]+\.[0-9]*)|(\.[0-9]+)"

    token SINGLE_QUOTE_STRING_LITERAL: "'(~[\\\n\r'`\u2018\u2019\u201B\u2032\u2035])*'"
    token DOUBLE_QUOTE_STRING_LITERAL: "\"(~[\\\n\r'`\u2018\u2019\u201B\u2032\u2035])*\""

    token TIME_INDICATOR: "[smhd]"
    token PM_INDICATOR: "[pP][mM]"
    token AM_INDICATOR: "[aA][mM]"

    token IDENTIFIER: "[a-zA-Z][a-zA-Z0-9]*"

    #
    # Rules of the grammar start here
    #
    rule graph_expression:
        (additive_expression)+ (connector function)* END {{ return 'graph_expression' }}

    rule connector:
        PIPE | COPY_PIPE | AMP

    rule metric:
        (METRIC|M) LPAREN (string_array|string_literal) "," (string_array|string_literal) "," (string_array|string_literal) [","(relative_time_literal|relative_time_array)] RPAREN

    rule string_array:
        LBRACKET string_literal (","string_literal)* RBRACKET

    rule function:
        function_name [ argument_list ]

    rule function_name:
        IDENTIFIER
        {{ return IDENTIFIER }}

    rule argument_list:
        LPAREN argument ("," argument)* RPAREN

    rule argument:
        relative_time_literal | additive_expression | string_literal | percent_literal | boolean_literal

    rule additive_expression:
        multiplicative_expression [ (PLUS|MINUS) additive_expression ]

    rule multiplicative_expression:
        (number_literal|metric|function) [ (STAR|SLASH) multiplicative_expression ]

    rule string_literal:
        SINGLE_QUOTE_STRING_LITERAL | DOUBLE_QUOTE_STRING_LITERAL

    rule number_literal:
        INTEGER_LITERAL | FLOATING_POINT_LITERAL

    rule relative_time_array:
        LBRACKET relative_time_literal ("," relative_time_literal)* RBRACKET

    rule relative_time_literal:
        [MINUS] integer_literal relative_time_indicator

    rule absolute_date_literal:
        integer_literal MINUS integer_literal MINUS integer_literal absolute_time_literal

    rule absolute_time_literal:
        integer_literal COLON integer_literal (PM_INDICATOR|AM_INDICATOR)?

    rule percent_literal:
        [MINUS] integer_literal REM

    rule boolean_literal:
        TRUE {{ return True }} | FALSE {{ return False }}

    rule integer_literal:
        INTEGER_LITERAL {{ return INTEGER_LITERAL }}

    rule relative_time_indicator:
        TIME_INDICATOR | M
