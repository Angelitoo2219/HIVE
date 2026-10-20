import flet as ft
from hivemarine_app.common import (
    YELLOW, GREEN, BLUE, ORANGE, TEXT_MUTED, CARD_BORDER,
    status_bar, bottom_nav, stat_card, navigate,
)

# Foto de fondo (placeholder). Para usar la tuya: guárdala en assets/images/hero.jpg
# y cambia HERO_URL por src local "images/hero.jpg" en el ft.Image de abajo.
HERO_URL = "https://images.unsplash.com/photo-1494412651409-8963ce7935a7?w=1200&q=80"


def inicio_view(page: ft.Page):
    # --- Header ---
    header = ft.Column(
        [
            ft.Text("¡Hola, Operador!", size=14, color="white"),
            ft.Text(
                "HIVEMARINE",
                size=30,
                weight=ft.FontWeight.BOLD,
                color="white",
                style=ft.TextStyle(letter_spacing=0.5),
            ),
            ft.Text(
                "Plataforma de mantenimiento submarino como servicio.",
                size=13,
                color="white",
            ),
        ],
        spacing=4,
    )

    # --- Botones de acción (glass, sobre la foto) ---
    btn_solicitar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED, color="black"),
                ft.Text("Solicitar mantenimiento", size=15, weight=ft.FontWeight.W_600, color="black"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor=YELLOW,
        height=52,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=14),
            elevation=8,
            shadow_color=YELLOW,
        ),
        on_click=lambda e: print("Solicitar mantenimiento"),
    )

    btn_servicios = ft.OutlinedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.EXPLORE_OUTLINED, color="white"),
                ft.Text("Ver mis servicios", size=15, weight=ft.FontWeight.W_600, color="white"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        height=52,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=14),
            side=ft.BorderSide(1, CARD_BORDER),
            bgcolor="#4D141C2E",
        ),
        # Ahora navega de verdad a la pantalla del mapa 3D
        on_click=lambda e: navigate(page, "mapa"),
    )

    # --- Resumen rápido (alturas parejas, número achicado si es largo) ---
    resumen_label = ft.Text(
        "RESUMEN RÁPIDO",
        size=12,
        weight=ft.FontWeight.BOLD,
        color=TEXT_MUTED,
        style=ft.TextStyle(letter_spacing=1.4),
    )

    resumen_row = ft.Row(
        [
            stat_card("3", "En servicio hoy", ft.Icons.BUILD_CIRCLE_OUTLINED, number_color=BLUE),
            stat_card("2", "En proceso", ft.Icons.AUTORENEW_ROUNDED, number_color=ORANGE),
            stat_card("24", "Completos total", ft.Icons.CHECK_CIRCLE_OUTLINE, number_color=GREEN),
            stat_card(
                "128.6 kg", "Residuos capturados", ft.Icons.ECO_OUTLINED,
                number_color=YELLOW, number_size=15,
            ),
        ],
        spacing=10,
    )

    # --- Contenido que va ENCIMA de la foto (transparente, deja ver la imagen) ---
    foreground = ft.Column(
        [
            status_bar(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=28),
                        header,
                        btn_solicitar,
                        btn_servicios,
                        ft.Container(height=4),
                        resumen_label,
                        resumen_row,
                    ],
                    spacing=16,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=ft.Padding(left=20, right=20, top=0, bottom=10),
                expand=True,
            ),
            bottom_nav(page, active_route="inicio"),
        ],
        spacing=0,
        expand=True,
    )

    # --- Stack final: foto a pantalla completa + degradado + contenido encima ---
    return ft.Stack(
        [
            ft.Image(src=HERO_URL, fit=ft.BoxFit.COVER, left=0, top=0, right=0, bottom=0),
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    colors=["#CC060A14", "#4D060A14", "#F2060A14"],
                    stops=[0.0, 0.42, 1.0],
                ),
                left=0, top=0, right=0, bottom=0,
            ),
            ft.Container(content=foreground, left=0, top=0, right=0, bottom=0),
        ],
        expand=True,
    )
