import flet as ft
import csv
from pathlib import Path
from datetime import datetime

def main(page: ft.Page):
    # --- CONFIGURACIÓN DE LA PÁGINA ---
    page.title = "Boleta de Calificaciones"
    page.window_width = 1200
    page.window_height = 800
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f5f5f5"  # Un gris claro para el fondo

    # --- SNACKBAR PARA NOTIFICACIONES ---
    snack_bar = ft.SnackBar(content=ft.Text(""), duration=3000)
    page.overlay.append(snack_bar)

    def mostrar_snackbar(texto: str, color):
        snack_bar.content = ft.Text(texto, color=ft.Colors.WHITE)
        snack_bar.bgcolor = color
        snack_bar.open = True
        page.update()

    # --- FUNCIÓN PARA CREAR DROPDOWNS CON ESTILO ---
    def make_dropdown(label: str, width: int = 140):
        options = [ft.dropdown.Option(str(i)) for i in range(10, 101, 10)] if label != "Alumno" else [
            ft.dropdown.Option("Juan Manuel Martinez"),
            ft.dropdown.Option("Maria Fernanda Perez"),
            ft.dropdown.Option("Jose Luis Gonzalez"),
            ft.dropdown.Option("Ana Maria Sanchez"),
            ft.dropdown.Option("Pedro Perez Perez"),
        ]
        return ft.Dropdown(
            label=label,
            options=options,
            width=250 if label == "Alumno" else width,
            bgcolor="#ffffff",
            border_radius=8,
            border_color="transparent",
            focused_border_color=ft.Colors.BLUE_500,
            content_padding=12
        )

    # --- DEFINICIÓN DE COMPONENTES DE ENTRADA ---
    lista_alumnos = make_dropdown("Alumno")
    materias_dropdowns = {
        "Español": make_dropdown("Español"),
        "Matemáticas": make_dropdown("Matemáticas"),
        "Inglés": make_dropdown("Inglés"),
        "Informática": make_dropdown("Informática"),
        "Historia": make_dropdown("Historia"),
        "C. Naturales": make_dropdown("C. Naturales"),
        "Ed. Física": make_dropdown("Ed. Física"),
    }

    # --- TABLA DE CALIFICACIONES ---
    tabla_calificaciones = ft.DataTable(
        heading_row_color=ft.Colors.BLUE_GREY_50,
        heading_row_height=45,
        columns=[
            ft.DataColumn(ft.Text("Alumno", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Español")),
            ft.DataColumn(ft.Text("Matemáticas")),
            ft.DataColumn(ft.Text("Inglés")),
            ft.DataColumn(ft.Text("Informática")),
            ft.DataColumn(ft.Text("Historia")),
            ft.DataColumn(ft.Text("C. Naturales")),
            ft.DataColumn(ft.Text("Ed. Física")),
            ft.DataColumn(ft.Text("Promedio", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[]
    )

    # --- LÓGICA DE FUNCIONAMIENTO ---
    def reconstruir_inputs():
        nonlocal lista_alumnos, materias_dropdowns
        # Se crean nuevas instancias de los dropdowns
        lista_alumnos = make_dropdown("Alumno")
        materias_dropdowns = {
            "Español": make_dropdown("Español"),
            "Matemáticas": make_dropdown("Matemáticas"),
            "Inglés": make_dropdown("Inglés"),
            "Informática": make_dropdown("Informática"),
            "Historia": make_dropdown("Historia"),
            "C. Naturales": make_dropdown("C. Naturales"),
            "Ed. Física": make_dropdown("Ed. Física"),
        }
        
        # --- CORRECCIÓN APLICADA AQUÍ ---
        # Actualizar los controles en la interfaz usando los índices correctos
        inputs_container.content.controls[1] = lista_alumnos # Índice 1 es el dropdown de alumno
        inputs_container.content.controls[2] = ft.Row(list(materias_dropdowns.values()), wrap=True, spacing=10) # Índice 2 es la fila de materias
        page.update()

    def limpiar_campos(e=None):
        reconstruir_inputs()
        if e:
            mostrar_snackbar("Campos limpiados.", ft.Colors.BLUE_500)

    def eliminar_fila(row):
        try:
            tabla_calificaciones.rows.remove(row)
            mostrar_snackbar("Alumno eliminado.", ft.Colors.GREEN_500)
            page.update()
        except Exception as ex:
            mostrar_snackbar(f"Error eliminando fila: {ex}", ft.Colors.RED_500)

    def agregar_calificaciones(e):
        if lista_alumnos.value in (None, ""):
            mostrar_snackbar("Selecciona un alumno.", ft.Colors.RED_500)
            return

        valores = []
        for nombre, d in materias_dropdowns.items():
            if d.value in (None, ""):
                mostrar_snackbar(f"Falta la calificación de {nombre}.", ft.Colors.RED_500)
                return
            valores.append(d.value)

        alumno = lista_alumnos.value
        for row in tabla_calificaciones.rows:
            if getattr(row.cells[0].content, "value", "") == alumno:
                mostrar_snackbar("Ese alumno ya tiene calificaciones registradas.", ft.Colors.ORANGE_500)
                return

        notas = [int(v) for v in valores]
        promedio = sum(notas) / len(notas)
        color_prom = (
            ft.Colors.GREEN_700 if promedio >= 90
            else ft.Colors.ORANGE_700 if promedio >= 70
            else ft.Colors.RED_700
        )

        boton_borrar = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=ft.Colors.RED_600,
            tooltip="Eliminar alumno",
        )

        celdas = [ft.DataCell(ft.Text(alumno))]
        for v in valores:
            celdas.append(ft.DataCell(ft.Text(str(v))))
        celdas.append(ft.DataCell(ft.Text(f"{promedio:.2f}", color=color_prom, weight=ft.FontWeight.BOLD)))
        celdas.append(ft.DataCell(boton_borrar))

        nueva_fila = ft.DataRow(cells=celdas)
        tabla_calificaciones.rows.append(nueva_fila)

        boton_borrar.on_click = lambda ev, r=nueva_fila: eliminar_fila(r)

        mostrar_snackbar("Calificaciones agregadas.", ft.Colors.GREEN_500)
        limpiar_campos()
        page.update()

    def exportar_csv(e):
        if not tabla_calificaciones.rows:
            mostrar_snackbar("No hay datos para exportar.", ft.Colors.RED_500)
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ruta = Path.home() / "Downloads" / f"BOLETA_{timestamp}.csv"

        try:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                header = [getattr(c.label, "value", str(c.label)) for c in tabla_calificaciones.columns[:-1]]
                writer.writerow(header)
                for row in tabla_calificaciones.rows:
                    fila = [
                        getattr(cell.content, "value", "") if isinstance(cell.content, ft.Text) else ""
                        for cell in row.cells[:-1]
                    ]
                    writer.writerow(fila)
            mostrar_snackbar(f"Exportado a {ruta}", ft.Colors.GREEN_500)
        except Exception as ex:
            mostrar_snackbar(f"Error exportando: {ex}", ft.Colors.RED_500)

    # --- DISEÑO DE LA INTERFAZ (UI) ---
    boton_agregar = ft.ElevatedButton(
        "Agregar Calificaciones",
        icon=ft.Icons.ADD_ROUNDED,
        on_click=agregar_calificaciones,
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE,
        height=45,
    )
    boton_limpiar = ft.IconButton(
        icon=ft.Icons.CLEAR_ALL_ROUNDED,
        tooltip="Limpiar campos",
        on_click=limpiar_campos,
        icon_color=ft.Colors.GREY_600,
        icon_size=25,
    )
    boton_exportar = ft.ElevatedButton(
        "Exportar a CSV",
        icon=ft.Icons.DOWNLOAD_ROUNDED,
        on_click=exportar_csv,
        bgcolor=ft.Colors.GREEN_500,
        color=ft.Colors.WHITE,
        height=45,
    )

    # Contenedor para los inputs con título
    inputs_container = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.EDIT_NOTE, color=ft.Colors.BLUE_GREY_600),
                ft.Text("1. Ingresar Datos del Alumno", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
            ]),
            lista_alumnos,
            ft.Row(list(materias_dropdowns.values()), wrap=True, spacing=10),
            ft.Divider(height=10, color="transparent"),
            ft.Row(
                [boton_agregar, boton_limpiar, boton_exportar],
                alignment=ft.MainAxisAlignment.START,
                spacing=15
            ),
        ]),
        padding=20,
        border_radius=12,
        bgcolor="#ffffff",
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.with_opacity(0.1, "black"),
            offset=ft.Offset(0, 2),
        )
    )

    # Contenedor para la tabla con título
    tabla_container = ft.Container(
        content=ft.Column([
             ft.Row([
                ft.Icon(ft.Icons.TABLE_CHART_ROUNDED, color=ft.Colors.BLUE_GREY_600),
                ft.Text("2. Registros de Calificaciones", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
            ]),
            ft.Divider(height=5),
            ft.Row([tabla_calificaciones], scroll=ft.ScrollMode.ALWAYS),
        ]),
        padding=20,
        border_radius=12,
        bgcolor="#ffffff",
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.with_opacity(0.1, "black"),
            offset=ft.Offset(0, 2),
        )
    )

    page.add(
        ft.Column(
            [
                ft.Text("Sistema de Registro de Calificaciones", style=ft.TextThemeStyle.HEADLINE_LARGE, weight=ft.FontWeight.BOLD),
                ft.Text("Una forma moderna y eficiente de gestionar las notas.", color=ft.Colors.GREY_700),
                ft.Divider(height=20),
                inputs_container,
                tabla_container,
            ],
            spacing=25
        )
    )

if __name__ == "__main__":
    ft.app(target=main)