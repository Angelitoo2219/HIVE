import os
import sys

# Bootstrap robusto: al ejecutar el script directamente, el directorio padre
# del paquete debe quedar en sys.path para que `hivemarine_app` pueda importarse
# correctamente desde cualquier entorno (terminal, botón ▶, depurador, tareas).
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import flet as ft
from hivemarine_app.views.inicio import inicio_view


def main(page: ft.Page):
    # --- Configuración general de la app ---
    page.title = "HIVEMARINE"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#060A14"
    page.padding = 0
    page.spacing = 0

    # Tamaño tipo móvil (sintaxis estable, sin el bug de page.window.*)
    page.window_width = 390
    page.window_height = 844
    page.window_resizable = False

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # --- Pantalla inicial ---
    page.add(inicio_view(page))
    page.update()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    ft.run(main, host="0.0.0.0", port=port, view=ft.AppView.WEB_BROWSER)
