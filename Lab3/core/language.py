from enum import Enum


class Language:
    class LexemeTypes(Enum):
        KEY_WORD = 0
        IDENTIFIER = 1
        DELIMITER = 2
        OPERATOR = 3
        INT_NUM = 4
        DOUBLE_NUM = 5
        STRING = 6

    class States(Enum):
        START = 0
        END = 1
        ERROR = 2
        ONE_LINE_COMMENT = 3
        ID_OR_KEY_WORD = 4
        NUMBER = 5
        STRING = 6
        OPERATOR = 7
        DELIMITER = 8

    class KeyWords(Enum):
        INT = 0
        DOUBLE = 1
        STRING = 2
        BOOL = 3
        TRUE = 4
        FALSE = 5
        VOID = 6
        NULLPTR = 7
        WHILE = 8
        CONTINUE = 9
        BREAK = 10
        IF = 11
        ELSE = 12
        PRINT = 13
        SCAN = 14
        TO_STRING = 15
        AUTO = 16
        CASE = 17
        CONST = 18
        DEFAULT = 19
        DO = 20
        ENUM = 21
        EXTERN = 22
        FOR = 23
        GOTO = 24
        REGISTER = 25
        RETURN = 26
        SIZEOF = 27
        STATIC = 28
        STRUCT = 29
        TYPEDEF = 30
        UNION = 31
        VOLATILE = 32
        INCLUDE = 33
        USING = 34
        NAMESPACE = 35
        CIN = 37
        COUT = 38
        STOI = 39
        STOD = 40
        EXIT = 41

    class Operators(Enum):
        INCREMENT = 0
        DECREMENT = 1
        DOUBLE_EQUAL = 2
        NOT_EQUAL = 3
        LESS_EQUAL = 4
        GREATER = 5
        GREATER_EQUAL = 6
        MULTIPLY_ASSIGN = 7
        DIVIDE_ASSIGN = 8
        PERCENT_ASSIGN = 9
        BITWISE_AND_ASSIGN = 10
        BITWISE_OR_ASSIGN = 11
        LOGICAL_AND = 12
        LOGICAL_OR = 13
        BITWISE_AND = 14
        BITWISE_OR = 15
        BITWISE_XOR = 16
        BITWISE_NOT = 17
        LEFT_SHIFT = 18
        RIGHT_SHIFT = 19
        ADD_ASSIGN = 20
        SUBTRACT_ASSIGN = 21
        LESS = 22
        MULTIPLY = 23
        SLASH = 24
        DOUBLE_SLASH = 25
        PERCENT = 26
        PLUS = 27
        MINUS = 28
        NOT = 29
        EQUAL = 30

    class Delimiters(Enum):
        OPEN_PARENTHESIS = 0
        CLOSE_PARENTHESIS = 1
        COMMA = 2
        SEMICOLON = 3
        OPEN_BRACES = 4
        CLOSE_BRACES = 5
        LEFT_BRACKET = 6
        RIGHT_BRACKET = 7

    class VariableTypes(Enum):
        UNKNOWN = 0
        INT = 1
        DOUBLE = 2
        STRING = 3
        BOOL = 4
        ARRAY = 5
        NAMESPACE = 6
        FUNCTION = 7

    class LiteralTypes(Enum):
        INT_CONSTANT = 1
        DOUBLE_CONSTANT = 2
        STRING_CONSTANT = 3

    class ExpressionTypes(Enum):
        ARITHMETIC = 0
        BOOL = 1
        STRING = 2

    class ComparisonTypes(Enum):
        ARITHMETIC = 0
        STRING = 1
