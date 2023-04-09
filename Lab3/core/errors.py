# Lexical analyzer errors
class LexicalAnalyzerError(Exception):
    """
        Error to specify lexical analysis failed.
    """

    def __init__(self, message, file_name, coordinate_line, coordinate_offset):
        self.ErrorMessage = f'File "{file_name}" [{str(coordinate_line)}:{str(coordinate_offset)}]: error: {message}'
        super().__init__(self.ErrorMessage)


# Tree parser errors
class ParserError(Exception):
    """
        Error to specify parser failed.
    """

    def __init__(self, message, file_name, coordinate_line, coordinate_offset):
        self.ErrorMessage = f'File "{file_name}" [{str(coordinate_line)}:{str(coordinate_offset)}]: error: {message}'
        super().__init__(self.ErrorMessage)


class ExpectedError(ParserError):
    """
        Error to specify parser failed on expected.
    """

    def __init__(self, expected, file_name, coordinate_line, coordinate_offset):
        super().__init__(
            f"{expected} was expected here.",
            file_name,
            coordinate_line,
            coordinate_offset,
        )


class UsingBeforeDeclarationError(ParserError):
    """
        Error to specify parser failed on unknown variable used.
    """

    def __init__(self, var_name, file_name, coordinate_line, coordinate_offset):
        super().__init__(
            f"Variable {var_name} using before declaration.",
            file_name,
            coordinate_line,
            coordinate_offset,
        )


class DoubleDeclarationError(ParserError):
    """
        Error to specify parser failed on variable declared twice.
    """

    def __init__(self, var_name, file_name, coordinate_line, coordinate_offset):
        super().__init__(
            f"Redeclaration of variable {var_name}.",
            file_name,
            coordinate_line,
            coordinate_offset,
        )
