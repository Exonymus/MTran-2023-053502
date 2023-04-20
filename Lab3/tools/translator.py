import types
import inspect
import ast

import astor

from core.checks import *
from core.tree import *


def CreateFunctionObj(name, args):
    """
        Creates a new function object from the given data.
    """

    # Build function signature string from arg_types
    args_str = ", ".join(args)
    function_str = f"def {name}({args_str}): pass"

    # Compile function
    compiled_func = compile(function_str, "<string>", "exec")
    func_code = next((c for c in compiled_func.co_consts if isinstance(c, types.CodeType)), None)

    # Creation error handler
    if func_code is None:
        raise ValueError("Unable to find function code object.")

    return types.FunctionType(func_code, globals(), name)


def UpdateFuncCode(func, new_code):
    """
        Updates provided function object's code with new instructions.
    """

    # Get function source code
    source = inspect.getsource(func)

    # Build AST from source code
    tree = ast.parse(source)

    # Append new code to AST
    new_code_node = ast.parse(new_code).body
    tree.body[0].body += new_code_node

    # Convert AST back to source code
    new_source = astor.to_source(tree)

    return type(func)(
        compile(new_source, "<string>", "exec").co_consts[0], func.__globals__
    )


class Translator:
    """
        CPP to Python translator.
    """

    def __init__(self, tree_root, literal_table, variable_table):
        """
            Initializes the translator object which can parse CPP AST and translate it to Python.
        """

        # Tree provided to translation
        self.Tree = tree_root

        # Environment, constants and variables
        self.LiteralTable = literal_table
        self.VariableTable = variable_table

        self.Translate()

    def Translate(self):
        """
            Core function of the translator: parses the function from AST and translates them to python in order to use.
        """

        if self.Tree is None:
            return

        children = self.Tree.GetChildren()

        for child in children:
            if child.Type == SyntaxTreNodeTypes.FUNCTION_DECLARATION:
                func_nodes = child.GetChildren()

                # Get function name
                func_name = self.GetVariable(func_nodes[1].GetLexeme().itemValue).itemName

                # Get function arguments
                func_args = self.GetFunctionArguments(func_nodes[2])

                # Get function object
                function_obj = CreateFunctionObj(func_name, func_args)

                # Fill function body with code
                body_instructions_nodes = func_nodes[3].GetChildren()
                # printSyntaxTree(func_nodes[3])
                for instruction_node in body_instructions_nodes:
                    if not instruction_node:
                        continue
                    new_code = self.ParseInstruction(instruction_node, 1)
                    print(new_code)
                    # UpdateFuncCode(function_obj, new_code)
                # Assign function object to global scope
                globals()[func_name] = function_obj

        # Call main function
        globals()["main"]()

    def GetFunctionArguments(self, node):
        """
            Parses function arguments node to get arguments in 'Python' form.
        """

        arguments = []

        for arg in node.GetChildren():
            arg_children = arg.GetChildren()

            variable = self.GetVariable(arg_children[1].GetLexeme().itemValue)

            arg_type = None

            if isinstance(variable.itemType, list):
                arg_type = "list"
            else:
                arg_type = self.GetArgType(variable.itemType)

            if arg_type is not None:
                arg_name = variable.itemName
                arguments.append(f"{arg_name}: {arg_type}")
            else:
                raise ValueError("Function argument type error")

        return arguments


    def GetArgType(self, arg_type):
        """
            Parses arguments CPP type to Python type.
        """

        if arg_type == Language.VariableTypes.INT:
            return "int"
        elif arg_type == Language.VariableTypes.STRING:
            return "str"
        elif arg_type == Language.VariableTypes.BOOL:
            return "bool"
        elif arg_type == Language.VariableTypes.DOUBLE:
            return "float"

    def GetVariable(self, variable_id):
        variable = None

        try:
            variable = [v for v in self.VariableTable if v.itemId == variable_id][0]
        except:
            raise ValueError("Bad variable id")

        return variable

    def GetLiteral(self, literal_id):
        literal = None

        try:
            literal = [v for v in self.LiteralTable.Literals if v.itemId == literal_id][0]
        except:
            raise ValueError("Bad variable id")

        return literal

    def ParseInstruction(self, instruction_node, level):
        """
            Parses given instruction node.
        """

        instruction = None
        lexeme = None

        if instruction_node.Type == SyntaxTreNodeTypes.COMMON:
            lexeme = instruction_node.GetLexeme()

        if instruction_node.Type == SyntaxTreNodeTypes.DECLARATION:
            instruction = str(self.ParseVariableDeclaration(instruction_node, level))
        elif instruction_node.Type == SyntaxTreNodeTypes.FUNCTION_CALL:
            instruction = str(self.ParseFunctionCall(instruction_node, level))
        elif lexeme and lexeme.itemValue == Language.Operators.EQUAL:
            instruction = str(self.ParseOperator(instruction_node, level))
        elif lexeme and lexeme.itemValue == Language.KeyWords.IF:
            instruction = str(self.ParseIfStatement(instruction_node, level))
        elif lexeme and lexeme.itemValue == Language.KeyWords.WHILE:
            instruction = str(self.ParseWhileStatement(instruction_node, level))
        elif lexeme and lexeme.itemValue == Language.KeyWords.DO:
            instruction = str(self.ParseDoWhileStatement(instruction_node, level))
        elif lexeme and lexeme.itemValue in [Language.Operators.INCREMENT, Language.Operators.DECREMENT]:
            instruction = str(self.ParseUnaryOperatorStatement(instruction_node, level))
        elif lexeme and lexeme.itemValue == Language.KeyWords.CIN:
            instruction = str(self.ParseCin(instruction_node, level))
        elif lexeme and lexeme.itemValue == Language.KeyWords.COUT:
            instruction = str(self.ParseCout(instruction_node, level))

        if instruction is not None:
            return  instruction

    def ParseOperator(self, operator_node, level):

        parts = []
        operator = None
        current_level = level * '\t'

        if operator_node.GetLexeme().itemType == Language.LexemeTypes.IDENTIFIER:
            return str(self.GetVariable(operator_node.GetLexeme().itemValue).itemName)
        elif operator_node.GetLexeme().itemType == Language.LexemeTypes.INT_NUM:
            return str(self.GetLiteral(operator_node.GetLexeme().itemValue).itemValue)

        try:
            operator = inverted_operators[operator_node.GetLexeme().itemValue]
        except:
            raise ValueError("Unknown operator")

        for node in operator_node.GetChildren():
            lexeme = node.GetLexeme()
            part = None

            if not node.GetChildren():
                if lexeme.itemType == Language.LexemeTypes.IDENTIFIER:
                    part = str(self.GetVariable(lexeme.itemValue).itemName)
                elif lexeme.itemType in [Language.LexemeTypes.INT_NUM, Language.LexemeTypes.DOUBLE_NUM,
                                         Language.LexemeTypes.STRING]:
                    part = str(self.GetLiteral(lexeme.itemValue).itemValue)
            elif lexeme.itemType == Language.LexemeTypes.IDENTIFIER:
                var_name = str(self.GetVariable(lexeme.itemValue).itemName)
                part = f"{var_name}[{self.ParseOperator(node.GetChildren()[0], 0)}]"
            elif IsOperator(operator):
                part = f"({self.ParseOperator(node, level)})"

            if part is not None:
                parts.append(part)
            else:
                raise ValueError("Bad operating part")

        return current_level + str(operator).join(parts)

    def ParseVariableDeclaration(self, declaration_node, level):

        declarations = []
        current_level = level * '\t'

        for node in declaration_node.GetChildren()[1:]:
            lexeme = node.GetLexeme()

            declaration = None
            if not node.GetChildren():
                if lexeme.itemType == Language.LexemeTypes.IDENTIFIER:
                    variable = str(self.GetVariable(lexeme.itemValue).itemName)
                    declaration = f"{current_level}{variable}=None"
            elif lexeme.itemType == Language.LexemeTypes.IDENTIFIER:
                var_name = str(self.GetVariable(lexeme.itemValue).itemName)
                var_len = self.ParseOperator(node.GetChildren()[0], 0)
                declaration = f"{current_level}{var_name}=list(None for _ in range({var_len}))"
            elif lexeme.itemValue == Language.Operators.EQUAL:
                declaration = f"{self.ParseOperator(node, level)}"
            if declaration is not None:
                declarations.append(declaration)
            else:
                raise ValueError("Unknown declaration")

        return "\n".join(declarations)

    def ParseIfStatement(self, if_node, level):

        current_level = level * '\t'
        condition_node = if_node.GetChildren()[0]

        code_node = if_node.GetChildren()[1]
        instructions = [self.ParseInstruction(instruction, level + 1) for instruction in code_node.GetChildren()]
        code_block = '\n'.join(instructions)

        return f"{current_level}if {self.ParseOperator(condition_node, 0)}:\n{code_block}"

    def ParseFunctionCall(self, call_node, level):

        current_level = level * '\t'

        function_name = self.GetVariable(call_node.GetChildren()[0].GetLexeme().itemValue).itemName
        arguments = [self.GetVariable(arg.GetLexeme().itemValue).itemName
                     for arg in call_node.GetChildren()[1].GetChildren()]

        return f"{current_level}globals()['{function_name}']({','.join(arguments)})"

    def ParseWhileStatement(self, while_node, level):

        current_level = level * '\t'
        condition_node = while_node.GetChildren()[0]

        code_node = while_node.GetChildren()[1]
        instructions = [self.ParseInstruction(instruction, level + 1) for instruction in code_node.GetChildren()]
        code_block = '\n'.join(instructions)

        return f"{current_level}while {self.ParseOperator(condition_node, 0)}:\n{code_block}"

    def ParseDoWhileStatement(self, doWhile_node, level):

        current_level = level * '\t'
        condition_node = doWhile_node.GetChildren()[1].GetChildren()[0]
        # printSyntaxTree(condition_node)

        code_node = doWhile_node.GetChildren()[0]
        instructions_out = [self.ParseInstruction(instruction, level) for instruction in code_node.GetChildren()]
        instructions_in = [self.ParseInstruction(instruction, level + 1) for instruction in code_node.GetChildren()]

        code_block_out = '\n'.join(instructions_out)
        code_block_in = '\n'.join(instructions_in)

        return f"{current_level}{code_block_out}" \
               f"\n{current_level}while {self.ParseOperator(condition_node, 0)}:\n{code_block_in}"

    def ParseUnaryOperatorStatement(self, unary_node, level):

        current_level = level * '\t'
        var_name = str(self.GetVariable(unary_node.GetChildren()[0].GetLexeme().itemValue).itemName)

        if unary_node.GetLexeme().itemValue == Language.Operators.INCREMENT:
            return f"{current_level}{var_name}+=1"
        elif unary_node.GetLexeme().itemValue == Language.Operators.DECREMENT:
            return f"{current_level}{var_name}-=1"

    def ParseCin(self, cin_node, level):

        current_level = level * '\t'
        children = cin_node.GetChildren()
        instructions = []

        for node in children:
            lexeme = node.GetLexeme()
            instruction = None

            if not node.GetChildren():
                if lexeme.itemType == Language.LexemeTypes.IDENTIFIER:
                    instruction = f"{current_level}input({str(self.GetVariable(lexeme.itemValue).itemName)})"
            elif lexeme.itemType == Language.LexemeTypes.IDENTIFIER:
                var_name = str(self.GetVariable(lexeme.itemValue).itemName)
                var_len = self.ParseOperator(node.GetChildren()[0], 0)
                instruction = f"{current_level}input({var_name}[{var_len}])"
            if instruction is not None:
                instructions.append(instruction)
            else:
                print(lexeme)
                raise ValueError("Bad arg to input")

        return '\n'.join(instructions)



    def ParseCout(self, cout_node, level):

        current_level = level * '\t'
        children = cout_node.GetChildren()
        messages = []

        for node in children:
            lexeme = node.GetLexeme()
            message = None

            if not node.GetChildren():
                if lexeme.itemType == Language.LexemeTypes.IDENTIFIER:
                    message = str(self.GetVariable(lexeme.itemValue).itemName)
                elif lexeme.itemType in [Language.LexemeTypes.INT_NUM, Language.LexemeTypes.DOUBLE_NUM]:
                    message = str(self.GetLiteral(lexeme.itemValue).itemValue)
                elif lexeme.itemType == Language.LexemeTypes.STRING:
                    message = repr(self.GetLiteral(lexeme.itemValue).itemValue)
                elif lexeme.itemValue == Language.KeyWords.ENDL:
                    message = repr("\n")
            elif lexeme.itemType == Language.LexemeTypes.IDENTIFIER:
                var_name = str(self.GetVariable(lexeme.itemValue).itemName)
                var_len = self.ParseOperator(node.GetChildren()[0], 0)
                message = f"{var_name}[{var_len}]"
            if message is not None:
                messages.append(message)
            else:
                print(lexeme)
                raise ValueError("Bad arg to print")

        return f"{current_level}print({','.join(messages)})"


