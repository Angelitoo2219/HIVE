import flet as ft
from common import (
    TEXT_MUTED, WIZARD_STATE, glass_card, info_row,
    step_header, primary_button, wizard_scaffold, navigate,
)

# Foto de equipo/drones (placeholder). Para usar la tuya: guárdala en
# assets/images/entrega.jpg y cambia FOTO_URL por src local "images/entrega.jpg".
FOTO_URL = "https://images.unsplash.com/photo-1508614999368-9260051292e5?w=1200&q=80"


def solicitud_entrega_drones_view(page: ft.Page):
    foto = ft.Container(
        height=180,
        border_radius=16,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Image(src=FOTO_URL, fit=ft.BoxFit.COVER),
    )

    desc = ft.Text(
        "Nuestro equipo llega al punto de encuentro y prepara los drones para el despliegue.",
        size=13, color=TEXT_MUTED,
    )

    detalle_card = glass_card(
        ft.Column(
            [
                info_row("Drones entregados", f"{WIZARD_STATE.get('drones_asignados', 20)} drones"),
                info_row("Hora de entrega", WIZARD_STATE.get("hora_entrega", "14:18")),
            ],
            spacing=12,
        )
    )

    def go_next(e):
        navigate(page, "solicitud_mision_progreso")

    continuar_btn = primary_button("Iniciar misión", go_next, icon=ft.Icons.PLAY_ARROW_ROUNDED)

    content = ft.Column(
        [
            ft.Container(content=step_header(9, "Entrega de drones"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=foto, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=14),
            ft.Container(content=desc, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=14),
            ft.Container(content=detalle_card, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=20),
            ft.Container(content=continuar_btn, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
