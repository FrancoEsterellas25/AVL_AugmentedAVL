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
            elif node_to_delete.left != None and node_to_delete.right != None:
                sucessor = node_to_delete.right
                while sucessor.left != None:
                    sucessor = sucessor.left

                nuevo_nombre = sucessor.name
                nuevo_valor = sucessor.value

                self.borrado_fisico_simple(sucessor)

                node_to_delete.name = nuevo_nombre
                node_to_delete.value = nuevo_valor  

            # CASO 2: Tiene un solo hijo
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
                
    def recursive_search_with_lims(self, currentNode, min_limit, max_limit, result):
        if currentNode is None:
            return

        lower_ok = min_limit is None or currentNode.value > min_limit
        upper_ok = max_limit is None or currentNode.value < max_limit

        if lower_ok:
            self.recursive_search_with_lims(currentNode.left, min_limit, max_limit, result)

        if lower_ok and upper_ok:
            result.append(currentNode)

        if upper_ok:
            self.recursive_search_with_lims(currentNode.right, min_limit, max_limit, result)

    def searching_with_lims(self, min_limit=None, max_limit=None):
        result = []
        self.recursive_search_with_lims(self.root, min_limit, max_limit, result)
        return result


class AVLNode(Node):
    def __init__(self, name, value, right=None, left=None, parent=None):
        super().__init__(name, value, right, left, parent)
        self.height = 1
        
class AVL(BinarySearchTree):
    def __init__(self):
        super().__init__()
    
    def get_height(self, node):
        if node is None:
            return 0
        return node.height
    
    # FIX: usa get_height (O(1)) en vez de height_recursive (O(n))
    def get_balance(self, nodo):
        if nodo is None:
            return 0
        return self.get_height(nodo.left) - self.get_height(nodo.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        x.parent = y.parent
        if y.parent:
            if y.parent.left == y:
                y.parent.left = x
            else:
                y.parent.right = x
        else:
            self.root = x

        y.parent = x
        if T2:
            T2.parent = y

        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x
    
    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        y.parent = x.parent
        if x.parent:
            if x.parent.left == x:
                x.parent.left = y
            else:
                x.parent.right = y
        else:
            self.root = y

        x.parent = y
        if T2:
            T2.parent = x

        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y
            
    def put(self, name, value):
        if self.root is None:
            self.root = AVLNode(name, value)
        else:
            # FIX: captura el retorno para que self.root se actualice si hay rotación en la raíz
            self.root = self._put(self.root, name, value)
            self.root.parent = None

    def _put(self, currentNode, name, value):
        # --- FASE 1: DESCENSO ---
        if value < currentNode.value:
            if currentNode.left:
                currentNode.left = self._put(currentNode.left, name, value)
            else:
                currentNode.left = AVLNode(name, value, parent=currentNode)
        else:
            if currentNode.right:
                currentNode.right = self._put(currentNode.right, name, value)
            else:
                currentNode.right = AVLNode(name, value, parent=currentNode)

        # --- FASE 2: ACTUALIZACIÓN ---
        alt_izq = self.get_height(currentNode.left)
        alt_der = self.get_height(currentNode.right)
        
        currentNode.height = 1 + max(alt_izq, alt_der)
        balance = alt_izq - alt_der

        # --- FASE 3: REBALANCEO ---
        if balance > 1:
            if self.get_balance(currentNode.left) >= 0:
                return self.rotate_right(currentNode)
            else:
                currentNode.left = self.rotate_left(currentNode.left)
                return self.rotate_right(currentNode)

        if balance < -1:
            if self.get_balance(currentNode.right) <= 0:
                return self.rotate_left(currentNode)
            else:
                currentNode.right = self.rotate_right(currentNode.right)
                return self.rotate_left(currentNode)

        return currentNode 

    # Override: eliminar con rebalanceo AVL usando el mismo patrón de retorno que _put
    def delete_node(self, X_value):
        self.root = self._delete(self.root, X_value)
        if self.root:
            self.root.parent = None

    def _delete(self, node, X_value):
        # --- FASE 1: DESCENSO (búsqueda) ---
        if node is None:
            return None

        if X_value < node.value:
            node.left = self._delete(node.left, X_value)
            if node.left:
                node.left.parent = node
        elif X_value > node.value:
            node.right = self._delete(node.right, X_value)
            if node.right:
                node.right.parent = node
        else:
            # Nodo encontrado — mismos 3 casos del BST
            if node.is_leaf():
                return None

            elif node.left is None:
                succ = node.right
                succ.parent = node.parent
                return succ

            elif node.right is None:
                succ = node.left
                succ.parent = node.parent
                return succ

            else:
                # Caso 3: sucesor in-order (mínimo del subárbol derecho)
                sucesor = node.right
                while sucesor.left:
                    sucesor = sucesor.left

                # Usurpar identidad del sucesor
                node.name = sucesor.name
                node.value = sucesor.value

                # Eliminar sucesor del subárbol derecho (recursivo, propaga rebalanceo)
                node.right = self._delete(node.right, sucesor.value)
                if node.right:
                    node.right.parent = node

        # --- FASE 2: ACTUALIZACIÓN ---
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # --- FASE 3: REBALANCEO ---
        # Pesado a la izquierda
        if balance > 1:
            if self.get_height(node.left.left) >= self.get_height(node.left.right):
                # LL
                return self.rotate_right(node)
            else:
                # LR
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        # Pesado a la derecha
        if balance < -1:
            if self.get_height(node.right.right) >= self.get_height(node.right.left):
                # RR
                return self.rotate_left(node)
            else:
                # RL
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node