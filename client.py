import os
import threading
from regex_parser import parse_file
import csv

def procesar_archivo(p):
    datos = parse_file(p['archivo'], p['pid'])
    guardar_csv(datos)
    print(f"[{p['pid']}] Completado. {datos['archivo']} procesado.")

def guardar_csv(data):
    encabezado = ["pid", "archivo", "fechas", "nombres", "palabras_suecas", "lugares", "transportes", "dinero"]
    file_exists = os.path.isfile("resultado.csv")
    with open("resultado.csv", "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=encabezado)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
