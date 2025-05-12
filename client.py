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
        "Nombres", "Paises", "Fechas_con_Formato", "Razones_Inmigracion", "Niveles_Educacion",
        "Escuelas_Mencionadas", "Lenguajes_Hablados", "Eventos_Historicos", "Ocupaciones",
        "Practicas_Culturales", "Destinos", "Puertos_de_Entrada", "Fechas_de_Emigracion",
        "Modos_de_Viaje", "Afiliaciones_Iglesia", "Problemas_de_Salud", "Ubicaciones_Geograficas",
        "Años_de_Graduacion", "Causas_de_Muerte", "Empleadores", "Titulos_de_Trabajo",
        "Participacion_Comunitaria", "Actividades_Sociales"
    ]

    file_exists = os.path.isfile("resultado.csv")

    with open("resultado.csv", "a", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=encabezado, extrasaction='ignore')

        if not file_exists or os.path.getsize("resultado.csv") == 0:
            writer.writeheader()

        writer.writerow(data)

