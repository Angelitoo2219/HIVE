import flet as ft
from common import (
    GREEN, TEXT_MUTED, WIZARD_STATE, glass_card, info_row,
    step_header, primary_button, wizard_scaffold, navigate,
)


def solicitud_mision_completada_view(page: ft.Page):
    icon_block = ft.Container(
        width=72, height=72,
        bgcolor="#334CD97B",
        border_radius=36,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=40, color=GREEN),
    )

    title = ft.Text("¡Misión completada!", size=20, weight=ft.FontWeight.BOLD, color="white",
                     text_align=ft.TextAlign.CENTER)
    desc = ft.Text(
        "El servicio se ha realizado exitosamente.",
        size=13, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER,
    )

    resultado_card = glass_card(
        ft.Column(
            [
                info_row("Duración total", WIZARD_STATE.get("duracion_total", "36 min")),
                info_row("Casco inspeccionado", WIZARD_STATE.get("casco_inspeccionado", "98%")),
                info_row("Limpieza completada", WIZARD_STATE.get("limpieza_completada", "94%")),
                info_row("Residuos capturados", WIZARD_STATE.get("residuos_capturados", "4.8 kg")),
            ],
            spacing=12,
        )
    )

    def go_next(e):
        navigate(page, "solicitud_recuperacion_drones")

    ver_btn = primary_button("Ver reporte", go_next, icon=ft.Icons.DESCRIPTION_ROUNDED)

    center_col = ft.Column(
        [
            icon_block,
            ft.Container(height=16),
            title,
            ft.Container(height=6),
            desc,
            ft.Container(height=24),
            resultado_card,
            ft.Container(height=24),
            ver_btn,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    content = ft.Column(
        [
            ft.Container(content=step_header(11, "Misión completada"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=30),
            ft.Container(content=center_col, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
