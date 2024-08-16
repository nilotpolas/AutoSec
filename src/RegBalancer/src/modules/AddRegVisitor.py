import modules
from modules.CrossDomainOp import CrossDomainOp
import pycparser.c_ast as cast

from modules.FindIdentifier import FindIdentifier


class AddRegVisitor(cast.NodeVisitor):
    """
    @class AddRegVisitor
    @brief A visitor class for adding register function calls to binary operations in an abstract syntax tree (AST).

    This class traverses the AST to find binary operations within assignment statements. It modifies the right-hand side (RHS)
    of the assignment expression to include a call to the `reg()` function if the operands of the binary operation belong to
    different domains.

    @param domain_map (dict): A dictionary that maps variable names to their corresponding domains.

    @attributes
        @var domain_map (dict): A dictionary mapping variable names to their corresponding domains.
        @var id_name (FindIdentifier): An instance of `FindIdentifier` used to retrieve identifier names.
        @var cross_domains (list): A list of variable names that are involved in cross-domain operations.
    """

    def __init__(self, domain_map):
        """
        @brief Initializes the AddRegVisitor with the given domain map.

        This constructor sets up the domain map, initializes the identifier finder, and prepares a list to track cross-domain
        operations.

        @param domain_map (dict): A dictionary that maps variable names to their corresponding domains.
        """
        self.domain_map = domain_map
        self.id_name = FindIdentifier()
        self.cross_domains = []
        super().__init__()

    def visit_Assignment(self, node):
        """
        @brief Visits an Assignment node in the AST and modifies the right-hand side if necessary.

        This method processes an assignment node by checking if the RHS of the assignment is a binary operation with operands
        from different domains. If so, it replaces the RHS with a `CrossDomainOp` instance to include a call to the `reg()`
        function. Additionally, it handles the case of XOR operations involving cross-domain operands and "random" domains.

        @param node (pycparser.c_ast.Assignment): The Assignment node to visit and potentially modify.

        @details
            - If the RHS of the assignment is a `BinaryOp` and the domains of the operands are different, it replaces the RHS
              with a `CrossDomainOp`.
            - If the operation is XOR (`^`) and involves cross-domain operands with one operand having a "random" domain, it
              also replaces the RHS with a `CrossDomainOp`.

        @see CrossDomainOp
        @see FindIdentifier
        """
        # If RHS of assignment is a Binary Operation, extract operands and comparse domains
        if (isinstance(node.rvalue, cast.BinaryOp)):
            op_left = self.id_name.name(node.rvalue.left)
            op_right = self.id_name.name(node.rvalue.right)
            domain_left = self.domain_map.get(op_left)
            domain_right = self.domain_map.get(op_right)
            # If operands are of different domain, add function call to reg() in RHS
            if (domain_left != None and domain_right != None and domain_left != domain_right):
                self.cross_domains.append(node.lvalue.name)
                print(
                    f"Cross domain between {op_left} and {op_right}")
                node.rvalue = CrossDomainOp(
                    node.rvalue.op,
                    node.rvalue.left,
                    node.rvalue.right
                )
            elif node.rvalue.op == '^' and (op_left in self.cross_domains and domain_right == "random") or (op_right in self.cross_domains and domain_left == "random"):
                print(
                    f"Identified resharing of cross domain product: {op_left} ^ {op_right}")
                node.rvalue = CrossDomainOp(
                    node.rvalue.op,
                    node.rvalue.left,
                    node.rvalue.right
                )
        else:
            self.generic_visit(node)
