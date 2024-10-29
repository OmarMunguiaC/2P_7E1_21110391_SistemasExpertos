"""
Sistemas Expertos
Profesor: Mauricio Alejandro Cabrera Arellano
Alumno: Omar Josue Munguia Camacho
Registro: 21110391
Grupo: 7E1
"""

import tkinter as tk
from tkinter import messagebox
import json
import os

# Archivo JSON donde se almacenará la base de datos
DATABASE_FILE = "7E1_21110391_P03_BaseDeDatosCNC.json"

class CNCEquipment:
    def __init__(self, name, features):
        self.name = name
        self.features = features

# Función para crear una base de datos inicial
def create_initial_database():
    initial_data = [
            {"name": "Torno CNC", "features": ["rotación", "torneado"]},
            {"name": "Fresadora CNC", "features": ["fijo", "fresado"]},
            {"name": "Fresadora CNC de multiples Ejes", "features": ["fijo", "rotación", "fresado"]},
            {"name": "Cortadora láser CNC", "features": ["corte", "laser", "fijo"]},
            {"name": "Router CNC", "features": ["gravado", "fijo", "laser"]},
            {"name": "Impresora 3D", "features": ["impresión 3D", "fijo"]}
        ]
    with open(DATABASE_FILE, 'w') as f:
        json.dump(initial_data, f, indent=4)

# Cargar base de datos desde el archivo JSON
def load_database():
    if not os.path.exists(DATABASE_FILE):
        # Si no existe el archivo, crearlo con los datos iniciales
        create_initial_database()
    
    try:
        # Intentar cargar la base de datos desde el archivo
        with open(DATABASE_FILE, 'r') as f:
            data = json.load(f)
        return [CNCEquipment(item["name"], item["features"]) for item in data]
    
    except (json.JSONDecodeError, FileNotFoundError):
        # Si hay un error en la lectura (archivo dañado o no encontrado), volver a crear la base de datos
        messagebox.showerror("Error", "Error al cargar la base de datos. Se restaurará a los valores iniciales.")
        create_initial_database()
        with open(DATABASE_FILE, 'r') as f:
            data = json.load(f)
        return [CNCEquipment(item["name"], item["features"]) for item in data]

# Guardar un nuevo equipo en la base de datos
def save_new_equipment(equipment):
    with open(DATABASE_FILE, 'r+') as f:
        data = json.load(f)
        new_entry = {"name": equipment.name, "features": equipment.features}
        data.append(new_entry)
        f.seek(0)
        json.dump(data, f, indent=4)

# Preguntas con las características correspondientes
questions = [
    ("¿El equipo hace girar la pieza?", "rotación"),
    ("¿La pieza se mantiene estatica o en una base?", "fijo"),
    ("¿Es utilizado principalmente para torneado?", "torneado"),
    ("¿Es utilizado principalmente para fresado?", "fresado"),
    ("¿Imprime en 3D?", "impresión 3D"),
    ("¿Utiliza un laser?", "laser"),
    ("¿Realiza corte de materiales?", "corte"),
    ("¿Realiza gravado de materiales?", "gravado"),
]

# Función de encadenamiento hacia adelante
def forward_chaining(database, answers):
    possible_equipment = database[:]
    
    for feature, answer in answers.items():
        if answer == "sí":
            possible_equipment = [eq for eq in possible_equipment if feature in eq.features]
        elif answer == "no":
            possible_equipment = [eq for eq in possible_equipment if feature not in eq.features]
    
    return possible_equipment

# Función para agregar un nuevo equipo a la base de datos
def add_new_equipment(answers):
    new_name = input("Introduce el nombre del nuevo equipo: ")
    new_features = [feature for feature, answer in answers.items() if answer == "sí"]
    new_equipment = CNCEquipment(new_name, new_features)
    save_new_equipment(new_equipment)
    print(f"¡Nuevo equipo '{new_name}' añadido a la base de datos!")

def adivinar_equipo(answers):
    possible_equipment = forward_chaining(database, answers)
    
    if len(possible_equipment) == 1:
        return possible_equipment[0].name
    elif len(possible_equipment) == 0:
        return "No pude adivinar el equipo."
    else:
        return None  # Aún no se puede adivinar

# Interfaz gráfica
class CNCGuessingGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Juego de Adivinanza de CNC")
        self.geometry("400x300")
        self.answers = {}

        self.question_index = 0
        self.create_widgets()

    def create_widgets(self):
        self.start_menu()

    def start_menu(self):
        # Limpiar pantalla
        for widget in self.winfo_children():
            widget.destroy()

        # Título del menú de inicio
        title_label = tk.Label(self, text="Juego de Adivinanza de CNC", font=("Arial", 16))
        title_label.pack(pady=20)

        # Botón Iniciar Juego
        start_button = tk.Button(self, text="Iniciar Juego", command=self.start_game)
        start_button.pack(pady=10)

        # Botón Salir
        quit_button = tk.Button(self, text="Salir", command=self.quit)
        quit_button.pack(pady=10)

    def start_game(self):
        # Limpiar pantalla para empezar el juego
        for widget in self.winfo_children():
            widget.destroy()

        # Etiqueta de pregunta
        self.question_label = tk.Label(self, text=questions[self.question_index][0])
        self.question_label.pack(pady=10)

        # Botones de respuesta
        self.si_button = tk.Button(self, text="Sí", command=lambda: self.answer("sí"))
        self.si_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.no_button = tk.Button(self, text="No", command=lambda: self.answer("no"))
        self.no_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def answer(self, respuesta):
        # Guardar la respuesta
        feature = questions[self.question_index][1]
        self.answers[feature] = respuesta

        # Continuar hasta que se terminen todas las preguntas
        self.question_index += 1
        
        if self.question_index < len(questions):
            self.question_label.config(text=questions[self.question_index][0])
        else:
            # Si se agotaron todas las preguntas, verificar el resultado
            possible_equipment = forward_chaining(database, self.answers)
            if len(possible_equipment) == 1:
                messagebox.showinfo("Resultado", f"¡Creo que el equipo es: {possible_equipment[0].name}!")
            else:
                messagebox.showinfo("Resultado", "No pude adivinar el equipo.")
                if messagebox.askyesno("Añadir equipo", "¿Te gustaría añadir un nuevo equipo?"):
                    add_new_equipment(self.answers)
            self.reset_game()

    def reset_game(self):
        # Limpiar respuestas y volver al menú
        self.answers = {}
        self.question_index = 0
        self.start_menu()

# Cargar la base de datos al iniciar el programa
database = load_database()

# Ejecutar el juego
if __name__ == "__main__":
    app = CNCGuessingGame()
    app.mainloop()
