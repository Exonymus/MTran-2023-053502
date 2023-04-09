from core.language import *


class SyntaxTreNodeTypes(Enum):
    COMMON = 0,
    DECLARATION = 1,
    CODE_BLOCK = 2


class SyntaxTreeNode:
    def __init__(self, lexeme, type=LexicalTreNodeTypes.COMMON):
        self.Lexeme = lexeme
        self.Children = []
        self.Type = type

    def AddChild(self, node):
        self.Children.append(node)

    def GetChildren(self):
        return self.Children

    def GetLexeme(self):
        return self.Lexeme

    def __str__(self):
        if self.Lexeme is None:
            return str(self.Type)
        elif self.Lexeme.type in [
            Language.LexemeTypes.IDENTIFIER,
            Language.LexemeTypes.INT_NUM,
            Language.LexemeTypes.DOUBLE_NUM
        ]:
            return f"{str(self.Lexeme.type)} : {str(self.Lexeme.value)}"
        elif self.Lexeme.type == Language.LexemeTypes.STRING:
            return f"{str(self.Lexeme.type)} : {repr(self.Lexeme.value)}"
        else:
            return str(self.Lexeme.value)


def printSyntaxTree(root, depth: int = 0):
    if root is None:
        return

    print('\t' * depth + str(root))
    for child in root.get_childs():
        printSyntaxTree(child, depth + 1)
