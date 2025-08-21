import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# --- Pantalla de Registro ---
class RegistroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema CRUD - UPJR")
        self.root.geometry("1600x1500")

        # Configurar estilo para Treeview con fondo azul claro
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#ADD8E6",  # Azul claro
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#ADD8E6")  # Fondo celeste para filas

        style.map('Treeview', background=[('selected', '#3399FF')])  # Color al seleccionar (más azul)

        self.conectar_db()
        self.crear_tabla()
        self.verificar_columnas()  # <-- Verifica y añade columnas si faltan
        self.crear_interfaz()
        self.mostrar_registros()

    def conectar_db(self):
        self.conn = sqlite3.connect('registro.db')
        self.cursor = self.conn.cursor()

    def crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL
                -- columnas carrera y matricula las agregamos después si faltan
            )
        ''')
        self.conn.commit()

    def verificar_columnas(self):
        self.cursor.execute("PRAGMA table_info(registros)")
        columnas = [col[1] for col in self.cursor.fetchall()]

        if 'carrera' not in columnas:
            self.cursor.execute("ALTER TABLE registros ADD COLUMN carrera TEXT DEFAULT ''")
        if 'matricula' not in columnas:
            self.cursor.execute("ALTER TABLE registros ADD COLUMN matricula TEXT DEFAULT ''")

        self.conn.commit()

    def crear_interfaz(self):
        # Etiquetas y entradas
        tk.Label(self.root, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
        self.entry_nombre = tk.Entry(self.root, width=30)
        self.entry_nombre.grid(row=0, column=1, pady=5)

        tk.Label(self.root, text="Edad").grid(row=1, column=0, padx=10, pady=5)
        self.entry_edad = tk.Entry(self.root, width=30)
        self.entry_edad.grid(row=1, column=1, pady=5)

        tk.Label(self.root, text="Carrera").grid(row=2, column=0, padx=10, pady=5)
        self.entry_carrera = tk.Entry(self.root, width=30)
        self.entry_carrera.grid(row=2, column=1, pady=5)

        tk.Label(self.root, text="Matrícula").grid(row=3, column=0, padx=10, pady=5)
        self.entry_matricula = tk.Entry(self.root, width=30)
        self.entry_matricula.grid(row=3, column=1, pady=5)

        # Botones (blancos por defecto)
        tk.Button(self.root, text="Agregar", command=self.agregar).grid(row=4, column=0, pady=10)
        tk.Button(self.root, text="Actualizar", command=self.actualizar).grid(row=4, column=1, pady=10)
        tk.Button(self.root, text="Eliminar", command=self.eliminar).grid(row=4, column=2, pady=10)

        # Tabla con fondo azul claro
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Edad", "Carrera", "Matricula"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Carrera", text="Carrera")
        self.tree.heading("Matricula", text="Matrícula")
        self.tree.column("ID", width=40, anchor='center')
        self.tree.column("Nombre", width=150, anchor='w')
        self.tree.column("Edad", width=50, anchor='center')
        self.tree.column("Carrera", width=150, anchor='w')
        self.tree.column("Matricula", width=100, anchor='center')
        self.tree.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Vincular evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_registro)

    def agregar(self):
        nombre = self.entry_nombre.get()
        edad = self.entry_edad.get()
        carrera = self.entry_carrera.get()
        matricula = self.entry_matricula.get()

        if nombre and edad and carrera and matricula:
            try:
                self.cursor.execute(
                    'INSERT INTO registros (nombre, edad, carrera, matricula) VALUES (?, ?, ?, ?)',
                    (nombre, edad, carrera, matricula)
                )
                self.conn.commit()
                messagebox.showinfo("Éxito", "Registro agregado")
                self.limpiar()
                self.mostrar_registros()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el registro: {e}")
        else:
            messagebox.showwarning("Advertencia", "Complete todos los campos")

    def actualizar(self):
        selected = self.tree.selection()
        if selected:
            id_registro = self.tree.item(selected)['values'][0]
            nombre = self.entry_nombre.get()
            edad = self.entry_edad.get()
            carrera = self.entry_carrera.get()
            matricula = self.entry_matricula.get()
            if nombre and edad and carrera and matricula:
                self.cursor.execute('''
                    UPDATE registros SET nombre=?, edad=?, carrera=?, matricula=? WHERE id=?
                ''', (nombre, edad, carrera, matricula, id_registro))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Registro actualizado")
                self.limpiar()
                self.mostrar_registros()
            else:
                messagebox.showwarning("Advertencia", "Complete todos los campos")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un registro")

    def eliminar(self):
        selected = self.tree.selection()
        if selected:
            id_registro = self.tree.item(selected)['values'][0]
            self.cursor.execute('DELETE FROM registros WHERE id=?', (id_registro,))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Registro eliminado")
            self.mostrar_registros()
            self.limpiar()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un registro")

    def mostrar_registros(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute('SELECT * FROM registros')
        for registro in self.cursor.fetchall():
            self.tree.insert('', 'end', values=registro)

    def limpiar(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
        self.entry_carrera.delete(0, tk.END)
        self.entry_matricula.delete(0, tk.END)

    def seleccionar_registro(self, event):
        selected = self.tree.selection()
        if selected:
            valores = self.tree.item(selected)['values']
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[1])
            self.entry_edad.delete(0, tk.END)
            self.entry_edad.insert(0, valores[2])
            self.entry_carrera.delete(0, tk.END)
            self.entry_carrera.insert(0, valores[3])
            self.entry_matricula.delete(0, tk.END)
            self.entry_matricula.insert(0, valores[4])

    def cerrar(self):
        self.conn.close()

# --- Pantalla de Login ---
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("900x800")
        self.root.configure(bg="#ADD8E6")  # Fondo azul claro

        # Frame para centrar los widgets
        frame = tk.Frame(root, bg="#ADD8E6")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Usuario", bg="#ADD8E6").pack(pady=5)
        self.entry_usuario = tk.Entry(frame)
        self.entry_usuario.pack(pady=5)

        tk.Label(frame, text="Contraseña", bg="#ADD8E6").pack(pady=5)
        self.entry_contrasena = tk.Entry(frame, show="*")
        self.entry_contrasena.pack(pady=5)

        self.btn_login = tk.Button(frame, text="Iniciar sesión", command=self.verificar_login)  # Sin color personalizado
        self.btn_login.pack(pady=20)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if usuario == "Miguel" and contrasena == "12345678":
            self.root.destroy()
            root_registro = tk.Tk()
            app = RegistroApp(root_registro)
            root_registro.mainloop()
            app.cerrar()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")

# --- Ejecutar App ---
if __name__ == "__main__":
    root_login = tk.Tk()
    login_app = LoginApp(root_login)
    root_login.mainloop()
