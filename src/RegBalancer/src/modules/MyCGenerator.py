from pycparser import c_generator
import pycparser.c_ast as cast

class MyCGenerator(c_generator.CGenerator):
    """
    @class MyCGenerator
    @brief A customized C code generator that supports a custom binary operation class.

    This class extends the `c_generator.CGenerator` class to handle a custom binary operation class, `CrossDomainOp`,
    which is a subclass of `pycparser.c_ast.BinaryOp`. The `visit_CrossDomainOp()` method is overridden to generate
    appropriate C code for this custom binary operation.

    @details
        The custom generator is designed to integrate with the PyCParser library's code generation process and
        ensure that instances of `CrossDomainOp` are properly represented in the generated C code.
    """

    def visit_CrossDomainOp(self, node):
        """
        @brief Visits a `CrossDomainOp` node and generates the corresponding C code.

        This method overrides the default behavior of `visit_CrossDomainOp()` in the `c_generator.CGenerator` class.
        It creates a new `pycparser.c_ast.BinaryOp` node with the same operator, left operand, and right operand as
        the input `CrossDomainOp` node. The generated `BinaryOp` node is then visited to produce the appropriate C code.

        @param node (CrossDomainOp): The `CrossDomainOp` node to visit.

        @return str: The C code generated for the `CrossDomainOp` node.
        
        @see pycparser.c_ast.BinaryOp
        """
        # Create a new BinaryOp node with the same operator, left operand, and right operand
        cast_node = cast.BinaryOp(node.op, node.left, node.right)
        # Generate and return the C code for the BinaryOp node
        return self.visit(cast_node)