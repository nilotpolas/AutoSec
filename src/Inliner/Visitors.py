from pycparser import c_ast
from DiGraph import DiGraph

class FunctionVisitor(c_ast.NodeVisitor):
    """
    @brief Visits function call nodes in the AST and updates the dependency graph.

    This visitor traverses the function call nodes in the AST to build a dependency graph of functions.

    @param diGraph: The directed graph that tracks function dependencies.
    @type diGraph: DiGraph
    @param functionName: The name of the current function being processed.
    @type functionName: str
    """
    def __init__(self,diGraph : DiGraph,functionName):
        self.diGraph = diGraph
        self.functionName = functionName
    def visit_FuncCall(self,node):
        """
        @brief Processes function call nodes and updates the function dependency graph.

        Adds the function called to the graph and creates an edge from the called function to the current function.

        @param node: The function call node being visited.
        @type node: pycparser.c_ast.FuncCall
        """
        if node.name.name != 'reg':
            self.diGraph.addFunction(node.name.name)
            self.diGraph.addEdgeBetween(node.name.name,self.functionName)

class LocalVariablesModifier(c_ast.NodeVisitor):
    """
    @brief Modifies local variable names by appending the function name.

    This visitor updates the names of local variables by appending the function name to ensure uniqueness.

    @param localVariables: List of local variable names to be modified.
    @type localVariables: list of str
    @param fName: The name of the function to append to local variable names.
    @type fName: str
    """
    def __init__(self,localVariables,fName):
        self.localVariables = localVariables
        self.fName = fName
    def visit_ID(self,node):
        """
        @brief Updates local variable names with function name suffix.

        Appends the function name to the local variable name if it is found in the list of local variables.

        @param node: The identifier node representing a local variable.
        @type node: pycparser.c_ast.ID
        """
        if(node.name in self.localVariables):
            node.name = node.name + '_' + self.fName

class DeclVisitor(c_ast.NodeVisitor):
    """
    @brief Visits declaration nodes to store array initialization values.

    This visitor collects initialization values for array declarations and stores them in a map.

    @param arrayMap: Dictionary to store array names and their corresponding values.
    @type arrayMap: dict
    @param ast: The Abstract Syntax Tree being processed.
    @type ast: pycparser.c_ast.FileAST
    """
    def __init__(self,arrayMap = None,ast = None):
        self.arrayMap = arrayMap
        self.ast = ast

    def storeArray(self,node):
        """
        @brief Stores the values of an array declaration in the array map.

        @param node: The array declaration node to process.
        @type node: pycparser.c_ast.Decl
        """
        arrName = node.name
        contents = []
        for item in node.init.exprs:
            if item.value.startswith("0x"):
                decVal = int(item.value[2:],16)
            else:
                decVal = int(item.value)
            contents.append(decVal)
        self.arrayMap[arrName] = contents

    def visit_Decl(self,node):
        """
        @brief Processes declaration nodes to handle array declarations.

        Calls the storeArray method if the declaration is an array.

        @param node: The declaration node being visited.
        @type node: pycparser.c_ast.Decl
        """
        declType = node.type.type

        if isinstance(node.type,c_ast.ArrayDecl):
            self.storeArray(node)

class InputParamModifier(c_ast.NodeVisitor):
    """
    @brief Modifies input parameter names based on a mapping.

    This visitor updates the names of input parameters according to a provided mapping.

    @param changedInputMap: Mapping of original input parameter names to new names.
    @type changedInputMap: dict
    """
    def __init__(self,changedInputMap):
        self.changedInputMap = changedInputMap
    def visit_ID(self,node):
        """
        @brief Updates input parameter names based on the mapping.

        Replaces the parameter name with the new name from the mapping if it exists.

        @param node: The identifier node representing an input parameter.
        @type node: pycparser.c_ast.ID
        """
        if node.name in self.changedInputMap:
            node.name = self.changedInputMap[node.name]

class IdVisitor(c_ast.NodeVisitor):
    """
    @brief Visits identifier nodes and updates their names based on provided mappings.

    This visitor changes the names of identifiers according to the argument and local variable mappings.

    @param argumentMap: Mapping of argument names to new names.
    @type argumentMap: dict
    @param localVariablesMap: Mapping of local variable names to new names.
    @type localVariablesMap: dict
    """
    def __init__(self,argumentMap,localVariablesMap):
        self.localVariablesMap = localVariablesMap
        self.argumentMap = argumentMap
    def visit_ID(self, node):
        """
        @brief Updates identifier names based on argument and local variable mappings.

        @param node: The identifier node to be updated.
        @type node: pycparser.c_ast.ID
        """
        if node.name in self.argumentMap:
            node.name = self.argumentMap[node.name]
        if node.name in self.localVariablesMap:
            node.name = self.localVariablesMap[node.name]

