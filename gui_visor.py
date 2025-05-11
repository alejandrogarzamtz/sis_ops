import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
import os
import shutil
from scheduler import fcfs, sjf, round_robin
from client import procesar_archivo
import random

root = tk.Tk()
modo = tk.StringVar(value='thread')
algoritmo = tk.StringVar(value='FCFS')
quantum = tk.IntVar(value=2)
cantidad_procesos = tk.IntVar(value=3)
procesos = []
burst_base = 3
uploads_folder = "uploads"
os.makedirs(uploads_folder, exist_ok=True)

def seleccionar_archivos():
    global procesos
    archivos = filedialog.askopenfilenames(filetypes=[("Archivos de texto", "*.txt")])
    if not archivos:
        return

    max_procesos = min(cantidad_procesos.get(), 8)
    inicio_index = len(procesos)
    for i, archivo in enumerate(archivos[:max_procesos]):
        destino = os.path.join(uploads_folder, os.path.basename(archivo))
        shutil.copy(archivo, destino)
        pid = f"P{inicio_index + i + 1}"
        arrival = 0  # tiempo base 0 para simplificar visual
        burst = burst_base + random.randint(1, 4)
        procesos.append({
            "pid": pid,
            "archivo": destino,
            "arrival": arrival,
            "burst": burst,
            "remaining": burst
        })
        listbox.insert(tk.END, f"{pid} - {os.path.basename(archivo)} (Burst={burst})")

def borrar_seleccionado():
    seleccion = listbox.curselection()
    if seleccion:
        index = seleccion[0]
        listbox.delete(index)
        del procesos[index]
        boton_eliminar.pack_forget()

def toggle_quantum():
    if algoritmo.get() == "RR":
        entry_quantum.config(state="normal")
    else:
        entry_quantum.config(state="disabled")

def mostrar_boton_eliminar(event):
    seleccion = listbox.curselection()
    if seleccion:
        boton_eliminar.pack(pady=5)
    else:
        boton_eliminar.pack_forget()

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
    y = 50
    escala = 40

    for i, p in enumerate(plan):
        color = f"#{random.randint(100,255):02x}{random.randint(100,255):02x}{random.randint(100,255):02x}"
        colores[p['pid']] = color
        x_inicio = x_base + int(p['start']) * escala
        x_fin = x_base + int(p['end']) * escala

        canvas.create_rectangle(x_inicio, y, x_fin, y + 30, fill=color, outline="black")
        canvas.create_text((x_inicio + x_fin) // 2, y + 15, text=p['pid'], fill="black")
        canvas.create_text(x_inicio, y + 35, text=str(int(p['start'])), fill="black")
        if i == len(plan) - 1:
            canvas.create_text(x_fin, y + 35, text=str(int(p['end'])), fill="black")

        resultados_tabla.insert("", "end", values=[
            p['pid'], os.path.basename(p['archivo']), round(p['start'], 2), round(p['end'], 2), p['burst'], round(p['waiting'], 2), round(p['turnaround'], 2)
        ])

        if modo.get() == "thread":
            threading.Thread(target=procesar_archivo, args=(p,)).start()
        elif modo.get() == "fork":
            pid = os.fork()
            if pid == 0:
                procesar_archivo(p)
                os._exit(0)

root.title("Simulador OS - Scheduling Visual")
root.geometry("1000x700")

frame_config = tk.Frame(root)
frame_config.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

frame_visual = tk.Frame(root)
frame_visual.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

tk.Label(frame_config, text="Modo:").pack()
tk.Radiobutton(frame_config, text="Threads", variable=modo, value='thread').pack(anchor="w")
tk.Radiobutton(frame_config, text="Forks", variable=modo, value='fork').pack(anchor="w")

tk.Label(frame_config, text="Algoritmo:").pack(pady=(10, 0))
tk.Radiobutton(frame_config, text="FCFS", variable=algoritmo, value='FCFS', command=toggle_quantum).pack(anchor="w")
tk.Radiobutton(frame_config, text="SJF", variable=algoritmo, value='SJF', command=toggle_quantum).pack(anchor="w")
tk.Radiobutton(frame_config, text="Round Robin", variable=algoritmo, value='RR', command=toggle_quantum).pack(anchor="w")

tk.Label(frame_config, text="Quantum (RR):").pack()
entry_quantum = tk.Entry(frame_config, textvariable=quantum, state="disabled")
entry_quantum.pack()

tk.Label(frame_config, text="Número de Forks/Threads:").pack()
tk.Entry(frame_config, textvariable=cantidad_procesos).pack()

tk.Button(frame_config, text="Subir archivos .txt", command=seleccionar_archivos).pack(pady=10)

listbox = tk.Listbox(frame_config, height=10, width=40)
listbox.pack(pady=5)

boton_eliminar = tk.Button(frame_config, text="Eliminar seleccionado", command=borrar_seleccionado)
listbox.bind("<<ListboxSelect>>", mostrar_boton_eliminar)

tk.Button(frame_config, text="Iniciar Ejecución", command=iniciar).pack(pady=10)

canvas = tk.Canvas(frame_visual, bg="#f5f5f5", height=300)
canvas.pack(fill=tk.X, padx=10, pady=10)

cols = ("PID", "Archivo", "Inicio", "Fin", "Burst", "Waiting", "Turnaround")
resultados_tabla = ttk.Treeview(frame_visual, columns=cols, show="headings")
for col in cols:
    resultados_tabla.heading(col, text=col)
    resultados_tabla.column(col, width=100)
resultados_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

toggle_quantum()
root.mainloop()

