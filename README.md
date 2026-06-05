# Blog de Consola Multiusuario - Ejercicio 5

Conformado por:juan carlos merchan
               Jhon mario guamanzar
               juan castañeda
               miguel castañeda


               
Una aplicación de consola simplificada y estéticamente atractiva escrita en Python. Este proyecto permite gestionar publicaciones de un blog con un sistema de autores (registro e inicio de sesión), búsqueda mediante tags y la posibilidad de agregar comentarios a cada publicación.

## Características

- **Gestión de Sesión:** Inicio de sesión y registro con validación de correos electrónicos mediante Expresiones Regulares. Las contraseñas permanecen ocultas (con `******`) al ser tecleadas por seguridad.
- **Modo Invitado:** Los usuarios no registrados pueden listar publicaciones, buscar por etiquetas y realizar comentarios.
- **Operaciones CRUD:** Los autores verificados pueden Crear, Leer, Modificar y Eliminar sus propias publicaciones y perfil, respetando una estricta validación de propiedad (un usuario no puede modificar el trabajo de otro).
- **Interfaz "Rich":** El proyecto incluye la librería `rich` para mostrar de manera estilizada y estructurada (a través de paneles y tablas) toda la información solicitada en la consola, solucionando también problemas de codificación de caracteres.
- **Almacenamiento Local:** Los datos son persistentes a través de archivos `.json` debidamente ubicados en su directorio `datos/`.

## Estructura de Carpetas

La arquitectura del proyecto sigue un diseño altamente modular inspirado en las mejores prácticas:

```text
trabajo-de-grupo-1-main/
│
├── datos/                  # Carpeta donde se guardan las bases de datos locales
│   ├── autores.json        # Almacena los perfiles con email y passwords
│   └── publicaciones.json  # Almacena los posts y sus comentarios
│
├── modulos/                # Lógica del programa encapsulada por módulos
│   ├── __init__.py         # Archivo que define la carpeta como un paquete
│   ├── autenticacion.py    # Login, registro y validaciones de seguridad
│   ├── autores.py          # CRUD visual para la gestión de cuentas
│   ├── gestor_datos.py     # Componente que interactúa con la lectura/escritura JSON
│   ├── interfaz.py         # Encargado único de la impresión visual mediante `rich`
│   └── publicaciones.py    # CRUD visual para los posts y comentarios
│
├── venv/                   # Entorno virtual de Python
├── principal.py            # Punto de entrada y corazón del programa (El Menú)
└── requirements.txt        # Dependencias externas necesarias para funcionar
```

## Instalación y Ejecución

Asegúrate de tener Python 3.x instalado en tu sistema.

1. Abre tu terminal de comandos en la carpeta raíz del proyecto.
2. Si no has inicializado tu entorno virtual (`venv`), instálalo con:
   ```bash
   python -m venv venv
   ```
3. Activa tu entorno virtual (Ejemplo en Windows):
   ```bash
   .\venv\Scripts\activate
   ```
4. Instala las dependencias estéticas (la librería `rich`):
   ```bash
   pip install -r requirements.txt
   ```
5. Ejecuta la aplicación:
   ```bash
   python principal.py
   ```

*(Nota: En algunos entornos de terminal de Windows, si llegaras a ver símbolos extraños con las tildes, asegúrate de utilizar una terminal que soporte UTF-8 o de declarar la variable de entorno `PYTHONIOENCODING="utf-8"` antes de ejecutar).*
