import flet as ft
from common import (
    YELLOW, GREEN, RED, ORANGE, BLUE, TEXT_MUTED,
    CARD_GLASS, CARD_BORDER, BG,
    status_bar, bottom_nav, glass_card, primary_button, navigate,
)

# Foto de la base (placeholder). Para usar la tuya: guárdala en
# assets/images/base.jpg y cambia FOTO_BASE_URL por src local "images/base.jpg".
FOTO_BASE_URL = "https://images.unsplash.com/photo-1553413077-190dd305871c?w=1200&q=80"

SOLICITUDES = [
    {"barco": "Neopanamax 01", "servicio": "Limpieza + inspección", "fecha": "25/05/2025",
     "hora": "14:00", "estado": "En progreso", "categoria": "activa"},
    {"barco": "Panamax 01", "servicio": "Inspección", "fecha": "20/05/2025",
     "hora": "10:00", "estado": "Pendiente", "categoria": "activa"},
    {"barco": "Neopanamax 02", "servicio": "Limpieza", "fecha": "19/05/2025",
     "hora": "15:00", "estado": "Pendiente", "categoria": "activa"},
    {"barco": "Panamax 02", "servicio": "Limpieza + inspección", "fecha": "10/05/2025",
     "hora": "09:00", "estado": "Completado", "categoria": "historial"},
]

ESCLUSAS = [
    {"nombre": "Esclusa Gatún", "servicios": 1, "color": BLUE},
    {"nombre": "Esclusa Pedro Miguel", "servicios": 1, "color": BLUE},
    {"nombre": "Esclusa Miraflores", "servicios": 2, "color": RED},
    {"nombre": "Esclusa Cocolí", "servicios": 0, "color": TEXT_MUTED},
]

BENEFICIOS = [
    "Ahorra tiempo y combustible.",
    "Reduce emisiones de CO2.",
    "Prolonga la vida útil del casco.",
    "Cumple regulaciones ambientales.",
    "Reportes digitales precisos.",
    "Tecnología de drones inteligente.",
]


def _status_badge(estado: str):
    color = GREEN if estado == "En progreso" else (ORANGE if estado == "Pendiente" else BLUE)
    return ft.Container(
        content=ft.Text(estado, size=11, weight=ft.FontWeight.W_600, color=color),
        bgcolor=f"#33{color[1:]}",
        border_radius=8,
        padding=ft.Padding(8, 3, 8, 3),
    )


def _solicitud_row(s: dict):
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    width=40, height=40,
                    bgcolor=CARD_GLASS,
                    border=ft.Border.all(1, CARD_BORDER),
                    border_radius=10,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.DIRECTIONS_BOAT_ROUNDED, color="white", size=18),
                ),
                ft.Column(
                    [
                        ft.Text(s["barco"], size=14, weight=ft.FontWeight.W_600, color="white"),
                        ft.Text(f"{s['servicio']} · {s['fecha']} - {s['hora']}",
                                size=12, color=TEXT_MUTED),
                    ],
                    spacing=2,
                    expand=True,
                ),
                _status_badge(s["estado"]),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=CARD_GLASS,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=12,
        padding=ft.Padding(12, 12, 12, 12),
    )


def _mis_solicitudes_block(page: ft.Page):
    tab_refs = {k: ft.Ref[ft.Container]() for k in ("activas", "historial", "pendientes")}
    label_refs = {k: ft.Ref[ft.Text]() for k in ("activas", "historial", "pendientes")}
    list_col = ft.Column(spacing=10)

    def filtro(tab: str):
        if tab == "activas":
            return [s for s in SOLICITUDES if s["categoria"] == "activa"]
        if tab == "historial":
            return [s for s in SOLICITUDES if s["categoria"] == "historial"]
        return [s for s in SOLICITUDES if s["estado"] == "Pendiente"]

    def set_tab(tab: str):
        for key in tab_refs:
            active = key == tab
            tab_refs[key].current.bgcolor = "#33E8B84B" if active else "transparent"
            tab_refs[key].current.border = ft.Border.all(1, YELLOW if active else CARD_BORDER)
            label_refs[key].current.color = YELLOW if active else TEXT_MUTED
        rows = filtro(tab)
        list_col.controls = (
            [_solicitud_row(s) for s in rows] if rows
            else [ft.Text("Sin solicitudes en esta categoría.", size=12, color=TEXT_MUTED)]
        )
        page.update()

    def tab_btn(key: str, label: str):
        return ft.Container(
            ref=tab_refs[key],
            content=ft.Text(label, ref=label_refs[key], size=13, weight=ft.FontWeight.W_600, color=TEXT_MUTED),
            border=ft.Border.all(1, CARD_BORDER),
            border_radius=10,
            padding=ft.Padding(0, 8, 0, 8),
            alignment=ft.Alignment.CENTER,
            expand=True,
            on_click=lambda e, k=key: set_tab(k),
            ink=True,
        )

    tabs = ft.Row(
        [tab_btn("activas", "Activas"), tab_btn("historial", "Historial"), tab_btn("pendientes", "Pendientes")],
        spacing=8,
    )

    def nueva_solicitud(e):
        navigate(page, "solicitudes")

    nueva_btn = primary_button("Nueva solicitud", nueva_solicitud, icon=ft.Icons.ADD_ROUNDED)

    body = ft.Column(
        [
            ft.Text("Mis solicitudes", size=16, weight=ft.FontWeight.BOLD, color="white"),
            ft.Container(height=12),
            tabs,
            ft.Container(height=12),
            list_col,
            ft.Container(height=14),
            nueva_btn,
        ],
        spacing=0,
    )

    block = glass_card(body)
    set_tab("activas")
    return block


