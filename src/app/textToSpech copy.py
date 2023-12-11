import logging
import os
import subprocess
import time
import unittest
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

load_dotenv()


URL = "https://speechgen.io/index.php?r=api/text"
PARAMS = {
    "token": os.getenv("API_TOKEN"),
    "email": os.getenv("API_EMAIL"),
    "voice": "Bartolo",
}
mensaje1 = ""


__all__ = ("TextToSpeechConverter", "message1")


logging.basicConfig(level=logging.INFO)


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
        """Perform text to audio conversion"""
        try:
            response = requests.get(URL, params=PARAMS | {"text": self.text})
            response.raise_for_status()
            data = response.json()

            audio_response = requests.get(data["file"], stream=True)
            audio_response.raise_for_status()

            with open(self.output_file, "wb") as f:
                f.write(audio_response.content)
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            return False
        return True

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
        self.text = mensaje1
        self.converter = TextToSpeechConverter(self.text)

    def test_convert_to_audio(self):
        result = self.converter.convert_to_audio()
        self.assertTrue(result and os.path.exists(self.converter.output_file))

    def test_play_audio(self):
        self.converter.convert_to_audio()
        self.converter.play_audio()

    def tearDown(self):
        # self.converter.delete_audio_file()
        pass


def run_tests_and_additional_code():
    # Ejecutar las pruebas
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTextToSpeechConverter)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

"""
if __name__ == "__main__":
    unittest.main()
"""