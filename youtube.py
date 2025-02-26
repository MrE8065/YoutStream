#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script en Python para reproducir solo el audio de streams de YouTube y obtener la miniatura.

Requisitos:
  - Instalar yt-dlp: pip install yt-dlp
  - Instalar python-vlc: pip install python-vlc
  - Tener VLC instalado en el sistema.

Uso:
  python reproducir_audio_youtube.py <URL_de_Youtube>
"""

import sys
import time
import vlc
import yt_dlp

def obtener_url_audio(youtube_url):
    """
    Utiliza yt-dlp para extraer la URL del stream de audio de mejor calidad.
    """
    opciones = {
        'format': 'bestaudio',  # Se solicita solo el mejor audio
        'quiet': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        print("URL: " + info.get('url'))
        # Retorna la URL del stream de audio
        return info.get('url')

def obtener_miniatura(youtube_url):
    """
    Utiliza yt-dlp para extraer la URL de la miniatura del video.
    """
    opciones = {
        'format': 'bestaudio',  # El formato no afecta la miniatura
        'quiet': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        print("Miniatura: " + info.get('thumbnail'))
        # Retorna la URL de la miniatura
        return info.get('thumbnail')

def reproducir_audio(url_audio):
    """
    Crea una instancia de VLC y reproduce el stream de audio.
    """
    instancia = vlc.Instance()
    reproductor = instancia.media_player_new()
    media = instancia.media_new(url_audio)
    reproductor.set_media(media)

    # Iniciar reproducción
    reproductor.play()
    print("Reproduciendo audio...")

    # Mantiene el script activo mientras se reproduce el audio
    while True:
        estado = reproductor.get_state()
        if estado in [vlc.State.Ended, vlc.State.Error]:
            break
        time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python reproducir_audio_youtube.py <URL_de_Youtube>")
        sys.exit(1)
    youtube_url = sys.argv[1]
    
    try:
        # Obtener y mostrar la miniatura
        thumbnail_url = obtener_miniatura(youtube_url)
        if thumbnail_url:
            print("Miniatura del stream:", thumbnail_url)
        else:
            print("No se pudo obtener la miniatura.")
        
        # Obtener el URL del audio y reproducirlo
        audio_url = obtener_url_audio(youtube_url)
        if audio_url:
            reproducir_audio(audio_url)
        else:
            print("No se pudo obtener el audio de la URL proporcionada.")
    except Exception as e:
        print("Error:", e)
