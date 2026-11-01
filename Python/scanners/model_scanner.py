#scans for AI models on pc 
#Identifies models and returns a list of available ones
#also scans for meta data to get info on AI model
import requests 
import subprocess
import json
from pathlib import Path



def find_ollama():
    #find ollama models
    try:
        #ollama discovery channel
        response = requests.get("http://localhost:11434/api/tags")
        models_list = [model["name"] for model in response.json()["models"]]

        return models_list
    
    except requests.exceptions.ConnectionError:
        return []

    except requests.exceptions.Timeout:
        return []

    except requests.exceptions.HTTPError:
        return []

def find_lm_studio():
    try:
        #lm studio discovery channel
        result = subprocess.run(
            ["lms", "ls", "--json"],
            capture_output=True,
            text=True,
            timeout=15
        )

        models = json.loads(result.stdout)
        
        return models

    
    except FileNotFoundError:
        return []

    except subprocess.TimeoutExpired:
        return []

    except json.JSONDecodeError:
        return []

    
def find_gguf():
    models = []
    try:
        #discovery channel for gguf files
        for file in Path("C:/").rglob("*.gguf"):
            models.append(str(file))
        return models

        

    except PermissionError:
        return []

    except OSError:
        return []