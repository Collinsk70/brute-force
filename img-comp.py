import face_recognition
import cv2

def load_reference_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        print("❌ No face found in the reference image.")
        return None
    return encodings[0]

def capture_webcam_image():
    cam = cv2.VideoCapture(0)
    print("📸 Press 's' to capture your face for login...")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Failed to access webcam.")
            break

        cv2.imshow("Live Webcam - Press 's' to capture", frame)

        key = cv2.waitKey(1)
        if key == ord('s'):
            print("📷 Captured!")
            cam.release()
            cv2.destroyAllWindows()
            return frame

    cam.release()
    cv2.destroyAllWindows()
    return None

def facial_login(reference_image_path, tolerance=0.6):
    print("🔐 Loading registered user image...")
    reference_encoding = load_reference_encoding(reference_image_path)
    if reference_encoding is None:
        return

    print("🎥 Opening webcam...")
    frame = capture_webcam_image()
    if frame is None:
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    webcam_encodings = face_recognition.face_encodings(rgb_frame)

    if not webcam_encodings:
        print("❌ No face detected in webcam capture.")
        return

    webcam_encoding = webcam_encodings[0]
    matches = face_recognition.compare_faces([reference_encoding], webcam_encoding, tolerance=tolerance)
    distance = face_recognition.face_distance([reference_encoding], webcam_encoding)[0]

    print(f"🧠 Face distance: {distance:.4f}")
    if matches[0]:
        print("✅ Login successful. Face matched.")
    else:
        print("❌ Login failed. Face does not match.")

# Set your reference image
reference_image = "T-test.jpg"  # Ensure it's in the same folder
facial_login(reference_image)
