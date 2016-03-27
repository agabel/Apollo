import datetime
import numpy
import socket
import spotipy
import subprocess

sp = spotipy.Spotify()
results = sp.search(q='Thrift Shop Macklemore', limit=20)
test_audio_url = results['tracks']['items'][0]['preview_url'].replace("https://", "http://")

frames = []
raw_audio = None
channels = 2
sample_rate = 44100
bytes_per_sample = numpy.dtype(numpy.int16).itemsize
frame_size = bytes_per_sample * channels
chunk_size = frame_size * sample_rate

HOST = '192.168.22.109'
PORT = 50025
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

command = [
    '/usr/local/bin/ffmpeg',
    '-i', test_audio_url,
    '-f', 's16le',
    '-acodec', 'pcm_s16le',
    '-ar', '44100',
    '-ac', '2',
    '-'
]

pipe = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=chunk_size)

while raw_audio != '':
    raw_audio = pipe.stdout.read(chunk_size)
    if raw_audio:
        s.sendall(raw_audio)

s.close()
