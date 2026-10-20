import flet as ft
from common import (
    YELLOW, GREEN, BLUE, TEXT_MUTED,
    CARD_GLASS, CARD_BORDER,
    WIZARD_STATE, step_header, primary_button, wizard_scaffold, navigate,
)

SERVICES = [
    {
        "id": "limpieza",
        "icon": ft.Icons.CLEANING_SERVICES_ROUNDED,
        "icon_bg": GREEN,
        "title": "Limpieza del casco",
        "desc": "Eliminamos bioincrustación y residuos adheridos.",
    },
    {
        "id": "inspeccion",
        "icon": ft.Icons.TRAVEL_EXPLORE_ROUNDED,
        "icon_bg": BLUE,
        "title": "Inspección submarina",
        "desc": "Revisión completa del casco y detección de anomalías.",
    },
    {
        "id": "combo",
        "icon": ft.Icons.WORKSPACE_PREMIUM_ROUNDED,
        "icon_bg": YELLOW,
        "title": "Limpieza + inspección",
        "desc": "Limpieza completa más inspección y reporte.",
    },
]


def solicitudes_view(page: ft.Page):
    selected = [WIZARD_STATE.get("servicio_id", "combo")]
    card_refs = {s["id"]: ft.Ref[ft.Container]() for s in SERVICES}

    def paint_cards():
        for s in SERVICES:
            is_selected = selected[0] == s["id"]
            c = card_refs[s["id"]].current
            c.bgcolor = "#33E8B84B" if is_selected else CARD_GLASS
            c.border = ft.Border.all(1.5 if is_selected else 1, YELLOW if is_selected else CARD_BORDER)

    def select_service(service_id: str):
        def handler(e):
            selected[0] = service_id
            paint_cards()
            page.update()
        return handler

    def service_card(s: dict):
        is_selected = selected[0] == s["id"]
        icon_badge = ft.Container(
            width=44, height=44,
            bgcolor=s["icon_bg"],
            border_radius=12,
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(s["icon"], color="black", size=22),
        )
        text_col = ft.Column(
            [
                ft.Text(s["title"], size=15, weight=ft.FontWeight.W_600, color="white"),
                ft.Text(s["desc"], size=12, color=TEXT_MUTED),
            ],
            spacing=2,
            expand=True,
        )
        return ft.Container(
            ref=card_refs[s["id"]],
            content=ft.Row([icon_badge, text_col], spacing=14,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#33E8B84B" if is_selected else CARD_GLASS,
            blur=14,
            border=ft.Border.all(1.5 if is_selected else 1, YELLOW if is_selected else CARD_BORDER),
            border_radius=14,
            padding=ft.Padding(14, 14, 14, 14),
            on_click=select_service(s["id"]),
            ink=True,
            shadow=ft.BoxShadow(blur_radius=16, color="#40000000", offset=ft.Offset(0, 6)),
        )

    subtitle = ft.Text("¿Qué servicio necesitas?", size=22, weight=ft.FontWeight.BOLD, color="white")
    cards_col = ft.Column([service_card(s) for s in SERVICES], spacing=14)

    def go_next(e):
        chosen = next(s for s in SERVICES if s["id"] == selected[0])
        WIZARD_STATE["servicio_id"] = chosen["id"]
        WIZARD_STATE["servicio_nombre"] = chosen["title"]
        navigate(page, "solicitud_barco")

    continue_btn = primary_button("Continuar", go_next, icon=ft.Icons.ARROW_FORWARD_ROUNDED)

    content = ft.Column(
        [
            ft.Container(content=step_header(1, "Solicitar servicio"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=18),
            ft.Container(content=subtitle, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=cards_col, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=20),
            ft.Container(content=continue_btn, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
