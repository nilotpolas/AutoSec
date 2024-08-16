from pycparser import c_ast
"""
@brief Provides utility functions for creating AST nodes related to assignments and declarations.

This module defines utility functions for generating AST nodes for simple and constant assignments, as well as variable declarations in C code.
"""
def getSimpleAssignmentNode(lvalue,rvalue):
    """
    Creates a simple assignment node with the specified left-hand side and right-hand side.

    @param lvalue: The left-hand side of the assignment, typically a variable name.
    @type lvalue: str
    @param rvalue: The right-hand side of the assignment, typically a variable name or expression.
    @type rvalue: str

    @return: A `c_ast.Assignment` node representing the assignment operation.
    @rtype: c_ast.Assignment
    """
    return c_ast.Assignment(lvalue=c_ast.ID(name=lvalue),rvalue=c_ast.ID(name=rvalue),op='=')

def getConstAssignmentNode(lvalue,rvalue):
    """
    Creates an assignment node where the right-hand side is a constant integer.

    @param lvalue: The left-hand side of the assignment, typically a variable name.
    @type lvalue: str
    @param rvalue: The constant integer value for the right-hand side of the assignment.
    @type rvalue: int

    @return: A `c_ast.Assignment` node representing the assignment of a constant integer value.
    @rtype: c_ast.Assignment
    """
    return c_ast.Assignment(lvalue=c_ast.ID(name=lvalue),rvalue=c_ast.Constant(type="int",value=rvalue),op='=')

def getDeclarationNode(idName,type):
    """
    Creates a declaration node for a variable with the specified name and type.

    @param idName: The name of the variable to declare.
    @type idName: str
    @param type: The type of the variable, e.g., 'int' or 'float'.
    @type type: str

    @return: A `c_ast.Decl` node representing the variable declaration.
    @rtype: c_ast.Decl
    """

    typeDeclNode = c_ast.TypeDecl(declname = idName,quals = [],align = None,
                                                  type=c_ast.IdentifierType(names=[type]))
    declNode = c_ast.Decl(name=idName, quals=[], storage=[], funcspec=[],
                type=typeDeclNode, init=None,
                bitsize=None, align=[])
    return declNode