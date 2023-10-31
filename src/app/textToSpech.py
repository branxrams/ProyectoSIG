import os

import gtts


def texto_a_voz(texto: str, archivo_salida: str):
    """Convierte un texto a voz y lo guarda en un archivo de audio.

    Parameters
    ----------
    texto : str
        Texto a convertir a voz.
    archivo_salida : str
        Dirección del archivo de salida.
    """
    tts = gtts.gTTS(text=texto, lang="es")

    try:
        tts.save(archivo_salida)
    except gtts.gTTSError:
        print("Error al generar el archivo de audio")
    else:
        # Reproduce el archivo de audio (opcional)
        os.system(f"start {archivo_salida}")  # En Windows
