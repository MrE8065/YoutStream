import flet as ft
from youtube import obtener_url_audio, reproducir_audio, obtener_miniatura

def main(page: ft.Page):
    page.title = "YoutStream"
    page.window.resizable = False
    page.window.width = 400
    page.window.height = 600
    page.window.alignment = ft.alignment.bottom_right
    
    image = ft.Image(src=None, visible=False)
    placeholder_text = ft.Text("A la espera de un stream...", visible=True)
    
    def update_image(e):
        url = url_input.value
        if url:
            image.src = obtener_miniatura(url)
            image.visible = True
            image.update()
            placeholder_text.visible = False
            placeholder_text.update()
        page.close(dialog)
    
    url_input = ft.TextField(hint_text="Stream de Youtube...", on_submit=update_image)
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Selecciona un stream"),
        content=url_input,
        actions=[
            ft.TextButton("Aceptar", on_click=update_image),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    things = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Nombre del stream"),
                ft.ElevatedButton("Abrir diálogo", on_click=lambda e: page.open(dialog)),
                placeholder_text,
                image,
                ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS_ROUNDED),
                        ft.IconButton(icon=ft.Icons.PLAY_CIRCLE_FILL_ROUNDED),
                        ft.IconButton(icon=ft.Icons.SKIP_NEXT_ROUNDED),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        alignment=ft.alignment.center,
        expand=True,
        padding=10,
        border=ft.border.all(1, ft.Colors.GREEN)
    )
    
    page.add(things)
    
ft.app(main)
