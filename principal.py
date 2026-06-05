# Importamos la librería 'os' principal de python para construcción segura de rutas (os.path.join)
import os
# Importamos herramientas estéticas de 'rich' exclusivas de nuestro archivo main
from rich.console import Console
from rich.prompt import Prompt

# Importamos los sub-módulos que hemos organizado bajo la carpeta (paquete) 'modulos'
from modulos.gestor_datos import cargar_datos, guardar_datos
from modulos.interfaz import mostrar_titulo, limpiar_pantalla, pausar, mostrar_info
from modulos import autenticacion
from modulos import autores
from modulos import publicaciones

# Establecemos de forma dinámica y portable dónde estarán los archivos JSON
# os.path.join asiste en generar "datos/autores.json" sin importar si estamos en Mac, Linux o Windows
RUTA_AUTORES = os.path.join("datos", "autores.json")
RUTA_PUBLICACIONES = os.path.join("datos", "publicaciones.json")

# Invocamos la consola enriquecida principal de nuestra App
console = Console()

def main():
    """Función de bucle de vida que gestiona los datos precargados, la sesión actual y rutea el menú."""
    # Primer paso: Almacenamos temporalmente en RAM el contenido íntegro de los JSON del disco duro
    lista_autores = cargar_datos(RUTA_AUTORES)
    lista_publicaciones = cargar_datos(RUTA_PUBLICACIONES)
    
    # Marcamos nuestro inicio. 'usuario_actual' es 'None' (Nada), lo que significa que arranca como Invitado
    usuario_actual = None

    # Bucle infinito del programa: la app no terminará hasta que usemos la opción 0 ('break')
    while True:
        # Borramos rastros de menús previos para dar la sensación de tener una GUI o aplicación limpia
        limpiar_pantalla()
        
        # Evaluamos qué frase de subtítulo pondremos; si hay usuario actual, ponemos su nombre, sino, decimos Modo Invitado
        subtitulo = f"Usuario actual: {usuario_actual['nombre_autor']}" if usuario_actual else "Modo Invitado"
        mostrar_titulo("Blog de Consola - Ejercicio 5", subtitulo=subtitulo)

        # Imprimimos opciones estáticas en el menú general
        console.print("\n--- Menú Principal ---")
        
        # Lógica de renderizado dinámico de menú: Mostramos cosas u otras según si se tiene sesión activa
        if not usuario_actual:
            # Mostramos estas para los Invitados
            console.print("1. Iniciar sesión")
            console.print("2. Registrar nuevo autor")
        else:
            # Mostramos estas para alguien logueado
            console.print("1. Cerrar sesión")
            console.print("2. Modificar mi perfil")
            console.print("3. Eliminar mi cuenta")

        # Estas opciones siempre son públicas para cualquiera
        console.print("4. Ver lista de autores")
        console.print("5. Ver todas las publicaciones")
        console.print("6. Ver publicaciones de un autor")
        console.print("7. Buscar publicaciones por tag")
        console.print("8. Leer y comentar una publicación")
        
        # Únicamente un usuario que superó un Login válido tiene la potestad de crear o borrar datos propios
        if usuario_actual:
            console.print("9. Crear publicación")
            console.print("10. Modificar publicación propia")
            console.print("11. Eliminar publicación propia")

        # Opción universal que rompe la matriz del ciclo
        console.print("0. Guardar y Salir")
        
        # 'Prompt.ask' pausa la pantalla pidiendo que insertes texto, de paso pinta el mensaje en negrita (bold) y cyan (azul)
        opcion = Prompt.ask("\n[bold cyan]Elige una opción[/bold cyan]")

        # A partir de este punto, iniciamos el switch condicional general evaluando la opción tecleada
        if opcion == "1":
            if not usuario_actual:
                # El usuario quiere Iniciar sesión, entonces solicitamos al módulo autenticacion la gestión
                usuario_actual = autenticacion.login(lista_autores)
            else:
                # Si digitó 1 pero SÍ había un usuario, significa que quiere hacer "Cerrar sesión"
                usuario_actual = None
                mostrar_info("Sesión cerrada.")
                
        elif opcion == "2":
            if not usuario_actual:
                # El invitado registrará una cuenta. La guardamos dentro de la lista
                nuevo = autenticacion.registrar_autor(lista_autores)
                if nuevo:
                    # Inmediatamente tras crearse, logueamos automáticamente al usuario
                    usuario_actual = nuevo
            else:
                # Si el usuario digita 2 y YA está logueado, se va a su menú de gestión de perfil
                autores.modificar_autor(lista_autores, usuario_actual)
                
        elif opcion == "3" and usuario_actual:
            # Llama a borrar perfil. Si retorna 'True', es porque el borrado fue confirmado y ejecutado.
            eliminado = autores.eliminar_autor(lista_autores, lista_publicaciones, usuario_actual)
            if eliminado:
                # Al borrar de la faz del proyecto al autor, también cerramos por inercia su sesión
                usuario_actual = None
                
        elif opcion == "4":
            # Delega pintar todos los perfiles de autor
            autores.ver_autores(lista_autores)
            
        elif opcion == "5":
            # Pinta todo el conjunto de posts
            publicaciones.ver_todas_publicaciones(lista_publicaciones, lista_autores)
            
        elif opcion == "6":
            # Extrae solo posts de 1 ID de autor
            publicaciones.ver_publicaciones_autor(lista_publicaciones, lista_autores)
            
        elif opcion == "7":
            # Lógica de búsqueda mediante coincidencias string en los arrays de tags
            publicaciones.buscar_por_tag(lista_publicaciones, lista_autores)
            
        elif opcion == "8":
            # Lee explícitamente UN (1) post identificándolo por ID
            publicaciones.leer_publicacion(lista_publicaciones, lista_autores)
            # Permite agregar un comentario nuevo solo si el usuario accede explícitamente a hacerlo contestando que sí ('s')
            if Prompt.ask("¿Quieres comentar esta publicación? (s/n)").lower() == 's':
                publicaciones.comentar_publicacion(lista_publicaciones, usuario_actual, lista_autores)
                
        # Opciones restringidas: el 'and usuario_actual' actúa como pared de fuego para evitar accesos indebidos
        elif opcion == "9" and usuario_actual:
            publicaciones.crear_publicacion(lista_publicaciones, usuario_actual)
            
        elif opcion == "10" and usuario_actual:
            publicaciones.modificar_publicacion(lista_publicaciones, usuario_actual)
            
        elif opcion == "11" and usuario_actual:
            publicaciones.eliminar_publicacion(lista_publicaciones, usuario_actual)
            
        elif opcion == "0":
            # Fase crítica de finalización: Persistencia de datos
            # Cogemos las listas (arrays) de RAM que usamos todo el rato y forzamos escritura sobre el disco
            guardar_datos(RUTA_AUTORES, lista_autores)
            guardar_datos(RUTA_PUBLICACIONES, lista_publicaciones)
            mostrar_info("Datos guardados. ¡Hasta luego!")
            # La instrucción 'break' fractura el ciclo while, terminando elegantemente el software
            break
        else:
            # Controlador de excepciones básicas por input no contemplado o fuera de lógica de permisos
            mostrar_info("Opción inválida o no disponible para tu nivel de acceso.")

        # Pausamos independientemente de lo que haya hecho para que lea los mensajes o las tablas antes de limpiar pantalla
        pausar()

# Script guard: si este archivo se ejecuta independientemente (que es lo previsto), correrá `main()` de inmediato.
# Pero, si algún otro script importase a `principal.py`, no se ejecutaría la aplicación abruptamente
if __name__ == "__main__":
    main()
