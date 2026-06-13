# Truequing

Truequing es una herramienta abierta para facilitar el intercambio de figuritas.

El proyecto ayuda a encontrar oportunidades de intercambio antes y durante los encuentros de coleccionistas mediante herramientas de búsqueda, matching, estadísticas colectivas y soporte offline.

A medida que más personas participan, la información colectiva permite construir estadísticas sobre disponibilidad, demanda y dificultad de las figuritas, enriqueciendo la experiencia de intercambio para toda la comunidad.

El proyecto nació en La Plata como un aporte abierto a la comunidad de coleccionistas y se desarrolla como software libre.

## Estado actual

Implementado:

- Gestión de álbum.
- Gestión de faltantes y repetidas.
- Búsqueda pública de disponibilidad.
- Posibles intercambios.
- QR para intercambio presencial.
- Escaneo de QR.
- PWA (Progressive Web App).
- Funcionamiento offline.
- Sincronización local mediante IndexedDB.
- Estadísticas colectivas básicas.

En desarrollo:

- Matching público.
- Mensajería simple entre usuarios.
- Estadísticas avanzadas.
- Puntuación de oportunidades de intercambio.

## Tecnologías

- Python
- Django
- PostgreSQL
- HTML
- CSS
- JavaScript
- IndexedDB
- Progressive Web App (PWA)

## Instalación

Crear y activar un entorno virtual:

python -m venv truequing
source truequing/bin/activate

Instalar dependencias:

pip install -r requirements.txt

Configurar PostgreSQL y actualizar los parámetros de conexión en:

config/settings.py

Aplicar migraciones:

python manage.py migrate

Crear un usuario administrador:

python manage.py createsuperuser

Iniciar el servidor:

python manage.py runserver

La aplicación estará disponible en:

http://127.0.0.1:8000/

## Documentación

La documentación funcional y de producto se encuentra en:

docs/vision.md
docs/roadmap.md

## Contribuciones

Las contribuciones son bienvenidas.

El objetivo del proyecto es construir una herramienta útil para la comunidad de coleccionistas manteniendo una filosofía abierta, comunitaria y libre.

## Licencia

Truequing se distribuye bajo licencia GNU AGPLv3.

Ver el archivo LICENSE para más información.
## Licencia




