# Image Tagging Script

This script automates the process of tagging images with keywords, description, and title using AI models and updating their metadata accordingly.

## Usage

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/your_username/image-tagging-script.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the necessary configuration in the script (e.g., LLama model URL, source directory, target directory, prompts). See below.

4. Run the script:

    ```bash
    python image_tagging_script.py
    ```

5. The script will process each image in the specified source directory, generate tags using AI models, and update the metadata of the images with the generated tags.

## Configuration
### Configuration Parameters:

- **OLLAMA_BASE_URL**: The base URL of the LLama model used for generating tags. This should be the URL where the LLama model is hosted.

- **SOURCE_DIR**: The directory where the source images are located. This is the directory from which the script will read images for processing.

- **TARGET_DIR**: The directory where the processed images will be saved. This is the directory where the script will save the images after updating their metadata.

### Prompt Parameters:

- **PROMPT_KEYWORDS**: The prompt used to request keywords for the image. Users are prompted to provide precise keywords separated by commas.

- **PROMPT_DESCRIPTION**: The prompt used to request a description for the image. Users are prompted to provide a description for the image.

- **PROMPT_TITLE**: The prompt used to request a title for the image. Users are prompted to provide a title for the image.

### Function Parameters:

- **image_path**: The path to the image file being processed.

### Custom EXIF Tag:

- **CUSTOM_EXIF_TAG**: The name of the custom EXIF tag used to mark images that have been processed by the script. This tag is added to the metadata of processed images.


These parameters control various aspects of the script's behavior, such as where to find images, how to prompt users for input, and how to update image metadata. Adjusting these parameters allows customization of the script to fit specific use cases and requirements.


## Tools Used

- **Python**: The script is written in Python, a versatile programming language widely used for automation tasks.
- **PIL (Python Imaging Library)**: PIL is used for image processing tasks such as resizing images.
- **IPTCInfo**: This library is used for reading and writing IPTC metadata in images.
- **LangChain LLama**: LLama is an AI model used for generating tags based on image content.
- **ExifTool**: ExifTool is used for reading and writing metadata in various file formats, including images.
- **Pathlib**: Pathlib is used for working with file paths in a more object-oriented way.
