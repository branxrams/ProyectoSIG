"""
    Librerias a instalar
    numpy, 
    opencv-python, 
    pydub
    moviepy
    instalar FFmpeg
"""

import cv2
import numpy as np
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip
import time

class AudioImageAnimator:
    def __init__(self, image_path, audio_path, output_path):
        self.image = cv2.imread(image_path)
        self.audio = AudioSegment.from_file(audio_path)
        self.output_path = output_path

    def create_animation(self):
        image_height, image_width, _ = self.image.shape
        frame_rate = 30
        audio_duration = len(self.audio) / 1000
        num_frames = int(frame_rate * audio_duration)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter(self.output_path, fourcc, frame_rate, (image_width, image_height))

        for i in range(num_frames):
            start_time = i * (len(self.audio) / num_frames)
            end_time = (i + 1) * (len(self.audio) / num_frames)
            audio_chunk = self.audio[start_time:end_time]
            audio_volume = audio_chunk.rms

            displacement = int(image_height / 2 - audio_volume / 2)
            displaced_image = np.roll(self.image, displacement, axis=0)

            video.write(displaced_image)

        video.release()

    def show_animation(self):
        cap = cv2.VideoCapture(self.output_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Video', frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
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

        video_clip.write_videofile(output_sound_path, codec='libx264')

        video_clip.close()
        audio_clip.close()

if __name__ == "__main__":
    image_path = 'imagen_prueba.jpg'
    audio_path = 'audio_prueba.mp3'
    output_path = 'video_prueba.mp4'
    output_sound_path = 'video_con_audio.mp4'

    animator = AudioImageAnimator(image_path, audio_path, output_path)
    animator.create_animation()
    #animator.show_animation()
    
    output_sound_path = "video_con_audio.mp4"

    combiner = VideoAudioCombiner(output_path, audio_path)
    combiner.combine_audio_with_video(output_sound_path)