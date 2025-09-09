#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Normaliza productos según reglas específicas y exporta a XLSX

INSTRUCCIONES DE INSTALACIÓN:
1) Python 3.8+
2) Dependencias:
   pip install pandas openpyxl

INSTRUCCIONES DE EJECUCIÓN:
1) Ajusta las variables de configuración (rutas, nombres de columnas y reglas)
2) Ejecuta: python product_normalizer.py

REGLAS IMPLEMENTADAS:
- Nombres en MAYÚSCULAS: si el nombre del producto está totalmente en mayúsculas, se normaliza a Title Case.
- Etiqueta para raíz "all /": si el campo de ruta/categoría raíz empieza con "all" (ignorando mayúsculas/minúsculas),
  se asigna el tag configurado al campo de etiquetas (product_tag_ids).
- default_code: si contiene un token que comienza con "PRO" (configurable), se elimina todo desde ese token hasta el final.

Todas las columnas no afectadas se mantienen iguales.
"""

from __future__ import annotations

import os
import sys
import re
import pandas as pd


# =============================================================================
# CONFIGURACIÓN - MODIFICA ESTAS VARIABLES SEGÚN TU CSV
# =============================================================================

# Rutas de entrada/salida (por defecto apunta a la carpeta data del proyecto)
input_file = "../data/Product (product.template) (1).csv"
output_file = "../data/exported/products_normalized.xlsx"

# Nombres de columnas en tu CSV
COL_PRODUCT_NAME = "name"                 # Nombre del producto
COL_ROOT_PATH = "categ_id"             # Ruta/categoría raíz (e.g., "All / ...")
COL_TAGS = "product_tag_ids"              # Columna de etiquetas
COL_DEFAULT_CODE = "default_code"         # Código interno del producto

# Reglas
ROOT_NAME = "All /"                         # Valor raíz a detectar (case-insensitive)
TAG_TO_ASSIGN = "Embassy Store"           # Tag a asignar cuando la raíz sea "all"
DEFAULT_CODE_TOKEN = "PRO"                # Token que indica desde dónde truncar hasta el final


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def is_all_uppercase(text: str) -> bool:
    """Devuelve True si el texto tiene al menos una letra y todas las letras están en mayúsculas."""
    if not isinstance(text, str):
        return False
    # Debe contener al menos una letra
    letters = re.findall(r"[A-Za-zÁÉÍÓÚÑÜáéíóúñü]", text)
    if not letters:
        return False
    return text == text.upper()


def normalize_name_to_title(name_value):
    if pd.isna(name_value) or name_value == "":
        return name_value
    text = str(name_value)
    if is_all_uppercase(text):
        return text.title()
    return text


def root_is_all(root_value: object) -> bool:
    if pd.isna(root_value):
        return False
    text = str(root_value).strip()
    # Case-insensitive: comienza por "all" (por ejemplo, "All / Ropa")
    return text.lower().startswith(ROOT_NAME.lower())


def strip_default_code_suffix(code_value: object) -> object:
    if pd.isna(code_value):
        return code_value
    text = str(code_value)
    # Busca el primer índice del token (e.g., "PRO") y corta desde ahí al final
    idx = text.find(DEFAULT_CODE_TOKEN)
    if idx != -1:
        text = text[:idx]
    # Limpia separadores residuales
    return text.rstrip(" -_#:/")


# =============================================================================
# PROCESAMIENTO
# =============================================================================

def process_products(input_path: str, output_path: str) -> bool:
    if not os.path.exists(input_path):
        print(f"❌ Error: No existe el archivo de entrada: {input_path}")
        return False

    try:
        print(f"📖 Leyendo: {input_path}")
        df = pd.read_csv(input_path, encoding="utf-8")
        print(f"✅ Leído: {len(df)} filas, {len(df.columns)} columnas")

        # 1) Normalizar nombres en MAYÚSCULAS a Title Case
        if COL_PRODUCT_NAME in df.columns:
            df[COL_PRODUCT_NAME] = df[COL_PRODUCT_NAME].apply(normalize_name_to_title)
        else:
            print(f"⚠️  Columna no encontrada: {COL_PRODUCT_NAME}")

        # 2) Asignar tag si la raíz empieza con 'all'
        if COL_ROOT_PATH in df.columns:
            mask_root_all = df[COL_ROOT_PATH].apply(root_is_all)
            # Si la columna de tags no existe, créala vacía
            if COL_TAGS not in df.columns:
                df[COL_TAGS] = ""
            # Asignar tag fijo (reemplaza el contenido); si preferieras concatenar, ajusta aquí
            df.loc[mask_root_all, COL_TAGS] = TAG_TO_ASSIGN
        else:
            print(f"⚠️  Columna no encontrada: {COL_ROOT_PATH}")

        # 3) Truncar default_code desde el token
        if COL_DEFAULT_CODE in df.columns:
            df[COL_DEFAULT_CODE] = df[COL_DEFAULT_CODE].apply(strip_default_code_suffix)
        else:
            print(f"⚠️  Columna no encontrada: {COL_DEFAULT_CODE}")

        # Guardar
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)

        print(f"💾 Exportando a: {output_path}")
        df.to_excel(output_path, index=False, engine="openpyxl")
        print("🎉 Exportación completada")
        return True

    except pd.errors.EmptyDataError:
        print("❌ Error: El archivo CSV está vacío")
        return False
    except pd.errors.ParserError as e:
        print(f"❌ Error de parseo: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def main() -> None:
    print("=" * 60)
    print("🛠️  NORMALIZADOR DE PRODUCTOS")
    print("=" * 60)
    print(f"📁 Entrada: {input_file}")
    print(f"📁 Salida:  {output_file}")
    print("-" * 60)
    ok = process_products(input_file, output_file)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()


