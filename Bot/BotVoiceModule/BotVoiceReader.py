from vosk import Model, KaldiRecognizer
import pathlib
from pathlib import Path
# import pyaudio
import time
from functools import wraps


class VoiceReader:
    def __init__(self):
        self.path = str(Path(pathlib.Path.cwd(), "BotVoiceModule", "models", "vosk-model-small-ru-0.22"))
        self.model = Model(self.path)
        self.rec = KaldiRecognizer(self.model, 16000)
        # self.p = pyaudio.PyAudio()
        self.history = []
        self.stream = None
        self.is_record = False

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
        self.stream = self.p.open(
            # format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=16000)
        self.stream.start_stream()
        self.is_record = True
        while True:
            try:
                data = self.stream.read(8000)
                if len(data) == 0:
                    self.is_record = False
                    break
                res = self.rec.Result() if self.rec.AcceptWaveform(data) else self.rec.PartialResult()
                res: str = res[res.index(":") + 2:]
                res = res[res.index('"') + 1: len(res) - 1 - res[::-1].index('"')]
                if len(self.history) == 0 or self.history[-1] != res:
                    func(res)
                    self.history.append(res)
            except OSError:
                self.is_record = False
                break

    def stop(self):
        self.is_record = False
        self.history.clear()
        if self.stream is not None:
            self.stream.stop_stream()

    def is_activ(self) -> bool:
        return self.is_record


if __name__ == "__main__":
    voice = VoiceReader()
    voice.start(print)
    time.sleep(60)
    voice.stop()
