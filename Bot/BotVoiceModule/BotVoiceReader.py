from vosk import Model, KaldiRecognizer
import pathlib
from pathlib import Path
import pyaudio
import time
from functools import wraps


class VoiceReader:
    def __init__(self):
        self.path = str(Path(pathlib.Path.cwd(), "media_files", "models", "vosk-model-small-ru-0.22"))\
            .replace("BotVoiceModule\\", "")
        self.model = Model(self.path)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=16000)
        self.stream.stop_stream()
        self.history = []

    @staticmethod
    def mult_threading(func):
        """Декоратор для запуска функции в отдельном потоке"""
        @wraps(func)
        def wrapper(*args_, **kwargs_):
            import threading
            func_thread = threading.Thread(target=func,
                                           args=tuple(args_),
                                           kwargs=kwargs_)
            func_thread.start()
            return func_thread

        return wrapper

    @mult_threading
    def start(self, func):
        self.stream.start_stream()
        while True:
            try:
                data = self.stream.read(8000)
                if len(data) == 0:
                    break
                res = self.rec.Result() if self.rec.AcceptWaveform(data) else self.rec.PartialResult()
                res: str = res[res.index(":") + 2:]
                res = res[res.index('"') + 1: len(res) - 1 - res[::-1].index('"')]
                if len(self.history) == 0 or self.history[-1] != res:
                    func(res)
                    self.history.append(res)
            except OSError:
                break

    def stop(self):
        self.history.clear()
        self.stream.stop_stream()

    def is_activ(self) -> bool:
        return self.stream.is_active()


if __name__ == "__main__":
    voice = VoiceReader()
    voice.start(print)
    time.sleep(60)
    voice.stop()
