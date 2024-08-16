import json
import os
import pycparser.c_ast as cast
import rustworkx as rx
from rustworkx.visualization import graphviz_draw
from modules.CrossDomainOp import CrossDomainOp
from modules.GraphNode import ASTGraphNode, BaseGraphNode, TextGraphNode
from modules.MyCGenerator import MyCGenerator
import copy

paths = []
def get_func_call_ast(func_name: str, func_arg: cast.Node):
    """
    @brief Creates an abstract syntax tree (AST) for a function call with the given
           function name and argument.

    @param func_name The name of the function to call.
    @param func_arg The argument to pass to the function.

    @return An AST node representing the function call.
    """
    return cast.FuncCall(name=cast.ID(name=func_name), args=cast.ExprList(
        exprs=[
            func_arg
        ]
    ))


def save_graph(graph: rx.PyDiGraph, name: str):
    """
    @brief Renders a directed graph and saves it as an image file with the given
           name.

    @param graph A directed graph to render and save.
    @param name The name of the file to save the image as.

    @return None

    @raises graphviz.backend.ExecutableNotFound If the Graphviz executable is not found on the system.
    """
    def node_attr(node):
        if (isinstance(node, BaseGraphNode)):
            return node.node_attr()
        return {}

    def edge_attr(edge):
        if (edge is not None):
            return {"label": f"{edge}"}
        return {}

    fig = graphviz_draw(graph, node_attr_fn=node_attr,
                        edge_attr_fn=edge_attr, method="dot")
    fig.save(name)
    print("Saving graph")


def file_exists(filename: str):
    """
    @brief Checks if a file exists and raises an exception if it doesn't.

    @param filename The name of the file to check.

    @return None

    @raises IOError If the file does not exist.
    """
    if (not os.path.exists(filename)):
        raise IOError(f"File {filename} not found")


def read_json(filename: str) -> dict:
    """
    @brief Reads a JSON file and returns the parsed content.

    @param filename The name of the JSON file to read.

    @return The parsed content of the JSON file.

    @raises IOError If the file does not exist.
    """
    with open(filename) as file:
        json_map = json.load(file)
    return json_map


def extract_func_body(ast: cast.FileAST) -> cast.Compound:
    """
    @brief Extracts the body of the first function present in the AST.

    @param ast AST representing the entire C file.

    @return Body of the first function.
    """
    # only the 0th entry of the ast has the function body information for a single function
    first_ext = ast.ext[0]
    func_body = first_ext.body
    return func_body


def generate_c_file(ast,filename):
    """
    @brief Generates C code from the provided Abstract Syntax Tree (AST) using MyCGenerator,
           and saves the generated code to a file.

    @param ast The Abstract Syntax Tree (AST) to generate C code from.
    @param filename The name of the file to save the generated C code.
    
    @return None
    """
    generator = MyCGenerator()
    with open(filename, 'w') as output_file:
        print(generator.visit(ast), file=output_file)


def add_source_sink(graph: rx.PyDiGraph):
    """
    @brief Adds a source node, a sink node, and edges to connect each non-source/sink node to either the source or sink node in the given Rust PyDiGraph.
           An edge is added from the source node to any node with zero incoming edges, and an edge is added from any node with zero outgoing edges to the sink node.
           The function modifies the input graph in-place.

    @param graph The directed graph to modify.

    @return None
    """
    source_index = graph.add_node(TextGraphNode("Source"))
    sink_index = graph.add_node(TextGraphNode("Sink"))
    for node_index in graph.node_indices():
        if (node_index == source_index or node_index == sink_index):
            continue
        if (graph.in_degree(node_index) == 0):
            graph.add_edge(source_index, node_index, 0)
        if (graph.out_degree(node_index) == 0):
            graph.add_edge(node_index, sink_index, 0)

    graph.add_edge(sink_index, source_index, 0)

def add_dummy_node(dfgCopy: rx.PyDiGraph):
    """
    @brief Adds a dummy node in the given dataflow graph after any AST node whose rvalue is annotated using CrossDomainOp.
           The added node is connected to the original node with a single edge.

    @param dfgCopy The directed graph to modify.

    @return None
    """
    existing_nodes = dfgCopy.node_indices()
    for node_index in existing_nodes:
        node = dfgCopy[node_index]
        # Nodes could either be ASTGraphNode or TextGraphNode
        if (isinstance(node, ASTGraphNode)):
            ast_node = node.ast

            # If the rvalue is annotated using CrossDomainOp, it means a dummy node
            # has to be added after the current node
            if (isinstance(ast_node.rvalue, CrossDomainOp)):
                dummy_node = dfgCopy.add_node(TextGraphNode("Dummy"))
                # Update node weight of cross domain operation
                node.node_weight = 1
                dfgCopy[dummy_node].node_weight = 1
                dfgCopy.insert_node_on_out_edges(dummy_node, node_index)
                # insert_node_on_out_edges() can add multiple edges between
                # current node and newly added node, hence we remove the
                # extra edges and keep only one
                while len(dfgCopy.successor_indices(node_index)) > 1:
                    dfgCopy.remove_edge(node_index, dummy_node)


