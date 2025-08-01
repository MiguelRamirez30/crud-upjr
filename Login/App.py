import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class RegistroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema CRUD - UPJR")

        self.conectar_db()
        self.crear_tabla()
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
            )
        ''')
        self.conn.commit()

    def crear_interfaz(self):
        # Etiquetas y entradas
        tk.Label(self.root, text="Nombre").grid(row=0, column=0)
        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(self.root, text="Edad").grid(row=1, column=0)
        self.entry_edad = tk.Entry(self.root)
        self.entry_edad.grid(row=1, column=1)

        # Botones
        tk.Button(self.root, text="Agregar", command=self.agregar).grid(row=2, column=0)
        tk.Button(self.root, text="Actualizar", command=self.actualizar).grid(row=2, column=1)
        tk.Button(self.root, text="Eliminar", command=self.eliminar).grid(row=2, column=2)

        # Tabla (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Edad"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Edad", text="Edad")
        self.tree.grid(row=3, column=0, columnspan=3, pady=10)

    def agregar(self):
        nombre = self.entry_nombre.get()
        edad = self.entry_edad.get()
        if nombre and edad:
            self.cursor.execute('INSERT INTO registros (nombre, edad) VALUES (?, ?)', (nombre, edad))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Registro agregado")
            self.limpiar()
            self.mostrar_registros()
        else:
            messagebox.showwarning("Advertencia", "Complete todos los campos")

    def actualizar(self):
        selected = self.tree.selection()
        if selected:
            id_registro = self.tree.item(selected)['values'][0]
            nombre = self.entry_nombre.get()
            edad = self.entry_edad.get()
            if nombre and edad:
                self.cursor.execute('UPDATE registros SET nombre=?, edad=? WHERE id=?', (nombre, edad, id_registro))
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

    def cerrar(self):
        self.conn.close()

# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroApp(root)
    root.mainloop()
    app.cerrar()