class ArrayValueReplacer(c_ast.NodeVisitor):
    """
    @brief Replaces array references with their actual values.

    This visitor converts array references in expressions to their constant values.

    @param arrayMap: Dictionary mapping array names to their values.
    @type arrayMap: dict
    @param constantArray: List to store unique constants found during replacement.
    @type constantArray: list of str
    """
    def __init__(self,arrayMap,constantArray):
        self.arrayMap = arrayMap
        self.constantArray = constantArray

    def visit_BinaryOp(self,node):
        """
        @brief Replaces array references in binary operations with their constant values.

        @param node: The binary operation node containing the array reference.
        @type node: pycparser.c_ast.BinaryOp
        """
        if isinstance(node.right,c_ast.ArrayRef):
            arrName = node.right.name.name
            contents = self.arrayMap[arrName]
            value = contents[int(node.right.subscript.value)]
            node.right = c_ast.Constant(type='int',value=str(value))
        self.generic_visit(node)
    
    def visit_Constant(self,node):
        """
        @brief Converts constant values to decimal and stores unique constants.

        @param node: The constant node being processed.
        @type node: pycparser.c_ast.Constant
        """
        value = node.value
        if value.startswith("0x"):
            decVal = str(int(value[2:],16))
        else:
            decVal = value
        node.value = decVal
        const = "dec_" + decVal
        if const not in self.constantArray:
            self.constantArray.append("dec_" + decVal)

class ConstToVar(c_ast.NodeVisitor):
    """
    @brief Converts constant values in the AST to variable names.

    This visitor replaces constant values in assignments and binary operations with corresponding variable names.

    """
    def visit_Assignment(self,node):
        """
        @brief Replaces constant values in assignment operations with variable names.

        @param node: The assignment node being processed.
        @type node: pycparser.c_ast.Assignment
        """
        if isinstance(node.rvalue,c_ast.Constant):
            constName = node.rvalue.value
            node.rvalue = c_ast.ID(name="dec_" + constName + "_inp")
            return
        else:
            self.generic_visit(node)
    def visit_BinaryOp(self,node):
        """
        @brief Replaces constant values in binary operations with variable names.

        @param node: The binary operation node being processed.
        @type node: pycparser.c_ast.BinaryOp
        """
        if isinstance(node.right,c_ast.Constant):
            constName = node.right.value
            node.right = c_ast.ID(name="dec_" + constName + "_inp")
        if isinstance(node.left,c_ast.Constant):
            constName = node.left.value
            node.left = c_ast.ID(name="dec_" + constName + "_inp")

class ConstantMerger(c_ast.NodeVisitor):
    """
    @brief Merges constants into global variables and updates local variable mappings.

    This visitor consolidates constant values into global variables and updates local variable mappings accordingly.

    @param constToGlobalMap: Mapping of constant values to global variable names.
    @type constToGlobalMap: dict
    @param localToGlobalMap: Mapping of local variable names to global variable names.
    @type localToGlobalMap: dict
    """
    def __init__(self,constToGlobalMap,localToGlobalMap):
        self.constToGlobalMap = constToGlobalMap
        self.localToGlobalMap = localToGlobalMap

    def __getNameForConstants(self,value):
        """
        @brief Generates a unique name for constants based on their value.

        @param value: The constant value.
        @type value: str
        @return: A unique name for the constant.
        @rtype: str
        """
        if value.startswith("0x"):
            return "hex" + value[2:]
        else: 
            return "dec" + value

    def visit_Assignment(self,node):
        """
        @brief Converts constant values in assignments to global variable names.

        @param node: The assignment node being processed.
        @type node: pycparser.c_ast.Assignment
        """
        if isinstance(node.rvalue,c_ast.Constant):
            constValue = node.rvalue.value
            idConstValue = self.__getNameForConstants(constValue)
            if constValue not in self.constToGlobalMap:
                self.constToGlobalMap[constValue] = idConstValue
            self.localToGlobalMap[node.lvalue.name] = idConstValue
        if isinstance(node.rvalue,c_ast.BinaryOp):
            constName = node.rvalue.right.name
            node.rvalue.right.name = self.localToGlobalMap[constName]

class AssignmentChecker(c_ast.NodeVisitor):
    """
    @brief Checks for multiple instantiations of the same variable in assignments.

    This visitor detects if a variable is assigned multiple times in the code.

    @param mp: Dictionary to track variables and their assignment status.
    @type mp: dict
    """
    mp = {}
    def visit_Assignment(self,node):
        """
        @brief Detects multiple instantiations of the same variable.

        @param node: The assignment node being processed.
        @type node: pycparser.c_ast.Assignment
        """
        if isinstance(node.lvalue,c_ast.ID):
            if node.lvalue.name in self.mp:
                print(f"{node.lvalue.name} instantiated twice")
            else:
                self.mp[node.lvalue.name] = True
