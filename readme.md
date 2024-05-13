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

3. Set up the necessary configuration in the script (e.g., LLama model URL, source directory, target directory, prompts).

4. Run the script:

    ```bash
    python image_tagging_script.py
    ```

5. The script will process each image in the specified source directory, generate tags using AI models, and update the metadata of the images with the generated tags.

## Tools Used

- **Python**: The script is written in Python, a versatile programming language widely used for automation tasks.
- **PIL (Python Imaging Library)**: PIL is used for image processing tasks such as resizing images.
- **IPTCInfo**: This library is used for reading and writing IPTC metadata in images.
- **LangChain LLama**: LLama is an AI model used for generating tags based on image content.
- **ExifTool**: ExifTool is used for reading and writing metadata in various file formats, including images.
- **Pathlib**: Pathlib is used for working with file paths in a more object-oriented way.
