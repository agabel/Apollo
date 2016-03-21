import socket
import numpy
import pyaudio
import thread
import select


from loggers import server_logger

HOST = '127.0.0.1'
PORT = 50023

_CONNECTIONS = {}

FRAMES = []


class AudioStream():
    stream = None

    def __init__(self):
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16,
                        channels=2,
                        rate=44100,
                        output=True)


AUDIO_STREAM = AudioStream()

def play_audio_frames():
    while True:
        if len(FRAMES):
            frame = FRAMES.pop(0)
            AUDIO_STREAM.stream.write(frame)

def process_audio():
    audio_thread = thread.start_new_thread(play_audio_frames)


def create_server_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    s.setblocking(0)

    return s


def start_server():
    ADDR = (HOST, PORT)
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    conn, addr = serversock.accept()
    while True:
        data = conn.recv(88200)
        if data != '':
            try:
                FRAMES.append(data)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    process_audio()
    start_server()








