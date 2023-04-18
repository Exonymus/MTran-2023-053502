from core.errors import *
from core.tree import *


class SemanticParser:
    """
        Python semantic analyzer designed to perform syntax tree analysis.
    """

    def __init__(self, file_name, tree_root, literal_table, variable_table):
        """
            Initializes the semantic parser object which can parse syntax tree and define its problems.
        """

        # File provided to analysis
        self.Source = file_name
        self.Tree = tree_root

        # Environment, constants and variables
        self.LiteralTable = literal_table
        self.VariableTable = variable_table
        self.Environment = {
            "Libraries": [],
            "Namespaces": [],
            "Functions": {},
            "Variables": {}
        }

        self.AnalyzeTree(self.Tree)

    def AnalyzeTree(self, node):
        """
            Analyzes the given node and searches for semantic errors.
        """

        # Check if we meet dead-end
        if node is None:
            return

        # Get lexeme children if there are
        children = node.GetChildren()

        # Update parser environment using tree node
        self.UpdateEnvironment(node)

        # Define parser behaviour
        if node.GetLexeme() is not None:

            # Check for cout / cin
            if node.GetLexeme().itemValue in [Language.KeyWords.CIN, Language.KeyWords.COUT]:
                if not self.Environment["Libraries"].__contains__("iostream"):
                    raise SemanticError("iostream library required.", self.Source,
                                         node.GetLexeme().coordinate_line, node.GetLexeme().coordinate_offset)
                if not self.Environment["Namespaces"].__contains__("std"):
                    raise SemanticError("std namespace required.", self.Source,
                                         node.GetLexeme().coordinate_line, node.GetLexeme().coordinate_offset)

            # Check for using undefined var in assignment and cout
            if node.GetLexeme().itemValue == Language.Operators.EQUAL:
                right_part = children[len(children) - 1].GetLexeme()
                if right_part.itemType == Language.LexemeTypes.IDENTIFIER:
                    self.CheckForDefined(right_part)
            elif node.GetLexeme().itemValue == Language.KeyWords.COUT:
                for child in children:
                    ch_lexeme = child.GetLexeme()
                    if ch_lexeme.itemType == Language.LexemeTypes.IDENTIFIER:
                        self.CheckForDefined(ch_lexeme)



            # TODO: Check for array index
            # TODO: Check for function call argument
            # TODO: Check for arithmetics

        # Check function call
        elif node.Type == SyntaxTreNodeTypes.FUNCTION_CALL:
            function_name = self.VariableTable[children[0].GetLexeme().itemValue].itemName
            arguments_node = children[1].GetChildren()

            # Check valid amount of arguments
            if len(arguments_node) != len(self.Environment["Functions"][function_name]["Arguments"]):
                if len(arguments_node) > len(self.Environment["Functions"][function_name]["Arguments"]):
                    len_err = "many"
                else:
                    len_err = "few"
                raise SemanticError(f"Too {len_err} arguments to function {function_name}", self.Source,
                                    arguments_node[0].GetLexeme().coordinate_line,
                                    arguments_node[0].GetLexeme().coordinate_offset)

            for i in range(len(arguments_node)):
                argument = arguments_node[i].GetLexeme()

                if argument.itemType == Language.LexemeTypes.IDENTIFIER:
                    # Check if argument is defined
                    self.CheckForDefined(argument)

                    # Check if argument has valid type
                    self.CheckArgumentType(function_name, argument, i)



        for child in children:
            self.AnalyzeTree(child)

    def UpdateEnvironment(self, node):
        """
            Updates semantic parser environment using info from tree nods.
        """

        # Get lexeme children if there are
        children = node.GetChildren()

        if node.GetLexeme() is not None:
            # Add libraries to parser environment
            if node.GetLexeme().itemValue == Language.KeyWords.INCLUDE:
                self.Environment["Libraries"].append(self.VariableTable[children[0].GetLexeme().itemValue].itemName)

            # Add namespaces to parser environment
            if node.GetLexeme().itemValue == Language.KeyWords.NAMESPACE:
                self.Environment["Namespaces"].append(self.VariableTable[children[0].GetLexeme().itemValue].itemName)

            if node.GetLexeme().itemValue == Language.Operators.EQUAL:
                for i in range(len(children)):
                    if children[i].GetLexeme().itemType == Language.LexemeTypes.IDENTIFIER and i != len(children) - 1:
                        variable = self.VariableTable[children[i].GetLexeme().itemValue]
                        variable_name = f"{str(variable.itemName)} " \
                                        f"[{str(variable.itemBlockId)}:{str(variable.itemBlockLevel)}]"
                        self.Environment["Variables"][variable_name] = "defined"


        else:
            # Add functions to parser environment
            if node.Type == SyntaxTreNodeTypes.FUNCTION_DECLARATION:
                arguments_node = children[2]
                arguments = []
                if arguments_node.GetChildren():
                    for arg in arguments_node.GetChildren():
                        variable = self.VariableTable[arg.GetChildren()[1].GetLexeme().itemValue]
                        arguments.append(variable.itemType)

                        variable_name = f"{str(variable.itemName)} " \
                                        f"[{str(variable.itemBlockId)}:{str(variable.itemBlockLevel)}]"
                        self.Environment["Variables"][variable_name] = "defined"
                function_name = self.VariableTable[children[1].GetLexeme().itemValue].itemName
                function_info = {
                    "Type": children[0].GetLexeme().itemValue,
                    "Arguments": arguments
                }

                self.Environment["Functions"][function_name] = function_info

    def CheckForDefined(self, lexeme):
        """
            Checks if variable initialized.
        """

        variable = self.VariableTable[lexeme.itemValue]
        variable_name = f"{str(variable.itemName)} " \
                        f"[{str(variable.itemBlockId)}:{str(variable.itemBlockLevel)}]"
        if self.Environment["Variables"].get(variable_name) is None:
            raise VariableUndefinedError(variable.itemName, self.Source,
                                         lexeme.coordinate_line, lexeme.coordinate_offset)

    def CheckArgumentType(self, function_name, argument, pos):
        """
            Checks function call statement.
        """

        required_type = self.Environment["Functions"][function_name]["Arguments"][pos]
        argument_type = self.VariableTable[argument.itemValue].itemType

        if isinstance(argument_type, list) and isinstance(required_type, list):
            if argument_type[1] != required_type[1]:
                raise FunctionArgumentError(required_type, self.Source,
                                            argument.coordinate_line, argument.coordinate_offset)

            if argument_type[0] != required_type[0]:
                if argument_type[0] == Language.VariableTypes.ARRAY \
                        and required_type[0] == Language.VariableTypes.POINTER:
                    return
                else:
                    raise FunctionArgumentError(required_type, self.Source,
                                                argument.coordinate_line, argument.coordinate_offset)
        elif argument_type != required_type:
            raise FunctionArgumentError(required_type, self.Source,
                                        argument.coordinate_line, argument.coordinate_offset)

    def CheckArithmetic(self, node):
        """
            Checks arithmetic problems in provided syntax tree node.
        """

        if node is None:
            return
