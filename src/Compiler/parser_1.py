#assumptions:
##############################################################################################
# -- Unhandled sequentiality
# -- Handling bool
# manual effort: replace return type with void
#                use: python3 parser_1.py --type=int

import argparse
from pycparser import parse_file
from pycparser import c_ast
from utils import processFunctions,writeVerilogToFile
import json

if __name__ == "__main__":
    """
    @brief The main entry point of the script that parses C code to generate Verilog code.

    This script reads a JSON configuration file for input arguments, parses C code using `pycparser`,
    processes functions to extract information, and writes the resulting Verilog code to a file.

    The script assumes certain conditions for sequentiality and boolean handling, which need to be manually addressed.

    @raises FileNotFoundError: If the JSON configuration file or input C code file cannot be found.
    @raises KeyError: If required keys are missing in the JSON configuration file.
    """
    with open('./systemArgs.json', 'r') as file:
        args = json.load(file)
    
    width = str(args["bitWidth"] - 1)
    functions = {}
    functionCalls = {}
    ast = parse_file(args["postProcessorOutput"], use_cpp=True)
    # print(ast)
    intermediateAssignments = {}

    for fDef in ast.ext:
        if isinstance(fDef,c_ast.FuncDef):
            processFunctions(functions,fDef,functionCalls,intermediateAssignments)
    
    for fName in functions:
        writeVerilogToFile(fName,functions,intermediateAssignments[fName],functionCalls,args["generatedRtl"],width)
        