def add_dummy_nodes_fan_out(dfgCopy: rx.PyDiGraph):
    """
    @brief Adds three dummy nodes to the outgoing edges of each ASTGraphNode in the graph if the
           rvalue of the node's AST is annotated using CrossDomainOp. The dummy nodes are added
           between the ASTGraphNode and its neighboring nodes, and the outgoing edges from the
           ASTGraphNode are redirected to the first dummy node in the chain. The first dummy node in the chain has node weight = 1, the other two have 0.
           The edge weight between the last two dummy nodes is = 1 to avoid redundant registers from being added when there are multiple cross-domain products in series.

    @param dfgCopy The directed graph to modify.

    @return None
    """
    existing_nodes = dfgCopy.node_indices()
    for node_index in existing_nodes:
        node = dfgCopy[node_index]
        if (isinstance(node, ASTGraphNode)):
            ast_node = node.ast

            # If the rvalue is annotated using CrossDomainOp, it means a dummy node
            # has to be added after the current node
            if (isinstance(ast_node.rvalue, CrossDomainOp)):
                out_edges = dfgCopy.out_edges(node_index)
                for out_edge in out_edges:
                    edge_neigh = out_edge[1]
                    dfgCopy.remove_edge(node_index, edge_neigh)
                    dummy_nodes = add_line_graph(dfgCopy, 3)
                    # Set node weight of current node and first dummy node to 1
                    node.node_weight = 1
                    dfgCopy[dummy_nodes[0]].node_weight = 1
                    # Edge weight between last two dummy nodes = 1
                    dfgCopy.update_edge(dummy_nodes[-2], dummy_nodes[-1], 1)
                    # Appropriately add the edge that was removed from current node and its neighbour
                    dfgCopy.add_edge(node_index, dummy_nodes[0], 0)
                    dfgCopy.add_edge(dummy_nodes[-1], edge_neigh, 0)


def add_line_graph(dfgCopy: rx.PyDiGraph, num=1) -> list[int]:
    """
    @brief Adds a line graph to an existing directed graph.

    @param dfgCopy The directed graph to add the line graph to.
    @param num The number of nodes to add to the line graph. Defaults to 1.

    @return A list of the indices of the nodes added to the line graph.
    """
    add_node_idx = []
    for i in range(num):
        idx = dfgCopy.add_node(TextGraphNode("Dummy"))
        add_node_idx.append(idx)

    for i in range(num-1):
        dfgCopy.add_edge(add_node_idx[i], add_node_idx[i+1], 0)

    return add_node_idx

def addDummyNodeBetween(dfgCopy,node_index,edge_neigh,node):
    """
    @brief Adds a dummy node between the specified nodes and updates the edges accordingly.

    @param dfgCopy The directed graph to modify.
    @param node_index The index of the current node.
    @param edge_neigh The index of the neighboring node.
    @param node The current node.

    @return None
    """
    dfgCopy.remove_edge(node_index, edge_neigh)
    dummy_node = dfgCopy.add_node(TextGraphNode("Dummy"))
    node.node_weight = 0
    dfgCopy[dummy_node].node_weight = 1
    dfgCopy.add_edge(node_index, dummy_node, 0)
    dfgCopy.add_edge(dummy_node, edge_neigh, 0)

    #3 nodes
    # dfgCopy.remove_edge(node_index, edge_neigh)
    # dummy_nodes = add_line_graph(dfgCopy, 4)
    # # Set node weight of current node and first dummy node to 1
    # node.node_weight = 1
    # dfgCopy[dummy_nodes[0]].node_weight = 1
    # # Edge weight between last two dummy nodes = 1
    # dfgCopy.update_edge(dummy_nodes[-2], dummy_nodes[-1], 1)
    # # Appropriately add the edge that was removed from current node and its neighbour
    # dfgCopy.add_edge(node_index, dummy_nodes[0], 0)
    # dfgCopy.add_edge(dummy_nodes[-1], edge_neigh, 0)

