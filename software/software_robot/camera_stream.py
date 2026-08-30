# Made by Timodrien 2025

import asyncio
import websockets
from picamera2 import Picamera2
from libcamera import controls
import io
from PIL import Image
from servo_control import handle_servo_command  # Import der Steuerfunktion
#from audio_stream import send_audio

# Kamera einrichten
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (1280, 720)},
    sensor={'output_size': (3280, 2464)},
    controls={
        #"ScalerCrop": (0, 0, 1280, 720),
        "FrameRate": 30
    }
)
picam2.configure(config)
picam2.start()

async def send_video(websocket):
    frame_interval = 1 / 30  # Für eine Bildrate von 30 FPS
    while True:
        try:
            image = picam2.capture_array("main")
            img = Image.fromarray(image).convert('RGB')
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=80)
            await websocket.send(img_byte_arr.getvalue())
            await asyncio.sleep(frame_interval)
        except Exception as e:
            print(f"[Video Error] {e}")
            break

async def receive_commands(websocket):
    async for message in websocket:
        await handle_servo_command(message)

async def video_and_control(websocket, path):
    print("Client connected")
    try:
        video_task = asyncio.create_task(send_video(websocket))
        command_task = asyncio.create_task(receive_commands(websocket))
        await asyncio.gather(video_task, command_task)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"[WebSocket Error] {e}")

#async def audio_stream_only(websocket, path):
#    print("Audio client connected")
#    try:
#        await send_audio(websocket)
#    except Exception as e:
#        print(f"[Audio WebSocket Error] {e}")

start_server = websockets.serve(video_and_control, "0.0.0.0", 8080)
#audio_server = websockets.serve(audio_stream_only, "0.0.0.0", 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
#loop.run_until_complete(audio_server)
loop.run_forever()