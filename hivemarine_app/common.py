import flet as ft

# --- Paleta de colores de la app (compartida por todas las pantallas) ---
YELLOW = "#E8B84B"
GREEN = "#4CD97B"
RED = "#FF5A5F"
ORANGE = "#FF8A65"
BLUE = "#5BC8FF"
TEXT_MUTED = "#B7C0D1"

CARD_GLASS = "#4D141C2E"        # navy semitransparente (efecto glass)
CARD_BORDER = "#33FFFFFF"       # borde blanco sutil (brillo de vidrio)
NAV_GLASS = "#D90B1220"         # barra inferior semitransparente
BG = "#060A14"

# --- Estado compartido del wizard "Solicitar servicio" ---
# Se va llenando en cada paso (servicio elegido, barco, fecha, etc.) y
# los siguientes pasos lo leen para mostrar el resumen y el pago.
WIZARD_STATE = {
    "servicio_id": "combo",
    "servicio_nombre": "Limpieza + inspección",
    "barco": "Neopanamax 01",
    "fecha": "29/05/2025",
    "ventana": "14:00 - 16:00",
    "esclusa": "Miraflores",
    "notas": "",
    "drones_asignados": 20,
    "total": "USD 4,850.00",
}

# (ruta_interna, ícono, etiqueta)
NAV_ITEMS = [
    ("inicio", ft.Icons.HOME_ROUNDED, "Inicio"),
    ("mapa", ft.Icons.MAP_OUTLINED, "Mapa"),
    ("solicitudes", ft.Icons.ASSIGNMENT_OUTLINED, "Solicitudes"),
    ("flota", ft.Icons.DIRECTIONS_BOAT_OUTLINED, "Flota"),
    ("reportes", ft.Icons.BAR_CHART_OUTLINED, "Reportes"),
    ("mas", ft.Icons.MORE_HORIZ, "Más"),
]


def navigate(page: ft.Page, route: str):
    """Router mínimo: intercambia el contenido de la página según la ruta.
    Se importan las vistas aquí adentro (import perezoso) para evitar
    import circular con los módulos de vistas, que a su vez importan
    este archivo para pintar su nav inferior."""
    from hivemarine_app.views.inicio import inicio_view
    from hivemarine_app.views.mapa import mapa_view
    from hivemarine_app.views.solicitudes import solicitudes_view
    from hivemarine_app.views.solicitud_barco import solicitud_barco_view
    from hivemarine_app.views.solicitud_detalles import solicitud_detalles_view
    from hivemarine_app.views.solicitud_recibida import solicitud_recibida_view
    from hivemarine_app.views.solicitud_confirmado import solicitud_confirmado_view
    from hivemarine_app.views.solicitud_pago import solicitud_pago_view
    from hivemarine_app.views.solicitud_pago_confirmado import solicitud_pago_confirmado_view
    from hivemarine_app.views.solicitud_dia_servicio import solicitud_dia_servicio_view
    from hivemarine_app.views.solicitud_entrega_drones import solicitud_entrega_drones_view
    from hivemarine_app.views.solicitud_mision_progreso import solicitud_mision_progreso_view
    from hivemarine_app.views.solicitud_mision_completada import solicitud_mision_completada_view
    from hivemarine_app.views.solicitud_recuperacion_drones import solicitud_recuperacion_drones_view
    from hivemarine_app.views.mas import mas_view
    from hivemarine_app.views.flota import flota_view
    from hivemarine_app.views.reportes import reportes_view

    builders = {
        "inicio": inicio_view,
        "mapa": mapa_view,
        "solicitudes": solicitudes_view,
        "solicitud_barco": solicitud_barco_view,
        "solicitud_detalles": solicitud_detalles_view,
        "solicitud_recibida": solicitud_recibida_view,
        "solicitud_confirmado": solicitud_confirmado_view,
        "solicitud_pago": solicitud_pago_view,
        "solicitud_pago_confirmado": solicitud_pago_confirmado_view,
        "solicitud_dia_servicio": solicitud_dia_servicio_view,
        "solicitud_entrega_drones": solicitud_entrega_drones_view,
        "solicitud_mision_progreso": solicitud_mision_progreso_view,
        "solicitud_mision_completada": solicitud_mision_completada_view,
        "solicitud_recuperacion_drones": solicitud_recuperacion_drones_view,
        "mas": mas_view,
        "flota": flota_view,
        "reportes": reportes_view,
    }

    builder = builders.get(route)
    if builder is None:
        print(f"Pantalla '{route}' aún no implementada.")
        return

    page.controls.clear()
    page.add(builder(page))
    page.update()


def nav_item(page: ft.Page, route: str, icon, label: str, active: bool = False):
    """Ítem individual de la barra de navegación inferior. Navega de verdad
    al tocarlo (antes solo hacía print)."""
    color = YELLOW if active else TEXT_MUTED
    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(icon, color=color, size=22),
                ft.Text(label, size=10, color=color),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        ),
        expand=True,
        alignment=ft.Alignment.CENTER,
        on_click=lambda e, r=route: navigate(page, r),
        ink=True,
        border_radius=8,
        padding=ft.Padding(left=0, right=0, top=6, bottom=6),
    )


def bottom_nav(page: ft.Page, active_route: str):
    """Barra de navegación inferior (glass), reutilizable en cualquier vista.
    `active_route` marca en amarillo el ítem de la pantalla actual."""
    return ft.Container(
        content=ft.Row(
            [
                nav_item(page, route, icon, label, active=(route == active_route))
                for route, icon, label in NAV_ITEMS
            ],
            spacing=0,
        ),
        bgcolor=NAV_GLASS,
        blur=24,
        border=ft.Border.only(top=ft.BorderSide(1, CARD_BORDER)),
        padding=ft.Padding(left=0, right=0, top=10, bottom=10),
    )


