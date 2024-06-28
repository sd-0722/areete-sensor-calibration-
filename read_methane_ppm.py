#!/usr/bin/env python

#!/usr/bin/env python

import asyncio
import websockets

async def hello(websocket):
    ppm = await websocket.recv()
    print("methane PPM ", ppm)
    while ppm!="":
        ppm = await websocket.recv()
        print("methane PPM ", ppm)

async def main():
    async with websockets.serve(hello, host="192.168.0.224", port=8888):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
# curr = time.time()

# p = pyaudio.PyAudio()
# CHUNK = 1024 * 4
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 output=True,
#                 frames_per_buffer=CHUNK)

# Recordframes = []


# stream.stop_stream()
# stream.close() 
# p.terminate()

# WAVE_OUTPUT_FILENAME = "BLEH3.wav"
# waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# waveFile.setnchannels(CHANNELS)
# waveFile.setsampwidth(p.get_sample_size(FORMAT))
# waveFile.setframerate(RATE)
# waveFile.writeframes(b''.join(Recordframes))
# waveFile.close()