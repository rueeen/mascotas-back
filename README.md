# Mascotas Back

API REST pública para publicar mascotas perdidas, encontradas, en adopción y adoptadas, construida con Django 5, Django REST Framework, SQLite y soporte para carga de imágenes.

## Requisitos

- Python 3.11+
- SQLite (incluido por defecto con Python/Django)

## Instalación y ejecución

### 1. Crear y activar el entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar migraciones

```bash
python manage.py migrate
```

### 4. Crear un superusuario

```bash
python manage.py createsuperuser
```

### 5. Levantar el servidor de desarrollo

```bash
python manage.py runserver
```

La API quedará disponible en `http://127.0.0.1:8000/api/` y el admin en `http://127.0.0.1:8000/admin/`.

## Endpoints principales

### Mascotas

- `GET /api/mascotas/`: lista mascotas paginadas.
- `POST /api/mascotas/`: crea una mascota usando `multipart/form-data` para enviar `imagen`.
- `GET /api/mascotas/{id}/`: muestra detalle con comentarios anidados.
- `PUT/PATCH /api/mascotas/{id}/`: actualiza una mascota.
- `DELETE /api/mascotas/{id}/`: elimina una mascota.
- `GET /api/mascotas/?estado=perdida`: filtra por estado.
- `GET /api/mascotas/?search=firulais`: busca por nombre.
- `POST /api/mascotas/{id}/comentar/`: agrega comentario a una mascota sin enviar `mascota` en el body.

### Comentarios

- `GET /api/comentarios/`: lista comentarios paginados.
- `POST /api/comentarios/`: crea comentario enviando `mascota` como PK.
- `GET /api/comentarios/{id}/`: muestra detalle.
- `PUT/PATCH /api/comentarios/{id}/`: actualiza comentario.
- `DELETE /api/comentarios/{id}/`: elimina comentario.
- `GET /api/comentarios/?mascota={id}`: filtra comentarios por mascota.
