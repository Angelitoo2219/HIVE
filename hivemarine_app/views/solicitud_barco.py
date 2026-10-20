import flet as ft
from common import (
    YELLOW, TEXT_MUTED, CARD_GLASS, CARD_BORDER,
    WIZARD_STATE, step_header, primary_button, wizard_scaffold, navigate,
)

BOATS = [
    {"name": "Neopanamax 01", "status": "En tránsito · ETA 14:30"},
    {"name": "Neopanamax 02", "status": "ETA 16:20"},
    {"name": "Panamax 01", "status": "ETA 18:45"},
    {"name": "Neopanamax 03", "status": "Disponible mañana"},
]


def solicitud_barco_view(page: ft.Page):
    selected = [WIZARD_STATE.get("barco", BOATS[0]["name"])]
    card_refs = {b["name"]: ft.Ref[ft.Container]() for b in BOATS}
    check_refs = {b["name"]: ft.Ref[ft.Icon]() for b in BOATS}

    def paint_cards():
        for b in BOATS:
            is_selected = selected[0] == b["name"]
            c = card_refs[b["name"]].current
            c.bgcolor = "#33E8B84B" if is_selected else CARD_GLASS
            c.border = ft.Border.all(1.5 if is_selected else 1, YELLOW if is_selected else CARD_BORDER)
            check_refs[b["name"]].current.visible = is_selected

    def select_boat(name: str):
        def handler(e):
            selected[0] = name
            paint_cards()
            page.update()
        return handler

    def boat_card(b: dict):
        is_selected = selected[0] == b["name"]
        return ft.Container(
            ref=card_refs[b["name"]],
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.DIRECTIONS_BOAT_ROUNDED, color="white", size=22),
                    ft.Column(
                        [
                            ft.Text(b["name"], size=14, weight=ft.FontWeight.W_600, color="white"),
                            ft.Text(b["status"], size=12, color=TEXT_MUTED),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE_ROUNDED, color=YELLOW, size=20,
                        ref=check_refs[b["name"]], visible=is_selected,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#33E8B84B" if is_selected else CARD_GLASS,
            border=ft.Border.all(1.5 if is_selected else 1, YELLOW if is_selected else CARD_BORDER),
            border_radius=12,
            padding=ft.Padding(14, 12, 14, 12),
            on_click=select_boat(b["name"]),
            ink=True,
        )

    def filter_boats(query: str):
        boats_list_col.controls = [
            boat_card(b) for b in BOATS if query.lower() in b["name"].lower()
        ]
        page.update()

    search_field = ft.TextField(
        hint_text="Buscar barco...",
        hint_style=ft.TextStyle(color=TEXT_MUTED),
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        color="white",
        bgcolor=CARD_GLASS,
        border_color=CARD_BORDER,
        focused_border_color=YELLOW,
        border_radius=12,
        height=48,
        content_padding=ft.Padding(12, 8, 12, 8),
        on_change=lambda e: filter_boats(e.control.value or ""),
    )

    boats_list_col = ft.Column([boat_card(b) for b in BOATS], spacing=12)

    def go_next(e):
        WIZARD_STATE["barco"] = selected[0]
        navigate(page, "solicitud_detalles")

    continue_btn = primary_button("Continuar", go_next, icon=ft.Icons.ARROW_FORWARD_ROUNDED)

    content = ft.Column(
        [
            ft.Container(content=step_header(2, "Selecciona tu barco"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=search_field, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=boats_list_col, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=20),
            ft.Container(content=continue_btn, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
