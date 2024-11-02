import base64
import glob
import os
from io import BytesIO
from pathlib import Path
from PIL import Image
from langchain_community.llms import Ollama
import exiftool
import json
import datetime
from tqdm import tqdm

# Constants for directories and prompts
OLLAMA_URL = "http://127.0.0.1:11434"
#SOURCE_DIR = "Z:/Photos/"
#TARGET_DIR = "Z:/Photos/"
SOURCE_DIR = "C:/Users/Sibby/Downloads/Image_KeywordTagging/examples"
TARGET_DIR = "C:/Users/Sibby/Downloads/Image_KeywordTagging/examples"

PROMPT_TITLE = "Give the photo a title. Avoid naming locations or people."
PROMPT_DESCRIPTION = "Provide a description of what is on the photo. Avoid repetitive sentences and words."
PROMPT_KEYWORDS = "Provide a minimum of 10 precise keywords separated by commas."

FILE_EXTENSIONS = ['*.jpeg', '*.jpg', '*.png']

FORCE_REPROCESS = True

# Function to convert PIL image to base64 string
def convert_to_base64(pil_image):
    buffered = BytesIO()
    rgb_im = pil_image.convert('RGB')
    rgb_im.save(buffered, format="JPEG") 
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Function to process image with LLama model
def process_image(image_path, prompt):
    # Connect to LLama 1.6
    #mymodel = Ollama(model="llava:v1.6", base_url=OLLAMA_URL, temperature=0)
    #mymodel = Ollama(model="llava-llama3", base_url=OLLAMA_URL, temperature=0)
    mymodel = Ollama(model="x/llama3.2-vision", base_url=OLLAMA_URL, temperature=0)
    #mymodel = Ollama(model="llava-phi3", base_url=OLLAMA_URL, temperature=0)
    
    try:
        # Read the image
        print(f"Processing image '{image_path}'...")
        pil_image = Image.open(image_path)

        # Resize the image to a width of 672 pixels
        base_width = 672
        wpercent = (base_width / float(pil_image.size[0]))
        hsize = int((float(pil_image.size[1]) * float(wpercent)))
        pil_image = pil_image.resize((base_width, hsize), Image.LANCZOS)

        # Convert image to base64 and pass it to the model along with the prompt
        image_b64 = convert_to_base64(pil_image)
        llm_with_image_context = mymodel.bind(images=[image_b64])
        response = llm_with_image_context.invoke(prompt)

        # Print LLama:v1.6 response
        print(response)
        
        # Check if XMP sidecar file exists
        xmp_path = Path(image_path).with_suffix('.xmp')
        if os.path.exists(xmp_path):
            # Update XMP metadata based on prompt type
            if prompt == PROMPT_KEYWORDS:
                tag = "-XMP:Subject"
            elif prompt == PROMPT_DESCRIPTION:
                tag = "-XMP:Description"
            elif prompt == PROMPT_TITLE:
                tag = "-XMP:Title"
            with exiftool.ExifTool() as et:
                et.execute(f"{tag}={response}", str(xmp_path))
                
        else:
            print(f"XMP sidecar file not found for {image_path}. Skipping.")
            
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

def is_image_processed(image_path):
    # Generate the path to the XMP sidecar file
    xmp_path = Path(image_path).with_suffix('.xmp')
    
    # Check if the XMP sidecar file exists
    if not xmp_path.exists():
        print(f"XMP sidecar file '{xmp_path}' not found.")
        return False
    
    # Check if the custom EXIF tag exists in the XMP sidecar file
    with exiftool.ExifToolHelper() as et:
        # Get the tags from the XMP sidecar file
        lst_tags = ["XMP:Subject", "XMP:Description", "XMP:Title"]
        tags = et.get_tags([str(xmp_path)], tags=lst_tags)

        # Get the first (and presumably only) file's tag data
        tag_data = tags[0] if tags else {}
        
        # Check if any of the specified fields are empty
        for tag in lst_tags:
            value = tag_data.get(tag)
            if not value or not str(value).strip():
                print(f"The field '{tag}' is empty.")
                return False  # Return False if any field is empt

        # Return True if all fields have content and not already processed
        print(f"Already processed: '{image_path}'")
        return True

if __name__ == "__main__":
    # Collect all files to be processed
    all_files = []
    print("Collecting file list...")
    for ext in FILE_EXTENSIONS:
        all_files.extend(glob.glob(SOURCE_DIR + '/**/' + ext, recursive=True))
        
    # Iterate through files with a progress bar
    for filepath in tqdm(all_files, desc="Processing images"):
        # Skip processing if the image is already tagged
        if not FORCE_REPROCESS:
            if is_image_processed(filepath):
                continue

        process_image(filepath, PROMPT_TITLE)
        process_image(filepath, PROMPT_DESCRIPTION)
        process_image(filepath, PROMPT_KEYWORDS)
    
    print("Finished. Yay!")