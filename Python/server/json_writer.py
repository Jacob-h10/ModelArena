import json
from scanners.hardware_scanner import get_hardware_info

# Writes the data from all the data
def json_writer(model_info, benchmark_results, shared_ram_results):
    hardware_info = get_hardware_info()

    data = {
          "selected_model": model_info,
          "hardware": hardware_info,
          "benchmark": benchmark_results,
          "ram usage": shared_ram_results
    }

    with open("results.json", "w") as file:      
            json.dump(data, file, indent=2)
            file.write('\n')
