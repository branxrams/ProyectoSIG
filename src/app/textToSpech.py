import os
import subprocess
import unittest
from dataclasses import dataclass

import gtts

__all__ = ("TextToSpeechConverter",)


@dataclass(slots=True, frozen=True)
class TextToSpeechConverter:
    text: str
    output_file: str = "output.mp3"

    def convert_to_audio(self):
        """Convert text to audio"""
        tts = gtts.gTTS(text=self.text, lang="es")
        with open(self.output_file, "wb") as f:
            tts.write_to_fp(f)

    def play_audio(self):
        """Play audio file"""
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


class TestTextToSpeechConverter(unittest.TestCase):
    def test_convert_to_audio(self):
        texto = "Hola mundo"
        archivo_salida = "test.mp3"

        converter = TextToSpeechConverter(texto, archivo_salida)
        converter.convert_to_audio()
        self.assertTrue(os.path.exists(archivo_salida))
        os.remove(archivo_salida)

    def test_play_audio(self):
        texto = "Hola mundo"
        archivo_salida = "test.mp3"

        converter = TextToSpeechConverter(texto, archivo_salida)
        converter.convert_to_audio()
        converter.play_audio()


if __name__ == "__main__":
    unittest.main()
