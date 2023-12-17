import logging
import os
from re import T
import subprocess
import time
import unittest
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

from audio_visual_animation import TalkingHeadAnimator, VideoAudioCombiner
import audio_visual_animation

load_dotenv()


URL = "https://speechgen.io/index.php?r=api/text"
PARAMS = {
    "token": os.getenv("API_TOKEN"),
    "email": os.getenv("API_EMAIL"),
    "voice": "Bartolo",
}

mensaje1 = ""
titulo = ""


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
    
    # Verificar si las pruebas fueron exitosas antes de continuar con el código adicional
    if result.wasSuccessful():
        audio_path = "output.mp3"
        output_path = "video.mp4"
        output_sound_path = f"{titulo}.mp4"
        audio_visual_animation.text1 = mensaje1
        audio_visual_animation.title = titulo
        animator = TalkingHeadAnimator(audio_path, output_path, 10)
        animator.create_animation()
        #output_sound_path = f"{titulo}.mp4"
        combiner = VideoAudioCombiner(output_path, audio_path)
        combiner.combine_audio_with_video(output_sound_path)
    
    for file_to_delete in ["output.mp3", f"{titulo}_prueba.mp4"]:
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
    
    for file_name in os.listdir("."):
        if file_name.endswith(".mp3"):
            os.remove(file_name)
    
"""
if __name__ == "__main__":
    unittest.main()
"""