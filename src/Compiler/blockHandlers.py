from pycparser import c_ast

# Define a function to recursively reconstruct expressions from AST nodes
def reconstruct_expression(node,internalVariables):
    """
    @brief Recursively reconstructs expressions from AST nodes.

    This function converts AST nodes into a string representation of the expression they represent. It supports binary operations, unary operations, constants, identifiers, and function calls.

    @param node: The AST node representing an expression.
    @type node: pycparser.c_ast.Node
    @param internalVariables: A dictionary to store and manage internal variables.
    @type internalVariables: dict
    @return: A string representing the reconstructed expression.
    @rtype: str
    @raises ValueError: If the node type is unsupported.
    """
    if isinstance(node, c_ast.BinaryOp):
        leftExpr = reconstruct_expression(node.left,internalVariables)
        rightExpr = reconstruct_expression(node.right,internalVariables)
        return f"({leftExpr} {node.op} {rightExpr})"
    elif isinstance(node, c_ast.ID):
        return node.name
    elif isinstance(node,c_ast.Constant):
        return node.value
    elif isinstance(node,c_ast.UnaryOp):
        return "!" + reconstruct_expression(node.expr,internalVariables)
    elif isinstance(node,c_ast.FuncCall):
        if node.name.name == "reg":
            varName = str(node.args.exprs[0].name) + "_reg";
            if varName not in internalVariables:
                internalVariables[varName] = {
                    "type" : "reg",
                    "value" : str(node.args.exprs[0].name)
                }
            return varName;
    else:
        raise ValueError(f"Unsupported node type: {type(node).__name__}")

#block handlers for corresponding blocks/nodes
def handleDeclBlock(node,internalVariables):
    """
    @brief Handles declaration blocks in the AST and updates internal variables.

    This function processes declaration nodes to determine the type of the variable (either "reg" or "wire") and reconstructs its initial value.

    @param node: The declaration node being processed.
    @type node: pycparser.c_ast.Decl
    @param internalVariables: A dictionary to store and manage internal variables.
    @type internalVariables: dict
    @return: Boolean indicating if a register variable is present.
    @rtype: bool
    """
    regPresent = False
    if node.name not in internalVariables:
        internalVariables[node.name] = {
            "type" : "",
            "value" : ""
        }
    if isinstance(node.init,c_ast.FuncCall) and node.init.name.name == "reg":
        internalVariables[node.name]["type"] = "reg"
        regPresent = True
        exp = reconstruct_expression(node.init.args.exprs[0],internalVariables)
    else:
        internalVariables[node.name]["type"] = "wire"
        exp = reconstruct_expression(node.init,internalVariables)
    internalVariables[node.name]["value"] = exp
    return regPresent

def handleAssignmentBlock(node,internalVariables):
    """
    @brief Handles assignment blocks in the AST and updates internal variables.

    This function processes assignment nodes to determine the type of the variable (either "reg" or "wire") and reconstructs its assigned value.

    @param node: The assignment node being processed.
    @type node: pycparser.c_ast.Assignment
    @param internalVariables: A dictionary to store and manage internal variables.
    @type internalVariables: dict
    @return: Boolean indicating if a register variable is present.
    @rtype: bool
    """
    regPresent = False
    lval = node.lvalue.name if isinstance(node.lvalue,c_ast.ID) else node.lvalue.expr.name
    
    if isinstance(node.rvalue,c_ast.FuncCall) and node.rvalue.name.name == "reg":
        exp = reconstruct_expression(node.rvalue.args.exprs[0],internalVariables)
        internalVariables[lval] = {}
        internalVariables[lval]["type"] = "reg"
        regPresent = True
    else:
        exp = reconstruct_expression(node.rvalue,internalVariables)
        internalVariables[lval] = {}
        if isinstance(node.lvalue,c_ast.UnaryOp):
            internalVariables[lval]["type"] = "reg"
            regPresent = True
        else:
            internalVariables[lval]["type"] = "wire"
        
    internalVariables[lval]["value"] = exp
    return regPresent

def handleReturnBlock(node,internalVariables,functions,fName):
    """
    @brief Handles return blocks in the AST and updates function outputs.

    This function processes return nodes to identify output variables and updates the function's output list or internal variables accordingly.

    @param node: The return node being processed.
    @type node: pycparser.c_ast.Return
    @param internalVariables: A dictionary to store and manage internal variables.
    @type internalVariables: dict
    @param functions: A dictionary containing function information.
    @type functions: dict
    @param fName: The name of the function being processed.
    @type fName: str
    """
    if isinstance(node.expr,c_ast.ID):
        if node.expr.name not in functions[fName]["outputs"]:
            functions[fName]["outputs"].append(node.expr.name)
    elif isinstance(node.expr, c_ast.BinaryOp):
        internalVariables["r_val"] = {}
        internalVariables["r_val"]["type"] = "wire"
        internalVariables["r_val"]["value"] = reconstruct_expression(node.expr,internalVariables)

def handleFuncCallBlock(node,functions,fName,functionCalls,internalVariables):
    """
    @brief Handles function call blocks in the AST and updates the function calls list.

    This function processes function call nodes to record the function instance, parameter list, and update the function call information.

    @param node: The function call node being processed.
    @type node: pycparser.c_ast.FuncCall
    @param functions: A dictionary containing function information.
    @type functions: dict
    @param fName: The name of the function making the call.
    @type fName: str
    @param functionCalls: A dictionary to store function calls information.
    @type functionCalls: dict
    @param internalVariables: A dictionary to store and manage internal variables.
    @type internalVariables: dict
    """
    called = functions[fName]["called"];
    called = called + 1
    inst = node.name.name + str(called)
    functions[fName]["called"] = called
    paramList = []
    paramList.append("clk")
    for expr in node.args.exprs:
        if isinstance(expr,c_ast.UnaryOp):
            exp = reconstruct_expression(expr.expr,internalVariables)
        else:
            exp = reconstruct_expression(expr,internalVariables)
        paramList.append(exp)
    functionCalls[fName].append({
        "instanceName" : inst,
        "paramList" : paramList,
        "callee" : node.name.name
    })