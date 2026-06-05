from datetime import datetime  # Trae la clase datetime para usar fechas y horas en el código
from modulos.interfaz import mostrar_tabla_publicaciones, mostrar_publicacion_completa, leer_input, mostrar_error, mostrar_exito, mostrar_info  # Trae las funciones que muestran datos en pantalla y leen entrada

# Convierte una lista de autores a un diccionario donde la clave es el id de autor
# y el valor es el nombre del autor. Esto facilita mostrar el nombre en lugar del id.
def obtener_diccionario_autores(autores):
    return {a.get("id_autor"): a.get("nombre_autor") for a in autores}  # Recorre cada autor y arma un mapa id->nombre


# Intenta transformar el valor ingresado a un número entero.
# Si el valor no es numérico, muestra un mensaje de error y devuelve None.
def _parse_int(valor, mensaje_error):
    try:
        return int(valor)  # Convierte el texto a entero cuando es posible
    except (TypeError, ValueError):
        mostrar_error(mensaje_error)  # Muestra el mensaje de error enviado
        return None  # Devuelve None para indicar que la conversión falló


# Busca en la lista de publicaciones la que tenga el id_post solicitado.
# Si la encuentra, la devuelve; si no, devuelve None.
def _buscar_publicacion(publicaciones, id_post):
    return next((p for p in publicaciones if p.get("id_post") == id_post), None)  # Devuelve la primera coincidencia o None


# Convierte una cadena de tags separada por comas en una lista de tags limpia.
# Quita espacios extras y descarta valores vacíos.
def _leer_tags(tags_str):
    return [t.strip() for t in (tags_str or "").split(",") if t.strip()]  # Divide la cadena y limpia cada tag


# Pide al usuario los datos de la publicación y crea un nuevo objeto de publicación.
def crear_publicacion(publicaciones, usuario_actual):
    if not usuario_actual:
        mostrar_error("Debes iniciar sesión para crear una publicación.")  # No permite crear publicación sin iniciar sesión
        return

    titulo = leer_input("Título de la publicación")  # Lee el título de la publicación
    contenido = leer_input("Contenido")  # Lee el contenido de la publicación
    tags = _leer_tags(leer_input("Tags (separados por coma)"))  # Lee los tags y los transforma en una lista
    nuevo_id = max((p.get("id_post", 0) for p in publicaciones), default=0) + 1  # Calcula el id siguiente usando el id más alto actual

    publicaciones.append({
        "id_post": nuevo_id,  # Guarda el nuevo id de la publicación
        "id_autor": usuario_actual.get("id_autor"),  # Asigna el id del autor que creó la publicación
        "titulo": titulo,  # Guarda el título ingresado por el usuario
        "contenido": contenido,  # Guarda el contenido ingresado por el usuario
        "fecha_publicacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Guarda la fecha y hora actual en formato legible
        "tags": tags,  # Guarda la lista de tags para esta publicación
        "comentarios": [],  # Inicia la lista de comentarios vacía
    })
    mostrar_exito("Publicación creada con éxito.")  # Muestra mensaje de confirmación


# Muestra todas las publicaciones existentes con sus autores.
def ver_todas_publicaciones(publicaciones, autores):
    mostrar_tabla_publicaciones(publicaciones, obtener_diccionario_autores(autores))  # Llama a la interfaz para mostrar la tabla


# Muestra solo las publicaciones de un autor específico.
def ver_publicaciones_autor(publicaciones, autores):
    id_autor = _parse_int(leer_input("Ingresa el ID del autor"), "El ID debe ser un número entero.")  # Lee el id del autor y lo convierte a entero
    if id_autor is None:
        return  # Detiene la función si el id no es válido

    pubs_autor = [p for p in publicaciones if p.get("id_autor") == id_autor]  # Filtra las publicaciones por id de autor
    if not pubs_autor:
        mostrar_info("Este autor no tiene publicaciones o no existe.")  # Informa si no hay publicaciones para ese autor
        return

    mostrar_tabla_publicaciones(pubs_autor, obtener_diccionario_autores(autores))  # Muestra solo las publicaciones del autor encontrado


# Busca publicaciones que tengan un tag específico escrito por el usuario.
def buscar_por_tag(publicaciones, autores):
    tag_buscado = leer_input("Ingresa el tag a buscar").lower()  # Lee el tag y lo pasa a minúscula para comparar
    pubs_filtradas = [p for p in publicaciones if tag_buscado in [t.lower() for t in p.get("tags", [])]]  # Filtra por tags iguales sin importar mayúsculas/minúsculas

    if not pubs_filtradas:
        mostrar_info(f"No se encontraron publicaciones con el tag '{tag_buscado}'.")  # Informa si no hay coincidencias
        return

    mostrar_tabla_publicaciones(pubs_filtradas, obtener_diccionario_autores(autores))  # Muestra las publicaciones encontradas


