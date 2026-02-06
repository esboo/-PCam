import cv2
import requests
import numpy as np
import pyvirtualcam

# --- CONFIGURATION ---
# Replace with the IP address shown on your phone app
PHONE_IP = "192.168.1.9"
PORT = "4747"
URL = f"http://{PHONE_IP}:{PORT}"

def resize_with_pad(image, target_width, target_height, zoom_factor=1.0):
    h, w = image.shape[:2]

    if zoom_factor > 1.0:
        new_h, new_w = int(h / zoom_factor), int(w / zoom_factor)
        start_h = (h - new_h) // 2
        start_w = (w - new_w) // 2
        image = image[start_h:start_h + new_h, start_w:start_w + new_w]
        h, w = image.shape[:2]

    ratio = min(target_width / w, target_height / h)
    new_w, new_h = int(w * ratio), int(h * ratio)

    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Create a black canvas of the target size
    padded = np.zeros((target_height, target_width, 3), dtype=np.uint8)

    # Center the resized image on the canvas
    x_offset = (target_width - new_w) // 2
    y_offset = (target_height - new_h) // 2
    padded[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized

    return padded

def main():
    print(f"Connecting to {URL}...")
    print("Controls: 'z' to zoom in, 'x' to zoom out, 'ESC' to exit")

    try:
        stream = requests.get(URL, stream=True, timeout=5)
    except Exception as e:
        print(f"Error: Could not connect to phone. Make sure the app is running and on the same WiFi.\n{e}")
        return

    bytes_data = bytes()
    zoom_level = 1.0

    # Initialize virtual camera
    with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
        print(f'Using virtual camera: {cam.device}')

        for chunk in stream.iter_content(chunk_size=1024):
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8') # JPEG start
            b = bytes_data.find(b'\xff\xd9') # JPEG end

            if a != -1 and b != -1:
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]

                # Decode JPEG
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                if img is not None:
                    # Resize while maintaining aspect ratio and applying zoom
                    img_final = resize_with_pad(img, 1280, 720, zoom_level)

                    # Convert BGR (OpenCV) to RGB (pyvirtualcam)
                    img_rgb = cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB)

                    # Send to virtual camera
                    cam.send(img_rgb)
                    cam.sleep_until_next_frame()

                    # Also show local preview
                    cv2.imshow('PCam Desktop Client', img_final)

                key = cv2.waitKey(1)
                if key == 27: # ESC to exit
                    break
                elif key == ord('z'): # Zoom in
                    zoom_level = min(zoom_level + 0.1, 5.0)
                    print(f"Zoom level: {zoom_level:.1f}x")
                elif key == ord('x'): # Zoom out
                    zoom_level = max(zoom_level - 0.1, 1.0)
                    print(f"Zoom level: {zoom_level:.1f}x")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
