# -PCam
📱 PCam: Turn Your Phone into a High-End Virtual Webcam

PCam is a two-part ecosystem that streams your Android camera directly to your PC, transforming it into a virtual webcam. Forget grainy laptop cameras—use the powerful optics already in your pocket for Zoom, Discord, OBS, and more.

✨ Features

•Wireless HD Streaming: Low-latency MJPEG streaming over your local Wi-Fi.

•Virtual Camera Integration: Seamlessly appears as a standard webcam in your favorite PC applications via pyvirtualcam.

•Real-time Zoom: Dynamically zoom in and out using keyboard controls ('Z' and 'X').

•Smart Letterboxing: Maintains your phone's aspect ratio without stretching the image, providing a professional 1280x720 output.

•Native Android Performance: Built with Kotlin and Jetpack Compose for a lightweight server experience.

🛠️ How It Works

1. The Server (Android): Your phone captures video and hosts a local HTTP server.

2. The Client (Python): Your PC fetches the stream, processes the frames (resizing/zooming), and injects them into a virtual camera device.

🚀 Getting Started

1. Setup the Android App

•
Open the PCam project in Android Studio.

•
Build and run the app on your Android device.

•
Note the IP Address displayed on the screen (e.g., 192.168.1.9).

2. Setup the Desktop Client            
            
Ensure you have Python installed, then set up the dependencies:

`pip install opencv-python requests numpy pyvirtualcam`

Note: You may need a virtual camera driver installed on your OS (like OBS Virtual Cam or UnityCapture).

3. Run the Stream

1. Open desktop_client/pcam_client.py.

2. Update the PHONE_IP variable with the IP shown on your phone.

3. Run the script:

`    python pcam_client.py
    `
    
If you want to run this via USB Mode - You can edit the python script by changing the IP address into `localhost`. Ensure that USB debugging is enabled in Developer Options. After that, type

`adb devices` - if you can see you device then type this next

`adb forward tcp:4747 tcp:4747`

then run the `python pcam_client.py`


⌨️ Desktop Controls

| Key | Action | | :--- | :--- | | Z | Zoom In (Up to 5.0x) | | X | Zoom Out (Down to 1.0x) | | ESC | Exit the client safely |
PCam/

├── app/                # Kotlin Android Source (The Server)
└── desktop_client/     # Python Source (The Client)
    └── pcam_client.py  # Virtual Cam & Processing Logic

🤝 Contributing

Feel free to fork this project, report issues, or submit pull requests. Future goals include adding:
•
[ ] Audio streaming support.
•
[ ] Toggle for Front/Back camera from the Desktop.
•
[ ] Auto-discovery via mDNS (no more typing IP addresses!).

Developed with ❤️ by ecaeca07 via vibe coding.
And this isn't possible without the help of Android CameraX - a Jetpack support library that simplifies camera app development by providing a consistent API across most Android 5.0+ devices.

Turn your phone into the ultimate workstation tool.

By the way, I vibe-coded this app because I don't want to purchase paid products like DroidCam or Iriun.
