from dataclasses import dataclass
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
        MODULO_ASSIGN = 9
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
        MODULO = 26
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


key_words = {
    'int': Language.KeyWords.INT,
    'double': Language.KeyWords.DOUBLE,
    'bool': Language.KeyWords.BOOL,
    'string': Language.KeyWords.STRING,
    'void': Language.KeyWords.VOID,
    'true': Language.KeyWords.TRUE,
    'false': Language.KeyWords.FALSE,
    'nullptr': Language.KeyWords.NULLPTR,
    'while': Language.KeyWords.WHILE,
    'continue': Language.KeyWords.CONTINUE,
    'break': Language.KeyWords.BREAK,
    'if': Language.KeyWords.IF,
    'else': Language.KeyWords.ELSE,
    'print': Language.KeyWords.PRINT,
    'scan': Language.KeyWords.SCAN,
    'to_string': Language.KeyWords.TO_STRING,
    'auto': Language.KeyWords.AUTO,
    'case': Language.KeyWords.CASE,
    'const': Language.KeyWords.CONST,
    'default': Language.KeyWords.DEFAULT,
    'do': Language.KeyWords.DO,
    'enum': Language.KeyWords.ENUM,
    'extern': Language.KeyWords.EXTERN,
    'for': Language.KeyWords.FOR,
    'goto': Language.KeyWords.GOTO,
    'register': Language.KeyWords.REGISTER,
    'return': Language.KeyWords.RETURN,
    'sizeof': Language.KeyWords.SIZEOF,
    'static': Language.KeyWords.STATIC,
    'struct': Language.KeyWords.STRUCT,
    'typedef': Language.KeyWords.TYPEDEF,
    'union': Language.KeyWords.UNION,
    'volatile': Language.KeyWords.VOLATILE,
    '#include': Language.KeyWords.INCLUDE,
    'using': Language.KeyWords.USING,
    'namespace': Language.KeyWords.NAMESPACE,
    'cin': Language.KeyWords.CIN,
    'cin::': Language.KeyWords.CIN,
    'cout': Language.KeyWords.COUT,
    'cout::': Language.KeyWords.COUT,
    'stoi': Language.KeyWords.STOI,
    'stod': Language.KeyWords.STOD,
    'exit': Language.KeyWords.EXIT,
}

delimiters = {
    '(': Language.Delimiters.OPEN_PARENTHESIS,
    ')': Language.Delimiters.CLOSE_PARENTHESIS,
    ',': Language.Delimiters.COMMA,
    ';': Language.Delimiters.SEMICOLON,
    '{': Language.Delimiters.OPEN_BRACES,
    '}': Language.Delimiters.CLOSE_BRACES,
    '[': Language.Delimiters.LEFT_BRACKET,
    ']': Language.Delimiters.RIGHT_BRACKET
}

operators = {
    '++': Language.Operators.INCREMENT,
    '--': Language.Operators.DECREMENT,
    '==': Language.Operators.DOUBLE_EQUAL,
    '!=': Language.Operators.NOT_EQUAL,
    '<=': Language.Operators.LESS_EQUAL,
    '>': Language.Operators.GREATER,
    '>=': Language.Operators.GREATER_EQUAL,
    '*=': Language.Operators.MULTIPLY_ASSIGN,
    '/=': Language.Operators.DIVIDE_ASSIGN,
    '%=': Language.Operators.MODULO_ASSIGN,
    '&=': Language.Operators.BITWISE_AND_ASSIGN,
    '|=': Language.Operators.BITWISE_OR_ASSIGN,
    '&&': Language.Operators.LOGICAL_AND,
    '||': Language.Operators.LOGICAL_OR,
    '&': Language.Operators.BITWISE_AND,
    '|': Language.Operators.BITWISE_OR,
    '^': Language.Operators.BITWISE_XOR,
    '~': Language.Operators.BITWISE_NOT,
    '<<': Language.Operators.LEFT_SHIFT,
    '>>': Language.Operators.RIGHT_SHIFT,
    '+=': Language.Operators.ADD_ASSIGN,
    '-=': Language.Operators.SUBTRACT_ASSIGN,
    '<': Language.Operators.LESS,
    '*': Language.Operators.MULTIPLY,
    '/': Language.Operators.SLASH,
    '//': Language.Operators.DOUBLE_SLASH,
    '%': Language.Operators.MODULO,
    '+': Language.Operators.PLUS,
    '-': Language.Operators.MINUS,
    '!': Language.Operators.NOT,
    '=': Language.Operators.EQUAL
}


@dataclass()
class LexTableItem:
    type: Language.LexemeTypes
    value: int or Language.KeyWords or Language.Delimiters or Language.Operators
    coordinate_line: int
    coordinate_offset: int


class LiteralTypes(Enum):
    INT_CONSTANT = 1
    DOUBLE_CONSTANT = 2
    STRING_CONSTANT = 3


class VariableTypes(Enum):
    UNKNOWN = 0
    INT = 1
    DOUBLE = 2
    STRING = 3
    BOOL = 4
    ARRAY = 5
    NAMESPACE = 6
    FUNCTION = 7


def IsKeyword(lexeme) -> bool:
    return lexeme in key_words


def IsDelimiter(lexeme) -> bool:
    return lexeme in delimiters


def IsOperator(lexeme) -> bool:
    return lexeme in operators


def IsWhitespace(whitespace) -> bool:
    return whitespace == ' ' \
        or whitespace == '\n' \
        or whitespace == '\t'


def IsEOF(EOF) -> bool:
    return EOF == ''


def GetEscSeq(ch: str) -> str:
    if ch == 'a':
        return '\a'
    elif ch == 'b':
        return '\b'
    elif ch == 'f':
        return '\f'
    elif ch == 'n':
        return '\n'
    elif ch == 'r':
        return '\r'
    elif ch == 't':
        return '\t'
    elif ch == 'v':
        return '\v'
    elif ch == "'":
        return "\'"
    elif ch == '"':
        return '\"'
    elif ch == '\\':
        return '\\'
    else:
        raise ValueError("No such escape sequence")
