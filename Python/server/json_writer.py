import json

from scanners.benchmark.benchmark import run_benchmark
from scanners.benchmark.memory_monitor import monitor_memory
from scanners.hardware_scanner import get_hardware_info
from scanners.model_scanner import model_identification
from gui import run_gui
#writes the data from all the data


def json_writer(model_info, benchmark_results, ram_usage):
    #initialize variables
    data = {} 
    hardware_info = get_hardware_info()

    data = {
          "selected_model": model_info,
          "hardware": hardware_info,
          "benchmark": benchmark_results,
          "ram usage": ram_usage
    }

    with open("results.json", "w") as file:      
            json.dump(data, file, indent=2)
            file.write('\n')
    
