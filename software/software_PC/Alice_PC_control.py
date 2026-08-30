# Made by Timodrien 2025

import tkinter as tk
import asyncio
import websockets
import pyaudio
from PIL import Image, ImageTk
import io
import threading
import time
from face_detection import FaceTracker, FaceDetectionThread

# Audio-Einstellungen
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 256

class RobotControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ALICE Control GUI")
        self.websocket = None
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_event_loop, daemon=True).start()
        
        # Haupt-Layout: 2 Spalten
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)

        # Linke Seite: Statusmeldungen & Slider
        self.left_frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # Status-Anzeige
        self.status_label = tk.Label(self.left_frame, text="Status: Not Connected", bg="lightgray", font=("Arial", 12), anchor="w")
        self.status_label.pack(fill="x", pady=5)
        self.command_log = tk.Text(self.left_frame, wrap="word", height=8, state="disabled", bg="white", font=("Arial", 10))
        self.command_log.pack(fill="both", expand=True, pady=10)

        # Button-Leiste
        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.pack(fill="both", pady=5)
        
        #Buttons-Keyboard
        self.active_keys = set()
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        
        # Audio Button
        self.start_audio_button = tk.Button(self.button_frame, text="Audio", command=self.start_audio_stream)
        self.start_audio_button.pack(side="left", expand=True, fill="x")
        # Gesichtserkennung
        self.face_tracker = None  # FaceTracker Instanz
        self.face_enabled = False
        self.face_button = tk.Button(self.button_frame, text="Gesichtserkennung: AUS", command=self.toggle_face_detection)
        self.face_button.pack(side="left", expand=True, fill="x")

        self.last_detection_time = 0
        self.detection_interval = 0.5  # alle 0.5 Sekunden erkennen

        # Servo-Winkel & Slider
        self.servo_angles = [90, 90, 90, 0, 0, 90, 90, 180, 180, 90, 90, 90] #0-180
        self.sliders = []
        for i in range(12):
            frame = tk.Frame(self.left_frame)
            frame.pack(fill="x", pady=2)
            label = tk.Label(frame, text=f"Servo {i+1}", width=10)
            label.pack(side="left")
            slider = tk.Scale(frame, from_=0, to =180, orient="horizontal", resolution=1, command=lambda val, idx=i: self.update_servo_angle(idx, val))
            slider.set(self.servo_angles[i])
            slider.pack(fill="x", expand=True)
            self.sliders.append(slider)

        # Rechte Seite: Videostream
        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.rowconfigure(0, weight=3)
        self.video_label = tk.Label(self.right_frame, text="Video Stream", bg="black", fg="white")
        self.video_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def toggle_face_detection(self):
        self.face_enabled = not self.face_enabled
        status = "AN" if self.face_enabled else "AUS"
        self.face_button.config(text=f"Gesichtserkennung: {status}", bg="green" if self.face_enabled else "red")
        self.log_command(f"Gesichtserkennung {status}")

        # FaceTracker initialisieren und Thread starten, wenn aktiviert
        if self.face_enabled:
            self.face_tracker = FaceTracker()
            self.face_detection_thread = FaceDetectionThread(self.face_tracker)  # Ein separater Thread für Gesichtserkennung
            self.face_detection_thread.start()
        else:
            self.face_tracker = None
            if hasattr(self, 'face_detection_thread'):
                self.face_detection_thread.stop()  # Stoppe den Gesichtserkennungs-Thread

    def start_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def connect_to_robot(self):
        self.status_label.config(text="Status: Connecting...")
        uri = "ws://192.168.4.1:81"  # Replace with your ESP32's IP
        uri = "ws://192.168.0.168:8080"
        #uri = "wss://robot-relay.onrender.com"
        asyncio.run_coroutine_threadsafe(self.establish_connection(uri), self.loop)

    async def establish_connection(self, uri):
        try:
            self.websocket = await websockets.connect(uri)
            self.status_label.config(text="Status: Connected")
            self.log_command("Connected to robot.")
            asyncio.create_task(self.receive_data())
        except Exception as e:
            self.status_label.config(text="Status: Connection Failed")
            self.log_command(f"Connection error: {e}")

    def start_audio_stream(self):
        threading.Thread(target=self.send_audio, daemon=True).start()

    def send_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        
        async def stream_audio():
            async with websockets.connect("ws://192.168.4.1:81") as ws:
                self.log_command("Streaming Audio...")
                try:
                    while True:
                        data = stream.read(CHUNK, exception_on_overflow=False)
                        await ws.send(data)
                except Exception as e:
                    self.log_command(f"Audio streaming error: {e}")
                finally:
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    self.log_command("Audio streaming beendet.")

        asyncio.run_coroutine_threadsafe(stream_audio(), self.loop)

    async def receive_data(self):
        while True:
            try:
                data = await self.websocket.recv()
                if isinstance(data, bytes):  # Binärdaten für Videostream
                    self.update_video_stream(data)
                elif isinstance(data, str):  # Textdaten für Statusmeldungen
                    self.update_status(data)
            except Exception as e:
                self.log_command(f"Error receiving data: {e}")
                break

    async def play_audio(websocket):
        p = pyaudio.PyAudio()
        device_index = 0  # Überprüfe, ob der Index richtig ist, je nach verwendeter Audioausgabe auf dem PC
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, output_device_index=device_index, frames_per_buffer=CHUNK)

        while True:
            try:
                # Empfang von Audio-Daten über WebSocket
                audio_data = await websocket.recv()
                if audio_data:
                    # Wiedergabe der empfangenen Audio-Daten
                    stream.write(audio_data)
            except Exception as e:
                print(f"[Audio Error] {e}")
                break

    def update_video_stream(self, frame_data):
        try:
            image = Image.open(io.BytesIO(frame_data))
            #image = image.rotate(180)  # Videostream um 180° drehen
            #image = image.resize((1280, 720), Image.Resampling.LANCZOS)
            current_time = time.time()
            
            # Wenn Gesichtserkennung aktiv ist
            if self.face_enabled and self.face_tracker and (current_time - self.last_detection_time > self.detection_interval):
                #image_array, pan, tilt = self.face_tracker.detect_faces(image)
                #image = Image.fromarray(image_array)
                _, pan, tilt = self.face_tracker.detect_faces(image)
                self.update_servo_angle(0, tilt)
                self.update_servo_angle(1, pan)
                self.last_detection_time = current_time

            photo = ImageTk.PhotoImage(image)
            self.video_label.configure(image=photo)
            self.video_label.image = photo

        except Exception as e:
            self.log_command(f"Error processing video frame: {e}")

    def update_status(self, status_message):
        self.log_command(f"Status Update: {status_message}")

    def log_command(self, message):
        self.command_log.config(state="normal")
        self.command_log.insert("end", message + "\n")
        self.command_log.see("end")
        self.command_log.config(state="disabled")

    def update_servo_angle(self, servo, value):
        self.servo_angles[servo] = int(value)
        time.sleep(0.05)  # Kleine Verzögerung
        self.send_command(f"S{servo + 1}:{self.servo_angles[servo]}")

    def send_command(self, command):
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.send(command), self.loop)
            self.log_command(f"Command sent: {command}")
        else:
            self.log_command("Not connected to the robot.")

    def on_key_press(self, event):
        key = event.keysym.lower()
        if key in {"w", "a", "s", "d"} and key not in self.active_keys:
            self.active_keys.add(key)
            if key == "w": self.send_command("Vor")
            elif key == "a": self.send_command("Links")
            elif key == "s": self.send_command("Rueck")
            elif key == "d": self.send_command("Rechts")

    def on_key_release(self, event):
        key = event.keysym.lower()
        if key in self.active_keys:
            self.active_keys.remove(key)
            if not self.active_keys:
                self.send_command("Stop")
                
# App ausführen
root = tk.Tk()
app = RobotControlApp(root)
root.after(1000, app.connect_to_robot)
root.mainloop()
