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

    # estado
    fila_seleccionada: ft.DataRow | None = None

    # SNACKBAR (reutilizable)
    snack_bar = ft.SnackBar(content=ft.Text(""), duration=3000)
    page.overlay.append(snack_bar)

    def mostrar_snackbar(texto: str, color):
        snack_bar.content = ft.Text(texto, color=ft.Colors.WHITE)
        snack_bar.bgcolor = color
        snack_bar.open = True
        page.update()

    # CONTROLES: alumno + materias
    lista_alumnos = ft.Dropdown(
        label="Alumno",
        width=300,
        options=[
            ft.dropdown.Option("Juan Manuel Martínez"),
            ft.dropdown.Option("María Fernanda Pérez"),
            ft.dropdown.Option("José Luis González"),
            ft.dropdown.Option("Ana María Sánchez"),
            ft.dropdown.Option("Pedro Pérez Pérez"),
        ],
    )

    # Creamos los dropdowns de materia en un dict para iterar fácilmente
    materias_dropdowns = {
        "Español": ft.Dropdown(label="Español", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)], width=120),
        "Matemáticas": ft.Dropdown(label="Matemáticas", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)], width=120),
        "Inglés": ft.Dropdown(label="Inglés", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)], width=120),
        "Informática": ft.Dropdown(label="Informática", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)], width=120),
        "Historia": ft.Dropdown(label="Historia", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)], width=120),
        "C. Naturales": ft.Dropdown(label="C. Naturales", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)], width=120),
        "Ed. Física": ft.Dropdown(label="Ed. Física", options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)], width=120),
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
            ft.DataColumn(ft.Text("Promedio"), numeric=True),
        ],
        rows=[]
    )

    # BOTONES
    boton_agregar = ft.ElevatedButton("Agregar Calificaciones", icon=ft.Icons.ADD)
    boton_limpiar = ft.IconButton(icon=ft.Icons.CLEAR, tooltip="Limpiar campos")
    boton_eliminar = ft.ElevatedButton("Eliminar Fila", icon=ft.Icons.DELETE, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, disabled=True)
    boton_exportar = ft.ElevatedButton("Exportar a CSV", icon=ft.Icons.DOWNLOAD, disabled=True)

    # FUNCIONES

    def actualizar_estado_botones():
        """Habilitar/deshabilitar botones según estado."""
        boton_exportar.disabled = len(tabla_calificaciones.rows) == 0
        boton_eliminar.disabled = fila_seleccionada is None
        boton_eliminar.update()
        boton_exportar.update()

    def gestionar_seleccion_fila(ev: ft.ControlEvent):
        """Se llama cuando cambia la selección de una fila (on_select_changed)."""
        nonlocal fila_seleccionada
        row = getattr(ev, "control", None)
        if row is not None:
            if getattr(row, "selected", False):
                if fila_seleccionada is not None and fila_seleccionada is not row:
                    try:
                        fila_seleccionada.selected = False
                        fila_seleccionada.update()
                    except Exception:
                        pass
                fila_seleccionada = row
            else:
                if fila_seleccionada is row:
                    fila_seleccionada = None
        else:
            fila_seleccionada = None

        actualizar_estado_botones()
        page.update()

    # --- FUNCIÓN CORREGIDA ---
    def limpiar_campos(e=None):
        """Limpia todos los dropdowns (alumno + materias) y actualiza la IU."""
        lista_alumnos.value = None
        lista_alumnos.update()  # <-- CORRECCIÓN: Actualizar visualmente

        for d in materias_dropdowns.values():
            d.value = None
            d.update()  # <-- CORRECCIÓN: Actualizar visualmente
        
        # Solo mostrar el snackbar si la función fue llamada por un evento de clic
        if e:
            mostrar_snackbar("Campos limpiados.", ft.Colors.BLUE_500)
        
        page.update() # Un update general para asegurar consistencia

    def agregar_calificaciones(e):
        """Valida entradas, calcula promedio y agrega la fila a la tabla."""
        if lista_alumnos.value in (None, ""):
            mostrar_snackbar("Error: Selecciona un alumno antes de agregar.", ft.Colors.RED_500)
            return

        valores = []
        for nombre, d in materias_dropdowns.items():
            if d.value in (None, ""):
                mostrar_snackbar(f"Error: Falta la calificación de {nombre}.", ft.Colors.RED_500)
                return
            valores.append(d.value)

        alumno = lista_alumnos.value
        for row in tabla_calificaciones.rows:
            cel0 = getattr(row.cells[0].content, "value", None)
            if cel0 == alumno:
                mostrar_snackbar("Error: Ese alumno ya tiene calificaciones registradas.", ft.Colors.ORANGE_500)
                return

        try:
            notas = [int(v) for v in valores]
        except Exception:
            mostrar_snackbar("Error: Las calificaciones deben ser números.", ft.Colors.RED_500)
            return

        promedio = sum(notas) / len(notas)
        color_prom = (
            ft.Colors.GREEN if promedio >= 90
            else ft.Colors.YELLOW_700 if promedio >= 70
            else ft.Colors.RED_700
        )

        celdas = [ft.DataCell(ft.Text(alumno))]
        for v in valores:
            celdas.append(ft.DataCell(ft.Text(str(v))))
        celdas.append(ft.DataCell(ft.Text(f"{promedio:.2f}", color=color_prom, weight=ft.FontWeight.BOLD)))

        nueva_fila = ft.DataRow(cells=celdas, selected=False, on_select_changed=gestionar_seleccion_fila)
        tabla_calificaciones.rows.append(nueva_fila)

        mostrar_snackbar("Calificaciones agregadas.", ft.Colors.GREEN_500)
        limpiar_campos()  # limpiar visualmente después de agregar
        actualizar_estado_botones()
        page.update()

    def eliminar_fila(e):
        """Elimina la fila seleccionada (si existe)."""
        nonlocal fila_seleccionada
        if fila_seleccionada:
            try:
                tabla_calificaciones.rows.remove(fila_seleccionada)
            except Exception:
                pass
            fila_seleccionada = None
            mostrar_snackbar("Fila eliminada.", ft.Colors.GREEN_500)
            actualizar_estado_botones()
            page.update()
        else:
            mostrar_snackbar("No hay fila seleccionada para eliminar.", ft.Colors.RED_500)

    def exportar_csv(e):
        if not tabla_calificaciones.rows:
            mostrar_snackbar("No hay datos para exportar.", ft.Colors.RED_500)
            return
        ruta = Path.home() / "Desktop" / "boleta_calificaciones.csv"
        try:
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                header = [getattr(c.label, "value", str(c.label)) for c in tabla_calificaciones.columns]
                writer.writerow(header)
                for row in tabla_calificaciones.rows:
                    fila = [getattr(cell.content, "value", str(cell.content)) for cell in row.cells]
                    writer.writerow(fila)
            mostrar_snackbar(f"Exportado a {ruta}", ft.Colors.GREEN_500)
        except Exception as ex:
            mostrar_snackbar(f"Error exportando: {ex}", ft.Colors.RED_500)

    # enlazar botones
    boton_agregar.on_click = agregar_calificaciones
    boton_limpiar.on_click = limpiar_campos
    boton_eliminar.on_click = eliminar_fila
    boton_exportar.on_click = exportar_csv

    # LAYOUT
    fila_entradas = ft.Row(
        [
            lista_alumnos,
            ft.Row(list(materias_dropdowns.values()), wrap=True, spacing=10),
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    fila_botones = ft.Row(
        [boton_agregar, boton_limpiar, boton_eliminar, boton_exportar],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )

    page.add(
        ft.Column(
            [
                ft.Text("Sistema de Registro de Calificaciones", style=ft.TextThemeStyle.HEADLINE_SMALL, color="white"),
                fila_entradas,
                fila_botones,
                ft.Divider(),
                tabla_calificaciones
            ],
            spacing=15
        )
    )

    actualizar_estado_botones()

if __name__ == "__main__":
    ft.app(target=main)