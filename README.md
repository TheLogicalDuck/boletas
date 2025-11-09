MANUAL TÉCNICO
📘 1. Descripción del Proyecto
Aplicación creada en Python con Flet que permite registrar, visualizar y exportar las
calificaciones de alumnos de forma intuitiva.
El sistema cuenta con menús desplegables para seleccionar alumnos y calificaciones por
materia, genera automáticamente el promedio final y permite exportar los datos a un
archivo CSV.
Además, utiliza una interfaz moderna con colores, botones y tablas, mostrando
notificaciones mediante SnackBars para mejorar la experiencia del usuario.
2. Herramientas Utilizadas
 Lenguaje: Python 3.12
 Framework de interfaz: Flet
 Control de versiones: Git y GitHub
 Despliegue: Vercel
 Editor usado: Visual Studio Code
🔄 3. Pseudocódigo Simplificado
Pseudocódigo del funcionamiento principal:
INICIAR aplicación Flet
CONFIGURAR ventana principal (título, tamaño, fondo)
CREAR lista de alumnos y dropdowns para materias
FUNCIÓN agregar_calificaciones:
 SI alumno no seleccionado → mostrar error
 SI falta alguna calificación → mostrar error
 CALCULAR promedio
 AGREGAR fila con calificaciones y botón eliminar
 MOSTRAR mensaje de éxito
FUNCIÓN eliminar_fila:
 QUITAR fila seleccionada
 MOSTRAR mensaje de confirmación
FUNCIÓN exportar_csv:
 GUARDAR datos de la tabla en archivo CSV en carpeta Descargas
 MOSTRAR mensaje con ruta del archivo
MOSTRAR interfaz con:
 - Sección de ingreso de datos
 - Tabla de calificaciones
 - Botones de control
FINALIZAR
📂 4. Estructura de Archivos

<img width="591" height="108" alt="image" src="https://github.com/user-attachments/assets/347ee333-280c-4b0b-b011-513988ae6777" />

⚙ 5. Explicación de Funciones Principales
Función Descripción
main(page) Función principal que configura la interfaz, los colores,
botones y contenedores.
mostrar_snackbar() Muestra mensajes flotantes de error, advertencia o
confirmación.
make_dropdown(label) Crea menús desplegables personalizados para alumno o
materias.
agregar_calificaciones(e) Valida los datos, calcula el promedio y agrega una nueva
fila a la tabla.
eliminar_fila(row) Elimina una fila de la tabla seleccionada.
exportar_csv(e) Exporta todas las calificaciones registradas a un archivo
CSV en la carpeta Descargas.
limpiar_campos() Reinicia los campos de entrada y dropdowns.
reconstruir_inputs() Recrea los dropdowns para evitar errores de referencia tras
limpiar los campos.
📸 6. Capturas del Código

<img width="425" height="661" alt="image" src="https://github.com/user-attachments/assets/3b92ed3d-1f13-4e9c-8de9-60eff48c96b6" />

🌐 7. Detalles de Despliegue
1. Subir el proyecto a un repositorio en GitHub.
2. Crear un nuevo proyecto en Vercel.
3. Vincular el repositorio de GitHub con Vercel.
4. Asegurarse de incluir el archivo requirements.txt con:
5. flet
6. Configurar Vercel para ejecutar el archivo principal main.py.
7. Una vez desplegado, copiar el enlace de la aplicación generada por Vercel.

👨💻 MANUAL DE USUARIO
📖 1. Descripción y Objetivo de la App
El Sistema de Registro de Calificaciones permite registrar las notas de diferentes
alumnos en varias materias, calcular automáticamente el promedio y exportar los
resultados a un archivo CSV para su almacenamiento o impresión.
💻 2. Requisitos para Ejecutarla
 Tener instalado Python 3.10 o superior
 Instalar la librería Flet con el comando:
 pip install flet
 Conexión a Internet (solo si se usa en Vercel)
 Navegador web moderno (Chrome, Edge, Firefox)
3. Guía Paso a Paso
1. Abrir la aplicación:
Se puede ejecutar localmente con:
2. python main.py o abrir el enlace en Vercel.
3. Seleccionar un alumno:
En el primer menú desplegable, elige el nombre del alumno.
4. Asignar calificaciones:
Llena las calificaciones para cada materia (Español, Matemáticas, Inglés, etc.).
5. Agregar registro:
Presiona el botón “Agregar Calificaciones” para registrar los datos.
6. Eliminar alumno:
Usa el ícono 🗑️ para borrar una fila del registro.
7. Exportar a CSV:
Pulsa “Exportar a CSV” y el sistema guardará el archivo con las notas en tu
carpeta Descargas.
8. Limpiar campos:
Usa el ícono ️ para limpiar los menús y volver a empezar.
🚦 4. Significado del Semáforo de Colores
Color del promedio Significado
️ Verde (≥ 90) Excelente rendimiento
️ Naranja (70–89) Desempeño aceptable
🔴 Rojo (< 70) Necesita mejorar
📸 5. Capturas del Funcionamiento

<img width="565" height="618" alt="image" src="https://github.com/user-attachments/assets/a70b1858-3fd9-4bc6-8de4-d564c9b22d53" />

🔗 6. Enlace del Proyecto en Vercel
👉 https://boletas-sandy.vercel.app/
7. Créditos y Autoría
Proyecto: Sistema de Registro de Calificaciones
Materia: Emplea frameworks para el desarrollo de software
Alumno: Carrillo Hernández Hugo Iván
Grupo: 3°A Programación
Plantel: Emplea frameworks para el desarrollo de software
Fecha: 08/11/25
