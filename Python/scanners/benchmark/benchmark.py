
# benchmarker to find data
import time
import requests
import threading
from memory_monitor import monitor_memory
from memory_monitor import baseline_monitor

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

    for model in data["models"]:
        if model["name"] == choice:
            if model["size_vram"] >= model["size"]:
                print("model loaded into vram continuing")
            else:
                return None, "Model is not fully loaded into VRAM. Please reload."
    #==========================================================
    #find ttl 
    start_time = time.perf_counter()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": choice,
            "prompt": "",
            "keep_alive": -1
        },
    )
    ttl = time.perf_counter() - start_time

    #===========================================================
    #find baseline then ttft
    stop_event = threading.Event()

    baseline = threading.Thread(
        target=baseline_monitor,
        args=(stop_event,)
    )
    #start thread
    baseline.start()
    #measure baseline 
    #peak will be the baseline
    time.sleep(10)
    stop_event.set()
    baseline.join()

    start_time = time.perf_counter()

    response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": choice,
                "messages": [{"role": "user", "content": "Hello"}],
                "stream": True
            },
        )
    
    for chunk in response.iter_lines():
        if chunk:
            ttft = time.perf_counter() - start_time
            break
    
    #===========================================================
    #calculate the t/s on first message
    #and start thread tracking for ram usage
    
    
    #create thread
    peak_average = threading.Thread(
        target=monitor_memory,
        args=(stop_event,)
    )
    
    #start thread 
    peak_average.start()


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
    average_generation_tps_across_runs = f"{average:.2f} t/s"

    #stop thread 
    stop_event.set()
    peak_average.join()

    #=============================================================
    #return data
    benchmark_results = {
        "time to first token": str(ttft),
        "tokens per second": str(tokens_second), 
        "average tokens per second": str(average_generation_tps_across_runs), 
                         }
    return benchmark_results



