import socket
from loggers import server_logger
import spotipy
import subprocess
import numpy
import pyaudio
import time




sp = spotipy.Spotify()

results = sp.search(q='Thrift Shop Macklemore', limit=20)

test_audio_url = results['tracks']['items'][0]['preview_url']

input_file = '/Users/Austin/Desktop/passenger-let-her-go.mp3'


command = [
    '/usr/local/bin/ffmpeg',
    '-i', input_file,
    '-f', 's16le',
    '-acodec', 'pcm_s16le',
    '-ar', '44100',  # ouput will have 44100 Hz
    '-ac', '2',  # stereo (set to '1' for mono)
    '-'
]

pipe = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10**8)


frames = []

raw_audio = None

while raw_audio != '':
    raw_audio = pipe.stdout.read(88200*4)
    audio_array = numpy.fromstring(raw_audio, dtype="int16")
    audio_array = audio_array.reshape((len(audio_array)/2, 2))
    frames.append(audio_array)


#
# p = pyaudio.PyAudio()
#
# stream = p.open(format=pyaudio.paInt16,
#                 channels=2,
#                 rate=44100,
#                 output=True)


# for current_frame in frames:
#     stream.write(current_frame.astype(numpy.int16).tostring())





HOST = '127.0.0.1'    # The remote host
PORT = 50023              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

for current_frame in frames:
    s.sendall(current_frame.astype(numpy.int16).tostring())

s.close()

server_logger.info("Received data")

