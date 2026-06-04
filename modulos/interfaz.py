# Importamos os para interactuar con comandos del sistema operativo (como limpiar pantalla)
import os
# Importamos Console de rich, que es el objeto principal para imprimir texto con estilos y colores
from rich.console import Console
# Importamos Panel de rich para mostrar cuadros con bordes alrededor del texto
from rich.panel import Panel
# Importamos Table de rich para crear y renderizar tablas estructuradas
from rich.table import Table
# Importamos box de rich, que contiene estilos de bordes (ej. bordes redondeados) para paneles y tablas
from rich import box
# Importamos Prompt de rich para solicitar información al usuario de forma interactiva y con colores
from rich.prompt import Prompt

# Instanciamos el objeto Console que usaremos en toda la interfaz para imprimir
console = Console()

def limpiar_pantalla():
    """Limpia la pantalla de la consola dependiendo del sistema operativo."""
    # Ejecutamos 'cls' si estamos en Windows (nt), o 'clear' si estamos en Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_titulo(texto, subtitulo=None):
    """Muestra un título principal dentro de un panel con estilo."""
    # Primero limpiamos la pantalla para que el título aparezca siempre arriba
    limpiar_pantalla()
    # Creamos un objeto Panel con el texto central, un subtítulo (si existe), color cyan en negrita, bordes azules redondeados, y que no se expanda por toda la terminal
    panel = Panel(texto, subtitle=subtitulo, style="bold cyan", border_style="blue", box=box.ROUNDED, expand=False)
    # Imprimimos el panel centrado en la pantalla
    console.print(panel, justify="center")
    # Imprimimos una línea en blanco para dejar espacio debajo del título
    console.print()

def mostrar_error(mensaje):
    """Muestra un mensaje indicando que ocurrió un error."""
    # Usamos sintaxis de rich (corchetes) para imprimir la X roja y el texto en negrita, seguido del mensaje
    console.print(f"[bold red]❌ Error:[/bold red] {mensaje}")

def mostrar_exito(mensaje):
    """Muestra un mensaje indicando que una acción fue exitosa."""
    # Imprimimos un check verde en negrita seguido del mensaje de éxito
    console.print(f"[bold green]✅ Éxito:[/bold green] {mensaje}")

def mostrar_info(mensaje):
    """Muestra un mensaje de información general."""
    # Imprimimos un ícono de info azul seguido del mensaje
    console.print(f"[bold blue]ℹ️ Info:[/bold blue] {mensaje}")

def pausar():
    """Detiene el programa hasta que el usuario decida continuar."""
    # Imprimimos un texto atenuado (dim) indicándole al usuario qué hacer
    console.print("\n[dim]Presiona Enter para continuar...[/dim]")
    # Usamos input() vacío, el cual se quedará esperando a que el usuario presione la tecla Enter
    input()

def leer_input(mensaje, password=False):
    """Pide al usuario que ingrese un dato, aplicando formato de color amarillo."""
    # Retornamos el resultado de Prompt.ask. Si password=True, el texto digitado se ocultará en la consola (útil para contraseñas)
    return Prompt.ask(f"[bold yellow]{mensaje}[/bold yellow]", password=password)

def mostrar_tabla_autores(autores):
    """Crea e imprime una tabla con la lista de autores registrados."""
    # Si la lista de autores está vacía, avisamos y salimos de la función
    if not autores:
        mostrar_info("No hay autores registrados.")
        return

    # Instanciamos una tabla de rich con título, bordes redondeados y encabezados en color magenta
    table = Table(title="Lista de Autores", box=box.ROUNDED, header_style="bold magenta")
    # Agregamos la columna 'ID', alineada a la derecha, en color cyan y que no permite saltos de línea (no_wrap)
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    # Agregamos la columna 'Nombre' en color blanco
    table.add_column("Nombre", style="white")
    # Agregamos la columna 'Email' en color verde
    table.add_column("Email", style="green")

    # Recorremos cada autor de nuestra lista
    for autor in autores:
        # Añadimos una fila a la tabla con los datos extraídos del diccionario del autor. Usamos .get() para evitar errores si falta un dato
        table.add_row(str(autor.get("id_autor", "")), autor.get("nombre_autor", ""), autor.get("email", ""))

    # Finalmente, imprimimos la tabla construida
    console.print(table)

