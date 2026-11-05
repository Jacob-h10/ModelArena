#scans for AI models on pc 
#Identifies models and returns a list of available ones
#also scans for meta data to get info on AI model
import requests 
import subprocess
import json
from pathlib import Path
from gguf import GGUFReader

def model_identification(choice):
    print(f"Starting identification for: {choice}")

    def ollama_id():
        print("Trying Ollama...")
        # try to find data on model if ollama
        try:
            response = requests.post(
                "http://localhost:11434/api/show",
                json={"model": choice},
                timeout=10
            )

            data = response.json()
    
            model_info = {
                "model": choice,
                "architecture": data.get("model_info", {}).get("general.architecture", "unknown"),
                "parameter": data.get("details", {}).get("parameter_size", "unknown"),
                "quantization": data.get("details", {}).get("quantization_level", "unknown"),
                "context_length": next(
                    (value for key, value in data.get("model_info", {}).items() if key.endswith(".context_length")),
                    "unknown"
                ),
                "kv_heads": next(
                    (value for key, value in data.get("model_info", {}).items() if key.endswith(".attention.head_count_kv")),
                    "unknown"
                ),
                "model license": data.get("license", "unknown")
            }
            print("Ollama identification successful!")
            return model_info

        except requests.exceptions.ConnectionError:
            print("Ollama connection failed.")
            return None

    def lm_studio_id():
        print("Trying LM Studio...")
        # try to find data on model if lm studio
        try:
            response = requests.get(
                f"http://localhost:1234/api/v0/models/{choice}",
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            model_info = {
                "model": data["id"],
                "architecture": data.get("arch"),
                "parameter": None,
                "quantization": data.get("quantization"),
                "model configuration": data,
                "model license": None
            }
            print("LM Studio identification successful!")
            return model_info

        except requests.exceptions.ConnectionError:
            print("LM Studio connection failed.")
            return None

    def gguf_id():
        print("Trying GGUF...")
        try:
            reader = GGUFReader(choice)

            # Access metadata
            metadata = reader.fields

            model_info = {
                "model": choice,
                "architecture": None,
                "parameter": None,
                "quantization": None,
                "model configuration": {},
                "model license": None
            }

            # Extract metadata values
            for key, field in metadata.items():
                value = field.parts[field.data[0]]
                model_info["model configuration"][key] = value

            print("GGUF identification successful!")
            return model_info

        except (OSError, ValueError):
            print("GGUF identification failed.")
            return None

    print("Running Ollama identification...")
    result = ollama_id()

    if result is None:
        print("Ollama unsuccessful. Moving to LM Studio...")
        result = lm_studio_id()

    if result is None:
        print("LM Studio unsuccessful. Moving to GGUF...")
        result = gguf_id()

    print(f"Final identification result: {result}")
    return result



def find_ollama():
    #find ollama models
    try:
        #ollama discovery channel
        response = requests.get("http://localhost:11434/api/tags")
        models = [model["name"] for model in response.json()["models"]]

        return models
    
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