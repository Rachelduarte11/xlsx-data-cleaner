#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de categorías en archivos CSV

INSTRUCCIONES DE INSTALACIÓN:
1) Python 3.8+
2) Dependencias: pandas
   pip install pandas

INSTRUCCIONES DE EJECUCIÓN:
1) Ajusta las variables de configuración (ruta del archivo, columna a analizar)
2) Ejecuta: python analyze_categories.py

Descripción:
- Analiza las categorías únicas en una columna específica
- Muestra conteos y estadísticas
- Exporta resultados a CSV y XLSX
"""

import os
import sys
import pandas as pd
from collections import Counter

# =============================================================================
# CONFIGURACIÓN - MODIFICA ESTAS VARIABLES
# =============================================================================

# Ruta del archivo CSV a analizar
INPUT_CSV = "../data/customers list (1).xlsx - Clientes (1).csv"

# Nombre de la columna a analizar
COLUMN_TO_ANALYZE = "Company"

# Archivos de salida
OUTPUT_CSV = "../data/exported/categories_analysis.csv"
OUTPUT_XLSX = "../data/exported/categories_analysis.xlsx"

# =============================================================================
# FUNCIONES DE ANÁLISIS
# =============================================================================

def analyze_categories(input_path: str, column_name: str, output_csv: str, output_xlsx: str) -> bool:
    """
    Analiza las categorías en una columna específica
    """
    if not os.path.exists(input_path):
        print(f"❌ Error: No existe el archivo: {input_path}")
        return False

    try:
        print(f"📖 Leyendo archivo: {input_path}")
        df = pd.read_csv(input_path, encoding="utf-8")
        
        if column_name not in df.columns:
            print(f"❌ Error: La columna '{column_name}' no existe en el archivo")
            print(f"Columnas disponibles: {', '.join(df.columns)}")
            return False

        print(f"✅ Archivo leído: {len(df)} filas, {len(df.columns)} columnas")
        print(f"🔍 Analizando columna: {column_name}")

        # Limpiar datos: eliminar valores nulos y vacíos
        clean_data = df[column_name].dropna()
        clean_data = clean_data[clean_data != ""]
        clean_data = clean_data[clean_data.str.strip() != ""]

        print(f"📊 Datos válidos para analizar: {len(clean_data)} de {len(df)} filas")

        # Contar categorías
        category_counts = Counter(clean_data)
        
        # Crear DataFrame con resultados
        results_df = pd.DataFrame([
            {"Category": category, "Count": count, "Percentage": round((count/len(clean_data))*100, 2)}
            for category, count in category_counts.most_common()
        ])

        # Mostrar estadísticas
        print("\n" + "="*60)
        print("📈 ESTADÍSTICAS DE CATEGORÍAS")
        print("="*60)
        print(f"Total de categorías únicas: {len(category_counts)}")
        print(f"Total de registros analizados: {len(clean_data)}")
        print(f"Categoría más frecuente: {category_counts.most_common(1)[0][0]} ({category_counts.most_common(1)[0][1]} registros)")
        
        print(f"\n📋 TOP 10 CATEGORÍAS:")
        print("-" * 40)
        for i, (category, count) in enumerate(category_counts.most_common(10), 1):
            percentage = (count/len(clean_data))*100
            print(f"{i:2d}. {category:<30} | {count:3d} ({percentage:5.1f}%)")

        # Crear directorio de salida si no existe
        out_dir = os.path.dirname(output_csv)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)

        # Exportar resultados
        print(f"\n💾 Exportando resultados...")
        
        # CSV
        results_df.to_csv(output_csv, index=False, encoding="utf-8")
        print(f"✅ CSV guardado: {output_csv}")
        
        # XLSX
        results_df.to_excel(output_xlsx, index=False, engine="openpyxl")
        print(f"✅ XLSX guardado: {output_xlsx}")

        # Mostrar todas las categorías si son pocas
        if len(category_counts) <= 20:
            print(f"\n📝 TODAS LAS CATEGORÍAS:")
            print("-" * 50)
            for category, count in category_counts.most_common():
                percentage = (count/len(clean_data))*100
                print(f"{category:<35} | {count:3d} ({percentage:5.1f}%)")

        print("\n🎉 Análisis completado exitosamente")
        return True

    except pd.errors.EmptyDataError:
        print("❌ Error: El archivo CSV está vacío")
        return False
    except pd.errors.ParserError as e:
        print(f"❌ Error al parsear CSV: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("📊 ANALIZADOR DE CATEGORÍAS")
    print("=" * 60)
    print(f"📁 Archivo: {INPUT_CSV}")
    print(f"🔍 Columna: {COLUMN_TO_ANALYZE}")
    print(f"📄 Salida CSV: {OUTPUT_CSV}")
    print(f"📄 Salida XLSX: {OUTPUT_XLSX}")
    print("-" * 60)

    success = analyze_categories(INPUT_CSV, COLUMN_TO_ANALYZE, OUTPUT_CSV, OUTPUT_XLSX)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
