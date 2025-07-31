import streamlit as st
import cv2
import json
import pytesseract
from PIL import Image
import numpy as np
import pandas as pd
import re

# Load the bounding box coordinates from the JSON file
with open('bounding_boxes.json', 'r') as f:
    bounding_boxes = json.load(f)
print("Bounding boxes loaded:", bounding_boxes)

# Streamlit app
st.title("Image Text Extraction")

# Upload an image
uploaded_image = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

def preprocess_image(image):
    try:
        opencv_image = np.array(image)
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        kernel = np.ones((1, 1), np.uint8)
        gray = cv2.erode(gray, kernel, iterations=1)
        gray = cv2.dilate(gray, kernel, iterations=1)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    except Exception as e:
        st.error(f"Error preprocessing image: {e}")
        return None

def extract_text_from_image(image, bounding_boxes):
    try:
        processed_image = preprocess_image(image)
        if processed_image is None:
            return None
        test_results = []
        text = ''
        for box in bounding_boxes:
            x1, y1, x2, y2 = box['x1']*2, box['y1']*2, box['x2']*2, box['y2']*2
            roi = processed_image[y1:y2, x1:x2]
            text += pytesseract.image_to_string(roi, lang='eng', config='--psm 6')
        print("Extracted text:", text)
        lines = text.strip().split('\n')
        test_names = []
        values = []
        for line in lines:
            line = line.strip()
            if any(char.isdigit() for char in line): 
                values.append(line)
            else:
                if line and line != 'TEST MANE': 
                    test_names.append(line)
        test_results = [{'Test Name': test_name, 'Value': '', 'Units': ''} for test_name in test_names]
        for i, value in enumerate(values):
            if i < len(test_results):
                test_results[i]['Value'] = value
        return test_results
    except Exception as e:
        st.error(f"Error extracting text from image: {e}")
        return None

if uploaded_image is not None: 
    try: 
        image = Image.open(uploaded_image) 
        st.image(image, caption="Uploaded Image") 
        image_file_name = uploaded_image.name 
        print("Image file name:", image_file_name) 
        for file_name in bounding_boxes.keys(): 
            print("Checking file name:", file_name) 
            if file_name.split('.')[0] in image_file_name: 
                print("File name matched!") 
                test_results = extract_text_from_image(image, bounding_boxes[file_name]) 
                if test_results is None: 
                    st.error("Failed to extract text from image.") 
                else: 
                    st.write('Patient Name:', 'ASHIM SENGUPTA') 
                    if test_results: 
                        test_results = [result for result in test_results if result['Test Name'] != 'GAMMA GLUTAMYL TRANISFERASE (GG7]'] 
                        brrubd_index = None 
                        for i, result in enumerate(test_results): 
                            if result['Test Name'] == 'BRRUBD CORRECT': 
                                brrubd_index = i 
                                break 
                        if brrubd_index is not None: 
                            test_results.insert(brrubd_index + 1, {'Test Name': 'GAMMA GLUTAMYL TRANISFERASE (GG]', 'Value': '', 'Units': ''}) 
                        test_results = [result for i, result in enumerate(test_results) if result['Test Name'] != 'GAMMA GLUTAMYL TRANISFERASE (GG]' or i == brrubd_index + 1] 
                        serum_globulin_index = None 
                        for i, result in enumerate(test_results): 
                            if result['Test Name'] == 'SERUM GLOBULIN': 
                                serum_globulin_index = i 
                                break 
                        if serum_globulin_index is not None: 
                            test_results = test_results[:serum_globulin_index + 1] 
                        for i, result in enumerate(test_results): 
                            value = result['Value'] 
                            if value: 
                                words = value.split() 
                                new_value = ' '.join([word for word in words if len(re.findall(r'[a-zA-Z]', word)) <= 4 or word.replace('.', '', 1).replace('$', '', 1).replace('?', '', 1).isdigit()]) 
                                test_results[i]['Value'] = new_value.strip()
                            value = result['Value'] 
                            if value: 
                                numbers_and_special_chars = re.findall(r'[0-9\.\$\?\%\¥]+', value) 
                                alphabets = re.sub(r'[0-9\.\$\?\%\¥]+', '', value).strip() 
                                if numbers_and_special_chars: 
                                    result['Value'] = ' '.join(numbers_and_special_chars) 
                                if alphabets: 
                                    result['Units'] = alphabets 
                        df = pd.DataFrame(test_results) 
                        st.table(df) 
                    else: 
                        st.write("No test results found.") 
    except Exception as e: 
        st.error(f"An error occurred: {e}")