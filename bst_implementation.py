class Node():
    def __init__(self, name, value, right = None, left = None, parent= None):
        self.name = name
        self.value = value
        self.right = right
        self.left = left
        self.parent = parent

    def is_leaf(self):
        return self.left == None and self.right == None
    
    def is_root(self):
        return self.parent == None

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

    def recursive_search(self, currentNode, X_value):
        if currentNode is None:
            return None

        if X_value == currentNode.value:
            return currentNode

        elif X_value > currentNode.value and currentNode.right:
            return self.recursive_search(currentNode.right, X_value)

        elif X_value < currentNode.value and currentNode.left:
            return self.recursive_search(currentNode.left, X_value)

        else:
            return None

        
    
    def searching(self, X_value):
        return self.recursive_search(self.root, X_value)
    
    def delete_node(self, X_value):
        node_to_delete = self.searching(X_value)

        if node_to_delete:
            # CASO 1: Es una hoja
            if node_to_delete.is_leaf():
                if node_to_delete.parent:
                    if node_to_delete.parent.left == node_to_delete:
                        node_to_delete.parent.left = None
                    else:
                        node_to_delete.parent.right = None
                else:
                    self.root = None

            # CASO 3: Tiene dos hijos
            # MOVIDO DENTRO DEL IF y convertido en ELIF del Caso 1
            elif node_to_delete.left != None and node_to_delete.right != None:
                sucessor = node_to_delete.right
                while sucessor.left != None:
                    sucessor = sucessor.left

                nuevo_nombre = sucessor.name
                nuevo_valor = sucessor.value

                # Primero podamos el sucesor de su posición original
                self.borrado_fisico_simple(sucessor)

                # Luego usurpamos su identidad
                node_to_delete.name = nuevo_nombre
                node_to_delete.value = nuevo_valor  

            # CASO 2: Tiene un solo hijo
            # Convertido en ELIF para que solo se ejecute si no son los anteriores
            else:
                hijo = node_to_delete.left if node_to_delete.left else node_to_delete.right
                
                if node_to_delete.parent:
                    hijo.parent = node_to_delete.parent
                    if node_to_delete.parent.left == node_to_delete:
                        node_to_delete.parent.left = hijo
                    else:
                        node_to_delete.parent.right = hijo
                else:
                    self.root = hijo
                    hijo.parent = None

    def borrado_fisico_simple(self, node):
        # Determinamos si tiene un hijo (derecho, porque es sucesor)
        hijo = node.right if node.right else None
        
        if node.parent:
            if node.parent.left == node:
                node.parent.left = hijo
            else:
                node.parent.right = hijo
            if hijo:
                hijo.parent = node.parent
        else:
            self.root = hijo
            if hijo:
                hijo.parent = None





tree = BinarySearchTree()

nodes = [['a',5],['b',6], ['c',2],['d',3]]

for node in nodes:
    name = node[0]
    value = node[1]

    tree.put(name,value)

tree.show_tree()
tree.delete_node(5)
tree.show_tree()