import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError as e:
            print(f"Error opening image: {image_path}, Error: {e}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

async def generate_image(prompt: str):
    tasks = []
    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, High resolution",
            "seed": str(randint(0, 1000000)),
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    folder_path = "Data"
    os.makedirs(folder_path, exist_ok=True)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:  # Check if image_bytes is not None (error occurred)
            file_path = os.path.join(folder_path, f"{prompt.replace(' ', '_')}{i+1}.jpg")
            with open(file_path, "wb") as f:
                f.write(image_bytes)

def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt))
    open_images(prompt)

while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data = f.read().strip()
        prompt, Status = Data.split(",")
        if Status.strip() == "True":
            print("Generating Images...")
            GenerateImages(prompt=prompt)
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break
        else:
            sleep(1)
    except FileNotFoundError:
        print("Error: ImageGeneration.data file not found.")
        sleep(1)
    except ValueError:
        print("Error: Invalid data format in ImageGeneration.data.")
        sleep(1)
    except KeyError as e:
        print(f"Error: Environment variable {e} not found")
        sleep(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sleep(1)