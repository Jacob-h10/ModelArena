import time
import psutil
import threading
#Peak and baseline memory usage
#=============================================================
#vram usage while sustained t/s runs 
#=============================================================
#ram usage

def monitor_memory(stop_event):
    
    peak_ram = 0
    peak_vram = 0
    current_ram = 0
    baseline_vram = 0
    ram_times = []
    vram_times = []

    

    while stop_event.is_set() is False:
        #diffentiate ram usage
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] and process.info['name'].lower() == 'ollama.exe':
        
                parent = process.info['pid']
                children = process.children(recursive=True)
        
                child_pids = [child.pid for child in children]
                pids = [parent] + child_pids
        
                current_ram = 0
        
                for pid in pids:
                        current_ram += psutil.Process(pid).memory_info().rss / (1024 ** 2)
                        continue
                    
        #make new peak
        if current_ram > peak_ram:
            peak_ram = current_ram

        ram_times.append(current_ram)
        time.sleep(0.5)

    #find the baseline
    average_ram = sum(ram_times) / len(ram_times)

    return average_ram, peak_ram