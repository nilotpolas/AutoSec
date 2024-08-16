from pycparser import c_ast

class AddRegs(c_ast.NodeVisitor):
    """
    @brief A visitor class for modifying specific nodes in a C AST based on their names.

    This class is used to traverse a C Abstract Syntax Tree (AST) and replace occurrences of
    specific identifiers with a given node.

    @param changedNode The node that will replace the identified nodes.
    @param idToChange The name of the identifier to be replaced.
    """

    def __init__(self,changedNode,idToChange):
        """
        @brief Initializes the AddRegs visitor.

        @param changedNode The node that will replace the identified nodes.
        @param idToChange The name of the identifier to be replaced.
        """
        self.changedNode = changedNode
        self.idToChange = idToChange
        
    def visit_FuncCall(self,node):
        """
        @brief Visits a function call node in the AST.

        If the function call's argument matches the identifier to be changed, it replaces it
        with the given changedNode.

        @param node The function call node to visit.

        @return None
        """
        # curr = node.args.exprs[0]
        if isinstance(node.args.exprs[0],c_ast.ID) and self.idToChange == node.args.exprs[0].name:
            node.args.exprs[0] = self.changedNode
            return
        self.generic_visit(node)

    def visit_BinaryOp(self,node):
        """
        @brief Visits a binary operation node in the AST.

        If either the left or right operand of the binary operation matches the identifier to be
        changed, it replaces it with the given changedNode.

        @param node The binary operation node to visit.

        @return None
        """
        if isinstance(node.right,c_ast.ID) and self.idToChange == node.right.name:
            node.right = self.changedNode
            return
        if isinstance(node.left,c_ast.ID) and self.idToChange == node.left.name:
            node.left = self.changedNode
            return
        self.generic_visit(node)