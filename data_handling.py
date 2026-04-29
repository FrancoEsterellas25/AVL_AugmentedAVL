import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from datasets import load_dataset
import polars as pl

# 1. Definimos las columnas que queremos limpiar y de las que sacaremos los únicos
target_columns = [
    "name", "author", "star_rating", 
    "num_reviews", "genres"
]

num_columns = ["star_rating", "num_reviews"] 

# Creamos el acumulador (diccionario de sets vacíos) para no saturar la RAM
unique_values_accumulator = {col: set() for col in target_columns}

# Cargamos el stream (ds es un IterableDataset)
ds = load_dataset("BrightData/Goodreads-Books", split="train", streaming=True)

print("Dataset cargado. Preparando el empaquetado...")

# 2. Transformamos el IterableDataset en uno que arroja lotes
batched_ds = ds.batch(batch_size=100000)

# 3. Iteramos sobre los lotes
# 3. Iteramos sobre los lotes
for i, batch in enumerate(batched_ds):
    # 'batch' es el diccionario con listas de 50k elementos. 
    # Polars lo convierte a DataFrame nativo de forma extremadamente eficiente.
    df = pl.DataFrame(batch, strict=False)  # strict=False para evitar errores por columnas faltantes

    # 2. Forzamos el cast a Float64 en las columnas numéricas.
    # Usamos 'with_columns' para transformar varias a la vez de forma eficiente.
    df = df.with_columns([
        pl.col(c).cast(pl.Float64, strict=False) for c in num_columns if c in df.columns
    ])

    # --- EXTRACCIÓN DE ÚNICOS (DROP_NULLS POR COLUMNA) ---
    for col in target_columns:
        # Drop nulls solo para la columna específica que estamos procesando
        if col in df.columns:
            df_col = df.select(pl.col(col)).drop_nulls()
            
            # Extrae los valores únicos
            if col == "genres":
                     # PRIMER ELEMENTO DE LISTA: Extraer solo el primer género
                lote_unicos = []
                for val in df_col[col].to_list():
                    primer_elemento = None
                    # Manejo de posibles formatos de lista
                    if isinstance(val, list) and len(val) > 0:
                        primer_elemento = val[0]
                    elif isinstance(val, str) and val.startswith("["):
                        # Si es un string que representa lista, parsearlo
                        try:
                            import ast
                            parsed = ast.literal_eval(val)
                            if isinstance(parsed, list) and len(parsed) > 0:
                                primer_elemento = parsed[0]
                        except:
                            primer_elemento = val  # Fallback: usar el string directo
                    elif isinstance(val, str):
                        # Si es un string directo (no lista), usarlo como es
                        primer_elemento = val
                    
                    if primer_elemento is not None and primer_elemento != "":
                        lote_unicos.append(primer_elemento)
            
            else:
                # Para otras columnas, extrae los únicos normalmente
                lote_unicos = df_col[col].unique().to_list()
            
            # ACTUALIZAR ACUMULADOR PARA TODAS LAS COLUMNAS (fuera del else)
            # Filtra None/null y actualiza
            lote_unicos = [x for x in lote_unicos if x is not None]
            if lote_unicos:  # Solo si hay datos
                unique_values_accumulator[col].update(lote_unicos)
        
    print(f"Lote {i+1} procesado... Acumulados: genres={len(unique_values_accumulator['genres'])}, first_published={len(unique_values_accumulator['first_published'])}")

print("\nLectura finalizada. Generando archivos CSV...\n")

# 4. Exportación a disco
for col in target_columns:
    # Obtener la lista de valores únicos
    valores_unicos = list(unique_values_accumulator[col])
    
    # VALIDACIÓN: Verificar que no esté vacío
    if len(valores_unicos) == 0:
        print(f"⚠️  ADVERTENCIA: {col}_unicos.csv estaría vacío. Saltando...")
        continue
    
    # Crear DataFrame con valores únicos e IDs secuenciales
    df_final = pl.DataFrame({
        "id": list(range(1, len(valores_unicos) + 1)),
        col: valores_unicos
    })
    
    # Guardar el CSV
    nombre_archivo = f"{col}_unicos.csv"
    df_final.write_csv(nombre_archivo)
    
    # Print de confirmación con conteo
    print(f"✓ {nombre_archivo}")
    print(f"  └─ {len(valores_unicos)} valores únicos guardados\n")

print("¡Pipeline completado!")