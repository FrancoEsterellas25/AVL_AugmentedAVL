import polars as pl
from datasets import load_dataset
import pandas as pd


# 1. Cargamos los mapeos directamente con Polars (más rápido que Pandas)
def get_map(file_path, col_name):
        # Leemos el CSV y creamos el diccionario { nombre: id }
        temp_df = pl.read_csv(file_path)
        return dict(zip(temp_df[col_name], temp_df['id']))
maps = {
        'name': get_map("name_unicos.csv", "name"),
        'author': get_map("author_unicos.csv", "author"),
        'star_rating': get_map("star_rating_unicos.csv", "star_rating"),
        'num_reviews': get_map("num_reviews_unicos.csv", "num_reviews"),
        'genres': get_map("genres_unicos.csv", "genres")
    }

def global_function(CANTIDAD, maps = maps):
    

    

    def fetch_goodreads_data_streaming(n_obs: int):
        print(f"Abriendo flujo para {n_obs} observaciones...")
        
        # 1. Cargamos con streaming=True
        dataset = load_dataset("BrightData/Goodreads-Books", split="train", streaming=True)
        
        # 2. 'Tomamos' n observaciones del flujo
        # dataset.take(n) devuelve un generador con las primeras n filas
        iterable_subset = dataset.take(n_obs)
        
        # 3. Convertimos esa lista de diccionarios a DataFrame de Polars
        # Pasamos por una lista de Python o un DF de Pandas intermedio
        df_polars = pl.from_dataframe(pd.DataFrame(list(iterable_subset)))
        
        return df_polars

    # --- Ejemplo de uso ---
    # n = 5000  # Podés cambiar este valor según lo que necesites testear
    # df = fetch_goodreads_data(n)

    def apply_positional_encoding(df, maps):
        """
        Recibe el DF de Polars y los diccionarios de mapeo para crear la clave maestra.
        """
        # Transformación de columnas a IDs numéricos
        df = df.with_columns([
            pl.col("name").replace(maps['name'], default=0).alias("name_id"),
            pl.col("author").replace(maps['author'], default=0).alias("author_id"),
            pl.col("star_rating").replace(maps['star_rating'], default=0).alias("star_rating_id"),
            pl.col("num_reviews").replace(maps['num_reviews'], default=0).alias("num_reviews_id"),
            pl.col("genres").replace(maps['genres'], default=0).alias("genres_id")
        ])

        # Creación de la clave (Uso de UInt128 para evitar overflow en 10^23)
        return df.with_columns(
            index_code = (
                (pl.col("star_rating_id").cast(pl.UInt128) * 10**23) +
                (pl.col("name_id").cast(pl.UInt128) * 10**16) +
                (pl.col("genres_id").cast(pl.UInt128) * 10**12) +
                (pl.col("author_id").cast(pl.UInt128) * 10**5) +
                (pl.col("num_reviews_id").cast(pl.UInt128))
            )
        )

    # --- EJECUCIÓN ---
     # Ajustá este parámetro aquí
    df_raw = fetch_goodreads_data_streaming(CANTIDAD)
    df_final = apply_positional_encoding(df_raw, maps)

    return df_final