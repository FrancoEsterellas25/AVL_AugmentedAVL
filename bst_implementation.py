import queue

class Node():
    def __init__(self, name, value, right = None, left = None, parent= None):
        self.name = name
        self.value = value
        self.right = right
        self.left = left
        self.parent = parent

class BinarySearchTree():
    def __init__(self):
        self.root = None

    def _put(self, currentNode, name, value):
        if value < currentNode.value:
            if currentNode.left:
                self._put(currentNode.left, name,value)
            else:
                currentNode.left = Node(name, value, parent=currentNode)
        else: 
            if currentNode.right:
                self._put(currentNode.right,name,value)
            else:
                currentNode.right = Node(name, value, parent = currentNode)

    def put(self, name, value): 
        if self.root == None:
            self.root = Node(name, value)
        else: 
            self._put(self.root, name, value)
    
    def show_tree(self):
        if self.root != None:
            self.show_tree_recursive(self.root)

    def show_tree_recursive(self,currentNode):
        
        if currentNode.left != None:
            self.show_tree_recursive(currentNode.left)
    
        print(currentNode.value)
        
        if currentNode.right != None:
            self.show_tree_recursive(currentNode.right)
            
        
        
        
        

tree = BinarySearchTree()

nodes = [['a',5],['b',6], ['c',2],['c',3]]

for node in nodes:
    name = node[0]
    value = node[1]

    tree.put(name,value)

tree.show_tree()