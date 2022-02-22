from vosk import Model, KaldiRecognizer
import pathlib
from pathlib import Path
import os
import pyaudio


class VoiceReader:
    def __init__(self):
        self.path_model = "C:\\Python Project\\Bot\\Bot\\media_files\\models\\vosk-model-small-ru-0.22"
        self.model = Model(self.path_model)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=16000)

    def start(self):
        self.stream.start_stream()
        while True:
            data = self.stream.read(8000)
            if len(data) == 0:
                break
            print(self.rec.Result() if self.rec.AcceptWaveform(data) else self.rec.PartialResult())
        print(self.rec.FinalResult())


if __name__ == "__main__":
    voice = VoiceReader()
    voice.start()
