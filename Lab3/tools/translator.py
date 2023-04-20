import types
import inspect
import ast

import astor

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
                var_id = func_nodes[1].GetLexeme().itemValue
                func_name = [v for v in self.VariableTable if v.itemId == var_id][0].itemName

                # Get function arguments
                func_args = self.GetFunctionArguments(func_nodes[2])

                # Get function object
                function_obj = CreateFunctionObj(func_name, func_args)

                # Fill function body with code
                body_instructions_nodes = func_nodes[3].GetChildren()
                for instruction_node in body_instructions_nodes:
                    new_code = self.ParseInstruction(instruction_node)
                    UpdateFuncCode(function_obj, new_code)

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

            var_id = arg_children[1].GetLexeme().itemValue
            variable = [v for v in self.VariableTable if v.itemId == var_id][0]

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

    def ParseInstruction(self, instruction_node):
        """
            Parses given instruction node.
        """

        return
