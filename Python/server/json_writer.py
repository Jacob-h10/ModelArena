import json

from scanners.hardware_scanner import get_hardware_info
#writes the data from all the data


def json_writer():
    #initialize variables
    hardware_info = get_hardware_info()

    with open("results.json", "w") as file:      
            json.dump(hardware_info, file, indent=2)
            file.write('\n')
    
