import os
import threading
from regex_parser import parse_file 
import csv

def procesar_archivo(p):
    datos = parse_file(p['archivo'], p['pid'])
    guardar_csv(datos)
   
    print(f"[{p['pid']}] Completado. {datos.get('archivo', os.path.basename(p['archivo']))} procesado.")

def guardar_csv(data):
    encabezado = [
        "pid", "archivo", 
        "fechas", "nombres", "palabras_suecas", "lugares", 
        "transportes", "dinero", "correos", "direcciones", "hashtags"
        # Pato, añade aquí cualquier otra clave nueva que el regex_parser.py pueda generar
    ]
    
    
    file_exists = os.path.isfile("resultado.csv")
    
    with open("resultado.csv", "a", newline='', encoding='utf-8') as f:
    
        
        writer = csv.DictWriter(f, fieldnames=encabezado, extrasaction='ignore') 

        if not file_exists or os.path.getsize("resultado.csv") == 0: 
            writer.writeheader()
        
        writer.writerow(data)
