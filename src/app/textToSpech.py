from gtts import gTTS
import os

def texto_a_voz(texto, archivo_salida):
    tts = gTTS(text=texto, lang='es')

    # Guarda la voz generada en un archivo de audio
    tts.save(archivo_salida)

    # Reproduce el archivo de audio (opcional)
    os.system(f"start {archivo_salida}")  # En Windows
