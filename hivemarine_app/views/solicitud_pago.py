import flet as ft
from common import (
    YELLOW, TEXT_MUTED, CARD_GLASS, CARD_BORDER,
    WIZARD_STATE, glass_card, info_row,
    step_header, primary_button, wizard_scaffold, navigate,
)

PAYMENT_METHODS = [
    {"id": "tarjeta", "icon": ft.Icons.CREDIT_CARD_ROUNDED, "label": "Tarjeta de crédito"},
    {"id": "transferencia", "icon": ft.Icons.ACCOUNT_BALANCE_ROUNDED, "label": "Transferencia bancaria"},
    {"id": "paypal", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED, "label": "PayPal"},
]


def solicitud_pago_view(page: ft.Page):
    selected = ["tarjeta"]
    row_refs = {m["id"]: ft.Ref[ft.Container]() for m in PAYMENT_METHODS}
    radio_refs = {m["id"]: ft.Ref[ft.Icon]() for m in PAYMENT_METHODS}

    def paint_rows():
        for m in PAYMENT_METHODS:
            is_selected = selected[0] == m["id"]
            row_refs[m["id"]].current.border = ft.Border.all(1.5 if is_selected else 1,
                                                               YELLOW if is_selected else CARD_BORDER)
            radio_refs[m["id"]].current.name = (
                ft.Icons.RADIO_BUTTON_CHECKED_ROUNDED if is_selected else ft.Icons.RADIO_BUTTON_UNCHECKED
            )
            radio_refs[m["id"]].current.color = YELLOW if is_selected else TEXT_MUTED

    def select_method(method_id: str):
        def handler(e):
            selected[0] = method_id
            paint_rows()
            page.update()
        return handler

    def payment_row(m: dict):
        is_selected = selected[0] == m["id"]
        return ft.Container(
            ref=row_refs[m["id"]],
            content=ft.Row(
                [
                    ft.Icon(m["icon"], color="white", size=20),
                    ft.Text(m["label"], size=14, color="white", expand=True),
                    ft.Icon(
                        ft.Icons.RADIO_BUTTON_CHECKED_ROUNDED if is_selected else ft.Icons.RADIO_BUTTON_UNCHECKED,
                        color=YELLOW if is_selected else TEXT_MUTED, size=20,
                        ref=radio_refs[m["id"]],
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=CARD_GLASS,
            border=ft.Border.all(1.5 if is_selected else 1, YELLOW if is_selected else CARD_BORDER),
            border_radius=12,
            padding=ft.Padding(14, 12, 14, 12),
            on_click=select_method(m["id"]),
            ink=True,
        )

    resumen_card = glass_card(
        ft.Column(
            [
                ft.Text("RESUMEN DEL SERVICIO", size=11, weight=ft.FontWeight.BOLD, color=TEXT_MUTED),
                ft.Container(height=6),
                info_row("Barco", WIZARD_STATE.get("barco", "—")),
                info_row("Servicio", WIZARD_STATE.get("servicio_nombre", "—")),
                info_row("Fecha", WIZARD_STATE.get("fecha", "—")),
                info_row("Ventana", WIZARD_STATE.get("ventana", "—")),
                info_row("Drones asignados", str(WIZARD_STATE.get("drones_asignados", 20))),
                ft.Divider(color=CARD_BORDER, height=18),
                info_row("Total a pagar", WIZARD_STATE.get("total", "USD 0.00"), value_color=YELLOW),
            ],
            spacing=10,
        )
    )

    metodo_col = ft.Column(
        [
            ft.Text("MÉTODO DE PAGO", size=11, weight=ft.FontWeight.BOLD, color=TEXT_MUTED),
            ft.Container(height=8),
            *[payment_row(m) for m in PAYMENT_METHODS],
        ],
        spacing=10,
    )

    def pagar(e):
        WIZARD_STATE["metodo_pago"] = selected[0]
        # Aquí se conectaría el cobro real (pasarela de pago). Por ahora
        # confirma el pago y regresa a Inicio.
        print(f"Pago procesado con: {selected[0]} — {WIZARD_STATE.get('total')}")
        navigate(page, "solicitud_pago_confirmado")

    pagar_btn = primary_button(f"Pagar {WIZARD_STATE.get('total', '')}", pagar)

    seguro_row = ft.Row(
        [
            ft.Icon(ft.Icons.LOCK_ROUNDED, size=14, color=TEXT_MUTED),
            ft.Text("Pago 100% seguro", size=12, color=TEXT_MUTED),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=6,
    )

    content = ft.Column(
        [
            ft.Container(content=step_header(6, "Realizar pago"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=resumen_card, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=metodo_col, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=20),
            ft.Container(content=pagar_btn, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=10),
            seguro_row,
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
