import time
import psutil
import threading
#Peak, baseline, average memory usage
#also calculates memory increase 
#ram usage
shared_ram_results = {}

def baseline_monitor(stop_event):
    #monitors baseline ram usage before message sends 
    current_ram = 0
    baseline_ticks = []
    
    
        
    
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
                    
        baseline_ticks.append(current_ram)

        time.sleep(.5)

    baseline_ram_usage = sum(baseline_ticks) / len(baseline_ticks)

    shared_ram_results["baseline ram usage"] = baseline_ram_usage


#==========================================================================================================

def monitor_memory(stop_event):
    #montiors peak and average ram usage
    peak_ram = 0
    current_ram = 0
    ram_times = []


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

        baseline_ram = peak_ram

        ram_times.append(current_ram)
        time.sleep(0.5)

    #find the average
    average_ram = sum(ram_times) / len(ram_times)

    shared_ram_results["average ram usage"] = average_ram
    shared_ram_results["peak ram usage"] = peak_ram


    return shared_ram_results
