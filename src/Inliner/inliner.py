
import sys
import json
from DiGraph import DiGraph
from Visitors import FunctionVisitor,DeclVisitor,ArrayValueReplacer,AssignmentChecker,ConstToVar
from utils import extractFunctionInfo,processDependantFunctions,generate_c_file,insertAssignmentsAndDeclForConstants

sys.path.extend(['.', '..'])

from pycparser import parse_file, c_ast

def mainInline(inputFile,outputFile,topModule):
    """
    @brief Processes a C source file to inline functions, handle constants, and generate a new C file.

    This function parses the provided C source file, constructs a directed graph of functions, performs topological
    sorting, processes functions based on dependencies, handles array and constant values, and finally generates
    an updated C source file.

    @param inputFile: The path to the input C source file to be processed.
    @type inputFile: str
    @param outputFile: The path where the processed C source file will be saved.
    @type outputFile: str
    @param topModule: The name of the top-level module (function) to be used as the entry point.
    @type topModule: str

    @raises SystemExit: If the top module is not found in the sorted function list or if no functions are present.
    """
    ast = parse_file(inputFile, use_cpp=True)
    arrMap = {}
    arrVisitor = DeclVisitor(arrayMap=arrMap,ast=ast)
    arrVisitor.visit(ast)
    functionGraph = DiGraph()
    functionInfo = {}

    for fDef in ast.ext:
        if isinstance(fDef,c_ast.FuncDef):
            functionGraph.addFunction(fDef.decl.name)
            visitor = FunctionVisitor(functionGraph,fDef.decl.name)
            visitor.visit(fDef)

    sortedList = functionGraph.topoSort()
    if topModule not in sortedList:
        print(f"No top module named {topModule} in given input file.")
        print("Note : The name of module is case sensitive")
        sys.exit(1)
    if(len(sortedList) == 1):
        generate_c_file(ast,outputFile)


    for function in sortedList:
        inDegree = functionGraph.getIndegreeOf(function)
        if inDegree == 0:
            for fDef in ast.ext[:]:
                if isinstance(fDef,c_ast.FuncDef) and fDef.decl.name == function:
                    extractFunctionInfo(fDef,functionInfo)
                    ast.ext.remove(fDef)
                    break
        
        elif function != topModule:
            for fDef in ast.ext[:]:
                if isinstance(fDef,c_ast.FuncDef) and fDef.decl.name == function:
                    processDependantFunctions(fDef,functionInfo,False)
                    extractFunctionInfo(fDef,functionInfo)
                    ast.ext.remove(fDef)
                    break
        else:
            for fDef in ast.ext[:]:
                if isinstance(fDef,c_ast.FuncDef) and fDef.decl.name == function:
                    processDependantFunctions(fDef,functionInfo,True)
    
    for fDef in ast.ext[:]:
        if isinstance(fDef,c_ast.Decl) and isinstance(fDef.type,c_ast.ArrayDecl):
            ast.ext.remove(fDef)

    constArr = []
    arrValueReplacer = ArrayValueReplacer(arrMap,constArr)
    arrValueReplacer.visit(ast)

    constToVar = ConstToVar()
    constToVar.visit(ast)
    insertAssignmentsAndDeclForConstants(ast,constArr)

    assignmentChecker = AssignmentChecker();
    assignmentChecker.visit(ast)
    generate_c_file(ast,outputFile)



if __name__ == "__main__":
    with open('./systemArgs.json', 'r') as file:
        args = json.load(file)
    mainInline(args['inputFile'],args["inlinerOutput"],args['topModule'])