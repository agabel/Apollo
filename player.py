import socket
import numpy
import pyaudio

from loggers import server_logger


server_logger.info("Starting player daemon...")

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                output=True)


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50023             # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    stream.write(data)

conn.close()

