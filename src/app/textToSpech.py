import os
import subprocess
import time
import unittest
from dataclasses import dataclass

import gtts

__all__ = ("TextToSpeechConverter",)


@dataclass(slots=True, frozen=True)
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

    def play_audio(self):
        """Reproduce el archivo de audio"""
        if os.name == "nt":
            subprocess.run(
                ["start", self.output_file],
                shell=True,
                check=True,
            )
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
            if os.name == "nt":
                subprocess.run(
                    ["del", self.output_file],
                    shell=True,
                    check=True,
                )
            else:
                subprocess.run(
                    ["rm", self.output_file],
                    check=True,
                )
        except Exception as e:
            print(f"Error al eliminar el archivo {self.output_file}: {e}")
        else:
            print(f"Archivo {self.output_file!r} eliminado")


class TestTextToSpeechConverter(unittest.TestCase):
    def setUp(self):
        self.text = "Hola mundo"
        self.output_file = "test.mp3"
        self.converter = TextToSpeechConverter(self.text, self.output_file)

    def test_convert_to_audio(self):
        self.converter.convert_to_audio()
        self.assertTrue(os.path.exists(self.output_file))

    def test_play_audio(self):
        self.converter.convert_to_audio()
        self.converter.play_audio()

    def tearDown(self):
        time.sleep(3)
        self.converter.delete_audio_file()


if __name__ == "__main__":
    unittest.main()
