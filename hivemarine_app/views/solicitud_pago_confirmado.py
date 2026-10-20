import flet as ft
from common import (
    GREEN, TEXT_MUTED, WIZARD_STATE, glass_card, info_row,
    step_header, primary_button, wizard_scaffold, navigate,
)


def solicitud_pago_confirmado_view(page: ft.Page):
    icon_block = ft.Container(
        width=72, height=72,
        bgcolor="#334CD97B",
        border_radius=36,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=40, color=GREEN),
    )

    title = ft.Text("¡Pago confirmado!", size=20, weight=ft.FontWeight.BOLD, color="white",
                     text_align=ft.TextAlign.CENTER)
    desc = ft.Text(
        "Tu servicio está reservado.",
        size=13, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER,
    )

    reserva_card = glass_card(
        ft.Column(
            [
                ft.Text("RESERVA", size=11, weight=ft.FontWeight.BOLD, color=TEXT_MUTED),
                ft.Container(height=6),
                info_row("Número de reserva", WIZARD_STATE.get("numero_reserva", "#4587")),
                info_row("Monto pagado", WIZARD_STATE.get("total", "USD 4,850.00")),
                info_row("Fecha de pago", WIZARD_STATE.get("fecha_pago", "29/05/2025 - 09:12 AM")),
            ],
            spacing=12,
        )
    )

    nota = ft.Text(
        "Recibirás una notificación el día del servicio con los detalles.",
        size=12, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER,
    )

    def go_next(e):
        navigate(page, "solicitud_dia_servicio")

    ver_btn = primary_button("Ver reserva", go_next)

    center_col = ft.Column(
        [
            icon_block,
            ft.Container(height=16),
            title,
            ft.Container(height=6),
            desc,
            ft.Container(height=24),
            reserva_card,
            ft.Container(height=16),
            nota,
            ft.Container(height=24),
            ver_btn,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    content = ft.Column(
        [
            ft.Container(content=step_header(7, "Pago confirmado"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=30),
            ft.Container(content=center_col, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
