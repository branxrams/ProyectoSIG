import os
import subprocess
import cv2
import numpy as np
from moviepy.editor import AudioFileClip, VideoFileClip, VideoClip
from pydub import AudioSegment
import tkinter as tk
from tkinter import messagebox
import string

text1 = "sssss"
title = ""

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

        # Obtiene la ruta completa del video generado
        video_path = os.path.abspath(title)

        # Muestra una ventana emergente indicando que el video se generó con éxito.
        messagebox.showinfo("Éxito", f"El video se generó con éxito!\nRuta del video: {video_path}.mp4")

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
    def __init__(self, audio_path, output_path, target_duration=10.0):
        self.images = [cv2.imread(f"src/app/images/{i}.png") for i in range(32)]
        self.audio = AudioSegment.from_file(audio_path)
        self.output_path = output_path
        self.target_duration = target_duration

    def animate_frame(self, t):
        frame_index = int(t / (self.audio.duration_seconds) * len(self.images))
        frame_index = min(frame_index, len(self.images) - 1)
        frame_image = cv2.resize(self.images[frame_index], (1000, 1200))
        return cv2.cvtColor(frame_image, cv2.COLOR_BGR2RGB)

    def create_animation(self):
        # Calcular la duración promedio por palabra
        avg_duration_per_word = self.audio.duration_seconds / len(text1)

        # Calcular el speed_factor necesario para alcanzar la duración deseada del video
        speed_factor = avg_duration_per_word / self.audio.duration_seconds

        # Calculate the adjusted frames per second
        if len(text1) <= 17:
            adjusted_fps = 30 * 0.5
        elif len(text1) <= 64:
            print(2)
            adjusted_fps = 30 * 0.2
        else:
            adjusted_fps = 30 * 0.02

        # Create a VideoClip with the animated frames
        video_clip = VideoClip(self.animate_frame, duration=self.audio.duration_seconds)

        # Set adjusted frames per second
        video_clip.fps = adjusted_fps

        # Write the video file
        video_clip.set_duration(self.audio.duration_seconds).write_videofile(self.output_path, codec='libx264')

        # Obtiene la ruta completa del video generado
        video_path = os.path.abspath(title)

        # Muestra una ventana emergente indicando que el video se generó con éxito.
        messagebox.showinfo("Éxito", f"El video se generó con éxito!\nRuta del video: {video_path}.mp4")

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