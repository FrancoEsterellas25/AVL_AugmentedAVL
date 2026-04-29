from bst_implementation import AVL
from index_code import global_function
import polars as pl

def create_avl_tree(CANTIDAD):
    avl_tree= AVL()
    df = global_function(CANTIDAD)
    
    df = df.select(["name", "author", "star_rating", "num_reviews", "genres", "index_code"])
    
    for row in df.iter_rows(named=True):
        # named=True devuelve diccionarios, named=False (default) devuelve tuplas
        value = row["index_code"]
        info = {
            "name": row["name"],
            "author": row["author"],
            "star_rating": row["star_rating"],
            "num_reviews": row["num_reviews"],
            "genres": row["genres"]
        }
        avl_tree.put(info, value)
        
    return avl_tree
        
        
        
result = create_avl_tree(100)

print(result.show_tree())
