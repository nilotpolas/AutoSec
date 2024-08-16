from collections import deque
from pycparser import c_ast
import copy

class DiGraph():
    """
    @brief A class representing a directed graph with nodes and edges.

    This class provides methods for adding nodes and edges, retrieving in-degrees, and performing topological sorting.
    """
    def __init__(self):
        """
        @brief Initializes an empty directed graph.

        Sets up internal data structures to keep track of nodes, adjacency lists, and in-degrees.
        """
        self.__inEdges = []
        self.__functionIndexMap = {}
        self.__indexFunctionMap = {}
        self.__adjacencyList = []
        self.numNodes = 0
    
    def addFunction(self,fName):
        """
        @brief Adds a function as a node to the graph.

        If the function is not already present, it adds it and initializes its adjacency list and in-degree.

        @param fName: The name of the function to be added as a node.
        @type fName: str

        @raises KeyError: If the function name is already in the graph.
        """
        if fName not in self.__functionIndexMap:
            self.__functionIndexMap[fName] = self.numNodes
            self.__indexFunctionMap[self.numNodes] = fName
            self.numNodes += 1
            self.__adjacencyList.append([])
            self.__inEdges.append(0)
    
    def addEdgeBetween(self,f1,f2):
        """
        @brief Adds a directed edge from function f1 to function f2.

        Updates the adjacency list and the in-degree of function f2.

        @param f1: The name of the source function.
        @type f1: str
        @param f2: The name of the target function.
        @type f2: str

        @raises KeyError: If either function name is not present in the graph.
        """
        f1Index = self.__functionIndexMap[f1]
        f2Index = self.__functionIndexMap[f2]
        if f2Index not in self.__adjacencyList[f1Index]:
            self.__adjacencyList[f1Index].append(f2Index)
            self.__inEdges[f2Index] += 1
    
    def getIndegreeOf(self,fName):
        """
        @brief Retrieves the in-degree of the specified function.

        @param fName: The name of the function whose in-degree is to be retrieved.
        @type fName: str

        @return: The in-degree of the specified function.
        @rtype: int

        @raises KeyError: If the function name is not present in the graph.
        """
        return self.__inEdges[self.__functionIndexMap[fName]]
    
    def topoSort(self):
        """
        @brief Performs a topological sort on the graph.

        Uses Kahn's algorithm to return a list of nodes in topologically sorted order.

        @return: A list of function names in topologically sorted order.
        @rtype: list of str
        """
        q = deque()
        inEdges = copy.deepcopy(self.__inEdges)
        for index in range(self.numNodes):
            if(inEdges[index] == 0):
                q.append(index)
        sortedList = []
        while q:
            node = q.popleft()
            sortedList.append(self.__indexFunctionMap[node])
            for adj in self.__adjacencyList[node]:
                inEdges[adj] -= 1
                if(inEdges[adj] == 0):
                    q.append(adj)
        return sortedList

