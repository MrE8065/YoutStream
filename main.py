import flet as ft
import os
from youtube import obtener_audio, obtener_miniatura, obtener_titulo, reproducir_audio, pausar_reanudar_audio, detener_audio

user = os.getlogin()
file_path = f"C:/Users/{user}/Documents/YoutStream.txt" # Ruta del archivo de links guardados

def main(page: ft.Page):
    page.title = "YoutStream"
    page.window.resizable = False
    page.window.maximizable = False
    page.window.width = 400
    page.window.height = 400
    page.window.alignment = ft.alignment.bottom_right
    
    image = ft.Image(src=None, visible=False)
    placeholder_text = ft.Text("A la espera de un stream...", visible=True) # Placeholder cuando no hay una imagen cargada
    
    audio_url = None # Variable global para almacenar la URL del audio
    
    def get_stream(url, nombre=None):
        nonlocal audio_url
        if url:
            detener_audio() # Detener cualquier audio en reproducción antes de obtener otro
            
            image.src = obtener_miniatura(url) # Obtiene la miniatura del video
            image.visible = True # Muestra la imagen
            placeholder_text.visible = False # Esconde el placeholder
            
            if not nombre:
                nombre = obtener_titulo(url) # Obtener el título real del stream
            
            page.title = nombre # Cambiar el título de la ventana al nombre del stream
            
            audio_url = obtener_audio(url) # Guarda la nueva URL del audio
            play_button.tooltip = "Reproducir/Pausar" # Cambia el tooltip del botón de reproducción
            play_button.disabled = False # Activa el botón de reproducción
        page.update()
    
    def get_direct_stream(e):
        url = e # Extraer la URL almacenada en el textfield
        get_stream(url)
        page.update()
        page.close(dialog)
        
    def get_stream_guardado(e):
        nombre, url = e.control.data # Extraer la URL almacenada en el botón
        get_stream(url, nombre)
        page.update()
        page.close(guardados_dialog)
    
    def toggle_audio(e):
        if audio_url:
            if play_button.icon == ft.Icons.PLAY_CIRCLE_ROUNDED:
                reproducir_audio(audio_url)
                play_button.icon = ft.Icons.PAUSE_CIRCLE_ROUNDED
            else:
                pausar_reanudar_audio()
                play_button.icon = ft.Icons.PLAY_CIRCLE_ROUNDED
        page.update()
    
    url_input = ft.TextField(hint_text="Stream de Youtube...", on_submit=lambda e: get_direct_stream(url_input.value))
    
    dialog_button = ft.IconButton(icon=ft.Icons.MENU_ROUNDED, on_click=lambda e: page.open(dialog))
    
    guardados_button = ft.IconButton(icon=ft.Icons.LIBRARY_BOOKS_ROUNDED, on_click=lambda e: page.open(guardados_dialog))
    
    def cargar_guardados():
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("""#Pega aquí los links que quieras guardar

#Sigue este estilo
#<nombre a mostrar>|<link al video o directo>

Lofi Girl-hip hop|https://www.youtube.com/live/jfKfPfyJRdk?si=r-nEogeG0hyLa0si""")
        
        guardados = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for linea in file:
                linea = linea.strip()
                if linea and not linea.startswith("#") and "|" in linea:
                    nombre, url = linea.split("|", 1)
                    boton = ft.TextButton(nombre, style=ft.ButtonStyle(color=ft.Colors.GREY_300), data=(nombre, url), on_click=get_stream_guardado)
                    guardados.append(boton)
        
        return guardados if guardados else [ft.Text("No hay nada guardado")]
    
    def abrir_guardados(e):
        try:
            os.startfile(file_path) # Solo funciona en Windows
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            page.snack_bar.open = True
            page.update()
    
    def recargar_lista(e):
        guardados_list.controls = cargar_guardados() # Vuelve a cargar las opciones de la lista
        page.update()
    
    guardados_list = ft.ListView(controls=cargar_guardados(), expand=1, spacing=10)
    
    guardados_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Seleccionar un stream guardado"),
        content=guardados_list,
        actions=[
            ft.TextButton("Guardados", on_click=abrir_guardados),
            ft.IconButton(icon=ft.Icons.REPLAY_ROUNDED, on_click=recargar_lista),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(guardados_dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER
    )
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cargar un stream"),
        content=url_input,
        actions=[
            ft.TextButton("Aceptar", on_click=lambda e: get_direct_stream(url_input.value)),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    
    topbar = ft.Row(
        controls=[guardados_button, dialog_button],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    
    play_button = ft.IconButton(icon=ft.Icons.PLAY_CIRCLE_FILL_ROUNDED, icon_size=35, tooltip="Establece un stream primero", disabled=True, on_click=toggle_audio)
    
    control_buttons = ft.Row(
        controls=[
            play_button
        ]
    )
    
    bottom_buttons = ft.Row(
        controls=[control_buttons],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    things = ft.Container(
        content=ft.Column(
            controls=[
                topbar,
                placeholder_text,
                image,
                bottom_buttons
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        alignment=ft.alignment.center,
        expand=True,
    )
    
    page.add(things)
    
ft.app(main)