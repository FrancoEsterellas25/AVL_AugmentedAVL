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


class AVLNode(Node):
    def __init__(self, name, value, right=None, left=None, parent=None):
        super().__init__(name, value, right, left, parent)
        self.height = 1
        self.balance = 0
        
class AVL(BinarySearchTree):
    def __init__(self):
        super().__init__()
    
    def get_height(self, node):
        # Si el nodo no existe (es un espacio vacío)
        if node is None:
            return 0
        
        # Si existe, simplemente devolvemos el valor que tiene guardado
        # Este acceso es instantáneo: O(1)
        return node.height
    
    def rotate_right(self, y):
        # Definimos los protagonistas
        x = y.left
        T2 = x.right # El subárbol que cambiará de padre

        # Paso 1: Reorganizar hijos
        x.right = y
        y.left = T2

        # Paso 2: Actualizar punteros de padre (Crucial en tu código)
        x.parent = y.parent
        if y.parent:
            if y.parent.left == y:
                y.parent.left = x
            else:
                y.parent.right = x
        else:
            self.root = x # Si y era la raíz global, ahora x lo es

        y.parent = x
        if T2:
            T2.parent = y

        # Paso 3: Actualizar alturas (Primero el que quedó más abajo)
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        # Importante: devolvemos la nueva raíz de este subárbol
        return x
    
    def rotate_left(self, x):
        # Definimos los protagonistas
        y = x.right
        T2 = y.left # El subárbol que cambiará de padre

        # Paso 1: Reorganizar hijos
        y.left = x
        x.right = T2

        # Paso 2: Actualizar punteros de padre
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

        # Paso 3: Actualizar alturas (Primero el que quedó más abajo)
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        # Devolvemos la nueva raíz del subárbol
        return y
            
    def put(self, name, value):
        if self.root is None:
            # Aquí es donde ocurre el cambio: usamos AVLNode
            self.root = AVLNode(name, value)
        else:
            self._put(self.root, name, value)

    def _put(self, currentNode, name, value):
        # --- FASE 1: DESCENSO (Inserción estándar) ---
        if value < currentNode.value:
            if currentNode.left:
                # El padre actualiza su hijo con lo que devuelva la recursión
                currentNode.left = self._put(currentNode.left, name, value)
            else:
                currentNode.left = AVLNode(name, value, parent=currentNode)
        else:
            if currentNode.right:
                currentNode.right = self._put(currentNode.right, name, value)
            else:
                currentNode.right = AVLNode(name, value, parent=currentNode)

        # --- FASE 2: ACTUALIZACIÓN (Al regresar de la recursión) ---
        # Usamos los atributos .height que ya están guardados en los hijos
        alt_izq = self.get_height(currentNode.left)
        alt_der = self.get_height(currentNode.right)
        
        currentNode.height = 1 + max(alt_izq, alt_der)
        balance = alt_izq - alt_der

        # --- FASE 3: REBALANCEO ---
        # Caso 1: Pesado a la Izquierda (Balance > 1)
        if balance > 1:
            # Sub-caso: ¿Es línea recta o Zig-Zag?
            if self.get_balance(currentNode.left) >= 0:
                # Caso Izquierda-Izquierda (Simple)
                return self.rotate_right(currentNode)
            else:
                # Caso Izquierda-Derecha (Doble)
                currentNode.left = self.rotate_left(currentNode.left)
                return self.rotate_right(currentNode)

        # Caso 2: Pesado a la Derecha (Balance < -1)
        if balance < -1:
            if self.get_balance(currentNode.right) <= 0:
                # Caso Derecha-Derecha (Simple)
                return self.rotate_left(currentNode)
            else:
                # Caso Derecha-Izquierda (Doble)
                currentNode.right = self.rotate_right(currentNode.right)
                return self.rotate_left(currentNode)

        # Si no hubo que rotar, devolvemos el nodo tal cual
        return currentNode 
            
    def height_recursive(self, nodo):
        # 1. Si el camino se termina, la altura es 0
        if nodo is None:
            return 0
        
        # 2. "Baja hasta abajo" por la izquierda
        altura_izq = self.height_recursive(nodo.left)
        
        # 3. "Baja hasta abajo" por la derecha
        altura_der = self.height_recursive(nodo.right)
        
        # 4. La altura del nodo actual es 1 (él mismo) más el camino más largo
        return 1 + max(altura_izq, altura_der)

    def get_balance(self, nodo):
        if nodo is None:
            return 0
        # El balance es la resta de las alturas de sus dos ramas
        return self.height_recursive(nodo.left) - self.height_recursive(nodo.right)
    
                

avl_tree = AVL()

nodes = [['a',5],['b',6], ['c',2],['d',3]]

for node in nodes: 
    name = node[0]
    value = node[1]
    
    avl_tree.put(name,value)

print(avl_tree.show_tree())
if avl_tree.root:
    print(avl_tree.get_balance(avl_tree.root))

