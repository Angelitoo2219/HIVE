import flet as ft
from common import (
    YELLOW, GREEN, RED, TEXT_MUTED,
    CARD_GLASS, CARD_BORDER, BG,
    status_bar, bottom_nav, glass_card, navigate,
)

# Imagen del feed en vivo (placeholder). Para usar tu propio stream/foto,
# guárdala en assets/images/feed.jpg y cambia FEED_URL por src local "images/feed.jpg".
FEED_URL = "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200&q=80"

DRONE_ACTUAL = {
    "id": "HM-07",
    "activo": True,
    "bateria": "68%",
    "profundidad": "4.2 m",
    "velocidad": "1.2 m/s",
    "estado": "Limpiando",
    "residuos": "420 g",
}


def _top_bar(page: ft.Page):
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_BACK, color="white", size=22),
                    on_click=lambda e: navigate(page, "flota"),
                    ink=True,
                    border_radius=20,
                    padding=6,
                ),
                ft.Text("Vista en tiempo real", size=17, weight=ft.FontWeight.W_600, color="white"),
                ft.Container(
                    content=ft.Icon(ft.Icons.FULLSCREEN_ROUNDED, color="white", size=20),
                    bgcolor=CARD_GLASS,
                    border=ft.Border.all(1, CARD_BORDER),
                    border_radius=10,
                    padding=8,
                    on_click=lambda e: print("Pantalla completa"),
                    ink=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.Padding(left=12, right=12, top=6, bottom=0),
    )


def _control_btn(icon):
    return ft.Container(
        width=40, height=40,
        bgcolor="#4D0D1730",
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=20,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(icon, color="white", size=18),
        on_click=lambda e: print(f"Control: {icon}"),
        ink=True,
    )


def _video_feed():
    return ft.Stack(
        [
            ft.Container(
                height=190,
                border_radius=14,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Image(src=FEED_URL, fit=ft.BoxFit.COVER),
            ),
            ft.Container(
                top=10, right=10,
                bgcolor="#CCFF5A5F",
                border_radius=8,
                padding=ft.Padding(8, 3, 8, 3),
                content=ft.Row(
                    [
                        ft.Container(width=6, height=6, bgcolor="white", border_radius=3),
                        ft.Text("LIVE", size=11, weight=ft.FontWeight.BOLD, color="white"),
                    ],
                    spacing=5,
                ),
            ),
        ],
    )


def _metric_row(icon, color: str, label: str, value: str):
    return ft.Row(
        [
            ft.Icon(icon, color=color, size=18),
            ft.Text(label, size=13, color=TEXT_MUTED, expand=True),
            ft.Text(value, size=14, weight=ft.FontWeight.W_600, color="white"),
        ],
        spacing=10,
    )


def reportes_view(page: ft.Page):
    encabezado = ft.Row(
        [
            ft.Text(f"Drone {DRONE_ACTUAL['id']}", size=15, weight=ft.FontWeight.W_600, color="white"),
            ft.Row(
                [
                    ft.Container(width=7, height=7, bgcolor=GREEN, border_radius=4),
                    ft.Text("Activo", size=12, color=GREEN),
                ],
                spacing=6,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    controles = ft.Row(
        [
            _control_btn(ft.Icons.VOLUME_OFF_ROUNDED),
            _control_btn(ft.Icons.VOLUME_UP_ROUNDED),
            _control_btn(ft.Icons.CAMERA_ALT_ROUNDED),
            ft.Container(expand=True),
            _control_btn(ft.Icons.SYNC_ROUNDED),
        ],
        spacing=10,
    )

    metricas_card = glass_card(
        ft.Column(
            [
                _metric_row(ft.Icons.BATTERY_FULL_ROUNDED, GREEN, "Batería",
                            DRONE_ACTUAL["bateria"]),
                _metric_row(ft.Icons.ANCHOR_ROUNDED, TEXT_MUTED, "Profundidad",
                            DRONE_ACTUAL["profundidad"]),
                _metric_row(ft.Icons.SPEED_ROUNDED, TEXT_MUTED, "Velocidad",
                            DRONE_ACTUAL["velocidad"]),
                _metric_row(ft.Icons.AUTO_FIX_HIGH_ROUNDED, YELLOW, "Estado",
                            DRONE_ACTUAL["estado"]),
                _metric_row(ft.Icons.DELETE_SWEEP_ROUNDED, TEXT_MUTED, "Residuos capturados",
                            DRONE_ACTUAL["residuos"]),
            ],
            spacing=16,
        )
    )

    def enviar_a_base(e):
        print(f"Enviando {DRONE_ACTUAL['id']} al punto base")
        navigate(page, "flota")

    enviar_btn = ft.ElevatedButton(
        content=ft.Text("Enviar al punto base", size=15, weight=ft.FontWeight.W_600, color="white"),
        bgcolor=RED,
        height=52,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14), elevation=8, shadow_color=RED),
        on_click=enviar_a_base,
    )

    panel_card = glass_card(
        ft.Column(
            [
                encabezado,
                ft.Container(height=12),
                _video_feed(),
                ft.Container(height=12),
                controles,
            ],
            spacing=0,
        )
    )

    scrollable_content = ft.Column(
        [
            ft.Container(content=panel_card, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
            ft.Container(content=metricas_card, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=20),
            ft.Container(content=enviar_btn, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    body = ft.Column(
        [
            status_bar(),
            ft.Container(height=6),
            _top_bar(page),
            ft.Container(height=14),
            ft.Container(content=scrollable_content, expand=True),
            bottom_nav(page, active_route="reportes"),
        ],
        spacing=0,
        expand=True,
    )

    return ft.Container(content=body, bgcolor=BG, expand=True)
