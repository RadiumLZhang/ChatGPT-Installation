import requests
import io
from PIL import Image
import argparse
import os
import sys
import random

API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-3.5-large"
headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxx"}

def generate_image(prompt, seed=None, guidance_scale=None, negative_prompt=None, num_inference_steps=None, width=None, height=None, scheduler=None):
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)

        # Debugging: Check response content
        print("Response status:", response.status_code)
        print("Response headers:", response.headers)
        print("Response content:", response.content[:500])  # Print first 500 bytes

        if response.status_code != 200:
            raise ValueError(f"Error from API: {response.status_code}, {response.text}")

        return response.content

    payload = {"inputs": prompt}
    if seed is not None:
        payload["seed"] = seed
    if guidance_scale is not None:
        payload["guidance_scale"] = guidance_scale
    if negative_prompt is not None:
        payload["negative_prompt"] = negative_prompt
    if num_inference_steps is not None:
        payload["num_inference_steps"] = num_inference_steps
    if width is not None:
        payload["width"] = width
    if height is not None:
        payload["height"] = height
    if scheduler is not None:
        payload["scheduler"] = scheduler

    image_bytes = query(payload)
    image = Image.open(io.BytesIO(image_bytes))
    return image

def save_image(image, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path)
    print(f"Image saved to {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and save an image based on a prompt.")
    parser.add_argument("prompt", type=str, help="The prompt to generate the image.")
    parser.add_argument("path", type=str, help="The path to save the generated image.")
    parser.add_argument("--seed", type=int, help="Seed for the random number generator.", default=None)
    parser.add_argument("--guidance_scale", type=float, help="Guidance scale for image generation.", default=None)
    parser.add_argument("--negative_prompt", type=str, help="Prompt to guide what NOT to include in image generation.", default=None)
    parser.add_argument("--num_inference_steps", type=int, help="Number of denoising steps.", default=None)
    parser.add_argument("--width", type=int, help="Width of the output image in pixels.", default=None)
    parser.add_argument("--height", type=int, help="Height of the output image in pixels.", default=None)
    parser.add_argument("--scheduler", type=str, help="Override the scheduler with a compatible one.", default=None)
    args = parser.parse_args()

    image = generate_image(args.prompt, args.seed, args.guidance_scale, args.negative_prompt, args.num_inference_steps, args.width, args.height, args.scheduler)
    save_image(image, args.path)
    sys.exit(0)

