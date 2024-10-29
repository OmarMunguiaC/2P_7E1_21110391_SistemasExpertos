"""
Sistemas Expertos
Profesor: Mauricio Alejandro Cabrera Arellano
Alumno: Omar Josue Munguia Camacho
Registro: 21110391
Grupo: 7E1
"""

import random
import tkinter as tk
from tkinter import messagebox

# Generamos los finales posibles con trasfondo
finales = [
    {
        "arma": "cuchillo",
        "personaje": "sirvienta",
        "lugar": "cocina",
        "narrativa_arma": "El cuchillo se encontró en la cocina con pequeñas manchas de sangre, parece que intentaron limpiarlas torpemente.",
        "narrativa_personaje": "La sirvienta asegura que estaba limpiando en la cocina cuando escuchó un ruido fuerte en la sala.",
        "narrativa_lugar": "La cocina tiene un aire tranquilo, pero parece desordenado."
    },
    {
        "arma": "candelabro",
        "personaje": "chef",
        "lugar": "gran salón",
        "narrativa_arma": "El candelabro fue hallado en el gran salón, la sirvienta afirma que normalmente se encuentra en la sala, parece que alguien lo movió.",
        "narrativa_personaje": "El chef afirma que estaba en la cocina preparando la cena, pero menciona haber visto al pintor en el gran salón poco antes del crimen.",
        "narrativa_lugar": "El gran salón es majestuoso, encuentro candelabro en el suelo rodeado de cera fresca."
    },
    {
        "arma": "pistola",
        "personaje": "pintor",
        "lugar": "jardín",
        "narrativa_arma": "La pistola fue hallada en el jardín, con un cartucho usado. Aún huele a pólvora.",
        "narrativa_personaje": "El pintor dice que estaba acomodando su equipo de pintura en la sala, pero escuchó un disparo proveniente del jardín.",
        "narrativa_lugar": "El jardín está tranquilo, sin embargo encuentro la pistola en unos arbustos."
    },
    {
        "arma": "garrote",
        "personaje": "jardinero",
        "lugar": "sala",
        "narrativa_arma": "El garrote, una herramienta improvisada, fue encontrado en la sala. Las marcas sugieren un uso reciente y violento.",
        "narrativa_personaje": "El jardinero afirma que estaba podando en el jardín, pero recuerda haber visto al chef en la sala poco antes del incidente.",
        "narrativa_lugar": "La sala tiene signos claros de lucha. El garrote encontrado aquí cuenta la historia de una pelea que terminó en tragedia."
    },
    {
        "arma": "vidrio roto",
        "personaje": "dueña de la mansión",
        "lugar": "recámara",
        "narrativa_arma": "Los fragmentos de vidrio roto en la recámara están manchados de sangre, indicando que alguien resultó herido durante el altercado.",
        "narrativa_personaje": "La dueña de la mansión afirma que estaba descansando en su recámara y escuchó un ruido fuerte en el gran salón, parece agitada.",
        "narrativa_lugar": "La recámara es elegante, pero los vidrios rotos y la sangre en el suelo sugieren que aquí ocurrió una confrontación violenta."
    }
]

