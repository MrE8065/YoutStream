import flet as ft
from youtube import obtener_audio, obtener_miniatura, obtener_titulo, reproducir_audio, pausar_reanudar_audio, detener_audio

def main(page: ft.Page):
    page.title = "YoutStream"
    page.window.resizable = False
    page.window.width = 400
    page.window.height = 400
    page.window.alignment = ft.alignment.bottom_right
    
    image = ft.Image(src=None, visible=False)
    placeholder_text = ft.Text("A la espera de un stream...", visible=True)
    
    audio_url = None  # Variable global para almacenar la URL del audio
    
    def get_stream(e):
        nonlocal audio_url
        url = url_input.value
        if url:
            detener_audio()  # Detener cualquier audio en reproducción antes de obtener otro
            
            image.src = obtener_miniatura(url)
            image.visible = True
            placeholder_text.visible = False
            page.title = obtener_titulo(url)
            
            audio_url = obtener_audio(url)  # Guarda la nueva URL del audio
            print(audio_url)
            play_button.tooltip = "Reproducir/Pausar"
            play_button.disabled = False

        page.close(dialog)
        page.update()

    def toggle_audio(e):
        if audio_url:
            if play_button.icon == ft.Icons.PLAY_CIRCLE_FILL_ROUNDED:
                reproducir_audio(audio_url)
                play_button.icon = ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
            else:
                pausar_reanudar_audio()
                play_button.icon = ft.Icons.PLAY_CIRCLE_FILL_ROUNDED
        page.update()
    
    url_input = ft.TextField(hint_text="Stream de Youtube...", on_submit=get_stream)
    
    dialog_button = ft.IconButton(icon=ft.Icons.MENU_ROUNDED, on_click=lambda e: page.open(dialog))
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Selecciona un stream"),
        content=url_input,
        actions=[
            ft.TextButton("Aceptar", on_click=get_stream),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    
    topbar = ft.Row(
        controls=[dialog_button],
        alignment=ft.MainAxisAlignment.END
    )
    
    play_button=ft.IconButton(icon=ft.Icons.PLAY_CIRCLE_FILL_ROUNDED, icon_size=35, tooltip="Establece un stream primero", disabled=True, on_click=toggle_audio)
    
    control_buttons=ft.Row(
        controls=[
            #ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS_ROUNDED, icon_size=35),
            play_button
            #ft.IconButton(icon=ft.Icons.SKIP_NEXT_ROUNDED, icon_size=35)
        ]
    )
    
    bottom_buttons=ft.Row(
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
