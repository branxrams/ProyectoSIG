import os
import cv2
import numpy as np
from moviepy.editor import AudioFileClip, VideoFileClip, VideoClip
from pydub import AudioSegment
import string

text1 = "sssss"

class AudioImageAnimator:
    def __init__(self, image_path, audio_path, output_path, target_height):
        self.image = cv2.imread(image_path)
        self.audio = AudioSegment.from_file(audio_path)
        self.output_path = output_path
        self.target_height = target_height

    def create_animation(self):
        # Resize the image to have the target height
        self.image = cv2.resize(self.image, (int(self.target_height * self.image.shape[1] / self.image.shape[0]), self.target_height))

        image_height, image_width, _ = self.image.shape
        frame_rate = 30
        audio_duration = len(self.audio) / 1000
        num_frames = int(frame_rate * audio_duration)

        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        video = cv2.VideoWriter(
            self.output_path, fourcc, frame_rate, (image_width, self.target_height)
        )

        for i in range(num_frames):
            start_time = i * (len(self.audio) / num_frames)
            end_time = (i + 1) * (len(self.audio) / num_frames)
            audio_chunk = self.audio[start_time:end_time]
            audio_volume = audio_chunk.rms

            displacement = int(self.target_height / 2 - audio_volume / 2)
            displaced_image = np.roll(self.image, displacement, axis=0)

            video.write(displaced_image)

        video.release()

    def show_animation(self):
        cap = cv2.VideoCapture(self.output_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)
            if cv2.waitKey(30) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


class VideoAudioCombiner:
    """
    Combina un archivo de audio con un archivo de video y guarda el resultado.

    Args:
        video_path (str): Ruta al archivo de video.
        audio_path (str): Ruta al archivo de audio que se agregará al video.
        output_path (str): Ruta donde se guardará el video resultante.

    Returns:
        None
    """

    def __init__(self, video_path, audio_path):
        self.video_path = video_path
        self.audio_path = audio_path

    def combine_audio_with_video(self, output_sound_path):
        video_clip = VideoFileClip(self.video_path)
        audio_clip = AudioFileClip(self.audio_path)

        video_clip = video_clip.set_audio(audio_clip)

        video_clip.write_videofile(output_sound_path, codec="libx264")

        video_clip.close()
        audio_clip.close()

class TalkingHeadAnimator:
    def __init__(self, image_path, audio_path, output_path):
        self.image = cv2.imread(image_path)
        self.audio: AudioSegment = AudioSegment.from_file(audio_path)
        self.output_path = output_path

        # Mapea letras del alfabeto a las imágenes correspondientes de la boca
        self.mouth_images = {}
        alphabet = string.ascii_uppercase
        for letter in alphabet:
            mouth_image_path = f"src/app/mouth_images/{letter}.png"  # Asegúrate de tener las imágenes adecuadas
            mouth_image = cv2.imread(mouth_image_path)
            # Convierte la imagen a formato BGR
            mouth_image_BGR = cv2.cvtColor(mouth_image, cv2.COLOR_RGB2BGR)
            # Resize the mouth image to match the dimensions of the base image
            mouth_image = cv2.resize(mouth_image_BGR, (1000, 1200))
            self.mouth_images[letter] = mouth_image

    def animate_mouth(self, t):
        audio_chunk = self.audio[t * 1000:(t + 1) * 1000]
        audio_volume = audio_chunk.rms
        text = text1  # Replace with your actual text
        text = text.upper()

        # Asegúrate de que el índice esté dentro de los límites válidos
        alphabet_index = min(int(t / self.audio.duration_seconds * len(text)), len(text) - 1)

        # Obtiene la letra correspondiente al índice
        letter = text[alphabet_index]
        # Obtiene la imagen de la boca correspondiente a la letra
        mouth_image = self.mouth_images.get(letter, self.mouth_images['A'])

        # Convierte la imagen a formato BGR
        animated_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

        # Sobrepone la imagen de la boca en toda la imagen base
        animated_image = mouth_image

        return animated_image

    def create_animation(self):
        video_clip = VideoClip(self.animate_mouth, duration=self.audio.duration_seconds)
        video_clip.fps = 30  # Establece la velocidad de cuadros por segundo
        video_clip.set_duration(self.audio.duration_seconds).write_videofile(self.output_path, codec='libx264')

"""
if __name__ == "__main__":
    image_path = "Base Image.png"
    audio_path = "output.mp3"
    output_path = "video_prueba.mp4"
    output_sound_path = "video_con_audio.mp4"

    animator = TalkingHeadAnimator(image_path, audio_path, output_path)
    animator.create_animation()

    output_sound_path = "video_con_audio.mp4"

    combiner = VideoAudioCombiner(output_path, audio_path)
    combiner.combine_audio_with_video(output_sound_path)

for file_to_delete in ["output.mp3", "video_prueba.mp4"]:
    if os.path.exists(file_to_delete):
        os.remove(file_to_delete)
    
    for file_name in os.listdir("."):
        if file_name.endswith(".mp3"):
            os.remove(file_name)

"""