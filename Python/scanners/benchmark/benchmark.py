
# benchmarker to find data
import time
import requests


def run_benchmark(choice):
    # first checks if model is loaded in memory 
    response = requests.get("http://localhost:11434/api/ps")
    data = response.json()

    loaded_models = [model["name"] for model in data["models"]]

    if choice in loaded_models:
        print("Models are loaded! Please unload the model and restart.")
    else:
        print("No models currently loaded.")

    #time how long it takes to load model
    #==========================================================
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
    #calculate sustained t/s

