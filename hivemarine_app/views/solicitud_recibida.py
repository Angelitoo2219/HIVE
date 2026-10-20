import flet as ft
from common import (
    BLUE, TEXT_MUTED, glass_card, info_row,
    step_header, outlined_button, wizard_scaffold, navigate,
)


def solicitud_recibida_view(page: ft.Page):
    icon_block = ft.Container(
        width=72, height=72,
        bgcolor="#3333A0FF",
        border_radius=36,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.ASSIGNMENT_TURNED_IN_ROUNDED, size=36, color=BLUE),
    )

    title = ft.Text("¡Solicitud recibida!", size=20, weight=ft.FontWeight.BOLD, color="white",
                     text_align=ft.TextAlign.CENTER)
    desc = ft.Text(
        "Estamos revisando tu solicitud y verificando disponibilidad.",
        size=13, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER,
    )

    info_card = glass_card(
        ft.Column(
            [
                info_row("Posición en la cola", "#2"),
                info_row("Drones disponibles", "18"),
                info_row("Tiempo estimado de espera", "18 min"),
            ],
            spacing=12,
        )
    )

    def go_next(e):
        navigate(page, "solicitud_confirmado")

    ver_btn = outlined_button("Ver mis solicitudes", go_next)

    center_col = ft.Column(
        [
            icon_block,
            ft.Container(height=16),
            title,
            ft.Container(height=6),
            desc,
            ft.Container(height=24),
            info_card,
            ft.Container(height=24),
            ver_btn,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    content = ft.Column(
        [
            ft.Container(content=step_header(4, "Solicitud recibida"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=30),
            ft.Container(content=center_col, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
