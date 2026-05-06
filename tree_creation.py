from bst_implementation import AVL
from index_code import global_function, maps
import polars as pl

map_value = {"star_rating":  10**23,
                "name" :  10**16,
                "genres" : 10**12,
                "author" : 10**5,
                "num_reviews" : 1}

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
        
def limited_search (avl_tree, param_for_search, lim_min = None, lim_max = None):
    
    if lim_min in maps[param_for_search].values() and lim_max in maps[param_for_search].values():
        pass
    if lim_max not in maps[param_for_search].values() or lim_max is None:
        lim_max = max(maps[param_for_search].values())
    if lim_min not in maps[param_for_search].values() or lim_min is None:
        lim_min = min(maps[param_for_search].values())
        
    
    lim_min = lim_min * map_value[param_for_search]
    lim_max = lim_max * map_value[param_for_search]
    return avl_tree.searching_with_lims(lim_min, lim_max)

tree = create_avl_tree(10000)
lim_tree = limited_search(tree, "star_rating", 4)

print(lim_tree)