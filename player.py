import socket
import numpy
import thread
import pyaudio

HOST = '192.168.22.109'
PORT = 50025

_CONNECTIONS = {}

FRAMES = []
channels = 2
sample_rate = 44100
bytes_per_sample = numpy.dtype(numpy.int16).itemsize
frame_size = bytes_per_sample * channels
chunk_size = frame_size * sample_rate


def play_audio_frames():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, output=True)
    while True:
        for frame in FRAMES:
            audio_frame = frame.tostring()
            stream.write(audio_frame)


def process_audio():
    print("processing audio")
    thread.start_new_thread(play_audio_frames, ())


def start_server():
    ADDR = (HOST, PORT)
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    conn, addr = serversock.accept()
    print("Accepting connections")
    while True:
        data = conn.recv(chunk_size)
        if data != '':
            print("Received data")
            audio_array = numpy.fromstring(data, dtype=numpy.int16)
            audio_array = audio_array.reshape((len(audio_array)/2, 2))
            FRAMES.append(audio_array)

if __name__ == "__main__":
    process_audio()
    start_server()








