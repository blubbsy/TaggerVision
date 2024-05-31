import base64
import glob
import os
from io import BytesIO
from pathlib import Path
from PIL import Image
#from iptcinfo3 import IPTCInfo
from langchain_community.llms import Ollama
import exiftool
import json
import datetime
from tqdm import tqdm

# Constants for directories and prompts
OLLAMA_BASE_URL = "http://127.0.0.1:11434"
SOURCE_DIR = "C:/Users/Sibby/Downloads/Image_KeywordTagging/examples"
TARGET_DIR = "C:/Users/Sibby/Downloads/Image_KeywordTagging/examples"
SOURCE_DIR = "Z:/Photos/"
TARGET_DIR = "Z:/Photos/"

PROMPT_KEYWORDS = "Please provide a minimum of 10 precise keywords separated by commas."
PROMPT_DESCRIPTION = "Please provide a description of what is on the photo. Avoid repetitive sentences and words."
PROMPT_TITLE = "Please give the photo an artistic title. Avoid naming locations or people."

FILE_EXTENSIONS = ['*.jpeg', '*.jpg', '*.png']

# Custom EXIF tag for marking processed images
CUSTOM_EXIF_TAG = "-Custom:ProcessedByTaggerVision"
VERSION_SCRIPT = "v1.0"  # Change this to the actual version of the script
FORCE_REPROCESS = False

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
    #llava_model = Ollama(model="llava:v1.6", base_url=OLLAMA_BASE_URL, temperature=0)
    #llava_model = Ollama(model="llava-llama3", base_url=OLLAMA_BASE_URL, temperature=0)
    llava_model = Ollama(model="llava-phi3", base_url=OLLAMA_BASE_URL, temperature=0)
    
    try:
        # Read the image
        print(f"Processing image '{image_path}'...")
        #info = IPTCInfo(image_path, force=True, inp_charset='utf8')
        pil_image = Image.open(image_path)

        # Resize the image to a width of 672 pixels
        base_width = 672
        wpercent = (base_width / float(pil_image.size[0]))
        hsize = int((float(pil_image.size[1]) * float(wpercent)))
        pil_image = pil_image.resize((base_width, hsize), Image.LANCZOS)

        # Convert image to base64 and pass it to the model along with the prompt
        image_b64 = convert_to_base64(pil_image)
        llm_with_image_context = llava_model.bind(images=[image_b64])
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
                
            # Write the custom EXIF tag to mark the image as processed
            now = datetime.datetime.now()
 
            custom_tag_value = now.strftime("%Y-%m-%d") + "_" + VERSION_SCRIPT
            with exiftool.ExifTool() as et:
                et.execute(f"{CUSTOM_EXIF_TAG}={custom_tag_value}", str(xmp_path))

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
        return True
    
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
        process_image(filepath, PROMPT_KEYWORDS)
        process_image(filepath, PROMPT_DESCRIPTION)