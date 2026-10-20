import flet as ft
from common import (
    YELLOW, GREEN, TEXT_MUTED, CARD_BORDER,
    WIZARD_STATE, glass_card, info_row,
    step_header, primary_button, wizard_scaffold, navigate,
)


def _mini_map():
    """Mapa simplificado que muestra el trayecto del equipo hacia la esclusa."""
    return ft.Container(
        height=90,
        bgcolor="#0D1730",
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=14,
        padding=10,
        content=ft.Stack(
            [
                ft.Container(left=10, top=44, right=10, height=2, bgcolor="#40FFFFFF"),
                ft.Container(left=10, top=40, width=10, height=10, border_radius=5, bgcolor=GREEN),
                ft.Container(
                    left=0, top=0, right=0, bottom=0,
                    content=ft.Icon(ft.Icons.DIRECTIONS_BOAT_ROUNDED, color=YELLOW, size=18),
                    alignment=ft.Alignment.CENTER_RIGHT,
                ),
            ],
        ),
    )


def solicitud_dia_servicio_view(page: ft.Page):
    proximo_label = ft.Text("PRÓXIMO SERVICIO", size=11, weight=ft.FontWeight.BOLD, color=TEXT_MUTED)
    fecha_text = ft.Text(WIZARD_STATE.get("fecha", "29/05/2025"), size=16,
                          weight=ft.FontWeight.BOLD, color="white")

    detalle_card = glass_card(
        ft.Column(
            [
                info_row("Barco", WIZARD_STATE.get("barco", "Neopanamax 01")),
                info_row("Esclusa", WIZARD_STATE.get("esclusa", "Miraflores")),
                info_row("Ventana de tránsito", WIZARD_STATE.get("ventana", "14:00 - 16:00")),
                info_row("Hora estimada de llegada", WIZARD_STATE.get("hora_llegada", "14:15")),
                info_row("Estado", "En camino", value_color=YELLOW),
            ],
            spacing=12,
        )
    )

    aviso = ft.Text(
        "Nuestro equipo va en camino a la esclusa.",
        size=13, color=TEXT_MUTED,
    )

    entrega_card = glass_card(
        ft.Column(
            [
                info_row("Drones asignados", f"{WIZARD_STATE.get('drones_asignados', 20)} drones"),
                info_row("Hora de entrega", WIZARD_STATE.get("hora_entrega", "14:18")),
            ],
            spacing=12,
        )
    )

    def go_next(e):
        navigate(page, "solicitud_entrega_drones")

    continuar_btn = primary_button("Entregados y listos", go_next, icon=ft.Icons.CHECK_ROUNDED)

    content = ft.Column(
        [
            ft.Container(content=step_header(8, "Día del servicio"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=proximo_label, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(content=fecha_text, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=14),
            ft.Container(content=detalle_card, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=14),
            ft.Container(content=aviso, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=14),
            ft.Container(content=_mini_map(), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=14),
            ft.Container(content=entrega_card, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=20),
            ft.Container(content=continuar_btn, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
