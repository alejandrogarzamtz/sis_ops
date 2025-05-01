import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
import os
import shutil
from scheduler import fcfs, sjf, round_robin
from client import procesar_archivo
import random

modo = tk.StringVar(value='thread')
algoritmo = tk.StringVar(value='FCFS')
quantum = tk.IntVar(value=2)
procesos = []
burst_base = 3
uploads_folder = "uploads"
os.makedirs(uploads_folder, exist_ok=True)

def seleccionar_archivos():
    global procesos
    archivos = filedialog.askopenfilenames(filetypes=[("Archivos de texto", "*.txt")])
    procesos.clear()
    listbox.delete(0, tk.END)
    for i, archivo in enumerate(archivos):
        destino = os.path.join(uploads_folder, os.path.basename(archivo))
        shutil.copy(archivo, destino)
        pid = f"P{i+1}"
        arrival = time.time() + i
        burst = burst_base + random.randint(1, 4)
        procesos.append({
            "pid": pid,
            "archivo": destino,
            "arrival": arrival,
            "burst": burst,
            "remaining": burst
        })
        listbox.insert(tk.END, f"{pid} - {os.path.basename(archivo)} (Burst={burst})")

def iniciar():
    if not procesos:
        messagebox.showerror("Error", "Carga al menos un archivo .txt")
        return

    canvas.delete("all")
    resultados_tabla.delete(*resultados_tabla.get_children())
    plan = []

    if algoritmo.get() == "FCFS":
        plan = fcfs(procesos)
    elif algoritmo.get() == "SJF":
        plan = sjf(procesos)
    elif algoritmo.get() == "RR":
        plan = round_robin(procesos, quantum.get())
    else:
        messagebox.showerror("Error", "Algoritmo inválido")
        return

    colores = {}
    x_base = 50
    y_base = 30
    escala = 40

    for i, p in enumerate(plan):
        color = f"#{random.randint(100,255):02x}{random.randint(100,255):02x}{random.randint(100,255):02x}"
        colores[p['pid']] = color
        p['y'] = y_base + i * 40

    def ejecutar(p):
        start = time.time()
        duracion = p['end'] - p['start']
        for i in range(int(duracion*10)):
            time.sleep(0.1)
            progreso = i / (duracion*10)
            canvas.create_rectangle(x_base + p['start']*escala,
                                    p['y'],
                                    x_base + (p['start'] + progreso*duracion)*escala,
                                    p['y'] + 20,
                                    fill=colores[p['pid']], outline="")
        procesar_archivo(p)
        resultados_tabla.insert("", "end", values=[
            p['pid'], os.path.basename(p['archivo']), p['start'], p['end'], p['burst'], p['waiting'], p['turnaround']
        ])

    for p in plan:
        if modo.get() == "thread":
            t = threading.Thread(target=ejecutar, args=(p,))
            t.start()
        elif modo.get() == "fork":
            pid = os.fork()
            if pid == 0:
                ejecutar(p)
                os._exit(0)

root = tk.Tk()
root.title("Simulador OS - Scheduling Visual")
root.geometry("1000x700")

frame_config = tk.Frame(root)
frame_config.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

frame_visual = tk.Frame(root)
frame_visual.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

tk.Label(frame_config, text="Modo:").pack()
tk.Radiobutton(frame_config, text="Threads", variable=modo, value='thread').pack(anchor="w")
tk.Radiobutton(frame_config, text="Forks", variable=modo, value='fork').pack(anchor="w")

tk.Label(frame_config, text="Algoritmo:").pack(pady=(10,0))
tk.Radiobutton(frame_config, text="FCFS", variable=algoritmo, value='FCFS').pack(anchor="w")
tk.Radiobutton(frame_config, text="SJF", variable=algoritmo, value='SJF').pack(anchor="w")
tk.Radiobutton(frame_config, text="Round Robin", variable=algoritmo, value='RR').pack(anchor="w")

tk.Label(frame_config, text="Quantum (RR):").pack()
tk.Entry(frame_config, textvariable=quantum).pack()

tk.Button(frame_config, text="Subir archivos .txt", command=seleccionar_archivos).pack(pady=10)

listbox = tk.Listbox(frame_config, height=10, width=40)
listbox.pack(pady=5)

tk.Button(frame_config, text="Iniciar Ejecución", command=iniciar).pack(pady=10)

canvas = tk.Canvas(frame_visual, bg="#f5f5f5", height=300)
canvas.pack(fill=tk.X, padx=10, pady=10)

cols = ("PID", "Archivo", "Inicio", "Fin", "Burst", "Waiting", "Turnaround")
resultados_tabla = ttk.Treeview(frame_visual, columns=cols, show="headings")
for col in cols:
    resultados_tabla.heading(col, text=col)
    resultados_tabla.column(col, width=100)
resultados_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
