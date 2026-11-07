#entry-point for program
#recieves submission, validates them, serves requests
from pathlib import Path
from server.json_writer import json_writer
from gui import run_gui
from scanners.model_scanner import model_identification
from scanners.benchmark.benchmark import run_benchmark
# IMPORT: Pull the shared RAM dictionary so you can hand it to the json_writer
from scanners.benchmark.memory_monitor import shared_ram_results

def main():

    while True:

        choice, restart = run_gui()

        if choice is None:
            return

        model_info = model_identification(choice)

        benchmark_results, error = run_benchmark(choice)

        if error:
            print(error)

            choice, restart = run_gui(error)

            if restart:
                results_file = Path(__file__).resolve().parent.parent / "results.json"

                if results_file.exists():
                    results_file.unlink()

                continue

            return

        if model_info is None:
            print("faild to indentify model")
            return

        json_writer(model_info, benchmark_results, shared_ram_results)

        print("results writter")
        return

if __name__ == "__main__":
    main()
