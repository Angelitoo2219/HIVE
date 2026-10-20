import flet as ft
from common import (
    YELLOW, GREEN, RED, ORANGE, TEXT_MUTED,
    CARD_GLASS, CARD_BORDER, BG,
    status_bar, top_bar, bottom_nav, glass_card,
)

HULL_W = 350   # ancho del visor 3D (encaja en 390 - 20*2 de padding)
HULL_H = 190   # alto del visor 3D


def _grid_lines():
    """Genera las líneas del wireframe sobre el casco (efecto malla 3D)."""
    lines = []
    cols, rows = 9, 6
    for i in range(1, cols):
        x = i * HULL_W / cols
        lines.append(
            ft.Container(left=x, top=0, width=1, height=HULL_H, bgcolor="#26FFFFFF")
        )
    for j in range(1, rows):
        y = j * HULL_H / rows
        lines.append(
            ft.Container(left=0, top=y, width=HULL_W, height=1, bgcolor="#26FFFFFF")
        )
    return lines


def _risk_zone(left, top, width, height, color, opacity=0.55):
    """'Mancha' de calor que representa una zona de riesgo sobre el casco."""
    return ft.Container(
        left=left, top=top, width=width, height=height,
        bgcolor=color, opacity=opacity, border_radius=999,
    )


def _hull_viewer(page: ft.Page):
    """Visor 3D estilizado del casco: fondo tipo capsula + manchas de riesgo
    + malla + dron + controles flotantes (3D / cubo / expandir)."""

    hull_shape = ft.Container(
        left=0, top=0, width=HULL_W, height=HULL_H,
        border_radius=HULL_H / 2,
        gradient=ft.RadialGradient(
            center=ft.Alignment(-0.1, -0.2),
            radius=1.1,
            colors=["#664CD97B", "#66E8B84B", "#66FF5A5F", "#1A4CD97B"],
            stops=[0.0, 0.35, 0.55, 1.0],
        ),
        border=ft.Border.all(1, "#40FFFFFF"),
    )

    drone_marker = ft.Container(
        left=HULL_W * 0.42, top=HULL_H * 0.38, width=26, height=26,
        bgcolor="#E6060A14",
        border=ft.Border.all(1, "white"),
        border_radius=13,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.AIRPLANEMODE_ACTIVE_ROUNDED, size=14, color="white"),
    )

    # rastro punteado detrás del dron (aproximado con puntitos)
    trail = [
        ft.Container(
            left=HULL_W * 0.42 - i * 16, top=HULL_H * 0.38 + i * 10,
            width=4, height=4, bgcolor="#99FFFFFF", border_radius=2,
        )
        for i in range(1, 5)
    ]

    def float_btn(icon=None, text=None, top=0):
        return ft.Container(
            right=8, top=top, width=34, height=34,
            bgcolor=CARD_GLASS, blur=10,
            border=ft.Border.all(1, CARD_BORDER),
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(text, size=11, weight=ft.FontWeight.BOLD, color="white") if text
            else ft.Icon(icon, size=16, color="white"),
            on_click=lambda e: print(f"Control 3D: {text or icon}"),
            ink=True,
        )

    controls_col = [
        float_btn(text="3D", top=0),
        float_btn(icon=ft.Icons.VIEW_IN_AR_OUTLINED, top=42),
        float_btn(icon=ft.Icons.OPEN_IN_FULL_ROUNDED, top=84),
    ]

    return ft.Container(
        content=ft.Stack(
            [hull_shape, *_grid_lines(), *trail, drone_marker, *controls_col],
            width=HULL_W, height=HULL_H,
        ),
        bgcolor="#0D1730",
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=20,
        padding=10,
        alignment=ft.Alignment.CENTER,
    )


