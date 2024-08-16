from pycparser import c_ast,c_generator
from Visitors import LocalVariablesModifier,DeclVisitor,InputParamModifier,IdVisitor
from astNodes import getDeclarationNode,getSimpleAssignmentNode
import copy

def getFunctionAssignments(functionInfo,argumentMap,localVariablesMap,assignmentNodes):
    """
    @brief Extracts and modifies function assignment nodes based on argument and local variable mappings.

    This function processes the assignment nodes of a given function, updating identifiers according to the provided 
    argument and local variable mappings, and appends the modified nodes to the assignmentNodes list.

    @param functionInfo: Dictionary containing function information, including assignment nodes.
    @type functionInfo: dict
    @param argumentMap: Mapping from function parameters to argument names.
    @type argumentMap: dict
    @param localVariablesMap: Mapping from local variables to new variable names.
    @type localVariablesMap: dict
    @param assignmentNodes: List to which modified assignment nodes will be appended.
    @type assignmentNodes: list
    """
    copyAssignmentNodes = copy.deepcopy(functionInfo['assignmentNodes'])
    for node in copyAssignmentNodes:
        visitor = IdVisitor(argumentMap,localVariablesMap)
        visitor.visit(node)
        assignmentNodes.append(node);

def getType(node):
    """
    @brief Retrieves the type name from a type node.

    This function extracts the type name from a given node. It supports both IdentifierType and other type nodes.

    @param node: The type node from which to extract the type name.
    @type node: pycparser.c_ast.Type
    @return: The type name as a string.
    @rtype: str
    """
    if isinstance(node,c_ast.IdentifierType):
        return node.names[0]
    else:
        return node.type.names[0]

def extractFunctionInfo(node,functionInfo):
    """
    @brief Extracts information about a function, including parameters, local variables, and assignment nodes.

    This function collects parameters, local variables, and assignment nodes from a function definition node and
    stores the information in the functionInfo dictionary.

    @param node: The function definition node to extract information from.
    @type node: pycparser.c_ast.FuncDef
    @param functionInfo: Dictionary to store extracted function information.
    @type functionInfo: dict
    """
    function_name = node.decl.name
    parameters = []
    localVariables = []
    localVariablesType = []
    assignmentNodes = []

    if node.decl.type.args:
        for param_decl in node.decl.type.args.params:
            parameters.append(param_decl.name)
    
    functionBody = node.body
    for blockItem in functionBody.block_items:
        if isinstance(blockItem,c_ast.Decl):
            typeOfId = getType(blockItem.type.type)
            localVariablesType.append(typeOfId)
            localVariables.append(blockItem.name)
        if isinstance(blockItem,c_ast.Assignment):
            if isinstance(blockItem.lvalue,c_ast.UnaryOp):
                blockItem.lvalue = c_ast.ID(blockItem.lvalue.expr.name)
            visitor = LocalVariablesModifier(localVariables,function_name)
            visitor.visit(blockItem)
            assignmentNodes.append(blockItem)
    
    for index in range(len(localVariables)):
        localVariables[index] += ('_' + function_name)

    functionInfo[function_name] = {
        'parameters' : parameters,
        'localVariables' : localVariables,
        'localVariablesType' : localVariablesType,
        'assignmentNodes' : assignmentNodes,
        'firstTimeProcessing' : True,
        'timesCalled' : 0
    }