def add_dummy_node_fan_out(dfgCopy: rx.PyDiGraph,nodesInfo,nameIndexMap):
    """
    @brief Adds a single dummy node to the outgoing edges of each ASTGraphNode in the given PyDiGraph.
           The function iterates over all the nodes in the PyDiGraph and checks if the node is an instance of ASTGraphNode.
           If the rvalue of the AST node is annotated using CrossDomainOp, a single dummy node is added after the current node.
           The function then adds an edge from the current node to the dummy node, and another edge from the dummy node to the original outgoing nodes.

    @param dfgCopy The directed graph to modify.
    @param nodesInfo A dictionary containing information about nodes.
    @param nameIndexMap A dictionary mapping node names to their indices.

    @return None
    """
    existing_nodes = dfgCopy.node_indices()
    for node_index in existing_nodes:
        node = dfgCopy[node_index]
        
        # Nodes could either be ASTGraphNode or TextGraphNode
        if (isinstance(node, ASTGraphNode)):
            # ast_node = node.ast
            nodeInfo = nodesInfo[node_index]
            # If the rvalue is annotated using CrossDomainOp, it means a dummy node
            # has to be added after the current node
            inputRegisters = nodeInfo["inputRegisters"]
            
            if inputRegisters:
                inputRegisters = [nameIndexMap[reg_name] for reg_name in inputRegisters]
                in_edges = dfgCopy.in_edges(node_index)
                for in_edge in in_edges:
                    if in_edge[0] in inputRegisters:
                        addDummyNodeBetween(dfgCopy,in_edge[0],node_index,node)

            if (nodeInfo["hasOutputRegister"]):
                out_edges = dfgCopy.out_edges(node_index)
                for out_edge in out_edges:
                    addDummyNodeBetween(dfgCopy,node_index,out_edge[1],node)



def constructOperandMap(isInputReg,name):
    """
    @brief Constructs a map for operands indicating whether it is an input register
           and its name.

    @param isInputReg A boolean indicating if the operand is an input register.
    @param name The name of the operand.

    @return A dictionary containing the operand information.
    """
    return {
        "isInputReg" : isInputReg,
        "name" : name
    }

def is_reg_call(node):
    """
    @brief Checks if a node is a call to the `reg()` function.

    @param node The node to check.

    @return True if the node is a function call to `reg`, False otherwise.
    """
    
    if (isinstance(node, cast.FuncCall) and node.name.name == 'reg'):
        return True
    return False

def extract_left_and_right_operands(node):
    """
    @brief Extracts the left and right operands from a node, which could be a binary operation,
           a function call, or an identifier.

    @param node The node to extract operands from.

    @return A list containing the left and right operands, if they exist. 
            If the node is a function call, it returns a dictionary with operand information.
            If the node is an identifier, it returns a dictionary with the identifier name.
    """
    if (isinstance(node, cast.BinaryOp)):
        leftOperand = extract_left_and_right_operands(node.left) 
        rightOperand = extract_left_and_right_operands(node.right) 
        return [leftOperand,rightOperand]
    elif is_reg_call(node):
        if isinstance(node.args.exprs[0], cast.ID):
            reg_operand = constructOperandMap(True,node.args.exprs[0].name)
        else:
            reg_operand = extract_left_and_right_operands(node.args.exprs[0])
        return reg_operand
    elif isinstance(node,cast.ID):
        return constructOperandMap(False,node.name)
    elif isinstance(node,cast.UnaryOp):
        return constructOperandMap(False,node.expr.name)

def get_source_index(dfgCopy: rx.PyDiGraph) -> int:
    """
    @brief Retrieves the index of the source node in the directed graph.

    @param dfgCopy The directed graph to search.

    @return The index of the source node. Raises an exception if source node is not found.
    """
    # print(dfgCopy.node_indices())
    for node_idx in dfgCopy.node_indices():
        node = dfgCopy[node_idx]
        
        if (isinstance(node, TextGraphNode) and node.label() == 'Source'):
            source_index = node_idx
    return source_index

def get_sink_index(dfgCopy: rx.PyDiGraph) -> int:
    """
    @brief Retrieves the index of the sink node in the directed graph.

    @param dfgCopy The directed graph to search.

    @return The index of the sink node. Raises an exception if sink node is not found.
    """
    for node_idx in dfgCopy.node_indices():
        node = dfgCopy[node_idx]
        if (isinstance(node, TextGraphNode) and node.label() == 'Sink'):
            sink_index = node_idx
    return sink_index

def dfs(wt,src,dest,dfgCopy: rx.PyDiGraph,maxWt):
    """
    @brief Performs a depth-first search to check if there's a path from the source to the destination
           with the specified weight.

    @param wt The current weight of the path.
    @param src The current node index.
    @param dest The destination node index.
    @param dfgCopy The directed graph to search.
    @param maxWt The maximum weight to compare against.

    @return True if a path with weight equal to maxWt is found, False otherwise.
    """
    if src==dest:
        return True if wt == maxWt else False
    neighbors = dfgCopy.out_edges(src)
    for neighbor in neighbors:
        wt += dfgCopy[neighbor[1]].node_weight
        balanced = dfs(wt,neighbor[1],dest,dfgCopy,maxWt)
        if not balanced:
            return False
        wt -= dfgCopy[neighbor[1]].node_weight

    return True

