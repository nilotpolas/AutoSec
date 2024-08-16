# ----------------------------------------------------------------------------------------------------------#
#  main file working the parser that constructs the dfg for a dom-c function and makes it hls ready        #
# use: python3 ./main.py  --filename=../test/AES/DOM/Linear/input.c --useLinearAlgorithm=True --outputFilename=../test/AES/DOM/Linear/output.c
# ----------------------------------------------------------------------------------------------------------#
import argparse
import json
import os
import modules
from modules.AddRegVisitor import AddRegVisitor
from modules.CrossDomainOp import CrossDomainOp
from modules.GenerateDFG import GenerateDFG
from modules.GraphNode import ASTGraphNode, BaseGraphNode, TextGraphNode
from modules.MyCGenerator import MyCGenerator
from modules.Retime import RetimeDFG
import rustworkx as rx
from pycparser import parse_file, c_generator
import pycparser.c_ast as cast
from rustworkx.visualization import graphviz_draw
from modules.utils import add_dummy_node_fan_out, add_source_sink, extract_func_body, file_exists, generate_c_file, save_graph,checkBalancing
from modules.utils import noOfRegistersManually
import time,sys

"""
@brief Main script for processing a C file into a data flow graph (DFG) and preparing it for high-level synthesis (HLS).

This script:
- Parses a C file to extract and process function definitions.
- Constructs a DFG from the function's AST.
- Adds source and sink nodes to the DFG.
- Adds dummy nodes for fan-out and calculates manual register requirements.
- Optionally, retimes the DFG and adds register calls.
- Generates a new C file with updated code based on the modified DFG.
- Saves visualization of the graph for analysis.

@details
- This script expects a configuration file `systemArgs.json` for input parameters.
- The script can be modified to include or exclude certain steps like checking balancing or saving graphs.

@file
Ensure that all required modules and dependencies are installed and properly configured.
"""

if __name__ == "__main__":
    with open('./systemArgs.json', 'r') as file:
        args = json.load(file)

    start_time = time.time()
    fileToParse = args["postProcessorOutput"] if(args["checkBalancing"])  else args["inlinerOutput"]
    ast = parse_file(fileToParse, use_cpp=True)
    func_body = extract_func_body(ast)

    dfg_gen = GenerateDFG()
    dfg_gen.visit(ast)
    add_source_sink(dfg_gen.dfg)
    add_dummy_node_fan_out(dfg_gen.dfg,dfg_gen.nodesInfo,dfg_gen.nameIndexMap)

#---------------------------------------------------------------------
    if(args["checkBalancing"]):
        checkBalancing(dfg_gen.dfg) 
        sys.exit(0)
#---------------------------------------------------------------
    # save_graph(dfg_gen.dfg, "graph.png")
    manualRegisters = noOfRegistersManually(dfg_gen.dfg)
    print("----------Nodes and edges------------")
    print(dfg_gen.dfg.num_nodes())
    print(dfg_gen.dfg.num_edges())
    print("-------------------------------------")
    useLinearAlgo = "true"
    retimer = RetimeDFG(dfg_gen.dfg)
    retimer.set_source_sink_weight(useLinearAlgo)
    retimer.update_retiming_labels()
    retimer.update_edge_weights()
    # retimer.printRetimedLabels()
    # retimer.printEdgeWeights()
    # save_graph(dfg_gen.dfg, "graph2.png")
    retimer.add_reg_calls(useLinearAlgo)
    print("No of registers if added levelwise: ",end="")
    print(manualRegisters)

    generate_c_file(ast,args["retimedOutput"])
    print("Execution Time")
    print("--- %s seconds ---" % (time.time() - start_time))