# Importamos datetime para estampar la fecha y hora en el momento exacto en el que se crea o comenta una publicación
from datetime import datetime
# Importamos funciones gráficas de la interfaz UI, requeridas para ver listas, entradas, errores y demás.
from modulos.interfaz import mostrar_tabla_publicaciones, mostrar_publicacion_completa, leer_input, mostrar_error, mostrar_exito, mostrar_info

def obtener_diccionario_autores(autores):
    """Mapea la lista de diccionarios de autores en un formato de {id: nombre} para hacer búsquedas rápidas."""
    # Usamos comprensión de diccionarios para agrupar rápidamente los ID de los autores y asociarlos con su nombre.
    # Esto es útil al momento de mostrar tablas donde tenemos el ID_Autor pero queremos presentar su Nombre en pantalla
    return {a.get("id_autor"): a.get("nombre_autor") for a in autores}

def crear_publicacion(publicaciones, usuario_actual):
    """Permite redactar un nuevo post y asignárselo al usuario autenticado."""
    # Verificación de seguridad: no se puede publicar si es Modo Invitado
    if not usuario_actual:
        mostrar_error("Debes iniciar sesión para crear una publicación.")
        return

    # Pedimos los datos base de un post: Título, contenido y sus etiquetas (tags)
    titulo = leer_input("Título de la publicación")
    contenido = leer_input("Contenido")
    # Los tags los solicitamos como una lista plana separada por comas
    tags_str = leer_input("Tags (separados por coma)")
    
    # Transformamos el texto plano a lista: dividimos por las comas (.split) y quitamos los espacios laterales de cada palabra (.strip)
    tags = [t.strip() for t in tags_str.split(",") if t.strip()]

    # Calculamos automáticamente cuál será el ID para este nuevo post, empezando desde 1
    nuevo_id = 1
    if publicaciones:
        # Si ya existen posts, buscamos el ID más alto existente y le sumamos 1
        nuevo_id = max(p.get("id_post", 0) for p in publicaciones) + 1

    # Construimos el diccionario del nuevo post
    nueva_pub = {
        "id_post": nuevo_id,
        "id_autor": usuario_actual.get("id_autor"),  # El autor es quien ha iniciado sesión
        "titulo": titulo,
        "contenido": contenido,
        "fecha_publicacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # Generamos la fecha exacta del sistema
        "tags": tags,
        "comentarios": [] # Inicializamos la lista de comentarios vacía
    }

    # Adjuntamos el objeto a nuestra base de datos local (lista 'publicaciones')
    publicaciones.append(nueva_pub)
    mostrar_exito("Publicación creada con éxito.")

def ver_todas_publicaciones(publicaciones, autores):
    """Procesa e imprime la tabla de absolutamente todos los posts existentes."""
    # Extraemos el diccionario id:nombre de todos los autores para poder mapearlos en pantalla
    autores_dict = obtener_diccionario_autores(autores)
    # Enviamos los datos directamente al módulo UI para ser renderizados
    mostrar_tabla_publicaciones(publicaciones, autores_dict)

def ver_publicaciones_autor(publicaciones, autores):
    """Permite filtrar los posts para mostrar únicamente los de un autor en particular."""
    autores_dict = obtener_diccionario_autores(autores)
    # Solicitamos el ID del autor objetivo como texto
    id_str = leer_input("Ingresa el ID del autor")
    
    # Bloque para intentar convertir el texto del usuario a número (int)
    try:
        id_autor = int(id_str)
    except ValueError:
        # Si el usuario inserta letras o caracteres raros, marcamos error
        mostrar_error("El ID debe ser un número entero.")
        return

    # Creamos una lista filtrada solo con los posts donde 'id_autor' coincide con el introducido
    pubs_autor = [p for p in publicaciones if p.get("id_autor") == id_autor]
    
    # Comprobamos si el autor no tiene publicaciones
    if not pubs_autor:
        mostrar_info("Este autor no tiene publicaciones o no existe.")
    else:
        # Mostramos los resultados
        mostrar_tabla_publicaciones(pubs_autor, autores_dict)

def buscar_por_tag(publicaciones, autores):
    """Itera sobre cada tag de cada publicación buscando un término dado (ignorando mayúsculas/minúsculas)."""
    autores_dict = obtener_diccionario_autores(autores)
    # Pedimos la palabra y la forzamos a minúsculas usando .lower() para evitar falsos negativos en la búsqueda
    tag_buscado = leer_input("Ingresa el tag a buscar").lower()
    
    # Usamos comprensión de listas para recuperar aquellas publicaciones cuya colección de 'tags' contenga la palabra buscada
    pubs_filtradas = [p for p in publicaciones if tag_buscado in [t.lower() for t in p.get("tags", [])]]
    
    # Si la lista obtenida está vacía, no hay resultados para ese filtro
    if not pubs_filtradas:
        mostrar_info(f"No se encontraron publicaciones con el tag '{tag_buscado}'.")
    else:
        # Imprimimos la tabla con los filtrados
        mostrar_tabla_publicaciones(pubs_filtradas, autores_dict)

