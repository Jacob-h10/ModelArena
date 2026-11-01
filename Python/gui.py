#UI for EXE
import customtkinter as ctk
from scanners.model_scanner import find_ollama
from scanners.model_scanner import find_gguf
from scanners.model_scanner import find_lm_studio


#appearence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#create window
app = ctk.CTk()
app.title("ModelArena Benchmarks")
app.geometry("600x400")

#grab models
models = find_ollama(), find_lm_studio(), find_gguf()
all_models = models[0] + models[1] + models[2]

#title
title = ctk.CTkLabel(
    app,
    text = "ModelArena Benchmarks",
    font = ("Arial", 24, "bold")
)
title.pack(pady=30)

#dropdown selection
def selected_choice(choice):
    print(f"selected model:{choice}")

model_dropdown = ctk.CTkOptionMenu(
    app,
    values=all_models,
    command = selected_choice
)
model_dropdown.pack(pady=30)

app.mainloop()