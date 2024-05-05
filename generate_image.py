import requests
from app import prodia_config

current_api_keys_index = []

def generate_request(prompt):
    # loop through the current api keys
    # if the api key is not exhausted, use it
    # if the api key is exhausted, move to the next one
    for i in range(len(current_api_keys_index)):
        key = prodia_config.api_keys[current_api_keys_index[i]]
        generate(prompt, key)





def generate(prompt, key):
    url = prodia_config.model_urls["sd"]

    payload = {
        "model": "Realistic_Vision_V5.0.safetensors [614d1063]",
        "prompt": prompt,
        "negative_prompt": "",
        "steps": 20,
        "cfg_scale": 7,
        "seed": -1,
        "sampler": "DPM++ 2M Karras",
        "width": 512,
        "height": 512
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": key,
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())

def retrieve(jobId):
    jobId = "be8f99eb-8eb6-48cd-92fe-dd6f925e0756"
    #url = "https://api.prodia.com/v1/job/jobId"
    url = "https://api.prodia.com/v1/job/" + jobId

    headers = {
        "accept": "application/json",
        "X-Prodia-Key": "f5097056-59c6-4fb7-b40a-74f9d75ba1cc"
    }

    response = requests.get(url, headers=headers)
    # {"job":"be8f99eb-8eb6-48cd-92fe-dd6f925e0756","status":"succeeded","imageUrl":"https://images.prodia.xyz/be8f99eb-8eb6-48cd-92fe-dd6f925e0756.png"}

    if response and response.json()["status"] == "succeeded":
        print(response.json()["imageUrl"])
    else:
        print("Job not completed yet")

# define main
if __name__ == "__main__":
    #generate(["This dreamlike digital art captures a vibrant, kaleidoscopic bird in a lush rainforest"])
    retrieve()