#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para asignar tipo de membresía y precio en base a datos familiares

INSTRUCCIONES DE INSTALACIÓN:
1. Instalar Python 3.8 o superior
2. Instalar dependencias:
   pip install pandas openpyxl

INSTRUCCIONES DE EJECUCIÓN:
1. Modificar las variables input_file, output_file y la configuración de columnas/precios
2. Ejecutar: python membership_assigner.py

LÓGICA:
- Si en cualquiera de las columnas configuradas (por ejemplo: Spouse Name, Child 1, Child 2, Child 3)
  hay algún valor no vacío en la fila, entonces:
    membership_type = FAMILY_LABEL
    membership_price = FAMILY_PRICE
  De lo contrario:
    membership_type = INDIVIDUAL_LABEL
    membership_price = INDIVIDUAL_PRICE

El script añade dos columnas nuevas al final del archivo:
- Membership Type (configurable)
- Membership Price (configurable)
"""

import os
import sys
import pandas as pd


# =============================================================================
# CONFIGURACIÓN - MODIFICA ESTAS VARIABLES SEGÚN TUS NECESIDADES
# =============================================================================

# Rutas de entrada/salida
input_file = "../data/customers list (1).xlsx - Clientes (1).csv"
output_file = "../data/clientes_con_membresia.xlsx"

# Columnas a inspeccionar para determinar si hay familia (cónyuge o hijos)
FAMILY_INDICATOR_COLUMNS = [
    "Spouse Name",
    "Child 1",
    "Child 2",
    "Child 3",
]

# Encabezados de las nuevas columnas a crear
OUTPUT_MEMBERSHIP_TYPE_COL = "Membership Type"
OUTPUT_MEMBERSHIP_PRICE_COL = "Membership Price"

# Etiquetas y precios configurables
INDIVIDUAL_LABEL = "Individual"
FAMILY_LABEL = "Family"

# Precios (números). Puedes usar float o int según tu caso
INDIVIDUAL_PRICE = 50
FAMILY_PRICE = 80


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def has_any_family_value(row: pd.Series, columns: list[str]) -> bool:
    """
    Devuelve True si alguna columna de `columns` en la fila `row` tiene un valor no nulo y no vacío.
    """
    for column_name in columns:
        if column_name in row.index:
            value = row[column_name]
            if pd.notna(value) and str(value).strip() != "":
                return True
    return False


def assign_membership(row: pd.Series) -> tuple[str, float]:
    """
    Determina (tipo, precio) de la membresía para una fila.
    """
    if has_any_family_value(row, FAMILY_INDICATOR_COLUMNS):
        return FAMILY_LABEL, FAMILY_PRICE
    return INDIVIDUAL_LABEL, INDIVIDUAL_PRICE


# =============================================================================
# PROCESAMIENTO PRINCIPAL
# =============================================================================

def process_file(input_path: str, output_path: str) -> bool:
    # Validación de existencia del archivo de entrada
    if not os.path.exists(input_path):
        print(f"❌ Error: El archivo '{input_path}' no existe.")
        return False

    try:
        print(f"📖 Leyendo archivo: {input_path}")
        df = pd.read_csv(input_path, encoding="utf-8")

        print(f"✅ Archivo leído: {len(df)} filas, {len(df.columns)} columnas")

        # Calcular membresía por fila
        types: list[str] = []
        prices: list[float] = []

        for _, row in df.iterrows():
            m_type, m_price = assign_membership(row)
            types.append(m_type)
            prices.append(m_price)

        # Añadir columnas al DataFrame
        df[OUTPUT_MEMBERSHIP_TYPE_COL] = types
        df[OUTPUT_MEMBERSHIP_PRICE_COL] = prices

        # Crear directorio de salida si no existe
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)

        print(f"💾 Guardando en: {output_path}")
        df.to_excel(output_path, index=False, engine="openpyxl")
        print("🎉 Archivo exportado con columnas de membresía añadidas")
        return True

    except pd.errors.EmptyDataError:
        print(f"❌ Error: El archivo '{input_path}' está vacío")
        return False
    except pd.errors.ParserError as e:
        print(f"❌ Error al parsear el CSV: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def main() -> None:
    print("=" * 60)
    print("🧩 ASIGNADOR DE MEMBRESÍA (INDIVIDUAL/FAMILY)")
    print("=" * 60)
    print(f"📁 Entrada: {input_file}")
    print(f"📁 Salida:  {output_file}")
    print("-" * 60)

    ok = process_file(input_file, output_file)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()


