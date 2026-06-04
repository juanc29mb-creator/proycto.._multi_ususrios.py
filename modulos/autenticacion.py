# Importamos la librería 're' (expresiones regulares) para realizar validaciones de formato de texto (ej. validar correos)
import re
# Importamos funciones de nuestra interfaz gráfica de consola 'ui' ubicadas en el mismo paquete 'modulos'
from modulos.interfaz import leer_input, mostrar_error, mostrar_exito

def validar_email(email):
    """Valida que un email tenga un formato correcto empleando expresiones regulares."""
    # Definimos un patrón que establece las reglas de un correo electrónico válido (texto@texto.texto)
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    # re.match compara el email dado contra nuestro patrón. Si no coincide, retorna None (Falso)
    return re.match(patron, email) is not None

def registrar_autor(autores):
    """Permite registrar un nuevo autor en el sistema y lo añade a la base de datos local."""
    # Pedimos al usuario su nombre usando nuestra función propia que da formato con rich
    nombre = leer_input("Ingresa tu nombre")
    # Validamos que el nombre no quede en blanco
    if not nombre:
        mostrar_error("El nombre no puede estar vacío.")
        return None

    # Pedimos el correo electrónico
    email = leer_input("Ingresa tu email (ej. correo@gmail.com)")
    # Evaluamos si el formato del correo introducido es correcto usando nuestra función 'validar_email'
    if not validar_email(email):
        mostrar_error("El formato del email es inválido. Debe ser como 'usuario@dominio.com'.")
        return None
    
    # Recorremos todos los autores existentes para asegurarnos de que el email ingresado no esté repetido
    for a in autores:
        # Si el email de un autor coincide con el que estamos intentando registrar, lanzamos un error y detenemos el proceso
        if a.get("email") == email:
            mostrar_error("Ya existe un autor con ese email.")
            return None

    # Pedimos la contraseña, indicando password=True para que se oculte el texto al escribir en pantalla
    password = leer_input("Ingresa tu contraseña", password=True)
    # Exigimos que la contraseña ingresada tenga como mínimo 4 caracteres por seguridad
    if not password or len(password) < 4:
        mostrar_error("La contraseña debe tener al menos 4 caracteres.")
        return None

    # Definimos un ID por defecto para el primer usuario
    nuevo_id = 1
    # Si la lista de autores ya contiene elementos, calculamos el nuevo ID encontrando el mayor ID actual y sumando 1
    if autores:
        nuevo_id = max(a.get("id_autor", 0) for a in autores) + 1

    # Construimos el objeto o diccionario que representa al nuevo autor, empaquetando todos sus datos
    nuevo_autor = {
        "id_autor": nuevo_id,
        "nombre_autor": nombre,
        "email": email,
        "password": password
    }
    
    # Añadimos a nuestro nuevo usuario al listado global de autores
    autores.append(nuevo_autor)
    # Mostramos mensaje confirmando la creación exitosa
    mostrar_exito(f"Autor '{nombre}' registrado correctamente con ID {nuevo_id}.")
    
    # Retornamos el diccionario del usuario recién creado para poder usarlo e "iniciarle sesión" automáticamente
    return nuevo_autor

def login(autores):
    """Solicita credenciales e intenta iniciar la sesión de un autor existente."""
    # Pedimos al usuario que introduzca el email con el cual fue registrado
    email = leer_input("Email")
    # Pedimos la contraseña ocultando los caracteres
    password = leer_input("Contraseña", password=True)

    # Revisamos uno por uno los registros de autores almacenados en memoria
    for autor in autores:
        # Verificamos si tanto el email como la contraseña concuerdan con la información registrada de este autor
        if autor.get("email") == email and autor.get("password") == password:
            # Si coinciden ambos datos, la validación es correcta, mostramos la bienvenida
            mostrar_exito(f"Bienvenido de nuevo, {autor.get('nombre_autor')}!")
            # Retornamos todo el objeto del autor, de esta manera el programa principal sabe QUIÉN está utilizando la app
            return autor
    
    # Si la iteración termina y ningún usuario coincidió, arrojamos un error
    mostrar_error("Email o contraseña incorrectos.")
    # Al retornar None, le indicamos al programa principal que la autenticación falló
    return None
