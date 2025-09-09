#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para formatear nombres en archivos CSV a Title Case y exportar a XLSX

INSTRUCCIONES DE INSTALACIÓN:
1. Instalar Python 3.6 o superior
2. Instalar las dependencias necesarias:
   pip install pandas openpyxl

INSTRUCCIONES DE EJECUCIÓN:
1. Modificar las variables input_file, output_file y COLUMNS_TO_FORMAT en este script
2. Ejecutar: python name_formated.py

El script procesará las columnas definidas en la variable COLUMNS_TO_FORMAT
para convertirlas a Title Case. Puedes modificar fácilmente esta lista según tus necesidades.

Todas las demás columnas se mantendrán sin cambios.
"""

import pandas as pd
import os
import sys
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN - MODIFICAR ESTAS RUTAS SEGÚN NECESITES
# =============================================================================

# Ruta del archivo CSV de entrada
input_file = "../data/customers list (1).xlsx - Clientes (1).csv"

# Ruta del archivo XLSX de salida
output_file = "../data/clientes_formateados.xlsx"

# =============================================================================
# CONFIGURACIÓN DE COLUMNAS - MODIFICAR ESTOS NOMBRES SEGÚN TU CSV
# =============================================================================

# Nombres de las columnas que quieres formatear a Title Case
# Agrega o quita columnas según necesites
COLUMNS_TO_FORMAT = [
    'Last Name',
    'First Name', 
    'Spouse Name',
    'Child 1',
    'Child 2',
    'Child 3'
]

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def format_to_title_case(text):
    """
    Convierte un texto a Title Case (primera letra de cada palabra en mayúscula)
    
    Args:
        text: String a formatear
        
    Returns:
        String formateado en Title Case
    """
    if pd.isna(text) or text == "":
        return text
    
    # Convertir a string si no lo es
    text = str(text)
    
    # Aplicar Title Case
    return text.title()

def process_csv_to_xlsx(input_path, output_path):
    """
    Procesa un archivo CSV, formatea las columnas de nombres y exporta a XLSX
    
    Args:
        input_path (str): Ruta del archivo CSV de entrada
        output_path (str): Ruta del archivo XLSX de salida
    """
    
    # Verificar que el archivo de entrada existe
    if not os.path.exists(input_path):
        print(f"❌ Error: El archivo '{input_path}' no existe.")
        print("Por favor, verifica la ruta del archivo de entrada.")
        return False
    
    try:
        print(f"📖 Leyendo archivo: {input_path}")
        
        # Leer el archivo CSV
        df = pd.read_csv(input_path, encoding='utf-8')
        
        print(f"✅ Archivo leído exitosamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
        
        # Formatear las columnas que existen en el DataFrame
        formatted_columns = []
        for column in COLUMNS_TO_FORMAT:
            if column in df.columns:
                print(f"🔄 Formateando columna: {column}")
                df[column] = df[column].apply(format_to_title_case)
                formatted_columns.append(column)
            else:
                print(f"⚠️  Columna '{column}' no encontrada en el archivo")
        
        if formatted_columns:
            print(f"✅ Columnas formateadas: {', '.join(formatted_columns)}")
        else:
            print("⚠️  No se encontraron columnas para formatear")
        
        # Crear el directorio de salida si no existe
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"💾 Exportando a: {output_path}")
        
        # Exportar a XLSX
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        print(f"✅ Archivo exportado exitosamente: {output_path}")
        print(f"📊 Resumen:")
        print(f"   - Filas procesadas: {len(df)}")
        print(f"   - Columnas totales: {len(df.columns)}")
        print(f"   - Columnas formateadas: {len(formatted_columns)}")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: No se pudo encontrar el archivo '{input_path}'")
        return False
    except pd.errors.EmptyDataError:
        print(f"❌ Error: El archivo '{input_path}' está vacío")
        return False
    except pd.errors.ParserError as e:
        print(f"❌ Error al parsear el archivo CSV: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """
    Función principal del script
    """
    print("=" * 60)
    print("🔄 PROCESADOR DE NOMBRES CSV A XLSX")
    print("=" * 60)
    print(f"📁 Archivo de entrada: {input_file}")
    print(f"📁 Archivo de salida: {output_file}")
    print("-" * 60)
    
    # Procesar el archivo
    success = process_csv_to_xlsx(input_file, output_file)
    
    if success:
        print("-" * 60)
        print("🎉 ¡Proceso completado exitosamente!")
        print(f"📄 Resultado guardado en: {output_file}")
    else:
        print("-" * 60)
        print("❌ El proceso falló. Revisa los errores anteriores.")
        sys.exit(1)

# =============================================================================
# EJECUTAR SCRIPT
# =============================================================================

if __name__ == "__main__":
    main()
