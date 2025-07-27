import cv2
import numpy as np
from tkinter import Tk, filedialog
from skimage.metrics import structural_similarity as ssim

def upload_image(prompt):
    # Open a file dialog to choose an image
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title=prompt, filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
    return file_path

def compare_images_with_upload(threshold=0.99):
    print("Please select the first image.")
    image1_path = upload_image("Select the first image")
    
    print("Please select the second image.")
    image2_path = upload_image("Select the second image")

    if not image1_path or not image2_path:
        print("❌ Image upload canceled.")
        return

    # Load images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    if img1 is None or img2 is None:
        print("❌ One or both images could not be loaded.")
        return

    # Resize if dimensions differ
    if img1.shape != img2.shape:
        print("⚠️ Images have different dimensions. Resizing second image to match the first.")
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM
    score, _ = ssim(gray1, gray2, full=True)
    print(f"🔍 Similarity Score: {score:.4f}")

    # Decision
    if score == 1.0:
        print("✅ The images are identical.")
    elif score >= threshold:
        print("⚠️ The images are similar but not identical.")
    else:
        print("❌ The images are different.")

# Run the function
compare_images_with_upload()
