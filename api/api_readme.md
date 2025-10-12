# API de Ejercicios de Transformación

Una API sencilla construida con FastAPI para servir ejercicios de reescritura de frases basados en un archivo JSON.

## Características

- Obtener ejercicios por ID, número o de forma aleatoria.
- Filtrar ejercicios por etiquetas (`tags`).
- Formato de "tarea" listo para mostrar al usuario.
- Documentación automática de la API con Swagger UI.

## Requisitos

- Python 3.8+

## Configuración del Entorno

1.  **Clona el repositorio:**
    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd <NOMBRE-DEL-PROYECTO>
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # En Windows: .\venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements-dev.txt
    ```

## Cómo Ejecutar la API

Con el entorno virtual activado, ejecuta el siguiente comando:

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

## Documentación de la API

Una vez que la API esté en ejecución, puedes acceder a la documentación interactiva (generada por Swagger UI) en la siguiente URL:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
