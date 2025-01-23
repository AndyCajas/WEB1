import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import sqlite3
import os

# === Clase CajaFuerte ===
class CajaFuerte:
    def __init__(self):
        self.password = None
        self.intentos_maximos = 3
        self.bloqueada = False
        self.conexion_db()

    def conexion_db(self):
        """Conectar a la base de datos SQLite y crear la tabla si no existe."""
        self.conn = sqlite3.connect("caja_fuerte.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS contenido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def establecer_password(self, root):
        """Permite al usuario establecer una contraseña."""
        while True:
            password = simpledialog.askstring("Contraseña", "Establezca una nueva contraseña:", show='*', parent=root)
            confirmar = simpledialog.askstring("Confirmar", "Confirme la contraseña:", show='*', parent=root)
            if password == confirmar:
                self.password = password
                messagebox.showinfo("Éxito", "Contraseña establecida exitosamente.", parent=root)
                break
            else:
                messagebox.showerror("Error", "Las contraseñas no coinciden. Intente nuevamente.", parent=root)

    def verificar_password(self, root):
        """Verifica la contraseña ingresada por el usuario."""
        intentos = 0
        while intentos < self.intentos_maximos:
            password = simpledialog.askstring("Contraseña", "Ingrese la contraseña:", show='*', parent=root)
            if password == self.password:
                return True
            else:
                intentos += 1
                restantes = self.intentos_maximos - intentos
                messagebox.showerror("Error", f"Contraseña incorrecta. Intentos restantes: {restantes}", parent=root)

        self.bloqueada = True
        messagebox.showwarning("Bloqueada", "Caja fuerte bloqueada. Intente más tarde.", parent=root)
        return False

    def guardar_item(self, item, root):
        """Guarda un nuevo item en la base de datos."""
        if self.verificar_password(root):
            self.cursor.execute("INSERT INTO contenido (item) VALUES (?)", (item,))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Item '{item}' guardado exitosamente.", parent=root)

    def ver_contenido(self, root):
        """Muestra el contenido actual almacenado en la base de datos."""
        if self.verificar_password(root):
            self.cursor.execute("SELECT id, item FROM contenido")
            rows = self.cursor.fetchall()
            if rows:
                contenido = "\n".join([f"{row[0]}. {row[1]}" for row in rows])
                messagebox.showinfo("Contenido", f"Contenido de la caja fuerte:\n{contenido}", parent=root)
            else:
                messagebox.showinfo("Vacío", "La caja fuerte está vacía.", parent=root)

    def retirar_item(self, id_item, root):
        """Elimina un item de la base de datos por su ID."""
        if self.verificar_password(root):
            self.cursor.execute("DELETE FROM contenido WHERE id = ?", (id_item,))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Item con ID '{id_item}' retirado exitosamente.", parent=root)

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        self.conn.close()


# === Funciones adicionales ===
def abrir_block_notas():
    """Abre un bloque de notas básico."""
    def guardar_notas():
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            with open(archivo, "w") as file:
                file.write(text.get("1.0", tk.END))
            messagebox.showinfo("Éxito", "Notas guardadas exitosamente.")

    notas = tk.Toplevel()
    notas.title("Block de Notas")
    notas.geometry("500x400")
    notas.configure(bg="#34495E")

    text = tk.Text(notas, wrap=tk.WORD, bg="#ECF0F1", fg="#2C3E50", font=("Arial", 12))
    text.pack(expand=True, fill=tk.BOTH)

    boton_guardar = tk.Button(notas, text="Guardar Notas", command=guardar_notas, bg="#27AE60", fg="white", font=("Arial", 12, "bold"), relief="flat")
    boton_guardar.pack(pady=10)

    notas.mainloop()


# === Interfaz principal ===
def main():
    caja = CajaFuerte()

    # Funciones para la interfaz
    def establecer_password():
        caja.establecer_password(root)

    def guardar_item():
        item = simpledialog.askstring("Guardar Item", "Ingrese el item a guardar:", parent=root)
        if item:
            caja.guardar_item(item, root)

    def ver_contenido():
        caja.ver_contenido(root)

    def retirar_item():
        id_item = simpledialog.askinteger("Retirar Item", "Ingrese el ID del item a retirar:", parent=root)
        if id_item:
            caja.retirar_item(id_item, root)

    def cambiar_password():
        if caja.verificar_password(root):
            caja.establecer_password(root)
        else:
            messagebox.showerror("Error", "Acceso denegado.", parent=root)

    # Configuración de la ventana principal
    root = tk.Tk()
    root.title("Caja Fuerte Digital")
    root.geometry("500x500")
    root.configure(bg="#2C3E50")  # Fondo oscuro

    # Estilo de botones
    button_style = {
        "font": ("Arial", 12, "bold"),
        "bg": "#2980B9",  # Azul
        "fg": "white",    # Texto blanco
        "activebackground": "#3498DB",  # Azul claro al presionar
        "activeforeground": "white",
        "relief": "flat",
        "width": 25,
    }

    # Encabezado
    tk.Label(root, text="Caja Fuerte Digital", font=("Arial", 20, "bold"), bg="#2C3E50", fg="#ECF0F1").pack(pady=20)

    # Botones principales
    tk.Button(root, text="Establecer Contraseña", command=establecer_password, **button_style).pack(pady=10)
    tk.Button(root, text="Guardar Item", command=guardar_item, **button_style).pack(pady=10)
    tk.Button(root, text="Ver Contenido", command=ver_contenido, **button_style).pack(pady=10)
    tk.Button(root, text="Retirar Item", command=retirar_item, **button_style).pack(pady=10)
    tk.Button(root, text="Cambiar Contraseña", command=cambiar_password, **button_style).pack(pady=10)
    tk.Button(root, text="Abrir Block de Notas", command=abrir_block_notas, **button_style).pack(pady=10)
    tk.Button(root, text="Salir", command=lambda: [caja.cerrar_conexion(), root.quit()], **button_style).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
