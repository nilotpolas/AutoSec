from copy import deepcopy
import os
from pycparser import parse_file, c_generator
import pycparser.c_ast as cast

"""
@brief Main script for parsing a C file, modifying its AST, and saving the updated C file.

This script parses a C source file, processes the function definitions to replace function call outputs
with modified declarations and assignments, and writes the modified AST back to a new C source file.

@details
- Parses a C file using pycparser.
- Updates function calls by introducing new variable declarations and assignments.
- Generates a new C file with the updated AST.

@file
This script is designed to work with C files and requires the `pycparser` library.
"""

if __name__ == "__main__":
    filepath = '../test/composibility/mult4.c'
    ast = parse_file(filepath, use_cpp=False)
    all_functions = ast.ext
    func_def = all_functions[0]
    func_call_outputs = []
    new_block_items = []
    type_decl = {}
    for line in func_def.body.block_items:
        if isinstance(line, cast.Decl):
            type_decl[line.name] = line
        if isinstance(line, cast.Assignment):
            lhs = line.lvalue
            rhs = line.rvalue
            if isinstance(rhs, cast.FuncCall):
                func_call_outputs.append(lhs.name)
                for arg in rhs.args:
                    if (arg.name in func_call_outputs):
                        new_decl = deepcopy(type_decl[arg.name])
                        new_decl.type.declname = f"{arg.name}_prime"
                        new_block_items.insert(0, new_decl)
                        new_block_items.append(cast.Assignment('=', cast.ID(
                            f"{arg.name}_prime"), cast.FuncCall(cast.ID('reg'), cast.ExprList([cast.ID(arg.name)]))))
                        arg.name = f"{arg.name}_prime"
                new_block_items.append(line)
        else:
            new_block_items.append(line)
    func_def.body.block_items = new_block_items
    c_gen = c_generator.CGenerator()
    rslt = c_gen.visit(ast)
    new_filepath = f"{filepath[:-2]}_output.c"
    with open(new_filepath, 'w+') as fptr:
        print(rslt, file=fptr)
