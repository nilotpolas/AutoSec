from pycparser import c_ast
from utils import isRegCall,getNewVarName,isNestedRegCall
from astNodes import getSimpleAssignmentNode,getDeclarationNode
import copy

"""
@brief Provides AST node visitors for handling unary and binary operations, and source register operations in C code.

This module defines various visitors for traversing and transforming an abstract syntax tree (AST) of C code.
These visitors handle unary operations, binary operations within register calls, and source register operations.

@details
- `UnaryOpNodeChanger`: Changes unary operation nodes in the AST based on a provided map.
- `NegationVisitor`: Handles negation operations and replaces unary operations with equivalent assignments.
- `BinaryOpInRegHandler`: Modifies binary operations inside register calls.
- `SourceRegHandler`: Handles source register operations, including adjustments for input registers.
"""


class UnaryOpNodeChanger(c_ast.NodeVisitor):
    """
    Visitor for changing unary operation nodes in the AST based on a provided map.

    @param unaryNodeMap: A dictionary mapping unary operation variable names to new variable names.
    """
    def __init__(self,unaryNodeMap):
        """
        Initializes the UnaryOpNodeChanger.

        @param unaryNodeMap: A dictionary mapping unary operation variable names to new variable names.
        """
        self.unaryNodeMap = unaryNodeMap
    
    def visit_BinaryOp(self,node):
        """
        Visits binary operation nodes and replaces unary operation nodes with corresponding IDs.

        @param node: The binary operation node to visit.
        """
        if isinstance(node.right,c_ast.UnaryOp):
            node.right = c_ast.ID(name=self.unaryNodeMap[node.right.expr.name])
            # self.generic_visit(node.left)
        if isinstance(node.left,c_ast.UnaryOp):
            node.left = c_ast.ID(name=self.unaryNodeMap[node.left.expr.name])
            # self.generic_visit(node.right)
        self.generic_visit(node)
    
    def visit_FuncCall(self,node):
        """
        Visits function call nodes and replaces unary operation arguments with corresponding IDs.

        @param node: The function call node to visit.
        """
        param = node.args.exprs[0]
        if isinstance(param,c_ast.UnaryOp):
            node.args.exprs[0] = c_ast.ID(name=self.unaryNodeMap[param.expr.name])
            return
        else:
            self.generic_visit(node)

class NegationVisitor(c_ast.NodeVisitor):
    """
    Visitor for handling negation operations and replacing unary operations with equivalent assignments.

    @param bodyNodes: A list to store transformed nodes.
    """
    def __init__(self,bodyNodes):
        """
        Initializes the NegationVisitor.

        @param bodyNodes: A list to store transformed nodes.
        """
        self.bodyNodes = bodyNodes
        self.assgnNo = 1
        self.unaryVarToNameMap = {}

    def visit_FuncDef(self,node):
        """
        Visits function definition nodes and continues traversal.

        @param node: The function definition node to visit.
        """
        self.generic_visit(node)

    def visit_Decl(self,node):
        """
        Visits declaration nodes and appends them to the body nodes list.

        @param node: The declaration node to visit.
        """
        if isinstance(node.type,c_ast.TypeDecl):
            self.bodyNodes.append(node)
        return
        
    def visit_Assignment(self,node):
        """
        Visits assignment nodes and processes the right-hand side based on its type.

        @param node: The assignment node to visit.
        """
        if isinstance(node.rvalue,c_ast.BinaryOp) or isRegCall(node.rvalue):
            self.generic_visit(node.rvalue)
            self.bodyNodes.append(node)
        else:
            self.bodyNodes.append(node)
            return

    def visit_UnaryOp(self,node):
        """
        Visits unary operation nodes and replaces them with equivalent assignments.

        @param node: The unary operation node to visit.
        """
        if node.expr.name in self.unaryVarToNameMap:
            return
        if node.op == '!' or node.op == '~':
            varName = getNewVarName(self.assgnNo)
            declNode = getDeclarationNode(varName)
            self.bodyNodes.append(declNode)
            assgnNode = getSimpleAssignmentNode(varName,node)
            self.bodyNodes.append(assgnNode)
            self.unaryVarToNameMap[node.expr.name] = varName
            self.assgnNo += 1

