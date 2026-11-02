#entry-point for program
#recieves submission, validates them, serves requests
from server.json_writer import json_writer
from gui import run_gui
from scanners.model_scanner import model_identification

def main():
    
    choice = run_gui()
    if choice is None:
        return
    
    model_info = model_identification(choice)

    if model_info is None:
        print("faild to indentify model")
        return
    
    json_writer(choice, model_info)

    print("results writter")

if __name__ == "__main__":
    main()