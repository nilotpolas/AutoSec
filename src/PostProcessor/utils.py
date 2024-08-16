from pycparser import c_ast,c_generator
from astNodes import getAssignmentNode,getDeclarationNode,getRegFuncCallNode,getSimpleAssignmentNode

"""
@brief Provides utilities for manipulating C code AST nodes.

This module contains functions for handling and transforming abstract syntax trees (AST) of C code.
It includes functionality for dealing with binary operations, register function calls, and generating C code.

@details
- `isRegCall`: Checks if a node represents a call to the "reg" function.
- `isNestedRegCall`: Determines if a node is a nested register call.
- `extractOperands`: Extracts operands from a node.
- `getVariableNameFromOperands`: Constructs a variable name based on operands and operators.
- `noneOperandStartsWithv`: Checks if none of the operands start with 'v'.
- `getNewVarName`: Generates a new variable name.
- `changeBinaryOpUtil`: Utility function for changing binary operations.
- `changeBinaryOps`: Modifies binary operations in the AST.
- `generate_c_file`: Generates a C file from an AST.
- `handleAssignmentNodes`: Processes and handles assignment nodes in the AST.
"""

def isRegCall(node):
    """
    Checks if a node represents a call to the "reg" function.

    @param node: The node to check.

    @return: True if the node is a `reg` function call, False otherwise.
    """
    return isinstance(node,c_ast.FuncCall) and node.name.name == 'reg'

def isNestedRegCall(node):
    """
    Checks if a node is a nested register function call.

    @param node: The node to check.

    @return: True if the node is a nested `reg` function call, False otherwise.
    """
    return isRegCall(node) and isRegCall(node.args.exprs[0])

def extractOperands(node):
    """
    Extracts operands from a node, handling different node types.

    @param node: The node from which to extract operands.

    @return: A list of operands or a string representing the operand.
    @raises ValueError: If the node type is unsupported.
    """
    if (isinstance(node, c_ast.BinaryOp)):
        leftOperand = extractOperands(node.left) 
        rightOperand = extractOperands(node.right)
        return [leftOperand,rightOperand]
    elif isRegCall(node):
        return "v_reg_" + node.args.exprs[0].name
    elif isinstance(node,c_ast.ID):
        return node.name
    elif isinstance(node,c_ast.UnaryOp):
        return "v_neg_" + extractOperands(node.expr)
    else:
        raise ValueError(f"Unsupported node type: {type(node).__name__}")
    
def getVariableNameFromOperands(operands,operatorNameMap,operator = ""):
    """
    Constructs a variable name based on operands and operator.

    @param operands: The list of operands.
    @param operatorNameMap: A dictionary mapping operators to their names.
    @param operator: The operator to include in the variable name.

    @return: A string representing the variable name.
    """
    variableName = operands[0]
    if(len(operands) > 1):
        variableName += ("_" + operatorNameMap[operator] + "_" + operands[1])
    return variableName

def noneOperandStartsWithv(operands):
    """
    Checks if none of the operands start with 'v'.

    @param operands: The list of operands.

    @return: True if none of the operands start with 'v', False otherwise.
    """
    for operand in operands:
        if operand.startswith("v"):
            return False
    return True

def getNewVarName(assgnNo):
    """
    Generates a new variable name for assignments.

    @param assgnNo: The assignment number to include in the variable name.

    @return: A string representing the new variable name.
    """
    return "z" + str(assgnNo) + "_assgn" + str(assgnNo)

def changeBinaryOpUtil(node,varForBinaryOp,bodyNodes):
    """
    Utility function for changing binary operations.

    @param node: The node representing the binary operation.
    @param varForBinaryOp: The variable name for the binary operation.
    @param bodyNodes: The list of body nodes to append the new nodes to.
    """
    bodyNodes.append(getDeclarationNode(varForBinaryOp))
    bodyNodes.append(getSimpleAssignmentNode(varForBinaryOp,node))

def changeBinaryOps(node,bodyNodes,assgnNo):
    """
    Modifies binary operations in the AST.

    @param node: The node containing the binary operation to modify.
    @param bodyNodes: The list of body nodes to append the modified nodes to.
    @param assgnNo: The current assignment number used for generating new variable names.
    """
    currNode = node.rvalue
    if isinstance(currNode,c_ast.BinaryOp):
        origLeft = currNode.left
        origRight = currNode.right
        
        if isNestedRegCall(currNode.right):
            varForBinaryOp = getNewVarName(assgnNo)
            changeBinaryOpUtil(currNode.right,varForBinaryOp,bodyNodes)
            origRight = c_ast.ID(varForBinaryOp)
        if isNestedRegCall(currNode.left):
            varForBinaryOp = getNewVarName(assgnNo+1)
            changeBinaryOpUtil(currNode.left,varForBinaryOp,bodyNodes)
            origLeft = c_ast.ID(varForBinaryOp)
        binaryOpNode = c_ast.BinaryOp(op=currNode.op,left=origLeft,right=origRight)
        bodyNodes.append(c_ast.Assignment(op='=',lvalue=node.lvalue,rvalue=binaryOpNode))
    else:
        bodyNodes.append(node)

def generate_c_file(ast,filename):
    """
    Generates C code from the provided Abstract Syntax Tree (AST) and saves it to a file.

    @param ast: The Abstract Syntax Tree (AST) to generate C code from.
    @param filename: The path to the file where the generated C code will be saved.
    """
    generator = c_generator.CGenerator()
    with open(filename, 'w') as output_file:
        print(generator.visit(ast), file=output_file)


def handleAssignmentNodes(node,bodyNodes,operatorNameMap,assgnNo):
    """
    Processes and handles assignment nodes in the AST.

    @param node: The assignment node to process.
    @param bodyNodes: The list of body nodes to append the processed nodes to.
    @param operatorNameMap: A dictionary mapping operators to their names.
    @param assgnNo: The current assignment number used for generating new variable names.
    """
    count = 1;
    currNode = node.rvalue
    if isRegCall(currNode):
        while isRegCall(currNode.args.exprs[0]):
            count += 1
            currNode = currNode.args.exprs[0]
        currNode = currNode.args.exprs[0]
        operands = extractOperands(currNode)
        if not isinstance(operands,list):
            operands = [operands]

        if count == 1 and noneOperandStartsWithv(operands):
             bodyNodes.append(node)
             return

        op = currNode.op if isinstance(currNode, c_ast.BinaryOp) else ""
        variableName = getNewVarName(assgnNo)
        assignmentNode = getAssignmentNode(operands,op,variableName)
        # if len(operands) > 1:
        bodyNodes.append(getDeclarationNode(variableName))
        bodyNodes.append(assignmentNode)
        prevVarName = variableName

        for index in range(count):
            newVarName = variableName + str(index)
            if index != count - 1:
                bodyNodes.append(getDeclarationNode(newVarName))
            regCallNode = getRegFuncCallNode(prevVarName)
            lvalue = c_ast.ID(newVarName) if index != count -1 else node.lvalue
            bodyNodes.append(c_ast.Assignment(op='=',lvalue=lvalue,rvalue=regCallNode))
            prevVarName = newVarName
        
    else:
        bodyNodes.append(node)
    