def modificar_publicacion(publicaciones, usuario_actual):
    """Busca una publicación propiedad del autor y permite reemplazar su título, contenido o tags."""
    if not usuario_actual:
        mostrar_error("Debes iniciar sesión para modificar una publicación.")
        return

    # Preguntamos cuál publicación se desea editar
    id_str = leer_input("ID de la publicación a modificar")
    # Validamos que se trate de un número entero
    try:
        id_post = int(id_str)
    except ValueError:
        mostrar_error("El ID debe ser numérico.")
        return

    # Buscamos la publicación. next() recorre la lista y entrega el primer coincidente. Si no lo halla, entrega 'None'
    pub = next((p for p in publicaciones if p.get("id_post") == id_post), None)

    if not pub:
        mostrar_error("Publicación no encontrada.")
        return

    # Control Crítico: Aseguramos que la publicación que el usuario intenta editar REALMENTE pertenece a él
    if pub.get("id_autor") != usuario_actual.get("id_autor"):
        mostrar_error("No tienes permiso para modificar esta publicación (no es tuya).")
        return

    # Importamos el objeto console para dar instrucciones visuales claras
    from modulos.interfaz import console
    console.print("Deja en blanco si no deseas modificar el campo.")
    
    # Pedimos los nuevos parámetros. Ponemos como referencia el valor que tenía antes (entre llaves)
    nuevo_titulo = leer_input(f"Nuevo título (actual: {pub.get('titulo')})")
    nuevo_contenido = leer_input("Nuevo contenido")
    nuevos_tags_str = leer_input(f"Nuevos tags separados por coma (actual: {', '.join(pub.get('tags', []))})")

    # Si se escribió algo para reemplazar el Título, lo actualizamos
    if nuevo_titulo:
        pub["titulo"] = nuevo_titulo
    # Si se escribió nuevo contenido, se actualiza
    if nuevo_contenido:
        pub["contenido"] = nuevo_contenido
    # Si ingresaron nuevas etiquetas, aplicamos nuestro split y strip habitual para recrear el arreglo
    if nuevos_tags_str:
        pub["tags"] = [t.strip() for t in nuevos_tags_str.split(",") if t.strip()]

    mostrar_exito("Publicación modificada.")

def eliminar_publicacion(publicaciones, usuario_actual):
    """Ubica una publicación del autor y la borra del listado global permanentemente."""
    if not usuario_actual:
        mostrar_error("Debes iniciar sesión para eliminar una publicación.")
        return

    # Pedimos y evaluamos que el ID post sea correcto
    id_str = leer_input("ID de la publicación a eliminar")
    try:
        id_post = int(id_str)
    except ValueError:
        mostrar_error("El ID debe ser numérico.")
        return

    # Usamos next() para localizar el diccionario de la publicación
    pub = next((p for p in publicaciones if p.get("id_post") == id_post), None)

    if not pub:
        mostrar_error("Publicación no encontrada.")
        return

    # Regla estricta: sólo el verdadero autor puede purgar un post
    if pub.get("id_autor") != usuario_actual.get("id_autor"):
        mostrar_error("No tienes permiso para eliminar esta publicación (no es tuya).")
        return

    # Solicitud de verificación doble ante acciones destructivas
    confirmacion = leer_input("¿Seguro que deseas eliminarla? (s/n)")
    if confirmacion.lower() == 's':
        # Removemos directamente el objeto JSON desde nuestra variable lista 'publicaciones'
        publicaciones.remove(pub)
        mostrar_exito("Publicación eliminada.")

def comentar_publicacion(publicaciones, usuario_actual, autores):
    """Permite buscar una publicación para que cualquier usuario, incluso invitado, le agregue un comentario."""
    autores_dict = obtener_diccionario_autores(autores)
    
    # Evaluamos y casteamos el ID a número entero
    id_str = leer_input("ID de la publicación a comentar")
    try:
        id_post = int(id_str)
    except ValueError:
        mostrar_error("El ID debe ser numérico.")
        return

    # Ubicamos el post solicitado
    pub = next((p for p in publicaciones if p.get("id_post") == id_post), None)

    if not pub:
        mostrar_error("Publicación no encontrada.")
        return

    # Averiguamos el nombre real del creador del post usando nuestro mapeo de diccionario
    nombre_autor = autores_dict.get(pub.get("id_autor"), "Desconocido")
    # Desplegamos el post visualmente completo para darle contexto al usuario de qué es lo que va a comentar
    mostrar_publicacion_completa(pub, nombre_autor)

    # Requerimos el comentario que debe quedar incrustado
    texto_comentario = leer_input("Escribe tu comentario")
    if not texto_comentario:
        mostrar_error("El comentario no puede estar vacío.")
        return

    # Determinamos el autor del comentario: si hay sesión iniciada sacamos su nombre, si no, lo llamamos 'Invitado'
    autor_comentario = usuario_actual.get("nombre_autor") if usuario_actual else "Invitado"
    
    # Creamos un bloque (diccionario) con los metadatos de este nuevo comentario
    nuevo_comentario = {
        "autor": autor_comentario,
        "texto": texto_comentario,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Nos aseguramos de que el post tenga declarada su lista de "comentarios", si no existe, la inicializamos vacía
    if "comentarios" not in pub:
        pub["comentarios"] = []
        
    # Anidamos nuestro comentario recién forjado en el interior de los datos de la publicación original
    pub["comentarios"].append(nuevo_comentario)
    mostrar_exito("Comentario agregado.")

def leer_publicacion(publicaciones, autores):
    """Sirve únicamente para explorar a profundidad el contenido y el hilo de comentarios de un post seleccionado."""
    autores_dict = obtener_diccionario_autores(autores)
    id_str = leer_input("ID de la publicación a leer")
    try:
        id_post = int(id_str)
    except ValueError:
        mostrar_error("El ID debe ser numérico.")
        return

    pub = next((p for p in publicaciones if p.get("id_post") == id_post), None)

    if not pub:
        mostrar_error("Publicación no encontrada.")
        return

    # Usamos la UI para imprimir el objeto completo
    nombre_autor = autores_dict.get(pub.get("id_autor"), "Desconocido")
    mostrar_publicacion_completa(pub, nombre_autor)
