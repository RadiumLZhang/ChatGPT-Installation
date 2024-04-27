# @title Install requirements
from io import BytesIO
import IPython
import json
import os
from PIL import Image
import requests
import time


import json

# Load the config.json file
with open('config.json') as f:
    config = json.load(f)

# Get the host URL and STABILITY_KEY from the config

STABILITY_KEY = config['sdxl']['stability_key']

def send_generation_request(host,params,):

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    # Encode parameters


    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.request(
        "POST",
        host,
        headers=headers,
        files={"none": ''},
        data=params
    )


    # Check for errors
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response


def send_async_generation_request(host, params,):
    headers = {

        "Accept": "application/json",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    # Encode parameters
    files = {}
    if "init_image" in params:
        init_image = params.pop("init_image")
        files = {"image": open(init_image, 'rb')}

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    # Process async response
    response_dict = json.loads(response.text)
    generation_id = response_dict.get("id", None)
    assert generation_id is not None, "Expected id in response"

    # Loop until result or timeout
    timeout = int(os.getenv("WORKER_TIMEOUT", 500))
    start = time.time()
    status_code = 202
    while status_code == 202:
        response = requests.get(
            f"{host}/result/{generation_id}",
            headers={
                **headers,
                "Accept": "image/*"
            },
        )

        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        status_code = response.status_code
        time.sleep(10)
        if time.time() - start > timeout:
            raise Exception(f"Timeout after {timeout} seconds")

    return response


def generate(prompt):

    host = config['sdxl']['host']
    model = config['sdxl']['model']
    aspect_ratio = config['sdxl']['aspect_ratio']
    seed = config['sdxl']['seed']
    negative_prompt = config['sdxl']['negative_prompt']
    output_format = config['sdxl']['output_format']
    style_preset = config['sdxl']['style_preset']
    # params = {
    #     "prompt": prompt,
    #     "negative_prompt": negative_prompt if model == "sd3" else "",
    #
    #     "aspect_ratio": aspect_ratio,
    #     "seed": seed,
    #     "output_format": output_format,
    #     "model": model,
    #     "mode": "text-to-image",
    #     "style_preset": style_preset
    # }

    params = json.dumps({
        "key":  "",
        "model_id":  "anything-v5",
        "prompt":  "actual 8K portrait photo of gareth person, portrait, happy colors, bright eyes, clear eyes, warm smile, smooth soft skin, big dreamy eyes, beautiful intricate colored hair, symmetrical, anime wide eyes, soft lighting, detailed face, by makoto shinkai, stanley artgerm lau, wlop, rossdraws, concept art, digital painting, looking into camera",
        "negative_prompt":  "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",
        "width":  "512",
        "height":  "512",
        "samples":  "1",
        "num_inference_steps":  "30",
        "safety_checker":  "no",
        "enhance_prompt":  "yes",
        "seed":  None,
        "guidance_scale":  7.5,
        "multi_lingual":  "no",
        "panorama":  "no",
        "self_attention":  "no",
        "upscale":  "no",
        "embeddings":  "embeddings_model_id",
        "lora":  "lora_model_id",
        "webhook":  None,
        "track_id":  None
    })

    response = send_generation_request(
        host,
        params
    )

    # Decode response
    output_image = response.content
    finish_reason = response.headers.get("finish-reason")
    seed = response.headers.get("seed")

    # Check for NSFW classification
    if finish_reason == 'CONTENT_FILTERED':
        raise Warning("Generation failed NSFW classifier")

    # Save and display result
    generated = f"generated_{seed}.{output_format}"
    with open(generated, "wb") as f:
        f.write(output_image)
    print(f"Saved image {generated}")



# define main
if __name__ == "__main__":
    generate(["This dreamlike digital art captures a vibrant, kaleidoscopic bird in a lush rainforest"])
