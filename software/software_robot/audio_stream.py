# Made by Timodrien 2025

import pyaudio
import asyncio

# Audio-Einstellungen
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

async def send_audio(websocket):
    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        #input_device_index=2,  # Entspricht hw:2,0
        frames_per_buffer=CHUNK
    )

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            await websocket.send(data)  # ← Jetzt korrekt await!
    except Exception as e:
        print(f"[Audio Error] {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