class BinaryOpInRegHandler(c_ast.NodeVisitor):
    """
    Visitor for handling binary operations inside register function calls.

    @param bodyNodes: A list to store transformed nodes.
    @param assignNo: The current assignment number used for generating new variable names.
    """
    def __init__(self,bodyNodes,assignNo):
        """
        Initializes the BinaryOpInRegHandler.

        @param bodyNodes: A list to store transformed nodes.
        @param assignNo: The current assignment number used for generating new variable names.
        """
        self.bodyNodes = bodyNodes
        self.assignNo = assignNo

    def visit_Decl(self,node):
        """
        Visits declaration nodes and appends them to the body nodes list.

        @param node: The declaration node to visit.
        """
        if isinstance(node.type,c_ast.TypeDecl):
            self.bodyNodes.append(node)
        return

    def visit_Assignment(self,node):
        """
        Visits assignment nodes and processes them based on their right-hand side type.

        @param node: The assignment node to visit.
        """
        if not isinstance(node.rvalue,c_ast.FuncCall):
            self.bodyNodes.append(node)
            return
        self.generic_visit(node)
        self.bodyNodes.append(node)
    
    def visit_FuncCall(self,node):
        """
        Visits function call nodes and processes binary operations within register function calls.

        @param node: The function call node to visit.
        """
        currNode = node
        while isRegCall(currNode.args.exprs[0]):
            currNode = currNode.args.exprs[0]
        insideNode = currNode.args.exprs[0]
        if isinstance(insideNode,c_ast.BinaryOp):
            if isRegCall(insideNode.right) or isRegCall(insideNode.left):
                varName = getNewVarName(self.assignNo)
                self.assignNo += 2
                currNode.args.exprs[0] = c_ast.ID(name=varName)
                self.bodyNodes.append(getDeclarationNode(varName))
                self.bodyNodes.append(getSimpleAssignmentNode(lvalue=varName,rvalue=insideNode))

class SourceRegHandler(c_ast.NodeVisitor):
    """
    Visitor for handling source register operations, including adjustments for input registers.

    @param bodyNodes: A list to store transformed nodes.
    @param assignNo: The current assignment number used for generating new variable names.
    """
    def __init__(self,bodyNodes,assignNo):
        """
        Initializes the SourceRegHandler.

        @param bodyNodes: A list to store transformed nodes.
        @param assignNo: The current assignment number used for generating new variable names.
        """
        self.bodyNodes = bodyNodes
        self.assignNo = assignNo
        self.sourceRegMap = {}
    
    def visit_Decl(self,node):
        """
        Visits declaration nodes and appends them to the body nodes list.

        @param node: The declaration node to visit.
        """
        if isinstance(node.type,c_ast.TypeDecl):
            self.bodyNodes.append(node)
        return
    
    def visit_ID(self,node):
        """
        Visits ID nodes and updates their names based on the source register map.

        @param node: The ID node to visit.
        """
        if node.name in self.sourceRegMap:
            node.name = self.sourceRegMap[node.name]
    
    def visit_Assignment(self,node):
        """
        Visits assignment nodes and processes source register operations.

        @param node: The assignment node to visit.
        """
        if isinstance(node.lvalue,c_ast.ID) and node.lvalue.name.endswith("inp"):
            if isinstance(node.rvalue,c_ast.FuncCall) and not isinstance(node.rvalue.args.exprs[0],c_ast.FuncCall):
                nodeCopy = copy.deepcopy(node.rvalue)
                nodeCopy.args.exprs[0].name += "_inp"
                node.rvalue = c_ast.ID(name=node.lvalue.name[:-4])
                self.bodyNodes.append(node)
                varName = getNewVarName(self.assignNo)
                self.bodyNodes.append(getDeclarationNode(varName))
                self.bodyNodes.append(getSimpleAssignmentNode(varName,nodeCopy))
                self.assignNo += 2
                self.sourceRegMap[node.lvalue.name] = varName
            else:
                self.bodyNodes.append(node)
            return
        else:
            self.generic_visit(node)
            self.bodyNodes.append(node)
