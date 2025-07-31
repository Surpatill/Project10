import cv2
import os

# Folder containing images
image_folder = '.'

# Initialize list to store image scores
image_scores = []

# Loop through images
for filename in os.listdir(image_folder):
    # Check if file is an image
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        # Read image
        img = cv2.imread(os.path.join(image_folder, filename))
        
        # Check if image was read successfully
        if img is not None:
            # Calculate sharpness score (variance of Laplacian)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            score = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Store image score
            image_scores.append((filename, score))

# Sort images by score
image_scores.sort(key=lambda x: x[1], reverse=True)

# Select top 10 images
top_images = image_scores[:10]

# Print top 10 image filenames
for filename, score in top_images:
    print(f"{filename} (Score: {score})")