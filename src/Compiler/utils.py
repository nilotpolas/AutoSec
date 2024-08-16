from pycparser import c_ast
from blockHandlers import handleDeclBlock,handleAssignmentBlock,handleReturnBlock,handleFuncCallBlock
import sys

def writeVerilogToFile(funcName, functions, internalVariables, functionCalls, filename,width):
    #width = " [7:0] " if width=='int' else " "
    """
    @brief Writes the Verilog code for a given function to a file.

    This function generates a Verilog module for the specified function based on its inputs, outputs,
    intermediate variables, and function calls. It writes the module declaration, input and output ports,
    intermediate value declarations, wire and reg assignments, and instantiations of other modules.

    @param funcName: The name of the function for which the Verilog code is generated.
    @param functions: A dictionary containing information about functions, including their inputs, outputs, and parameter order.
    @param internalVariables: A dictionary of internal variables used in the function, including their types and values.
    @param functionCalls: A dictionary of function calls made within the function, including the instance names and parameter lists.
    @param filename: The name of the file to which the Verilog code will be written.
    @param width: The bit width for the variables. If '0', no width is added; otherwise, a range is added to the variable declaration.

    @raises IOError: If the file cannot be opened or written to.
    """
    width = " " if width=='0' else " [" + width + ":0] "
    with open(filename, 'w') as file:
        # Redirect print output to the file
        print("module " + funcName + "(", file=file)
        for ip in functions[funcName]["inputs"]:
            print("    " + ip + ",", file=file)
        for op in functions[funcName]["outputs"]:
            print("    " + op + ",", file=file)
        print(");", file=file)

        print("//INPUTS", file=file)
        for ip in functions[funcName]["inputs"]:
            if (ip=="clk"):
                print("    input " +ip + ";", file=file)
            else:
                print("    input " + width +ip + ";", file=file)

        print("//OUTPUTS", file=file)
        for op in functions[funcName]["outputs"]:
            if internalVariables[op]["type"] == "reg":
                print("    output reg " + width + op + ";", file=file)
            else:
                print("    output " + width + op + ";", file=file)

        # intermediate value decl
        print("//Intermediate values", file=file)
        for key in internalVariables.keys():
            if key not in functions[funcName]["outputs"]:
                print("    " + internalVariables[key]["type"] + width + key + ";", file=file)

        # wire assignments
        print("", file=file)
        for key in internalVariables.keys():
            if internalVariables[key]["type"] == "wire":
                print("    assign " + key + " = " + internalVariables[key]["value"] + ";", file=file)

        # reg assignments
        print("", file=file)
        if functions[funcName]["regPresent"] is True:
            print("    always @(posedge clk) begin", file=file)
            for key in internalVariables.keys():
                if internalVariables[key]["type"] == "reg":
                    print("        " + key + " <= " + internalVariables[key]["value"] + ";", file=file)
            print("    end", file=file)

        # module instantiations
        print("", file=file)
        for func_calls in functionCalls[funcName]:
            callee = func_calls["callee"]
            inst = func_calls["instanceName"]
            paramList = func_calls["paramList"]
            print("    " + callee + " " + inst + "(", end="", file=file)
            paramOrder = functions[callee]["paramOrder"]
            for i in range(len(paramOrder)):
                print("." + paramOrder[i] + "(" + paramList[i] + ")", end="", file=file)
                if i != len(paramOrder) - 1:
                    print(", ", end="", file=file)
                else:
                    print(");", file=file)

        print("endmodule", file=file)
        print("",file=file)


def processFunctions(functions,fDef,functionCalls,intermediateAssignments):
    """
    @brief Processes a function definition to extract its inputs, outputs, intermediate variables, and function calls.

    This function analyzes the function definition to build a dictionary of function information, including
    the inputs, outputs, and function calls. It also updates intermediate variable assignments based on the function body.

    @param functions: A dictionary to store information about functions, including their inputs, outputs, and parameter order.
    @param fDef: The function definition node from the C Abstract Syntax Tree (AST).
    @param functionCalls: A dictionary to store function calls made within the function.
    @param intermediateAssignments: A dictionary to store intermediate variable assignments for the function.

    @raises ValueError: If the return type of the function is other than `void`.
    """
    regPresent = False
    function_decl = fDef.decl
    fName = function_decl.name
    functions[fName] = {
        "inputs" : [],
        "outputs" : [],
        "paramOrder" : [],
        "called" : 0,
        "regPresent" : False
    }
    functionCalls[fName] = []
    intermediateAssignments[fName] = {}

    defineInputsAndOutputs(fName,functions,function_decl)

    #type, value
    internalVariables = {}
    exp = ""
    function_body = fDef.body
    for node in function_body.block_items:
        if isinstance(node,c_ast.Decl) and node.init is not None:
            regPresent = handleDeclBlock(node,internalVariables)

        elif isinstance(node,c_ast.Assignment):
            regPresent = handleAssignmentBlock(node,internalVariables)

        elif isinstance(node,c_ast.Return):
            handleReturnBlock(node,internalVariables,functions,fName)

        elif isinstance(node,c_ast.FuncCall):
            handleFuncCallBlock(node,functions,fName,functionCalls,internalVariables)

        if(regPresent):
            functions[fName]["regPresent"] = regPresent
    intermediateAssignments[fName] = internalVariables
    
def defineInputsAndOutputs(fName,functions,function_decl):
    """
    @brief Defines the inputs and outputs for a function based on its declaration.

    This function updates the `functions` dictionary with the input and output ports of the function,
    and also stores the order of parameters.

    @param fName: The name of the function being processed.
    @param functions: A dictionary to store information about functions.
    @param function_decl: The function declaration node from the C Abstract Syntax Tree (AST).

    @raises ValueError: If the return type of the function is other than `void`.
    """
    functions[fName]["inputs"].append("clk")
    functions[fName]["paramOrder"].append("clk")
    params = function_decl.type.args.params
    for param_decl in params:
        node = param_decl.type;
        if isinstance(node,c_ast.TypeDecl):
            functions[fName]["inputs"].append(node.declname)
            functions[fName]["paramOrder"].append(node.declname)
        else:
            functions[fName]["outputs"].append(node.type.declname)
            functions[fName]["paramOrder"].append(node.type.declname)
    if(function_decl.type.type.type.names[0] != "void"):
        print("Return type other than void not supported.")
        sys.exit(1)