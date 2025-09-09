#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Divisor de CSV en archivos de N filas (por defecto 1000)

INSTRUCCIONES DE INSTALACIÓN:
1) Python 3.8+
2) Dependencias: pandas
   pip install pandas

INSTRUCCIONES DE EJECUCIÓN:
1) Ajusta las variables de configuración (rutas, tamaño por archivo, prefijo)
2) Ejecuta: python split_csv.py

Descripción:
- Lee un CSV y genera múltiples CSVs con un máximo de ROWS_PER_FILE filas cada uno
- Mantiene los encabezados en todos los archivos generados
"""

import os
import sys
import math
import pandas as pd


# =============================================================================
# CONFIGURACIÓN - MODIFICA ESTAS VARIABLES
# =============================================================================

# Ruta del CSV de entrada
INPUT_CSV = "../data/products_normalized.xlsx - Sheet1.csv"

# Carpeta de salida donde se guardarán los archivos divididos
OUTPUT_DIR = "../data/exported/chunks"

# Número de filas por archivo
ROWS_PER_FILE = 1000

# Prefijo para los archivos de salida
OUTPUT_PREFIX = "products_chunk_"


# =============================================================================
# LÓGICA DE DIVISIÓN
# =============================================================================

def split_csv(input_path: str, output_dir: str, rows_per_file: int, prefix: str) -> bool:
    if rows_per_file <= 0:
        print("❌ Error: ROWS_PER_FILE debe ser mayor a 0")
        return False

    if not os.path.exists(input_path):
        print(f"❌ Error: No existe el archivo de entrada: {input_path}")
        return False

    try:
        print(f"📖 Leyendo CSV: {input_path}")
        df = pd.read_csv(input_path, encoding="utf-8")
        total_rows = len(df)
        print(f"✅ Leído: {total_rows} filas, {len(df.columns)} columnas")

        if total_rows == 0:
            print("⚠️  El archivo no contiene filas, no hay nada que dividir")
            return True

        # Crear directorio de salida
        os.makedirs(output_dir, exist_ok=True)

        num_files = math.ceil(total_rows / rows_per_file)
        print(f"🔪 Dividiendo en {num_files} archivo(s) de hasta {rows_per_file} filas")

        for i in range(num_files):
            start = i * rows_per_file
            end = min(start + rows_per_file, total_rows)
            chunk = df.iloc[start:end]
            out_path = os.path.join(output_dir, f"{prefix}{i+1}.csv")
            chunk.to_csv(out_path, index=False, encoding="utf-8")
            print(f"💾 Guardado: {out_path} ({len(chunk)} filas)")

        print("🎉 División completada")
        return True

    except pd.errors.EmptyDataError:
        print("❌ Error: El archivo CSV está vacío o corrupto")
        return False
    except pd.errors.ParserError as e:
        print(f"❌ Error al parsear CSV: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def main() -> None:
    print("=" * 60)
    print("🧩 DIVISOR DE CSV")
    print("=" * 60)
    print(f"📁 Entrada: {INPUT_CSV}")
    print(f"📁 Salida:  {OUTPUT_DIR}")
    print(f"⚙️  Filas por archivo: {ROWS_PER_FILE}")
    print("-" * 60)

    ok = split_csv(INPUT_CSV, OUTPUT_DIR, ROWS_PER_FILE, OUTPUT_PREFIX)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()


