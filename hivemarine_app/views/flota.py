import flet as ft
from common import (
    YELLOW, GREEN, RED, ORANGE, TEXT_MUTED,
    CARD_GLASS, CARD_BORDER, BG,
    status_bar, bottom_nav, navigate,
)

DRONES = [
    {"id": "HM-01", "estado": "Limpiando", "dot": GREEN, "zona": "Zona B-17",
     "bateria": 82, "categoria": "activo"},
    {"id": "HM-02", "estado": "En progreso", "dot": GREEN, "zona": "Zona C-05",
     "bateria": 74, "categoria": "activo"},
    {"id": "HM-03", "estado": "Limpiando", "dot": GREEN, "zona": "Zona A-12",
     "bateria": 68, "categoria": "activo"},
    {"id": "HM-04", "estado": "En progreso", "dot": GREEN, "zona": "Zona A-09",
     "bateria": 53, "categoria": "activo"},
    {"id": "HM-05", "estado": "Regresando a base", "dot": ORANGE, "zona": None,
     "bateria": 21, "categoria": "activo"},
    {"id": "HM-06", "estado": "En mantenimiento", "dot": RED, "zona": None,
     "bateria": None, "categoria": "mantenimiento"},
    {"id": "HM-07", "estado": "En base", "dot": TEXT_MUTED, "zona": None,
     "bateria": 100, "categoria": "base"},
    {"id": "HM-08", "estado": "En base", "dot": TEXT_MUTED, "zona": None,
     "bateria": 100, "categoria": "base"},
]


def _flota_top_bar(page: ft.Page):
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_BACK, color="white", size=22),
                    on_click=lambda e: navigate(page, "inicio"),
                    ink=True,
                    border_radius=20,
                    padding=6,
                ),
                ft.Text("Drones en misión", size=17, weight=ft.FontWeight.W_600, color="white"),
                ft.Container(
                    content=ft.Icon(ft.Icons.OPEN_IN_FULL_ROUNDED, color="white", size=18),
                    bgcolor=CARD_GLASS,
                    border=ft.Border.all(1, CARD_BORDER),
                    border_radius=10,
                    padding=8,
                    on_click=lambda e: navigate(page, "mapa"),
                    ink=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.Padding(left=12, right=12, top=6, bottom=0),
    )


def _battery_view(pct):
    if pct is None:
        return ft.Text("—", size=14, color=TEXT_MUTED)
    if pct > 50:
        color, icon = GREEN, ft.Icons.BATTERY_FULL_ROUNDED
    elif pct > 20:
        color, icon = ORANGE, ft.Icons.BATTERY_5_BAR_ROUNDED
    else:
        color, icon = RED, ft.Icons.BATTERY_ALERT_ROUNDED
    return ft.Row(
        [
            ft.Text(f"{pct}%", size=14, weight=ft.FontWeight.W_600, color=color),
            ft.Icon(icon, color=color, size=18),
        ],
        spacing=4,
    )


def _dot_line(color: str, text: str):
    return ft.Row(
        [
            ft.Container(width=7, height=7, bgcolor=color, border_radius=4),
            ft.Text(text, size=12, color=TEXT_MUTED),
        ],
        spacing=6,
    )


def _drone_row(d: dict):
    is_alerta = d["categoria"] == "mantenimiento"
    icon_badge = ft.Container(
        width=44, height=44,
        bgcolor="#33FF5A5F" if is_alerta else CARD_GLASS,
        border=ft.Border.all(1, RED if is_alerta else CARD_BORDER),
        border_radius=12,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(
            ft.Icons.BUILD_ROUNDED if is_alerta else ft.Icons.AIRPLANEMODE_ACTIVE_ROUNDED,
            color=RED if is_alerta else "white", size=20,
        ),
    )

    info_lines = [ft.Text(d["id"], size=15, weight=ft.FontWeight.W_600, color="white")]
    info_lines.append(_dot_line(d["dot"], d["estado"]))
    if d["zona"]:
        info_lines.append(_dot_line(TEXT_MUTED, d["zona"]))

    return ft.Container(
        content=ft.Row(
            [
                icon_badge,
                ft.Column(info_lines, spacing=4, expand=True),
                _battery_view(d["bateria"]),
            ],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=CARD_GLASS,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=14,
        padding=ft.Padding(14, 12, 14, 12),
    )


def flota_view(page: ft.Page):
    tab_refs = {k: ft.Ref[ft.Container]() for k in ("todos", "activos", "base")}
    label_refs = {k: ft.Ref[ft.Text]() for k in ("todos", "activos", "base")}
    list_col = ft.Column(spacing=12)

    def filtro(tab: str):
        if tab == "activos":
            return [d for d in DRONES if d["categoria"] == "activo"]
        if tab == "base":
            return [d for d in DRONES if d["categoria"] == "base"]
        return DRONES

    def set_tab(tab: str):
        for key in tab_refs:
            active = key == tab
            tab_refs[key].current.bgcolor = YELLOW if active else "transparent"
            tab_refs[key].current.border = ft.Border.all(1, YELLOW if active else CARD_BORDER)
            label_refs[key].current.color = "black" if active else TEXT_MUTED
        list_col.controls = [_drone_row(d) for d in filtro(tab)]
        page.update()

    def tab_label(key: str):
        counts = {
            "todos": len(DRONES),
            "activos": len([d for d in DRONES if d["categoria"] == "activo"]),
            "base": len([d for d in DRONES if d["categoria"] == "base"]),
        }
        names = {"todos": "Todos", "activos": "Activos", "base": "Base"}
        return f"{names[key]} ({counts[key]})"

    def tab_btn(key: str):
        return ft.Container(
            ref=tab_refs[key],
            content=ft.Text(tab_label(key), ref=label_refs[key], size=13,
                             weight=ft.FontWeight.W_600, color=TEXT_MUTED),
            border=ft.Border.all(1, CARD_BORDER),
            border_radius=10,
            padding=ft.Padding(0, 10, 0, 10),
            alignment=ft.Alignment.CENTER,
            expand=True,
            on_click=lambda e, k=key: set_tab(k),
            ink=True,
        )

    tabs = ft.Row(
        [tab_btn("todos"), tab_btn("activos"), tab_btn("base")],
        spacing=8,
    )

    scrollable_content = ft.Column(
        [
            ft.Container(content=tabs, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=list_col, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    set_tab("todos")

    body = ft.Column(
        [
            status_bar(),
            ft.Container(height=6),
            _flota_top_bar(page),
            ft.Container(height=14),
            ft.Container(content=scrollable_content, expand=True),
            bottom_nav(page, active_route="flota"),
        ],
        spacing=0,
        expand=True,
    )

    return ft.Container(content=body, bgcolor=BG, expand=True)