def _mini_services_map():
    """Mapa estilizado del canal con las esclusas marcadas (sin dependencias externas)."""
    markers = [
        {"top": 10, "color": BLUE},
        {"top": 45, "color": BLUE},
        {"top": 82, "color": RED},
        {"top": 118, "color": TEXT_MUTED},
    ]
    stack_items = [
        ft.Container(left=28, top=6, width=2, height=128, bgcolor="#40FFFFFF"),
    ]
    for m in markers:
        stack_items.append(
            ft.Container(
                left=22, top=m["top"], width=14, height=14, border_radius=7,
                bgcolor=m["color"], border=ft.Border.all(2, "#0D1730"),
            )
        )
    stack_items.append(
        ft.Container(
            left=140, top=60,
            content=ft.Icon(ft.Icons.HOME_WORK_ROUNDED, color=YELLOW, size=18),
        )
    )
    return ft.Container(
        height=150,
        bgcolor="#0D1730",
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=14,
        padding=10,
        content=ft.Stack(stack_items),
    )


def _esclusa_row(e: dict):
    return ft.Row(
        [
            ft.Icon(ft.Icons.LOCATION_ON_ROUNDED, color=e["color"], size=18),
            ft.Text(e["nombre"], size=13, color="white", expand=True),
            ft.Text(f"{e['servicios']} servicio{'s' if e['servicios'] != 1 else ''}",
                    size=12, color=TEXT_MUTED),
        ],
        spacing=8,
    )


def _legend_dot(color: str, label: str, icon=None):
    marker = (ft.Icon(icon, color=color, size=14) if icon
              else ft.Container(width=9, height=9, bgcolor=color, border_radius=5))
    return ft.Row([marker, ft.Text(label, size=11, color=TEXT_MUTED)], spacing=6)


def _mapa_servicios_block():
    legend = ft.Row(
        [
            _legend_dot(GREEN, "En servicio"),
            _legend_dot(BLUE, "En camino"),
            _legend_dot(ORANGE, "Pendiente"),
            _legend_dot(YELLOW, "Base HiveMarine", icon=ft.Icons.HOME_WORK_ROUNDED),
        ],
        spacing=14,
        wrap=True,
    )

    body = ft.Column(
        [
            ft.Text("Mapa de servicios (en tiempo real)", size=16, weight=ft.FontWeight.BOLD, color="white"),
            ft.Container(height=12),
            _mini_services_map(),
            ft.Container(height=12),
            ft.Column([_esclusa_row(e) for e in ESCLUSAS], spacing=10),
            ft.Container(height=12),
            legend,
        ],
        spacing=0,
    )
    return glass_card(body)


def _beneficios_block():
    items = [
        ft.Row(
            [
                ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=GREEN, size=18),
                ft.Text(b, size=13, color="white", expand=True),
            ],
            spacing=10,
        )
        for b in BENEFICIOS
    ]
    body = ft.Column(
        [
            ft.Text("¿Por qué elegir HiveMarine?", size=16, weight=ft.FontWeight.BOLD, color="white"),
            ft.Container(height=12),
            ft.Column(items, spacing=12),
        ],
        spacing=0,
    )
    return glass_card(body)


def _base_block():
    foto = ft.Container(
        height=150,
        border_radius=14,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Image(src=FOTO_BASE_URL, fit=ft.BoxFit.COVER),
    )
    caption = ft.Text(
        "Estamos estratégicamente ubicados cerca del Canal de Panamá para ofrecer el mejor servicio.",
        size=12, color=TEXT_MUTED,
    )
    body = ft.Column(
        [
            ft.Text("Nuestra base HiveMarine", size=16, weight=ft.FontWeight.BOLD, color="white"),
            ft.Container(height=12),
            foto,
            ft.Container(height=10),
            caption,
        ],
        spacing=0,
    )
    return glass_card(body)


def mas_view(page: ft.Page):
    scrollable_content = ft.Column(
        [
            ft.Container(content=_mis_solicitudes_block(page), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=_mapa_servicios_block(), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=_beneficios_block(), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=_base_block(), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    body = ft.Column(
        [
            status_bar(),
            ft.Container(
                content=ft.Text("Más", size=22, weight=ft.FontWeight.BOLD, color="white"),
                padding=ft.Padding(20, 14, 20, 0),
            ),
            ft.Container(height=10),
            ft.Container(content=scrollable_content, expand=True),
            bottom_nav(page, active_route="mas"),
        ],
        spacing=0,
        expand=True,
    )

    return ft.Container(content=body, bgcolor=BG, expand=True)
