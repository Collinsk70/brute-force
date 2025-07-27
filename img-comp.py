import cv2
import numpy as np
from tkinter import Tk, filedialog
from skimage.metrics import structural_similarity as ssim

def upload_image(prompt):
    root = Tk()
    root.withdraw()  # Hide main window
    file_path = filedialog.askopenfilename(title=prompt, filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
    return file_path

def facial_login(threshold=0.98):  # Adjusted for more realistic similarity
    print("🔐 Step 1: Select your registered face image (reference image).")
    reference_image_path = upload_image("Select the registered (reference) face image")

    print("📸 Step 2: Select the login attempt image (e.g., live capture or uploaded photo).")
    login_image_path = upload_image("Select the login attempt image")

    if not reference_image_path or not login_image_path:
        print("❌ Login cancelled. Both images must be selected.")
        return

    # Load images
    img_ref = cv2.imread(reference_image_path)
    img_login = cv2.imread(login_image_path)

    if img_ref is None or img_login is None:
        print("❌ One or both images couldn't be loaded.")
        return

    # Resize login image to match reference image size
    if img_ref.shape != img_login.shape:
        print("⚠️ Resizing login image to match the reference image size...")
        img_login = cv2.resize(img_login, (img_ref.shape[1], img_ref.shape[0]))

    # Convert to grayscale
    gray_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)
    gray_login = cv2.cvtColor(img_login, cv2.COLOR_BGR2GRAY)

    # Compare images using SSIM
    similarity_score, _ = ssim(gray_ref, gray_login, full=True)
    print(f"🔍 Similarity Score: {similarity_score:.4f}")

    # Login decision
    if similarity_score >= threshold:
        print("✅ Login successful. Welcome!")
    else:
        print("❌ Login failed. Faces do not match.")

# Run the login function
facial_login()
