## ✅ Funcionalidades

- Subida de archivos .txt desde GUI (no desde consola)
- Selección del algoritmo de planificación:
  - FCFS (First Come First Serve)
  - SJF (Shortest Job First)
  - RR (Round Robin) con quantum configurable
- Elección entre ejecución con forks o threads
- Visualización en tiempo real (tipo Gantt) con animaciones por proceso
- Extracción de datos relevantes con expresiones regulares
- Generación automática de resultado.csv con los datos de los archivos procesados
- Arquitectura Cliente-Servidor opcional (con server.py), permite que múltiples clientes inicien procesamiento al mismo tiempo mediante un trigger

---

## 🗂️ Estructura del Proyecto

sistema_scheduling/
├── gui_visor.py         # Interfaz gráfica principal
├── client.py            # Lógica de procesamiento con fork/thread
├── server.py            # Servidor que maneja eventos y triggers
├── scheduler.py         # Implementación de algoritmos FCFS, SJF, RR
├── regex_parser.py      # Extracción de datos con regex
├── resultado.csv        # (se genera automáticamente)
├── uploads/             # Carpeta donde se copian los archivos .txt subidos
└── README.md            # Este archivo

---

## ⚙️ Requisitos

- Python 3.8 o superior
- Tkinter para la GUI (ya viene preinstalado en Windows/macOS)

En Linux, si no lo tienes:
sudo apt install python3-tk

---

## 🚀 Instrucciones para correr el proyecto

1. Ejecutar el servidor (solo si usarás múltiples clientes):

python3 server.py

Esto abre un servidor en el puerto 9999, capaz de aceptar múltiples clientes a la vez. Los clientes se conectan, esperan, y al recibir el trigger LIMPIEZA, comienzan a procesar.

2. Ejecutar la interfaz gráfica (el cliente):

python3 gui_visor.py

Desde la interfaz puedes:
- Subir uno o varios .txt
- Elegir algoritmo y modo de ejecución
- Ver la animación visual de cada proceso
- Ver métricas por proceso (inicio, fin, turnaround, waiting time, etc.)
- Generar automáticamente resultado.csv

---

## 🌐 IP del servidor (si usas múltiples equipos)

Por defecto, en el código está esta línea:
SERVER_HOST = 'localhost'

Si corres el servidor en otra computadora:

1. En esa computadora, ejecuta:
   - ipconfig (Windows) o ifconfig (Linux/Mac)
2. Copia la IP local, por ejemplo: 192.168.0.52
3. En los clientes, reemplaza la línea anterior con:
   SERVER_HOST = '192.168.0.52'
4. Ya podrán conectarse desde otras computadoras en la misma red

La IP puede dejarse quemada en el código, solo asegúrate de actualizarla si cambia.

---

## 🖱️ ¿Qué hace el usuario?

- No toca la terminal
- Solo abre gui_visor.py
- Sube los archivos .txt
- Selecciona algoritmo y modo
- Da clic en “Iniciar ejecución”
- Observa la animación y los resultados

---

## 📌 Consideraciones técnicas

- La carpeta uploads/ debe existir (se crea sola si no está)
- Todos los archivos .py deben estar en el mismo directorio
- El sistema puede usarse en modo local (solo GUI) o con arquitectura cliente-servidor

---

## ✨ Mejoras sugeridas (futuras)

- Agregar un campo en la GUI para permitir ingresar la IP del servidor
- Implementar logging por proceso
- Exportación PDF o JSON de las métricas
- Permitir colas dinámicas con más usuarios concurrentes

---

## 👤 Créditos

Desarrollado por: Alejandro Garza, Vinicio Cantú, Patricio Dávila, Ricardo Aguirre

Proyecto final para la materia de Sistemas Operativos