def _legend():
    def item(color, label):
        return ft.Row(
            [
                ft.Container(width=10, height=10, bgcolor=color, border_radius=3),
                ft.Text(label, size=12, color="white"),
            ],
            spacing=6,
        )

    return ft.Row(
        [item(RED, "Riesgo: Alto"), item(YELLOW, "Atención"), item(GREEN, "Limpio")],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


def _progress_card(value: float, label: str, color: str):
    """Tarjeta con anillo de progreso circular (Progreso total)."""
    pct_text = f"{int(value * 100)}%"
    ring = ft.Stack(
        [
            ft.ProgressRing(value=value, width=56, height=56, stroke_width=6,
                             color=color, bgcolor="#22FFFFFF"),
            ft.Container(
                width=56, height=56, alignment=ft.Alignment.CENTER,
                content=ft.Text(pct_text, size=14, weight=ft.FontWeight.BOLD, color="white"),
            ),
        ],
        width=56, height=56,
    )
    return glass_card(
        ft.Column(
            [ring, ft.Text(label, size=12, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        expand=True,
    )


def _drones_card(active: int, total: int, label: str):
    return glass_card(
        ft.Column(
            [
                ft.Icon(ft.Icons.AIRPLANEMODE_ACTIVE_ROUNDED, size=26, color=YELLOW),
                ft.Row(
                    [
                        ft.Text(str(active), size=22, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text(f" / {total}", size=14, color=TEXT_MUTED),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                ),
                ft.Text(label, size=12, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
        expand=True,
    )


def _mini_stat(pct: str, label: str, color: str):
    return glass_card(
        ft.Column(
            [
                ft.Text(pct, size=18, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(label, size=11, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        padding=ft.Padding(8, 12, 8, 12),
        expand=True,
    )


def mapa_view(page: ft.Page):
    # --- Tabs "Vista general" / "Por secciones" (togglables) ---
    tab_general = ft.Ref[ft.Container]()
    tab_secciones = ft.Ref[ft.Container]()
    tab_label_general = ft.Ref[ft.Text]()
    tab_label_secciones = ft.Ref[ft.Text]()

    def set_tab(active: str):
        is_general = active == "general"
        tab_general.current.bgcolor = "#33E8B84B" if is_general else "transparent"
        tab_general.current.border = ft.Border.all(1, YELLOW if is_general else CARD_BORDER)
        tab_label_general.current.color = YELLOW if is_general else TEXT_MUTED

        tab_secciones.current.bgcolor = "#33E8B84B" if not is_general else "transparent"
        tab_secciones.current.border = ft.Border.all(1, YELLOW if not is_general else CARD_BORDER)
        tab_label_secciones.current.color = YELLOW if not is_general else TEXT_MUTED
        page.update()

    tabs = ft.Row(
        [
            ft.Container(
                ref=tab_general,
                content=ft.Text("Vista general", ref=tab_label_general, size=13,
                                 weight=ft.FontWeight.W_600, color=YELLOW),
                bgcolor="#33E8B84B",
                border=ft.Border.all(1, YELLOW),
                border_radius=10,
                padding=ft.Padding(0, 10, 0, 10),
                alignment=ft.Alignment.CENTER,
                expand=True,
                on_click=lambda e: set_tab("general"),
                ink=True,
            ),
            ft.Container(
                ref=tab_secciones,
                content=ft.Text("Por secciones", ref=tab_label_secciones, size=13,
                                 weight=ft.FontWeight.W_600, color=TEXT_MUTED),
                bgcolor="transparent",
                border=ft.Border.all(1, CARD_BORDER),
                border_radius=10,
                padding=ft.Padding(0, 10, 0, 10),
                alignment=ft.Alignment.CENTER,
                expand=True,
                on_click=lambda e: set_tab("secciones"),
                ink=True,
            ),
        ],
        spacing=10,
    )

    stats_row_1 = ft.Row(
        [
            _progress_card(0.67, "Progreso total", GREEN),
            _drones_card(18, 20, "Drones activos"),
        ],
        spacing=10,
    )

    stats_row_2 = ft.Row(
        [
            _mini_stat("23%", "Sin limpiar", RED),
            _mini_stat("17%", "En progreso", ORANGE),
            _mini_stat("60%", "Completado", GREEN),
        ],
        spacing=10,
    )

    scrollable_content = ft.Column(
        [
            ft.Container(content=tabs, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=_hull_viewer(page), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=14),
            ft.Container(content=_legend(), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=stats_row_1, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=10),
            ft.Container(content=stats_row_2, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    body = ft.Column(
        [
            status_bar(),
            ft.Container(height=6),
            top_bar(page, "Mapa 3D del casco", back_route="inicio"),
            ft.Container(height=14),
            ft.Container(content=scrollable_content, expand=True),
            bottom_nav(page, active_route="mapa"),
        ],
        spacing=0,
        expand=True,
    )

    return ft.Container(content=body, bgcolor=BG, expand=True)