# Clase principal para el juego
class JuegoClue(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuración inicial de la ventana
        self.title("Juego tipo CLUE")
        self.geometry("600x600")
        self.final = None
        self.preguntas_restantes = 5
        self.acusacion_personaje = None
        self.acusacion_arma = None
        self.acusacion_lugar = None

        # Listas de armas, personajes y lugares para preguntas
        self.armas_restantes = ["cuchillo", "candelabro", "pistola", "garrote", "vidrio roto"]
        self.personajes_restantes = ["sirvienta", "chef", "pintor", "jardinero", "dueña de la mansión"]
        self.lugares_restantes = ["jardín", "cocina", "sala", "gran salón", "recámara"]

        # Mostrar el menú inicial
        self.menu_inicio()

    # Método para crear el menú de inicio
    def menu_inicio(self):
        self.clear_widgets()

        self.label_intro = tk.Label(self, text="¡Bienvenido al juego CLUE!\n", font=("Arial", 20))
        self.label_intro.pack(pady=20)

        self.boton_iniciar = tk.Button(self, text="Iniciar Partida", command=self.iniciar_partida, font=("Arial", 14))
        self.boton_iniciar.pack(pady=10)

        self.boton_salir = tk.Button(self, text="Salir", command=self.quit, font=("Arial", 14))
        self.boton_salir.pack(pady=10)

    # Método para iniciar una nueva partida
    def iniciar_partida(self):
        self.acusacion_arma = 0
        self.acusacion_lugar = 0
        self.acusacion_personaje = 0
        self.final = random.choice(finales)
        self.preguntas_restantes = 5

        # Reiniciar las listas de preguntas disponibles
        self.armas_restantes = ["cuchillo", "candelabro", "pistola", "garrote", "vidrio roto"]
        self.personajes_restantes = ["sirvienta", "chef", "pintor", "jardinero", "dueña de la mansión"]
        self.lugares_restantes = ["jardín", "cocina", "sala", "gran salón", "recámara"]

        self.clear_widgets()

        self.label_preguntas = tk.Label(self, text=f"Te quedan {self.preguntas_restantes} preguntas.")
        self.label_preguntas.pack()

        self.text_area = tk.Text(self, height=10, width=60, state="disabled")
        self.text_area.pack()

        self.label_opciones = tk.Label(self, text="Elige sobre qué quieres preguntar:")
        self.label_opciones.pack()

        self.mostrar_opciones_preguntas()

        # Botón para acusación
        self.boton_acusacion = tk.Button(self, text="Hacer Acusación", command=self.mostrar_menu_acusacion)
        self.boton_acusacion.pack(pady=10)

    # Método para mostrar las opciones de preguntas
    def mostrar_opciones_preguntas(self):
        self.clear_opciones_widgets()

        # Botones de armas
        self.label_armas = tk.Label(self.frame_botones, text="Armas:")
        self.label_armas.grid(row=0, column=0)
        for i, arma in enumerate(self.armas_restantes):
            boton = tk.Button(self.frame_botones, text=arma.capitalize(), command=lambda a=arma: self.hacer_pregunta(a))
            boton.grid(row=1, column=i)

        # Botones de personajes
        self.label_personajes = tk.Label(self.frame_botones, text="Personajes:")
        self.label_personajes.grid(row=2, column=0)
        for i, personaje in enumerate(self.personajes_restantes):
            boton = tk.Button(self.frame_botones, text=personaje.capitalize(), command=lambda p=personaje: self.hacer_pregunta(p))
            boton.grid(row=3, column=i)

        # Botones de lugares
        self.label_lugares = tk.Label(self.frame_botones, text="Lugares:")
        self.label_lugares.grid(row=4, column=0)
        for i, lugar in enumerate(self.lugares_restantes):
            boton = tk.Button(self.frame_botones, text=lugar.capitalize(), command=lambda l=lugar: self.hacer_pregunta(l))
            boton.grid(row=5, column=i)

    # Método para limpiar los widgets de opciones
    def clear_opciones_widgets(self):
        try:
            self.frame_botones.destroy()
        except AttributeError:
            pass

        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack()

    # Método para limpiar la ventana de widgets
    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    # Método para mostrar texto en el área de texto
    def mostrar_texto(self, texto):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, texto + "\n")
        self.text_area.config(state="disabled")

    # Método para hacer preguntas
    def hacer_pregunta(self, pregunta):
        if self.preguntas_restantes > 0:
            self.preguntas_restantes -= 1
            self.label_preguntas.config(text=f"Te quedan {self.preguntas_restantes} preguntas.")

            if pregunta in self.armas_restantes:
                self.armas_restantes.remove(pregunta)
                if pregunta == self.final["arma"]:
                    self.mostrar_texto(f"Inspeccionas el {pregunta}. {self.final['narrativa_arma']}")
                elif pregunta in ["cuchillo", "candelabro", "pistola", "garrote", "vidrio roto"]:
                    self.mostrar_texto(f"Inspeccionas el {pregunta}. {self.get_dialogo_generico(pregunta)}")

            elif pregunta in self.personajes_restantes:
                self.personajes_restantes.remove(pregunta)
                if pregunta == self.final["personaje"]:
                    self.mostrar_texto(f"Hablas con {pregunta}. {self.final['narrativa_personaje']}")
                elif pregunta in ["sirvienta", "chef", "pintor", "jardinero", "dueña de la mansión"]:
                    self.mostrar_texto(f"{pregunta.capitalize()}: {self.get_dialogo_generico(pregunta)}")

            elif pregunta in self.lugares_restantes:
                self.lugares_restantes.remove(pregunta)
                if pregunta == self.final["lugar"]:
                    self.mostrar_texto(f"Inspeccionas el {pregunta}. {self.final['narrativa_lugar']}")
                elif pregunta in ["jardín", "cocina", "sala", "gran salón", "recámara"]:
                    self.mostrar_texto(f"Inspeccionas el {pregunta}. {self.get_dialogo_generico(pregunta)}")

            # Actualizar las opciones después de cada pregunta
            self.mostrar_opciones_preguntas()
        
        if self.preguntas_restantes == 0:
            messagebox.showerror("",f"Ya no te quedan más preguntas.")

    # Método para obtener el diálogo genérico de personajes, armas o lugares
    def get_dialogo_generico(self, elemento):
        generico = {
            "cuchillo": "Un cuchillo común de cocina, bastante desgastado por el uso del chef.",
            "candelabro": "Un candelabro bastante elegante chapado en oro, parece que no le han limpiado la cera caída en algún tiempo.",
            "pistola": "Una pistola antigua adornada y elegante, con signos de haber tenido su mantenimiento no hace mucho.",
            "garrote": "Un garrote de jardín, típico, pero algo desgastado por el duro uso de trabajo.",
            "vidrio roto": "Fragmentos de vidrio que parecen haber pertenecido a un objeto frágil, pero sin signos de sangre.",
            "sirvienta": "La sirvienta se encuentra nerviosa, dice que tiene miedo por lo que le pueda ocurrir.",
            "chef": "El chef afirma que estaba fuera a la hora del crimen, no parece nervioso por lo ocurrido.",
            "pintor": "'Solo estaba pintando, no tengo nada que ver con esto.', responde de manera enojada mientras acomoda sus cosas para irse.",
            "jardinero": "El jardinero tiene las manos malheridas, afirma que estaba cortando los rosales durante lo ocurrido.",
            "dueña de la mansión": "La dueña de la mansión afirma que se tropezó y rompio la ventana de su recamara 'accidentalmente'.",
            "jardín": "Bastante bien arreglado, parece que el jardinero hace bien su trabajo.",
            "cocina": "La cocina luce un poco sucia, pero rebosan platillos en la mesa dignos de un festín.",
            "sala": "La sala luce bastante tranquila, parece que no esperaban visitas recientes.",
            "gran salón": "El gran salón luce majestuoso, las luces adornan bastante bien el lugar, no parece haber signos de pelea aqui.",
            "recámara": "La recamara se encuentra un poco desordenada, la ventana esta rota por algún motivo."
        }
        return generico[elemento]

    # Método para mostrar el menú de acusación con botones
    def mostrar_menu_acusacion(self):
        self.clear_widgets()

        self.label_acusacion = tk.Label(self, text="Haz tu acusación final:")
        self.label_acusacion.pack(pady=10)

        # Seleccionar personaje
        self.label_acusar_personaje = tk.Label(self, text="Selecciona el personaje:")
        self.label_acusar_personaje.pack()
        self.frame_personajes = tk.Frame(self)
        self.frame_personajes.pack()
        for i, personaje in enumerate(["sirvienta", "chef", "pintor", "jardinero", "dueña de la mansión"]):
            boton = tk.Button(self.frame_personajes, text=personaje.capitalize(), command=lambda p=personaje: self.seleccionar_acusacion("personaje", p))
            boton.grid(row=0, column=i)

        # Seleccionar arma
        self.label_acusar_arma = tk.Label(self, text="Selecciona el arma:")
        self.label_acusar_arma.pack()
        self.frame_armas = tk.Frame(self)
        self.frame_armas.pack()
        for i, arma in enumerate(["cuchillo", "candelabro", "pistola", "garrote", "vidrio roto"]):
            boton = tk.Button(self.frame_armas, text=arma.capitalize(), command=lambda a=arma: self.seleccionar_acusacion("arma", a))
            boton.grid(row=0, column=i)

        # Seleccionar lugar
        self.label_acusar_lugar = tk.Label(self, text="Selecciona el lugar:")
        self.label_acusar_lugar.pack()
        self.frame_lugares = tk.Frame(self)
        self.frame_lugares.pack()
        for i, lugar in enumerate(["jardín", "cocina", "sala", "gran salón", "recámara"]):
            boton = tk.Button(self.frame_lugares, text=lugar.capitalize(), command=lambda l=lugar: self.seleccionar_acusacion("lugar", l))
            boton.grid(row=0, column=i)

        # Sección para mostrar las elecciones del jugador
        self.label_selecciones = tk.Label(self, text="Tu elección:")
        self.label_selecciones.pack(pady=10)

        self.label_personaje_seleccionado = tk.Label(self, text="Personaje: Ninguno")
        self.label_personaje_seleccionado.pack()

        self.label_arma_seleccionada = tk.Label(self, text="Arma: Ninguna")
        self.label_arma_seleccionada.pack()

        self.label_lugar_seleccionado = tk.Label(self, text="Lugar: Ninguno")
        self.label_lugar_seleccionado.pack()

        # Botón para confirmar la acusación
        self.boton_confirmar_acusacion = tk.Button(self, text="Confirmar Acusación", command=self.hacer_acusacion)
        self.boton_confirmar_acusacion.pack(pady=10)

    # Método para seleccionar una acusación
    def seleccionar_acusacion(self, tipo, valor):
        if tipo == "personaje":
            self.acusacion_personaje = valor
            self.label_personaje_seleccionado.config(text=f"Personaje: {valor.capitalize()}")
        elif tipo == "arma":
            self.acusacion_arma = valor
            self.label_arma_seleccionada.config(text=f"Arma: {valor.capitalize()}")
        elif tipo == "lugar":
            self.acusacion_lugar = valor
            self.label_lugar_seleccionado.config(text=f"Lugar: {valor.capitalize()}")

    # Método para hacer la acusación final
    def hacer_acusacion(self):
        if self.acusacion_personaje and self.acusacion_arma and self.acusacion_lugar:
            if (self.acusacion_personaje == self.final["personaje"] and
                self.acusacion_arma == self.final["arma"] and
                self.acusacion_lugar == self.final["lugar"]):
                messagebox.showinfo("¡Correcto!", f"¡Has resuelto el misterio! El culpable era {self.final['personaje']}, usando el {self.final['arma']} en el {self.final['lugar']}.")
                # Regresar al menú principal
                self.menu_inicio()
            else:
                messagebox.showinfo("Incorrecto", f"Fallaste. El culpable era {self.final['personaje']}, usando el {self.final['arma']} en el {self.final['lugar']}.")
                # Regresar al menú principal
                self.menu_inicio()
        elif (self.acusacion_personaje == "Ninguno" or
                self.acusacion_arma != "Ninguno" or
                self.acusacion_lugar != "Ninguno"):
            messagebox.showerror("Error", f"Debes elejir un arma, un lugar y un personaje antes de hacer la acusación")

# Inicializa el juego
if __name__ == "__main__":
    app = JuegoClue()
    app.mainloop()

