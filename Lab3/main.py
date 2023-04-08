from analyzer import *


def br():
    """
        Prints text separator.
    """
    print('\n', '#' * 150, '\n')


def main():
    # Define the testing files name
    fileName = "main.cpp"

    # Define tables for the literals and variables
    literalTable = LiteralTable()
    variableTable = []

    try:
        lexAnalyzer = LexicalAnalyzer(fileName, literalTable, variableTable)
        lexemes = lexAnalyzer.GetLexemes()
        br()

        # Parsed lexemes
        print("\t⇒ LEXEMES:\n")
        for lexeme in lexemes:
            print('[', lexeme.coordinate_line, ':', lexeme.coordinate_offset, '] ', lexeme)
        br()

        # Parsed literals
        print("\t⇒ LITERAL TABLE:\n")
        for i in literalTable.Literals:
            print('[ Literal -', i.itemId, '] ', i)
        br()

        # Parsed variables
        print("\t⇒ VARIABLE TABLE:\n")
        for i in variableTable:
            print('[ Variable -', i.itemName, '] ', i)
        br()

    except LexicalAnalyzerError as ex:
        print(ex)


if __name__ == '__main__':
    main()
