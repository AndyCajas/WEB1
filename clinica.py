import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from collections import defaultdict

# Simulación de Base de Datos en memoria
usuarios = [
    {"ID": 1, "Nombre": "Admin", "Tipo": "Administrador"},
    {"ID": 2, "Nombre": "Juan Perez", "Tipo": "Paciente"}
]

medicos = [
    {"ID": 1, "Nombre": "Dra. Ana Lopez", "Especialidad": "Cardiología"},
    {"ID": 2, "Nombre": "Dr. Mario Gómez", "Especialidad": "Dermatología"}
]

citas = []  # Lista para almacenar citas

# Función para iniciar sesión
def iniciar_sesion():
    usuario = entry_usuario.get()
    tipo_usuario = None

    for u in usuarios:
        if u["Nombre"] == usuario:
            tipo_usuario = u["Tipo"]
            usuario_id = u["ID"]
            break

    if tipo_usuario:
        ventana_inicio.destroy()
        if tipo_usuario == "Paciente":
            mostrar_interfaz_paciente(usuario_id)
        elif tipo_usuario == "Administrador":
            mostrar_interfaz_administrador()
    else:
        messagebox.showerror("Error", "Usuario no encontrado")

# Función para agendar citas
def agendar_cita(usuario_id, tipo):
    medico_id = combo_medico.get()
    fecha = entry_fecha.get()
    hora = entry_hora.get()

    # Validar disponibilidad
    for cita in citas:
        if cita["MédicoID"] == int(medico_id) and cita["Fecha"] == fecha and cita["Hora"] == hora:
            messagebox.showerror("Error", "El horario ya está ocupado")
            return

    # Agregar cita a la lista
    citas.append({"ID": len(citas)+1, "UsuarioID": usuario_id, "MédicoID": int(medico_id), "Fecha": fecha, "Hora": hora, "Estado": "Confirmada"})
    messagebox.showinfo("Éxito", "Cita agendada correctamente")

    # Refrescar vista de citas si es administrador
    if tipo == "Administrador":
        mostrar_citas_administrador()

# Interfaz para pacientes
def mostrar_interfaz_paciente(usuario_id):
    ventana_paciente = tk.Tk()
    ventana_paciente.title("Gestión de Citas - Paciente")

    tk.Label(ventana_paciente, text="Agendar Nueva Cita", font=("Arial", 14)).pack(pady=10)

    tk.Label(ventana_paciente, text="Médico:").pack()
    global combo_medico
    combo_medico = ttk.Combobox(ventana_paciente, values=[f"{m['ID']} - {m['Nombre']} ({m['Especialidad']})" for m in medicos])
    combo_medico.pack()

    tk.Label(ventana_paciente, text="Fecha (YYYY-MM-DD):").pack()
    global entry_fecha
    entry_fecha = tk.Entry(ventana_paciente)
    entry_fecha.pack()

    tk.Label(ventana_paciente, text="Hora (HH:MM):").pack()
    global entry_hora
    entry_hora = tk.Entry(ventana_paciente)
    entry_hora.pack()

    tk.Button(ventana_paciente, text="Agendar Cita", command=lambda: agendar_cita(usuario_id, "Paciente")).pack(pady=10)

    ventana_paciente.mainloop()

# Interfaz para administrador
def mostrar_interfaz_administrador():
    ventana_admin = tk.Tk()
    ventana_admin.title("Gestión de Citas - Administrador")

    tk.Label(ventana_admin, text="Citas Programadas", font=("Arial", 14)).pack(pady=10)

    # Mostrar citas
    global tabla_citas
    tabla_citas = ttk.Treeview(ventana_admin, columns=("ID", "Paciente", "Médico", "Fecha", "Hora", "Estado"), show="headings")
    tabla_citas.heading("ID", text="ID")
    tabla_citas.heading("Paciente", text="Paciente")
    tabla_citas.heading("Médico", text="Médico")
    tabla_citas.heading("Fecha", text="Fecha")
    tabla_citas.heading("Hora", text="Hora")
    tabla_citas.heading("Estado", text="Estado")
    tabla_citas.pack(fill="both", expand=True)

    mostrar_citas_administrador()

    ventana_admin.mainloop()

# Función para mostrar citas en la vista del administrador
def mostrar_citas_administrador():
    for row in tabla_citas.get_children():
        tabla_citas.delete(row)

    for cita in citas:
        paciente = next((u["Nombre"] for u in usuarios if u["ID"] == cita["UsuarioID"]), "Desconocido")
        medico = next((m["Nombre"] for m in medicos if m["ID"] == cita["MédicoID"]), "Desconocido")
        tabla_citas.insert("", "end", values=(cita["ID"], paciente, medico, cita["Fecha"], cita["Hora"], cita["Estado"]))

# Ventana de inicio de sesión
ventana_inicio = tk.Tk()
ventana_inicio.title("Inicio de Sesión")

frame_inicio = tk.Frame(ventana_inicio)
frame_inicio.pack(pady=20)

tk.Label(frame_inicio, text="Usuario:").pack()
entry_usuario = tk.Entry(frame_inicio)
entry_usuario.pack()

tk.Button(frame_inicio, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)

ventana_inicio.mainloop()
