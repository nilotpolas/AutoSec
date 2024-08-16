import modules
from abc import ABC, abstractmethod
from modules.MyCGenerator import MyCGenerator


class BaseGraphNode(ABC):
    """
    @class BaseGraphNode
    @brief An abstract base class for graph nodes with a weight attribute.

    This class serves as a base for creating different types of graph nodes. It provides a common interface for nodes,
    including methods to get node labels and attributes.

    @param node_weight (int): An optional weight for the node, default is 0.

    @attributes
        @var node_weight (int): The weight of the node.
    """
    def __init__(self, node_weight=0) -> None:
        """
        @brief Initializes a new instance of the BaseGraphNode class.

        The constructor sets up the node with a specified weight.

        @param node_weight (int): The weight to assign to the node.
        """
        super().__init__()
        self.node_weight = node_weight

    @abstractmethod
    def label(self) -> str:
        """
        @brief Abstract method to get the label of the node.

        This method must be implemented by subclasses to return a string that represents the label of the node.

        @return A string representing the label of the node.
        """
        pass

    @abstractmethod
    def node_attr(self) -> dict:
        """
        @brief Abstract method to get the attributes of the node.

        This method must be implemented by subclasses to return a dictionary of attributes for the node.

        @return A dictionary of attributes for the node.
        """
        pass


class TextGraphNode(BaseGraphNode):
    """
    @class TextGraphNode
    @brief A graph node that holds a text label and provides attributes for visualization.

    This class represents a graph node with a text label and a weight. It provides methods to get the label and
    attributes for visualization purposes.

    @param node_text (str): The text to use as the label for the node.
    @param node_weight (int): An optional weight for the node, default is 0.
    """
    def __init__(self, node_text, node_weight=0) -> None:
        """
        @brief Initializes a new instance of the TextGraphNode class.

        The constructor sets up the node with a specified text label and weight.

        @param node_text (str): The text to assign as the label of the node.
        @param node_weight (int): The weight to assign to the node.
        """
        super().__init__(node_weight)
        self.node_text = node_text

    def label(self) -> str:
        """
        @brief Gets the label of the node.

        This method returns the text label of the node.

        @return A string representing the label of the node.
        """
        return self.node_text

    def node_attr(self) -> dict:
        """
        @brief Gets the attributes of the node for visualization.

        This method returns a dictionary of attributes including label formatting and color based on the node's text.

        @return A dictionary of attributes for the node.
        """
        fillcolor = "yellow"
        if (self.node_text == "Dummy"):
            fillcolor = "cyan"
        return {"label": f"{self.node_text} , {self.node_weight}", "style": "filled", "fillcolor": fillcolor}


class ASTGraphNode(BaseGraphNode):
    """
    @class ASTGraphNode
    @brief A graph node that holds an AST node and provides attributes for visualization.

    This class represents a graph node that contains an abstract syntax tree (AST) node and provides methods to get
    the label and attributes for visualization purposes.

    @param ast (pycparser.c_ast.Node): The AST node to be used as the content of the graph node.
    @param node_weight (int): An optional weight for the node, default is 0.
    """
    def __init__(self, ast, node_weight=0) -> None:
        """
        @brief Initializes a new instance of the ASTGraphNode class.

        The constructor sets up the node with a specified AST node and weight.

        @param ast (pycparser.c_ast.Node): The AST node to assign to the graph node.
        @param node_weight (int): The weight to assign to the node.
        """
        super().__init__(node_weight)
        self.ast = ast

    def label(self) -> str:
        """
        @brief Gets the label of the node by generating code from the AST node.

        This method uses `MyCGenerator` to generate a string representation of the AST node.

        @return A string representing the label of the node.
        """
        generator = MyCGenerator()
        return generator.visit(self.ast)

    def node_attr(self) -> dict:
        """
        @brief Gets the attributes of the node for visualization.

        This method returns a dictionary of attributes including the label generated from the AST node and the node's weight.

        @return A dictionary of attributes for the node.
        """
        return {"label": f"{self.label()} , {self.node_weight}"}
