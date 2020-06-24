import pyaudio
import wave
import os, errno
import mfcc as mf

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 6 # 5 sec
FOLDER = "audio_data"

try:
    if not(os.path.isdir(FOLDER)):
        os.makedirs(os.path.join(FOLDER))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!!!!")
        raise

for i in range(5):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording", i)

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording", i)

    stream.stop_stream()
    stream.close()
    p.terminate()

    WAVE_OUTPUT_FILENAME = os.path.join(FOLDER, str(i)+".wav")

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


mf.audio_preprocessing()