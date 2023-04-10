from core.errors import *
from core.tree import *
from core.checks import *


class Parser:
    """
        Python syntax tree parser designed to build up a syntax tree from lexemes provided.
    """

    def __init__(self, file_name, lexemes, literal_table, variable_table):
        """
            Initializes the syntax tree parser object which can build up a syntax tree from lexemes provide.
        """

        #  File provided to analysis
        self.Source = file_name

        #  Lexemes, constants and variables
        self.Lexemes = lexemes
        self.LiteralTable = literal_table
        self.VariableTable = variable_table

        # Parser variables
        self.CurrLexemeIndex = 0
        self.BlockLevel = 0
        self.BlockId = 0
        self.Scope = [(self.BlockLevel, self.BlockId)]
        self.Root = SyntaxTreeNode(None, SyntaxTreNodeTypes.CODE_BLOCK)
        # self.NestingLoop = 0

        self.ParseLexemes()

    def ParseLexemes(self):
        """
            Core function of the parser: performs the parsing of provided lexemes and building up the syntax tree.
        """

        while self.LexemesRemaining():
            node = self.ParseStatement()
            self.Root.AddChild(node)

    def ParseStatement(self):
        """
            Parses full statement to define its type and build proper node for the tree.
        """

        # Current lexeme being parsed
        lexeme = self.GetCurrentLexeme()

        if lexeme.itemType == Language.LexemeTypes.KEY_WORD:
            if lexeme.itemValue == Language.KeyWords.INCLUDE:
                return self.ParseInclude()
            elif lexeme.itemValue == Language.KeyWords.USING:
                return self.ParseUsing()
            elif IsVariableType(lexeme.itemValue) \
                    and self.GetNeighbourLexeme(1).itemType == Language.LexemeTypes.IDENTIFIER\
                    and self.GetNeighbourLexeme(2).itemValue == Language.Delimiters.OPEN_PARENTHESIS:
                return self.ParseFunctionDeclaration()
            elif IsVariableType(lexeme.itemValue):
                return self.ParseVariableDeclaration()
            else:
                raise ParserError(
                    f"unexpected lexeme: {str(lexeme)}",
                    self.Source,
                    lexeme.coordinate_line,
                    lexeme.coordinate_offset,
                )
        elif lexeme.itemType == Language.LexemeTypes.DELIMITER:
            if lexeme.itemValue == Language.Delimiters.OPEN_BRACES:
                return self.ParseBlockCode()
            else:
                raise ParserError(
                    f"unexpected lexeme: {str(lexeme)}",
                    self.Source,
                    lexeme.coordinate_line,
                    lexeme.coordinate_offset,
                )
        else:
            raise ParserError(
                f"unexpected lexeme: {str(lexeme)}",
                self.Source,
                lexeme.coordinate_line,
                lexeme.coordinate_offset,
            )

    def GetCurrentLexeme(self):
        """
            Returns the current lexeme being parsed.
        """

        if not self.LexemesRemaining():
            lexeme = self.Lexemes[self.CurrLexemeIndex - 1]
            raise ParserError("unexpected end of file", self.Source, lexeme.coordinate_offset, lexeme.coordinate_offset)
        return self.Lexemes[self.CurrLexemeIndex]

    def GetNeighbourLexeme(self, offset):
        """
            Returns the lexeme offset current being parsed.
        """

        if not self.CurrLexemeIndex + offset < len(self.Lexemes):
            lexeme = self.Lexemes[self.CurrLexemeIndex + offset]
            raise ParserError("unexpected end of file", self.Source, lexeme.coordinate_offset, lexeme.coordinate_offset)
        return self.Lexemes[self.CurrLexemeIndex + offset]

    def ParseInclude(self):
        """
            Parses an include statement.
        """

        # #include
        self.WaitForKeyword(Language.KeyWords.INCLUDE)
        include_node = SyntaxTreeNode(self.GetCurrentLexeme())

        # <
        self.NextLexeme()
        self.WaitForDelimiter(Language.Operators.LESS)

        # LIBRARY
        self.NextLexeme()
        self.WaitForIdentifier()
        library_node = SyntaxTreeNode(self.GetVariable(self.GetCurrentLexeme()))

        # >
        self.NextLexeme()
        self.WaitForDelimiter(Language.Operators.GREATER)

        self.NextLexeme()
        include_node.AddChild(library_node)

        return include_node

    def ParseUsing(self):
        """
            Parses a using statement.
        """

        # using
        self.WaitForKeyword(Language.KeyWords.USING)
        using_node = SyntaxTreeNode(self.GetCurrentLexeme())

        # namespace
        self.NextLexeme()
        self.WaitForKeyword(Language.KeyWords.NAMESPACE)
        namespace_node = SyntaxTreeNode(self.GetCurrentLexeme())

        # NAMESPACE_NAME
        self.NextLexeme()
        self.WaitForIdentifier()
        namespace_name_node = SyntaxTreeNode(self.GetVariable(self.GetCurrentLexeme()))

        # ;
        self.NextLexeme()
        self.WaitForDelimiter(Language.Delimiters.SEMICOLON)

        self.NextLexeme()
        namespace_node.AddChild(namespace_name_node)
        using_node.AddChild(namespace_node)

        return using_node

    def ParseFunctionDeclaration(self):
        """
            Parses the function declaration statement and its body.
        """

        self.EnterBlock()

        # Function type
        type_node, var_type = self.ParseVariableType()

        # Function name
        identifier_node = self.ParseDeclareIdentifier(var_type)
        self.GetVariable(identifier_node.GetLexeme()).itemBlockLevel -= 1

        # Function declaration statement
        declaration_node = SyntaxTreeNode(None, SyntaxTreNodeTypes.FUNCTION_DECLARATION)
        declaration_node.AddChild(type_node)
        declaration_node.AddChild(identifier_node)

        # (
        self.NextLexeme()

        # Function arguments
        arguments_node = SyntaxTreeNode(None, SyntaxTreNodeTypes.FUNCTION_ARGUMENTS)
        while self.GetNeighbourLexeme(-1).itemValue != Language.Delimiters.CLOSE_PARENTHESIS:
            arguments_node.AddChild(self.ParseVariableDeclaration(True))

        declaration_node.AddChild(arguments_node)

        # Function body
        declaration_node.AddChild(self.ParseBlockCode(True))

        # Exiting function scope
        self.ExitBlock()

        return declaration_node

    def ParseVariableDeclaration(self, function_declaration=False):
        """
            Parses a variable declaration statement.
        """

        # Variable type
        type_node, var_type = self.ParseVariableType()

        # Variable name
        identifier_node = self.ParseDeclareIdentifier(var_type)

        # Variable declaration statement
        declaration_node = SyntaxTreeNode(None, SyntaxTreNodeTypes.DECLARATION)
        declaration_node.AddChild(type_node)
        declaration_node.AddChild(identifier_node)

        # Expected delimiter depending on variable type
        if function_declaration is not True:
            self.WaitForDelimiter(Language.Delimiters.SEMICOLON)
        elif self.GetNeighbourLexeme(1).itemValue == Language.Delimiters.CLOSE_PARENTHESIS:
            self.WaitForDelimiter(Language.Delimiters.COMMA)
        self.NextLexeme()

        return declaration_node

    def ParseVariableType(self):
        """
            Parses a variable type statement.
        """

        type_lexeme = self.GetCurrentLexeme()
        type_node = SyntaxTreeNode(type_lexeme)
        var_type = Language.VariableTypes.UNKNOWN

        # Define correct variable type
        if self.GetNeighbourLexeme(1).itemType == Language.LexemeTypes.IDENTIFIER \
                and self.GetNeighbourLexeme(2).itemValue == Language.Delimiters.OPEN_PARENTHESIS:
            var_type = Language.VariableTypes.FUNCTION
        elif self.GetNeighbourLexeme(1).itemValue == Language.Operators.MULTIPLY:
            self.NextLexeme()
            var_type = Language.VariableTypes.POINTER
        elif self.GetNeighbourLexeme(1).itemValue == Language.Operators.BITWISE_AND:
            self.NextLexeme()
            var_type = Language.VariableTypes.REFERENCE
        elif type_lexeme.itemValue == Language.KeyWords.INT:
            var_type = Language.VariableTypes.INT
        elif type_lexeme.itemValue == Language.KeyWords.DOUBLE:
            var_type = Language.VariableTypes.DOUBLE
        elif type_lexeme.itemValue == Language.KeyWords.STRING:
            var_type = Language.VariableTypes.STRING
        elif type_lexeme.itemValue == Language.KeyWords.BOOL:
            var_type = Language.VariableTypes.BOOL
        elif type_lexeme.itemValue == Language.KeyWords.VOID:
            var_type = Language.VariableTypes.VOID
        else:
            raise ParserError("unknown variable type",
                              self.Source, type_lexeme.coordinate_line, type_lexeme.coordinate_offset)

        # Switch to variable name
        self.NextLexeme()

        return type_node, var_type

    def ParseDeclareIdentifier(self, var_type):
        """
            Parses a variable name statement.
        """

        # Check if current lexeme is a variable name
        self.WaitForIdentifier()

        lexeme = self.GetCurrentLexeme()
        node = SyntaxTreeNode(lexeme)
        curr_var = self.GetVariable(lexeme)

        # Set scope for the variable
        block_level = self.Scope[-1][0]
        block_id = self.Scope[-1][1]

        if curr_var.itemType not in [Language.VariableTypes.UNKNOWN]:
            # Check for the double declaration of the variable
            for var in self.VariableTable:
                if curr_var.name == var.name and block_id == var.block_id:
                    raise DoubleDeclarationError(curr_var.name,
                                                 self.Source, lexeme.coordinate_line, lexeme.coordinate_offset)

            self.VariableTable.append(VariableTableItem(curr_var.name, var_type, block_level, block_id))
            curr_var = self.VariableTable[-1]
            lexeme.itemValue = len(self.VariableTable) - 1

        # Setup correct variable data
        curr_var.itemType = var_type
        curr_var.itemBlockLevel = block_level
        curr_var.itemBlockId = block_id

        self.NextLexeme()

        return node

    def ParseBlockCode(self, function_declaration=False):
        """
            Parses a block of code.
        """

        # Check for the '{'
        self.WaitForDelimiter(Language.Delimiters.OPEN_BRACES)
        self.NextLexeme()

        # If we outside the function declaration open new scope
        if not function_declaration:
            self.EnterBlock()

        code_block_node = SyntaxTreeNode(None, SyntaxTreNodeTypes.CODE_BLOCK)

        # Parse the lexemes of the block
        while self.LexemesRemaining() and \
                self.GetCurrentLexeme().itemValue != Language.Delimiters.CLOSE_BRACES:
            code_block_node.AddChild(self.ParseStatement())

        # Check for the '}'
        self.WaitForDelimiter(Language.Delimiters.CLOSE_BRACES)
        self.NextLexeme()

        # If we outside the function declaration close new scope
        if not function_declaration:
            self.ExitBlock()

        return code_block_node

    def PrintSyntaxTree(self):
        """
            Prints the syntax tree.
        """

        printSyntaxTree(self.Root)

    def GetTree(self):
        """
            Returns the syntax tree root.
        """

        return self.Root

    def NextLexeme(self):
        """
            Switches parser focus to the next lexeme.
        """

        self.CurrLexemeIndex += 1

    def WaitForKeyword(self, key_word):
        """
            Checks current lexeme if it is a keyword.
        """

        lexeme = self.GetCurrentLexeme()
        if lexeme.itemValue != key_word:
            raise ExpectedError(str(key_word), self.Source, lexeme.coordinate_line, lexeme.coordinate_offset)

    def WaitForDelimiter(self, delimiter):
        """
            Checks current lexeme if it is a delimiter.
        """

        lexeme = self.GetCurrentLexeme()
        if lexeme.itemValue != delimiter:
            raise ExpectedError(str(delimiter), self.Source, lexeme.coordinate_line, lexeme.coordinate_offset)

    def WaitForOperator(self, operator):
        """
            Checks current lexeme if it is an operator.
        """

        lexeme = self.GetCurrentLexeme()
        if lexeme.itemValue != operator:
            raise ExpectedError(str(operator), self.Source, lexeme.coordinate_line, lexeme.coordinate_offset)

    def WaitForVariableType(self, lexeme, type):
        """
            Checks current lexeme if it is a variable type.
        """

        if lexeme.itemType != Language.LexemeTypes.IDENTIFIER:
            raise ExpectedError(
                f"{str(type)} variable",
                self.Source,
                lexeme.coordinate_line,
                lexeme.coordinate_offset,
            )
        var = self.GetVariable(lexeme)
        if isinstance(type, Language.VariableTypes):
            if var.itemType != type:
                raise ExpectedError(
                    f"{str(type)} variable",
                    self.Source,
                    lexeme.coordinate_line,
                    lexeme.coordinate_offset,
                )
        elif var.itemType not in type:
            raise ExpectedError(
                f"one of the following variable types: {str(type)}",
                self.Source,
                lexeme.coordinate_line,
                lexeme.coordinate_offset,
            )

    def WaitForIdentifier(self):
        """
            Checks current lexeme if it is an identifier.
        """

        lexeme = self.GetCurrentLexeme()
        if lexeme.itemType != Language.LexemeTypes.IDENTIFIER:
            raise ExpectedError("identifier", self.Source, lexeme.coordinate_line, lexeme.coordinate_offset)

    def LexemesRemaining(self):
        """
            Checks if there are any remaining lexemes.
        """

        return self.CurrLexemeIndex < len(self.Lexemes)

    def GetVariable(self, lexeme):
        """
            Returns the variable associated with the lexeme.
        """

        return self.VariableTable[lexeme.itemValue]

    def EnterBlock(self):
        """
            Change scope values for the entering code block.
        """

        self.BlockLevel += 1
        self.BlockId += 1
        self.Scope.append((self.BlockLevel, self.BlockId))

    def ExitBlock(self):
        """
            Change scope values for the exiting code block.
        """

        self.BlockLevel -= 1
        self.Scope.pop()
            