import flet as ft
from common import (
    GREEN, TEXT_MUTED, WIZARD_STATE, glass_card, info_row,
    step_header, outlined_button, wizard_scaffold, navigate,
)


def solicitud_confirmado_view(page: ft.Page):
    icon_block = ft.Container(
        width=72, height=72,
        bgcolor="#334CD97B",
        border_radius=36,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=40, color=GREEN),
    )

    title = ft.Text("¡Servicio confirmado!", size=20, weight=ft.FontWeight.BOLD, color="white",
                     text_align=ft.TextAlign.CENTER)
    desc = ft.Text(
        "Hemos asignado un equipo para tu servicio.",
        size=13, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER,
    )

    equipo_card = glass_card(
        ft.Column(
            [
                ft.Text("EQUIPO ASIGNADO", size=11, weight=ft.FontWeight.BOLD, color=TEXT_MUTED),
                ft.Container(height=6),
                info_row("Equipo", "HiveMarine · HM-03"),
                info_row("Drones asignados", f"{WIZARD_STATE.get('drones_asignados', 20)} drones"),
                info_row("Fecha", WIZARD_STATE.get("fecha", "—")),
                info_row("Ventana", WIZARD_STATE.get("ventana", "—")),
            ],
            spacing=12,
        )
    )

    def go_next(e):
        navigate(page, "solicitud_pago")

    ver_btn = outlined_button("Ver detalles", go_next)

    center_col = ft.Column(
        [
            icon_block,
            ft.Container(height=16),
            title,
            ft.Container(height=6),
            desc,
            ft.Container(height=24),
            equipo_card,
            ft.Container(height=24),
            ver_btn,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    content = ft.Column(
        [
            ft.Container(content=step_header(5, "Servicio confirmado"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=30),
            ft.Container(content=center_col, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