def is_dummy_node(node_index,dfg):
    """
    @brief Checks if a node is a dummy node in the directed graph.

    @param node_index The index of the node to check.
    @param dfg The directed graph containing the node.

    @return True if the node is a dummy node, False otherwise.
    """
    node = dfg[node_index]
    return isinstance(node, TextGraphNode) and node.node_text == 'Dummy'

def removeDummyNodes(dfg : rx.PyDiGraph):
    """
    @brief Removes dummy nodes from the graph and reconnects their incoming and outgoing edges.

    @param dfg The directed graph to modify.

    @return None
    """
    nodeList = dfg.node_indices()

    for node in nodeList:
        inEdges = dfg.in_edges(node)
        for inEdge in inEdges:
            if is_dummy_node(inEdge[0],dfg):
                dummyNode = inEdge[0]
                dfg.remove_edge(dummyNode,node)
                inComingNode = dfg.in_edges(dummyNode)[0][0]
                dfg.remove_edge(inComingNode,dummyNode)
                dfg.remove_node(dummyNode)
                dfg.add_edge(inComingNode,node,1)

#implementation can be optimized
def noOfRegistersManually(dfg : rx.PyDiGraph):
    """
    @brief Calculates the number of registers needed manually by analyzing the graph's structure.

    @param dfg The directed graph to analyze.

    @return The number of registers needed.
    """
    dfgCopy = copy.deepcopy(dfg)
    srcIndex = get_source_index(dfgCopy) 
    sinkIndex = get_sink_index(dfgCopy)
    dfgCopy.remove_edge(sinkIndex,srcIndex)
    registersNeededManually = 0
    maxLevel = 0

    removeDummyNodes(dfgCopy)
    
    sortedNodeList = rx.topological_sort(dfgCopy)
    levelOfNodes = [0 for _ in range(dfgCopy.num_nodes())]
    registerAfterLevel = {}

    for node in sortedNodeList:
        inEdges = dfgCopy.in_edges(node)
        outEdges = dfgCopy.out_edges(node)
        for edge in inEdges:
            levelOfNodes[node] = max(levelOfNodes[edge[0]] + 1,levelOfNodes[node])

        level = levelOfNodes[node]
        maxLevel = max(level,maxLevel)
        for edge in outEdges:
            if edge[2] == 1:
                registerAfterLevel[level] = True
    
    edgesCutThroughLevel = [0 for _ in range(maxLevel + 2)]
    edges = dfgCopy.edge_list()
    for edge in edges:
        l1 = levelOfNodes[edge[0]]
        l2 = levelOfNodes[edge[1]]
        edgesCutThroughLevel[l1] += 1
        edgesCutThroughLevel[l2] -= 1
    
    for i in range(1, len(edgesCutThroughLevel)):
        edgesCutThroughLevel[i] += edgesCutThroughLevel[i - 1]
    
    for key in registerAfterLevel:
        registersNeededManually += edgesCutThroughLevel[key]

    # for node in sortedNodeList:
    #     dfgCopy[node].node_weight = levelOfNodes[node]
    # save_graph(dfgCopy,"graph.png")

    return registersNeededManually

def checkBalancing(dfgCopy: rx.PyDiGraph):
    """
    @brief Checks if the design is balanced by analyzing the dummy nodes on all paths from source to sink.

    @param dfgCopy The directed graph to analyze.

    @return None
    """
    dfgCopy = copy.deepcopy(dfgCopy) # new copy of the dfg
    # check number of dummy  nodes on all paths from source to sink 
    srcIndex = get_source_index(dfgCopy) 
    sinkIndex = get_sink_index(dfgCopy)
    num_nodes = dfgCopy.num_nodes()
    
    # removing unwanted backedge to do topo sort
    dfgCopy.remove_edge(sinkIndex,srcIndex)
    max_path_weights = [0 for index in range(num_nodes)]
    sortedNodeList = rx.topological_sort(dfgCopy)
    for nodeIndex in sortedNodeList:
        # what is the max node weight from souce to that node till now
        inEdges = dfgCopy.in_edges(nodeIndex)
        maxWeightTillNode = 0
        for inEdge in inEdges:
            maxWeightTillNode = max(max_path_weights[inEdge[0]],maxWeightTillNode)
        if is_dummy_node(nodeIndex,dfgCopy):
            maxWeightTillNode += 1
        max_path_weights[nodeIndex] = maxWeightTillNode
    max_path_weight = max(max_path_weights)
    balanced = dfs(0,srcIndex,sinkIndex,dfgCopy,max_path_weight)
    if balanced:
        print("Design is balanced")
    else:
        print("Design is not balanced")