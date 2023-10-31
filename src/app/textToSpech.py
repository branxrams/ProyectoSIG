import os
import subprocess
import tempfile
import time
import unittest
from dataclasses import dataclass

import gtts

__all__ = ("TextToSpeechConverter",)


@dataclass(slots=True, unsafe_hash=True)
class TextToSpeechConverter:
    text: str
    output_file: str = "output.mp3"

    def __post_init__(self):
        """Verfica si el archivo de salida existe, si existe le agrega un timestamp al nombre del archivo"""
        if os.path.exists(self.output_file):
            filename, file_extension = os.path.splitext(self.output_file)
            self.output_file = f"{filename}_{int(time.time())}{file_extension}"

    def convert_to_audio(self):
        """Realiza la conversión de texto a audio"""
        tts = gtts.gTTS(text=self.text, lang="es")
        with open(self.output_file, "wb") as f:
            tts.write_to_fp(f)

    def convert_to_temporal_audio(self):
        """Realiza la conversión de texto a audio y lo guarda en un archivo temporal"""
        tts = gtts.gTTS(text=self.text, lang="es")
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tts.write_to_fp(f)
            self.output_file = f.name

    def play_audio(self):
        """Reproduce el archivo de audio"""
        if os.name == "nt":
            os.startfile(self.output_file, "open")
        else:
            subprocess.run(
                ["xdg-open", self.output_file],
                check=True,
            )

    def delete_audio_file(self):
        """Elimina el archivo de audio"""
        if not os.path.exists(self.output_file):
            return print(f"{self.output_file} no ha sido creado")

        try:
            os.remove(self.output_file)
        except FileNotFoundError:
            print(f"El archivo {self.output_file} no existe")
        except Exception as e:
            print(f"Error al eliminar el archivo {self.output_file}: {e}")


class TestTextToSpeechConverter(unittest.TestCase):
    def setUp(self):
        self.text = "Hola mundo"
        self.output_file = "test.mp3"
        self.converter = TextToSpeechConverter(self.text, self.output_file)

    def test_convert_to_audio(self):
        self.converter.convert_to_audio()
        self.assertTrue(os.path.exists(self.output_file))

    def test_convert_to_temporal_audio(self):
        self.converter.convert_to_temporal_audio()
        self.assertTrue(os.path.exists(self.converter.output_file))

    def test_play_audio(self):
        self.converter.convert_to_audio()
        self.converter.play_audio()

    def tearDown(self):
        time.sleep(3)
        self.converter.delete_audio_file()


if __name__ == "__main__":
    unittest.main()
