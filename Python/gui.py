
#UI for EXE
import customtkinter as ctk
from scanners.model_scanner import find_ollama
from scanners.model_scanner import find_gguf
from scanners.model_scanner import find_lm_studio
from concurrent.futures import ThreadPoolExecutor

def run_gui(error=None):
    choice = None
    restart = False

    #appearence
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    #create window
    app = ctk.CTk()
    app.title("ModelArena Benchmarks")
    app.geometry("600x400")

    #title
    title = ctk.CTkLabel(
        app,
        text = "ModelArena Benchmarks",
        font = ("Arial", 24, "bold")
    )
    title.pack(pady=30)

    if error:
        error_label = ctk.CTkLabel(
            app,
            text=error
        )
        error_label.pack(pady=20)

        #restart button
        def restart_benchmark():
            nonlocal restart
            restart = True
            app.destroy()

        restart_button = ctk.CTkButton(
            app,
            text="Restart Benchmark",
            command=restart_benchmark,
        )
        restart_button.pack(pady=20)

    else:
        #grab models
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(find_ollama),
                executor.submit(find_lm_studio),
                executor.submit(find_gguf)
            ]

            models = [future.result() for future in futures]
        all_models = models[0] + models[1] + models[2]

        #dropdown selection
        def selected_choice(choice):
            print(f"selected model:{choice}")

        model_dropdown = ctk.CTkOptionMenu(
            app,
            values=all_models,
            command=selected_choice
        )
        model_dropdown.pack(pady=30)

        def confirm_choice():
            nonlocal choice
            choice = model_dropdown.get()
            print(f"Confirmed model: {choice}")
            app.destroy()

        confirm_button = ctk.CTkButton(
            app,
            text="Confirm Model",
            command=confirm_choice
        )
        confirm_button.pack(pady=20)

    app.mainloop()
    return choice, restart
