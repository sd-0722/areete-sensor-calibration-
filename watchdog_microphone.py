import sys
import os
import logging
import time
import pyaudio
import wave
from websockets.sync.client import connect
from typing import override
from multiprocessing import Process
from google.cloud import storage
import watchdog.events
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEvent


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

class CustomEventHandler(LoggingEventHandler):
    @override
    def on_created(self, event: FileSystemEvent) -> None:
        what = "directory" if event.is_directory else "file"
        self.logger.info("Created %s: %s", what, event.src_path)
        now = time.time()
        upload_blob("cow_sounds", event.src_path, f"test_{now}.txt")


#upload_blob("cow_sounds", "./bucket_upload_test/brat.png", "brat.png")
def upload_on_file_create():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = CustomEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()

def random_file_creator():
    fileSizeInBytes = 1024
    while True:
        now = time.time()
        with open(f"out_{now}.txt", 'wb') as fout:
            fout.write(os.urandom(fileSizeInBytes))
            time.sleep(20)

def client():
    def todatetime(epoch):
        return datetime.fromtimestamp(epoch) 
    
    def todatetime(epoch):
        return datetime.fromtimestamp(epoch)  

    curr = time.time()

    CHUNK = 1024 * 4
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    def return_stream_objects():
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
        
        return stream, p

    Recordframes = []
    _stream, _p = return_stream_objects()
    idx = 0

    with connect("ws://192.168.0.166:8888/") as websocket:
        data = websocket.recv(4096)
        while data != "":
            time_2 = time.time()
            if time_2-curr > 182:
                _stream.stop_stream()
                _stream.close()
                _p.terminate()

                WAVE_OUTPUT_FILENAME = f"BLEH_{todatetime(curr)}.wav"
                waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                waveFile.setnchannels(CHANNELS)
                waveFile.setsampwidth(_p.get_sample_size(FORMAT))
                waveFile.setframerate(RATE)
                waveFile.writeframes(b''.join(Recordframes))
                waveFile.close()

                Recordframes = []
                #make a new object to record to 
                _stream, _p = return_stream_objects() 
                curr = time.time()
            try:
                data = websocket.recv(4096)
                Recordframes.append(data)
                _stream.write(data)
            except:
                print("Client Disconnected")
                break

if __name__ == '__main__':
    watcher = Process(target=upload_on_file_create)
    writer = Process(target=client)
    watcher.start()
    writer.start()
