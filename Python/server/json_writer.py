import json

from scanners.hardware_scanner import get_hardware_info
from scanners.model_scanner import model_identification
from gui import run_gui
#writes the data from all the data


def json_writer(choice, model_info):
    #initialize variables
    data = {}
    hardware_info = get_hardware_info()

    data = {
          "selected_model": model_info,
          "hardware": hardware_info
    }

    with open("results.json", "w") as file:      
            json.dump(data, file, indent=2)
            file.write('\n')
    
