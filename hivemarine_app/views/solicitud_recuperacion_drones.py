import flet as ft
from common import (
    GREEN, TEXT_MUTED, WIZARD_STATE, glass_card, info_row,
    step_header, primary_button, wizard_scaffold, navigate,
)

# Foto de recuperación (placeholder). Para usar la tuya: guárdala en
# assets/images/recuperacion.jpg y cambia FOTO_URL por src local "images/recuperacion.jpg".
FOTO_URL = "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200&q=80"


def solicitud_recuperacion_drones_view(page: ft.Page):
    foto = ft.Container(
        height=160,
        border_radius=16,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Image(src=FOTO_URL, fit=ft.BoxFit.COVER),
    )

    desc = ft.Text(
        "Recuperamos todos los drones utilizados y verificamos que estén en buen estado.",
        size=13, color=TEXT_MUTED,
    )

    total_drones = WIZARD_STATE.get("drones_asignados", 20)
    detalle_card = glass_card(
        ft.Column(
            [
                info_row("Estado recuperado", f"{total_drones}/{total_drones}"),
                info_row("Hora de recuperación", WIZARD_STATE.get("hora_recuperacion", "15:05")),
                info_row("Estado", "Recuperados", value_color=GREEN),
            ],
            spacing=12,
        )
    )

    def go_next(e):
        navigate(page, "inicio")

    finalizar_btn = primary_button("Finalizar", go_next, icon=ft.Icons.HOME_ROUNDED)

    content = ft.Column(
        [
            ft.Container(content=step_header(12, "Recuperación de drones"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=foto, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=14),
            ft.Container(content=desc, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=14),
            ft.Container(content=detalle_card, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=20),
            ft.Container(content=finalizar_btn, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
