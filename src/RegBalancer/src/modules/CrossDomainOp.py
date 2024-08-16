import pycparser.c_ast as cast


class CrossDomainOp(cast.BinaryOp):
    """   
    Custom BinaryOp class that inherits from `pycparser.c_ast.BinaryOp`.
    This class is used to annotate some BinaryOp nodes in an AST.
    This annotation allows use to mark cross domain operations in the AST

    """

    def __init__(self, op, left, right, coord=None):
        super().__init__(op, left, right, coord)
