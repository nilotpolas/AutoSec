from pycparser import c_ast
import globalVariables
"""
@brief Provides utility functions for creating and manipulating AST nodes.

This module defines several utility functions for generating different types of AST nodes, including assignments, declarations, and function calls in C code.
"""
def getRegFuncCallNode(name):
    """
    Creates a function call node for the 'reg' function with a given argument.

    @param name: The argument name for the 'reg' function.
    @type name: str

    @return: A `c_ast.FuncCall` node representing a function call to 'reg' with the specified argument.
    @rtype: c_ast.FuncCall
    """
    node = c_ast.FuncCall(name=c_ast.ID(name='reg'),args=c_ast.ExprList(exprs=[c_ast.ID(name=name)]))
    return node

def getLeftOrRightNodeOfAssignment(operand):
    """
    Generates the corresponding AST node for a given operand based on its type.

    @param operand: The operand for which to create the AST node.
    @type operand: str

    @return: A `c_ast.ID`, `c_ast.UnaryOp`, or `c_ast.FuncCall` node based on the operand's prefix.
    @rtype: c_ast.ID | c_ast.UnaryOp | c_ast.FuncCall
    """
    if operand.startswith("v_reg"):
        node = getRegFuncCallNode(operand[6:])
    elif operand.startswith("v_neg"):
            node = c_ast.UnaryOp(op='!',expr=c_ast.ID(name=operand[6:]))
    else:
        node = c_ast.ID(name=operand)
    return node

def getSimpleAssignmentNode(lvalue,rvalue):
    """
    Creates a simple assignment node with the specified left-hand side and right-hand side.

    @param lvalue: The left-hand side of the assignment.
    @type lvalue: str
    @param rvalue: The right-hand side of the assignment.
    @type rvalue: c_ast.Node

    @return: A `c_ast.Assignment` node representing the assignment operation.
    @rtype: c_ast.Assignment
    """
    return c_ast.Assignment(op='=',lvalue=c_ast.ID(name=lvalue),rvalue=rvalue)

def getAssignmentNode(operands,operator,varToAssign):
    """
    Creates an assignment node with a binary operation if there are multiple operands, or a single operand otherwise.

    @param operands: A list of operands for the assignment.
    @type operands: list of str
    @param operator: The operator to use if there are multiple operands.
    @type operator: str
    @param varToAssign: The variable name to which the result is assigned.
    @type varToAssign: str

    @return: A `c_ast.Assignment` node with the specified operands and operator.
    @rtype: c_ast.Assignment
    """
    left = None
    right = None
    rvalue = None

    left = getLeftOrRightNodeOfAssignment(operands[0])
    if len(operands) > 1:
        right = getLeftOrRightNodeOfAssignment(operands[1])
    
    if right is not None:
        rvalue = c_ast.BinaryOp(op=operator,left=left,right=right)
    else:
        rvalue = left
    
    return c_ast.Assignment(op="=",lvalue=c_ast.ID(name=varToAssign),rvalue=rvalue)

def getDeclarationNode(idName):
    """
    Creates a declaration node for a variable with the specified name and the global type.

    @param idName: The name of the variable to declare.
    @type idName: str

    @return: A `c_ast.Decl` node representing the variable declaration.
    @rtype: c_ast.Decl
    """
    
    # print(globalVariables.globalType)
    typeDeclNode = c_ast.TypeDecl(declname = idName,quals = [],align = None,
                                                type=c_ast.IdentifierType(names=[globalVariables.globalType]))
    declNode = c_ast.Decl(name=idName, quals=[], storage=[], funcspec=[],
                type=typeDeclNode, init=None,
                bitsize=None, align=[])
    return declNode