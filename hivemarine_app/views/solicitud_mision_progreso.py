import flet as ft
from common import (
    GREEN, RED, ORANGE, TEXT_MUTED,
    glass_card, step_header, primary_button, wizard_scaffold, navigate,
)


def _progress_ring(value: float, color: str):
    pct_text = f"{int(value * 100)}%"
    return ft.Stack(
        [
            ft.ProgressRing(value=value, width=110, height=110, stroke_width=10,
                             color=color, bgcolor="#22FFFFFF"),
            ft.Container(
                width=110, height=110, alignment=ft.Alignment.CENTER,
                content=ft.Text(pct_text, size=26, weight=ft.FontWeight.BOLD, color="white"),
            ),
        ],
        width=110, height=110,
    )


def _legend_item(color: str, pct: str, label: str):
    return ft.Row(
        [
            ft.Container(width=10, height=10, bgcolor=color, border_radius=3),
            ft.Text(f"{pct}  {label}", size=13, color="white"),
        ],
        spacing=8,
    )


def solicitud_mision_progreso_view(page: ft.Page):
    progreso_card = glass_card(
        ft.Column(
            [
                ft.Text("PROGRESO TOTAL", size=11, weight=ft.FontWeight.BOLD, color=TEXT_MUTED),
                ft.Container(height=10),
                ft.Row([_progress_ring(0.67, GREEN)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=16),
                _legend_item(RED, "23%", "Sin limpiar"),
                ft.Container(height=6),
                _legend_item(ORANGE, "17%", "En progreso"),
                ft.Container(height=6),
                _legend_item(GREEN, "60%", "Completado"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    def go_next(e):
        navigate(page, "solicitud_mision_completada")

    ver_btn = primary_button("Ver misión en tiempo real", go_next, icon=ft.Icons.VISIBILITY_ROUNDED)

    content = ft.Column(
        [
            ft.Container(content=step_header(10, "Misión en progreso"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=18),
            ft.Container(content=progreso_card, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=20),
            ft.Container(content=ver_btn, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
