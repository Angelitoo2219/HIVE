import flet as ft
from common import (
    YELLOW, TEXT_MUTED, CARD_GLASS, CARD_BORDER,
    WIZARD_STATE, step_header, primary_button, wizard_scaffold, navigate,
)

VENTANAS = ["10:00 - 12:00", "12:00 - 14:00", "14:00 - 16:00", "16:00 - 18:00", "18:00 - 20:00"]
ESCLUSAS = ["Miraflores", "Pedro Miguel", "Gatún"]
TIPOS_SERVICIO = ["Limpieza del casco", "Inspección submarina", "Limpieza + inspección"]


def _field_label(text: str):
    return ft.Text(text, size=12, color=TEXT_MUTED, weight=ft.FontWeight.W_600)


def _dropdown(options: list[str], value: str, on_change=None):
    return ft.Dropdown(
        value=value,
        options=[ft.DropdownOption(key=o, text=o) for o in options],
        color="white",
        bgcolor=CARD_GLASS,
        border_color=CARD_BORDER,
        focused_border_color=YELLOW,
        border_radius=12,
        content_padding=ft.Padding(12, 8, 12, 8),
        on_select=on_change,
    )


def solicitud_detalles_view(page: ft.Page):
    tipo_dd = _dropdown(TIPOS_SERVICIO, WIZARD_STATE.get("servicio_nombre", TIPOS_SERVICIO[-1]))

    fecha_field = ft.TextField(
        value=WIZARD_STATE.get("fecha", ""),
        hint_text="dd/mm/aaaa",
        hint_style=ft.TextStyle(color=TEXT_MUTED),
        suffix_icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
        color="white",
        bgcolor=CARD_GLASS,
        border_color=CARD_BORDER,
        focused_border_color=YELLOW,
        border_radius=12,
        height=48,
        content_padding=ft.Padding(12, 8, 12, 8),
    )

    ventana_dd = _dropdown(VENTANAS, WIZARD_STATE.get("ventana", VENTANAS[2]))
    esclusa_dd = _dropdown(ESCLUSAS, WIZARD_STATE.get("esclusa", ESCLUSAS[0]))

    notas_field = ft.TextField(
        hint_text="Escribe aquí...",
        hint_style=ft.TextStyle(color=TEXT_MUTED),
        color="white",
        bgcolor=CARD_GLASS,
        border_color=CARD_BORDER,
        focused_border_color=YELLOW,
        border_radius=12,
        min_lines=3,
        max_lines=5,
        content_padding=ft.Padding(12, 10, 12, 10),
        multiline=True,
    )

    def go_next(e):
        WIZARD_STATE["servicio_nombre"] = tipo_dd.value
        WIZARD_STATE["fecha"] = fecha_field.value or WIZARD_STATE.get("fecha", "")
        WIZARD_STATE["ventana"] = ventana_dd.value
        WIZARD_STATE["esclusa"] = esclusa_dd.value
        WIZARD_STATE["notas"] = notas_field.value or ""
        navigate(page, "solicitud_recibida")

    enviar_btn = primary_button("Enviar solicitud", go_next)

    form_col = ft.Column(
        [
            _field_label("TIPO DE SERVICIO"),
            tipo_dd,
            ft.Container(height=14),
            _field_label("FECHA PREFERIDA"),
            fecha_field,
            ft.Container(height=14),
            _field_label("VENTANA DE TRÁNSITO"),
            ventana_dd,
            ft.Container(height=14),
            _field_label("ESCLUSA"),
            esclusa_dd,
            ft.Container(height=14),
            _field_label("NOTAS ADICIONALES (OPCIONAL)"),
            notas_field,
        ],
        spacing=6,
    )

    content = ft.Column(
        [
            ft.Container(content=step_header(3, "Detalles del servicio"), padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=18),
            ft.Container(content=form_col, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=20),
            ft.Container(content=enviar_btn, padding=ft.Padding(20, 0, 20, 0)),
            ft.Container(height=16),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return wizard_scaffold(page, content, active_route="solicitudes")
