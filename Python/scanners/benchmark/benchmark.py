
# benchmarker to find data
import time
import requests
import threading
from memory_monitor import monitor_memory

def run_benchmark(choice):
    # first checks if model is loaded in memory 
    response = requests.get("http://localhost:11434/api/ps")
    data = response.json()

    loaded_models = [model["name"] for model in data["models"]]

    if choice in loaded_models:
        return None, "Model is already loaded. Please unload it."
    #==========================================================
    #time how long it takes to load model
    #also make sure it is specifically VRAM not RAM
    requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": choice,
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": False
    }
    )

    data = response.json()
    #add to json to send to json_writer
    load_time = data["load_duration"] / 1_000_000_000

    for model in data["models"]:
        if model["name"] == choice:
            if model["size_vram"] >= model["size"]:
                print("model loaded into vram continuing")
            else:
                return None, "Model is not fully loaded into VRAM. Please reload."
    #==========================================================
    #find ttft innacurate for now 
    start_time = time.perf_counter()

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": choice,
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": True
        },
        stream=True
    )

    for chunk in response.iter_lines():
        if chunk:
            ttft = time.perf_counter() - start_time
            break
    #===========================================================
    #calculate the t/s on first message
    #and start thread tracking for ram usage
    stop_event = threading.Event()
    
    #create thread
    monitor_thread = threading.Thread(
        target=monitor_memory,
        args=(stop_event,)
    )
    
    #start thread 
    monitor_thread.start()


    start_time = time.perf_counter()    
        
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": choice,
            "messages": [{"role": "user", "content": "Can you explain what redshift is"}],
            "stream": False 
        },
    )

    data = response.json()

    eval_count = data.get("eval_count")
    eval_duration = data.get("eval_duration")
    tokens_scalc = eval_count / (eval_duration / 1e9)
    tokens_second = f"{tokens_scalc:.2f} t/s"
    #=============================================================
    #calculate sustained t/s with 10 messages averages, How fast it generates over repeated requests, including potential performance changes as the workload continues.
    total_runs = 10
    tokens_speeds = []
    for i in range(total_runs):
        response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": choice,
                    "messages": [{"role": "user", "content": "explain to me how a microphone works in detail"}],
                    "stream": False
                },
                stream=False
            )
        data = response.json()

        eval_count = data.get("eval_count")
        eval_duration = data.get("eval_duration")
        tokens_scalc = eval_count / (eval_duration / 1e9)
        #append values 
        tokens_speeds.append(tokens_scalc)
    average = sum(tokens_speeds) / len(tokens_speeds)
    sustained_generation_tps_across_runs = f"{average:.2f} t/s"

    #stop thread 
    stop_event.set()
    monitor_thread.join()



