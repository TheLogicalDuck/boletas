import flet as ft
import csv
from pathlib import Path

def main(page: ft.Page):
    page.title = "Boleta de Calificaciones"
    page.bgcolor = "black"
    page.window_width = 1200
    page.window_height = 700
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE

    snack_bar = ft.SnackBar(content=ft.Text(""), duration=3000)
    page.overlay.append(snack_bar)

    def mostrar_snackbar(texto: str, color):
        snack_bar.content = ft.Text(texto, color=ft.Colors.WHITE)
        snack_bar.bgcolor = color
        snack_bar.open = True
        page.update()

    # Helper para crear dropdowns
    def make_dropdown(label: str, width: int = 120):
        options = [ft.dropdown.Option(str(i)) for i in range(10, 101, 10)] if label != "Alumno" else [
            ft.dropdown.Option("Juan Manuel Martinez"),
            ft.dropdown.Option("Maria Fernanda Perez"),
            ft.dropdown.Option("Jose Luis Gonzalez"),
            ft.dropdown.Option("Ana Maria Sanchez"),
            ft.dropdown.Option("Pedro Perez Perez"),
        ]
        return ft.Dropdown(label=label, options=options, width=300 if label == "Alumno" else width)

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

    # TABLA
    tabla_calificaciones = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Alumno")),
            ft.DataColumn(ft.Text("Español")),
            ft.DataColumn(ft.Text("Matemáticas")),
            ft.DataColumn(ft.Text("Inglés")),
            ft.DataColumn(ft.Text("Informática")),
            ft.DataColumn(ft.Text("Historia")),
            ft.DataColumn(ft.Text("C. Naturales")),
            ft.DataColumn(ft.Text("Ed. Física")),
            ft.DataColumn(ft.Text("Promedio")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[]
    )

    # Función para reconstruir los inputs
    def reconstruir_inputs():
        nonlocal lista_alumnos, materias_dropdowns
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
        inputs_row.controls[0] = lista_alumnos
        inputs_row.controls[1] = ft.Row(list(materias_dropdowns.values()), wrap=True, spacing=10)
        page.update()

    # LIMPIAR CAMPOS
    def limpiar_campos(e=None):
        reconstruir_inputs()
        if e:
            mostrar_snackbar("Campos limpiados.", ft.Colors.BLUE_500)

    # FUNCIÓN PARA ELIMINAR UNA FILA
    def eliminar_fila(row):
        try:
            tabla_calificaciones.rows.remove(row)
            mostrar_snackbar("Alumno eliminado.", ft.Colors.GREEN_500)
            page.update()
        except Exception as ex:
            mostrar_snackbar(f"Error eliminando fila: {ex}", ft.Colors.RED_500)

    # AGREGAR CALIFICACIONES
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
            ft.Colors.GREEN if promedio >= 90
            else ft.Colors.YELLOW_700 if promedio >= 70
            else ft.Colors.RED_700
        )

        # Botón de eliminar por fila
        boton_borrar = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_700,
            tooltip="Eliminar alumno",
        )

        celdas = [ft.DataCell(ft.Text(alumno))]
        for v in valores:
            celdas.append(ft.DataCell(ft.Text(str(v))))
        celdas.append(ft.DataCell(ft.Text(f"{promedio:.2f}", color=color_prom, weight=ft.FontWeight.BOLD)))
        celdas.append(ft.DataCell(boton_borrar))

        nueva_fila = ft.DataRow(cells=celdas)
        tabla_calificaciones.rows.append(nueva_fila)

        # Conectar botón al eliminar la fila
        boton_borrar.on_click = lambda ev, r=nueva_fila: eliminar_fila(r)

        mostrar_snackbar("Calificaciones agregadas.", ft.Colors.GREEN_500)
        limpiar_campos()
        page.update()

    def exportar_csv(e):
        if not tabla_calificaciones.rows:
            mostrar_snackbar("No hay datos para exportar.", ft.Colors.RED_500)
            return
        ruta = Path.home() / "Downloads" / "BOLETA DE CALIFICACIÓNES.csv"
        try:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                header = [getattr(c.label, "value", str(c.label)) for c in tabla_calificaciones.columns]
                writer.writerow(header)
                for row in tabla_calificaciones.rows:
                    fila = [getattr(cell.content, "value", "") if isinstance(cell.content, ft.Text) else "" for cell in row.cells[:-1]]
                    writer.writerow(fila)
            mostrar_snackbar(f"Exportado a {ruta}", ft.Colors.GREEN_500)
        except Exception as ex:
            mostrar_snackbar(f"Error exportando: {ex}", ft.Colors.RED_500)

    # UI
    boton_agregar = ft.ElevatedButton("Agregar Calificaciones", icon=ft.Icons.ADD, on_click=agregar_calificaciones)
    boton_limpiar = ft.IconButton(icon=ft.Icons.CLEAR, tooltip="Limpiar campos", on_click=limpiar_campos)
    boton_exportar = ft.ElevatedButton("Exportar a CSV", icon=ft.Icons.DOWNLOAD, on_click=exportar_csv)

    inputs_row = ft.Row(
        [
            lista_alumnos,
            ft.Row(list(materias_dropdowns.values()), wrap=True, spacing=10),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20
    )

    fila_botones = ft.Row(
        [boton_agregar, boton_limpiar, boton_exportar],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )

    page.add(
        ft.Column(
            [
                ft.Text("Sistema de Registro de Calificaciones", style=ft.TextThemeStyle.HEADLINE_SMALL, color="white"),
                inputs_row,
                fila_botones,
                ft.Divider(),
                tabla_calificaciones,
            ],
            spacing=15
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)