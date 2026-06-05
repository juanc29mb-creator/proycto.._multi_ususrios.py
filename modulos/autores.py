# Importamos las herramientas de nuestra interfaz gráfica de consola necesarias para las funciones de este módulo
from modulos.interfaz import mostrar_tabla_autores, leer_input, mostrar_error, mostrar_exito

def ver_autores(autores):
    """Llama a la función de la interfaz para renderizar la lista completa de todos los autores registrados."""
    # Delega la tarea a ui.py donde se construirá visualmente la tabla de usuarios
    mostrar_tabla_autores(autores)

def modificar_autor(autores, usuario_actual):
    """Permite al autor activo cambiar los datos de su propia cuenta (nombre o contraseña)."""
    # Primero verificamos que exista un usuario_actual; si es invitado (None), denegamos la acción
    if not usuario_actual:
        mostrar_error("Debes iniciar sesión para modificar tu perfil.")
        return

    # Importamos el objeto console de ui para imprimir un mensaje informativo especial
    from modulos.interfaz import console
    # Advertimos al usuario cómo evitar cambiar campos que desea mantener igual
    console.print("Deja en blanco si no deseas modificar el campo.")
    
    # Pedimos el nuevo nombre, mostrando entre paréntesis el nombre actual como referencia
    nuevo_nombre = leer_input(f"Nuevo nombre (actual: {usuario_actual.get('nombre_autor')})")
    # Pedimos la nueva contraseña ocultando lo que digita el usuario
    nuevo_password = leer_input("Nueva contraseña", password=True)

    # Si el usuario escribió un texto para el nombre, reemplazamos el valor antiguo en el diccionario
    if nuevo_nombre:
        usuario_actual["nombre_autor"] = nuevo_nombre
    
    # Si ingresó contraseña y esta tiene un tamaño mínimo seguro (4 caracteres), se guarda
    if nuevo_password and len(nuevo_password) >= 4:
        usuario_actual["password"] = nuevo_password
    # Si ingresó una contraseña pero esta es demasiado corta, lanzamos un error y omitimos ese cambio específico
    elif nuevo_password:
        mostrar_error("La contraseña debe tener al menos 4 caracteres. No se actualizó.")

    # Concluimos anunciando el éxito de la actualización
    mostrar_exito("Perfil actualizado correctamente.")

def eliminar_autor(autores, publicaciones, usuario_actual):
    """Elimina permanentemente la cuenta del usuario conectado y purga todas las publicaciones de su autoría."""
    # Control de seguridad: debe haber un usuario autenticado para proceder
    if not usuario_actual:
        mostrar_error("Debes iniciar sesión para eliminar tu perfil.")
        return False

    # Solicitamos confirmación explícita para prevenir borrados accidentales de cuentas
    confirmacion = leer_input("¿Estás seguro de que quieres eliminar tu cuenta? (s/n)")
    
    # Comprobamos si la respuesta introducida (convertida a minúsculas) es 's' (sí)
    if confirmacion.lower() == 's':
        # Eliminamos el objeto del autor recreando la lista global. Incluimos solo aquellos autores cuyo ID NO sea el ID del usuario_actual
        autores[:] = [a for a in autores if a.get("id_autor") != usuario_actual.get("id_autor")]
        
        # Eliminación en cascada: también buscamos y purgamos los posts donde 'id_autor' sea el de este usuario eliminado
        publicaciones[:] = [p for p in publicaciones if p.get("id_autor") != usuario_actual.get("id_autor")]
        
        # Avisamos la terminación exitosa de las eliminaciones
        mostrar_exito("Tu cuenta y tus publicaciones han sido eliminadas.")
        # Retornamos True para indicarle al menú principal que el perfil actual se borró y debe cerrar la sesión del usuario
        return True 
    
    # Si el usuario decidió no confirmar ('n' u otro texto), no hacemos nada y devolvemos False
    return False
