#!/usr/bin/env python

import asyncio
import pyaudio
import wave
from websockets.sync.client import connect
import time

curr = time.time()

p = pyaudio.PyAudio()
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

Recordframes = []

with connect("ws://192.168.0.166:8888/") as websocket:
    data = websocket.recv(4096)
    while data != "":
        time_2 = time.time()
        if time_2-curr > 20:
            break
        try:
            data = websocket.recv(4096)
            Recordframes.append(data)
            stream.write(data)
        except:
            print("Client Disconnected")
            break

stream.stop_stream()
stream.close()
p.terminate()

WAVE_OUTPUT_FILENAME = "BLEH2.wav"
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(p.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(Recordframes))
waveFile.close()