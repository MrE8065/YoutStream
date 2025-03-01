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
import vlc
import yt_dlp

reproductor = None
ultima_url = None

def obtener_titulo(youtube_url):
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
        # Retorna la URL del stream de audio
        return info.get('title')

def obtener_audio(youtube_url):
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
        # Retorna la URL de la miniatura
        return info.get('thumbnail')

def reproducir_audio(url_audio):
    """
    Reproduce el audio o reanuda si ya es el mismo.
    """
    global reproductor, ultima_url
    
    if reproductor and ultima_url == url_audio:
        # Si el audio ya está cargado, solo lo reanuda
        reproductor.play()
        print("Reanudando audio...")
        return
    
    detener_audio()  # Si es una nueva URL, detiene el audio anterior

    # Crear reproductor VLC
    instancia = vlc.Instance()
    reproductor = instancia.media_player_new()
    media = instancia.media_new(url_audio)
    reproductor.set_media(media)
    
    reproductor.play()
    ultima_url = url_audio  # Guarda la nueva URL activa
    print("Reproduciendo nuevo audio...")
    
def pausar_reanudar_audio():
    """
    Pausa o reanuda el audio sin perder la posición.
    """
    global reproductor
    if reproductor:
        estado = reproductor.get_state()
        if estado == vlc.State.Playing:
            reproductor.pause()
            print("Audio pausado.")
        elif estado == vlc.State.Paused:
            reproductor.play()
            print("Audio reanudado.")

def detener_audio():
    """
    Detiene el audio y libera recursos.
    """
    global reproductor, ultima_url
    if reproductor:
        reproductor.stop()
        reproductor = None
        ultima_url = None  # Borra la última URL activa
        print("Audio detenido.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python reproducir_audio_youtube.py <URL_de_Youtube>")
        sys.exit(1)
    youtube_url = sys.argv[1]
    
    try:
        # Obtener y mostrar el titulo
        title = obtener_titulo(youtube_url)
        if title:
            print("Titulo del stream:", title)
        else:
            print("No se pudo obtener el titulo")
        
        # Obtener y mostrar la miniatura
        thumbnail_url = obtener_miniatura(youtube_url)
        if thumbnail_url:
            print("Miniatura del stream:", thumbnail_url)
        else:
            print("No se pudo obtener la miniatura.")
        
        # Obtener el URL del audio y reproducirlo
        audio_url = obtener_audio(youtube_url)
        if audio_url:
            reproducir_audio(audio_url)
        else:
            print("No se pudo obtener el audio de la URL proporcionada.")
    except Exception as e:
        print("Error:", e)