# Permite al autor modificar los datos de una publicación que ya existe.
def modificar_publicacion(publicaciones, usuario_actual):
    if not usuario_actual:
        mostrar_error("Debes iniciar sesión para modificar una publicación.")  # No permite modificar sin iniciar sesión
        return

    id_post = _parse_int(leer_input("ID de la publicación a modificar"), "El ID debe ser numérico.")  # Lee el id de la publicación a modificar
    if id_post is None:
        return  # Detiene la función si el id no es válido

    pub = _buscar_publicacion(publicaciones, id_post)  # Busca la publicación solicitada
    if not pub:
        mostrar_error("Publicación no encontrada.")  # Informa si no existe
        return
    if pub.get("id_autor") != usuario_actual.get("id_autor"):
        mostrar_error("No tienes permiso para modificar esta publicación (no es tuya).")  # Verifica que solo el autor pueda modificarla
        return

    from modulos.interfaz import console  # Importa la consola de la interfaz para mostrar texto simple
    console.print("Deja en blanco si no deseas modificar el campo.")  # Explica al usuario que puede dejar campos sin cambiar

    nuevo_titulo = leer_input(f"Nuevo título (actual: {pub.get('titulo')})")  # Pregunta por el nuevo título
    nuevo_contenido = leer_input("Nuevo contenido")  # Pregunta por el nuevo contenido
    nuevos_tags = _leer_tags(leer_input(f"Nuevos tags separados por coma (actual: {', '.join(pub.get('tags', []))})"))  # Pregunta por los nuevos tags

    if nuevo_titulo:
        pub["titulo"] = nuevo_titulo  # Actualiza el título solo si el usuario ingresó uno nuevo
    if nuevo_contenido:
        pub["contenido"] = nuevo_contenido  # Actualiza el contenido solo si se ingresó uno nuevo
    if nuevos_tags:
        pub["tags"] = nuevos_tags  # Actualiza los tags solo si se agregaron nuevos tags

    mostrar_exito("Publicación modificada.")  # Informa que la publicación se actualizó correctamente


# Elimina una publicación solo si el autor lo confirma y es el dueño.
def eliminar_publicacion(publicaciones, usuario_actual):
    if not usuario_actual:
        mostrar_error("Debes iniciar sesión para eliminar una publicación.")  # No permite eliminar sin iniciar sesión
        return

    id_post = _parse_int(leer_input("ID de la publicación a eliminar"), "El ID debe ser numérico.")  # Lee el id de la publicación a eliminar
    if id_post is None:
        return  # Detiene la función si el id no es válido

    pub = _buscar_publicacion(publicaciones, id_post)  # Busca la publicación en la lista
    if not pub:
        mostrar_error("Publicación no encontrada.")  # Informa si no existe la publicación
        return
    if pub.get("id_autor") != usuario_actual.get("id_autor"):
        mostrar_error("No tienes permiso para eliminar esta publicación (no es tuya).")  # Verifica que el usuario sea el autor
        return

    if leer_input("¿Seguro que deseas eliminarla? (s/n)").lower() == "s":  # Confirma la decisión del usuario
        publicaciones.remove(pub)  # Elimina la publicación de la lista
        mostrar_exito("Publicación eliminada.")  # Informa que se borró correctamente


# Agrega un comentario a una publicación existente.
def comentar_publicacion(publicaciones, usuario_actual, autores):
    id_post = _parse_int(leer_input("ID de la publicación a comentar"), "El ID debe ser numérico.")  # Lee el id de la publicación a comentar
    if id_post is None:
        return  # Detiene la función si el id no es válido

    pub = _buscar_publicacion(publicaciones, id_post)  # Busca la publicación para comentar
    if not pub:
        mostrar_error("Publicación no encontrada.")  # Informa si no existe la publicación
        return

    mostrar_publicacion_completa(pub, obtener_diccionario_autores(autores).get(pub.get("id_autor"), "Desconocido"))  # Muestra la publicación antes de comentar
    texto_comentario = leer_input("Escribe tu comentario")  # Lee el texto del comentario
    if not texto_comentario:
        mostrar_error("El comentario no puede estar vacío.")  # No permite comentarios sin texto
        return

    pub.setdefault("comentarios", []).append({
        "autor": usuario_actual.get("nombre_autor") if usuario_actual else "Invitado",  # Guarda el nombre del autor que comenta
        "texto": texto_comentario,  # Guarda el texto ingresado
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Guarda la fecha y hora del comentario
    })
    mostrar_exito("Comentario agregado.")  # Informa que el comentario se agregó correctamente


# Muestra una publicación completa a partir de su id.
def leer_publicacion(publicaciones, autores):
    id_post = _parse_int(leer_input("ID de la publicación a leer"), "El ID debe ser numérico.")  # Lee el id de la publicación a mostrar
    if id_post is None:
        return  # Detiene la función si el id ingresado no es válido

    pub = _buscar_publicacion(publicaciones, id_post)  # Busca la publicación solicitada
    if not pub:
        mostrar_error("Publicación no encontrada.")  # Informa si no existe la publicación
        return

    mostrar_publicacion_completa(pub, obtener_diccionario_autores(autores).get(pub.get("id_autor"), "Desconocido"))  # Muestra la publicación completa en pantalla