def processDependantFunctions(node,functionInfo,isTopModule):
    """
    @brief Processes function calls within a given function, handling parameter and local variable modifications.

    This function modifies function calls within the function body, updates the parameter and local variable mappings,
    and inserts appropriate declarations and assignments into the function body.

    @param node: The function definition node to process.
    @type node: pycparser.c_ast.FuncDef
    @param functionInfo: Dictionary containing information about all functions.
    @type functionInfo: dict
    @param isTopModule: Boolean indicating if the function is the top module.
    @type isTopModule: bool
    """
    functionBody = node.body
    changedInputMap = {}
    bodyNodes = []

    if isTopModule:
        if node.decl.type.args:
            for param_decl in node.decl.type.args.params:
                visitor = DeclVisitor()
                visitor.visit(param_decl)
                declType = param_decl.type
                if isinstance(declType,c_ast.TypeDecl):
                    typeOfId = getType(declType.type)
                    bodyNodes.append(getDeclarationNode(param_decl.name + '_inp',typeOfId))
                    changedInputMap[param_decl.name] = param_decl.name + '_inp'
            for param_decl in node.decl.type.args.params:
                declType = param_decl.type
                if isinstance(declType,c_ast.TypeDecl):
                    bodyNodes.append(getSimpleAssignmentNode(param_decl.name + '_inp',param_decl.name))
    
    for blockItem in functionBody.block_items:
        if isinstance(blockItem,c_ast.Decl):
            visitor = DeclVisitor()
            visitor.visit(blockItem)
            bodyNodes.append(blockItem)
        
        if isinstance(blockItem,c_ast.Assignment):
            visitor = InputParamModifier(changedInputMap)
            visitor.visit(blockItem)
            bodyNodes.append(blockItem)

        if isinstance(blockItem,c_ast.FuncCall):
            argumentMap = {}
            localVariablesMap = {}
            
            functionName = blockItem.name.name
            parameters = functionInfo[functionName]['parameters']
            localVariables = functionInfo[functionName]['localVariables']
            localVariablesType = functionInfo[functionName]['localVariablesType']
            timesCalled = functionInfo[functionName]['timesCalled']
            arguments = blockItem.args.exprs
            for index in range(len(arguments)):
                if isinstance(arguments[index],c_ast.UnaryOp):
                    arguments[index] = c_ast.ID(arguments[index].expr.name)

            for localVariable,localVariableType in zip(localVariables,localVariablesType):
                declNode = getDeclarationNode(localVariable + str(timesCalled),localVariableType)
                localVariablesMap[localVariable] = localVariable + str(timesCalled)
                bodyNodes.append(declNode)
            
            for index in range(len(parameters)):
                if arguments[index].name in changedInputMap:
                    argName = arguments[index].name + '_inp'
                else:
                    argName = arguments[index].name
                argumentMap[parameters[index]] = argName
            
            getFunctionAssignments(functionInfo[functionName],argumentMap,localVariablesMap,bodyNodes)
            functionInfo[functionName]['timesCalled'] += 1
    node.body = c_ast.Compound(block_items=bodyNodes)

def mergeConstants(ast):
    """
    @brief Placeholder function for merging constants.

    This function currently does nothing and is intended to be implemented with logic for merging constants in the AST.

    @param ast: The Abstract Syntax Tree to be processed.
    @type ast: pycparser.c_ast.FileAST
    """
    a = 1

def insertAssignmentsAndDeclForConstants(ast,constArr):
    """
    @brief Inserts assignments and declarations for constants into the AST.

    This function adds declarations and assignments for constants into the function's parameter list and body nodes.

    @param ast: The Abstract Syntax Tree to be updated.
    @type ast: pycparser.c_ast.FileAST
    @param constArr: List of constant names to be added to the AST.
    @type constArr: list of str
    @return: The updated Abstract Syntax Tree.
    @rtype: pycparser.c_ast.FileAST
    """
    paramList = ast.ext[0].decl.type.args.params
    bodyNodes = ast.ext[0].body.block_items
    for const in constArr:
        bodyNodes.insert(0,getSimpleAssignmentNode(const + "_inp",const))
    for const in constArr:
        bodyNodes.insert(0,getDeclarationNode(const + "_inp","int"))
    for const in constArr:
        paramList.append(getDeclarationNode(const,"int"))
    return ast


def generate_c_file(ast,filename):
    """
    @brief Generates C code from the provided Abstract Syntax Tree (AST) and writes it to a file.

    This function uses the C generator to convert the AST into C code and saves the generated code to the specified file.

    @param ast: The Abstract Syntax Tree to be converted into C code.
    @type ast: pycparser.c_ast.FileAST
    @param filename: The name of the file where the generated C code will be saved.
    @type filename: str
    """
    generator = c_generator.CGenerator()
    with open(filename, 'w') as output_file:
        print(generator.visit(ast), file=output_file)