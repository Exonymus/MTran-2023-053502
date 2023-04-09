from tools.analyzer import *


def br():
    """
        Prints text separator.
    """
    print('\n', '#' * 100, '\n')


def printLexemes(lexemes):
    """
        Beautifies the lexemes output  and prints it.
    """

    print("{:<10} {:<32} {:<20}".format('   POS', ' ' * 14 + 'TYPE', ' ' * 8 + 'VALUE'))
    print("{:<10} {:<32} {:<20}".format('-' * 10, '-' * 32, '-' * 20))

    for lexeme in lexemes:
        if lexeme.coordinate_offset < 10:
            coordinate = '[' + str(lexeme.coordinate_line) + ':0' + str(lexeme.coordinate_offset) + ']'
        else:
            coordinate = '[' + str(lexeme.coordinate_line) + ':' + str(lexeme.coordinate_offset) + ']'

        lexeme_type = str(lexeme.type)
        if lexeme.type in [Language.LexemeTypes.STRING, Language.LexemeTypes.INT_NUM, Language.LexemeTypes.DOUBLE_NUM]:
            value = 'Constant-ID: ' + str(lexeme.value)
        elif lexeme.type == Language.LexemeTypes.IDENTIFIER:
            value = 'Identifier-ID: ' + str(lexeme.value)
        else:
            value = str(lexeme.value)

        print("{:<10} {:<32} {:<20}".format(coordinate, lexeme_type, value))

    br()


def printLiterals(literals):
    """
        Beautifies the literals output and prints it.
    """

    print("{:<4} {:<32} {:<20}".format(' ID', ' ' * 14 + 'TYPE', ' ' * 8 + 'VALUE'))
    print("{:<4} {:<32} {:<20}".format('-' * 4, '-' * 32, '-' * 20))

    for literal in literals:
        literal_id = str(literal.itemId)
        literal_type = str(literal.itemType)

        if literal.itemType == LiteralTypes.STRING_CONSTANT:
            literal_value = repr(literal.itemValue)
        else:
            literal_value = str(literal.itemValue)

        print("{:<4} {:<32} {:<20}".format(literal_id, literal_type, literal_value))

    br()


def printVariables(variables):
    """
        Beautifies the variables output  and prints it.
    """

    print("{:<20} {:<32}".format(' ' * 8 + 'NAME', ' ' * 14 + 'Type'))
    print("{:<20} {:<32}".format('-' * 20, '-' * 32))

    for variable in variables:
        variable_name = str(variable.itemName)
        variable_type = str(variable.itemType)

        print("{:<20} {:<32}".format(variable_name, variable_type))

    br()


def main():
    # Define the testing files name
    fileName = "main.cpp"

    # Define tables for the literals and variables
    literalTable = LiteralTable()
    variableTable = []

    try:
        # Perform lexical analysis
        lexAnalyzer = LexicalAnalyzer(fileName, literalTable, variableTable)

        # Get resulting lexemes from the analyzer
        lexemes = lexAnalyzer.GetLexemes()
        br()

        # Parsed lexemes
        print("\t⇒ LEXEMES:\n")
        printLexemes(lexemes)

        # Parsed literals
        print("\t⇒ LITERAL TABLE:\n")
        printLiterals(literalTable.Literals)

        # Parsed variables
        print("\t⇒ VARIABLE TABLE:\n")
        printVariables(variableTable)

    except LexicalAnalyzerError as ex:
        print(ex)


if __name__ == '__main__':
    main()
