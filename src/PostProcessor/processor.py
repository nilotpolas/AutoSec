# use: python3 processor.py --type=int > output.c for AES design
import sys
import json
import argparse
sys.path.extend(['.', '..'])


from pycparser import parse_file, c_ast
from utils import handleAssignmentNodes,changeBinaryOps,getNewVarName,isRegCall,generate_c_file
from astNodes import getDeclarationNode,getSimpleAssignmentNode
from Visitor import NegationVisitor,UnaryOpNodeChanger,BinaryOpInRegHandler,SourceRegHandler
import globalVariables

"""
@brief Processes C code to handle specific operations and generate modified output.

This script:
- Parses a C file into an abstract syntax tree (AST).
- Applies transformations to handle unary operations, source registers, and nested operations.
- Generates a new C file with the transformations applied.

@details
1. Handles unary operations by replacing variables and updating the AST.
2. Processes source registers to manage variable assignments and their usage.
3. Changes binary operations to handle nested register calls.
4. Updates assignments and generates a new C file with the processed AST.

@file
Ensure that `pycparser` and custom modules are properly installed and configured.
"""

def postProcess(inputFile,outputFile):
    """
    Processes the input C file, applies transformations, and generates the output C file.

    @param inputFile: Path to the input C file to be processed.
    @param outputFile: Path to the output C file where the processed code will be saved.

    @raises FileNotFoundError: If the input file does not exist.
    @raises IOError: If there is an issue with file reading or writing.
    """

    assgnNo = 1
    ast = parse_file(inputFile, use_cpp=True)
    bodyNodes = []
    with open('systemArgs.json', 'r') as file:
        json_data = file.read()
    operatorNameMap = json.loads(json_data)

#handling unary ops
    negationVisitor = NegationVisitor(bodyNodes)
    negationVisitor.visit(ast)
    assgnNo = negationVisitor.assgnNo
    ast.ext[0].body.block_items = bodyNodes
    bodyNodes = []

    unaryOpNodeChanger = UnaryOpNodeChanger(negationVisitor.unaryVarToNameMap)
    unaryOpNodeChanger.visit(ast)

#handling source regs
    sourceRegHandler = SourceRegHandler(bodyNodes,assgnNo)
    sourceRegHandler.visit(ast)
    assgnNo = sourceRegHandler.assignNo
    ast.ext[0].body.block_items = bodyNodes
    bodyNodes = []

#handling nested reg binary op inside a reg call
    binaryOpInRegHandler = BinaryOpInRegHandler(bodyNodes,assgnNo)
    binaryOpInRegHandler.visit(ast)
    assgnNo = binaryOpInRegHandler.assignNo
    ast.ext[0].body.block_items = bodyNodes
    bodyNodes = []

#handling nested reg binary op
    for node in ast.ext[0].body.block_items:
        if not isinstance(node,c_ast.Assignment):
            bodyNodes.append(node)
        else:
            changeBinaryOps(node,bodyNodes,assgnNo)
            assgnNo += 2
    ast.ext[0].body.block_items = bodyNodes
    # # print(ast)

    bodyNodes = []
    for node in ast.ext[0].body.block_items:
        if not isinstance(node,c_ast.Assignment):
            bodyNodes.append(node)
        else:
            handleAssignmentNodes(node,bodyNodes,operatorNameMap,assgnNo)
            assgnNo += 2
    # print(bodyNodes)
    ast.ext[0].body.block_items = bodyNodes
    # print(ast)
    generate_c_file(ast,outputFile)


if __name__ == "__main__":
    """
    Main execution block for processing command-line arguments and invoking the post-process function.

    @raises FileNotFoundError: If the system arguments file is missing.
    @raises KeyError: If required keys are missing from the system arguments file.
    """
    with open('./systemArgs.json', 'r') as file:
        args = json.load(file)
    
    global globalType
    globalVariables.globalType = '_Bool' if args["bitWidth"] == 1 else 'int'
    # print(globalVariables.globalType)

    postProcess(args["retimedOutput"],args["postProcessorOutput"])