def mostrar_tabla_publicaciones(publicaciones, autores_dict=None):
    """Muestra una lista de publicaciones en formato tabla."""
    # Si la lista está vacía, mostramos un mensaje de información y terminamos
    if not publicaciones:
        mostrar_info("No hay publicaciones.")
        return

    # Creamos la tabla principal
    table = Table(title="Publicaciones", box=box.ROUNDED, header_style="bold magenta")
    # Agregamos las respectivas columnas de la tabla (ID, Autor, Título, Fecha y Tags) con sus colores asignados
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Autor", style="green")
    table.add_column("Título", style="white")
    table.add_column("Fecha", style="yellow")
    table.add_column("Tags", style="blue")

    # Recorremos cada publicación en nuestra base de datos
    for pub in publicaciones:
        # Obtenemos el ID del autor que creó la publicación
        id_autor = pub.get("id_autor")
        # Si pasamos un diccionario de autores, buscamos su nombre; sino, solo mostramos su ID
        nombre_autor = autores_dict.get(id_autor, f"ID: {id_autor}") if autores_dict else str(id_autor)
        # Convertimos la lista de etiquetas (tags) en un string separado por comas
        tags = ", ".join(pub.get("tags", []))
        # Añadimos la fila a la tabla pasando los valores obtenidos como cadenas de texto
        table.add_row(
            str(pub.get("id_post", "")),
            nombre_autor,
            pub.get("titulo", ""),
            pub.get("fecha_publicacion", ""),
            tags
        )

    # Imprimimos la tabla de publicaciones en la consola
    console.print(table)

def mostrar_publicacion_completa(pub, nombre_autor):
    """Muestra todo el contenido de una sola publicación, incluyendo sus comentarios."""
    # Unimos los tags en un solo string, separados por comas
    tags = ", ".join(pub.get("tags", []))
    
    # Construimos el texto base con información del autor, la fecha y los tags, usando formato bold
    content = f"[bold]Autor:[/bold] {nombre_autor}\n"
    content += f"[bold]Fecha:[/bold] {pub.get('fecha_publicacion', '')}\n"
    content += f"[bold]Tags:[/bold] {tags}\n\n"
    # Agregamos finalmente el contenido o cuerpo del post
    content += f"{pub.get('contenido', '')}"

    # Metemos todo este texto dentro de un Panel de rich para que luzca como una tarjeta, y usamos el título del post como título del panel
    panel = Panel(content, title=f"[bold cyan]{pub.get('titulo', 'Sin título')}[/bold cyan]", box=box.ROUNDED, border_style="magenta")
    # Mostramos el panel en la pantalla
    console.print(panel)

    # Obtenemos la lista de comentarios; si no hay, por defecto es una lista vacía
    comentarios = pub.get("comentarios", [])
    # Si hay comentarios, los mostramos uno por uno
    if comentarios:
        console.print("[bold yellow]Comentarios:[/bold yellow]")
        for c in comentarios:
            # Imprimimos cada comentario mostrando su fecha (atenuada), su autor (negrita) y el texto del comentario
            console.print(f"  [dim]{c.get('fecha', '')}[/dim] [bold]{c.get('autor', 'Anon')}:[/bold] {c.get('texto', '')}")
    else:
        # Si la lista está vacía, mostramos un mensaje sutil (atenuado)
        console.print("[dim]No hay comentarios aún.[/dim]")
    # Dejamos un salto de línea al final por estética
    console.print()
