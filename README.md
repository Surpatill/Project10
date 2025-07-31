**Image Text Extraction using Streamlit, OpenCV, and Tesseract**

**Overview**

This project aims to extract text from medical images using a combination of image processing and optical character recognition (OCR) techniques. The project uses a multi-step approach to extract text from medical images, including image selection and preprocessing, bounding box creation, text extraction, and data processing.

**Features**

- Image Selection: Selects the top 10 images based on their sharpness score and preprocesses them to enhance quality.
- Bounding Box Creation: Defines bounding boxes around the regions of interest in each image manually using a custom script.
- Text Extraction: Uses Tesseract to extract text from each region of interest.
- Data Processing: Processes the extracted data to format it into a readable table.

**Requirements**

- Python 3.x
- OpenCV: For image processing and bounding box creation.
- Tesseract: For text extraction.
- Streamlit: For creating a user interface to upload images and extract text.

**Usage**

1. Clone the repository: git clone https://github.com/your-username/image-text-extraction.git
2. Navigate to the project directory: cd image-text-extraction
3. Install required libraries: pip install opencv-python pytesseract streamlit
4. Run the Streamlit interface: streamlit run app.py
5. Upload images and extract text using the Streamlit interface.

**Results**

The project demonstrates the potential of using Streamlit, OpenCV, and Tesseract for image text extraction. While there are limitations to the accuracy of the extracted text, the project highlights the challenges and opportunities for further research and development.

**Future Work**

- Improving Accuracy: Refine the image processing and text extraction techniques to improve accuracy.
- Handling Complex Layouts: Develop techniques to handle complex layouts and multi-column text.
- Integrating with Other Technologies: Integrate the project with other technologies, such as natural language processing, to further enhance the extracted data.

**Contributing**

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.
