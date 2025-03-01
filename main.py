import flet as ft
from youtube import obtener_url_audio, reproducir_audio, obtener_miniatura, obtener_titulo

def main(page: ft.Page):
    page.title = "YoutStream"
    page.window.resizable = False
    page.window.width = 400
    page.window.height = 400
    page.window.alignment = ft.alignment.bottom_right
    
    image = ft.Image(src=None, visible=False)
    placeholder_text = ft.Text("A la espera de un stream...", visible=True)
    
    def get_stream(e):
        url = url_input.value
        if url:
            image.src = obtener_miniatura(url) # Obtener la miniatura del video
            image.visible = True # Mostrar la imagen
            placeholder_text.visible = False # Esconder el placeholder
            titulo = obtener_titulo(url)  # Obtener el título del video
            page.title = titulo  # Cambiar el título de la ventana
        page.close(dialog) # Cierra el diálogo
        page.update() # Actualiza la página para mostrar los cambios
    
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
    
    control_buttons=ft.Row(
        controls=[
            #ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS_ROUNDED, icon_size=35),
            ft.IconButton(icon=ft.Icons.PLAY_CIRCLE_FILL_ROUNDED, icon_size=35),
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
