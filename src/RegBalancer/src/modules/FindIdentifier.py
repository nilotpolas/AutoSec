import pycparser.c_ast as cast


class FindIdentifier(cast.NodeVisitor):
    """
    @class FindIdentifier
    @brief A visitor class for finding identifiers in an abstract syntax tree (AST).

    This class extends `pycparser.c_ast.NodeVisitor` and is used to traverse an AST to locate identifiers. It stores the name of the first identifier found during the traversal.

    @see pycparser.c_ast.NodeVisitor
    """

    def __init__(self) -> None:
        """
        @brief Initializes the FindIdentifier instance.

        The constructor initializes the base `NodeVisitor` class and sets up the storage for the identifier.
        """
        super().__init__()
        self.identifier = None

    def visit_ID(self, node):
        """
        @brief Visits an ID node and stores the identifier name.

        This method is called when an ID node is encountered in the AST. It updates the stored identifier name with the name from the ID node.

        @param node The ID node that contains the identifier name to be stored.
        """
        self.identifier = node.name

    def name(self, ast):
        """
        @brief Retrieves the name of the identifier from the AST.

        This method traverses the provided AST to find an identifier. If an identifier is found, its name is returned. If no identifier is found, an exception is raised.

        @param ast The AST to traverse and search for an identifier.

        @return The name of the found identifier.

        @throws Exception If no identifier is found in the AST.
        """
        self.visit(ast)
        if (self.identifier == None):
            raise Exception(
                "FindIdentifier could not find any identifier in the ast")
        return self.identifier