def status_bar():
    """Barra de estado decorativa (hora + señal/wifi/batería)."""
    return ft.Container(
        content=ft.Row(
            [
                ft.Text("9:41", size=13, weight=ft.FontWeight.W_600, color="white"),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SIGNAL_CELLULAR_ALT, size=15, color="white"),
                        ft.Icon(ft.Icons.WIFI, size=15, color="white"),
                        ft.Icon(ft.Icons.BATTERY_FULL, size=15, color="white"),
                    ],
                    spacing=6,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.Padding(left=20, right=20, top=10, bottom=0),
    )


def top_bar(page: ft.Page, title: str, back_route: str = "inicio", on_filter=None):
    """Barra superior con flecha de regreso, título centrado e ícono de filtro
    a la derecha. Usada en pantallas internas (no en Inicio)."""
    filter_btn = ft.Container(
        content=ft.Icon(ft.Icons.TUNE_ROUNDED, color="white", size=20),
        bgcolor=CARD_GLASS,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=10,
        padding=8,
        on_click=on_filter if on_filter else (lambda e: print("Filtros")),
        ink=True,
    )
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_BACK, color="white", size=22),
                    on_click=lambda e: navigate(page, back_route),
                    ink=True,
                    border_radius=20,
                    padding=6,
                ),
                ft.Text(title, size=17, weight=ft.FontWeight.W_600, color="white"),
                filter_btn,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.Padding(left=12, right=12, top=6, bottom=0),
    )


def glass_card(content, padding=ft.Padding(16, 16, 16, 16), expand=None, height=None):
    """Tarjeta base con efecto glass, reutilizable en cualquier pantalla."""
    return ft.Container(
        content=content,
        bgcolor=CARD_GLASS,
        blur=14,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=14,
        padding=padding,
        expand=expand,
        height=height,
        shadow=ft.BoxShadow(blur_radius=16, color="#40000000", offset=ft.Offset(0, 6)),
    )


def step_header(step_num: int, title: str):
    """Círculo numerado + título, usado en cada paso del wizard de
    'Solicitar servicio' (1, 2, 3, 4, 5, 6)."""
    return ft.Row(
        [
            ft.Container(
                width=32, height=32,
                bgcolor="#33E8B84B",
                border=ft.Border.all(1, YELLOW),
                border_radius=16,
                alignment=ft.Alignment.CENTER,
                content=ft.Text(str(step_num), size=14, weight=ft.FontWeight.BOLD, color=YELLOW),
            ),
            ft.Text(title, size=17, weight=ft.FontWeight.W_600, color="white"),
        ],
        spacing=10,
    )


def info_row(label: str, value: str, value_color: str = "white"):
    """Fila 'etiqueta ....... valor', usada en resúmenes y confirmaciones."""
    return ft.Row(
        [
            ft.Text(label, size=13, color=TEXT_MUTED),
            ft.Text(value, size=13, weight=ft.FontWeight.W_600, color=value_color),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


def primary_button(label: str, on_click, icon=None, height: int = 52):
    """Botón principal amarillo, reutilizable (Continuar / Enviar / Pagar)."""
    row_items = [ft.Text(label, size=15, weight=ft.FontWeight.W_600, color="black")]
    if icon:
        row_items.append(ft.Icon(icon, color="black", size=18))
    return ft.ElevatedButton(
        content=ft.Row(row_items, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        bgcolor=YELLOW,
        height=height,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14), elevation=8, shadow_color=YELLOW),
        on_click=on_click,
    )


def outlined_button(label: str, on_click, icon=None, height: int = 52):
    """Botón secundario (borde), reutilizable (Ver detalles / Ver mis solicitudes)."""
    row_items = [ft.Text(label, size=15, weight=ft.FontWeight.W_600, color="white")]
    if icon:
        row_items.append(ft.Icon(icon, color="white", size=18))
    return ft.OutlinedButton(
        content=ft.Row(row_items, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        height=height,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=14),
            side=ft.BorderSide(1, CARD_BORDER),
            bgcolor=CARD_GLASS,
        ),
        on_click=on_click,
    )


def wizard_scaffold(page: ft.Page, content_column: ft.Column, active_route: str = "solicitudes"):
    """Estructura base de cada pantalla del wizard: status bar arriba,
    contenido scrolleable en medio, nav inferior fija abajo. Evita repetir
    la estructura Column(expand)+Container(expand)+scroll en cada archivo."""
    body = ft.Column(
        [
            status_bar(),
            ft.Container(height=10),
            ft.Container(content=content_column, expand=True),
            bottom_nav(page, active_route=active_route),
        ],
        spacing=0,
        expand=True,
    )
    return ft.Container(content=body, bgcolor=BG, expand=True)


def stat_card(number: str, label: str, icon=None, number_color: str = "white", number_size: int = 20):
    """Tarjeta de estadística pequeña (número + ícono + etiqueta), la misma
    que se usa en el resumen rápido de Inicio."""
    items = []
    if icon is not None:
        items.append(ft.Icon(icon, size=15, color=number_color))
    items.append(
        ft.Text(
            number,
            size=number_size,
            weight=ft.FontWeight.BOLD,
            color=number_color,
            max_lines=1,
            text_align=ft.TextAlign.CENTER,
        )
    )
    items.append(ft.Text(label, size=11, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER))

    return ft.Container(
        content=ft.Column(
            items,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            spacing=4,
        ),
        bgcolor=CARD_GLASS,
        blur=14,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=14,
        padding=ft.Padding(left=4, right=4, top=12, bottom=10),
        height=90,
        shadow=ft.BoxShadow(blur_radius=16, color="#40000000", offset=ft.Offset(0, 6)),
        expand=True,
    )
